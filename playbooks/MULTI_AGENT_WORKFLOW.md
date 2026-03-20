# Multi-Agent Workflow

## Use When

Use multiple agents only when the task can be decomposed into isolated streams.

Good candidates:

- test-writing in parallel with implementation
- documentation in parallel with code changes
- independent modules with disjoint write surfaces
- verification sidecars such as benchmarks or reviews

## Coordination Model

### Primary Agent

Owns:

- overall plan
- critical path
- integration
- final verification

### Side Agents

Own:

- bounded subtasks
- disjoint files or responsibilities
- outputs that can be integrated cleanly

## Rules

1. Never split unclear work.
2. Assign explicit file or module ownership.
3. Keep one source of truth for the plan.
4. Avoid duplicate exploration.
5. Integrate frequently enough to catch drift.
6. Let the primary agent keep the critical path local.

## Common Safe Splits

- worker A: implementation
- worker B: tests
- worker C: docs or migration notes

## Common Unsafe Splits

- two agents editing the same core file
- parallelizing a task before architecture is understood
- handing the critical-path exploration to side agents and waiting idly

## Exit Criteria

The task is not done when side agents finish.

It is done when:

- outputs are integrated
- conflicts are resolved
- end-to-end verification passes
