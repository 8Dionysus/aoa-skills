# Install and Profiles

## Profiles

| Profile | Membership | Intended use |
| --- | --- | --- |
| `repo-default` | `aoa-decision` | normal advertised installation |
| `repo-capability-sources` | all seven bundles | explicit research, comparison, and KAG/capability work |

Profile membership comes from `config/skill_pack_profiles.json`; resolved
membership and revisions are generated.

## Host visibility

Use `repo-default` for an ordinary installation on every host. It expresses the
portable initial catalog directly: only `aoa-decision` is present.

`repo-capability-sources` deliberately transports all seven bundles. Its six
deferred members are hidden from implicit Codex discovery by the OpenAI host
adapter in `agents/openai.yaml`, but that adapter is not portable policy. A host
that ignores OpenAI metadata may expose or enable every installed member. Treat
this profile as an explicit laboratory/source profile, never as a portable way
to enforce deferred visibility.

After installation, inspect the actual host catalog and run behavioral trials.
File parity proves neither host visibility nor selection behavior.

## Handoff

Use the bundle commands in this order:

1. `stage_skill_pack.py` builds a deterministic plan and optionally a staged
   directory plus ZIP transport.
2. `inspect_skill_pack.py` validates manifest, layout, file digests, and bundle
   digest without consulting a live export.
3. `import_skill_pack.py` performs receiver-side inspect, optional install, and
   verify.
4. `verify_skill_pack.py` compares an installed root to the selected handoff or
   current export.

The generated bundle `README.md` is a human companion;
`bundle_manifest.json` is the machine contract. Extra sibling bundles are
reported and fail only in strict-root posture.

Run `smoke_skill_pack_handoff.py --transport both` for the bounded directory
and ZIP roundtrip. Installation parity is not native prompt visibility or
behavioral evidence.
