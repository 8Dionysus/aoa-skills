# Release-Support Manifests

This directory carries release-support manifests owned by the mechanic package.

- `release_manifest.bundle.json` describes `generated/release_manifest.json` as
  an OS Abyss artifact bundle subject for the root `abyss-machine` verifier.
  It names the subject and artifact class only; signing controls stay in
  `abyss-machine` artifact policy.

The local validation entrypoint is
`scripts/validation/validate_abyss_machine_artifact_bundle.py`. It is part of
the release lane; local OS Abyss runs may satisfy the verifier dependency with
`ABYSS_MACHINE_REPO_ROOT`, `~/src/abyss-machine`, `/srv/AbyssOS/abyss-machine`,
or an installed `abyss_machine` package.
