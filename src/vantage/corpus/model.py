"""Corpus vocabulary shared by every ingester (see CONTEXT.md)."""

from dataclasses import asdict, dataclass
from enum import StrEnum


class AccessLevel(StrEnum):
    """Niveau d'accès: a strict ladder, each tier includes everything below it."""

    PUBLIC = "public"
    INTERNE = "interne"
    CONFIDENTIEL = "confidentiel"


class Portee(StrEnum):
    """The legal weight of a Chunk."""

    CONTRAIGNANT = "contraignant"
    INTERPRETATIF = "interprétatif"
    POLITIQUE_INTERNE = "politique interne"


@dataclass(frozen=True)
class Chunk:
    """A passage lying entirely within one structural unit of a Document.

    `access_level` is always the Document's; it is never set per Chunk.
    `heading` is the title of the enclosing article, annex or section, kept
    apart from `text` so callers decide how to combine them.
    """

    document_id: str
    reference: str
    portee: Portee
    access_level: AccessLevel
    heading: str
    text: str

    def to_dict(self) -> dict:
        return asdict(self)
