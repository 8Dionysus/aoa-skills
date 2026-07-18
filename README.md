# aoa-skills

`aoa-skills` is the source repository for the AoA capability ecosystem and its
portable agent skill bundles.

The current architecture separates:

- a semantic capability tree for discovery;
- typed graph relations for compatibility and composition;
- a task-local DAG for one request;
- nine shared host-callable source bundles with evidence-gated visibility;
  repository-owned bundles remain with their owners and join the OS user
  profile without transferring procedure truth here.

## Start here

| Question | Surface |
| --- | --- |
| what this repository owns | [CHARTER.md](CHARTER.md) |
| how the capability system works | [DESIGN.md](DESIGN.md) |
| authored capability contracts | [capabilities/README.md](capabilities/README.md) |
| callable bundles | [skills/README.md](skills/README.md) |
| sibling repository skill homes | [docs/HOME_SKILL_PORT.md](docs/HOME_SKILL_PORT.md) |
| current lifecycle disposition | [docs/reviews/2026-07-15-capability-family-lifecycle.md](docs/reviews/2026-07-15-capability-family-lifecycle.md) |
| compact agent index | [SKILL_INDEX.md](SKILL_INDEX.md) |
| generated projections | [generated/README.md](generated/README.md) |
| portable release and handoff | [mechanics/release-support/README.md](mechanics/release-support/README.md) |
| local KAG projection | [kag/README.md](kag/README.md) |
| validation topology | [docs/validation/README.md](docs/validation/README.md) |

## Source-to-use path

```text
capability sources + SKILL.md
        -> deterministic capability graph and portable export
        -> host discovery or KAG retrieval
        -> compatible task-local DAG
        -> execution and manual outcome review
        -> candidate revision, promotion, demotion, merge, split, or removal
```

Techniques are optional provenance only. Runtime state, session traces, proof,
retrieval policy, workflows, and project facts remain with their owners.

## Verification posture

Manual trials decide usefulness. Automated checks only preserve stable
structural and packaging invariants learned from those trials. See
`config/validation_lanes.json` for current commands.
