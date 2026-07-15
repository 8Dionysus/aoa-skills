---
name: aoa-decision
description: Find, record, or correct durable repository decisions through one decision family. Use when prior rationale, a meaningful accepted decision, supersession, or source/index drift is the task. Select exactly one internal mode and keep authored owner records authoritative. Do not use for ordinary docs edits or unresolved source-of-truth mapping.
scope: core
status: reviewed
summary: One self-contained decision family with find, record, and correct modes over owner-authored decision records.
invocation_mode: implicit-friendly
---

# aoa-decision

## Intent

Provide one front door for durable decision work. `find`, `record`, and
`correct` are internal modes, not separately advertised skills. Owner-authored
records are authoritative; indexes, KAG packets, caches, and session evidence
only help locate them.

## Trigger boundary

Use this skill when:

- existing rationale, status, supersession, a meaningful accepted decision, or
  drift between a decision source and its derived views is the task

Do not use this skill when:

- the task is an ordinary edit, unresolved source-of-truth mapping, an
  undecided option, or a change whose rationale fits a bounded note

Lack of write authority never becomes implicit approval.

## Inputs

- intent and target owner, subject, ID, or path when known
- owner decision route, source records, template, and index contract
- accepted choice plus alternatives for `record`, or mismatch for `correct`

## Outputs

- exactly one mode result with owner source, confidence, effect, verification,
  skipped checks, uncertainty, and stop line

## Procedure

### Mode selection

Choose exactly one mode:

| Mode | Select when | Do not select when |
|---|---|---|
| `find` | Existing rationale, status, supersession, or impact is requested. | A write or correction is already known to be required. |
| `record` | A meaningful accepted decision lacks an adequate owner record. | The choice is open, trivial, already recorded, or only needs correction. |
| `correct` | An existing source record or derived view is stale or wrong. | The task is pure lookup or a genuinely new decision. |

Legacy decision-child names are migration aliases. Do not load them after
selecting a mode.

### Shared procedure

1. Confirm applicability and select one mode. Separate lifecycle steps when two
   modes target the same record.
2. Read the nearest owner decision route, source records, and index contract.
3. A retriever may narrow candidates, but every used claim must be checked in
   the authored record.
4. Execute only the selected mode and report source, effect, verification,
   skipped checks, and uncertainty.

Stop as `blocked_missing_input` when owner source is unavailable. Missing
evidence is neither approval nor material to fill from memory.

### Mode: find

#### Applicability

Use for prior rationale, status, supersession, or changed-path impact.

#### Procedure

1. Search by the narrowest anchor: ID, path, source surface, owner, then repo.
2. Check derived lookup freshness; stale results are hints.
3. Read every authored record used and classify matches as exact, likely,
   analogy, stale, superseded, or missing.

#### Verification and termination

Return compact source refs, status, relevance, confidence, and next route.
Never invent a missing decision.

### Mode: record

#### Applicability

Use only after a meaningful decision is accepted and lacks an adequate record.

#### Procedure

1. Confirm acceptance, owner, value beyond a lighter note, and absence of an
   adequate existing record.
2. Read the owner route, template, latest IDs, and related records.
3. Capture context, material alternatives, choice, rationale, consequences,
   owner boundary, affected sources, and follow-up.
4. Do not infer alternatives, rationale, or consequences from the accepted
   choice. When owner evidence for any material section is missing, return an
   explicitly incomplete draft with `[owner input required]` and
   `blocked_missing_input`; an accepted choice does not imply rejected options.
5. Write only when authorized, then rebuild derived indexes from source and run
   owner-local validation.

#### Verification and termination

Verify why and tradeoffs rather than diff narration. Stop before writing when
acceptance, owner evidence, placement, source surface, or authority is missing.

### Mode: correct

#### Applicability

Use when an existing source record or its derived view is stale or wrong.

#### Procedure

1. Read target source and owner law; classify source error, metadata error,
   semantic supersession, generated drift, or stale cache.
2. Correct source first when meaning changed, preserving history through status
   or supersession. For derived-only drift, leave source untouched and use the
   owner-declared builder; never hand-edit a generated view. If its builder or
   index contract is unavailable, state the expected target state and stop as
   `blocked_missing_input` without proposing a manual generated-file patch.
3. Validate owner source and compare every refreshed consumer to it.

#### Verification and termination

Report mismatch, correction, effect, and residual risk. Do not widen cache or
typo repair into new rationale, and do not report an unrebuilt view as fixed.

## Contracts

- exactly one mode controls one target at a time
- owner-authored records outrank every retriever or generated view
- `record` and `correct` effects require current authority
- generated indexes follow source; session evidence is not decision authority

## Risks and anti-patterns

- loading legacy children, trusting a title/index, or writing pre-decision
- recording trivial diffs, cache-only correction, or silent history rewrite
- copying a sibling owner's rationale or template as local law

## Verification

- one mode; owner-source claims; authorized effects
- source-first correction and rebuilt consumers where relevant
- explicit termination, validation, skipped checks, and uncertainty

## Adaptation points

Each repository supplies its ID format, template, source home, index builder,
validation command, and supersession vocabulary.
