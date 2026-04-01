# Ability Loadout Posture

## Purpose

This note explains the honest second-wave meaning of "loadout" inside `aoa-skills`.

In this wave, a loadout is not runtime inventory and not per-agent equipped state. It is a reviewable subset posture derived from existing skill pack and trust surfaces.

## Honest sources

Use the existing repo-owned surfaces first:

- `config/skill_pack_profiles.json`
- `config/skill_policy_matrix.json`
- `generated/skill_pack_profiles.resolved.json`
- `generated/trust_policy_matrix.json`
- `generated/local_adapter_manifest*.json`
- `generated/skill_runtime_contracts.json`
- `generated/tiny_router_candidate_bands.json`

These already describe subsets, trust gates, runtime posture, and install / activation context.

## What "loadout" means now

In this second wave, loadout posture may say:

- which pack profiles are a sane fit for an ability
- whether portable-only use is realistic
- whether a local adapter is optional or expected
- whether the ability is core, project-shaped, or risk-heavy
- whether activation should remain explicit-only

That is enough for a reader layer. It is not enough for a runtime equipment system, and this wave should not pretend otherwise.

## What stays out

Do not add:

- committed per-agent equipped state
- slot counts or gear inventories
- cooldown or resource systems
- route-specific combo sequencing
- automatic selection logic that bypasses trust and invocation policy

If later work needs route-specific builds or rotations, that contour should open in `aoa-playbooks` as scenario method, not here as pseudo-inventory.

## Final rule

Let existing pack profiles do the honest subset work first. A second-wave RPG loadout is a reader hint over those sources, not a new control plane.
