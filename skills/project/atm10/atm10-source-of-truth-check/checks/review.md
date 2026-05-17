# Review Checklist

## Purpose

Review checklist for the `atm10` source-of-truth overlay.
It checks that local ATM10 document roles become clearer without making the overlay a broader policy owner.

## When it applies

- when local docs and canonical guidance need explicit repo-relative ownership
- when active commands, archived/recoverable references, public status, support-profile claims, runtime-baseline notes, or local-only planning surfaces are getting mixed
- when the family review doc and the local skill wording need to stay aligned

## Review checklist

- [ ] confirm `mechanics/boundary-bridge/overlays/atm10/REVIEW.md` still describes the same family posture
- [ ] confirm ATM10 `AGENTS.md` and `docs/SOURCE_OF_TRUTH.md` were read before assigning authority
- [ ] confirm authoritative repo-relative docs are named explicitly
- [ ] confirm active/current, archived, generated/export, local-only, internal, and runtime-adjacent surfaces keep distinct roles
- [ ] confirm entrypoints such as `README.md` stay short and route to canonical homes where those exist
- [ ] confirm runnable commands route to `docs/RUNBOOK.md` and archived/recoverable references route away from the active runbook
- [ ] confirm the base `aoa-source-of-truth-check` meaning is unchanged
- [ ] confirm local review posture remains visible rather than implied
- [ ] confirm public-safe exclusions remain explicit for private paths, logs, hostnames, tokens, screenshots, local model paths, and tool-local config

## Not a fit

- not for purely code-local changes with no docs ambiguity
- not for broader policy design that should live outside the thin overlay
- not for deciding ATM10 runtime behavior, model-host selection, perception truth, service exposure, or operator automation authority
- not when the authoritative files are already clear and the remaining work is a bounded implementation change
