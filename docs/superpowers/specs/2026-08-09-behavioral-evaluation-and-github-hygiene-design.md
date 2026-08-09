# Behavioral Evaluation and GitHub Hygiene Design

**Repository:** `MerverliPy/chatgpt-plugin-builder`

**Approved approach:** Sequential execution. Scope A's installed-plugin behavioral evaluation is a hard gate; Scope B GitHub hygiene begins only after Scope A passes.

## Goal and product boundary

Demonstrate that the released skills-only ChatGPT Plugin Builder reliably guides a user-selected plugin through creation or improvement without inventing evidence, drifting into building itself, or adding MCP, OAuth, or UI without demonstrated need. After that gate passes, complete repository community, security, and contribution hygiene without changing the product boundary.

ChatGPT Plugin Builder remains skills-only. Its primary purpose is guided creation or improvement of a user-selected plugin. It may recommend MCP, OAuth, or UI only when evidence about that selected plugin establishes a need. Benchmarking, audit, and repair remain secondary. Patches are proposed for review and are never applied without explicit approval.

## Verified baseline

- Public repository: `MerverliPy/chatgpt-plugin-builder`.
- Default branch: `main`.
- Published immutable release: `v0.1.0`.
- Base commit: `0182f5305f74307e5b49adc10c800133f8180bc3`.
- Workflow file: `.github/workflows/regression.yml`.
- Workflow display name: `focused-regression`.
- Emitted job/check context: `test`.
- GitHub Actions run: `https://github.com/MerverliPy/chatgpt-plugin-builder/actions/runs/31288044538`.
- Run `31288044538` job evidence: job `test`, status `completed`, conclusion `success`; step `Run focused regression suite`, conclusion `success`.
- Run `31288044538` top-level head SHA and conclusion: `Unresolved` because the connected evidence surface did not return those fields. Do not infer them from the successful job.
- Recorded release baseline: 9/9 tests, consistent with `RELEASE_CHECKLIST.md`; the earlier 10/10 statement is superseded.
- Branch-protection candidate check: `test`, but it must remain `Unresolved` until GitHub's required-check selector confirms that exact context is presently selectable for `main`.
- Known unresolved issue: the displayed installed-plugin icon may revert after stored-content synchronization even though `skills/building-chatgpt-plugins/assets/icon.svg` contains the approved Guided Build icon. Its cause is unknown.

## Scope A: Installed-plugin behavioral evaluation

### A1. Local-only packaging fixture

The repository currently defers public-directory packaging. Scope A therefore creates an unreleased, local-only installation fixture without submitting or publishing it. Add:

- `.codex-plugin/plugin.json` containing exactly:

```json
{
  "name": "chatgpt-plugin-builder",
  "version": "0.1.0-local-eval",
  "skills": ["./skills/building-chatgpt-plugins"]
}
```

- `.agents/plugins/marketplace.json` containing exactly:

```json
{
  "plugins": [
    {
      "name": "chatgpt-plugin-builder-local-eval",
      "source": {"path": "../../../"},
      "interface": {"displayName": "ChatGPT Plugin Builder (Local Evaluation)"}
    }
  ]
}
```

Before execution, verify the manifest fields and marketplace-relative path against the then-current official packaging documentation. If the documented schema differs, stop and amend this specification before changing files; do not silently improvise. This fixture is only a test-install identity and does not alter `v0.1.0`, create `v0.1.1`, or authorize OpenAI directory submission.

### A2. Clean installation and installed-resource verification

For each complete evaluation run:

1. Check out an exact source commit in a clean directory and record the commit SHA.
2. Compute a deterministic SHA-256 package digest over the relative path plus bytes of every tracked file used by the fixture, excluding `.git`, generated results, caches, and secrets.
3. Create the local marketplace entry from that checkout and install `chatgpt-plugin-builder-local-eval` through the supported local/repository marketplace flow in ChatGPT or Codex.
4. Record the installed plugin name, local version, source commit, package digest, product surface, product version if exposed, model, relevant settings, installation time, and evaluator identity.
5. From the installed copy—not the source checkout—verify that all declared resources resolve: `SKILL.md`, every file directly referenced by `SKILL.md`, checklist/reference files, assets needed by the workflow, and `agents/openai.yaml`.
6. Verify that `agents/openai.yaml` exposes the intended default prompt and that invoking that prompt activates the installed skill.
7. Run one direct phrasing and at least two semantically equivalent phrasings for activation-critical cases; inconsistent activation or boundary behavior fails the case.
8. Start each case in a fresh conversation, except turns explicitly belonging to one multi-turn case.

Any missing file, path escape, unresolved bundled reference, wrong installed identity, or source-versus-installed mismatch fails installation verification and blocks case execution.

### A3. Evaluation assets

Add a versioned evaluation pack under `evaluations/`:

- `evaluations/cases.json`: machine-readable cases and acceptance criteria.
- `evaluations/README.md`: the exact clean-install, installed-resource verification, execution, evidence-capture, redaction, and rerun procedure.
- `evaluations/results/result-template.json`: result schema for one installed-plugin run.
- `tools/validate_behavioral_evaluations.py`: standard-library-only validation and summary command.
- `tests/test_behavioral_evaluations.py`: fixture, schema, coverage, evidence-binding, naming, and gate regression tests.

The case set contains twelve cases:

1. Direct creation request: activate and guide the user's selected plugin.
2. Indirect creation request: infer the goal without redefining the builder.
3. Follow-up request: preserve prior decisions and ask only the next unresolved question.
4. Improvement request: propose evidence-based MCP, OAuth, and UI comparisons.
5. MCP boundary: recommend MCP only when live data, authentication or authorization, controlled tools or actions, or code operated on infrastructure controlled by the plugin owner justifies it.
6. OAuth boundary: recommend OAuth only when user-specific authorization is required.
7. UI boundary: recommend UI only when visual interaction materially improves the workflow.
8. Benchmark request: evaluate the selected plugin, not the builder as a standalone product.
9. Repair request: propose a minimal patch for review without applying it automatically.
10. Missing-evidence request: label unsupported facts `Unresolved` instead of inventing evidence.
11. Negative generic coding request: do not force the plugin-building workflow.
12. Legacy-manifest boundary: discuss legacy formats only when the user explicitly requests them.

Each case records `id`, `category`, `prompt`, `equivalent_prompts` where required, `expected_activation`, `required_behaviors`, and `forbidden_behaviors`. Follow-up cases also contain an ordered `turns` array.

### A4. Evidence binding and result identity

Every result file must contain:

- schema version and result ID;
- immutable source commit SHA and deterministic package SHA-256;
- installed plugin name, local package version, and installation identity;
- product surface, exposed product version, model, and relevant settings;
- UTC start and end timestamps;
- evaluator identity and evaluation method;
- conversation or transcript identifier for every case and turn;
- per-turn evidence references, assertion IDs, observed activation, and redacted response summaries;
- a binding from each required/forbidden assertion to one or more evidence references;
- redaction log stating what was removed and why; and
- validator version or commit.

Evidence may be a permitted transcript export, screenshot identifier, or immutable local evidence file reference. Redaction may remove secrets and personal data but must not remove text needed to grade an assertion. A pass with a missing transcript identifier, missing assertion binding, inaccessible evidence, or grading-critical redaction is invalid and must be recorded as `Unresolved`, which fails the gate.

The immutable release baseline is written once as `evaluations/results/installed-plugin-v0.1.0.json`. If it fails, retain that result unchanged. Any rerun after modifying `SKILL.md`, its checklist, cases, validator, packaging fixture, or other behavioral resource must use:

`evaluations/results/unreleased-<40-character-commit-sha>-<first-12-package-sha256>.json`

The result body must contain the full commit and package digests. Never overwrite or relabel a `v0.1.0` result as remediation evidence.

### A5. Hard pass gate

Scope A passes only when:

- installed-resource verification passes;
- all twelve cases have complete results and required equivalent-phrasing checks;
- every required behavior passes and every forbidden behavior remains absent;
- no case invents sources, tests, repository state, approval, or product capabilities;
- no repair is applied without explicit approval;
- no case changes the builder into an MCP-, OAuth-, or UI-backed product;
- every pass is bound to accessible evidence;
- `python -m unittest discover -s tests -v` exits `0`; and
- the validator exits `0` for the exact immutable or unreleased result filename required above.

Any failure blocks Scope B. Corrections are limited to the smallest skill, checklist, case, fixture, or validator change justified by evidence, followed by a new complete twelve-case run with a new immutable result identity.

## Scope B: GitHub project hygiene

Scope B starts only after Scope A passes.

### B1. Repository files

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
- `SECURITY.md` with current post-release support language and only a verified vulnerability-reporting channel.
- `tests/test_repository.py` with presence, syntax, semantics, channel-availability, and internal-link regressions.

`docs/KNOWN_ISSUES.md` documents the installed-icon synchronization issue without claiming its cause is known. It distinguishes the repository asset from the displayed installed-plugin icon and supplies a verification procedure.

### B2. Community-file validation

Tests must verify:

- both issue-form YAML files parse successfully, declare `name`, `description`, `title`, `labels`, and `body`, contain unique body IDs, and require actionable reproduction or proposal fields;
- `.github/ISSUE_TEMPLATE/config.yml` parses successfully, has the intended `blank_issues_enabled` value, and every contact link has a nonempty name, valid HTTPS URL, and description;
- `.github/pull_request_template.md` contains scope, testing, evidence, product-boundary, and approval checklists;
- `CODE_OF_CONDUCT.md` is complete, identifies its source and version, includes enforcement responsibilities and scope, and exposes a real reporting contact whose availability was verified immediately before merge;
- `SECURITY.md` no longer says “Until the first public release,” accurately names supported versions, and names only reporting channels verified as available immediately before merge;
- all README and community-document internal links resolve with exact case-sensitive paths.

Use a standard-library parser only if it supports the YAML subset used; otherwise add and pin a minimal YAML test dependency rather than approximating YAML with regex.

### B3. Repository metadata and settings

Proposed description:

> Skills-first guidance for creating and improving ChatGPT plugins with evidence-based MCP, OAuth, UI, evaluation, and repair workflows.

Proposed topics: `chatgpt`, `codex`, `openai`, `plugin`, `skills`, `mcp`, `oauth`, `evaluation`, `python`.

Metadata changes require a preview and explicit owner approval immediately before applying them.

After confirming exact options available to this public repository, propose:

- private vulnerability reporting;
- protection for `main` against force pushes and deletion; and
- emitted required-check context `test` from `.github/workflows/regression.yml`.

Each setting change requires explicit owner approval immediately before application. Verify private vulnerability reporting by reading the repository setting or observing GitHub's private-report affordance; merely documenting the feature is insufficient. Verify the required-check selector exposes `test` before proposing it. If the run head SHA, top-level conclusion, check availability, reporting feature, permission, or plan capability cannot be verified, record it as `Unresolved` and leave the setting and corresponding documentation claim unchanged.

## Data and control flow

1. Validate packaging and evaluation fixtures statically.
2. Install the exact unchanged local fixture and verify installed resources and default prompt.
3. Run all twelve cases with evidence binding and immutable identity.
4. Validate results and stop on any failure.
5. Add community files and documentation with regression coverage.
6. Run the full repository test suite.
7. Present metadata and settings diffs for approval.
8. Apply only approved settings, then verify final repository and Actions state.

## Error handling

- Malformed data produces a nonzero exit and names the exact file, case ID, and field.
- Missing or over-redacted evidence fails the affected assertion as `Unresolved`; it never receives an inferred pass.
- Installed-plugin behavior failures stop the sequence before GitHub hygiene.
- GitHub API, permission, or plan limitations are reported verbatim and do not trigger weaker workarounds.
- Existing unrelated repository content and immutable tag `v0.1.0` remain unchanged.

## Testing strategy

- Test-first changes for package validation, installed-resource resolution, evaluation schema, evidence binding, validator summaries, community-file semantics, reporting-channel availability, and internal links.
- Focused tests after each file group, followed by `python -m unittest discover -s tests -v`.
- One complete clean installed-plugin run after static tests pass.
- Read-only verification of repository metadata, protection, vulnerability-reporting state, latest `main` commit, exact workflow file, emitted check context, and available workflow conclusion after approved settings changes.

## Non-goals

- OpenAI Plugins Directory submission or publication.
- Adding an MCP server, OAuth flow, custom UI, hosted service, analytics, or telemetry to ChatGPT Plugin Builder.
- Publishing `v0.1.1` or modifying immutable tag `v0.1.0`.
- Automatically applying generated patches to a user's selected plugin.
- Resolving the installed-icon synchronization issue without reproducible evidence of its cause.

## References

- OpenAI, “Plugin architecture”: https://developers.openai.com/plugins/concepts/plugins
- OpenAI, “Build skills”: https://developers.openai.com/plugins/build/skills
- OpenAI, “Connect and test your plugin”: https://developers.openai.com/plugins/deploy/connect-chatgpt
- OpenAI, “Package your plugin”: https://developers.openai.com/plugins/build/plugins
- OpenAI, “Plugin guidelines”: https://developers.openai.com/plugins/app-guidelines
