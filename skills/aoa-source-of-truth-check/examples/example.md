# Example

## Scenario

A repository has a top-level `README`, a `MANIFEST`, a runbook, and canonical docs for setup and rollout. The `README` and `MANIFEST` have started collecting long status history, run counters, and troubleshooting notes even though the canonical docs already exist.

## Why this skill fits

- the main problem is both authority mapping and summary-doc drift
- contributors need a clearer map of which file to trust first
- the goal is to keep top-level docs short and link-driven once canonical homes already exist

## Expected inputs

- the set of documents that currently overlap
- the area of ambiguity, such as setup, deployment, incident response, or status reporting
- any known canonical files or unclear ownership rules
- examples of contributor confusion caused by the overlap or bloated snapshot docs

## Expected outputs

- a clearer source-of-truth map for the affected concerns
- notes on conflicting or duplicated guidance
- lightweight snapshot guidance for `README` or `MANIFEST` when canonical homes already exist
- a short verification summary explaining why the docs surface is easier to navigate

## Boundary notes

- this example is about clarifying document ownership and authority, plus keeping summary docs lightweight
- it is not about writing a decision record unless the main unresolved problem is rationale rather than conflicting docs
- it is not about generic docs cleanup when no canonical homes exist yet

## Verification notes

- verify that each concern now has a named authoritative file
- verify that overview docs no longer silently compete with canonical instructions
- verify that top-level snapshot docs stay short and route detail outward
- verify that a new contributor could orient faster after the clarification
