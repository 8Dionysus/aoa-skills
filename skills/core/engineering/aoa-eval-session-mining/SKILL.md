---
name: aoa-eval-session-mining
scope: core
status: scaffold
summary: Mine .aoa session evidence for missed eval triggers only after web and repo owner surfaces are checked, producing candidate refs rather than proof.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0075
  - AOA-T-0067
  - AOA-T-0081
---

# aoa-eval-session-mining

## Intent

Use this skill to mine `.aoa` session evidence for missed eval-trigger moments,
candidate regression cases, and local eval pressure after external and repo
owner surfaces have already been studied.

## Trigger boundary

Use this skill when:
- the user asks to study sessions for eval moments, missed triggers, regressions,
  or repeated failures
- repo and web research has already defined candidate trigger classes
- `.aoa` search hits can reveal real prompts, failures, validations, or
  corrections that should become eval cases
- the output should be candidate evidence with raw/segment refs and freshness

Do not use this skill when:
- the task is only `.aoa` preservation, hook repair, or search-index maintenance
- a current repository source file can answer the question without session
  mining
- session evidence would be treated as reviewed proof
- memory writeback, decision records, or checkpoint closeout are the real owner
  routes

## Inputs

- trigger classes or target failure modes from prior research
- `.aoa` search index status, raw refs, segment refs, freshness, and diagnostics
- target repositories, touched paths, validators, tests, and local eval ports
- review criteria for candidate vs accepted evidence

## Outputs

- missed-trigger examples with session id, label, segment, event, raw ref, and
  freshness
- candidate eval-case themes and owner routes
- rejected examples and nearest wrong owner routes
- local intake or design handoff when evidence is strong enough

## Procedure

1. confirm the research gates: web sources, repo-local eval surfaces, and owner
   boundaries are already mapped
2. check `.aoa` search provider status and index freshness
3. run narrow searches by trigger class, not one broad vague query
4. inspect enough surrounding segment context to avoid false positives
5. classify each hit as candidate eval trigger, candidate local need, existing
   eval apply moment, non-eval validation, or wrong owner route
6. preserve raw and segment refs; do not summarize them into authority
7. hand off accepted candidates to `aoa-eval-local-need` or `aoa-eval-design`
   only after owner-route checks

## Contracts

- `.aoa` evidence is candidate evidence until reviewed
- session search must include freshness and refs
- raw transcript evidence cannot override source-owned repo files
- mining happens after owner boundaries are known, not as a replacement for
  source archaeology

## Risks and anti-patterns

- using session snippets as proof without source verification
- mining all sessions before trigger classes are defined
- confusing `.aoa` maintenance with eval mining
- turning repeated frustration into a generic eval without a reproducible case

## Verification

- confirm index freshness and provider
- confirm each example has session, segment, event, raw ref, and freshness
- confirm candidate owner route and rejected nearest wrong owner
- confirm no raw evidence was promoted to proof
- confirm next local need/design/apply route when applicable

## Technique traceability

Manifest-backed techniques:
- AOA-T-0075 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/continuity/donor-harvest/session-donor-harvest/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0067 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/history/history-artifacts/transcript-linked-code-lineage/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0081 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/recovery/diagnosis-repair/diagnosis-from-reviewed-evidence/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- `.aoa` search command and provider
- session ref format
- local intake handoff criteria
