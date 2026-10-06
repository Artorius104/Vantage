from vantage.corpus.ai_act import load_ai_act
from vantage.corpus.internal_documents import load_internal_documents
from vantage.corpus.model import Chunk


def load_corpus() -> list[Chunk]:
    """Every Chunk ingested so far, public and internal."""
    internal = [chunk for document in load_internal_documents() for chunk in document.chunks]
    return load_ai_act() + internal
