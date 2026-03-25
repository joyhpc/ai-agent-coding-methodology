# 2026-03-25 Human-First Convergence

## Task

Use a coding agent to drive project-layer convergence for a hardware design effort:

- choose the right repository
- separate project-layer and execution-layer artifacts
- freeze starter-pack conclusions
- review anchor documents before downstream packaging

## Outcome

Worked:

- the repository boundary was eventually clarified
- source-of-truth separation became explicit
- the need for session layering became clear

Failed or was inefficient:

- the agent repeatedly drifted across layers
- the agent reviewed the wrong repository copy before the working copy was locked
- the human had to restate already-known facts instead of only approving candidate values

## Failure Surface

This was a high-judgment, low-code, high-responsibility phase.

That is exactly where agent-first execution performs poorly.

## Missing Signals

- explicit instruction that the human, not the agent, owns convergence decisions
- explicit working-copy lock before review
- explicit instruction to propose candidate frozen values before asking questions

## Root Cause

The task bottleneck was not implementation.

The bottleneck was deciding:

- what is true
- what is frozen
- which repository owns which layer

The agent was asked to help in a space where ambiguity resolution mattered more than mechanical execution.

## Fix

Use this rule:

- `human-first` for convergence phases
- `agent-second` for structured execution after decisions are made

Operationally:

1. the human freezes the working copy, source of truth, and decision boundary
2. the agent converts those decisions into structured artifacts
3. the agent may review for consistency, but must not replace human freezing

## Promotion Candidate

- add a formal methodology principle: when the bottleneck is judgment rather than execution, default to `human-first, agent-second`
