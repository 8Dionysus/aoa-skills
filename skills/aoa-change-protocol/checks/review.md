# Review Checklist

## Purpose

Use this checklist when reviewing a non-trivial change that claims to follow `aoa-change-protocol`.

## When it applies

- the change touches code, config, docs, or operational guidance in a meaningful way
- the author claims the work stayed bounded and explicitly verified
- the review needs to confirm that the workflow was visible rather than implicit

## Review checklist

- [ ] The goal and touched surfaces are named before the change is applied.
- [ ] The main risk is stated, and rollback thinking exists before execution.
- [ ] The diff stays inside the declared scope and avoids unrelated cleanup.
- [ ] At least one explicit verification step was run, or a clear reason is given for intentionally skipping it.
- [ ] The final report names what changed, what was verified, and what remains risky or deferred.

## Not a fit

- tiny wording or formatting edits with no meaningful review or operational consequence
- tasks where a more specific risk skill should own the workflow
