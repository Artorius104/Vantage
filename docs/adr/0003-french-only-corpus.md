# French-only Corpus

The Corpus is entirely in French: the official French version of the AI Act (equally authentic in law), CNIL guides, only those EDPB guidelines with an official French translation, and fictional internal Documents, gold questions and Faits canaris written in French. This fits the story (a French consultancy under CNIL oversight) and keeps language out of our retrieval evaluations, since mixed-language retrieval systematically favours same-language matches.

## Consequences

- The original brief's `bge-small-en` suggestion is out; embedding and reranking models must handle French. We use `BAAI/bge-m3` for embeddings and `BAAI/bge-reranker-v2-m3` for reranking: both multilingual, local and free, and from the same family. Comparing embedding models is out of scope.
- The public side is the full AI Act (one parser, over EUR-Lex's regular structure), plus 3–4 CNIL guides matching the fictional Documents' themes. EDPB is optional: at most one guideline with an official French translation, and only if it fits those themes.
- A mixed-language Corpus with cross-lingual retrieval is a later extension, not part of the MVP.
