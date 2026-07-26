# Install and Profiles

## Portable consumer profiles

| Profile | Membership | Intended use |
| --- | --- | --- |
| `portable-consumer-advertised` | seven advertised shared bundles | explicit external repository consumer or ordinary handoff |
| `portable-consumer-all-sources` | all nine shared source bundles | explicit research, comparison, and capability/KAG work |

Profile membership comes from `config/skill_pack_profiles.json`; resolved
membership and revisions are generated.

Neither portable profile is the OS user catalog. `os-user-default` is a
separate managed-copy profile assembled from shared source bundles and
admitted owner homes by `scripts/install_os_skill_profile.py`.

## Source and consumer boundary

The `aoa-skills` source repository keeps `.agents/skills` absent. A direct
source stage or verification builds all portable bytes under a temporary
directory and removes it when the operation ends. An explicit
`build_agent_skills.py --output-root <empty-external-skill-root>` may create a
consumer assembly outside this source repository.

Inside a staged handoff, `.agents/skills/<name>` is the logical portable
layout. A receiving repository may install that layout only when it is the
intended explicit consumer and the same canonical bundle is not already
prompt-visible from the OS user root. Direct installation from the source
repository therefore requires an explicit external `--dest-root`.

`portable-consumer-all-sources` includes the two deferred packages. Their
OpenAI adapters request non-implicit posture, but another Agent Skills host may
ignore that adapter and expose every installed package. Treat this profile as
an explicit research/source transport, never as a portable visibility
enforcement mechanism.

## Host visibility

After installation, inspect the actual host catalog in a fresh session and run
behavioral trials.
File parity proves neither host visibility nor selection behavior.

For the normal OS catalog, install `os-user-default` into the verified Codex
user root and ensure no selected canonical ID is also present in a
repository-visible projection.

The aggregate profile verifies owner-managed links but never creates or
repairs them. On a clean user root, first invoke the `.aoa` owner operation for
both advertised session-memory routes:

```bash
python /srv/AbyssOS/.aoa/scripts/aoa_session_memory.py install-user-skill \
  --aoa-root /srv/AbyssOS/.aoa \
  --skill aoa-session-memory-global-route
python /srv/AbyssOS/.aoa/scripts/aoa_session_memory.py install-user-skill \
  --aoa-root /srv/AbyssOS/.aoa \
  --skill aoa-session-memory-evidence-route
```

Each command is owner-idempotent: an exact current link is preserved; a
conflicting target requires that owner command's explicit `--force` review.
Only after both owner links are current should the aggregate profile execute.
If an owner link is missing or misdirected, the profile stops before changing
its managed-copy entries and reports the required owner operation.

Preview the complete owner resolution and destination plan before installation:

```bash
PYTHONPATH=scripts python scripts/install_os_skill_profile.py \
  --profile os-user-default
```

The normal execute and parity routes require clean Git owner sources:

```bash
PYTHONPATH=scripts python scripts/install_os_skill_profile.py \
  --profile os-user-default --execute
PYTHONPATH=scripts python scripts/install_os_skill_profile.py \
  --profile os-user-default --check
```

For a reviewed candidate trial, override the candidate owner roots and install
only into a separate disposable destination:

```bash
PYTHONPATH=scripts python scripts/install_os_skill_profile.py \
  --profile os-user-default \
  --source-root owner-repo=/path/to/candidate-worktree \
  --dest-root /path/to/disposable/skill-root \
  --allow-dirty-source \
  --execute
```

`--allow-dirty-source` is rejected for the normal user destination. An
unmanaged same-name collision requires `--replace-unmanaged`; a stale entry
named in the prior managed receipt requires `--prune-managed`. Both are
reviewed execute-time choices. The installer preserves unrelated user skills,
refuses unsafe receipt names and destination roots, verifies the aggregate
receipt as well as each source-return handle, and leaves a current repeated
execute byte- and timestamp-stable.

## Handoff

Use the bundle commands in this order:

1. `stage_skill_pack.py` builds a deterministic plan and optionally a staged
   directory plus ZIP transport from a temporary portable source assembly.
2. `inspect_skill_pack.py` validates manifest, layout, file digests, and bundle
   digest without consulting a live export.
3. `import_skill_pack.py` performs receiver-side inspect, optional install, and
   verify.
4. `verify_skill_pack.py` compares an installed root to the selected handoff or
   a freshly assembled source projection.

The generated bundle `README.md` is a human companion;
`bundle_manifest.json` is the machine contract. Extra sibling bundles are
reported and fail only in strict-root posture.

Run `smoke_skill_pack_handoff.py --transport both` for the bounded directory
and ZIP roundtrip. Installation parity is not native prompt visibility or
behavioral evidence.
