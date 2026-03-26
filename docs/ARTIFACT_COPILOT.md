# Artifact Copilot

## Purpose

Define a faster collaboration mode where the agent acts as a draft-and-write copilot instead of a process-heavy manager.

This mode is designed for situations where:

- the working copy already contains useful context
- the next step should be a real artifact
- the human wants less ceremony and less repeated explanation

## Core Diagnosis

Many agent systems become inefficient because they optimize process instead of output.

Common symptoms:

1. the human becomes a router between sessions
2. the agent keeps producing prompts instead of drafts
3. one engineering step is split into too many pseudo-governance turns
4. the final document is still not written

This is AI bureaucracy.

The correction is to switch from process-driven interaction to artifact-driven interaction.

## Core Rule

The agent should default to drafting the next useful artifact, not to managing the next ritual.

## Artifact Copilot Behavior

### 1. Read The Workspace First

Before asking the human anything, the agent should:

1. inspect the active working copy
2. read the relevant source files
3. extract what is already known
4. draft the target artifact

### 2. Draft First, Ask Later

The agent should directly produce:

- a document draft
- a file patch
- a record stub
- a summary page

Only after drafting may it ask for the smallest missing values.

### 3. Unknowns Become TODOs

If the agent cannot infer a physical-world value, it should write:

- `[TODO: human input required]`

This is better than blocking the entire artifact.

### 4. Ask For At Most 1-3 Missing Values

Do not ask broad questions such as:

- "please provide more context"
- "please restate your needs"

Instead ask for the smallest missing values needed to finish the draft.

### 5. Use Plain Engineering Language

The output should read like something a project owner or engineer can use directly.

Avoid:

- management jargon
- abstract workflow language
- excessive structure that hides the actual decision

### 6. Write Back After Human Input

Once the human fills the missing values, the agent should update the file directly.

The interaction loop should be:

- draft
- fill gaps
- write back
- done

## When To Use Artifact Copilot

Use this mode when:

- the next useful move is a file, not a planning ritual
- the source documents already exist
- the human knows the direction but does not want to hand-author every page

Examples:

- current truth summary
- architecture role page
- first execution record
- object dictionary entry
- design note draft

## When Not To Use It

Do not use this mode when:

- the working copy is not locked
- no trustworthy source documents exist yet
- the task is still in a human-first convergence phase

In those cases, do a short convergence step first.

## Relationship To Truth Kernel

Artifact Copilot does not replace the truth kernel.

It changes the interaction pattern around it:

- truth kernel remains the structured source of truth
- artifact copilot becomes the default way to create and update projections

## Minimal Prompt Pattern

```text
You are this project's Artifact Copilot, not a process manager.

Goal:
Draft or update the next useful artifact directly.

Working copy:
<absolute path>

Target artifact:
<file path or artifact name>

Rules:
1. Scan the working copy first.
2. Extract known facts before asking me anything.
3. Draft the file directly.
4. Use [TODO: human input required] for missing physical values.
5. Ask me for at most 1-3 missing values.
6. Use plain engineering language, not process jargon.
7. After I answer, update the file directly.
```

## Anti-Patterns

Avoid:

1. using the agent as a prompt factory
2. forcing every step through a manager session
3. asking the human to restate facts already present in files
4. making the human manually propagate the same fact to multiple documents
5. letting management language replace engineering clarity

## Outcome Standard

The mode is working when:

- the human spends less time explaining process
- the agent produces useful drafts faster
- fewer sessions are required per engineering step
- the human mostly supplies irreducible missing facts instead of rewriting known ones
