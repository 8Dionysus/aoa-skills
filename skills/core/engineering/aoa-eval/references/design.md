# Design bounded owner-local evaluation

### Mode: design

Use this mode after selection found no fit and the invariant, owner home, and
acceptance target are stable enough to shape runnable evidence. It is distinct
from local-need: design specifies a suite/report/fixture contract, while intake
records pressure that still needs owner review.

Procedure:

1. Return `blocked_missing_input` if the explicit invariant or behavior, target
   owner, local design path, acceptance target, or rejected surfaces is absent.
2. Restate the invariant and failure modes in observable terms.
3. Derive positive, negative, collision, and regression cases from manual
   examples. Preserve the raw manual cases as the truth from which automation
   may later be derived.
4. Choose the lowest-level deterministic evidence that constrains the
   behavior. Add trace or rubric review only where objective checks cannot
   observe the relevant judgment.
5. Separate temporary fixtures and exploratory probes from durable suite
   components. A validator is admitted only for a recurring stable invariant
   whose manual interpretation has stopped changing.
6. Select the effect independently from the design judgment. Place the design
   only when owner-local write authority is explicit and the local port admits
   that write. Otherwise return a read-only proposed design with effect
   `none`; a request to design does not itself authorize a file.
7. Keep both a placed and a proposed design inside the owner-local eval/report
   boundary.
8. Name exact runner inputs, outputs, artifacts, accepted outcomes, proof
   limit, cleanup, actual effect, and the owner-review route. When the design
   describes a surface that does not yet exist, a separately authorized owner
   implementation must create it. Then selection must inspect the resulting
   exact surface and produce a complete apply contract before apply may run it.
   Apply never creates a test, validator, suite, fixture, report, or runner.

Return a `local-eval-design`, not central proof acceptance. It must explain how
each automated check traces back to manual evidence and how false-green risk is
detected. Its next route is owner review, not direct execution of an absent
surface.
