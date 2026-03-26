# Fourth wave

Wave 4 turns the earlier activation shim into a full dedicated-tool runtime seam.

The shared surface remains `.agents/skills/*`, because that is the Codex-facing export and the most stable portability layer.

The new seam adds an AoA-specific middle tier:

1. discover
2. disclose
3. activate
4. protect during compaction
5. reactivate cleanly when needed

## Why this wave exists

The earlier waves solved export, policy, trigger quality, trust posture, install profiles, and basic activation.

What remained was the second-path runtime seam for local-friendly adapters that do not want to rely on raw file reads alone.

Wave 4 adds that seam without introducing a second authoring format.

## Main additions

- `scripts/skill_runtime_seam.py`
- `scripts/build_runtime_seam.py`
- generated discovery, disclosure, alias, tool-schema, session-contract, prompt-block, router-hint, and runtime-seam manifests
- wave-4 tests for discover/disclose/activate/session/compact flows

## Output philosophy

- Discovery stays light and prompt-safe.
- Disclosure gives policy, resources, and section summaries without dumping the full skill.
- Activation returns the full body, a structured wrapper, resource inventory, trust/runtime/context manifests, and optional session state.
- Session compaction preserves `must_keep`, `retain_sections`, and rehydration hints.
