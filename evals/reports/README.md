# Local Reports

Store local run or review reports that explain skill-local eval pressure.

Reports here are evidence notes, not central verdicts, scoring, regression, or
proof doctrine. Route central proof adoption to `aoa-evals`.

Active local report notes:

Public-safe live-dispatch receipts may be written here only through the
field-whitelisting review action. Raw receipts remain in the host-private
temporary root and must not be copied into this directory.

- [aoa-skill-live-dispatch-smoke-20260711-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-needs-rerun.json)
  records the reviewed pre-turn strict-config transport failure that opened the
  rollout-budget reminder-list repair loop; it contains no model-quality
  evidence and explicitly requires a rerun.
- [aoa-skill-live-dispatch-smoke-20260711-output-schema-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-output-schema-needs-rerun.json)
  records the reviewed Responses API strict-schema rejection that followed the
  transport repair; the request reached the API but no model output was
  produced, so it also carries no skill-quality evidence.
- [aoa-skill-live-dispatch-smoke-20260711-trajectory-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-trajectory-budget-needs-rerun.json)
  records the first two completed model arms plus the root-child budget stop.
  The implicit pair remains candidate evidence, the structured arm did not run,
  and the full smoke requires a rerun before widening.
- [aoa-skill-live-dispatch-smoke-20260711-classification-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-classification-needs-rerun.json)
  preserves the reviewed four-arm receipt that exposed two classifier defects:
  a valid structured result was overridden by a late budget marker, and the
  expected root was treated as its own collision competitor. Its source-locked
  historical failure labels remain immutable evidence of the old classifier;
  they are not current verdicts, and the corrected harness requires a rerun.
- [aoa-skill-live-dispatch-smoke-20260711-control-contamination-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-control-contamination-needs-rerun.json)
  corrects the interpretation of the complete post-classifier smoke. Later
  `codex debug prompt-input` evidence showed a user-installed target skill in
  the supposed no-skill control and both user and repo copies in the aided arm;
  the run also lacked a uniform executable full-read/procedure path and used an
  ambiguous route/procedure grader. Its former trigger, trajectory, procedure,
  and no-lift labels are harness diagnostics only, not skill-defect evidence.
  The raw receipt remains immutable and a corrected smoke is required.
- [aoa-skill-live-dispatch-smoke-20260711-v2-cli-mcp-config-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-cli-mcp-config-needs-rerun.json)
  records the first protocol-v2 smoke after its 12/12 prompt gate passed. The
  first CLI arm then failed before model spend because per-MCP disable
  overrides synthesized incomplete transport-free tables alongside
  `--ignore-user-config`; it contains adapter evidence only and requires the
  same smoke to be rerun after the CLI isolation repair.
- [aoa-skill-live-dispatch-smoke-20260711-v2-control-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-control-budget-needs-rerun.json)
  records the repaired CLI run in which the aided arm completed exact
  selection, full read, and atomic verification, while the matched control
  legitimately followed the equal-background session-memory route and
  exhausted the former 28k cap on its required owner reads. It publishes no
  pair/lift and requires the same smoke under an equal 48k paired cap.
- [aoa-skill-live-dispatch-smoke-20260711-v2-native-load-contract-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-native-load-contract-needs-rerun.json)
  preserves the complete 48k v2 smoke. Its source-locked implicit
  positive-lift pair is candidate evidence and its root arm exposes a candidate
  missing-child-read gap, but the App arm used unsupported structured-only
  input. Its App `skill_load_gap` is a harness diagnosis, not a skill verdict.
- [aoa-skill-live-dispatch-smoke-20260711-v3-reviewed.json](aoa-skill-live-dispatch-smoke-20260711-v3-reviewed.json)
  records the first complete v3 smoke under its then-current grader. The
  implicit pair has candidate positive lift, the official App invocation passes
  native load, procedure, verification, and completion, and the explicit
  `aoa-eval` root selects
  `aoa-eval-apply` but does not full-read that child before following its
  procedure. The reviewed `skill_load_gap` routes back to the root handoff
  instruction and requires a same-case rerun after repair; it is not central
  proof or promotion evidence. Its fields remain source-locked to the v3
  grader and are not upgraded in place by later evidence semantics.
- [aoa-skill-live-dispatch-smoke-20260711-v3-read-command-ambiguity-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v3-read-command-ambiguity-needs-rerun.json)
  preserves the exact-merged-tree v3 rerun after the root handoff repair. Its
  first three arms exposed four harness defects: model self-report still gated
  objective load, an implicitly selected child escaped the read check,
  read-only inspection was ambiguous under the "one command" fixture wording,
  and a zero-return output-contract failure was mislabeled as transport
  failure. The report preserves those historical measures without endorsing
  them and supports no pair, lift, skill-effect, or family conclusion. Repeat
  the smoke under v4 before widening.
- [aoa-skill-live-dispatch-smoke-20260711-v4-external-source-contamination-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v4-external-source-contamination-needs-rerun.json)
  preserves the exact-merged-tree v4 rerun. The aided arm passed objective root
  and dynamic-child reads, but the control read a complete `aoa-eval` source
  file from an external canonical checkout before exhausting 48k. The public
  receipt immutably retains the historical `budget_exhausted` label; reviewed
  private command evidence places the earlier fault at filesystem-scope
  contamination. It supports no pair, lift, skill-effect, or family conclusion
  and requires a v5 fixture-scope rerun.
- [aoa-skill-live-dispatch-smoke-20260711-v5-chunked-read-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v5-chunked-read-needs-rerun.json)
  preserves the exact-merged-tree v5 rerun. Prompt and filesystem scope were
  clean and all four arms completed, but the aided target's complete source was
  read across two ordered exact-path outputs. The v5 single-output detector
  recorded a false `skill_load_gap` and no-lift result. Historical fields stay
  immutable; replay validates only the v6 detector repair, and a fresh
  exact-merged v6 smoke is required before widening.
- [aoa-skill-live-dispatch-smoke-20260712-v6-transport-timeout-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v6-transport-timeout-needs-rerun.json)
  preserves the exact-merged v6 rerun. Prompt visibility and fixture scope
  passed, but the first CLI transport reached its 180-second timeout before any
  turn event, output, usage, or pair. The private receipt stopped early while
  the historical v6 command still exited zero. This is transport and CLI-status
  evidence only; repeat after runtime availability under exact-merged v7.
- [aoa-skill-live-dispatch-smoke-20260712-v7-reviewed-route-lift.json](aoa-skill-live-dispatch-smoke-20260712-v7-reviewed-route-lift.json)
  preserves the complete exact-merged v7 smoke as reviewed candidate evidence.
  All four arms completed with clean prompt, fixture, load, procedure, and
  safety gates. Its generic `observed_lift=1` was derived only from
  route-contract correctness, so review accepts positive route lift and
  explicitly rejects completion or outcome-lift interpretation. V8 must repeat
  the same smoke with a pre-authored source-locked bounded outcome contract.
- [aoa-skill-live-dispatch-smoke-20260712-v8-outcome-answer-key-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v8-outcome-answer-key-needs-rerun.json)
  preserves the complete exact-merged v8 smoke and its historical source-locked
  grader output: positive route lift, negative outcome lift, and one
  `bounded_outcome_miss`. Review returned to the source contract and found that
  its key expected deflection of the unavailable whole repository task even
  though the constrained output and fixture define the scored disposition for
  the exact downstream procedure. The aided arm completed and verified that
  fixture procedure while separately preserving external owner stop-lines.
  The recorded negative outcome is therefore answer-key pressure, not a skill
  verdict; v9 corrects the scope from source and requires replay plus a fresh
  exact-merged smoke.

Corrected live receipts under the v9 evidence protocol are reviewable only
after canonical user-skill shadows, plugins, and every configured MCP id are
isolated with the adapter-appropriate mechanism (`--ignore-user-config` for
CLI exec, explicit per-id disables for prompt inspection and App Server);
prompt entry descriptions match the locked background; structured
`skills/list` exposes the exact unique 57-skill fixture map with zero MCP
startup; the official `$skill` text plus matching `skill` item is accepted;
native input acceptance remains separate from exact fixture-path full reads;
model `claims_loaded` stays separate from objective load; every expected or
dynamically selected child has a complete exact-path read; read-only inspection
commands remain allowed evidence rather than procedure commands; one complete
output or ordered continuously covering source chunks can prove that read,
while overlaps are accepted and gaps, reverse-only coverage, unrelated output,
inventory mentions, and shadow paths remain insufficient; zero-return
output-contract invalidity remains separate from transport failure; every
model command remains within the fixture root, with external or parent-path
access classified as contamination before budget; one atomic
guidance-bound validator event is proved; caught transport exceptions preserve
elapsed duration and partial private stdout/stderr so recoverable events retain
their normal precedence; incomplete stopped-early cohorts return nonzero after
their private receipt is written, while complete negative cohorts remain valid
executions; and invalid pairs are
omitted without rewriting arm history. Public v9 pairs name route lift and
bounded downstream procedure-outcome lift separately. Outcome lift is
scored only when both arms share the same source-locked case contract; missing
contracts are explicit `not_scored_no_contract`, the scope is not completion of
an external repository task, and the observed live answer never becomes its own
grader. Public validation rejects embedded absolute host
paths as well as raw prompts,
transport ids, and credential-shaped values. Retained v1/v2 smokes remain
historical `needs-rerun` evidence; retained v3-v8 reports keep their original
review status and grader semantics, including v4's budget label and v5's
single-output read label, while v6 keeps its zero-duration and wrapper-success
history, v7 keeps its generic route-derived lift, and v8 keeps its invalid
whole-task answer key rather than being rewritten in place.
- [aoa-eval-session-mining.report.md](aoa-eval-session-mining.report.md)
  records the first `.aoa` mining pass for `aoa-eval` trigger evidence and its
  proof limits.
- [aoa-eval-runtime-adoption-20260621.report.md](aoa-eval-runtime-adoption-20260621.report.md)
  records the local Codex runtime-adoption smoke for the `aoa-eval` front-door
  skill.
- [aoa-eval-self-awareness-contract-lane.report.md](aoa-eval-self-awareness-contract-lane.report.md)
  applies existing central eval surfaces to the `abyss-machine`
  self-awareness contract-lane episode as a local dogfood readout.
- [aoa-eval-battle-path-20260621.report.md](aoa-eval-battle-path-20260621.report.md)
  records an end-to-end local eval-port route through `aoa-evals-mcp`,
  `aoa-eval-apply`, deterministic skill checks, session refs, and post-write
  validation.
- [aoa-eval-prompt-trigger-harness-20260625.report.md](aoa-eval-prompt-trigger-harness-20260625.report.md)
  records the focused deterministic prompt-trigger harness for `aoa-eval`
  route correctness across front-door, subskill, negative, and owner-boundary
  cases.
