# Evaluation Snapshot

## Prompt
Prepare logs and diagnostics for a broader audience without leaking secrets, private paths, or internal identifiers.

## Expected selection
use

## Why
The material may contain sensitive detail, so the skill should sanitize it before sharing.

## Expected object
A public-safe summary or redacted version that preserves the lesson while removing sensitive surfaces.

## Boundary notes
The goal is safe sharing, not the underlying operational fix.

## Verification hooks
- mentions sensitive surfaces explicitly
- preserves the technical lesson
- removes or generalizes private detail
- keeps the result shareable for a broader audience
