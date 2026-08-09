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

### A1. External local-only packaging wrapper

The immutable `v0.1.0` tag predates plugin packaging and must not be changed. Scope A therefore creates a temporary evaluation wrapper outside the tagged checkout. The wrapper copies the exact tracked `v0.1.0` tree, then adds only local installation metadata. Store the wrapper under a generated temporary directory, never commit it to the tag, and record both the immutable source-tree identity and wrapper identity. Remediation commits may use the same external-wrapper procedure. The implementation adds wrapper templates and a deterministic staging tool to the evaluation branch, but the staged wrapper itself remains generated evidence rather than source.

The generated wrapper contains:

- `.codex-plugin/plugin.json` containing exactly:

```json
{
  "name": "chatgpt-plugin-builder",
  "version": "0.1.0-local-eval",
  "description": "Local-only behavioral evaluation fixture for the skills-only ChatGPT Plugin Builder.",
  "skills": "./skills/"
}
```

- `.agents/plugins/marketplace.json` containing exactly:

```json
{
  "name": "chatgpt-plugin-builder-local-evaluation",
  "interface": {
    "displayName": "ChatGPT Plugin Builder Local Evaluation"
  },
  "plugins": [
    {
      "name": "chatgpt-plugin-builder-local-eval",
      "source": {
        "source": "local",
        "path": "./"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

The wrapper marketplace root is the generated wrapper root, so `source.path: "./"` resolves to that wrapper and never to the immutable source checkout. Before execution, verify the manifest fields and marketplace-relative path against the then-current official packaging documentation. If the documented schema differs, stop and amend this specification before changing files; do not silently improvise. This wrapper is only a test-install identity and does not alter `v0.1.0`, create `v0.1.1`, or authorize OpenAI directory submission.

### A2. Clean installation and installed-resource verification

For each complete evaluation run:

1. For the baseline, check out exact tag `v0.1.0`, resolve and record its 40-character commit SHA, verify the tag tree is clean, and copy only tracked files into a new temporary wrapper directory. For remediation, use the exact 40-character commit SHA instead of the tag.
2. Add the two wrapper metadata files from A1 only inside that temporary directory and record the staging-tool commit SHA.
3. Compute the source-tree and wrapper SHA-256 digests independently. For each digest, enumerate included files by normalized relative POSIX path, reject absolute paths, `..`, symlinks, duplicates, and non-UTF-8 paths, sort by the UTF-8 path bytes, then hash for each file: 8-byte big-endian path length, path bytes, 8-byte big-endian content length, and exact content bytes. The source digest covers only copied tracked source files; the wrapper digest also covers the two generated metadata files.
4. Add the marketplace rooted at the temporary wrapper and install `chatgpt-plugin-builder-local-eval` through the supported local marketplace flow in the ChatGPT desktop app or Codex host. Restart the host as required by the official packaging procedure.
5. Record the installed plugin name, local version, source tag or commit, source-tree digest, wrapper digest, staging-tool commit, product surface, product version if exposed, model, relevant settings, installation time, and evaluator identity.
6. Locate the installed cache at `~/.codex/plugins/cache/chatgpt-plugin-builder-local-evaluation/chatgpt-plugin-builder-local-eval/local/`, resolving the actual home directory without using an unresolved environment variable. Record its canonical absolute path. If the selected host uses a documented equivalent path, record that path and the documentation reference. If no readable installed cache or documented export is available, stop with installation verification `Unresolved`; do not grade behavior from the wrapper source.
7. Copy the readable installed cache to a read-only evidence snapshot, compute its canonical digest using step 3, and require it to equal the wrapper digest. Record the snapshot path and digest. Any host-generated files must be enumerated and excluded only by an explicit, versioned rule tested by the staging tool; unexplained differences fail verification.
8. From that installed-cache snapshot—not the source checkout or temporary wrapper—verify that all declared resources resolve: `SKILL.md`, every file directly referenced by `SKILL.md`, checklist/reference files, assets needed by the workflow, and `agents/openai.yaml`.
9. Verify that the installed snapshot's `agents/openai.yaml` exposes the intended default prompt and that invoking that prompt activates the installed skill.
10. Run one direct phrasing and at least two semantically equivalent phrasings for activation-critical cases; inconsistent activation or boundary behavior fails the case.
11. Start each case in a fresh conversation, except turns explicitly belonging to one multi-turn case.

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
- immutable source tag or commit, source-tree SHA-256, wrapper SHA-256, staging-tool commit, installed-cache snapshot SHA-256, and canonical installed-cache path;
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

The immutable release baseline is written once as:

`evaluations/results/source-v0.1.0-wrapped-<first-12-wrapper-sha256>.json`

It must bind the resolved `v0.1.0` commit, source-tree digest, wrapper digest, staging-tool commit, and installed-cache snapshot digest. If it fails, retain that result unchanged. Never describe the wrapper metadata as content of `v0.1.0`. Any rerun against a remediation commit after modifying `SKILL.md`, its checklist, cases, validator, wrapper templates, staging tool, or another behavioral resource must use:

`evaluations/results/unreleased-<40-character-commit-sha>-<first-12-package-sha256>.json`

The result body must contain every full commit and digest. Never overwrite or relabel a `v0.1.0` source result as remediation evidence.

### A5. Hard pass gate

Scope A passes only when:

- installed-cache snapshot verification passes and its digest equals the staged wrapper digest;
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
