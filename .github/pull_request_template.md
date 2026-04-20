## PLAN
<!--
- restate the task
- list touched or inspected skills or surfaces
- name the main risk: boundary, bridge drift, status/evidence, overlay, or public hygiene
-->
- ...

## DIFF
<!--
- say what changed
- say whether skill meaning changed or only metadata/docs/generated surfaces changed
- say whether technique dependencies or invocation posture changed
-->
- ...

## VERIFY
<!--
- `python scripts/release_check.py` status
- `build_catalog`, `validate_skills`, `report_skill_evaluation`, `inspect_skill`, or drift commands actually run
- `pytest` modules actually run
- what was not run
-->
- ...

## REPORT
<!--
- current skill boundary after the change
- whether status, invocation mode, technique traceability, or overlay posture changed
- downstream follow-up likely needed in `aoa-evals`, `aoa-routing`, or a downstream project repo
-->
- ...

## RESIDUAL RISK
<!--
- upstream technique refs not yet refreshed
- generated surfaces not re-read
- overlay assumptions or evidence paths not exercised
-->
- ...
