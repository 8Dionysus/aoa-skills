---
name: project-overlay-skill-name
scope: project
status: scaffold
summary: Project-local overlay for a bounded skill workflow.
invocation_mode: explicit-preferred
technique_dependencies: []
---

# project-overlay-skill-name

## Intent

Adapt a base skill to one repository family without changing the upstream technique meaning.

## Trigger boundary

Use this skill when:
- the target repository needs local paths, local commands, or local approval posture
- the base skill is still the right workflow, but the project shape needs a thin adaptation

Do not use this skill when:
- the task really needs a broader playbook
- the task would require new upstream technique meaning
- the work depends on live cross-repo fetches instead of local repository facts

## Inputs

- repository-local paths
- repository-local commands
- local approval rules
- base skill reference

## Outputs

- bounded project overlay guidance
- local commands or path adjustments
- reviewable verification notes

## Procedure

1. identify the base skill
2. state the local repository shape
3. adapt only the thin overlay surface
4. verify the overlay stays bounded

## Contracts

- preserve the base skill meaning
- keep paths and commands repository-relative
- keep approval posture explicit
- keep the overlay public-safe

## Risks and anti-patterns

- hiding project-specific authority inside vague prose
- widening the overlay into a scenario bundle
- copying upstream technique prose instead of adapting the skill

## Verification

- confirm the overlay still reads as a thin adaptation
- confirm the skill still points back to the base canon
- confirm the output remains reviewable by another human or agent

## Technique traceability

List the upstream techniques that shape the base skill and any local overlay notes that matter for this repository family.

## Adaptation points

- local paths
- local commands
- source-of-truth files
- approval rules
