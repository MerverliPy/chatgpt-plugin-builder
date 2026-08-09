# Behavioral Evaluation and GitHub Hygiene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and pass an evidence-bound installed-plugin behavioral gate, then add verified GitHub hygiene.

**Architecture:** Scope A stages an external wrapper around immutable source, computes canonical digests, validates twelve cases, and binds assertions to installed-cache evidence. Scope B remains blocked until Scope A has an independently verified complete pass.

**Tech Stack:** Python 3.12, standard library, `unittest`, JSON, YAML issue forms, GitHub Actions, local ChatGPT/Codex plugin marketplace.

## Global Constraints

- Preserve the skills-only, user-selected-plugin product boundary.
- Scope A must pass before any Scope B file or setting change.
- Never modify or relabel `v0.1.0`.
- No directory submission, `v0.1.1`, Builder MCP/OAuth/UI, telemetry, or automatic patch application.
- Missing evidence is `Unresolved` and fails its gate.
- Preview GitHub mutations and obtain explicit approval immediately before each one.
- Recheck official OpenAI packaging schemas before fixture creation.

---

## Scope A

### Task 1: Canonical external wrapper

**Files:**
- Create: `tools/stage_evaluation_wrapper.py`
- Create: `tests/test_evaluation_wrapper.py`
- Create: `evaluations/fixtures/plugin.json`
- Create: `evaluations/fixtures/marketplace.json`

**Interfaces:**
- `canonical_digest(root: Path, relative_paths: Iterable[str]) -> str`
- `tracked_paths(repo: Path, ref: str) -> list[str]`
- `stage_wrapper(repo: Path, ref: str, destination: Path) -> dict[str, str]`
- Result keys: `source_commit`, `source_digest`, `wrapper_digest`, `wrapper_root`.

- [ ] **Step 1: Write failing digest tests**

```python
def test_digest_order_and_content(self):
    first = canonical_digest(self.root, ["b.txt", "a.txt"])
    self.assertEqual(first, canonical_digest(self.root, ["a.txt", "b.txt"]))
    (self.root / "b.txt").write_bytes(b"changed")
    self.assertNotEqual(first, canonical_digest(self.root, ["a.txt", "b.txt"]))

def test_rejects_escape(self):
    with self.assertRaisesRegex(ValueError, "unsafe relative path"):
        canonical_digest(self.root, ["../outside"])
```

- [ ] **Step 2: Confirm missing-module failure**

Run: `python -m unittest tests.test_evaluation_wrapper -v`

Expected: import failure for `tools.stage_evaluation_wrapper`.

- [ ] **Step 3: Add exact fixtures**

`plugin.json` uses name `chatgpt-plugin-builder`, version `0.1.0-local-eval`, a nonempty description, and `skills: ./skills/`.

`marketplace.json` uses marketplace `chatgpt-plugin-builder-local-evaluation`, plugin `chatgpt-plugin-builder-local-eval`, source `{source: local, path: ./}`, policy `{installation: AVAILABLE, authentication: ON_INSTALL}`, and category `Developer Tools`.

- [ ] **Step 4: Implement canonical framing**

```python
def canonical_digest(root, relative_paths):
    digest = hashlib.sha256()
    items = validated_unique_regular_files(root, relative_paths)
    for path_bytes, path in sorted(items):
        content = path.read_bytes()
        digest.update(len(path_bytes).to_bytes(8, "big"))
        digest.update(path_bytes)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()
```

`validated_unique_regular_files` rejects absolute paths, `..`, non-POSIX normalization, duplicates, symlinks, and nonfiles. Use argument arrays for `git ls-tree -r --name-only` and `git rev-parse`. Copy only tracked files into a new external directory; add wrapper metadata after the source digest.

- [ ] **Step 5: Verify and commit**

```bash
python -m unittest tests.test_evaluation_wrapper -v
python -m unittest discover -s tests -v
git add tools/stage_evaluation_wrapper.py tests/test_evaluation_wrapper.py evaluations/fixtures
git commit -m "feat: add deterministic evaluation wrapper staging"
```

### Task 2: Twelve cases and result schema

**Files:**
- Create: `evaluations/cases.json`
- Create: `evaluations/result-schema.json`
- Create: `evaluations/results/result-template.json`
- Create: `tests/test_behavioral_evaluations.py`

**Interfaces:** Each case has `id`, `category`, `prompt`, optional `equivalent_prompts`, `expected_activation`, `required_behaviors`, `forbidden_behaviors`, and optional ordered `turns`. Every behavior has a stable `assertion_id`.

- [ ] **Step 1: Write failing coverage tests**

```python
def test_exact_case_ids(self):
    expected = {"direct-create", "indirect-create", "follow-up", "improve",
        "mcp-boundary", "oauth-boundary", "ui-boundary", "benchmark",
        "repair", "missing-evidence", "negative-generic-coding",
        "legacy-manifest"}
    self.assertEqual(expected, {case["id"] for case in self.cases})

def test_activation_phrasings(self):
    for case in self.cases:
        if case["expected_activation"]:
            self.assertGreaterEqual(len(case.get("equivalent_prompts", [])), 2)
```

- [ ] **Step 2: Run and confirm missing-fixture failures**

Run: `python -m unittest tests.test_behavioral_evaluations -v`

- [ ] **Step 3: Add all cases**

MCP covers live data, authentication/authorization, controlled tools/actions, and operated code. Repair forbids applying patches. Missing evidence requires `Unresolved`. Generic coding forbids forced activation. Legacy formats require explicit request.

- [ ] **Step 4: Add schema/template**

Require source ref/commit/digest, wrapper and installed-cache digests, staging-tool commit, cache path, surface/version/model/settings, UTC timestamps, evaluator, redactions, conversation IDs, turns, assertions, statuses, and evidence references.

- [ ] **Step 5: Verify and commit**

```bash
python -m unittest tests.test_behavioral_evaluations -v
python -m unittest discover -s tests -v
git add evaluations/cases.json evaluations/result-schema.json evaluations/results/result-template.json tests/test_behavioral_evaluations.py
git commit -m "test: define behavioral cases and evidence schema"
```

### Task 3: Evidence validator

**Files:**
- Create: `tools/validate_behavioral_evaluations.py`
- Modify: `tests/test_behavioral_evaluations.py`

**Interfaces:**
- `validate_cases(data: dict) -> list[str]`
- `validate_result(cases: dict, result: dict, filename: str) -> list[str]`
- CLI: `python tools/validate_behavioral_evaluations.py CASES RESULT`

- [ ] **Step 1: Write failing binding/naming tests**

```python
def test_rejects_unbound_pass(self):
    result = copy.deepcopy(self.valid_result)
    result["case_results"][0]["assertions"][0]["evidence_refs"] = []
    errors = validator.validate_result(self.cases, result, self.filename)
    self.assertTrue(any("pass assertion requires evidence" in e for e in errors))

def test_filename_uses_wrapper_digest(self):
    name = f"unreleased-{self.valid_result['source_commit']}-000000000000.json"
    errors = validator.validate_result(self.cases, self.valid_result, name)
    self.assertTrue(any("wrapper digest prefix" in e for e in errors))
```

- [ ] **Step 2: Confirm validator import failure**

Run: `python -m unittest tests.test_behavioral_evaluations -v`

- [ ] **Step 3: Implement validation**

Validate types, exact coverage, unique IDs, UTC timestamps, 40-character commits, 64-character digests, wrapper/cache digest equality, accessible evidence, redaction reasons, assertion bindings, and aggregate pass. Accept only `source-v0.1.0-wrapped-<wrapper-prefix>.json` or `unreleased-<commit>-<wrapper-prefix>.json`.

- [ ] **Step 4: Verify CLI behavior**

The incomplete checked-in template exits `1`. A complete synthetic result created in a test temporary directory exits `0`.

- [ ] **Step 5: Verify and commit**

```bash
python -m unittest discover -s tests -v
git add tools/validate_behavioral_evaluations.py tests/test_behavioral_evaluations.py
git commit -m "feat: validate evidence-bound behavioral results"
```

### Task 4: Installed-cache verifier

**Files:**
- Create: `tools/verify_installed_plugin.py`
- Create: `tests/test_installed_plugin.py`
- Create: `evaluations/README.md`

**Interfaces:** `verify_installed_cache(cache_root: Path, expected_digest: str) -> dict[str, object]` returns path, digest, resources, default prompt, exclusions, and errors.

- [ ] **Step 1: Write failing installed-resource tests**

```python
def test_resources_resolve(self):
    report = verify_installed_cache(self.fixture, self.digest)
    self.assertEqual([], report["errors"])
    self.assertIn("skills/building-chatgpt-plugins/SKILL.md",
                  report["resolved_resources"])

def test_digest_mismatch_blocks(self):
    report = verify_installed_cache(self.fixture, "0" * 64)
    self.assertIn("installed cache digest does not match wrapper digest",
                  report["errors"])
```

- [ ] **Step 2: Confirm missing-module failure**

Run: `python -m unittest tests.test_installed_plugin -v`

- [ ] **Step 3: Implement installed-only checks**

Default to resolved `~/.codex/plugins/cache/chatgpt-plugin-builder-local-evaluation/chatgpt-plugin-builder-local-eval/local/`. Permit another path only with documented evidence. Snapshot read-only, reuse canonical hashing, resolve every installed `SKILL.md` reference, and require `agents/openai.yaml` `interface.default_prompt`. Never inspect source as fallback.

- [ ] **Step 4: Document receipts**

Document tag staging, marketplace addition, restart, cache discovery, snapshot, digest comparison, direct plus two equivalent prompts, conversation/evidence IDs, redaction, and mandatory `Unresolved` stop.

- [ ] **Step 5: Verify and commit**

```bash
python -m unittest tests.test_installed_plugin -v
python -m unittest discover -s tests -v
git add tools/verify_installed_plugin.py tests/test_installed_plugin.py evaluations/README.md
git commit -m "feat: verify installed plugin cache and resources"
```

### Task 5: Execute immutable baseline gate

**Files:**
- Create after execution: `evaluations/results/source-v0.1.0-wrapped-<actual-prefix>.json`
- Modify only after failure evidence and separate approval: `skills/building-chatgpt-plugins/SKILL.md`
- Modify only after failure evidence and separate approval: `skills/building-chatgpt-plugins/references/plugin-workflow-checklist.md`

- [ ] **Step 1:** Run `python -m unittest discover -s tests -v`; require exit `0`.
- [ ] **Step 2:** Stage `v0.1.0` into a new external directory, install, restart, snapshot cache, and require cache digest equals wrapper digest.
- [ ] **Step 3:** Run twelve cases in fresh conversations except ordered follow-ups; run equivalent phrasings and bind every assertion.
- [ ] **Step 4:** Run the validator and full tests, then obtain independent evidence review.
- [ ] **Step 5:** If any assertion fails, commit the immutable failing result and stop Scope B. Remediation needs separate approval and a complete `unreleased-<commit>-<wrapper-prefix>.json` rerun.
- [ ] **Step 6:** If all pass, commit only the actual result:

```bash
git add evaluations/results/source-v0.1.0-wrapped-<actual-prefix>.json
git commit -m "test: record immutable v0.1.0 behavioral evaluation"
```

---

## Scope B — blocked until Task 5 passes

### Task 6: Community files and semantic tests

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/pull_request_template.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `docs/KNOWN_ISSUES.md`
- Modify: `tests/test_repository.py`

- [ ] **Step 1: Add failing semantic tests**

```python
def test_issue_forms_have_required_semantics(self):
    for name in ("bug_report.yml", "feature_request.yml"):
        data = load_yaml(ROOT / ".github/ISSUE_TEMPLATE" / name)
        self.assertTrue({"name", "description", "title", "labels", "body"}
                        <= data.keys())
        ids = [item["id"] for item in data["body"] if "id" in item]
        self.assertEqual(len(ids), len(set(ids)))
```

Also test HTTPS contact links, actionable fields, PR checklists, Code of Conduct source/version/scope/enforcement/contact, post-release SECURITY text, and case-sensitive links.

- [ ] **Step 2:** Run `python -m unittest tests.test_repository -v`; confirm missing-file failures.
- [ ] **Step 3:** Read-only verify private vulnerability reporting and a private conduct contact. Stop for owner direction if unavailable.
- [ ] **Step 4:** Add complete files. State only that icon synchronization may differ and its cause is unknown.
- [ ] **Step 5: Verify and commit**

```bash
python -m unittest tests.test_repository -v
python -m unittest discover -s tests -v
git add .github/ISSUE_TEMPLATE .github/pull_request_template.md CODE_OF_CONDUCT.md docs/KNOWN_ISSUES.md tests/test_repository.py
git commit -m "docs: add tested community health files"
```

### Task 7: Documentation and CI

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `SECURITY.md`
- Modify: `.github/workflows/regression.yml`
- Modify: `tests/test_repository.py`

- [ ] **Step 1:** Add failing tests for README commands/links, CONTRIBUTING Scope A gate, post-release security language, verified reporting channel, workflow name `focused-regression`, context `test`, and full unittest command.
- [ ] **Step 2:** Run `python -m unittest tests.test_repository -v`; confirm failures.
- [ ] **Step 3:** Apply minimal docs/workflow changes. Preserve skills-only scope and public `v0.1.0`; do not describe wrapper metadata as release content.
- [ ] **Step 4: Verify and commit**

```bash
python -m unittest discover -s tests -v
git add README.md CONTRIBUTING.md SECURITY.md .github/workflows/regression.yml tests/test_repository.py
git commit -m "docs: connect evaluation and contribution gates"
```

### Task 8: Separately approved GitHub settings

**Files:** No repository changes unless verification requires a documentation correction.

**Interfaces:**
- Description: `Skills-first guidance for creating and improving ChatGPT plugins with evidence-based MCP, OAuth, UI, evaluation, and repair workflows.`
- Topics: `chatgpt`, `codex`, `openai`, `plugin`, `skills`, `mcp`, `oauth`, `evaluation`, `python`.
- Candidate check context: `test`.

- [ ] **Step 1:** Read-only record description/topics, default branch, latest `main`, vulnerability-reporting availability, protection capabilities, selector availability for `test`, and current Actions evidence.
- [ ] **Step 2:** Present separate before/after previews for metadata, vulnerability reporting, and protection.
- [ ] **Step 3:** Obtain explicit owner approval immediately before each mutation; leave every `Unresolved` setting unchanged.
- [ ] **Step 4:** Apply only approved changes and reread exact state. Never publish a release, tag, or directory submission.
- [ ] **Step 5:** Run `python -m unittest discover -s tests -v`, require exit `0`, and obtain independent final review.
