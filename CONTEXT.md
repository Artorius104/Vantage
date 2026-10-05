# Vantage — Enterprise Knowledge Copilot

A conversational assistant for everyday questions and tasks that, whenever an answer depends on documents, answers only from the European AI regulation and fictional internal company documents the asker's role is allowed to see.

## Language

### Corpus

**Corpus**:
All the **Documents** Vantage can answer from — regulatory texts plus fictional internal documents, entirely in French.
_Avoid_: knowledge base, dataset, index

**Document**:
One source text in the corpus (a regulation, a guide, a fictional internal note), carrying exactly one **Niveau d'accès**. A text that mixes sensitivities is split into separate Documents before it enters the corpus.
_Avoid_: file, source, page

**Chunk**:
A passage cut from a **Document**, lying entirely within one structural unit of it (an article, a recital, an annex point, a section), so it has exactly one **Référence** and one **Portée**. It always inherits its Document's **Niveau d'accès** and is never tagged independently.
_Avoid_: passage, segment, fragment

**Référence**:
The precise location a **Chunk** comes from — e.g. *AI Act, Article 6, §2*; *AI Act, Annexe III, point 4*; *Note interne X, section 3*. Citations in answers point to Références.
_Avoid_: source, citation, metadata

**Portée**:
The legal weight of a **Chunk**: `contraignant` (binding law — regulation articles and annexes), `interprétatif` (recitals, CNIL and EDPB guidance) or `politique interne` (the company's own Documents). Unlike **Niveau d'accès**, it can vary within one Document and follows the Chunk's position in it. When sources conflict, `contraignant` prevails and the contradiction is flagged; any other conflict is flagged by presenting both positions with their Références and naming no winner. A conflict is never silently resolved, and an internal policy stricter than guidance is not a conflict.
_Avoid_: authority, source type, priority

### Access control

**Niveau d'accès** (`access_level`):
The sensitivity tier of a piece of content — exactly one of `public`, `interne`, `confidentiel`. The tiers form a strict ladder: each includes everything below it.
_Avoid_: permission, clearance, visibility

**`public`**:
Official regulatory texts (AI Act, CNIL, EDPB) that anyone may read.

**`interne`**:
Fictional internal company procedures and notes.

**`confidentiel`**:
Fictional sensitive cases and internal decisions.

**Rôle**:
Who is asking — there is no separate user identity; the Rôle is the account. It determines the highest **Niveau d'accès** visible and owns its own **Conversations**. One of Employé, Manager, Conformité — one per **Niveau d'accès**.
_Avoid_: user, profile, group, account

**Employé**:
A **Rôle** limited to `public`.
_Avoid_: Externe, Client

**Manager**:
A **Rôle** that may see up to `interne`.

**Conformité**:
A **Rôle** (compliance / DPO) that may see everything, up to `confidentiel`.
_Avoid_: DPO, admin

### Conversations

**Conversation**:
A persisted sequence of questions and answers bound to exactly one **Rôle** for its whole life; changing Rôle means switching to that Rôle's Conversations, never carrying one across.
_Avoid_: chat, session, thread

**Comparaison des Rôles**:
One question answered side by side for every **Rôle**, each as the first turn of that Rôle with no history. It is not a **Conversation**: nothing is stored and it appears in no Rôle's history.
_Avoid_: side-by-side chat, multi-role conversation

### Answering

**Routage**:
The decision whether a question is a **Question documentaire** or a **Question générale**, made from the question and its **Conversation** only — blind to the **Rôle** and to the **Corpus**, so it can never reveal what exists above a Rôle's level. When unsure, it chooses **Question documentaire**.
_Avoid_: intent detection, triage, dispatch

**Question documentaire**:
A question whose answer depends on **Corpus** content (what a regulation says, how the company does something). A task whose substance comes from the Corpus ("draft an email explaining our procedure") is still a Question documentaire: the requested form is applied, but every fact comes from **Chunks** within the Rôle's scope — never from the model's general knowledge — or it gets a **Refus**.
_Avoid_: RAG question, search query

**Question générale**:
A question or task that does not depend on the **Corpus** (a recipe, rewriting an email); answered directly, without retrieval. This includes reshaping an answer already given in the same **Conversation** (a table, a translation, a summary), provided no fact is added.
_Avoid_: chit-chat, off-topic question

**Sous-question**:
One independently searchable part of a **Question documentaire**. Each is searched within the Rôle's scope on its own; one that finds nothing is dropped silently.
_Avoid_: sub-query, intent, facet

**Réponse partielle**:
An answer to a **Question documentaire** built only from in-scope Chunks, when only part of the question can be answered; it never mentions that anything is missing.

### Leaks

**Fuite**:
Any exposure, to a **Rôle**, of content from — or the existence of — a **Document** above that Rôle's **Niveau d'accès**. Measured as two distinct kinds: **Fuite de contexte** and **Fuite de réponse**.
_Avoid_: breach, data leak, violation

**Fuite de contexte**:
A **Chunk** above the Rôle's **Niveau d'accès** reaching answer generation, whether or not the answer uses it.

**Fuite de réponse**:
An answer revealing content or existence of a **Document** above the Rôle's **Niveau d'accès**; detected by the presence of a **Fait canari**.

**Fait canari**:
A unique, invented name or identifier (a code name, a fictional entity, a file reference — never a figure or a common word) planted in every **Chunk** of an `interne` or `confidentiel` **Document**, so its appearance in an answer proves a **Fuite de réponse**.
_Avoid_: canary token, marker, watermark

**Refus**:
The single fixed answer given, identically for every **Rôle**, to a **Question documentaire** when nothing in the Rôle's scope answers it — so the wording itself never hints that out-of-scope content exists. Given either when every **Sous-question** is dropped for lack of relevant Chunks, or when the Chunks found are related but don't actually answer; an approximate answer is never given instead.
_Avoid_: denial, access denied message

### Evaluation

**Jeu de référence**:
The gold set: questions written once as gold **Sous-questions**, each with its **Références**, a short reference answer and any **Faits canaris**, plus an expected **Routage**. Each Rôle's expectations (Références, full / partial / **Refus**, forbidden canaries) are computed from it, never written per Rôle. It also holds **Questions générales** and multi-turn scripts. It is split into a dev part (~20 questions, used for tuning) and a test part (~10, committed before any tuning, covering every kind of case, used only for reported scores).
_Avoid_: test set, benchmark, golden dataset

**Évaluation témoin**:
The leak evaluation re-run with the **Niveau d'accès** filter disabled; on the **Paires exposées** it must show a **Fuite** rate above thresholds fixed before any run, proving the test can detect leaks at all. Falling short means fixing the **Corpus**, never the thresholds. Possible only because `interne` and `confidentiel` **Documents** deliberately cover the same topics as the regulation and outrank it for some questions.
_Avoid_: control run, ablation, negative test

**Paire exposée**:
A question of the **Jeu de référence** paired with a **Rôle** for which some expected **Référence** lies in a **Document** above that Rôle's **Niveau d'accès**. Computed from the Jeu de référence. The only pairs a **Fuite** rate is measured on, so pairs where nothing is hidden don't dilute it.
_Avoid_: sensitive question, at-risk pair
