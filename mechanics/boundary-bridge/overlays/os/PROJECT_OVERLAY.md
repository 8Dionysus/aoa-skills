# OS Abyss overlay

## Purpose

This live overlay family groups `os-abyss-*` skills that adapt bounded skill practice to OS Abyss artifact-trust work: ABI, provenance, signatures, SBOM, C2PA, durable evidence, drift, and consumer gates.

It does not change the base skill boundary and does not turn `aoa-skills` into the authority for host runtime truth, trust roots, owner producer commands, or artifact registry mutation.

## Authority

- overlay family: `os`
- canonical overlay doc: `mechanics/boundary-bridge/overlays/os/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- host artifact-trust authority: `abyss-machine`
- MCP access plane: existing `abyss-machine` MCP read models
- proof authority: `aoa-evals`
- typed consumer/assertion layer: `aoa-sdk`
- session evidence routing: `.aoa`, without trust-policy authority
- owner producer truth: each owner repo route, manifest, producer profile, validator, and release command
- explicit approval rules: signing, evidence promotion, registry repair, trust-root mutation, privileged host actions, and release publication stay owner-authorized and outside the skill layer

## Local surface

- repository-relative skill bundle: `skills/project/abyss/os-abyss-artifact-trust-loop/`
- family review doc: `mechanics/boundary-bridge/overlays/os/REVIEW.md`
- bundle-local review checklist: `skills/project/abyss/os-abyss-artifact-trust-loop/checks/review.md`
- generated readouts: `generated/overlay_readiness.md`, `generated/governance_backlog.md`, `generated/mcp_dependency_manifest.json`, and generated skill export surfaces
- commands stay repo-relative, such as `PYTHONPATH=scripts python scripts/validation/validate_skills.py --skill os-abyss-artifact-trust-loop`, `PYTHONPATH=scripts python scripts/builders/build_catalog.py --check`, and the local MCP wiring validator
- artifact-trust runtime checks stay in `abyss-machine artifacts ... --json` and the existing read-only `abyss_machine` MCP surfaces

## Overlayed skills

- `os-abyss-artifact-trust-loop` - routes OS Abyss artifact-trust work through existing `abyss-machine` read models, owner-local producer routes, consumer trust gates, and proof surfaces without creating a second trust MCP

## Risks and anti-patterns

- do not widen the overlay into OS doctrine, release policy, or host-runtime authority
- do not hide signing, evidence promotion, registry writes, trust-root changes, service mutation, or `pkexec` behind skill wording
- do not create a second artifact-trust MCP when the existing `abyss-machine` MCP can expose read-only typed surfaces
- do not let `.aoa`, generated exports, or central matrices override owner-local producer commands and validators
- do not claim public C2PA production readiness without a real accepted credential and owner route
- do not treat this overlay as downstream adoption by OS Abyss organs until generated visibility, MCP wiring, owner validators, and OS-facing gates are verified

## Validation

- confirm the overlay does not change the base skill boundary
- confirm every listed overlay skill has a matching authored bundle and bundle-local review checklist
- confirm the family review doc mentions every matching `os-abyss-*` bundle
- confirm MCP dependency metadata points to the existing `abyss_machine` server and remains read-only
- confirm generated/export surfaces are rebuilt after source changes
- confirm downstream authority remains explicit and owner-local
