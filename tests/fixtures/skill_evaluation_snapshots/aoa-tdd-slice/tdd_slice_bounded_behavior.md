# Evaluation Snapshot
## Prompt
Add a small behavior change that can be specified in tests before coding.
## Expected selection
use
## Why
A behavior change can be expressed as tests before implementation, and the task fits a bounded slice rather than a broad rewrite. The slice may be code, CLI, builder, validator, generated/export, adapter, router, or workflow behavior as long as the behavior is observable.
## Expected object
A small test-first slice with clear acceptance checks and a limited implementation surface.
## Boundary notes
Use this skill for a bounded change where tests can define the behavior first. Do not use it for exploratory work with unclear behavior, or for source-of-truth authority confusion that should be resolved before testing.
## Verification hooks
The response should show a testable slice, keep the scope narrow enough for TDD, and point generated/export or workflow assertions back to the source-owned behavior under test.
