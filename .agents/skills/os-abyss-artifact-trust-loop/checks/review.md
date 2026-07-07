# Review Checklist

## Purpose

Use this checklist when reviewing an OS Abyss ABI, provenance, signatures, SBOM, C2PA, durable evidence, drift, or trust-gate change that claims to follow `os-abyss-artifact-trust-loop`.

## When it applies

- a task touches artifact-trust requirements, producer profiles, durable evidence, sidecars, signatures, registry records, trust-gates, update lanes, C2PA posture, or generated trust surfaces
- an agent or installer wants to consume a bundle, container, model, runtime, media export, report, portable memory bundle, source seed, browser extension, or generated machine surface
- the review needs to confirm that MCP remained read-only and owner-local commands handled production or mutation

## Review checklist

- [ ] The artifact class and consumer intent are named, or the unknown class is marked `manual-review`.
- [ ] Requirements, producer profile, affected/drift, coverage, registry/latest, trust-gate, scenarios, and validate surfaces were inspected through MCP or equivalent CLI.
- [ ] The existing `abyss-machine` MCP remained a read-only typed access plane and did not build, sign, promote, repair, mutate registry state, change trust roots, run `pkexec`, or execute arbitrary artifact commands.
- [ ] Any sidecar generation, verify, sign, materialize, evidence promotion, release, update, OCI, or C2PA action used the owner-local route.
- [ ] The final posture preserves allow, warn, deny, or manual-review without flattening warn into green.
- [ ] Dirty repo state, sibling lag, stale evidence, source refs, digests, verifier versions, and lifecycle are labeled when they matter.
- [ ] C2PA public media claims stay warn or deferred unless a real production trust credential and owner route are present.
- [ ] Generated skill export and MCP dependency manifests were rebuilt when skill or adapter wiring changed.

## Not a fit

- ordinary local code edits with no artifact-trust consequence
- raw `.aoa` session search or memory rehydration that does not change trust policy or artifact consumption
- direct signing, evidence promotion, registry repair, service mutation, or public release without an authorized owner route
