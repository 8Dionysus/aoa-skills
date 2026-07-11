# Evaluation Snapshot

## Prompt

Before an OS Abyss runtime bundle is consumed, inspect its artifact class,
producer profile, drift, registry evidence, and trust-gate verdict through
abyss-machine, then route any rebuild or signing action to its owner.

## Expected selection

use

## Why

The request is an OS Abyss artifact-trust admission decision with explicit
read-model evidence and an owner-routed mutation boundary.

## Expected object

Decision: use `os-abyss-artifact-trust-loop`. Inspect read-only trust state
first, preserve the consumer verdict, and route mutation to the owner producer.

## Boundary notes

The trust plane may classify and inspect. It must not silently build, sign,
promote, repair registry state, or replace the owner producer.

## Verification hooks

The response should name the artifact class and consumer intent, inspect the
bounded abyss-machine trust surfaces, preserve allow, warn, deny, or
manual-review, and route every mutation through the owner.
