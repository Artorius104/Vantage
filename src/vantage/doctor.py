"""Check that every feature of Vantage is ready to run, and fix what can be fixed.

    python -m vantage.doctor          # report; exit 1 if something blocking is missing
    python -m vantage.doctor --fix    # also restore sources, build the index, install web deps

Run it through `./vantage check` or `./vantage start` (see README).
"""

import argparse
import os
import shutil
import socket
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import find_dotenv, load_dotenv

WEB_DIR = Path("web")


@dataclass(frozen=True)
class Result:
    name: str
    ok: bool
    detail: str
    blocking: bool = True  # a non-blocking failure is a warning: Vantage still runs
    fix: Callable[[], None] | None = None  # how --fix repairs it, when it can


def check_sources() -> Result:
    from vantage.corpus.sources import load_manifest, restore

    files = load_manifest()
    missing = [f for f in files if not f.is_present()]

    def restore_missing():
        for file in missing:
            restore(file)
            print(f"    restauré : {file.path}", flush=True)

    if missing:
        return Result("Sources brutes", False, f"{len(missing)}/{len(files)} fichiers manquants", fix=restore_missing)
    return Result("Sources brutes", True, f"{len(files)} fichiers présents")


def check_corpus() -> tuple[Result, int]:
    from vantage.corpus import load_corpus
    from vantage.corpus.model import AccessLevel

    try:
        chunks = load_corpus()
    except Exception as error:
        return Result("Corpus", False, f"ingestion impossible : {error}"), 0
    counts = {level: sum(c.access_level is level for c in chunks) for level in AccessLevel}
    detail = f"{len(chunks)} Chunks (" + ", ".join(f"{n} {level}" for level, n in counts.items()) + ")"
    return Result("Corpus", all(counts.values()), detail), len(chunks)


def check_index(expected: int, client_factory=None) -> Result:
    from vantage.rag.index import COLLECTION, qdrant_client_from_env

    def rebuild():
        _run([sys.executable, "-m", "vantage.rag", "index"], "construction de l'index")

    try:
        client = (client_factory or qdrant_client_from_env)()
    except Exception as error:
        detail = "stockage local verrouillé : l'API tourne-t-elle déjà ?" if "already accessed" in str(error) else str(error)
        return Result("Index Qdrant", False, detail)
    try:
        if not client.collection_exists(COLLECTION):
            return Result("Index Qdrant", False, "collection absente", fix=rebuild)
        count = client.count(COLLECTION).count
    finally:
        client.close()
    if count != expected:
        return Result("Index Qdrant", False, f"{count} points indexés pour {expected} Chunks : index périmé", fix=rebuild)
    where = os.environ.get("QDRANT_URL", "local (data/qdrant)")
    return Result("Index Qdrant", True, f"{count} points · {where}")


def check_llm() -> Result:
    """The model answers will come from: Claude Haiku (reference) unless VANTAGE_LLM=ollama."""
    if os.environ.get("VANTAGE_LLM", "claude") == "ollama":
        return check_ollama(blocking=True)
    return check_claude()


def check_claude() -> Result:
    import anthropic

    from vantage.rag.generation import REFERENCE_MODEL

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return Result("LLM", False, "ANTHROPIC_API_KEY absente (à mettre dans .env)")
    try:
        anthropic.Anthropic(max_retries=0, timeout=10).models.retrieve(REFERENCE_MODEL)
    except anthropic.AuthenticationError:
        return Result("LLM", False, "clé Anthropic refusée (ANTHROPIC_API_KEY)")
    except anthropic.PermissionDeniedError:
        return Result("LLM", False, f"la clé n'a pas accès à {REFERENCE_MODEL}")
    except anthropic.APIConnectionError:
        return Result("LLM", False, "API Anthropic injoignable (réseau)")
    except anthropic.APIStatusError as error:
        return Result("LLM", False, f"API Anthropic : erreur {error.status_code}")
    return Result("LLM", True, f"API Anthropic · {REFERENCE_MODEL} (modèle de référence)")


def check_ollama(*, blocking: bool) -> Result:
    from vantage.rag.generation import dev_model

    name = "LLM" if blocking else "LLM de dev"
    model = dev_model()
    base = model.base_url.removesuffix("/v1")
    try:
        tags = httpx.get(f"{base}/api/tags", timeout=5).json()
    except httpx.HTTPError:
        return Result(name, False, f"Ollama injoignable sur {base} (systemctl status ollama)", blocking=blocking)
    names = {m["name"] for m in tags.get("models", [])}
    if model.model not in names:
        return Result(name, False, f"modèle {model.model} absent d'Ollama (ollama pull {model.model})", blocking=blocking)
    return Result(name, True, f"Ollama · {model.model} (développement, --llm ollama)", blocking=blocking)


def check_gpu() -> Result:
    try:
        import torch
    except ImportError:
        return Result("GPU", False, "torch absent", blocking=False)
    if torch.cuda.is_available():
        return Result("GPU", True, torch.cuda.get_device_name(0), blocking=False)
    return Result("GPU", False, "CUDA indisponible : embeddings sur CPU, plus lents", blocking=False)


def check_web() -> Result:
    if not shutil.which("npm"):
        return Result("Interface web", False, "npm introuvable (Node.js 20+ requis)")
    if not (WEB_DIR / "node_modules").is_dir():
        return Result("Interface web", False, "dépendances non installées",
                      fix=lambda: _run(["npm", "--prefix", str(WEB_DIR), "install"], "npm install"))
    return Result("Interface web", True, "dépendances installées")


def check_port(port: int, name: str) -> Result:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        busy = sock.connect_ex(("127.0.0.1", port)) == 0
    if busy:
        return Result(f"Port {port}", False, f"déjà utilisé : {name} tourne-t-il déjà ?")
    return Result(f"Port {port}", True, f"libre pour {name}")


def run_checks(*, fix: bool, ports: dict[int, str]) -> list[Result]:
    """Every check, in dependency order; with `fix`, a fixable failure is repaired then re-checked."""
    results: list[Result] = []

    def add(result: Result, recheck: Callable[[], Result]) -> None:
        if fix and not result.ok and result.fix is not None:
            print(f"  → réparation : {result.name} ({result.detail})", flush=True)
            result.fix()
            result = recheck()
        results.append(result)

    add(check_sources(), check_sources)
    corpus, chunk_count = check_corpus()
    results.append(corpus)
    if corpus.ok:
        add(check_index(chunk_count), lambda: check_index(chunk_count))
    else:
        results.append(Result("Index Qdrant", False, "non vérifié : corpus invalide"))
    results.append(check_llm())
    if os.environ.get("VANTAGE_LLM", "claude") != "ollama":
        results.append(check_ollama(blocking=False))  # optional: only needed for --llm ollama
    results.append(check_gpu())
    add(check_web(), check_web)
    results += [check_port(port, name) for port, name in ports.items()]
    return results


def _run(command: list[str], what: str) -> None:
    _require(subprocess.run(command).returncode == 0, what)


def _require(ok: bool, what: str) -> None:
    if not ok:
        raise SystemExit(f"échec : {what}")


def report(results: list[Result]) -> bool:
    width = max(len(r.name) for r in results)
    for r in results:
        mark = "✓" if r.ok else ("✗" if r.blocking else "!")
        print(f"  {mark} {r.name:<{width}}  {r.detail}")
    return all(r.ok or not r.blocking for r in results)


def main(argv: list[str] | None = None) -> int:
    load_dotenv(find_dotenv(usecwd=True))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fix", action="store_true", help="restore sources, build the index, install web deps")
    parser.add_argument("--api-port", type=int, default=int(os.environ.get("API_PORT", 8000)))
    parser.add_argument("--web-port", type=int, default=int(os.environ.get("WEB_PORT", 3000)))
    parser.add_argument("--no-ports", action="store_true", help="skip the free-port checks")
    args = parser.parse_args(argv)
    ports = {} if args.no_ports else {args.api_port: "l'API", args.web_port: "l'interface web"}
    return 0 if report(run_checks(fix=args.fix, ports=ports)) else 1


if __name__ == "__main__":
    sys.exit(main())
