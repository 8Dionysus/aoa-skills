## Prompt

A repo task shows repeated owner-boundary confusion; the agent skipped existing validators and tests, treated a generated readiness packet as proof, and needs a route that separates central proof, local intake, MCP access, and session evidence before continuing.

## Expected selection

use

## Why

Decision: use `aoa-eval`. Route signs can trigger this skill even when the user never says `eval`; select one route because repeated validation, proof, and owner-boundary pressure is present.

## Expected object

A router result that raises readiness when available, checks existing validators and tests first, and chooses exactly one eval route.

## Boundary notes

This is not keyword matching. Central proof, local intake, MCP access, and session evidence remain separate; the aoa-eval-keyword-mining-blindspot packet stays candidate-only.

## Verification hooks

Check route-sign evidence, validate any candidate packet, and confirm one selected subskill before writing local or central surfaces.
