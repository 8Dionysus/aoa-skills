# Verify a broad property

### Mode: property

Use this mode when a real rule must hold across many inputs, artifacts, states,
transformations, lifecycle phases, route choices, or provenance chains and a
few fixed examples are materially too narrow. Do not use it when the rule is
unknown, a bounded contract is sufficient, or randomization adds no meaningful
variation.

Required inputs:

- owner-authored property and why broad variation matters
- valid domain or generator, preconditions, exclusions, edge cases
- independent oracle, known counterexamples, reproduction/shrink path
- artifact, lifecycle, source-ref, authorization, or compatibility bounds

Return a `property-evidence-package` containing the property, domain/generator,
oracle, cases, counterexamples, smallest authorized durable check or no-check
decision, claim limit, and stop line.

Procedure:

1. Separate a stable invariant from a hope or one example stated abstractly.
2. Prefer semantic properties such as conservation, monotonicity, idempotence,
   round-trip, uniqueness, source-ref preservation, lifecycle ordering,
   freshness bounds, or authorization limits.
3. Define a bounded, reviewable input/artifact/state domain with preconditions
   and exclusions; preserve a few concrete examples that explain failures.
4. Exercise manual boundary and counterexample cases before choosing a
   generator or durable harness.
5. Define an oracle independent from the implementation and a deterministic
   reproduction or shrink path. Once a minimal reproducible counterexample
   falsifies the universal property, stop expanding or rerunning the same
   failure class. Continue only to separate another independent property,
   establish reproduction/shrink, or bound a positive subdomain.
6. Add a property check only when recurrence, domain, oracle, and write
   authority are all present; otherwise return a no-check or blocked decision.

Operational shapes:

When the property is wider than one ordinary data rule, choose the narrowest
shape below. Use one stable truth, one meaningful variation space, one
independent oracle, and one claim limit; do not treat the table as a checklist.

| Shape | Protected truth | Variation space | Property | Avoid | Useful check |
|---|---|---|---|---|---|
| Conservation or accounting | Totals, balances, references, or counts remain conserved. | Operation sequences, grouped artifacts, filtered subsets. | Sum, count, or reference relation stays equal under valid operations. | Counting examples while missing state sequences. | Stateful property plus boundary examples. |
| Monotonicity or ordering | Progress, version, priority, timestamp, or maturity moves only in allowed directions. | Status transitions, append-only logs, sorted lists, version bumps. | Movement never reverses or violates ordering rules. | Assuming newer data is automatically better or authoritative. | Transition sequence with invalid-reversal cases. |
| Idempotency or repeatability | Repeating a safe operation does not change meaning after the first run. | Rebuilds, imports, normalization, refreshes, retries. | Same source and options produce an equivalent result. | Ignoring timestamps, nondeterministic IDs, or environment effects. | Repeated-run property with stable fields and explicit exclusions. |
| Round trip or normalization | Parse, serialize, import, export, or normalize preserves intended meaning. | Encodings, field order, optional values, aliases. | `decode(encode(x))` or normalized variants preserve semantic fields. | Treating formatting bytes as meaning unless required. | Round-trip fixtures plus generated optional-field cases. |
| Structural or schema relationship | Required relationships between fields or nodes remain valid. | Manifests, trees, graphs, references, nested objects. | IDs are unique, refs resolve, and parent/source/output links hold. | Schema validity without relationship checks. | Generated variants with invalid-ref negative cases. |
| Lifecycle or state machine | Objects move only through allowed states and evidence gates. | Candidate/evaluated/canonical, pending/active/closed, draft/released/deprecated. | Every transition is allowed and required evidence appears at gates. | Treating roadmap or provenance as current state. | Transition generator plus forbidden-transition examples. |
| Source to generated/export | Derived surfaces preserve source identity and remain subordinate. | Builders, compact indexes, installed copies, exports, reports. | Eligible sources appear once, refs survive, and excluded sources stay out. | Generated freshness as proof of source meaning. | Rebuild/idempotency property plus source-ref and exclusion checks. |
| Routing or selection | Selection is stable under irrelevant variation and changes under decisive signals. | Dispatch hints, filters, priority rules, compatibility choices. | Equivalent inputs route alike; changing the decisive signal changes the result. | Encoding incidental ordering as law. | Permutation/irrelevant-field property plus tie-break examples. |
| Authorization or risk boundary | Unsafe actions require explicit authority or a safer fallback. | Mutation surfaces, share targets, infrastructure actions, risk tiers. | A risky route cannot proceed without the required approval or gate output. | Using property language to bypass human approval. | Generated deny/allow cases with the real guard as oracle. |
| Provenance or memory/recall | Retrieved, stored, or derived evidence keeps source and freshness limits clear. | Recall objects, writebacks, capsules, summaries, retention windows. | Source refs, timestamps, retention bounds, and claim limits survive transformations. | Treating recall output as live proof. | Transformation property plus stale or missing-source negative case. |

Compact invariant pass:

| Field | Answer |
|---|---|
| Stable truth | |
| Shape selected | |
| Variation space | |
| Valid inputs | |
| Exclusions | |
| Property statement | |
| Independent oracle | |
| Reproduction or shrink path | |
| Concrete examples retained | |
| Claim limit | |

Contracts and risks:

- generated data volume is not evidence when the generator misses important
  states or the oracle repeats the implementation
- broad input coverage never implies total quality or unbounded lifecycle
  coverage
- avoid harness complexity, unreviewable generators, weak tautologies, and
  turning every stable example into a property

Verify the protected owner rule, meaningful variation, bounded domain,
independent oracle, reproducible failure, and explicit claim limit.
