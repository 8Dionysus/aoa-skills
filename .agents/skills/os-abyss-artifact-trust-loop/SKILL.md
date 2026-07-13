---
name: os-abyss-artifact-trust-loop
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Route OS Abyss ABI, provenance, signatures, SBOM, SLSA/in-toto, Sigstore/Cosign, C2PA, TUF, SCITT, durable evidence, drift, producer profiles, and trust-gate work through existing abyss-machine read models and owner-local producer routes. Use when an agent needs to inspect or consume bundles, containers, models, runtimes, reports, media exports, source seeds, portable memory bundles, browser extensions, generated machine surfaces, or release artifacts without creating a second trust MCP or violating owner boundaries. Do not use for ordinary local edits, raw .aoa session search, or direct signing/promotion/registry mutation without an authorized owner route.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/project/abyss/os-abyss-artifact-trust-loop/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0001,AOA-T-0002,AOA-T-0028
  aoa_portable_profile: codex-facing-wave-3
---

# os-abyss-artifact-trust-loop

## Intent
Use this skill to route OS Abyss ABI, provenance, signature, SBOM, SLSA/in-toto, Sigstore/Cosign, C2PA, TUF, SCITT, durable evidence, drift, and trust-gate work through the existing `abyss-machine` trust plane without creating a second trust authority.

The skill gives agents one natural loop: detect the artifact class, inspect requirements, inspect owner producer routes, inspect affected or stale evidence, refresh evidence only through the owner route, then require a consumer trust-gate verdict before consumption or landing.

## Trigger boundary
Use this skill when:

- a task mentions ABI, provenance, signs, signatures, SBOM, SLSA, in-toto, Sigstore, Cosign, C2PA, TUF, SCITT, artifact trust, producer profiles, durable evidence, trust gates, registry latest, stale bundles, or drift across OS Abyss
- an agent needs to consume, build, release, update, or audit a bundle, container, model, runtime, report, media export, source seed, portable memory bundle, browser extension package, or generated machine surface
- MCP or skill automation must inspect artifact-trust state before an owner-local producer, installer, runtime, or agent consumes an artifact
- sibling repos may lag, a checkout is dirty, or source refs need explicit evidence labeling instead of false clean claims

Do not use this skill when:

- the task is an ordinary local test or code edit unrelated to artifact trust
- the task asks to invent new trust policy rather than follow current owner surfaces
- the request is only about `.aoa` session search, evidence routing, memory rehydration, or graph indexing
- the operator asks for direct signing, evidence promotion, registry repair, privileged host mutation, or release publication without a confirmed owner route and authorization

## Inputs
- artifact path, artifact class, or suspected artifact family
- consumer intent, such as `agent`, `installer`, `runtime`, `release_consumer`, or another owner-defined intent
- source repo, source ref, changed paths, dirty-state notes, or sibling lag context when known
- owner route cards, manifests, release docs, producer profiles, validators, and current `abyss-machine artifacts` output
- existing durable registry refs, sidecar paths, bundle dirs, eval reports, or C2PA/media evidence when provided
- OS posture such as local dev, host-managed key, GitHub OIDC, OCI signature, public release attestation, pre-organization, or future external accountability mode

## Outputs
- resolved or explicitly unknown artifact class
- requirements, producer profile, affected/drift, registry/latest, trust coverage, and trust-gate summary
- named owner route for build, verify, sign, sidecar refresh, evidence promotion, release, eval, or manual review
- allow, warn, deny, or manual-review posture for the requested consumer intent
- proof and validator plan covering local owner checks, OS-facing gates, and `aoa-evals` scenarios when behavior or trust claims change
- concise closeout naming verified controls, skipped checks, deferred blockers, stale evidence, dirty-state limits, and remaining risk

## Procedure
1. Read the nearest owner route before touching artifacts. Start from the owning repo `AGENTS.md`, local manifests, release docs, or validator surfaces. Use center or doctrine docs only as orientation, not as a replacement for the owner route.
2. Detect the artifact class. Prefer current `abyss-machine artifacts` requirements, classify, producer-profile, affected, or registry surfaces over guessing. If the class remains unclear, stop with `manual-review` posture instead of forcing a class.
3. Inspect read-only trust surfaces through the existing `abyss_machine` MCP when it is runtime-visible:
   - `abyss_machine_surface(name="artifact-trust-requirements", artifact_class=CLASS)`
   - `abyss_machine_surface(name="artifact-trust-producer-profiles", artifact_class=CLASS)`
   - `abyss_machine_surface(name="artifact-trust-affected", artifact_class=CLASS)`
   - `abyss_machine_surface(name="artifact-trust-affected", artifact_class=CLASS, source_repo=OWNER, source_ref=SOURCE_REF)` when source-ref or dirty-state evidence is known
   - `abyss_machine_surface(name="artifact-trust-coverage")`
   - `abyss_machine_surface(name="artifact-trust-coverage", source_repo=OWNER, source_ref=SOURCE_REF)` when coverage must be checked against a specific source-ref context
   - `abyss_machine_surface(name="artifact-trust-registry-latest", artifact_class=CLASS, consumer_intent=INTENT)`
   - `abyss_machine_surface(name="artifact-trust-gate", artifact_class=CLASS, consumer_intent=INTENT)`
   - `abyss_machine_surface(name="artifact-trust-scenarios")`
   - `abyss_machine_surface(name="artifact-trust-validate")`
4. If the MCP surface is unavailable, stale, or not yet reloaded in the current session, use the equivalent read-only CLI commands:
   - `abyss-machine artifacts requirements --artifact-class CLASS --json`
   - `abyss-machine artifacts producer-profiles --artifact-class CLASS --require-command-resolution --json`
   - `abyss-machine artifacts affected --artifact-class CLASS --json`
   - `abyss-machine artifacts trust-coverage --json`
   - `abyss-machine artifacts trust-coverage --source-root PUBLIC_SEED_ROOT --source-repo OWNER --source-ref SOURCE_REF --json` when separating installed public-seed evidence from a dirty source checkout
   - `abyss-machine artifacts registry-latest --artifact-class CLASS --consumer-intent INTENT --json`
   - `abyss-machine artifacts trust-gate --artifact-class CLASS --consumer-intent INTENT --json`
   - `abyss-machine artifacts scenarios --json`
   - `abyss-machine artifacts validate --json`
5. Compare MCP and CLI output when changing MCP behavior, access-plane wiring, or consumer admission. Treat mismatch as a route bug, stale runtime, or different `source_context.public_seed_root` until stronger evidence explains it.
6. If affected, drift, registry, or trust-gate output says stale, missing, rebuild, reverify, warn, deny, or manual-review, route to the owner-local producer commands. Do not use MCP to build, sign, promote, repair, mutate registry state, change trust roots, or run privileged host actions.
7. Produce or refresh evidence only through the owner route. Depending on artifact class this may include owner validators, sidecar generation, `verify`, `sign`, `materialize-subjects`, `evidence-promote`, OCI signing checks, update metadata checks, C2PA sidecars, or release bundle commands.
8. Require `trust-gate` allow or an explicitly preserved warn posture before consumption. Treat warn as a live warning with a reason, not as green. Treat deny as blocking. Treat missing class or missing registry evidence as manual-review or deny according to owner rules.
9. Run local owner validators and `aoa-evals` proof or negative scenarios when behavior, consumer admission, artifact policy, public claim, generated machine surface, or release posture changes.
10. Land only after local owner checks and OS-facing gates pass. If the repo is dirty and the route allows dirty work, carry explicit source-ref, dirty-state, digest, verifier-version, and lifecycle labeling in the evidence instead of demanding a fake clean checkout.

## Contracts
- Keep `abyss-machine` as authority for host enforcement, durable registry, trust gates, trust roots, update lane, and artifact policy read models.
- Keep the `abyss-machine` MCP read-only, typed, allowlisted, and bounded. It may inspect artifact-trust read models; it must not become a signer, builder, promoter, registry writer, privileged runner, or repair tool.
- Keep owner repos authoritative for producer behavior, source manifests, release commands, and validator meaning.
- Keep `aoa-sdk` as typed reader/assertion surface, not the producer of host truth.
- Keep `aoa-evals` as proof and negative-scenario authority when trust claims or consumer decisions need durable proof.
- Keep `.aoa` as session evidence routing, memory rehydration, and graph/index context. It is not trust policy authority and cannot override current owner files or live gates.
- Keep public media C2PA posture honest: pre-organization or non-trust-list credentials can support local integrity and warn/deferred evidence, not production-ready public trust claims.
- Keep TUF/update and SCITT/accountability lanes separate: TUF can be required for updateable artifacts; SCITT can be a future external accountability layer without blocking v1 unless an owner route requires it now.

## Risks and anti-patterns
- Creating a separate trust MCP when the existing `abyss-machine` MCP can expose the needed read-only surfaces.
- Turning MCP access into hidden build, sign, promote, registry-write, trust-root-change, `pkexec`, service restart, or arbitrary command execution.
- Treating a disk-present skill, generated file, or stale session prompt as runtime-visible without checking generated export and prompt/runtime visibility.
- Calling C2PA public media production-ready before OS Abyss has a real organization credential or accepted trust-list posture.
- Making fake ABI for living doctrine, prose, or source truth that has not become a machine-consumable artifact contract.
- Letting central matrices, sibling examples, or `.aoa` summaries replace owner-local producer commands and validators.
- Collapsing dirty repo state into a clean proof claim instead of labeling dirty source evidence honestly.
- Treating `warn` as success, or treating a narrow smoke test as full OS Abyss artifact-trust coverage.

## Verification
- Confirm the artifact class and consumer intent were named or explicitly marked unknown.
- Confirm requirements, producer profile, affected/drift, coverage, registry/latest, trust-gate, scenarios, and validate surfaces were inspected through MCP or equivalent CLI.
- Confirm arbitrary artifact commands are not reachable through MCP; only allowlisted typed read models are exposed.
- Confirm owner-local producer commands handled any build, verify, sign, materialize, evidence-promote, release, update, C2PA, or OCI action.
- Confirm `trust-gate` returned allow, warn, deny, or manual-review and the final recommendation preserved that verdict.
- Confirm representative classes are covered when auditing the whole OS plane: `public_source_seed`, `bootstrap_install_bundle`, `runtime_or_container_artifact`, `ai_model_or_runtime_bundle`, `aoa_sdk_python_distribution`, `aoa_session_memory_portable_bundle`, and `public_media_export`.
- Confirm C2PA public media remains warn or deferred when the only blocker is missing production trust credentials.
- Confirm generated/export skill surfaces and MCP dependency manifests were rebuilt when the skill bundle or adapter wiring changed.

## Technique traceability
Manifest-backed techniques:

- AOA-T-0001 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- Add owner-specific artifact classes only after the owner route has a real producer profile, required controls, and trust-gate behavior.
- Add generated machine-surface or sibling-repo drift checks through `abyss-machine artifacts affected` rather than hard-coding sibling topology in this skill.
- Add richer MCP helper prompts only as read-only route guidance. Keep mutation commands in owner CLIs and repo validators.
- Promote this scaffold only after forward tests show agents can complete the loop without guessing commands, violating owner boundaries, or turning warnings into green claims.
