# Contributing to aoa-skills

Thank you for contributing.

## What belongs here

Good contributions:
- reusable Codex skills
- skill bundles that compose one or more public techniques into a bounded agent workflow
- skill templates and repository conventions
- validation or review helpers for skill bundles
- thin project overlay examples that clarify how a core skill adapts to a real repository

Bad contributions:
- private operational context
- secrets, tokens, or sensitive infrastructure details
- one-off prompts without reusable skill structure
- project-specific hacks with no adaptation notes
- undocumented scripts
- techniques that belong in `aoa-techniques` rather than here
- skills that duplicate a technique without adding Codex-facing workflow value

## Before opening a PR

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

Run the local validator before opening a PR:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_catalog.py
python scripts/validate_skills.py
```

`python scripts/build_catalog.py --check` should also pass before you open a PR.

To focus on one bundle while iterating:

```bash
python scripts/validate_skills.py --skill aoa-change-protocol
```

To inspect the current runtime path for one skill while authoring or reviewing:

```bash
python scripts/inspect_skill.py --skill aoa-change-protocol
```

To preview a manifest-driven `SKILL.md` refresh without rewriting files:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol
```

To apply that refresh, use explicit single-skill write mode:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol --write
```

The helper does not support repo-wide write mode in this pass.

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

`aoa-techniques` is the source of truth for public reusable engineering techniques.
`aoa-skills` is the Codex-facing layer that packages one or more techniques into an executable workflow.

If the contribution is primarily a reusable engineering pattern, publish or refine it in `aoa-techniques` first.
If the contribution is primarily an agent-facing workflow bundle, it belongs here.

## Preferred PR scope

Prefer:
- 1 new skill per PR
- or 1 focused refresh to an existing skill
- or 1 clear repository-level docs or template improvement

Promotion or maturity-changing PRs should also align with `docs/MATURITY_MODEL.md`
and `docs/PROMOTION_PATH.md`, and make the supporting evidence explicit.

## Recommended PR title format

- `skill: add <skill-name>`
- `skill: improve <skill-name>`
- `skill: refresh <skill-name> from techniques`
- `skill: add project overlay <skill-name>`
- `docs: refine repo guidance`
- `repo: improve templates or validation`

## Review criteria

PRs are reviewed for:
- bounded scope
- Codex usefulness
- traceability to techniques when relevant
- public safety
- reviewability of the final `SKILL.md`
- clarity of trigger boundary
- quality of risks and verification guidance
- coherence with repository philosophy

## Maturity and promotion

Status changes are governance changes, not cosmetic relabeling.
The repository-level promotion path lives in `docs/PROMOTION_PATH.md`.

When proposing a promotion step:
- state the current and target maturity status
- cite the evidence that supports promotion
- explain whether the runtime `SKILL.md` meaning changed
- name any remaining gaps that block the next maturity step
- add or update the public review record under `docs/reviews/status-promotions/`
- use `templates/STATUS_PROMOTION_REVIEW.template.md` for non-canonical promotion reviews
- make the review record explicit about machine-checkable floors and what still blocks the next status step

When proposing `canonical` specifically:
- ensure the skill uses `## Technique traceability`, not `## Future traceability`
- ensure `technique_dependencies` and `techniques.yaml` contain no pending IDs or `TBD` source refs
- ensure the skill has evaluation coverage in `tests/fixtures/skill_evaluation_cases.yaml`
- rely on existing validator checks for `explicit-only` policy correctness rather than bypassing them
- add or update the public review record under `docs/reviews/canonical-candidates/`
- use `templates/CANDIDATE_REVIEW.template.md` for new candidate-review records
- make the review record explicit about machine floors, whether the runtime meaning changed, and what still blocks the next maintenance step

## Drift and refresh

A skill may summarize or compose techniques, but it should not silently drift away from them.
When a source technique changes materially, dependent skills should be reviewed and refreshed.

A good PR should make it clear:
- which techniques are referenced
- whether the skill meaning changed
- whether only metadata changed
- whether project overlays also require updates

If you think a richer integration would need another repository, leave a local stub or TODO note instead of adding live cross-repo behavior in this repository wave.

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
