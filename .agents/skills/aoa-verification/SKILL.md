---
name: aoa-verification
description: An implicit match may suggest this skill, but must not load or execute it until explicit invocation or a source-authorized parent-route selection. Turn one stable technical truth into bounded evidence through contract, coverage-audit, or property mode. Use when a named consumer boundary, an important invariant's real coverage, or a generative system property must be made reviewable. Do not use when behavior is undefined, the task is a general test plan, or green checks are being requested as whole-system proof.
license: Apache-2.0
compatibility: Designed for Codex or a compatible coding-agent host with repository file access and an interactive shell. Network access is optional and owner-specific tools are never assumed.
metadata:
  aoa_scope: core
  aoa_status: reviewed
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-verification/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_portable_profile: codex-facing-v2
---

# aoa-verification

## Intent
Start from owner meaning and observed behavior, then choose the smallest evidence
form whose green result has an explicit claim limit.

## Trigger boundary
Use this skill when:

- a stable producer-consumer seam, an important invariant, or a property across
  many inputs/states needs evidence that can reveal a meaningful break

Do not use this skill when:

- behavior or ownership is undefined, the change is private, the request is a
  generic test strategy, or automation would exist only to produce green status

## Inputs
- owner rule, system/boundary under review, named consumers where relevant
- manual cases or failures, current checks, and available oracle

## Outputs
- exactly one mode result: evidence package, gaps, smallest durable check or
  no-check decision, claim limit, and termination

## Procedure
### Mode selection

| Mode | Select when | Do not select when |
|---|---|---|
| `contract` | A named consumer relies on a stable ABI, receipt, schema, tool result, or handoff. | No consumer-visible seam exists. |
| `coverage-audit` | Checks exist and the question is what stable invariant they truly constrain. | The invariant itself is still unknown. |
| `property` | Correctness must hold across many inputs or states. | A bounded example or contract is sufficient. |

### Shared procedure

1. Read owner meaning before generated views or checks.
2. Exercise or reconstruct reality manually: expected, rejected, and motivating
   failure cases where available. Name missing cases.
3. Distinguish stable invariant from implementation detail and state the oracle.
4. Create durable automation only for a repeated or owner-declared long-lived
   rule. Temporary probes stay session-local and are removed after learning.
5. Review the evidence manually and state what green does not prove.

### Mode: contract

Name producer, consumer, inputs, outputs, errors/effects, compatibility, and
failure behavior. A durable seam check must reject the observed break before it
accepts owner-approved behavior. Stop `blocked_missing_input` when the consumer
or material ABI is unknown.

### Mode: coverage-audit

Map every important invariant to the check path that would fail if it broke.
Classify direct, indirect, example-only, absent, or false-confidence coverage.
Return only the smallest uncovered risks; do not turn line count into proof.

### Mode: property

State the property, domain/generator, preconditions, oracle, shrink/reproduction
path, and known counterexamples. Prefer algebraic or semantic truth such as
idempotence, monotonicity, conservation, or round-trip behavior over random
input volume.

## Contracts
- manual observation and owner meaning precede durable automation
- a check protects one claim and cannot certify the whole system
- generated/exported views remain subordinate to owner sources
- no-check is valid when recurrence, oracle, or stability is missing

## Risks and anti-patterns
- restating a fixture, snapshot, formatting, or field order as semantic law
- property tests with a self-fulfilling oracle
- adding validators after the fact to hide an unresolved manual failure

## Verification
- confirm selected mode, owner rule, manual cases, and oracle
- if automation is proposed, show the motivating failure it catches
- make claim limit, evidence gap, consumer impact, and stop line explicit

## Adaptation points
Owners supply local commands, generators, schemas, fixtures, consumers, and
compatibility windows without duplicating this procedure.
