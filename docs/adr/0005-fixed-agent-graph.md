# Fixed agent graph, not a free ReAct loop

The original brief suggested a ReAct-style agent. We use a fixed LangGraph graph instead: Routage → Reformulation (standalone question from the Conversation) → Décomposition into Sous-questions → for each Sous-question, a search within the Rôle's scope, reranking, at most one reworded retry, then a silent drop → generation (full or Réponse partielle) or Refus. Each step is a node that can be tested and measured on its own, and cost and latency are bounded. Retries and drops behave identically whether the missing content sits above the Rôle's level or doesn't exist, so even response timing doesn't reveal hidden Documents.

## Considered Options

- **Free ReAct loop** — more flexible, but the number of searches is unbounded, each decision is buried in free-form reasoning, and the behaviour is harder to test and explain.
- **No agent (single search)** — kept as the measured baseline, so RAGAS isolates what Reformulation and Décomposition add.
