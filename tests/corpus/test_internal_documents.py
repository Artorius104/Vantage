from collections import Counter
from pathlib import Path

import pytest

from vantage.corpus.internal_documents import load_internal_documents, parse_document
from vantage.corpus.model import AccessLevel, Portee

PUBLIC_SOURCES = ["ai-act", "reg-376-2014", "rgpd", "nis2", "cnil"]


@pytest.fixture(scope="module")
def documents():
    return load_internal_documents()


def test_eleven_documents_on_two_levels(documents):
    levels = Counter(d.access_level for d in documents)
    assert levels == {AccessLevel.INTERNE: 9, AccessLevel.CONFIDENTIEL: 2}
    assert sum(len(d.chunks) for d in documents) == 53


def test_every_chunk_inherits_its_documents_level(documents):
    for document in documents:
        for chunk in document.chunks:
            assert chunk.document_id == document.document_id
            assert chunk.access_level is document.access_level
            assert chunk.portee is Portee.POLITIQUE_INTERNE


def test_every_chunk_carries_one_of_its_documents_canaries(documents):
    for document in documents:
        assert document.canaries
        for chunk in document.chunks:
            assert any(canary in chunk.text for canary in document.canaries), chunk.reference


def test_canaries_belong_to_a_single_document_and_never_appear_in_public_sources(documents):
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for source in PUBLIC_SOURCES
        for path in Path("data/raw", source).iterdir()
    )
    for document in documents:
        others = "\n".join(c.text for d in documents if d is not document for c in d.chunks)
        for canary in document.canaries:
            assert canary not in others, f"{canary} also appears outside {document.document_id}"
            assert canary not in public_text, f"{canary} appears in a public source"


def test_reference_names_document_page_and_section_title(documents):
    references = [c.reference for d in documents for c in d.chunks]
    assert len(references) == len(set(references))
    assert "VAS-PRO-SAF-030, page 2 — Triage et obligations externes" in references


def test_markup_and_preamble_are_dropped(documents):
    for chunk in (c for d in documents for c in d.chunks):
        assert "page-break" not in chunk.text
        assert "**" not in chunk.text
        assert "Document entièrement fictif" not in chunk.text


def _markdown(level):
    return (
        "---\ndocument_id: X-1\ntitre: Note\nniveau_acces: "
        + level
        + "\nportee: politique_interne\nfaits_canaris: [CANARI-X]\n---\n\n# Note\n\n## Page 1/1 — Seule\n\nTexte CANARI-X.\n"
    )


def test_an_internal_document_cannot_be_public():
    with pytest.raises(ValueError, match="cannot be public"):
        parse_document(_markdown("public"))


def test_front_matter_level_must_match_the_manifest(tmp_path):
    (tmp_path / "note.md").write_text(_markdown("confidentiel"), encoding="utf-8")
    (tmp_path / "manifest.yaml").write_text(
        "documents:\n  - {id: X-1, fichier: note.md, niveau: interne}\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="!= manifest interne"):
        load_internal_documents(tmp_path)
