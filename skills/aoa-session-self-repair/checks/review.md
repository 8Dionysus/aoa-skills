# Review Checklist

## Purpose

Use this checklist when reviewing work that turns a reviewed diagnosis into a
bounded `REPAIR_PACKET`.

## When it applies

- a diagnosis already exists and the next honest move is repair planning
- the reviewer must check checkpoint posture, rollback thinking, and owner-layer
  fit
- the route must stay smaller than a playbook-scale rollout

## Review checklist

- [ ] A reviewed diagnosis exists and is cited explicitly.
- [ ] The chosen repair is the smallest honest shape.
- [ ] The primary owner repo and artifact class are named.
- [ ] Checkpoint posture is explicit: policy fit, approval gate, rollback marker, health check, iteration limit, and improvement log.
- [ ] Validation and stop conditions are named.
- [ ] Escalation exists if the repair widens beyond one bounded unit.
- [ ] Role-law and proof-law changes were routed to the correct owner layers.
- [ ] No silent doctrine edit or approval bypass happened.

## Not a fit

- repair work without a reviewed diagnosis
- broad scenario rollouts that belong in `aoa-playbooks`
- vague self-improvement rhetoric with no bounded target
