# Behavioral Evaluation and GitHub Hygiene Design

**Repository:** `MerverliPy/chatgpt-plugin-builder`

**Approved approach:** Sequential execution. The installed-plugin behavioral evaluation is a hard gate; GitHub hygiene begins only after the evaluation passes.

## Goal

Demonstrate that the released skills-only ChatGPT Plugin Builder reliably guides a user-selected plugin through creation or improvement without inventing evidence, drifting into building itself, or adding MCP, OAuth, or UI without demonstrated need. After that gate passes, complete the repository's community, security, and contribution hygiene without changing the plugin's product boundary.

## Current Baseline

- Public repository: `MerverliPy/chatgpt-plugin-builder`
- Default branch: `main`
- Published release: `v0.1.0`
- Latest verified workflow supplied in the project history: GitHub Actions run `31288044538`, reported as 10/10 passing.
- Architecture: skills-only; no MCP server, OAuth flow, or custom UI belongs to the builder itself.
- Known unresolved issue: the installed skill's displayed icon may revert after stored-content synchronization even though `skills/building-chatgpt-plugins/assets/icon.svg` contains the approved Guided Build icon.

## Scope A: Installed-Plugin Behavioral Evaluation

### Evaluation assets

Add a versioned evaluation pack under `evaluations/`:

- `evaluations/cases.json`: machine-readable cases and acceptance criteria.
- `evaluations/README.md`: clean-install, execution, evidence-capture, and rerun procedure.
- `evaluations/results/result-template.json`: result schema for one installed-plugin run.
- `tools/validate_behavioral_evaluations.py`: standard-library-only validation and summary command.
- `tests/test_behavioral_evaluations.py`: fixture, schema, coverage, and gate regression tests.

The case set will contain twelve cases:

1. Direct creation request: activate and guide the user's selected plugin.
2. Indirect creation request: infer the goal without redefining the builder.
3. Follow-up request: preserve prior decisions and ask only the next unresolved question.
4. Improvement request: propose evidence-based MCP, OAuth, and UI comparisons.
5. MCP boundary: recommend MCP only when live data or controlled tools justify it.
6. OAuth boundary: recommend OAuth only when user-specific authorization is required.
7. UI boundary: recommend UI only when visual interaction materially improves the workflow.
8. Benchmark request: evaluate the selected plugin, not the builder as a standalone product.
9. Repair request: propose a minimal patch for review without applying it automatically.
10. Missing-evidence request: label unsupported facts `Unresolved` instead of inventing evidence.
11. Negative generic coding request: do not force the plugin-building workflow.
12. Legacy-manifest boundary: discuss legacy formats only when the user explicitly requests them.

Each case records `id`, `category`, `prompt`, `expected_activation`, `required_behaviors`, and `forbidden_behaviors`. Follow-up cases also contain an ordered `turns` array.

### Execution and evidence

Run all cases against a clean installation of the packaged plugin in fresh conversations. Record the observed activation, response summary, required-behavior checks, forbidden-behavior checks, and redacted evidence for each case. The evaluator must not grade prose style; it grades observable boundary and workflow behavior.

### Hard pass gate

Scope A passes only when:

- all twelve cases have complete results;
- every required behavior passes;
- every forbidden behavior remains absent;
- no case invents sources, test results, repository state, user approval, or product capabilities;
- no repair is applied without explicit approval;
- no case changes the builder into an MCP-, OAuth-, or UI-backed product;
- `python -m unittest discover -s tests -v` exits `0`; and
- `python tools/validate_behavioral_evaluations.py evaluations/cases.json evaluations/results/installed-plugin-v0.1.0.json` exits `0`.

Any failure blocks Scope B. Corrections must be limited to the smallest skill, checklist, case, or validator change justified by the evidence, followed by the complete twelve-case rerun.

## Scope B: GitHub Project Hygiene

Scope B starts only after Scope A passes.

### Repository files

Add:

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/pull_request_template.md`
- `CODE_OF_CONDUCT.md`
- `docs/KNOWN_ISSUES.md`

Update:

- `README.md` with evaluation commands and links to contribution, security, conduct, and known-issues documents.
- `CONTRIBUTING.md` with the required test and behavioral-evaluation gates.
- `SECURITY.md` with the verified vulnerability-reporting channel.
- `tests/test_repository.py` with presence and internal-link regressions for the new community files.

`docs/KNOWN_ISSUES.md` will document the installed-icon synchronization issue without claiming its cause is known. It will distinguish the repository asset from the displayed installed-plugin icon and provide a verification procedure.

### Repository metadata

Proposed description:

> Skills-first guidance for creating and improving ChatGPT plugins with evidence-based MCP, OAuth, UI, evaluation, and repair workflows.

Proposed topics:

`chatgpt`, `codex`, `openai`, `plugin`, `skills`, `mcp`, `oauth`, `evaluation`, `python`

Metadata changes require a preview and explicit owner approval immediately before applying them.

### Security and branch settings

After confirming the exact options available to this public repository, propose:

- private vulnerability reporting;
- protection for `main` against force pushes and deletion; and
- the existing focused regression workflow as a required status check before merge.

Each GitHub setting change requires explicit owner approval immediately before it is applied. If a required check name or account-plan capability cannot be verified, label it `Unresolved` and leave the setting unchanged.

## Data and Control Flow

1. Validate the evaluation fixtures statically.
2. Install the unchanged skills-only plugin and run the twelve cases.
3. Validate the recorded results and stop on any failure.
4. Add community files and documentation with regression coverage.
5. Run the full repository test suite.
6. Present repository metadata and settings diffs for approval.
7. Apply only approved GitHub settings, then verify the final repository state and Actions status.

## Error Handling

- Malformed evaluation data produces a nonzero exit and names the exact file, case ID, and field.
- Missing or redacted evidence that prevents grading fails the affected case as `Unresolved`; it never receives an inferred pass.
- Installed-plugin behavior failures stop the sequence before repository-hygiene changes.
- GitHub API, permission, or plan limitations are reported verbatim and do not trigger workarounds that weaken protection.
- Existing unrelated repository content and the immutable `v0.1.0` tag remain unchanged.

## Testing Strategy

- Test-first changes for the evaluation schema, validator, result summary, community-file presence, and internal links.
- Focused tests after each file group, followed by `python -m unittest discover -s tests -v`.
- One complete installed-plugin run after static tests pass.
- Read-only verification of repository metadata, protection, vulnerability-reporting state, latest `main` commit, and workflow conclusion after approved settings changes.

## Non-Goals

- OpenAI Plugins Directory submission or publication.
- Adding an MCP server, OAuth flow, custom UI, hosted service, analytics, or telemetry to ChatGPT Plugin Builder.
- Publishing `v0.1.1` or modifying the immutable `v0.1.0` tag.
- Automatically applying generated patches to a user's selected plugin.
- Resolving the installed-icon synchronization issue without reproducible evidence of its cause.

## References

- OpenAI, “Connect and test your plugin”: https://developers.openai.com/plugins/deploy/connect-chatgpt
- OpenAI, “Package your plugin”: https://developers.openai.com/plugins/build/plugins
- OpenAI, “Plugin guidelines”: https://developers.openai.com/plugins/app-guidelines
