# AGENTS.md

## Applies to

This card applies to the local eval port under evals/.

## Role

The port may preserve reusable evaluation needs and owner-safe suites after
manual trials establish that they are durable. Raw traces, one-session
reports, scratch runners, and promotion verdicts do not belong here.

aoa-evals owns central proof doctrine, scoring, regression, and adoption.

## Read before editing

Read the root route, evals/README.md, and evals/PORT.yaml. Start with a manual
comparison in session-local storage. Add a repository suite only when repeated
manual evidence exposes a stable owner invariant and a long-lived consumer.

## Boundaries

Keep raw prompts, transcripts, temporary runners, one-off reports, model
verdicts, and session-memory extracts outside the repository. Do not copy
central proof authority from aoa-evals into this port.

## Validation

Use the release_check lane from config/validation_lanes.json. A green local
suite protects only its named invariant and never proves that a skill improves
real outcomes.

## Closeout

Report the manual evidence that justified any durable admission, the exact
invariant retained, its owner and consumer, checks run, and temporary material
removed.
