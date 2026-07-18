# Apply an exact evaluation surface

### Mode: apply

Use this mode only after selection supplies the exact surface, owner/source,
command, prerequisites, artifacts, accepted exits, and pass criteria.

Procedure:

1. Read only the supplied selection packet and perform this complete preflight
   before reading the selected source, prerequisites, command implementation,
   or owner evidence:

   | Required dotted field | Valid only when |
   |---|---|
   | `verdict` | exactly `exact_fit` |
   | `owner` | explicit and non-empty |
   | `source_ref` | explicit and non-empty |
   | `source_digest` | explicit, non-empty, and checkable before execution |
   | `environment` | explicit object describing the required execution environment |
   | `command.argv` | non-empty list of exact string arguments |
   | `command.cwd` | explicit owner-relative or absolute working directory |
   | `command.timeout_seconds` | explicit positive number |
   | `command.accepted_exit_codes` | explicit non-empty list of integers |
   | `prerequisites` | explicit list, including an explicitly empty list when none exist |
   | `artifacts` | explicit list, including an explicitly empty list when none are expected |
   | `pass_criteria` | explicit non-empty acceptance object |
   | `effect_authority` | explicit authority covering the requested effect |
   | `expected_effect` | explicit effect allowed by `effect_authority` |
   | `proof_authority` | explicit boolean |
   | `proof_limit` | explicit and non-empty |

   Record `present_valid` or `missing_or_invalid` for every row. Do not infer a
   default cwd, timeout, accepted exit, empty list, effect, or proof posture
   from conventions, prose, another field, the command implementation, or the
   likely process result. In particular, `pass_criteria.process_exit` does not
   supply `command.accepted_exit_codes`.
2. If any row is `missing_or_invalid`, return
   `blocked_missing_input` naming every exact dotted field and stop. Report
   actual effect `none`. Do not read the selected source or prerequisites, run
   a probe or command, create a receipt, or substitute a fixture, wrapper, or
   broader gate.
3. Confirm the owner root, source ref, and source digest. When exact merged
   evidence is needed,
   use a clean exact tree rather than changing a dirty canonical checkout.
4. For `evals/suites/<slug>.suite.json`, run the current owner validator just in
   time and require `source-contract-ready`. Inventory or MCP read models may
   inspect a sidecar but may not execute it.
5. Compare the exact command's declared effects with its effect authority
   before execution. A stdout-only command may have effect `none`; generated
   artifacts require `generated-write`; an owner-local execution receipt
   requires explicit `owner-local-write`. Do not invent a receipt or another
   write merely because apply mode was selected.
6. Execute only the validated argv, cwd, timeout, accepted exits, and declared
   effects. Capture interpreter, dependency/config posture, ambient plugins,
   and relevant environment before interpreting the result.
7. Capture stdout, artifacts, actual effects, unexpected drift, source head,
   and sidecar digest. Keep an authorized execution receipt owner-local and
   private by default; omit it when the exact contract authorizes no write.
8. Inspect output and artifacts manually against the acceptance contract.
9. Classify separately: process exit, invariant satisfaction, evidence class,
   reproducibility posture, and central-proof limit.
10. If execution exposes missing coverage, hand off to local-need; if a stable
   invariant needs new coverage, hand off to design.

Return an `evaluation-observation` with exact command/environment/source,
artifacts, actual effects, drift, skipped checks, verdict, proof limit, and next
route.

For a blocked preflight, return the preflight state, exact missing or invalid
field paths, actual effect `none`, proof limit, and the stop line instead of an
`evaluation-observation`.

Applying an eval cannot promote central proof, and live output cannot rewrite
the source contract or its tracked hashes.
