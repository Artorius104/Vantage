"""Ingest the fictional internal Documents of Vantage Aerospace Systems.

Each Markdown file carries a YAML front matter (document_id, titre,
niveau_acces, portee, faits_canaris) and is cut into `## Page n/m — Title`
sections; each section is one Chunk. The Niveau d'accès comes only from the
front matter and must agree with the corpus manifest, so a Document can never
be indexed at the wrong level by accident.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from vantage.corpus.model import AccessLevel, Chunk, Portee

RAW_DIR = Path("data/raw/vantage-aerospace")  # restored by vantage.corpus.sources

_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_SECTION = re.compile(r"^## Page (\d+)/\d+ — (.+)$", re.MULTILINE)
_PAGE_BREAK = re.compile(r"<div[^>]*page-break[^>]*></div>")
_PORTEE = {"politique_interne": Portee.POLITIQUE_INTERNE}


@dataclass(frozen=True)
class InternalDocument:
    document_id: str
    title: str
    access_level: AccessLevel
    canaries: tuple[str, ...]
    chunks: tuple[Chunk, ...]


def parse_document(markdown: str) -> InternalDocument:
    match = _FRONT_MATTER.match(markdown)
    if not match:
        raise ValueError("missing YAML front matter")
    meta = yaml.safe_load(match.group(1))
    document_id = meta["document_id"]
    title = meta["titre"]
    access_level = AccessLevel(meta["niveau_acces"])
    if access_level is AccessLevel.PUBLIC:
        raise ValueError(f"{document_id}: an internal Document cannot be public")
    portee = _PORTEE[meta["portee"]]

    body = markdown[match.end():]
    headings = list(_SECTION.finditer(body))
    if not headings:
        raise ValueError(f"{document_id}: no '## Page' section")
    chunks = []
    for heading, following in zip(headings, headings[1:] + [None]):
        end = following.start() if following else len(body)
        text = _clean(body[heading.end():end])
        chunks.append(
            Chunk(
                document_id=document_id,
                reference=f"{document_id}, page {heading.group(1)} — {heading.group(2).strip()}",
                portee=portee,
                access_level=access_level,
                heading=title,
                text=text,
            )
        )
    return InternalDocument(
        document_id=document_id,
        title=title,
        access_level=access_level,
        canaries=tuple(meta.get("faits_canaris") or ()),
        chunks=tuple(chunks),
    )


def load_internal_documents(raw_dir: Path = RAW_DIR) -> list[InternalDocument]:
    """Every Document listed in the corpus manifest, checked against its front matter."""
    manifest = yaml.safe_load((raw_dir / "manifest.yaml").read_text(encoding="utf-8"))
    documents = []
    for entry in manifest["documents"]:
        document = parse_document((raw_dir / entry["fichier"]).read_text(encoding="utf-8"))
        if document.document_id != entry["id"]:
            raise ValueError(f"{entry['fichier']}: front matter id {document.document_id} != manifest {entry['id']}")
        if document.access_level != AccessLevel(entry["niveau"]):
            raise ValueError(
                f"{entry['id']}: front matter level {document.access_level} != manifest {entry['niveau']}"
            )
        documents.append(document)
    return documents


def _clean(text: str) -> str:
    text = _PAGE_BREAK.sub("", text).replace("**", "")
    return "\n".join(line.strip() for line in text.strip().splitlines() if line.strip())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["chunk"])
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    args = parser.parse_args(argv)
    for document in load_internal_documents(args.raw_dir):
        for chunk in document.chunks:
            sys.stdout.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
