---
name: skill-name
description: State the exact positive trigger, useful outcome, important exclusion, and selection boundary in plain language.
scope: core
status: scaffold
summary: One-sentence procedural identity.
invocation_mode: explicit-preferred
---

# skill-name

## Intent

Name the bounded outcome this callable family provides and why it needs a
host-visible entry rather than only a capability node or internal mode.

## Trigger boundary

Use this skill when:

- positive case

Do not use this skill when:

- nearby negative or owner-routed case

## Inputs

- required input, owner, and authority

## Outputs

- typed result, evidence, effect, and stop line

## Procedure

1. Confirm applicability and select at most one internal mode when modes exist.
2. Read the current owner sources and verify required tools or inputs.
3. Perform the bounded procedure.
4. Verify the result and terminate explicitly.

## Contracts

- stable invariant and owner boundary

## Risks and anti-patterns

- likely false trigger, unsafe effect, or authority error

## Verification

- manual positive, negative, coexistence, and failure cases
- structural checks that preserve only the stable invariants above

## Adaptation points

- owner paths, commands, tools, permissions, and output vocabulary supplied by
  a named adapter rather than copied into the core procedure
