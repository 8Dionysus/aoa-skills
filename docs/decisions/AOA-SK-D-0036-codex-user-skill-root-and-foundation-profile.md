# Codex User Skill Root And Foundation Profile

- Decision ID: AOA-SK-D-0036
- Status: Accepted
- Date: 2026-06-13
- Owner surface: `config/skill_pack_profiles.json`

## Index Metadata

- Original date: 2026-06-13
- Surface classes: export/runtime, agent route, generated/readout
- Skill lanes: core/engineering, core/session-growth, risk, portable/export
- Mechanic parents: release-support
- Guard families: export/runtime, permission allowlist, install profile, source topology
- Posture: accepted Codex user-skill-root repair

## Context

Codex discovers user skills from `$HOME/.codex/skills`, while the AoA skill-pack
builders still treated the user scope as `$HOME/.agents/skills`. That mismatch
left the authored and exported AoA bundles healthy in this repository, but made
normal Codex sessions see only a small subset of AoA skills unless they were
manually copied or separately linked.

At the same time, installing all exported bundles into the top user root would
mix portable AoA foundation workflows with project-family overlays such as
`abyss`, `atm10`, and `titan`. The recursive source topology decision keeps
those overlay families distinct from portable core and risk guards.

## Options Considered

- Keep `$HOME/.agents/skills` as the user profile target and rely on manual
  compatibility links.
- Install every exported bundle into `$HOME/.codex/skills`.
- Make Codex user scope target `$HOME/.codex/skills` and add a curated AoA
  foundation profile for the top user root.

## Decision

Choose the third option.

Set the standard `user` install root in AoA export, install-contract, and
runtime-guardrail tooling to `$HOME/.codex/skills`.

Add `user-aoa-foundation` as the Codex top-root profile. It installs the
portable foundation needed across AoA sessions: reviewed session-growth skills,
core engineering skills, risk guards, the AoA eval chain, `aoa-commit-growth-seam`,
and `aoa-summon`.

Do not include project-family overlays in that profile. `abyss-*`, `atm10-*`,
and `titan-*` remain available through source/export and project-specific
profiles, not the global user root.

## Rationale

The top user root is a Codex runtime surface, not merely an AoA export artifact.
Pointing user-scope installs at `$HOME/.codex/skills` makes generated profiles,
install contracts, snippets, and permission allowlists match the place Codex
actually loads.

The curated foundation profile repairs daily AoA behavior without flattening
every project overlay into every session. That preserves the source topology
boundary between portable workflows and owner-family specializations while
still making the common AoA route skills available by default.

## Consequences

- Positive: profile-based installs can refresh the live Codex user skill root
  without hand-copying bundles.
- Positive: generated config snippets and permission allowlists now describe
  the same user root as the installer.
- Positive: project overlays stay visible as project overlays instead of
  becoming global default behavior.
- Tradeoff: hosts that intentionally consumed `$HOME/.agents/skills` as their
  Codex user root need an explicit compatibility profile or destination override.
- Follow-up: if another runtime still needs `.agents/skills` as a user root,
  add a named legacy/compatibility profile instead of moving the default back.

## Current Applicability

As of 2026-06-13:

- Still valid: source skills remain under `skills/**`, and generated portable
  export remains under `.agents/skills`.
- Still valid: `$HOME/.codex/skills` is the Codex user skill root for normal
  local sessions on this machine.
- Changed: user-scope install profiles no longer point at `$HOME/.agents/skills`.
- Not superseded.

## Review Log

### 2026-07-12 - Make non-invoke activation visible at the user root

- Trigger: the installed profile carried `implicit_activation_policy` and
  `aoa_invocation_mode` as generated metadata, but Codex routing primarily saw
  a description that still said `Use when`; live session-growth evidence
  exposed three false target-facing invoke reports.
- Decision: derive a leading activation sentence from the policy matrix during
  portable export. Manual skills require explicit invocation or a
  source-authorized parent selection; suggest skills may be recommended but
  not loaded implicitly; invoke descriptions stay unchanged.
- Boundary: keep authored descriptions in
  `config/portable_skill_overrides.json`; policy wording is an export/runtime
  contract, not duplicated prose in 45 overrides. Parent-selected decision and
  eval children remain valid explicit routes.
- Validation: compare catalog descriptions to exported SKILL frontmatter,
  enforce the 1024-character bound, rebuild every generated consumer, stage and
  inspect the foundation bundle, import it, verify 36/36 installed parity, and
  inspect live prompt input before rerunning the affected cohort.

### 2026-06-13 - Codex user-root repair

- Previous assumption: `$HOME/.agents/skills` was a suitable user-scoped
  install target.
- New reality: the active Codex session listed skills from
  `$HOME/.codex/skills`, so the old user root made profile installs invisible
  to Codex.
- Reason: AoA skills should be installed through the repo-owned profile and
  installer path that the runtime actually reads.
- Source surfaces updated: `config/skill_pack_profiles.json`,
  `scripts/export/build_agent_skills.py`,
  `scripts/bundles/skill_pack_install_contract.py`,
  `scripts/runtime/build_runtime_guardrails.py`,
  `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`, and
  `mechanics/release-support/docs/TRUST_GATE_AND_ALLOWLIST.md`.
- Validation: rebuild export, generated catalogs, runtime guardrails, decision
  indexes, and profile install/verify surfaces.

## Boundaries

This decision does not make project-family overlays global default skills. It
does not change the canonical authored source tree, and it does not make
generated `.agents/skills` the source of truth.

This decision also does not forbid a project or host from using a different
install destination when explicitly routed through a named profile or installer
override.

## Source Surfaces

- `config/skill_pack_profiles.json`
- `scripts/export/build_agent_skills.py`
- `scripts/bundles/skill_pack_install_contract.py`
- `scripts/runtime/build_runtime_guardrails.py`
- `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`
- `mechanics/release-support/docs/TRUST_GATE_AND_ALLOWLIST.md`

## Validation

- `PYTHONPATH=scripts python scripts/export/build_agent_skills.py --repo-root .`
- `PYTHONPATH=scripts python scripts/builders/build_catalog.py --check`
- `PYTHONPATH=scripts python scripts/runtime/build_runtime_guardrails.py --check --repo-root .`
- `PYTHONPATH=scripts python scripts/decisions/generate_decision_indexes.py --check`
- `PYTHONPATH=scripts python scripts/validation/validate_skills.py`
- `PYTHONPATH=scripts python scripts/bundles/verify_skill_pack.py --repo-root . --profile user-aoa-foundation --install-root /home/dionysus/.codex/skills`
