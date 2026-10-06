"""HTTP API in front of the RAG pipeline, consumed by the web frontend.

    uvicorn vantage.api.app:app --reload        # http://localhost:8000

POST /api/chat answers as Server-Sent Events: one `sources` event with the
retrieved Chunks, then `token` events with the answer text, then `done`,
whose `refus` flag says whether the answer was the Refus.
The server keeps no Conversation: each question is answered on its own, within
the Rôle sent with it.
"""

import json
from collections.abc import Iterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from vantage.access import Role
from vantage.rag.generation import REFUS, ChatModel, stream_answer
from vantage.rag.index import CorpusIndex, ScoredChunk

RETRIEVAL_LIMIT = 5


class ChatRequest(BaseModel):
    role: Role
    question: str = Field(min_length=1, max_length=4000)


def create_app(index: CorpusIndex | None = None, model: ChatModel | None = None) -> FastAPI:
    """With no index or model given, the real ones are built at startup."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if index is None or model is None:
            from vantage.rag.embedding import BgeM3Embedder
            from vantage.rag.generation import model_from_env
            from vantage.rag.index import qdrant_client_from_env

            app.state.index = index or CorpusIndex(qdrant_client_from_env(), BgeM3Embedder())
            app.state.model = model or model_from_env()
        else:
            app.state.index, app.state.model = index, model
        yield

    app = FastAPI(title="Vantage", lifespan=lifespan)

    @app.get("/api/roles")
    def roles() -> list[dict]:
        return [
            {"id": role.value, "levels": [level.value for level in role.visible_levels]} for role in Role
        ]

    @app.post("/api/chat")
    def chat(request: ChatRequest) -> StreamingResponse:
        retrieved = app.state.index.search(request.question, request.role, RETRIEVAL_LIMIT)
        return StreamingResponse(
            _events(request.question, retrieved, app.state.model),
            media_type="text/event-stream",
            # Keep proxies (Next.js rewrites, nginx) from compressing or buffering the stream.
            headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"},
        )

    return app


def _events(question: str, retrieved: list[ScoredChunk], model: ChatModel) -> Iterator[str]:
    yield _event("sources", [_source(scored) for scored in retrieved])
    text = ""
    try:
        for piece in stream_answer(question, retrieved, model):
            text += piece
            yield _event("token", piece)
    except Exception as error:  # the stream has started; report instead of cutting it silently
        yield _event("error", f"Le modèle n'a pas pu répondre : {error}")
    yield _event("done", {"refus": text.strip() == REFUS})


def _source(scored: ScoredChunk) -> dict:
    return {**scored.chunk.to_dict(), "score": round(scored.score, 3)}


def _event(name: str, data) -> str:
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


app = create_app()
