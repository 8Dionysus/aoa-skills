# Evaluation Snapshot

## Prompt

Compare a first-pass context map with a seam-making refactor and choose the clearer fit when the boundary is already named but one concrete dependency still needs a port or adapter seam.

## Expected selection

use

## Why

The broader context boundary is already clear, so the real pressure is the concrete dependency and the need for a narrower seam around it.

## Expected object

A narrower seam, port, or adapter move around the concrete dependency after the broader context boundary is already clear.

## Boundary notes

This is a port-adapter-refactor case, not a bounded-context-map case.

## Verification hooks

- name the concrete dependency
- show the seam or adapter boundary
- avoid reopening the already-settled broader context map
