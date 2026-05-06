# Release Support

This package owns the `aoa-skills` side of portable release support: generated
exports, install profiles, local adapters, runtime seam contracts, guardrails,
support resources, release manifests, and compaction posture.

## Mechanic card

Status: `landed-local-route`.

### Trigger

Use this package when work touches `.agents/skills/`, portable export,
install/profile policy, runtime seam contracts, support resources, release
manifest, release procedure, trust gates, context retention, or compaction.

### Local owns

`aoa-skills` owns release-support contracts for packaging and portable skill
consumption.

### Stronger owner split

`abyss-stack` owns runtime infrastructure. `aoa-sdk` owns typed workspace
helpers. Host runtimes own host behavior. Generated exports never replace
authored `skills/**/SKILL.md`.

### Inputs

- canonical skill bundle change
- export or adapter drift
- install/profile or trust-policy change
- support-resource change
- release-manifest or release-process change

### Outputs

- refreshed export or support contract
- release-support validation route
- install, adapter, guardrail, or runtime seam readout
- no runtime activation or release approval by itself

### Must not claim

- generated export as source truth
- public release approval without release route
- runtime behavior authority
- downstream install success without evidence

### Validation

Use [AGENTS](AGENTS.md#validation).

### Next route

Start with [DIRECTION](DIRECTION.md), [PARTS](PARTS.md), and the relevant doc
under [docs](docs/README.md). Use [PROVENANCE](PROVENANCE.md) and
[legacy waves](legacy/waves/README.md) for older wave accounting.

## Active route

- [Direction](DIRECTION.md)
- [Parts](PARTS.md)
- [Provenance](PROVENANCE.md)
- [Landing Log](LANDING_LOG.md)
- [Roadmap](ROADMAP.md)
- [Docs](docs/README.md)
