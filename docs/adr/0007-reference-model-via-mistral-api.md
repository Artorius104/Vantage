# One reference model via the Mistral API; local Ministral 8B for development only

The original brief developed against a local Ollama model and switched to a paid API only for the final demo. The published numbers would then describe a different model than the one demoed: Routage, Décomposition, the generator's Refus gate and its obedience to "answer only from Chunks" all change with the model. So one **reference model**, Mistral Small via the Mistral API, runs every node (Routage, Reformulation, Décomposition, generation). Every published score and the demo use it. Ministral 8B runs locally through Ollama for free iteration during development; no number in the README comes from it. RAGAS uses a fixed judge that is stronger than the reference model and from another provider, identical for the baseline and the agentic runs.

## Considered Options

- **Mistral Small locally** — about 14 GB at Q4, which doesn't fit the 8 GB of an RTX 4060; partial CPU offload is too slow for hundreds of evaluation runs.
- **Ministral 8B as the reference model** — fits in VRAM, but structured output (Routage, Décomposition) and grounding are markedly less reliable.

## Consequences

- The Fuite metrics need no judge (ADR 0001) and depend only on the reference model.
- Optional extension, first to go after everything ADR 0006 never cuts: re-run the Fuite and RAGAS evaluations with Ministral 8B and publish them as a separate column.
