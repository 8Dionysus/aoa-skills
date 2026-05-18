# Candidate Validation Gate

## Scope

This gate checks that Agon skill-binding candidate requests stay deterministic,
requested-only, and below stronger owner authority.

It does not create canonical skills.

## Validation

Use [parts/AGENTS](../AGENTS.md#validation) and the package [AGENTS](../../AGENTS.md#validation).
This gate follows the workflow candidate bridge build check, validator, and
part-local test before package-level topology checks.

## Exit criteria

- candidate requests are deterministic;
- all candidates remain `requested_not_landed`;
- no candidate defines lawful move vocabulary;
- no candidate issues proof verdicts;
- no candidate writes durable scars;
- no candidate opens an arena session;
- no candidate silently widens task scope.

## Later growth

A later reviewed skill pass may choose candidates after practice guidance exists
or after an explicit single-technique exception.

Do not convert every lawful move into a skill immediately. A named move is not
automatically a reviewed workflow.
