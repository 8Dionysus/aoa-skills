# Loadout Posture

## Use When

Use this part when a reader needs to understand which pack profiles, trust
postures, adapter contexts, or overlay contexts are a sane fit for an ability.

## Do Not Use When

Do not use this part to create committed per-agent equipped state, slot counts,
gear inventory, cooldown systems, combo sequencing, or automatic selection
logic that bypasses trust and invocation policy.

## Route Check

- Which pack profile or trust surface already describes the subset?
- Is portable-only use realistic, or is a local adapter expected?
- Is the ability core, project-shaped, risk-heavy, or explicit-only?
- Does route-specific build advice belong in `aoa-playbooks`?

## Active Outputs

- loadout reader posture
- pack-profile hint
- adapter or overlay cue
- explicit-only or trust-policy cue
- no runtime inventory

## Next Route

Let existing pack profiles do the subset work first. Route build or rotation
method to `aoa-playbooks`, and route runtime state to the runtime owner.
