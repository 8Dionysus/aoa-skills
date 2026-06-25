# Release-Support Manifests

This directory carries release-support manifests owned by the mechanic package.

- `release_manifest.bundle.json` describes `generated/release_manifest.json` as
  an OS Abyss artifact bundle subject for the root `abyss-machine` verifier.
  It names the subject, lifecycle, and consumer registry contract; signing
  controls stay in `abyss-machine` artifact policy.

The local validation entrypoint is
`scripts/validation/validate_abyss_machine_artifact_bundle.py`. It is part of
the release lane; it builds sidecars, promotes durable release-ready evidence
with source and trust-root metadata, materializes the release-manifest subject
store, checks the consumer `trust-gate`, and rehearses missing ABI, wrong
external subject, unverified latest, materialized subject-store, and
revoked-record denial. Local OS Abyss runs may satisfy the verifier dependency
with `ABYSS_MACHINE_REPO_ROOT`, `~/src/abyss-machine`,
`/srv/AbyssOS/abyss-machine`, `ABYSS_MACHINE_PACKAGE_ROOT`, or an installed
`abyss_machine` package. The validator emits compact JSON by default; use
`--full-json` for nested verifier evidence capture.
