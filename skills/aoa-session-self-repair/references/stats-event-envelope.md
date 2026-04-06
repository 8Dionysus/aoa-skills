# Stats Event Envelope

Use this shared envelope when the session-harvest family emits one bounded
finish receipt.

## Required fields

- `event_kind`
- `event_id`
- `observed_at`
- `run_ref`
- `session_ref`
- `actor_ref`
- `object_ref`
- `evidence_refs`
- `payload`

## Optional fields

- `supersedes`
- `notes`
- `owner_ref`
- `related_event_refs`

## Rules

- Keep receipts append-only.
- If a correction is needed, emit a new receipt and set `supersedes`.
- Link to inspectable artifacts through `evidence_refs` instead of duplicating
  raw transcripts, patches, or reports.
- Keep `payload` bounded to the skill's own emitted packet or card set.
- Do not let receipt presence act as proof, routing authority, or score
  authority.
