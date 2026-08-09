# Plugin Workflow Checklist

Use current official documentation fetched for the task; this checklist does not replace it.

## Selected-plugin gate

- Name the selected plugin and record its source or planned structure, user outcomes, audience, data, identity boundary, mutation limits, and assumptions.
- Keep every skill, MCP/OAuth/UI artifact, fixture, test, metric, and patch inside that plugin's work. Decline or redirect standalone infrastructure for unspecified future plugins.
- Treat a missing repository, specification, credential, test tenant, safe dataset, traffic allowance, or threshold as `Unresolved` rather than evidence.

## Create or improve

- Run creation as a conversational interview. Ask one focused question per turn unless the user requests a batch, preserve confirmed answers, and resume from the next unresolved decision.
- Define the selected plugin's audience, job, inputs or data, expected result, identity boundary, and actions before choosing capabilities.
- Assess or design the skill layer first. For MCP, OAuth, and UI, record `needed`, `not needed`, or `Unresolved`. Mark `needed` only from a selected-plugin functional, data, identity, or interaction requirement or inspected evidence. A request naming the technology or an assumption may illustrate alternatives but cannot justify expansion.
- Still suggest relevant MCP, OAuth, and UI improvement ideas. For each, state the user-visible benefit, implementation complexity or risk, recommendation level, and the concrete requirement that would justify adding it.
- Add MCP for needed live data, controlled actions, or operated code. Give each tool one job, exact schemas, useful model-readable results, truthful annotations, bounded inputs, timeouts, and replay-safe retries.
- Add OAuth only when identity or external-account access is needed. Enforce authorization and tenant ownership server-side with least privilege, secure secret storage, token redaction, and verified tokens, scopes, audience, and target identifiers.
- Keep UI optional, accessible, state-restorable, and useful only for visual interaction. Preserve a useful non-UI result, exact CSP domains, and no secrets in component data.
- Compare the actual or stated baseline with the proposed plugin using an architecture/workflow diagram and capability table. Label assumptions and conceptual changes. Add a wireframe only when UI is planned; never fabricate screenshots, implementation, tests, results, or performance gains.
- Obtain approval of the creation design before implementation, then proceed through small, reviewable build and validation stages.
- For Improve, attach observed evidence, bounded recommendations, and regression checks to each selected-plugin gap.
- Ensure skill resources and package paths resolve after installation.

## Benchmark

Build the measurement plan from the selected plugin's user outcomes, tool boundaries, risks, and environment. Do not replace the selected plugin with a reusable benchmark product or dashboard.

1. **Quality:** test correct outcome, tool selection, inputs, results, unsupported requests, negative selection, safety annotations, and model-readable fallbacks.
2. **Reliability:** test malformed and empty inputs, authentication and authorization, failures, timeouts, rate limits, retries, replay, concurrency, and duplicate-write prevention.
3. **Stress tolerance:** define safe ramp, spike, soak, and concurrency cases within explicit service and test-tenant limits; never load-test production without target-specific approval.
4. **Performance:** record environment, workload, sample size, thresholds, latency percentiles, throughput, error rate, saturation, and cold-start behavior where applicable.
5. Run static, type, unit, integration, MCP Inspector, and ChatGPT direct/indirect/follow-up/boundary checks that apply. If UI exists, test rendering and interaction, approval handoff, state restoration, accessibility, CSP and console errors, model-readable fallback, and relevant UI latency or resource-failure states. Preserve inputs, outputs, errors, and confirmation behavior with secrets redacted.
6. Separate measured results from estimates, planned checks, blocked checks, and `Unresolved` evidence. Compare releases only under equivalent conditions.

## Repair

- Reproduce the selected-plugin defect and capture redacted evidence before proposing a change.
- Provide a minimal reviewable patch or diff, the regression test that fails before it, retest evidence, impact, risks, and rollback notes.
- Do not apply a proposed patch, modify an account, deploy, submit, publish, or change an external system until the user explicitly approves that exact action and target.
- After approval, apply only the reviewed scope and rerun the relevant regression and benchmark gates. Report divergence and stop for renewed approval.

## Audit, test, and release

Report scope and redacted evidence; `Ready`, `Conditional`, or `Blocked`; findings with severity, impact, remediation, and retest; test register; unresolved facts; and smallest safe next action.

Block release on unconfirmed sensitive actions, cross-account access, exposed secrets, duplicate non-idempotent writes, prompt-injection-led disclosure/action, silent third-party-state divergence, fabricated evidence, or unresolved critical tests. Require target-specific approval before release and distinguish readiness from actual approval or publication.
