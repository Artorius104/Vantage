# Vantage — interface web

Next.js (App Router). Le navigateur ne parle qu'à Next.js ; `/api/*` est relayé vers l'API FastAPI (`VANTAGE_API_URL`, par défaut `http://localhost:8000`). Voir le README à la racine pour tout lancer.

- `components/ChatApp.tsx` : état de l'application, une liste de Conversations par Rôle (ADR 0002), conservée dans le navigateur en attendant #16.
- `lib/api.ts` : client de l'API, lecture du flux SSE (`sources`, `token`, `error`, `done`).
- `components/MessageView.tsx` : rendu Markdown ; les `[Référence]` effectivement récupérées deviennent des liens vers leur source.
