# One reference model, Claude Haiku 4.5; local Ministral 8B for development only

The original brief developed against a local Ollama model and switched to a paid API only for the final demo. The published numbers would then describe a different model than the one demoed: Routage, Décomposition, the generator's Refus gate and its obedience to "answer only from Chunks" all change with the model. So one **reference model**, Claude Haiku 4.5 (`claude-haiku-4-5`) through the Anthropic API, runs every node (Routage, Reformulation, Décomposition, generation). Every published score and the demo use it. Ministral 8B runs locally through Ollama for free iteration during development (`--llm ollama`); no number in the README comes from it.

## Status

Accepted. Revised on 2026-10-10: the reference model was first Mistral Small through the Mistral API. It became Claude Haiku 4.5, the model the project has API access to, before any number had been published. The judge rule below was relaxed at the same time.

## Considered Options

- **Mistral Small via the Mistral API**: the first choice, in the same family as the dev model. Replaced before any measurement.
- **Mistral Small locally**: about 14 GB at Q4, which doesn't fit the 8 GB of an RTX 4060. Partial CPU offload is too slow for hundreds of evaluation runs.
- **Ministral 8B as the reference model**: fits in VRAM, but structured output (Routage, Décomposition) and grounding are markedly less reliable.

## Consequences

- The Fuite metrics need no judge (ADR 0001) and depend only on the reference model.
- The RAGAS judge is still to be chosen (#10). The original rule (stronger than the reference model, from another provider) can't hold while Haiku is the only model in use. Either Haiku judges itself, with that bias documented, or a stronger Claude model is made an exception for judging only.
- The Refus must be word for word the same for every Rôle. Haiku tends to append an explanation after it, and that explanation differs from one Rôle to another. So the code, not the prompt, guarantees it: an answer that opens with the Refus is cut to the fixed wording, in streaming too.
- Haiku still sometimes invents a sub-reference (`[AI Act, Annexe III, point 4.a]`) despite the prompt. Citations need a check in code (planned).
- Optional extension, first to go after everything ADR 0006 never cuts: re-run the Fuite and RAGAS evaluations with Ministral 8B and publish them as a separate column.
