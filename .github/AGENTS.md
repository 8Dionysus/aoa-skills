# AGENTS.md

## Applies to

This card applies to `.github/` and GitHub-native workflow, issue, PR, and repository automation files in this repository.

## Role

Keep GitHub landing support aligned with root `AGENTS.md` without making GitHub configuration the source of skill-layer truth.

## Read before editing

Inspect the changed workflow or template. Use `DESIGN.AGENTS.md` for card-shape
changes; for release behavior inspect `release_check.py` and its callers.

## Boundaries

Do not encode skill meaning, status promotion, or generated-surface authority in GitHub files. GitHub workflows may verify repository claims; they do not author those claims.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local
card may name only focused owner checks, lane ids, or the nearest route for the
changed surface. Select the narrowest matching lane, then use the explicit
[`GitHub`](../VALIDATION.md#github) route for release-facing workflow changes
or wording-only templates.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Platform Sync

Keep `.github/CODEOWNERS`, PR templates, workflow names, and root landing
expectations aligned.

`Repo Validation` is the landing check expected by the root GitHub workflow.
`build-validate` is also a live required check in branch protection, so the
portable-export workflow must keep reporting a completed check even when export
work is skipped for growth-safe PRs. If either check is added, renamed, skipped,
or its meaning changes, update the root route, PR expectations, and this file in
the same change.

Report the GitHub surface touched, local validation run, CI-name impact, and
remaining platform risk.
