# Review Checklist

## Purpose

Review checklist for the `atm10` change-protocol overlay.
It checks that local ATM10 route evidence sharpens the base change workflow without making `aoa-skills` the owner of ATM10 runtime behavior.

## When it applies

- when a bounded change needs repo-relative paths and commands in an `atm10-*` repo
- when touched ATM10 docs, scripts, schemas, source modules, tests, workflows, or generated/export companions need route-card evidence before mutation
- when the family review doc and the local skill wording need to stay aligned

## Review checklist

- [ ] confirm `mechanics/boundary-bridge/overlays/atm10/REVIEW.md` still describes the same family posture
- [ ] confirm the ATM10 root route card and nearest nested `AGENTS.md` are named for every touched path
- [ ] confirm `docs/SOURCE_OF_TRUTH.md`, `docs/RUNBOOK.md`, or `docs/PRODUCT_EDGE_POSTURE.md` is referenced when docs, commands, support claims, or test tiers move
- [ ] confirm repo-relative files and commands are named explicitly
- [ ] confirm the base `aoa-change-protocol` meaning is unchanged
- [ ] confirm downstream authority remains explicit
- [ ] confirm the selected verification tier matches the touched ATM10 surface, or the skipped check is named with reason
- [ ] confirm dry-run or report-only posture remains default for automation and policy surfaces unless ATM10-owned evidence supports a stronger path
- [ ] confirm rollback or recovery posture is named before execution

## Not a fit

- not for broad playbooks or cross-repo orchestration
- not for code changes that do not need overlay adaptation
- not for changing live input events, service exposure, perception truth, retrieval/KAG truth, model-host posture, or operator automation authority without downstream ATM10-owned approval
- not for a pure document-authority question before a change plan exists; use `atm10-source-of-truth-check`
