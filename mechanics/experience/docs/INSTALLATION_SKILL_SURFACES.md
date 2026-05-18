# Installation Skill Surfaces

Version: 1.0.0

## Purpose

Defines bounded skills for validate, migrate, smoke, replay, and rollback.
Use the stronger owner split in [Experience](../README.md). This file only
defines owner-local installation skill constraints.

## Owns

- skill surfaces
- bounded invocation
- evidence refs

## Must not do

- skill as policy
- durable authority
- hidden side effects

## Flow

```text
owner-local artifact
  -> validation
  -> operator review
  -> activation or denial
```

## Authority Source

This surface consumes upstream release and no-direct-write gates; it does not
become release approval or Tree-of-Sophia write authority.

## Exit signal

This surface is ready when it can produce a typed artifact, route it to the true owner, survive replay, and fail closed when authority is missing.
