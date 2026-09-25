# The Rôle is the account — no user identity

The original brief described a user → Rôle mapping (a JSON file of users). We dropped it: there are no users, the demo selects one of the three Rôles directly, and each Rôle owns its own persisted Conversations. Combined with "a Conversation is bound to exactly one Rôle", this makes a history-based Fuite impossible by construction, and it keeps effort on the RAG/RBAC mechanics rather than on identity.

## Considered Options

- **Users with an assigned Rôle, Conversations owned by (user, Rôle)** — closer to production, but a Rôle change (e.g. a Manager demoted to Employé) would leave `interne` history visible to an Employé unless we added a second rule locking Conversations to their creation Rôle. That's the path to describe for production, not to build.

## Consequences

- All askers under the same Rôle share its Conversations — acceptable for a demo, and stated as such.
- Switching Rôle in the UI behaves like switching accounts: it lists that Rôle's Conversations and never carries one across.
- The original brief also listed an Externe Rôle (clients), seeing "a restricted subset of `public`". Since all of `public` is official, openly published text, there was nothing to restrict, which left it with exactly the same access as Employé, so it only duplicated every evaluation pair and every demo column. We dropped it: there is one Rôle per Niveau d'accès.
