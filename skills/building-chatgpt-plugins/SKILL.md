---
name: building-chatgpt-plugins
description: Use when guiding a user through creating or improving a current ChatGPT plugin, including deciding whether its selected workflow benefits from skills, MCP, authentication, or custom UI. Also use for explicitly requested testing, benchmarking, repair, audit, packaging, or release work on that selected plugin.
---

# Building ChatGPT Plugins

## Primary purpose: guided creation

Guide the user conversationally from an idea to a working selected ChatGPT plugin. Start with its outcome and skills; suggest MCP, OAuth, and custom UI where each could improve it.

When the brief is incomplete, ask one focused question at a time and preserve confirmed answers. Enter Audit, Benchmark, or Repair only when requested or its creation stage is reached.

## Target-first boundary

Identify the plugin before proposing artifacts. Ground decisions in its structure and requirements; label missing facts `Unresolved` and planned structures `Assumption`.

Every skill, MCP server, OAuth flow, UI, test, metric, and patch must belong to it. Do not create standalone infrastructure or benchmark products for unspecified plugins.

Use the current plugin model; treat legacy `ai-plugin.json` or OpenAPI plugins only as explicit migration targets.

**REQUIRED SUB-SKILL:** Use `openai-docs` before planning, changing, testing, or auditing a plugin. Always fetch the Plugins overview; fetch other official pages only for capabilities or stages in scope. Official documentation overrides this skill.

## Creation workflow

1. Establish the plugin's audience, recognizable job, inputs or data, expected result, identity boundary, and actions. Ask one question per turn unless the user requests a batch.
2. Propose the smallest useful skills-first design and explain how the user would experience it.
3. Consider MCP, OAuth, and UI separately. Classify each as `Recommended`, `Optional improvement`, `Not currently needed`, or `Unresolved`. State its benefit, visible difference, complexity or risk, and justification.
4. Show a grounded before/after diagram and capability comparison. For UI candidates, provide a requirements-based wireframe. Label concepts and assumptions; never fabricate screenshots, implementation, tests, results, or gains.
5. Obtain design approval, then guide implementation, testing, packaging, and release through small, reviewable stages.

Suggesting a capability is not approval to add it. Add MCP only for demonstrated live data, controlled actions, or operated code; OAuth only for demonstrated identity or external-account access; UI only for demonstrated visual interaction.

## Secondary support

| Mode | Result for the selected plugin |
| --- | --- |
| Improve | Evidence-backed gaps, improvement ideas, bounded recommendations, comparison, and regression checks. |
| Benchmark | Quality, reliability, stress-tolerance, and performance evidence, separated from planned or blocked checks. |
| Repair | Reproduction, reviewable patch, regression evidence, risks, and rollback notes. Never apply without explicit approval. |
| Audit | Read-only evidence report with missing proof marked `Unresolved`. |

## Safety and routed detail

Freshly confirm state-changing, destructive, financial, externally visible, deployment, submission, publication, account, and patch-application actions. Never convert source review or an unknown into a pass.

Read [plugin-workflow-checklist.md](references/plugin-workflow-checklist.md) only for the active creation stage or explicitly selected secondary mode.
