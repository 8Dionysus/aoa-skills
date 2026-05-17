# Review Checklist

## Purpose

Use this checklist when reviewing `titan-event-replay` output inside an explicit Titan service-cohort route.

## When it applies

- the operator invoked the Titan skill directly or requested an explicit Titan service-cohort step
- the output touches a receipt, gate, ledger, console, replay, bridge, or candidate-memory surface
- owner-repo truth, human judgment, or gate authority must remain stronger than the local artifact

## Review checklist

- [ ] The replay identifies source event stream, ordering assumptions, and gaps.
- [ ] Replayed state is marked derived and cannot open gates by itself.
- [ ] Receipt or ledger comparison is shown when available.
- [ ] Titan owner surfaces remain named or clearly implied by the route.
- [ ] Forge mutation and Delta judgment gates remain distinct and visible.
- [ ] Receipt, source, ledger, console, replay, approval, or memory refs are preserved when available.
- [ ] Candidate or derived artifacts are not promoted to owner truth.
- [ ] Missing approval, source refs, validation, or owner-route follow-up is treated as a stop line.
- [ ] No hidden background execution or auto-approval was introduced.

## Not a fit

- requests that infer approval from silence
- ordinary repo work with no explicit Titan route
- hidden execution or silent mutation
- memory canonization without owner confirmation
- proof, verdict, or role claims wider than the bounded evidence
