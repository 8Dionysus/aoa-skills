# Session and compaction

The runtime seam keeps a separate JSON session file when asked.

Recommended path:

- `.aoa/skill-runtime-session.json`

## What is tracked

- active skills
- activation count
- last explicit handle
- allowlist paths
- compact summary
- must-keep state
- retain sections
- rehydration hint
- activation log

## Why it matters

If a long-running agent compacts or truncates context, the skill body can silently fall out of memory.

The session packet preserves the state that matters most so the runtime can:

- avoid duplicate activation spam
- keep resource allowlists stable
- rebuild the active skill set after compaction
- tell the agent exactly what to reload before resuming
