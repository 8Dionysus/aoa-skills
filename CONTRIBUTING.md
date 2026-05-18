# Contributing to aoa-skills

Thank you for contributing.

## What belongs here

Good contributions:
- reusable AoA skill bundles
- bounded agent workflows that stand on their own and reference sibling practice only when useful
- skill templates and repository conventions
- validation or review helpers for skill bundles
- thin project overlay examples that clarify how a core skill adapts to a real repository
- docs-only truth sync that keeps the current public surface and derived layers readable

Bad contributions:
- private operational context
- secrets, tokens, or sensitive infrastructure details
- one-off prompts without reusable skill structure
- project-specific shortcuts with no adaptation notes
- undocumented scripts
- techniques that belong in `aoa-techniques` rather than here
- skills that mirror another repository's practice without adding executable workflow value

## Before opening a PR

Start from the public route:

1. [CHARTER](CHARTER.md) for repository authority
2. [AGENTS](AGENTS.md) and the nearest nested `AGENTS.md` for editing route
3. [RELEASING](mechanics/release-support/docs/RELEASING.md) for release-facing
   or full-packaging checks
4. the target `SKILL.md`, `techniques.yaml`, mechanic package, config, schema,
   builder, or review record that owns the change

Please make sure:
- the skill has a clear purpose and trigger boundary
- the skill remains bounded and reviewable
- the skill includes a canonical `SKILL.md`
- the skill records technique dependencies in `techniques.yaml` when relevant
- invocation policy is stated clearly when the skill is risky or operationally sensitive
- risks and anti-patterns are documented
- verification expectations are explicit
- runtime examples and review checklists use the repository artifact contract when present
- examples and references are public-safe
- project-shaped overlays do not silently change the core meaning of the skill
- runtime, evaluation, and public-surface layers stay distinct from one another
- portable export drift is refreshed when canonical skill bodies, invocation modes, portable descriptions, or trigger boundaries change

Use the validation commands named by the nearest owner surface. Do not copy a
stale command list from this file into a PR; route to the current `AGENTS.md`,
builder, validator, or release-support document.

If you add a new runtime example, start from `templates/RUNTIME_EXAMPLE.template.md`
and keep the canonical headings exactly:
- `Scenario`
- `Why this skill fits`
- `Expected inputs`
- `Expected outputs`
- `Boundary notes`
- `Verification notes`

If you add `checks/review.md`, keep the canonical checklist headings exactly:
- `Purpose`
- `When it applies`
- `Review checklist`
- `Not a fit`

## Core distinction

`aoa-skills` owns self-contained execution workflows for local coding agents.
`aoa-techniques` owns public reusable engineering practice.

If the contribution is primarily a reusable engineering pattern, publish or refine it in `aoa-techniques` first.
If the contribution is primarily an agent-facing workflow bundle, it belongs here.

## Preferred PR scope

Prefer:
- 1 new skill per PR
- or 1 focused refresh to an existing skill
- or 1 clear repository-level docs or template improvement

Promotion or maturity-changing PRs should also align with `mechanics/method-growth/docs/MATURITY_MODEL.md`
and `mechanics/method-growth/docs/PROMOTION_PATH.md`, and make the supporting evidence explicit.

## Recommended PR title format

- `skill: add <skill-name>`
- `skill: improve <skill-name>`
- `skill: refresh <skill-name> from techniques`
- `skill: add project overlay <skill-name>`
- `docs: refine repo guidance`
- `repo: improve templates or validation`
- `docs: truth-sync roadmap and phase guidance`

## Review criteria

PRs are reviewed for:
- bounded scope
- execution usefulness
- traceability to techniques when relevant
- public safety
- reviewability of the final `SKILL.md`
- clarity of trigger boundary
- quality of risks and verification guidance
- coherence with repository philosophy

## Maturity and promotion

Status changes are governance changes, not cosmetic relabeling.
The repository-level promotion path lives in `mechanics/method-growth/docs/PROMOTION_PATH.md`.

When proposing a promotion step:
- state the current and target maturity status
- cite the evidence that supports promotion
- explain whether the runtime `SKILL.md` meaning changed
- name any remaining gaps that block the next maturity step
- add or update the public review record under `docs/reviews/status-promotions/`
- use `templates/STATUS_PROMOTION_REVIEW.template.md` for non-canonical promotion reviews
- make the review record explicit about machine-checkable floors and what still blocks the next status step
- keep governance review records separate from runtime walkthroughs and evaluation evidence

When proposing `canonical` specifically:
- ensure the skill uses `## Technique traceability`, not `## Future traceability`
- ensure `technique_dependencies` and `techniques.yaml` contain no pending IDs or `TBD` source refs
- ensure the skill has evaluation coverage in `tests/fixtures/skill_evaluation_cases.yaml`
- rely on existing validator checks for `explicit-only` policy correctness rather than bypassing them
- add or update the public review record under `docs/reviews/canonical-candidates/`
- use `templates/CANDIDATE_REVIEW.template.md` for new candidate-review records
- make the review record explicit about machine floors, whether the runtime meaning changed, and what still blocks the next maintenance step
- keep canonical-candidate records aligned with the current public surface rather than historical scaffold wording

## Drift and refresh

A skill may summarize or compose techniques, but it should not silently drift away from them.
When a source technique changes materially, dependent skills should be reviewed and refreshed.

A good PR should make it clear:
- which techniques are referenced
- whether the skill meaning changed
- whether only metadata changed
- whether project overlays also require updates
- whether the change belongs in `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`
  as a repo-local overlay contract clarification or in a live exemplar skill
  bundle
- whether generated or portable export surfaces changed

If richer integration belongs in another repository, record the owner route or follow-up surface instead of adding live cross-repo behavior here.

## Public hygiene

Assume everything here is public and portable.

Write for reuse:
- generalize paths
- generalize service names when they are not essential
- keep examples sanitized
- strip secrets and internal-only assumptions
- prefer small explicit contracts

## Security

Do not use public issues or PRs for leaks, secrets, credentials, or infrastructure-sensitive details.
If a contribution reveals sensitive material, sanitize it first or keep it out of the public repository.
