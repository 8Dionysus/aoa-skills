# Trigger evals and collision tests

The trigger-eval surface is a policy-aware JSONL dataset derived from the earlier CSV seed.
It stays separate from install profiles and trust policy.
The description-first activation suite validates the portable `description` field without replacing the seed data.

## Why the format changed

The first dataset shape was enough for seed coverage.
It was not enough for policy-aware evaluation.

We now need to distinguish:

- explicit invocation
- implicit positive routing
- adjacent negative controls
- collision prompts against nearby skills
- explicit-only skills that should require manual invocation even when the semantic match is strong
- `suggest` skills that may appear as candidates without hidden activation
- `manual` skills that must keep natural-language semantic matches out of hidden activation and candidate-surfacing paths

## Dataset fields

Each JSONL object includes:

- `case_id`
- `skill_name`
- `mode`
- `expected_behavior`
- `expected_skill`
- `competing_skills`
- `invocation_mode`
- `prompt`
- `note`

## `expected_behavior`

Possible values:

- `invoke-skill`
- `do-not-invoke-skill`
- `manual-invocation-required`

`manual-invocation-required` is the key addition for explicit-only skills.

## Collision families

The collision matrix groups the skills most likely to blur together.
These prompts are designed to reveal description drift and routing overlap, not just activation success.
Collision cases must still obey `implicit_activation_policy`: `invoke` cases may expect `invoke-skill`, `suggest` cases may produce candidate-only coverage, and `manual` cases must resolve to `manual-invocation-required` even when the local match is strong.

## Description Activation Contract

The description activation suite adds:

- `generated/skill_description_signals.json`
- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_cases.csv`
- `generated/description_trigger_eval_manifest.json`
- `generated/skills_ref_validation_manifest.json`

This layer treats the portable `description` field as the primary activation surface.
It adds mirrored defer cases so neighboring skills are tested for staying out of the match, not only for winning it.

The newer case classes are:

- `explicit-handle`
- `should-trigger`
- `manual-invocation-required`
- `should-not-trigger`
- `prefer-other-skill`

Stress coverage stays inside the same contract. Use
`../mechanics/antifragility/parts/collision-stress-program/README.md` when you
need the bounded stress-specific extension for:

- timeout or repair prompts that should stay manual
- source-of-truth wins over ADR drafting under stress-doc overlap
- one-off incident prompts that must stay negative instead of lifting into automation
- downstream tiny-router precision that should inherit those same boundaries

## Maintenance rule

When any of these change, update the trigger evals in the same pull request:

- skill description
- invocation mode
- a major trigger boundary
- a major `do not use` boundary
- overlay activation conditions

Then use the activation/trigger owner checks named by
`mechanics/audit/AGENTS.md` and the generated/export lane manifest. The focused
owners are the trigger-eval builder/lint, description-trigger builder/lint, and
tiny-router validation surfaces.

Pack profiles and trust posture live in separate support surfaces and should be checked with:

Use the pack-profile owner lint when install profile membership or generated
config snippets can move.

If you want the soft open-standard conformance lane as well, run:

Use the skills-ref soft conformance wrapper after portable export has been
built. Missing external validator remains a clean skip; real validator failures
remain failures.
