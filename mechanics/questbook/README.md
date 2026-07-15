# Questbook Contract

Questbook preserves only durable unresolved obligations owned by this
repository. Source YAML lives under `quests/<lane>/<state>/`; `QUESTBOOK.md` is
the active human index; `generated/quest_*` files are deterministic read models.

Admission requires:

- the obligation survives the current bounded change;
- it is not already capability or skill source, a decision, a session-only
  follow-up, or another owner's backlog;
- owner, activation, evidence, effect scope, and closure criteria are explicit.

An empty catalog is valid. Closed or superseded quests are removed from the
active tree and remain recoverable from Git history.
