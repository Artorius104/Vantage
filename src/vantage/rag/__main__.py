"""Index the Corpus, or ask a question as a Rôle.

    python -m vantage.rag index
    python -m vantage.rag ask --role Employé "Quel rôle approuve un risque résiduel A3 ?"
    python -m vantage.rag ask --role Manager --retrieve-only "..."   # no LLM call

Qdrant runs in Docker when QDRANT_URL is set (e.g. http://localhost:6333);
otherwise it uses a local on-disk store under data/qdrant/.
"""

import argparse
import os
import sys

from qdrant_client import QdrantClient

from vantage.access import Role
from vantage.corpus import load_corpus
from vantage.rag.embedding import BgeM3Embedder
from vantage.rag.generation import answer, dev_model, reference_model
from vantage.rag.index import CorpusIndex

LOCAL_STORE = "data/qdrant"


def _client() -> QdrantClient:
    url = os.environ.get("QDRANT_URL")
    return QdrantClient(url=url) if url else QdrantClient(path=LOCAL_STORE)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("index")
    ask = commands.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--role", type=Role, choices=list(Role), required=True)
    ask.add_argument("--limit", type=int, default=5)
    ask.add_argument("--llm", choices=["mistral", "ollama"], default="mistral")
    ask.add_argument("--retrieve-only", action="store_true")
    args = parser.parse_args(argv)

    index = CorpusIndex(_client(), BgeM3Embedder())
    if args.command == "index":
        print(f"{index.build(load_corpus())} Chunks indexed")
        return

    retrieved = index.search(args.question, args.role, args.limit)
    for scored in retrieved:
        print(f"{scored.score:.3f}  [{scored.chunk.access_level}] {scored.chunk.reference}", file=sys.stderr)
    if args.retrieve_only:
        return
    model = reference_model() if args.llm == "mistral" else dev_model()
    print(answer(args.question, retrieved, model).text)


if __name__ == "__main__":
    main()
