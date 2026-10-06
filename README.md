# Vantage

Assistant documentaire qui ne répond qu'à partir de ce que le Rôle de la personne qui pose la question peut consulter. Vocabulaire : [`CONTEXT.md`](CONTEXT.md). Décisions : [`docs/adr/`](docs/adr/).

## Lancer en local

Prérequis : Python 3.12+, Node.js 20+, et un LLM (Ollama avec `ministral-3:8b` pour le développement, ou `MISTRAL_API_KEY` pour le modèle de référence).

```bash
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m vantage.corpus.sources       # vérifie et restaure les sources brutes
.venv/bin/python -m vantage.rag index            # embeddings bge-m3 + Qdrant (~4 min sur GPU)

.venv/bin/uvicorn vantage.api.app:app --port 8000   # API ; VANTAGE_LLM=mistral pour le modèle de référence
cd web && npm install && npm run dev                # interface sur http://localhost:3000
```

Qdrant tourne en local sur disque (`data/qdrant/`), ou dans Docker avec `docker compose up -d` et `QDRANT_URL=http://localhost:6333`. Le stockage local n'accepte qu'un processus à la fois : arrêtez l'API avant de relancer `vantage.rag index`.

## Tests

```bash
.venv/bin/pytest
cd web && npm run lint
```
