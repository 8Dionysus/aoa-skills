# Example

## Scenario

A repository has a top-level `README`, a deployment guide, a runbook, and a setup doc. Contributors keep getting different answers about which file is authoritative for local startup commands, production rollout steps, and incident recovery notes.

## Why this skill fits

- the main problem is overlap and ambiguity across documentation surfaces
- contributors need a clearer map of which file to trust first
- the goal is to reduce silent conflict between overview docs and canonical instructions

## Expected inputs

- the set of documents that currently overlap
- the area of ambiguity, such as setup, deployment, or incident response
- any known canonical files or unclear ownership rules
- examples of contributor confusion caused by the overlap

## Expected outputs

- a clearer source-of-truth map for the affected concerns
- notes on conflicting or duplicated guidance
- proposed document-role clarification
- a short verification summary explaining why the docs surface is easier to navigate

## Boundary notes

- this example is about clarifying document ownership and authority
- it is not about writing a decision record unless the main unresolved problem is rationale rather than conflicting docs

## Verification notes

- verify that each concern now has a named authoritative file
- verify that overview docs no longer silently compete with canonical instructions
- verify that a new contributor could orient faster after the clarification
