# Adaptive Orchestration

## Use When

Use this part when a request touches more than one plausible skill, ring, or
post-session promotion lane and the agent needs to decide what applies now,
what defers, and what belongs to closeout or harvest.

## Do Not Use When

Do not use this part to run every skill in a ring mechanically, to skip
closeout, to force harvest before evidence exists, or to replace canonical skill
instructions.

## Route Check

- Are task execution, closeout, and harvest separated?
- Does each relevant skill have `apply_now`, `defer`, or `skip`?
- Are defer and skip reasons explicit?
- Did any reusable candidate survive closeout?
- Is the next owner layer named?

## Active Outputs

- applicability map route
- closeout check
- harvest trigger signal
- explicit next owner layer
- no promotion verdict by itself

## Next Route

Use checkpoint, method-growth, questbook, or the explicit session-harvest family
only when the evidence matches that next route.

Source doc:

- [Adaptive Skill Orchestration](../../docs/ADAPTIVE_SKILL_ORCHESTRATION.md)
