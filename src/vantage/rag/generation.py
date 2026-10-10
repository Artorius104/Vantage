"""Answer generation from retrieved Chunks only, with their Références.

The reference model is Claude Haiku 4.5, called through the Anthropic SDK
(ADR 0007): every published number and the demo come from it. Ministral 8B,
served by a local Ollama through its OpenAI-compatible endpoint, is kept for
free iteration during development only.
"""

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Protocol

import anthropic
import httpx

from vantage.rag.index import ScoredChunk

REFERENCE_MODEL = "claude-haiku-4-5"
MAX_TOKENS = 16000

REFUS = "Je ne trouve pas d'information permettant de répondre à cette question dans les documents auxquels vous avez accès."

SYSTEM_PROMPT = f"""Tu es Vantage, l'assistant documentaire de Vantage Aerospace Systems.
Réponds en français, uniquement à partir des extraits fournis. N'utilise jamais tes connaissances générales, même pour compléter.
Après chaque affirmation, cite entre crochets la Référence de l'extrait qui la justifie, recopiée caractère pour caractère depuis l'en-tête de cet extrait, par exemple [AI Act, Article 6, §2]. N'invente, n'abrège et ne complète jamais une Référence.
Si les extraits ne permettent pas de répondre, réponds exactement et uniquement : {REFUS}
Dans ce cas, n'ajoute aucune explication ni aucune autre phrase."""


class ChatModel(Protocol):
    def complete(self, system: str, user: str) -> str: ...

    def stream(self, system: str, user: str) -> Iterator[str]:
        """The answer as successive text pieces."""
        ...


@dataclass
class ClaudeChat:
    """Claude through the Anthropic SDK; the key comes from ANTHROPIC_API_KEY."""

    model: str = REFERENCE_MODEL
    client: anthropic.Anthropic = field(default_factory=anthropic.Anthropic)

    def complete(self, system: str, user: str) -> str:
        response = self.client.messages.create(**self._request(system, user))
        return "".join(block.text for block in response.content if block.type == "text").strip()

    def stream(self, system: str, user: str) -> Iterator[str]:
        with self.client.messages.stream(**self._request(system, user)) as stream:
            yield from stream.text_stream

    def _request(self, system: str, user: str) -> dict:
        return {
            "model": self.model,
            "max_tokens": MAX_TOKENS,
            # SDK 1.x dropped the sampling keyword arguments; Haiku 4.5 still honours
            # temperature, and reproducible measurements depend on it.
            "extra_body": {"temperature": 0},
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }


@dataclass(frozen=True)
class OpenAICompatibleChat:
    """An OpenAI-compatible chat endpoint; used for Ollama."""

    base_url: str
    model: str
    api_key: str | None = None
    timeout: float = 120.0

    def complete(self, system: str, user: str) -> str:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=self._headers(),
            json=self._body(system, user, stream=False),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def stream(self, system: str, user: str) -> Iterator[str]:
        with httpx.stream(
            "POST",
            f"{self.base_url}/chat/completions",
            headers=self._headers(),
            json=self._body(system, user, stream=True),
            timeout=self.timeout,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith("data: ") or line == "data: [DONE]":
                    continue
                delta = json.loads(line.removeprefix("data: "))["choices"][0]["delta"].get("content")
                if delta:
                    yield delta

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def _body(self, system: str, user: str, *, stream: bool) -> dict:
        return {
            "model": self.model,
            "temperature": 0,
            "stream": stream,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }


def reference_model() -> ClaudeChat:
    """Claude Haiku 4.5: the only model behind published numbers."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY is not set (put it in .env)")
    return ClaudeChat()


def dev_model() -> OpenAICompatibleChat:
    """Ministral 8B through a local Ollama, for free iteration only."""
    return OpenAICompatibleChat(
        os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/v1",
        os.environ.get("VANTAGE_OLLAMA_MODEL", "ministral-3:8b"),
    )


def model_from_env() -> ChatModel:
    """VANTAGE_LLM=ollama selects the local dev model; otherwise the reference model."""
    return dev_model() if os.environ.get("VANTAGE_LLM", "claude") == "ollama" else reference_model()


@dataclass(frozen=True)
class Answer:
    text: str
    sources: tuple[ScoredChunk, ...]

    @property
    def is_refus(self) -> bool:
        return self.text == REFUS


def answer(question: str, retrieved: list[ScoredChunk], model: ChatModel) -> Answer:
    """Generate from the retrieved Chunks; with nothing retrieved, the Refus without asking the model."""
    if not retrieved:
        return Answer(REFUS, ())
    text = model.complete(SYSTEM_PROMPT, _user_prompt(question, retrieved))
    return Answer(REFUS if _starts_with_refus(text) else text, tuple(retrieved))


def stream_answer(question: str, retrieved: list[ScoredChunk], model: ChatModel) -> Iterator[str]:
    """Same contract as `answer`, delivered piece by piece.

    The Refus must be word for word the same for every Rôle, so whatever a model
    adds after it is cut here, in code: the opening is held back until it either
    proves to be the Refus (then only the fixed wording is sent) or diverges from it.
    """
    if not retrieved:
        yield REFUS
        return
    held = ""
    for piece in model.stream(SYSTEM_PROMPT, _user_prompt(question, retrieved)):
        if held is None:
            yield piece
            continue
        held += piece
        if _starts_with_refus(held):
            yield REFUS
            return
        if not _normalise(REFUS).startswith(_normalise(held.lstrip())):
            yield held
            held = None
    if held:
        yield held


def _starts_with_refus(text: str) -> bool:
    return _normalise(text.lstrip()).startswith(_normalise(REFUS))


def _normalise(text: str) -> str:
    return text.replace("\u2019", "'")


def _user_prompt(question: str, retrieved: list[ScoredChunk]) -> str:
    extracts = "\n\n".join(
        f"[{scored.chunk.reference}]\n{scored.chunk.heading}\n{scored.chunk.text}" for scored in retrieved
    )
    return f"Extraits :\n\n{extracts}\n\nQuestion : {question}"
