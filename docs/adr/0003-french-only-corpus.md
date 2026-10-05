# French-only Corpus

The Corpus is entirely in French: the official French version of the AI Act (equally authentic in law), CNIL guides, only those EDPB guidelines with an official French translation, and fictional internal Documents, gold questions and Faits canaris written in French. This fits the story (a French consultancy under CNIL oversight) and keeps language out of our retrieval evaluations, since mixed-language retrieval systematically favours same-language matches.

## Consequences

- The original brief's `bge-small-en` suggestion is out; embedding and reranking models must handle French. We use `BAAI/bge-m3` for embeddings and `BAAI/bge-reranker-v2-m3` for reranking: both multilingual, local and free, and from the same family. Comparing embedding models is out of scope.
- The public side is the four EUR-Lex texts the fictional Documents of *Vantage Aerospace Systems* lean on most: the AI Act, Regulation (EU) No 376/2014 (occurrence reporting in civil aviation), the GDPR and NIS2. They share one HTML structure, so one parser covers them. It also includes four CNIL AI guides: impact assessment, development security, data collection and management, and qualification of actors. EDPB is optional. Other texts those Documents mention (2018/1139, 2019/947, 2019/945, 2021/821, EASA guidance) are left out: their annexes are huge or their guidance is in English. Every raw source is listed in `data/sources.toml`.
- A mixed-language Corpus with cross-lingual retrieval is a later extension, not part of the MVP.
