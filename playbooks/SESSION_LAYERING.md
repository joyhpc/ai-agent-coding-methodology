# Session Layering

## Purpose

Prevent mixed-context sessions from collapsing project design, execution packaging, and implementation into one noisy thread.

## Core Rule

One session should solve one layer.

Recommended layers:

1. project layer
2. execution layer
3. implementation layer
4. review layer

## Layer Definitions

### Project Layer

Use for:

- goals
- success criteria
- boundaries
- risks
- PoCs
- abstract rules

Typical source of truth:

- project docs
- decision logs
- architecture notes

Typical outputs:

- starter packs
- boundary documents
- frozen candidate decisions

### Execution Layer

Use for:

- turning project truth into structured inputs
- requirements packages
- system definitions
- design-package metadata

Typical source of truth:

- approved project-layer artifacts
- repository packaging conventions

Typical outputs:

- `requirements.yaml`
- `system.yaml`
- `design_note.md`
- `traceability.yaml`
- `verification_matrix.yaml`

### Implementation Layer

Use for:

- code changes
- schematic edits
- BOM changes
- layout decisions
- bring-up details

Typical source of truth:

- approved execution-layer artifacts

Typical outputs:

- actual implementation changes
- verification evidence

### Review Layer

Use for:

- auditing the previous layer
- checking consistency
- reducing human approval cost

Typical source of truth:

- the exact file set under review

Typical outputs:

- critical findings
- important findings
- downstream-safe items
- minimal approval questions

## Mandatory Opening Checks

Before substantial work:

1. name the layer
2. name the source of truth
3. name what this session must not do
4. name the expected artifact

## Working-Copy Rule

If multiple repository copies exist:

1. discover all candidate copies
2. identify the active working copy
3. lock the session to that copy
4. treat all other copies as secondary evidence only

Never start review before this is done.

## Human Review Rule

If the task includes freezing truth:

- the agent may propose candidate frozen values
- the human must approve the frozen values
- the agent must not push already-known facts back to the human as data-entry work

## Good Session Shape

- narrow layer
- single source of truth
- exact file set
- clear output

## Bad Session Shape

- project design and implementation in one thread
- review before working-copy lock
- asking the human to restate facts already present in context
- using the agent to lead convergence when judgment is the bottleneck
