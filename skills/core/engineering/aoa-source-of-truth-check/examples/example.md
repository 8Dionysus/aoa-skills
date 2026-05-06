# Example

## Scenario

A repository has a top-level `README`, `ROADMAP`, runbook, mechanics package, generated manifest, and preserved legacy receipts. The entrypoint docs have started collecting historical audit detail and package-local notes even though canonical active surfaces and provenance bridges already exist.

## Why this skill fits

- the main problem is both authority mapping and summary-doc drift
- contributors need a clearer map of which file to trust first
- the goal is to keep top-level docs short and link-driven once canonical homes already exist
- the legacy material must stay recoverable without becoming the active contract

## Expected inputs

- the set of documents that currently overlap
- the area of ambiguity, such as setup, deployment, incident response, or status reporting
- any known canonical files or unclear ownership rules
- active, legacy/provenance, generated, and decision surfaces that may be carrying the same meaning
- examples of contributor confusion caused by the overlap or bloated snapshot docs

## Expected outputs

- a clearer source-of-truth map for the affected concerns
- a placement decision for active behavior, historical evidence, generated companions, and decision rationale
- notes on conflicting or duplicated guidance
- lightweight snapshot guidance for `README` or `MANIFEST` when canonical homes already exist
- a short verification summary explaining why the docs surface is easier to navigate

## Boundary notes

- this example is about clarifying document ownership and authority, plus keeping summary docs lightweight
- it is not about writing a decision record unless the main unresolved problem is rationale rather than conflicting docs
- it is not about generic docs cleanup when no canonical homes exist yet
- it is not about erasing legacy evidence; it is about routing active readers through current surfaces first

## Verification notes

- verify that each concern now has a named authoritative file
- verify that overview docs no longer silently compete with canonical instructions
- verify that top-level snapshot docs stay short and route detail outward
- verify that legacy/provenance and generated surfaces remain discoverable but subordinate to active source docs
- verify that a new contributor could orient faster after the clarification
