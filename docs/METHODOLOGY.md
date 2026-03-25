# Methodology

## Objective

Build a repeatable operating model for using coding agents in production-grade engineering work.

## Primary Claim

Coding-agent success is dominated by system design, not raw model quality alone.

The operating model should be:

1. repo-native
2. task-scoped
3. verification-first
4. feedback-driven
5. safe under failure

## The Six-Layer Model

### 1. Rule Layer

Persistent repo instructions define:

- architecture boundaries
- coding conventions
- verification commands
- dangerous areas
- examples of correct patterns

Artifacts:

- `AGENTS.md`
- subdirectory rule files
- framework-specific rules

### 2. Task Protocol Layer

Every task should define:

- objective
- scope
- constraints
- acceptance criteria
- relevant files
- verification method

If the task lacks these, the agent must infer too much.

### 3. Plan Layer

Non-trivial work needs a living execution plan.

Use plans when work is:

- multi-file
- multi-step
- risky
- ambiguous
- expected to take more than a short edit cycle

### 4. Execution Layer

Execution should follow:

1. inspect
2. plan
3. implement
4. verify
5. summarize

The key rule: do not treat code generation as completion.

### 5. Verification Layer

Verification must be explicit and runnable.

Preferred signals:

- tests
- lint
- typecheck
- build
- reproducible run output
- screenshots for UI
- benchmarks for performance-sensitive changes

### 6. Retrospective Layer

Repeated mistakes should not remain in chat history only.

Retrospectives should answer:

- what failed
- why the agent failed
- what signal was missing
- what rule or workflow should be changed

## Default Workflow

1. intake the task
2. classify complexity
3. create a plan if needed
4. execute in the smallest safe slice
5. verify immediately
6. update rules if a pattern repeats

## Design Principles

### Verification First

A coding agent works best when success can be self-checked.

### Persistent Context Beats Repeated Prompting

Stable repo rules outperform re-explaining the same expectations every session.

### Smallest Sufficient Context Beats Maximum Context

Do not feed every available artifact into the same session.

Prefer:

- the right layer
- the right source of truth
- the smallest sufficient file set

Too much mixed context produces false synthesis:

- project-layer questions drift into implementation
- execution-layer reviews inherit stale project assumptions
- different repository copies get merged in the model's head

### Narrow Scope Beats Broad Ambition

Well-scoped tasks outperform vague, end-to-end requests.

### Human Judgment Moves Up the Stack

The human role shifts from line-by-line implementation to:

- problem framing
- boundary setting
- review
- acceptance
- system improvement

### Human-First In Convergence Phases

When the bottleneck is judgment rather than execution, use `human-first, agent-second`.

Typical convergence-phase tasks:

- defining project goals
- freezing boundaries
- choosing a source of truth
- resolving document ownership
- deciding object identity, scope, and role

In these phases:

- the human should make the key decisions first
- the agent should structure, rewrite, cross-check, and propagate the decision

Do not let the agent lead when the main difficulty is "figuring out what is true".

Let the agent lead when the main difficulty is "turning an already-decided truth into artifacts".

### Lock The Working Copy Before Review

In multi-copy environments, no review or synthesis should begin until the working copy is explicit.

First confirm:

1. the active repository copy
2. the source of truth for this layer
3. the exact file set under review

If multiple copies exist, the agent must discover and compare them before asking the human for help.

The human should only decide when multiple plausible copies remain after local discovery.

### Agent Friendliness Is an Engineering Property

Clean repo structure, discoverable scripts, and explicit commands improve outcomes materially.

## Failure Modes

Common failure modes:

- vague task statements
- no verification target
- hidden architecture assumptions
- oversized context dumps
- uncontrolled multi-agent overlap
- no mechanism to learn from repeated errors

## Outcome Standard

The goal is not "agent produced code".

The goal is:

- correct changes
- verified changes
- explainable changes
- repeatable process
