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

The `live-skill-dispatch-*` contracts validate the source plan, pre-authored
selected-child/procedure-disposition expectations, separate bounded owner-action
outcomes, constrained model output, private raw receipt, and public
field-whitelisted projection for the local live-dispatch harness. Procedure
contracts do not turn the independent fixture probe or a model disposition
report into outcome evidence. Outcome contracts require one atomic
transport-observed candidate command and still do not claim whole-task
completion, an eval verdict, or proof authority. Public measures also keep
external-filesystem scope distinct from broad in-fixture inventory scope so a
later budget marker cannot erase either boundary.

The live plan additionally owns broad-cohort partition shape and the
source-locked second-confirmation flag. Its runner must prove that bounded waves
are disjoint, exactly cover their parent trial identities, remain inside the
declared turn and resource envelope, and cannot execute implicit pairs with
declared-only procedure or outcome posture. Receipt schemas enumerate the
reviewable parent and wave identifiers; that enumeration does not grant proof
or promotion authority.
