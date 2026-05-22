# aoa-skills Memo Port

This is the skill-layer local memory port for `aoa-skills`.

Use it for candidates, receipts, exports, and local notes that should be visible
to future agents without making `aoa-skills` the central memory authority.

| Path | Use |
|---|---|
| `PORT.yaml` | skill-layer port contract |
| `INDEX.md` / `index.min.json` | generated local read model over packets |
| `candidates/` | proposed memory claims with evidence refs |
| `receipts/` | accept, reject, validate, or forward traces |
| `exports/` | reviewed-intake packets for `aoa-memo` |
| `local/` | skill-layer memory notes that should remain local |

Default write mode: `write_candidate_only`.
