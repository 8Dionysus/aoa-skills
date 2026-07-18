# Audit invariant coverage

### Mode: coverage-audit

Use this mode when tests, validators, schemas, fixtures, reports, receipts,
generated parity checks, or proof surfaces already exist and the question is
which stable truths they actually constrain. Do not use it when the invariant
itself is unknown or the task is merely to run an already selected eval.

Required inputs:

- owner-authored stable truth and consumers relying on it
- current checks and their real execution paths
- manual expected, rejected, edge, and motivating failure cases
- known claim limits, input/state space, and available oracle

Return an `invariant-coverage-audit` containing an invariant-to-check map,
direct/indirect/example-only/absent/false-confidence classifications, concrete
gaps, smallest follow-up or no-change decision, claim limit, and stop line.

Procedure:

1. State each material invariant in plain language before reading green status.
2. Trace each current check to the code, artifact, or behavior that would make
   it fail. Do not infer coverage from a filename or test count.
3. Exercise the strongest expected and rejected cases manually. Record when a
   green check accepts behavior contrary to the owner rule.
4. Classify coverage as direct, indirect, example-only, absent, redundant, or
   false confidence and name downstream exposure.
5. Prioritize only the smallest uncovered stable risk. Do not turn the audit
   into a general test strategy or create automation unless a later authorized
   task adopts the gap.
6. Report exactly what the current surface proves and what it does not.

Operational shapes:

When the evidence surface is wider than an ordinary test suite, choose the
narrowest shape below. Map one stable invariant to one real failure path and
one claim limit; do not treat the table as a checklist.

| Shape | Existing surface | Invariant question | Gap to look for | Useful follow-up |
|---|---|---|---|---|
| Code test suite | Unit, integration, smoke, or regression tests. | Does behavior hold across the important input or state space? | Happy-path examples do not protect the stable rule. | Boundary, negative, property, or regression case. |
| Schema or manifest | JSON schema, YAML manifest, registry, config, or typed model. | Does structural validity protect the rule consumers rely on? | Required fields pass while semantic relationships remain unchecked. | Invalid fixture, enum drift check, or cross-field validation. |
| Fixture family | Golden files, snapshots, canned inputs, or sample repositories. | Do examples represent meaningful variation? | Many fixtures repeat the same shape. | One fixture per missing state, role, boundary, or failure mode. |
| Generated/export parity | Builder output, compact index, installed copy, adapter export, or capsule. | Does generated material remain derived from source truth? | Freshness passes while source-to-output meaning is unchecked. | Rebuild check plus source-ref, field-map, or stale-output failure. |
| Report or receipt | Markdown report, JSON receipt, run summary, status surface, or dashboard feed. | Does the report constrain the claim readers infer? | A complete-looking report overstates the verdict or hides exclusions. | Claim-limit assertion, required exclusion field, or malformed-receipt case. |
| Eval or proof result | Eval bundle, scorer output, verdict, benchmark result, or review gate. | Does the proof surface justify exactly the claim being made? | One score is treated as total quality or broad intelligence. | Claim-scope fixture, scorer edge case, or verdict-schema failure. |
| Router, SDK, or adapter compatibility | Dispatch hints, typed loader, SDK facade, CLI report, or adapter bridge. | Does compatibility preserve stable consumer assumptions? | Only the common route works. | Unsupported-shape fixture, error contract, or version case. |
| Workflow or role scenario | Playbook phase, handoff, role contract, session route, approval gate, or operator step. | Does the workflow guard the invariant under realistic route changes? | Scenario prose states a rule but no check catches a skipped gate. | Minimal route trial, handoff receipt, stop-condition, or negative path. |
| Memory, recall, or provenance surface | Recall object, writeback envelope, source reference, retention rule, or retrieval capsule. | Does evidence keep provenance and freshness limits clear? | Recall looks authoritative without source or freshness bounds. | Source-ref check, stale-recall case, retention invariant, or writeback envelope. |
| Metrics or source coverage | Coverage report, metric summary, source-count report, adoption audit, or dashboard. | Does the metric constrain the stable claim it supports? | Counts are treated as proof of quality, adoption, or completeness. | Denominator check, source gap, active-view rule, or exclusion case. |

Compact audit pass:

| Field | Answer |
|---|---|
| Stable invariant | |
| Existing surface | |
| Shape selected | |
| Evidence that directly constrains it | |
| Evidence that only repeats examples | |
| Claim limit | |
| Smallest useful follow-up | |
| Downstream reader risk | |

Contracts and risks:

- every coverage claim must resolve to a check path and independent oracle
- schema validity, report completeness, generated freshness, line count, and
  random input volume are not invariant evidence by themselves
- avoid abstract quality sermons, example counting, or post-hoc validators
  designed only to restore green status

Verify that another reviewer can follow the invariant-to-failure path, the gap
list is bounded, and the next move remains separate from the audit verdict.
