# atm10-demo Project Overlay

## Overlay target

- downstream repository family: `atm10-demo`
- overlay family: `atm10-*`

## Base skill surface

- base canon: `aoa-skills`
- example base skills: `aoa-change-protocol`, `aoa-source-of-truth-check`
- this overlay does not change the base skill boundary; it only binds local execution details

## Local authority and approvals

- downstream approval posture is explicit and local
- local maintainers decide whether project-specific commands are safe to run

## Local paths and commands

- keep every path repository-relative to the downstream repo
- example docs surface: `README.md`, `docs/ARCHITECTURE.md`, `docs/BRIDGE_SPEC.md`
- example commands: `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`

## Local verification

- confirm the overlay remains thin and public-safe
- confirm local commands are still reviewable before execution

## Non-goals and boundaries

- do not widen this overlay into project doctrine or a full playbook
- do not hide private paths, secrets, or internal-only operations
- keep any richer downstream adaptation as a future stub rather than live scope expansion
