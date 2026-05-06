# Adoption Wave Distillation Log

## 2026-05-06

Direct-read source family:

- `docs/SKILL_ADOPTION_COMPATIBILITY.md`
- `docs/SKILL_ADOPTION_RECEIPTS.md`
- `docs/SKILL_ADOPTION_REGRESSION.md`
- `docs/SKILL_ADOPTION_RETIREMENT.md`
- `docs/SKILL_PATTERN_ADOPTION.md`

Decision:

- preserve the repetitive v0.7 downstream adoption wave docs as raw legacy
  under this package
- distill active behavior into four method-growth parts:
  adoption boundary, adoption evidence receipts, retention/regression/
  retirement, and pattern adoption handoff
- leave `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md` in place because it belongs to the
  later experience/polis-governance contour, not this adoption lifecycle slice

Stop-line:

- adoption lifecycle may require explicit owner consent, rollback, shadow
  proof, and retention watch; it does not grant owner acceptance, release
  approval, runtime activation, proof verdicts, or automatic skill promotion
