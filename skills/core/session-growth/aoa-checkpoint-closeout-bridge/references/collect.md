# Collect provisional checkpoint focus

### Mode: collect

Use only while the session is still active or when a caller explicitly asks
to preserve checkpoint focus without running reviewed closeout.

1. Bind the note to one session, workspace, checkpoint moment, and source refs.
2. Record candidate hints for donor extraction, progression axes, quest or
   route follow-through, and unresolved residue.
3. Classify each hint as provisional and record its source, freshness, owner
   hypothesis, and nearest wrong target when known.
4. Append to an explicitly supplied local checkpoint note only when the caller
   requested that effect. Otherwise return the packet inline.
5. Return the ordered future target groups: donor harvest, progression, quest
   promotion, then optional branch routing.
6. Stop. Do not load downstream skills and do not emit final candidates or
   verdicts.

Return `provisional-checkpoint-focus` with `session_id`, `checkpoint_ref`,
`hint_dispositions`, `future_stage_order`, `effects`, and `stop_line`.
