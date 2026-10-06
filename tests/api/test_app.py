import json

import pytest
from fastapi.testclient import TestClient
from qdrant_client import QdrantClient

from vantage.api.app import create_app
from vantage.corpus.model import AccessLevel, Chunk, Portee
from vantage.rag.generation import REFUS
from vantage.rag.index import CorpusIndex

from fakes import HashingEmbedder, RecordingChat

CHUNKS = [
    Chunk("ai-act", "AI Act, Article 6, §2", Portee.CONTRAIGNANT, AccessLevel.PUBLIC, "Classification",
          "Les systèmes d'IA visés à l'annexe III sont à haut risque."),
    Chunk("VAS-1", "VAS-1, page 1 — Procédure", Portee.POLITIQUE_INTERNE, AccessLevel.INTERNE, "Procédure",
          "Le comité IA valide les systèmes à haut risque. CANARI-TEST-1"),
    Chunk("VAS-2", "VAS-2, page 1 — Dossier", Portee.POLITIQUE_INTERNE, AccessLevel.CONFIDENTIEL, "Dossier",
          "Le PROJET-TEST a échoué sur les systèmes à haut risque."),
]


def _client(model=None):
    index = CorpusIndex(QdrantClient(":memory:"), HashingEmbedder())
    index.build(CHUNKS)
    return TestClient(create_app(index, model or RecordingChat()))


def _events(response):
    events = []
    for block in response.text.strip().split("\n\n"):
        name, data = block.split("\n")
        events.append((name.removeprefix("event: "), json.loads(data.removeprefix("data: "))))
    return events


def test_roles_lists_each_role_with_its_levels():
    with _client() as client:
        roles = client.get("/api/roles").json()
    assert roles == [
        {"id": "Employé", "levels": ["public"]},
        {"id": "Manager", "levels": ["public", "interne"]},
        {"id": "Conformité", "levels": ["public", "interne", "confidentiel"]},
    ]


@pytest.mark.parametrize(
    ("role", "visible"),
    [
        ("Employé", {"public"}),
        ("Manager", {"public", "interne"}),
        ("Conformité", {"public", "interne", "confidentiel"}),
    ],
)
def test_chat_streams_sources_within_the_role_then_the_answer(role, visible):
    with _client() as client:
        response = client.post("/api/chat", json={"role": role, "question": "systèmes à haut risque"})
    assert response.headers["content-type"].startswith("text/event-stream")
    events = _events(response)
    names = [name for name, _ in events]
    assert names[0] == "sources" and names[-1] == "done" and "token" in names
    assert {source["access_level"] for source in events[0][1]} == visible
    answer = "".join(data for name, data in events if name == "token")
    assert answer.strip() == "Réponse [AI Act, Article 6, §2]"
    assert events[-1] == ("done", {"refus": False})


def test_unknown_role_is_rejected():
    with _client() as client:
        assert client.post("/api/chat", json={"role": "Admin", "question": "?"}).status_code == 422


def test_nothing_retrieved_streams_the_refus():
    index = CorpusIndex(QdrantClient(":memory:"), HashingEmbedder())
    index.build([])
    with TestClient(create_app(index, RecordingChat())) as client:
        events = _events(client.post("/api/chat", json={"role": "Employé", "question": "?"}))
    assert events == [("sources", []), ("token", REFUS), ("done", {"refus": True})]


def test_model_failure_is_reported_in_the_stream():
    with _client(RecordingChat(fail=True)) as client:
        events = _events(client.post("/api/chat", json={"role": "Employé", "question": "haut risque"}))
    assert [name for name, _ in events] == ["sources", "error", "done"]
