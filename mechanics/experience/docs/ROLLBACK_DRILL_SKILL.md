# Rollback Drill Skill

Version: 1.0.0

## Purpose

Defines rollback drill skill constraints.
Use the stronger owner split in [Experience](../README.md). This file only
defines owner-local rollback drill constraints.

## Owns

- rollback skill
- dry run
- safe execution

## Must not do

- unsafe rollback
- missing proof
- durable side effect without review

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
