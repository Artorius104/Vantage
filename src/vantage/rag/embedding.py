"""Turning text into vectors. Indexing and search only depend on the Embedder protocol."""

from typing import Protocol

from vantage.corpus.model import Chunk

EMBEDDING_MODEL = "BAAI/bge-m3"  # ADR 0003


class Embedder(Protocol):
    dimension: int

    def embed(self, texts: list[str]) -> list[list[float]]:
        """One normalised vector per text."""
        ...


class BgeM3Embedder:
    """`BAAI/bge-m3` dense vectors, run locally (on the GPU when there is one)."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        from sentence_transformers import SentenceTransformer  # heavy import, only when used

        self._model = SentenceTransformer(model_name)
        self.dimension = self._model.get_embedding_dimension()

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, batch_size=16, normalize_embeddings=True, show_progress_bar=len(texts) > 64)
        return vectors.tolist()


def chunk_text_for_embedding(chunk: Chunk) -> str:
    """The Référence and heading go with the text, so "article 6" or a section title match too."""
    return "\n".join(part for part in (chunk.reference, chunk.heading, chunk.text) if part)
