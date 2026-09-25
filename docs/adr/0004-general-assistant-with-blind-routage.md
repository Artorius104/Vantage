# General assistant with Rôle-blind, Corpus-blind Routage

The original brief described a pure RAG system. Vantage instead answers everyday questions and tasks (Questions générales) directly, and uses retrieval only for Questions documentaires. A dedicated classifier node makes that choice from the question and its Conversation alone. It never sees the Rôle or the Corpus, because a routing decision that depends on content above a Rôle's level is itself a side channel: "search, and route by whether anything matched" would answer a question about a hidden case with a Refus but a question about a non-existent case with a chatty invented reply, which reveals the hidden case exists. When uncertain, the classifier chooses documentaire, and a Question documentaire never falls back to the model's general knowledge. A wrong documentaire costs at worst a needless Refus; a wrong générale produces invented company facts.

## Considered Options

- **ReAct agent with a search tool** — the most natural agent pattern, but the routing decision is buried inside free-form reasoning, can't be tested on its own, and is made after the agent has seen search results.
- **Keyword rules** — deterministic and free, but they miss questions like "Est-ce que mon chatbot RH est à haut risque ?".

## Consequences

- Routing accuracy is a measured metric: each gold question carries an expected routing label.
- Anyone "optimising" the router by letting it peek at retrieval results reopens this decision and the leak path it closes.
