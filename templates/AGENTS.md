# AGENTS.md

Guidance for coding agents and humans working under `templates/`.

## Purpose

`templates/` stores public authoring scaffolds for `aoa-skills`. Templates teach the expected contract shape for skills, overlays, review surfaces, snapshots, and supporting manifests. They do not override live repository doctrine, schemas, or validators.

## Read this first

Before editing a template, read in this order:

1. `../AGENTS.md`
2. `../docs/REPOSITORY_STRUCTURE.md`
3. `../docs/BRIDGE_SPEC.md`
4. `../docs/OVERLAY_SPEC.md` when the template is overlay-related
5. the live source objects that the template is meant to model
6. any validator or test that currently checks the same contract

## Primary templates

The main template surfaces here are:

- `SKILL.template.md`
- `RUNTIME_EXAMPLE.template.md`
- `EVALUATION_SNAPSHOT.template.md`
- `PROJECT_OVERLAY.template.md`
- `PROJECT_OVERLAY_SKILL.template.md`
- `SKILL_COMPOSITION_EXCEPTION_REVIEW.template.md`
- `CANDIDATE_REVIEW.template.md`
- `STATUS_PROMOTION_REVIEW.template.md`
- `techniques.template.yaml`

## Allowed changes

Safe, normal contributions here include:

- clarifying placeholders and section guidance
- tightening required structure so templates match live contracts more clearly
- adding a new template when a repeated, reviewed pattern clearly exists
- aligning template wording with validators, docs, and current repository doctrine

## Changes requiring extra care

Use extra caution when:

- changing placeholder names or frontmatter keys
- changing status vocabulary or review-stage language
- changing required sections that validators or docs expect
- hard-coding a repository-specific assumption into a supposedly reusable template

## Hard NO

Do not:

- bake secrets, private paths, or internal URLs into templates
- turn a template into hidden project doctrine
- let template wording outrun the validators, docs, or schemas it is supposed to support
- remove placeholders just to make a template read like a finished artifact

Preserve placeholder intent. Keep examples repo-relative, public-safe, and obviously illustrative.

## Validation

After changing a template, run the smallest checks that cover the touched contract. In most cases that means:

- `python -m unittest discover -s tests`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_skills.py`

Run `python scripts/build_catalog.py` as well if the template change affects generated guidance or release prep expectations.

## Output expectations

When reporting work in `templates/`, include:

- which templates changed
- which live contract or validator the template was aligned with
- whether the change affects structure, wording, or both
- whether any follow-up is needed in docs, tests, or schemas
