# Evaluation Snapshot

## Prompt

Compare diagnosis with repair planning when a reviewed session shows repeated drift and no reviewed diagnosis packet exists yet.

## Expected selection

use

## Why

The route has symptoms and probable causes, but no reviewed diagnosis yet. The
next honest object is diagnostic classification before any repair packet.

## Expected object

A diagnosis packet that classifies symptoms, causes, and repair shapes before patching.
The diagnosis should carry evidence posture before any repair packet can be
honest.

## Boundary notes

This is a session-self-diagnose case, not a session-self-repair case.

## Verification hooks

- separate symptoms from probable causes
- keep probable causes posture-limited when evidence is provisional or contested
- name likely repair shapes without executing them
- require reviewed diagnosis before repair work starts
