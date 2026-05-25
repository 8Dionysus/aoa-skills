# Evaluation Snapshot

## Prompt

A live session corrected an owner-route mistake, the landed diff only shows the
final docs update, and the reason to remember it lives in `.aoa` search hits
plus a repo-local `memo/` port that can hold a candidate.

## Expected selection

use

## Why

The work produced a bounded memory-worthy owner-route correction whose evidence
lives in session refs as well as source refs, so the right move is writeback
routing rather than relying on the final diff alone.

## Expected object

A memo_writeback_decision of `write_candidate` with one local memo candidate,
source refs, .aoa evidence refs, review-required guardrails, and no direct
durable aoa-memo object.

## Boundary notes

Use this skill when session evidence explains why a landed change matters and a
local memo port can hold the reviewed-later candidate. Keep `.aoa` as evidence,
not memory authority.

## Verification hooks

The response should name the owner repo, keep the candidate local, include one
source ref and one `.aoa` evidence ref, validate the memo port, and stop before
durable reviewed memory landing.
