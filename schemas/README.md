# Schema District

`schemas/` holds repo-wide machine-readable contracts used by public examples,
generated surfaces, validators, and skill-layer integration artifacts.

Schemas constrain shape. Owning docs, skills, mechanics, builders, and
validators still own meaning.

Mechanic-local schemas may live with a mechanic or part when the contract is
private to that surface. Root schemas remain appropriate when several packages,
tests, generated outputs, or public readers share the same contract.

Use `mechanics/ARTIFACT_TOPOLOGY.md` before adding or moving a schema that is
near a mechanic. If the schema only validates one mechanic package or part, keep
it with that owner.

## Owner Route

Use [AGENTS](AGENTS.md) before editing. Identify the owner surface for the
meaning, keep schema changes paired with examples and validators, and do not
loosen a schema only to quiet an example.

The `live-skill-dispatch-*` contracts validate the source plan, constrained
model output, private raw receipt, and public field-whitelisted projection for
the local live-dispatch harness. They carry no eval verdict or proof authority.
