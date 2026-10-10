import pytest
from qdrant_client import QdrantClient

from vantage.access import Role
from vantage.corpus import load_corpus
from vantage.corpus.model import AccessLevel
from vantage.rag.generation import REFUS, SYSTEM_PROMPT, answer, stream_answer
from vantage.rag.index import CorpusIndex

from fakes import HashingEmbedder, RecordingChat


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


class StreamingChat:
    def __init__(self, pieces):
        self.pieces = pieces

    def complete(self, system, user):
        return "".join(self.pieces)

    def stream(self, system, user):
        yield from self.pieces


def _one_chunk(index):
    return index.search("systèmes d'IA à haut risque", Role.EMPLOYE, limit=1)


def test_refus_followed_by_an_explanation_is_cut_to_the_fixed_wording(index):
    head = "Je ne trouve pas d’information permettant"  # typographic apostrophe, as models often write it
    pieces = ["Je ne trouve pas d", head[18:], REFUS[len(head):], "\n\nLes extraits fournis concernent l'AI Act."]
    retrieved = _one_chunk(index)
    assert "".join(stream_answer("q", retrieved, StreamingChat(pieces))) == REFUS
    assert answer("q", retrieved, StreamingChat(pieces)).text == REFUS


def test_ordinary_answer_streams_through_unchanged(index):
    pieces = ["Je ", "ne peux ", "que citer [AI Act, Article 6, §2]."]
    assert "".join(stream_answer("q", _one_chunk(index), StreamingChat(pieces))) == "Je ne peux que citer [AI Act, Article 6, §2]."
