# Evaluation Snapshot

## Prompt
Review an existing validation surface to see whether it really constrains the stable rule or only repeats examples.

## Expected selection
use

## Why
The task is to audit existing invariant coverage, not to invent a new invariant from scratch.

## Expected object
An invariant coverage audit that names the stable truth, maps current checks to it, and isolates the smallest bounded gaps.

## Boundary notes
Keep the answer focused on coverage strength. Do not widen into generic test strategy or contract review.

## Verification hooks
- names the stable truth under review
- maps existing checks to the invariant
- identifies bounded weak or missing coverage
- avoids turning the audit into open-ended discovery
