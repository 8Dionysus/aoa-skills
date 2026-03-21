# Evaluation Snapshot
## Prompt
Introduce a seam around a concrete dependency because business logic is tightly coupled to infrastructure and testing is hard.
## Expected selection
use
## Why
Business or domain logic is tightly coupled to a concrete dependency, and tests are hard to write because external concerns leak into the core logic.
## Expected object
A seam, port, or adapter boundary that reduces coupling to the concrete dependency.
## Boundary notes
Use this skill when the problem is dependency pressure at the edges, not a general boundary clarification problem.
## Verification hooks
The response should show the dependency seam and explain how it helps isolate core logic from infrastructure.

