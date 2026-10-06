"""The Corpus in Qdrant, searched within a Rôle's scope.

Every search is filtered by Niveau d'accès inside Qdrant itself, so a Chunk
above the Rôle's level is never even returned. The only way to search without
that filter is to build the index with `access_filter=False`, which exists
solely for the Évaluation témoin.
"""

import uuid
import warnings
from collections.abc import Iterable
from dataclasses import dataclass

from qdrant_client import QdrantClient, models

from vantage.access import Role
from vantage.corpus.model import AccessLevel, Chunk, Portee
from vantage.rag.embedding import Embedder, chunk_text_for_embedding

COLLECTION = "corpus"
_BATCH = 64


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: float


class CorpusIndex:
    def __init__(
        self,
        client: QdrantClient,
        embedder: Embedder,
        collection: str = COLLECTION,
        *,
        access_filter: bool = True,
    ):
        self._client = client
        self._embedder = embedder
        self._collection = collection
        self._access_filter = access_filter

    def build(self, chunks: Iterable[Chunk]) -> int:
        """Replace the collection with these Chunks; returns how many were indexed."""
        if self._client.collection_exists(self._collection):
            self._client.delete_collection(self._collection)
        self._client.create_collection(
            self._collection,
            vectors_config=models.VectorParams(size=self._embedder.dimension, distance=models.Distance.COSINE),
        )
        with warnings.catch_warnings():  # local Qdrant ignores payload indexes; Docker Qdrant uses it
            warnings.simplefilter("ignore", UserWarning)
            self._client.create_payload_index(self._collection, "access_level", models.PayloadSchemaType.KEYWORD)
        chunks = list(chunks)
        for start in range(0, len(chunks), _BATCH):
            batch = chunks[start : start + _BATCH]
            vectors = self._embedder.embed([chunk_text_for_embedding(c) for c in batch])
            self._client.upsert(
                self._collection,
                points=[
                    models.PointStruct(id=_point_id(chunk), vector=vector, payload=chunk.to_dict())
                    for chunk, vector in zip(batch, vectors)
                ],
            )
        return len(chunks)

    def search(self, question: str, role: Role, limit: int = 5) -> list[ScoredChunk]:
        """The `limit` Chunks closest to the question among those the Rôle may see."""
        [vector] = self._embedder.embed([question])
        response = self._client.query_points(
            self._collection,
            query=vector,
            query_filter=self._scope(role),
            limit=limit,
            with_payload=True,
        )
        return [ScoredChunk(_chunk_from_payload(point.payload), point.score) for point in response.points]

    def _scope(self, role: Role) -> models.Filter | None:
        if not self._access_filter:
            return None
        levels = [level.value for level in role.visible_levels]
        return models.Filter(must=[models.FieldCondition(key="access_level", match=models.MatchAny(any=levels))])


def _point_id(chunk: Chunk) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{chunk.document_id}|{chunk.reference}"))


def _chunk_from_payload(payload: dict) -> Chunk:
    return Chunk(
        document_id=payload["document_id"],
        reference=payload["reference"],
        portee=Portee(payload["portee"]),
        access_level=AccessLevel(payload["access_level"]),
        heading=payload["heading"],
        text=payload["text"],
    )
