import socket

from qdrant_client import QdrantClient

from vantage import doctor
from vantage.corpus.model import AccessLevel, Chunk, Portee
from vantage.rag.index import CorpusIndex

from fakes import HashingEmbedder

CHUNK = Chunk("ai-act", "AI Act, Article 6, §2", Portee.CONTRAIGNANT, AccessLevel.PUBLIC, "", "Texte.")


def _client_with(chunks):
    client = QdrantClient(":memory:")
    if chunks is not None:
        CorpusIndex(client, HashingEmbedder()).build(chunks)
    return lambda: client


def test_missing_index_is_fixable():
    result = doctor.check_index(1, _client_with(None))
    assert not result.ok and result.fix is not None
    assert "absente" in result.detail


def test_stale_index_is_fixable():
    result = doctor.check_index(2, _client_with([CHUNK]))
    assert not result.ok and result.fix is not None
    assert "périmé" in result.detail


def test_index_matching_the_corpus_is_ok():
    assert doctor.check_index(1, _client_with([CHUNK])).ok


def test_corpus_of_the_repo_has_every_level():
    result, count = doctor.check_corpus()
    assert result.ok and count > 0


def test_unreachable_ollama_blocks(monkeypatch):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]  # bound but not listening: connection refused
        monkeypatch.setenv("OLLAMA_URL", f"http://127.0.0.1:{port}")
        monkeypatch.setenv("VANTAGE_LLM", "ollama")
        result = doctor.check_llm()
    assert not result.ok and result.blocking and "injoignable" in result.detail


def test_reference_model_without_key_blocks(monkeypatch):
    monkeypatch.delenv("VANTAGE_LLM", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = doctor.check_llm()
    assert not result.ok and result.blocking and "ANTHROPIC_API_KEY" in result.detail


def test_missing_dev_model_only_warns(monkeypatch):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        monkeypatch.setenv("OLLAMA_URL", f"http://127.0.0.1:{sock.getsockname()[1]}")
        result = doctor.check_ollama(blocking=False)
    assert not result.ok and not result.blocking


def test_busy_port_is_reported():
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen()
        assert not doctor.check_port(server.getsockname()[1], "l'API").ok


def test_warnings_do_not_block_but_failures_do(capsys):
    warning = doctor.Result("GPU", False, "CPU", blocking=False)
    assert doctor.report([doctor.Result("Corpus", True, "ok"), warning])
    assert not doctor.report([doctor.Result("LLM", False, "absent")])
    assert "!" in capsys.readouterr().out
