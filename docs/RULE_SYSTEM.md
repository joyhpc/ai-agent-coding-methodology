# Rule System

## Purpose

Define how stable lessons become reusable agent rules.

## Rule Hierarchy

### Level 1: Global Rules

Apply to the whole repository.

Examples:

- always verify after edits
- distinguish sourced facts from synthesis
- prefer task templates for non-trivial work

### Level 2: Domain Rules

Apply to a specific area.

Examples:

- backend service rules
- frontend UI verification rules
- documentation standards
- research documentation rules

### Level 3: Task-Specific Constraints

Temporary constraints for the current task.

Examples:

- do not change public API
- keep migration backward compatible
- no new dependencies

## Promotion Path

Lessons should move through this path:

1. incident or observation
2. retrospective note
3. candidate rule
4. validated repeated usefulness
5. promotion into stable repo rule or playbook

## Good Rule Criteria

A good rule is:

- specific
- observable
- testable
- durable
- scoped

Bad rule patterns:

- vague preferences
- motivational language
- tool worship
- one-off fixes disguised as universal law

## Rule Format

Recommended structure:

1. rule statement
2. scope
3. rationale
4. verification signal
5. failure mode if ignored

## Examples

### Example: Verification Rule

- Rule: Every code change must name at least one concrete verification method.
- Scope: all implementation tasks
- Verification signal: test, lint, typecheck, build, benchmark, or screenshot
- Failure mode: unverified output masquerades as completion

### Example: Planning Rule

- Rule: Create a living plan before executing risky multi-file changes.
- Scope: non-trivial implementation work
- Verification signal: plan exists and is updated as the task evolves
- Failure mode: hidden coupling and aimless edits
