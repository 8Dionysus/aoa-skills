# Release Support Direction

Release support keeps portable consumption reviewable.

The active route is:

```text
authored skill or support input
  -> generated export/support surface
  -> validation and release-support readout
  -> host, SDK, runtime, or downstream route when stronger truth is needed
```

## Current contour

- Active contracts live under `docs/`.
- Historical wave descriptions live under `legacy/waves/`.
- Generated files remain projections over authored skill and config inputs.

## Boundary

Release support packages and validates portable surfaces. It does not approve
release or own runtime behavior by itself.
