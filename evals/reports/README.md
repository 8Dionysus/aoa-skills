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

Corrected live receipts under the v2 App Server protocol are reviewable only
after canonical user-skill shadows, plugins, and every configured MCP id are
isolated with the adapter-appropriate mechanism (`--ignore-user-config` for
CLI exec, explicit per-id disables for prompt inspection and App Server);
prompt entry descriptions match the locked background; structured
`skills/list` exposes the exact unique 57-skill fixture map with zero MCP
startup; exact fixture-path reads and one atomic guidance-bound validator event
are proved; and invalid pairs are omitted without rewriting arm history. Public
validation rejects embedded absolute host paths as well as raw prompts,
transport ids, and credential-shaped values. The retained complete smoke
remains source-locked to protocol v1 and `needs-rerun`.
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
