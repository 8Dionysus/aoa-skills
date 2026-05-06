# Technique Traceability Path Refresh

Date: 2026-05-06

Status: accepted

## Context

After the mechanics reformation pass, the repository's full verification path
still failed on `scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift`.
The failure was not caused by mechanics movement. It came from old
`aoa-techniques` paths such as `techniques/agent-workflows/...` that no longer
exist after the `aoa-techniques` tree reform.

`aoa-techniques` owns reusable technique truth and current technique paths.
`aoa-skills` owns skill-side traceability references into that truth.

## Decision

Refresh skill technique traceability from
`../aoa-techniques/generated/technique_catalog.json` at current
`aoa-techniques` HEAD `cd276f040d55d490bd015b8698c7a5d594b9f875`.

For each non-pending `AOA-T-*` reference:

- update `skills/**/techniques.yaml` to the current `technique_path`
- update `source_ref` to the current `aoa-techniques` commit
- regenerate each `SKILL.md` technique traceability section from the manifest
- rebuild generated catalogs and the `.agents/skills` export
- update status-promotion review revision anchors for bundles whose source
  revision changed

Pending summon and titan technique references remain `TBD`.

## Follow-up

`aoa-techniques` commit `7f17c22ddd96de4b63873eff4c8e9e4c94a6aee9`
renamed the `AOA-T-0087` automation-readiness technique path from
`human-loop-to-seed-lift` to `human-loop-to-first-landing` and adjusted adjacent
automation-readiness wording. `aoa-automation-opportunity-scan` refreshes that
bounded automation-readiness group to the newer ref while preserving skill
meaning.

## Consequences

- `report_technique_drift` can compare against current `aoa-techniques` paths
  without missing-path runtime errors.
- Skill meaning is not changed; the change is traceability metadata and
  generated/export refresh.
- Review truth-sync revisions changed because `SKILL.md` traceability sections
  changed.

## Verification

Verify with:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_agent_skills.py --repo-root .
```
