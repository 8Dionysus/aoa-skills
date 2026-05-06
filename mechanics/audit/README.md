# Audit

This package owns the `aoa-skills` side of audit mechanics: how skill evidence,
public readouts, trigger behavior, conformance, and repository audit contracts
are read without turning them into proof authority.

## Mechanic card

Status: `landed-local-route`.

### Trigger

Use this package when work touches evaluation evidence, public-status readouts,
trigger and description activation checks, skills-ref conformance, status-review
evidence, or repository audit contracts.

### Local owns

`aoa-skills` owns audit routes over skill-layer evidence and generated readouts.
It may define how to read local evidence, where review records live, and which
checks must run before a local claim is repeated.

### Stronger owner split

`aoa-evals` owns proof doctrine and verdicts. `aoa-routing` owns routing policy.
`Agents-of-Abyss` owns center Audit mechanics. Generated readouts summarize
source surfaces and do not author truth.

### Inputs

- skill evaluation fixtures and matrices
- trigger and description activation cases
- public-surface and governance readouts
- review records
- repo-local audit contract changes

### Outputs

- audit route guidance
- local evidence-reading path
- validation command set
- review or follow-up target
- no proof, runtime, remediation, routing, or owner-acceptance authority

### Must not claim

- proof verdict
- public quality claim without support evidence
- downstream remediation authority
- runtime activation or routing sovereignty
- generated report as source truth

### Validation

Use [AGENTS](AGENTS.md#validation).

### Next route

Start with [DIRECTION](DIRECTION.md), [PARTS](PARTS.md), and the matching doc
under [docs](docs/README.md). Use [PROVENANCE](PROVENANCE.md) when auditing
how former flat docs moved here.

## Active route

- [Direction](DIRECTION.md)
- [Parts](PARTS.md)
- [Provenance](PROVENANCE.md)
- [Landing Log](LANDING_LOG.md)
- [Roadmap](ROADMAP.md)
- [Docs](docs/README.md)
