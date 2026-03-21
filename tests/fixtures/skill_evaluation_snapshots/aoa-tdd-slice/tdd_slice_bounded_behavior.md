# Evaluation Snapshot
## Prompt
Add a small behavior change that can be specified in tests before coding.
## Expected selection
use
## Why
A behavior change can be expressed as tests before implementation, and the task fits a bounded slice rather than a broad rewrite.
## Expected object
A small test-first slice with clear acceptance checks and a limited implementation surface.
## Boundary notes
Use this skill for a bounded change where tests can define the behavior first. Do not use it for exploratory work with unclear behavior.
## Verification hooks
The response should show a testable slice and keep the scope narrow enough for TDD.

