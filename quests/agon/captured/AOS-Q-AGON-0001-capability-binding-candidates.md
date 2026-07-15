# AOS-Q-AGON-0001: Agon Capability Binding Candidates

## Intent

Receive bounded workflow candidate requests from `Agents-of-Abyss`.

## Done when

- config and generated candidate index are present;
- every candidate remains `requested_not_landed`;
- validation passes;
- no candidate is promoted as a callable skill by this quest.

## Verify

Use the workflow-candidate bridge build check, validator, and part-local test
named by `mechanics/agon/AGENTS.md`. The captured quest should preserve the
verification route, not a second copy of the command block.
