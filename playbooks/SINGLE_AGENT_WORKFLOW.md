# Single-Agent Workflow

## Use When

- the task is well-scoped
- the write surface is limited
- the main bottleneck is not parallelizable

## Workflow

1. inspect the codebase or target files
2. restate the task as an objective with constraints
3. create a plan if the task is non-trivial
4. implement the smallest useful slice
5. verify immediately
6. continue iterating until acceptance criteria are met
7. summarize what changed, how it was verified, and any residual risks

## Guardrails

- do not edit before understanding the target area
- do not skip verification
- do not expand scope unless the task requires it
- do not claim success without evidence

## Preferred Task Shape

Single-agent work is strongest for:

- bug fixes
- test additions
- focused refactors
- documentation updates tied to real code
- small feature additions with explicit acceptance criteria

## Failure Modes

- large ambiguous scope
- hidden dependencies
- missing runtime environment
- chat-only guidance with no repo artifacts
