# Execute reviewed checkpoint closeout

### Mode: execute

## Preconditions

Require a closed, explicitly reviewed artifact, its current-session boundary,
and any checkpoint, handoff, or receipt hints. Hints are navigation inputs only.

Before the first node, classify every hint as `accepted`, `rejected`, `stale`,
`cross_session`, `contaminated`, or `unresolved`. A hint cannot become evidence
without corroboration in the primary reviewed artifact.

## Observable reread law

For every node that actually executes:

1. select and load that node's exact skill mode or report procedure;
2. reopen the primary reviewed artifact with a read tool after selection/load
   and immediately before `started`;
3. record the observable read action as
   `primary_evidence_reread: {path, action_ref, order}` on that node;
4. use that fresh observation plus only the typed accepted upstream outputs as
   the node input.

An initial read, cached model context, a prior node's reread, a hint packet, or
the statement "reread performed" is not evidence of the action. Each
`classify[*]` instance needs its own reread. A skipped or deferred node records
`primary_evidence_reread: not_executed`; an executed node without an observable
action ref terminates as `unverified_missing_evidence_reread` and cannot be
reported as verified or completed.

## Serial execution law

Tool parallelism is allowed only inside one node when the node contract says
the reads are independent. It is forbidden across dependency gates or DAG
nodes.

For every executed node, use three observable phases:

1. `load`: select the node, then issue one tool turn that reads only its exact
   mode/report procedure and await the result;
2. `reread`: in a later tool turn, read only the primary reviewed artifact and
   await the result;
3. `execute`: derive the typed output, verify it, and record the terminal state
   before selecting another node.

Record `procedure_load.action_ref` and
`primary_evidence_reread.action_ref`. Do not load the next mode or reread for
another node until the current node is terminal. If reads for two nodes share
one assistant tool batch, mark every affected node
`unverified_nonserial_node_execution`; do not repair the run by citing the
separate tool output IDs afterward.

Dependency preflight follows the same law. When progression is selected:

1. load its `SKILL.md` and await it;
2. inspect only `.aoa-skill-source.json` in that exact loaded bundle and await
   it; use its direct-source git fallback only when that exact handle is absent;
3. read only the resolved owner manifest and await it;
4. after manifest success, read the named owner-model documents in a later
   tool turn and await them.

A manifest and owner-document read issued in the same tool batch terminates the
progression node as `blocked_owner_source_gate_not_observed`. A lookup under
`.system`, a sibling skill, the profile root, or another guessed path terminates
it as `blocked_missing_owner_source`; do not retry with a second path.

## Task-local DAG

Execute only nodes whose typed prerequisites are satisfied:

1. `harvest.extract`
   - select and load only `aoa-session-harvest` contract plus `extract` mode;
     do not preload other harvest modes
   - reopen the primary artifact and record its read action ref
   - produce and verify one `harvest-packet`
2. `harvest.classify[*]`
   - for each isolated unit that genuinely needs owner/object judgment, make a
     separate `classify` selection
   - load only the `classify` procedure for that exact instance
   - reopen the primary artifact for that exact instance, record its read
     action ref, and then read the exact extracted unit
   - produce and verify one `candidate-object-classification` per node
3. `progression.lift`
   - after successful serial owner preflight, select and load only the
     progression contract plus `lift` procedure
   - reopen the primary artifact, record its read action ref, then read accepted
     donor outputs
   - require one agent identity and an honest baseline posture
   - produce and verify one `progression-delta-candidate`, or record why the
     stage is skipped, deferred, or blocked
4. `harvest.promote`
   - run only when exactly one isolated, reviewed, repeated quest-shaped unit
     remains after donor and progression stages
   - make a fresh `aoa-session-harvest` selection and load only `promote` mode
   - reopen the primary artifact, record its read action ref, then read relevant
     prior outputs
   - produce and verify one `quest-promotion-verdict`; otherwise record
     `skipped` with the unmet prerequisite
5. `harvest.branch`
   - run only when materially different continuations remain visible
   - make a fresh `aoa-session-harvest` selection and load only `branch` mode
   - reopen the primary artifact and record its read action ref before forming
     branch cards
   - return branch cards and a handoff; never delegate or schedule from this
     node
6. `closeout.report`
   - select and freshly load this report procedure, reopen the primary artifact, and
     record its read action ref before verification
   - verify node order and terminal states
   - compare report claims against observable loads, reads, tool calls, effects,
     and state transitions; downgrade every unsupported claim
   - separate conclusions supported by the primary artifact from accepted
     hints and from rejected or unresolved residue
   - name every destination owner and nearest wrong target

Do not hide missing nodes. Every planned node must finish as `completed`,
`blocked`, `failed`, `skipped`, `deferred`, `handed-off`, or
`unverified_missing_evidence_reread` with a reason and evidence refs.

## Output

Return `checkpoint-closeout-execution-report` containing:

- reviewed artifact and current-session refs
- accepted, rejected, and unresolved hint dispositions
- DAG nodes with selected skill/mode, source identity, input and output ABI,
  state transitions, procedure-load action refs, observable primary-evidence
  read action refs,
  verification, effects, and terminal reason
- harvest units and classifications
- progression candidate or honest non-execution state
- quest-promotion verdict or honest non-execution state
- branch cards when applicable
- owner handoffs, rejected nearest targets, residual uncertainty, and stop line

Stats refresh, memo writeback, owner authorship, quest mutation, and playbook
execution remain explicit later routes.
