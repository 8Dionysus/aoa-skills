# Manifests District

Root `manifests/` is a route district, not a catch-all home.

Manifest records live with the package or part that owns the behavior they
describe. Root `manifests/` exists so future registries or route cards have a
stable place without forcing component records back into the root.

## Current Homes

| Manifest family | Home |
|---|---|
| Skill recurrence component and hook bindings | `mechanics/recurrence/manifests/` |
| Agon recurrence component and hook bindings | `mechanics/agon/parts/recurrence-observation/manifests/` |

## Owner Route

Use [AGENTS](AGENTS.md) before editing. Choose the owning package first, put
records under that owner rather than root, and keep provenance, tests, and
generated consumers aligned.
