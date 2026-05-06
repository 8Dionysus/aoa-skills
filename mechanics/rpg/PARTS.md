# RPG Parts

This file maps current RPG-shaped reader behavior to active `aoa-skills` parts.
It is not the AoA center RPG part map and not a replacement for skill canon.

## Part Map

| Part | Local function | Stronger owner route |
|---|---|---|
| [Ability Reader Boundary](parts/ability-reader-boundary/README.md) | keep skill ability cards derived from existing skill, evaluation, portable, adapter, overlay, and profile surfaces | skill bundles own meaning; generated cards remain reader companions |
| [Loadout Posture](parts/loadout-posture/README.md) | keep loadout as pack-profile and trust-policy reader posture rather than runtime inventory | `aoa-playbooks`, `abyss-stack`, and owner projects own scenario builds and live state |

## Active Part Contract

Every part keeps this active-route shape:

- `## Use When`
- `## Do Not Use When`
- `## Route Check`
- `## Active Outputs`
- `## Next Route`

## Provenance Bridge

Use [PROVENANCE](PROVENANCE.md) when an ability or loadout source route must be
audited. Active part docs should not carry generated snapshots or skill
inventories.

## Validation

Use the validation lane in [mechanics/rpg/AGENTS.md](AGENTS.md#validation) for
package commands.
