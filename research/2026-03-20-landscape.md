# 2026-03-20 Landscape Survey

## Objective

Summarize current best practices for using coding agents in real engineering work.

## Key Synthesis

The field is converging on a system view:

- persistent repo rules
- structured task intake
- explicit planning for non-trivial work
- runnable verification
- retrospective-driven improvement

The strongest pattern is not "prompt better".

It is "design an agent operating system around the repository and workflow".

## High-Signal Official Sources

- OpenAI: Codex usage guidance and harness engineering
- Anthropic: Claude Code best practices and effective agents
- GitHub: Copilot coding agent task guidance and responsible use
- Cursor: coding with agents best practices
- Windsurf: prompt engineering and use-case guidance

## High-Signal GitHub Repositories

- `agentsmd/agents.md`
- `openai/openai-agents-python`
- `anthropics/skills`
- `anthropics/claude-code`
- `Aider-AI/aider`
- `OpenHands/OpenHands`
- `microsoft/autogen`
- `langchain-ai/langgraph`
- `langchain-ai/deepagents`
- `sanjeed5/awesome-cursor-rules-mdc`

## Converging Best Practices

1. keep stable guidance in repo-native rule files
2. require explicit acceptance criteria
3. create execution plans for long or risky work
4. verify with runnable evidence
5. use parallel agents only for isolated subtasks
6. promote repeated failures into stable rules

## Open Questions

- how to evaluate methodology quality across repositories
- what belongs in global rules vs task-specific plans
- where to draw the boundary between tool-specific and tool-agnostic methods

## Next Research Directions

- compare single-agent and multi-agent success patterns
- define maturity levels for agent-enabled repositories
- define leading indicators for "agent legibility"
