# Trust gate and allowlist

## Trust gate

The trust gate exists to stop repo-scoped skills from auto-entering a session merely because a repository is present.

Policy:

- repo-scoped skills require an explicit trust decision for the repository
- user-scoped skills may load without repo trust
- admin-scoped and system-scoped skills may load without repo trust
- if a repo is untrusted, discovery hides repo-scoped skills by default and guarded disclosure or activation returns a blocked payload

Trust decisions are stored in a small JSON trust store.
The default hint is:

- `.aoa/repo-trust-store.json`

The governed seam matches trust by repo root and, when available, Git origin URL.

## Permission allowlist

The allowlist exists to make bundled resources usable.
A skill may include scripts, references, and assets. The model should be able to read those files without tripping a confirmation dialog for each path.

Policy:

- allow read-only access only
- merge paths across all active skills in the session
- do not eagerly read every file in the skill bundle
- list directories for `scripts/`, `references/`, and `assets/` even when they are empty, so future skills stay compatible

The governed seam resolves path templates for:

- repo scope: `$REPO_ROOT/.agents/skills/<skill-name>`
- user scope: `$HOME/.agents/skills/<skill-name>`
- admin scope: `/etc/codex/skills/<skill-name>`

The merged allowlist is emitted by `scripts/skill_runtime_guardrails.py allowlist`.
