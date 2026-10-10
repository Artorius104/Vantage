from contextlib import contextmanager
from types import SimpleNamespace

from vantage.rag.generation import REFERENCE_MODEL, ClaudeChat


class FakeMessages:
    def __init__(self):
        self.requests = []

    def create(self, **request):
        self.requests.append(request)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=" Réponse [AI Act, Article 6, §2] ")])

    @contextmanager
    def stream(self, **request):
        self.requests.append(request)
        yield SimpleNamespace(text_stream=iter(["Ré", "ponse"]))


def _chat():
    messages = FakeMessages()
    return ClaudeChat(client=SimpleNamespace(messages=messages)), messages


def test_reference_model_is_haiku():
    assert REFERENCE_MODEL == "claude-haiku-4-5"


def test_request_carries_system_prompt_question_and_deterministic_sampling():
    chat, messages = _chat()
    assert chat.complete("consignes", "question") == "Réponse [AI Act, Article 6, §2]"
    [request] = messages.requests
    assert request["model"] == "claude-haiku-4-5"
    assert request["system"] == "consignes"
    assert request["messages"] == [{"role": "user", "content": "question"}]
    assert request["extra_body"] == {"temperature": 0}


def test_stream_yields_text_pieces():
    chat, messages = _chat()
    assert list(chat.stream("consignes", "question")) == ["Ré", "ponse"]
    assert messages.requests[0]["model"] == "claude-haiku-4-5"
