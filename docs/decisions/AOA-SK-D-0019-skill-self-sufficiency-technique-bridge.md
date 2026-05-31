# Skill Self-Sufficiency And Technique Bridge

- Decision ID: AOA-SK-D-0019

## Index Metadata

- Original date: 2026-05-07
- Surface classes: skill source, technique bridge, public status
- Skill lanes: none
- Mechanic parents: none
- Guard families: technique bridge, skill maturity
- Posture: accepted skill self-sufficiency bridge

Date: 2026-05-07

## Context

`aoa-skills` grew as the operational companion to `aoa-techniques`.
That relationship is real and direct: skills can compose techniques, and skill
execution can reveal new technique candidates.

The previous maturity wording and generated governance readouts treated pending
technique lineage as a canonical blocker. That made technique bridge completeness
too easy to confuse with skill maturity, especially for skill-native workflows
that are already used across the workspace.

## Decision

Skills are self-contained execution objects.

Technique links remain first-class bridge evidence, but they are adjacent to the
skill maturity path rather than identical with it.

The bridge is bidirectional:

- techniques can be composed into skills
- repeated skill workflows can be decomposed into technique extraction requests

Pending or drifted technique lineage must stay visible as a bridge finding.
It should route refresh, repair, or extraction work to `aoa-techniques`, but it
should not by itself block a skill-native promotion review.

## Consequences

- `SKILL.md` remains the execution meaning source.
- `techniques.yaml` remains the technique bridge manifest.
- Generated public-surface rows can expose `technique_bridge_findings` separately
  from `canonical_candidate_blockers`.
- Promotion-pressure reporting treats bridge findings differently from hard
  skill-native blockers.
- Reviewers still need to ask whether a canonical claim is skill-native,
  technique-bridge-complete, or both.

## Verification

The expected verification path is:

- rebuild generated public/governance/quality/promotion surfaces
- run focused tests for public surface, quality audit, promotion pressure, and
  validation
- run the full repository test suite before merge
