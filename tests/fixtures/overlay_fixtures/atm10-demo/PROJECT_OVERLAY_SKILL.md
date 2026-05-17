# atm10-demo Overlay Skill Fixture

## Base skill

- base skill: `aoa-change-protocol`
- base canon remains `aoa-skills`

## Overlay triggers

- use this future fixture when the base change workflow is already correct but the repo needs local paths or commands
- do not use it for upstream technique changes or broad scenario composition

## Local inputs

- repository-relative paths
- repository-relative commands
- explicit local approval rules

## Local outputs

- a thin local adaptation note
- a repository-relative command sketch
- a bounded verification reminder

## Local procedure notes

- start from the base skill instead of rewriting it
- bind only the local repo details that the downstream maintainer must inspect

## Authority and safety notes

- local authority remains downstream and explicit
- this overlay does not expand hidden operational scope

## Verification notes

- verify that every path and command stays repository-relative
- verify that the output remains reviewable and public-safe

## Fixture-only notes

- this is a future fixture, not a live project-family skill
- richer downstream behavior should stay fixture-bound until a separate overlay contract is promoted
