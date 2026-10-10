# Vantage

Assistant documentaire qui ne répond qu'à partir de ce que le Rôle de la personne qui pose la question peut consulter : textes réglementaires européens (`public`), procédures internes (`interne`) et dossiers sensibles (`confidentiel`) d'une entreprise fictive de drones. Vocabulaire : [`CONTEXT.md`](CONTEXT.md). Décisions : [`docs/adr/`](docs/adr/).

## Démarrage rapide

```bash
./vantage start
```

Cette commande vérifie chaque brique et répare ce qui manque. Elle lance ensuite l'API et l'interface. Ouvrez **http://localhost:3000**. Ctrl+C arrête tout.

Prérequis : Python 3.12+ et Node.js 20+. Il faut aussi une clé API Anthropic pour le modèle de référence, Claude Haiku 4.5 (ADR 0007). Elle va dans un fichier `.env` à la racine (`ANTHROPIC_API_KEY=…`), ignoré par git. Ollama avec `ministral-3:8b` est optionnel : il sert à développer sans payer d'appels. Un GPU NVIDIA est conseillé, mais pas obligatoire.

## Commandes

| Commande | Effet |
|---|---|
| `./vantage check` | Vérifie toutes les briques, sans rien modifier. Sort en erreur si l'une d'elles bloque. |
| `./vantage setup` | Crée le venv Python, installe les dépendances Python et npm, restaure les sources brutes manquantes et construit l'index si besoin. |
| `./vantage start` | `setup` puis `check`, puis lance l'API (port 8000) et l'interface en mode développement (port 3000). |
| `./vantage start --prod` | Pareil, avec l'interface compilée (`next build` puis `next start`). |
| `./vantage start --llm ollama` | Utilise Ministral 8B en local (développement) au lieu de Claude Haiku. |
| `./vantage index` | Reconstruit l'index Qdrant : embeddings bge-m3, environ 4 min sur GPU. |
| `./vantage test` | Lance les tests Python, puis le lint et la vérification de types du frontend. |

`check` contrôle, dans l'ordre :

| Brique | Ce qui est vérifié | Réparé par `setup` / `start` |
|---|---|---|
| Sources brutes | Chaque fichier de `data/sources.toml` est présent. | Oui : téléchargement ou extraction du zip. |
| Corpus | L'ingestion produit des Chunks des trois niveaux. | — |
| Index Qdrant | La collection existe et contient autant de points que le corpus de Chunks. | Oui : reconstruction. |
| LLM | La clé Anthropic est présente et donne accès à `claude-haiku-4-5`, ou, avec `--llm ollama`, Ollama répond avec son modèle. | — |
| LLM de dev | Ollama et `ministral-3:8b`. C'est un simple avertissement : seul `--llm ollama` en a besoin. | — |
| GPU | CUDA est disponible. C'est un simple avertissement : sans GPU, les embeddings tournent sur CPU. | — |
| Interface web | npm est présent et les dépendances sont installées. | Oui : `npm install`. |
| Ports | 8000 et 3000 sont libres. | — |

Variables d'environnement :

| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `API_PORT`, `WEB_PORT` | Ports de l'API et de l'interface | `8000`, `3000` |
| `VANTAGE_LLM` | `claude` ou `ollama` | `claude` |
| `ANTHROPIC_API_KEY` | Clé de l'API Anthropic, lue dans `.env` | — |
| `OLLAMA_URL`, `VANTAGE_OLLAMA_MODEL` | Adresse d'Ollama et modèle utilisé | `http://localhost:11434`, `ministral-3:8b` |
| `QDRANT_URL` | Qdrant dans Docker (`docker compose up -d`) | stockage local dans `data/qdrant/` |

Le stockage Qdrant local n'accepte qu'un processus à la fois. `check` le signale si l'API tourne déjà.

## Architecture

```
data/raw/            sources brutes, un dossier par source (data/sources.toml)
src/vantage/corpus/  ingestion : AI Act (EUR-Lex) et Documents internes → Chunks
src/vantage/rag/     index Qdrant filtré par Niveau d'accès, génération avec Références
src/vantage/api/     API FastAPI : /api/roles, /api/chat (flux SSE)
src/vantage/doctor.py  vérifications et réparations utilisées par ./vantage
web/                 interface Next.js, qui relaie /api vers FastAPI
```

Chaque module peut aussi se lancer seul :
- `python -m vantage.corpus.sources` restaure les sources brutes ;
- `python -m vantage.rag ask --role Manager "…"` pose une question en ligne de commande ;
- `python -m vantage.doctor` lance les vérifications.
