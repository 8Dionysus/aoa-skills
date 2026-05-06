# Adoption Boundary

## Use When

Use this part when a shared pattern, candidate skill, or existing skill
requires explicit local adoption before it can become durable behavior.

## Do Not Use When

Do not use this part to approve adoption for another repository, bypass local
owner consent, replace release-support checks, or turn a shared pattern approval
into automatic activation.

## Route Check

- Is adoption being requested explicitly?
- Which local owner can consent, hold, reject, or quarantine the adoption?
- What readiness, shadow, decision, activation, rollback, and retention hooks
  are required before behavior becomes durable?
- Is the output only a compatibility report, or is an owner decision already in
  scope?
- Does direct Tree-of-Sophia runtime write, KAG-forced uptake, routing-layer
  authorship, or hidden assistant self-adoption need to be blocked?

## Active Outputs

- `skill_adoption_compatibility_report`
- owner-consent cue
- rollback and retention requirement
- quarantine fallback cue
- no owner acceptance by itself

## Next Route

Route owner decisions and durable receipts to
[Adoption Evidence Receipts](../adoption-evidence-receipts/README.md). Route
pattern-to-skill formation to
[Pattern Adoption Handoff](../pattern-adoption-handoff/README.md). Route
operator-facing consent or installation posture to experience or release-support
after direct reading.
