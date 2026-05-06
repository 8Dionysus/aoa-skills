# Pattern Adoption Handoff

## Use When

Use this part when a shared pattern may become a bounded reusable skill, but
local owner adoption and skill-canon review still need to stay separate.

## Do Not Use When

Do not use this part to promote a technique into a skill automatically, approve
downstream adoption, rewrite technique truth, or make a routing layer author
meaning.

## Route Check

- What shared pattern is being proposed?
- Does the pattern need a technique, a skill, an overlay, a playbook, or an
  owner-local runbook?
- What local owner consent, shadow proof, rollback, and retention watch are
  needed before adoption?
- Does the proposal have enough bounded execution shape for normal
  `skills/**/SKILL.md` review?

## Active Outputs

- `skill_pattern_adoption_patch`
- skill-proposal cue
- technique or playbook handoff cue
- owner-consent requirement
- no automatic skill promotion

## Next Route

Route reusable practice truth to `aoa-techniques`. Route bounded execution
workflow changes through `skills/**/SKILL.md` review and generated catalog
validation. Route recurring scenario choreography to `aoa-playbooks`.
