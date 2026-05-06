# Runtime governance layer

## Raw seam versus governed seam

Raw seam:

- `scripts/skill_runtime_seam.py`
- fast, direct, useful for debugging
- does not by itself enforce repo trust or manage merged resource allowlists

Governed seam:

- `scripts/skill_runtime_guardrails.py`
- wraps the raw seam with trust, allowlists, and context protection
- is the better default for local-friendly adapters and smaller models

## Command map

### Discover through trust gate

```bash
python scripts/skill_runtime_guardrails.py discover \
  --repo-root . \
  --trust-store .aoa/repo-trust-store.json
```

### Trust the repository explicitly

```bash
python scripts/skill_runtime_guardrails.py trust \
  --repo-root . \
  --trust-store .aoa/repo-trust-store.json \
  --decision trusted \
  --reason "reviewed repo-local skills"
```

### Activate with guarded session state

```bash
python scripts/skill_runtime_guardrails.py activate \
  --repo-root . \
  --skill aoa-change-protocol \
  --session-file .aoa/skill-runtime-session.json \
  --explicit-handle '$aoa-change-protocol' \
  --trust-store .aoa/repo-trust-store.json
```

### Resolve merged allowlist paths

```bash
python scripts/skill_runtime_guardrails.py allowlist \
  --repo-root . \
  --session-file .aoa/skill-runtime-session.json
```

### Compact and rehydrate

```bash
python scripts/skill_runtime_guardrails.py compact \
  --repo-root . \
  --session-file .aoa/skill-runtime-session.json

python scripts/skill_runtime_guardrails.py rehydrate \
  --repo-root . \
  --session-file .aoa/skill-runtime-session.json \
  --include-activation-call
```
