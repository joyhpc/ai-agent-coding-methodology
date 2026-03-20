# AI Agent Coding Methodology

Repository for building, testing, and iterating a practical methodology for using coding agents in real software engineering.

## Scope

This repository focuses on:

- methodology for using coding agents to do real coding work
- repository design patterns for agent-friendly engineering
- task intake, planning, execution, verification, and review workflows
- multi-agent coordination patterns
- retrospectives and failure analysis

This repository does not aim to be:

- a benchmark repo
- a generic prompt collection
- a tool-specific feature list

## Core Thesis

The best coding-agent practice is not "better prompts only".

It is an engineering system with six layers:

1. rules
2. task protocol
3. plan
4. execution
5. verification
6. retrospective learning

## Repository Map

- `docs/` — core methodology and design principles
- `playbooks/` — operational workflows
- `templates/` — intake, plan, and retrospective templates
- `research/` — external research summaries and source-backed synthesis
- `retrospectives/` — concrete lessons from real usage
- `AGENTS.md` — rules for maintaining this repository with coding agents

## Starting Points

- [docs/METHODOLOGY.md](docs/METHODOLOGY.md)
- [docs/RULE_SYSTEM.md](docs/RULE_SYSTEM.md)
- [playbooks/SINGLE_AGENT_WORKFLOW.md](playbooks/SINGLE_AGENT_WORKFLOW.md)
- [playbooks/MULTI_AGENT_WORKFLOW.md](playbooks/MULTI_AGENT_WORKFLOW.md)
- [research/2026-03-20-landscape.md](research/2026-03-20-landscape.md)

## Working Model

Recommended flow:

1. capture the task using [templates/TASK_INTAKE.md](templates/TASK_INTAKE.md)
2. if the task is non-trivial, write an execution plan using [templates/EXEC_PLAN.md](templates/EXEC_PLAN.md)
3. execute with one agent first; add more agents only for isolated side tasks
4. verify using explicit commands, tests, screenshots, or measurable outputs
5. write a retrospective using [templates/RETROSPECTIVE.md](templates/RETROSPECTIVE.md)
6. promote repeated lessons into `AGENTS.md`, rules, or playbooks

## Initial Research Basis

The initial version is grounded in official materials and high-signal repositories from:

- OpenAI
- Anthropic
- GitHub Copilot
- Cursor
- Windsurf
- Aider
- OpenHands
- AutoGen
- LangGraph

See [research/2026-03-20-landscape.md](research/2026-03-20-landscape.md) for the first research synthesis.
