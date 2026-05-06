# Owner Status Landing

## Use When

Use this part after `candidate_ref` exists and the next honest move is a
reviewed owner-local status surface that is weaker than final object truth.

## Do Not Use When

Do not use this part for raw checkpoint carry, seed truth, final object truth,
proof authority, scheduler authority, or unreviewed chat memory.

## Route Check

- Does the packet already have `candidate_ref`?
- Is the owner repo explicit?
- Is the status posture one of the live reviewed states?
- Are evidence refs present?
- Are merge, supersession, or drop fields explicit when terminal?

## Active Outputs

- reviewed owner landing bundle
- owner repo and owner shape
- status posture
- status note
- supersession, merge, or drop metadata

## Next Route

Route to [Governed Followthrough](../governed-followthrough/README.md) when a
bounded next-step verdict is needed.

Source doc:

- [Owner Status Surfaces](../../docs/OWNER_STATUS_SURFACES.md)
