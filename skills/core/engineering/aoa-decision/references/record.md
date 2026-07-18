### Mode: record

Record one accepted meaningful decision in its owner repository. Absorb the
former ADR-writing capability here without turning every change into an ADR.

### Input ABI

Consume `accepted-decision` with:

- explicit accepted choice and target owner
- context and durable problem
- material alternatives, including an explicit statement when no alternative
  shaped the choice
- rationale and accepted consequences or tradeoffs
- canonical decision home or owner route
- affected owner source surfaces and follow-up boundary
- explicit effect authority

Owner ID, template, index-builder, and validation details may be resolved only
from the target owner's current decision law.

### Admission gate

1. Confirm that a decision is accepted rather than proposed.
2. State what future reader would lose if only a commit, PR summary, review
   note, runbook, test, or incident note existed. If nothing material is lost,
   return `no_record_needed` immediately. Once the exact owner law and named
   lighter artifact establish that result, do not inspect unrelated decision
   records or indexes, look for a builder, compute before/after tree hashes,
   probe Git, or continue into duplicate-record discovery.
3. Use `find` logic narrowly to confirm that no adequate record already exists;
   do not load the `find` mode reference or start a second mode.
4. Require every material input above. Do not infer rejected options,
   rationale, consequences, owner, or placement from the chosen path.
5. When a material field is missing, return an inline incomplete draft with
   `[owner input required]`, `blocked_missing_input`, and no file effect. Write
   a draft file only when the caller explicitly authorizes that distinct
   effect and supplies its destination.

### Procedure

1. Read the target root and decision-lane law, local template, ID/index
   contract, and only the related records needed for placement and conflicts.
2. Choose the next ID from owner source files or the owner-declared source
   index. Never derive it from memory, another repository, or a generated
   federation view.
3. Select only boundary lenses that change interpretation or placement:
   decision object, owner/source, placement, evidence state, workflow context,
   lifecycle/time, portability/overlay, runtime/body, handoff/fan-out,
   risk/approval, scale, or lighter-artifact sufficiency. For each selected
   lens state what this record decides and what remains with a stronger owner.
4. Author one record in the owner's established format. Preserve at least:
   context, decision boundary, material options, chosen path, rationale,
   consequences, owner/source surfaces, status, and follow-up.
5. Keep evidence, generated output, planning, session, runtime, and audit
   material as context. None of them accepts the decision or becomes its
   governing source.
6. Before writing, confirm effect authority, target path, preservation of
   existing owner files, and the smallest intended diff. Use Git status only
   when the owner route is a Git workspace; in an explicit non-VCS fixture use
   direct file comparison and do not retry Git commands. Write only the owner
   source.
7. Run the owner-declared decision index builder, then its check and affected
   source validator. Never hand-edit a generated index.
8. Treat workspace graph or KAG refresh as a derived consumer handoff. Refresh
   it when an authorized owner route exists; otherwise report it as unresolved
   federation debt without weakening the authored record.

### Output ABI

Return `decision-record` with:

- disposition: `recorded`, `no_record_needed`, or `blocked_missing_input`
- canonical ID, owner, source path, status, and selected boundary lenses
- context, alternatives, choice, rationale, consequences, and source surfaces
- actual source and generated effects
- owner index/validation results, external refresh posture, skipped checks,
  residual uncertainty, and stop line

### Failure and termination

Stop before writing when acceptance, owner evidence, meaningfulness,
placement, required content, builder contract, or effect authority is missing.
Do not narrate a diff as rationale, import sibling-owner law, or report an
unbuilt index as current.
