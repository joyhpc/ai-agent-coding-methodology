# 2026-03-25 Working-Copy Lock

## Task

Review a set of newly created project-layer documents and decide whether they were ready for downstream use.

## Outcome

The review drifted to the wrong repository copy before the active working copy was locked.

This invalidated early conclusions.

## Failure Surface

Multiple copies of the same repository existed:

- main working copy
- regression copy
- tool workspace copy

The review began before explicitly choosing one.

## Missing Signals

- no mandatory working-copy lock at session start
- no explicit target file set before review
- no rule preventing the agent from defaulting to an arbitrary copy

## Root Cause

The session treated repository identity as implicit.

In multi-copy environments, that assumption fails.

## Fix

Before any review:

1. discover all candidate copies
2. identify the active working copy
3. list the exact target files
4. only then begin review

## Promotion Candidate

- add a methodology rule: lock the working copy before review or synthesis
