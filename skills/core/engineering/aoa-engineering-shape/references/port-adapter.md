# Shape a port and adapter boundary

### Mode: port-adapter

Use this mode when a concrete database, API, filesystem, CLI, clock, network
client, subprocess, provider, environment lookup, credential path, or runtime
detail leaks into reusable logic and a named consumer needs a stable seam. Do
not use it for incidental setup, a seam with no consumer, or unresolved core
placement.

Required inputs:

- target slice and target-specific owner or explicit unresolved owner edge
- concrete dependency pressure and the behavior the consumer actually needs
- inputs, outputs, errors, fallback, retries, limits, observability, effects,
  callers, and compatibility expectations

Return a `port-adapter-boundary` containing the narrow consumer-shaped port,
adapter responsibilities, composition-root policy, error/fallback behavior,
parity checks, migration edge, and stop line.

Procedure:

1. Confirm that the dependency materially blocks change, testing, reuse, or
   portability and that the core-versus-edge boundary is sufficiently clear.
2. Define the port from the consumer purpose, not by copying the provider API.
3. Include inputs, outputs, typed errors, fallback, limits, observability, and
   effect posture in the port contract.
4. Put translation, transport, credentials, local paths, retries, process calls,
   runtime discovery, and provider quirks behind the adapter.
5. Keep policy selection and adapter wiring at the composition root.
6. Preserve current behavior through the smallest migration seam; keep
   degraded, truncated, missing, and fallback states visible.

Adapter-seam shapes:

Choose the narrowest shape for one concrete dependency. Define the port from
the consumer's need; do not copy the provider API or introduce every seam in
the table.

| Shape | Dependency pressure | Port should expose | Adapter owns | Avoid | Verify |
|---|---|---|---|---|---|
| External service or API | Vendor client, HTTP, auth, retry, or remote error shape. | The one operation or query the consumer needs. | Transport, credentials, retries, provider errors, response mapping. | Mirroring the whole vendor SDK. | Success, failure, timeout, and response-shape checks. |
| Storage or database | SQL driver, ORM, transaction, collection API, migration state. | Purpose-shaped reads, writes, or repository queries. | Connection, transaction, serialization, and storage errors. | Hiding domain query meaning behind a generic repository. | Core cases with a fake plus one focused adapter integration check. |
| Filesystem, path, or environment | Local paths, workspace layout, env vars, permissions, profile discovery. | Logical read, write, or discovery need. | Path resolution, env lookup, permissions, platform differences. | Treating a local layout as domain truth. | Temporary-root, missing-path, and permission/error cases. |
| Clock, randomness, or ID | Time, timer, UUID, entropy, random choice. | The smallest time, ID, or entropy operation needed. | Real clock, monotonic behavior, random source, deterministic substitute. | Nondeterminism leaking into core cases. | Ordering, uniqueness, expiry, and deterministic-fake cases. |
| CLI, subprocess, or tool runner | Executable, arguments, cwd, exit codes, stdout/stderr, timeout. | Command outcome shape the consumer uses. | Invocation, environment, timeout, output parsing. | Freezing human log text as the port. | Fake runner, malformed output, and one real smoke when available. |
| Generated or export writer | Install path, artifact format, export profile, copy/write mechanics. | Source-to-output intent and target artifact identity. | Formatting, writes, profile paths, install layout, freshness markers. | Generated output becoming source authority. | Rebuild, source-ref preservation, stale-output, and parity checks. |
| Runtime discovery or configuration | Runtime inventory, flags, service discovery, config, plugin lookup. | Stable capability or setting required by the consumer. | Discovery mechanics, defaults, missing capability, config parsing. | Runtime presence becoming hidden source truth. | Missing-capability, default, and compatibility cases. |
| SDK or typed facade | Loader, typed model, compatibility layer, versioned API. | Stable typed operation or compatibility result. | Version translation, deprecation, and provider error mapping. | SDK convenience owning source meaning. | Old/new version, invalid input, and compatibility cases. |
| Queue, event, or scheduler | Bus, queue, cron, worker, callback runner. | Enqueue, publish, schedule, or consume intent. | Delivery, retries, ordering guarantees, dead-letter behavior. | Treating asynchronous delivery as immediate core behavior. | Fake queue and focused ordering/failure adapter smoke. |

Compact output shape:

| Field | Required content |
|---|---|
| Reusable consumer | The named consumer whose need defines the seam. |
| Concrete dependency | Exact provider or runtime detail leaking inward. |
| Shape selected | One row from the seam table, or a simpler direct seam. |
| Port operation | Purpose-shaped input, output, errors, effects, and limits. |
| Adapter owns | Translation, transport, credentials, paths, retries, and quirks. |
| Composition root | Where policy selection and wiring remain explicit. |
| Fallback and observability | Visible degraded states and bounded signals. |
| Migration compatibility | Smallest seam preserving existing callers and behavior. |
| Contract check | Separate consumer-visible evidence still required. |
| Stop line | Unrelated abstractions and rewrites excluded from this task. |

Contracts and risks:

- the seam must reduce real coupling rather than add decorative interfaces
- generated/export consumers keep their own contract checks
- avoid provider-shaped ports, wrapper proliferation, hidden rewrites, or
  claiming that adapter introduction proves downstream compatibility

Verify the original dependency pressure, narrower consumer need, unchanged
behavior/effects, explicit failure states, bounded scope, and separate
consumer-visible contract evidence.
