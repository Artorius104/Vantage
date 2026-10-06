"""Answer generation from retrieved Chunks only, with their Références.

Both the Mistral API and Ollama expose an OpenAI-compatible chat endpoint, so
one small client serves the reference model and the local dev model (ADR 0007).
"""

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Protocol

import httpx

from vantage.rag.index import ScoredChunk

REFUS = "Je ne trouve pas d'information permettant de répondre à cette question dans les documents auxquels vous avez accès."

SYSTEM_PROMPT = f"""Tu es Vantage, l'assistant documentaire de Vantage Aerospace Systems.
Réponds en français, uniquement à partir des extraits fournis. N'utilise jamais tes connaissances générales, même pour compléter.
Après chaque affirmation, cite entre crochets la Référence exacte de l'extrait qui la justifie, par exemple [AI Act, Article 6, §2].
Si les extraits ne permettent pas de répondre, réponds exactement et uniquement : {REFUS}"""


class ChatModel(Protocol):
    def complete(self, system: str, user: str) -> str: ...

    def stream(self, system: str, user: str) -> Iterator[str]:
        """The answer as successive text pieces."""
        ...


@dataclass(frozen=True)
class OpenAICompatibleChat:
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


def reference_model() -> OpenAICompatibleChat:
    """Mistral Small through the Mistral API: the only model behind published numbers."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is not set")
    return OpenAICompatibleChat("https://api.mistral.ai/v1", os.environ.get("VANTAGE_MISTRAL_MODEL", "mistral-small-latest"), api_key)


def dev_model() -> OpenAICompatibleChat:
    """Ministral 8B through a local Ollama, for free iteration only."""
    return OpenAICompatibleChat(
        os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/v1",
        os.environ.get("VANTAGE_OLLAMA_MODEL", "ministral-3:8b"),
    )


def model_from_env() -> OpenAICompatibleChat:
    """VANTAGE_LLM=mistral selects the reference model; anything else, the local dev model."""
    return reference_model() if os.environ.get("VANTAGE_LLM", "ollama") == "mistral" else dev_model()


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
    return Answer(model.complete(SYSTEM_PROMPT, _user_prompt(question, retrieved)), tuple(retrieved))


def stream_answer(question: str, retrieved: list[ScoredChunk], model: ChatModel) -> Iterator[str]:
    """Same contract as `answer`, delivered piece by piece."""
    if not retrieved:
        yield REFUS
        return
    yield from model.stream(SYSTEM_PROMPT, _user_prompt(question, retrieved))


def _user_prompt(question: str, retrieved: list[ScoredChunk]) -> str:
    extracts = "\n\n".join(
        f"[{scored.chunk.reference}]\n{scored.chunk.heading}\n{scored.chunk.text}" for scored in retrieved
    )
    return f"Extraits :\n\n{extracts}\n\nQuestion : {question}"
