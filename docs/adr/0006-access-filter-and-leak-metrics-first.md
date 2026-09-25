# Niveau d'accès filter and Fuite metrics first, cut order fixed in advance

The original brief's plan built plain RAG in weeks 1–3 and left RBAC and the leak metric to week 4. Scope has since grown (Routage, stored Conversations, Portée, Décomposition, Faits canaris, Évaluation témoin, a split Jeu de référence) while the deadline stays at 4 weeks, so a week-3 overrun would squeeze out the very thing that makes Vantage different. We reorder: week 1 builds the Corpus with the Niveau d'accès filter from day one; week 2 commits the Jeu de référence test part, then measures both Fuite kinds and the Évaluation témoin on the single-search pipeline; week 3 adds the fixed graph and compares it with that baseline; week 4 is presentation (stored Conversations, UI, Portée conflict flagging, README, demo).

## Consequences

If we fall behind, cuts happen in this order, first to go first:

1. **Measured chunking comparison** — the original brief's fixed-size vs structural comparison, run as a retrieval-only experiment on the dev part (context precision / recall). Fixed-size chunks exist only in this experiment, never cross a Document boundary, and carry every Référence they span. The product only knows structure-bounded Chunks. Fallback: justify the choice with concrete examples of fixed-size chunks breaking Référence and Portée.
2. **Portée conflict flagging** — Portée stays shown in citations; conflicting sources are no longer arbitrated.
3. **Décomposition** — Reformulation stays; Réponses partielles come from a single search.
4. **Stored Conversations** — kept in memory, still one Rôle per Conversation.

The UI is Streamlit. Its stateless Comparaison des Rôles view carries the demo and outlasts stored Conversations if week 4 is squeezed.

Never cut: the Niveau d'accès filter, both Fuite metrics, the Évaluation témoin, the committed test part of the Jeu de référence, Routage, and the baseline-vs-agent comparison. Any cut beyond this list is a new decision and gets recorded as such.
