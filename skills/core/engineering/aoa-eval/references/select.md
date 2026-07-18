# Select an evaluation surface

### Mode: select

Use this mode when no exact evidence surface has been selected for a named
invariant and acceptance target. Its effect is read-only selection; it does not
execute, design, or write intake.

Required inputs:

- target repo, touched paths, invariant, acceptance target, and source ref
- local `evals/` route when present and the bounded candidate inventory named
  by supplied paths, owner routes, or the touched behavior

Procedure:

1. If the target, invariant, acceptance target, source ref, or a bounded route
   to candidate surfaces is unavailable, return `blocked_missing_input`.
2. Read the target route law and local `evals/PORT.yaml` when present.
3. Inspect exact supplied paths first, then only candidate tests, validators,
   scripts, reports, schemas, or generated manifests declared by the owner
   route, local port, or touched behavior. Do not use repository-wide inventory
   merely to make the candidate list look complete. Use broad discovery only
   when the owner route leaves a required candidate location unresolved or the
   caller explicitly requested a repository-wide inventory.
4. Stop candidate discovery as soon as the inspected bounded inventory proves
   `exact_fit`, `partial_fit`, `nearest_wrong_target`, or `no_fit` for the named
   invariant and acceptance target. Do not read unrelated memo, closeout,
   session, decision, or other-domain evidence after the verdict is decisive.
5. Consult central `aoa-evals` only when the bounded local inventory points to
   reusable doctrine, a local-port standard, or a plausible matching bundle;
   do not consult it for completeness or let centrality outweigh owner fit.
6. Compare candidate surfaces by exercised invariant, command, prerequisites,
   expected artifacts, freshness, owner, and proof class.
7. Classify the result as `exact_fit`, `partial_fit`, `nearest_wrong_target`,
   `no_fit`, or `blocked_missing_input`; name why nearest alternatives fail.
8. Hand off to apply only for an exact fit with a complete execution contract.
   Hand off to local-need or design only after an explicit no-fit.

Return an `evaluation-selection` containing the verdict, chosen or rejected
surfaces, owner/source, freshness, proof class, and next route. A `no_fit`
result has no chosen evaluation surface; identify any gap document or manual
case only as supporting selection evidence.

Verify that no command ran, no design or packet was created, and missing input
was not converted into a guessed fit or no-fit.
