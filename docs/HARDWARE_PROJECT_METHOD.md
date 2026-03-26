# Hardware Project Method

## Purpose

Define a practical collaboration method for running hardware projects with coding agents without turning the human into a data-entry clerk.

This method is intended for any hardware project with:

- evolving requirements
- multiple design documents
- review tooling
- repeated design sessions across architecture, interfaces, power, bring-up, and verification

## Core Diagnosis

Traditional hardware collaboration with AI becomes inefficient when:

1. the same fact is maintained in many documents
2. project truth, execution inputs, and implementation details are mixed in one place
3. the agent asks the human to restate known facts instead of proposing candidate values
4. review starts before the working copy and source of truth are locked

The fix is not better prompting alone.

The fix is a new operating model:

- single-question sessions
- a structured truth kernel
- human approval of deltas
- generated projections instead of hand-maintained duplicate documents

## Core Principles

### 1. One Session, One Question

Each session should solve one bounded problem only.

Examples:

- how should this board be positioned
- which interface contract should be frozen
- how should the power topology be organized
- how should the block diagram be structured

Do not mix:

- project definition
- execution packaging
- implementation
- review

in the same session.

### 2. Human-First For Convergence, Agent-First For Execution

Use `human-first, agent-second` when the bottleneck is judgment:

- choosing object identity
- freezing boundaries
- selecting the source of truth
- deciding document ownership

Use `agent-first, human-approved` when the bottleneck is structured execution:

- extracting candidate values
- rewriting into structured form
- projecting truth into derived artifacts
- running consistency checks

### 3. Truth Must Be Structured

Project truth should not live primarily in chat logs or duplicated Markdown.

Use a single structured truth kernel as the primary project memory.

Recommended first format:

- YAML

The truth kernel should hold:

- approved facts
- frozen facts
- open items
- rationale
- source references

### 4. Documents Are Projections

Starter packs, dictionaries, indexes, and execution inputs should be treated as projections of truth, not parallel truth sources.

If a fact changes, update the truth kernel first.

Never patch the projection as the source of truth.

### 5. Lock The Working Copy First

Before review, synthesis, or extraction:

1. identify the active working copy
2. identify the source of truth for this layer
3. identify the exact file set under review

If multiple copies exist, no review should begin until one is locked.

### 6. The Agent Must Propose, Not Re-Interview

When facts already exist in context or source documents, the agent must:

1. propose candidate values
2. attach rationale and source references
3. ask only the smallest remaining approval question

The agent must not push known information back to the human as form-filling work.

## The Four Layers

### Project Layer

Owns:

- mission
- scope
- success criteria
- object identity
- boundary assumptions
- risks
- PoCs
- abstract rules

Primary artifacts:

- truth kernel
- starter pack summary
- approved project decisions

### Execution Layer

Owns:

- packaging project truth into structured inputs
- preparing formal review inputs
- requirements and system definitions

Primary artifacts:

- `requirements.yaml`
- `system.yaml`
- `design_note.md`
- `traceability.yaml`
- `verification_matrix.yaml`

### Implementation Layer

Owns:

- schematic
- BOM
- layout
- firmware hooks
- bring-up steps

Primary artifacts:

- implementation changes
- evidence
- measurements

### Review Layer

Owns:

- auditing outputs from another layer
- finding inconsistencies
- deciding what is downstream-safe

Primary artifacts:

- findings
- approval questions
- promotion candidates

## Session-As-A-Transaction

Treat every design session as a transaction with five stages.

### 1. Hydrate

Mount:

- the active working copy
- the current topic
- the smallest sufficient truth slice

### 2. Explore

Use the session as a sandbox for:

- tradeoff analysis
- datasheet interpretation
- option comparison
- partial reasoning

Nothing from this stage is true by default.

### 3. Human Arbitrate

The human chooses:

- accept
- reject
- refine

This is where the expensive engineering judgment happens.

### 4. Harvest

At session end, force the agent to output only:

- ADR-style rationale
- structured delta

The delta must use statuses such as:

- `proposed`
- `approved`
- `frozen`
- `open`

### 5. Merge

The human reviews the delta outside the chat window and merges it into the truth kernel.

Only then may projections or downstream inputs be refreshed.

## Minimal Truth Kernel

For a new hardware project, start with one file:

- `.truth-kernel/<project>.kernel.yaml`

Minimum sections:

- `identity`
- `mission`
- `contracts`
- `boundaries`
- `paths`
- `open_items`
- `approval_log`

Every important node should carry:

- `status`
- `rationale`
- `source_refs`
- `updated_at`

## Recommended Status Semantics

- `proposed`
  - candidate extracted from a session
  - not yet project truth
- `approved`
  - accepted by the human
  - usable as the current baseline
- `frozen`
  - explicitly locked for downstream execution or review tooling
- `open`
  - known gap or undecided item

## Session Types

### A. Bootstrap Session

Goal:

- create the first truth kernel from already approved project facts

Mode:

- human-first

Output:

- initial kernel skeleton

### B. Single-Question Design Session

Goal:

- resolve one design question

Examples:

- block diagram
- interface contract
- power topology
- component selection

Mode:

- mixed, but ends with human approval

Output:

- delta patch
- rationale

### C. Packaging Session

Goal:

- transform approved truth into execution-layer artifacts

Mode:

- agent-first, human-approved

Output:

- review input package

### D. Review Session

Goal:

- inspect one existing layer

Mode:

- stateless

Output:

- findings
- safe downstream items
- minimal approval questions

### E. Manager Session

Goal:

- choose the next session
- maintain the problem map
- absorb session outputs into the workflow

Mode:

- coordination only

Output:

- next session prompt
- updated queue
- recovery actions

## Minimal File Layout

```text
<repo-root>/
  .workspace.lock
  .truth-kernel/
    <project>.kernel.yaml
    deltas/
    adr/
  projections/
```

Recommended meaning:

- `.workspace.lock`
  - absolute path of the only legal working copy
- `.truth-kernel/`
  - project truth and approved deltas
- `projections/`
  - generated human-readable artifacts

## What To Keep Manual vs Generated

Keep manual:

- truth kernel
- approval actions
- a lightweight project summary for humans

Generate or semi-generate:

- object dictionaries
- index pages
- truth summaries
- block diagrams from structured topology
- power tree views from structured topology
- execution-layer packaging stubs

## Anti-Patterns

Avoid:

1. asking the agent to redesign the project in one session
2. reviewing before locking the working copy
3. maintaining the same fact by hand in multiple Markdown pages
4. letting implementation details overwrite project truth
5. treating chat transcripts as project memory
6. asking the human to re-enter facts already present in context

## First-Week Adoption Plan

### Day 1

- lock the working copy
- create the initial truth kernel
- move only already-approved project facts into it

### Day 2

- run one single-question design session
- harvest one delta
- merge manually

### Day 3

- add a first projection such as a current truth summary

### Day 4

- add a second projection such as a block diagram or power topology view

### Day 5

- run a review session against the kernel and projections
- refine status semantics and session discipline

## Outcome Standard

The method is working when:

- the human mostly approves deltas instead of restating facts
- each session solves one question cleanly
- the active working copy is never ambiguous
- project truth is recoverable from one structured kernel
- downstream packaging becomes easier over time
