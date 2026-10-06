import hashlib
import math
import re

import pytest
from qdrant_client import QdrantClient

from vantage.access import Role
from vantage.corpus import load_corpus
from vantage.corpus.model import AccessLevel
from vantage.rag.generation import REFUS, SYSTEM_PROMPT, answer
from vantage.rag.index import CorpusIndex


class HashingEmbedder:
    """A deterministic bag-of-words stand-in for bge-m3: identical texts get identical vectors."""

    dimension = 512

    def embed(self, texts):
        vectors = []
        for text in texts:
            vector = [0.0] * self.dimension
            for word in re.findall(r"\w+", text.lower()):
                vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dimension] += 1.0
            norm = math.sqrt(sum(v * v for v in vector)) or 1.0
            vectors.append([v / norm for v in vector])
        return vectors


class RecordingChat:
    def __init__(self, reply="Réponse [AI Act, Article 6, §2]"):
        self.reply = reply
        self.calls = []

    def complete(self, system, user):
        self.calls.append((system, user))
        return self.reply


@pytest.fixture(scope="module")
def corpus():
    return load_corpus()


def _index(corpus, *, access_filter=True):
    index = CorpusIndex(QdrantClient(":memory:"), HashingEmbedder(), access_filter=access_filter)
    index.build(corpus)
    return index


@pytest.fixture(scope="module")
def index(corpus):
    return _index(corpus)


@pytest.fixture(scope="module")
def internal_chunks(corpus):
    return [c for c in corpus if c.access_level is not AccessLevel.PUBLIC]


def test_role_ladder():
    assert Role.EMPLOYE.visible_levels == (AccessLevel.PUBLIC,)
    assert Role.MANAGER.visible_levels == (AccessLevel.PUBLIC, AccessLevel.INTERNE)
    assert Role.CONFORMITE.visible_levels == tuple(AccessLevel)


def test_corpus_holds_public_and_internal_chunks(corpus):
    levels = {c.access_level for c in corpus}
    assert levels == set(AccessLevel)


def test_employe_never_gets_internal_or_confidential_chunks(index, internal_chunks):
    # Each internal Chunk's own text is the strongest possible query for it.
    for chunk in internal_chunks:
        results = index.search(chunk.text, Role.EMPLOYE, limit=20)
        assert results
        assert all(r.chunk.access_level is AccessLevel.PUBLIC for r in results), chunk.reference


def test_manager_never_gets_confidential_chunks(index, internal_chunks):
    for chunk in internal_chunks:
        results = index.search(chunk.text, Role.MANAGER, limit=20)
        assert all(r.chunk.access_level is not AccessLevel.CONFIDENTIEL for r in results), chunk.reference


def test_each_role_finds_what_it_may_see(index, internal_chunks):
    for chunk in internal_chunks:
        allowed = [role for role in Role if chunk.access_level in role.visible_levels]
        for role in allowed:
            assert index.search(chunk.text, role, limit=1)[0].chunk == chunk


def test_unfiltered_index_for_evaluation_temoin_does_leak(corpus, internal_chunks):
    temoin = _index(corpus, access_filter=False)
    confidential = next(c for c in internal_chunks if c.access_level is AccessLevel.CONFIDENTIEL)
    assert temoin.search(confidential.text, Role.EMPLOYE, limit=1)[0].chunk == confidential


def test_answer_is_generated_from_the_retrieved_chunks_only(index):
    retrieved = index.search("systèmes d'IA à haut risque annexe III", Role.EMPLOYE, limit=3)
    chat = RecordingChat()
    result = answer("Quels systèmes sont à haut risque ?", retrieved, chat)
    [(system, user)] = chat.calls
    assert system == SYSTEM_PROMPT
    for scored in retrieved:
        assert f"[{scored.chunk.reference}]" in user
    assert result.text == chat.reply
    assert result.sources == tuple(retrieved)


def test_nothing_retrieved_gives_the_refus_without_calling_the_model():
    chat = RecordingChat()
    result = answer("Question", [], chat)
    assert result.is_refus and result.text == REFUS
    assert chat.calls == []
