# Plan: TOOL_POLICY.md Tier 1 Validator Extensions

## Context

The TOOL_POLICY.md Constitutional Conformance slice (closed 2026-04-04, recorded in `docs/PLAN.md` §6) added TOOL_POLICY.md presence check (#11) to `tools/validation/validate_skill_metadata.py`. The slice declared canonical section headings (5 H2 + 2 H3) and applied the two-part tool derivation rule across all 15 live skills.

During that slice, 2 of 4 parallel backfill subagents diverged on how to handle tools appearing in both the `allowed-tools` frontmatter and the `## Tool usage` body (dependency-extract, estimate-snapshot) — both produced TOOL_POLICY.md files where tools were duplicated across the two H3 subsections. Main-thread consolidation caught it and applied manual corrections. A deterministic validator check would have flagged the divergence before review.

This slice extends the validator with 4 additional TOOL_POLICY.md structural checks (Tier 1) that catch drift deterministically. It closes the R10 machine-enforcement piece for the skill-contract layer. It does NOT address Tier 2 (agent-based semantic fidelity auditing) or R11 (tool-contract validator) — both remain deferred per `docs/PLAN.md` §6.

**Outcome:** TOOL_POLICY.md structural conformance is machine-enforced on every validator run; drift between SKILL.md `allowed-tools` frontmatter and TOOL_POLICY.md TASK-enforced subsection is caught automatically.

---

## Scope — 4 new validator checks

| # | Check | Enforces |
|---|---|---|
| 12 | Canonical H2 headings (set + order) | All H2s from canonical 5-heading set; required H2s present; H2s appear in canonical order |
| 13 | Canonical H3 subheadings presence | `### TASK-enforced` and `### Operationally invoked` both present in file |
| 14 | `allowed-tools` ↔ TASK-enforced full-spec set equality | Full command specs (interpreter + path + scope_glob) in SKILL.md `allowed-tools` match exactly the specs listed under `### TASK-enforced` |
| 15 | Floor sections have meaningful content | Each required floor zone contains at least one list-item content line (not just H3 scaffolding/italic descriptors) |

**Canonical H2 headings (exact-string-match; case-sensitive):**
1. `## Preferred tool order` (optional)
2. `## Allowed deterministic tools` (required)
3. `## Expected use of reasoning` (optional)
4. `## Disallowed use` (required)
5. `## Write boundary` (required)

**Canonical H3 subheadings under `## Allowed deterministic tools`:**
- `### TASK-enforced` (required)
- `### Operationally invoked` (required)

---

## Implementation

### Check #12 — H2 heading canonical set + order

1. Read TOOL_POLICY.md content (after presence check passes at #11).
2. Extract lines matching `^## ` (strip prefix + trailing whitespace).
3. Validate each extracted heading is in the canonical 5-heading set.
4. Validate required H2s present (Allowed deterministic tools, Disallowed use, Write boundary).
5. Validate H2 appearance order is a subsequence of the canonical order.

**Failure messages:**
- `TOOL_POLICY.md: non-canonical H2 heading "<heading>"`
- `TOOL_POLICY.md: required H2 heading "<heading>" missing`
- `TOOL_POLICY.md: H2 headings appear out of canonical order`

### Check #13 — H3 subheadings presence

Scan TOOL_POLICY.md for exact-match `^### TASK-enforced` and `^### Operationally invoked`. Both must be present.

**Failure messages:**
- `TOOL_POLICY.md: required H3 subheading "### TASK-enforced" missing`
- `TOOL_POLICY.md: required H3 subheading "### Operationally invoked" missing`

*(Position check — verifying these H3s are under `## Allowed deterministic tools` specifically — is deferred. Presence check is sufficient for Tier 1; out-of-place subheadings would be caught by Tier 2 semantic review.)*

### Check #14 — `allowed-tools` ↔ TASK-enforced full-spec set equality

**Equality semantics:** full command spec equality. A spec is the complete string `<interpreter> <repo-relative-tool-path>:<scope_glob>` (e.g., `python3 tools/pdf2md/rasterize_pdf.py:*`). Interpreter and scope_glob are part of the TASK-enforced contract (already validated by existing Check #9) and must round-trip into TOOL_POLICY.md verbatim.

1. Refactor: split `parse_allowed_tools(raw_value, repo_root)` into two helpers:
   - `extract_allowed_tool_specs(raw_value) -> list[str]` — returns list of full spec strings from the comma-space-delimited raw value, no validation.
   - `validate_allowed_tool_specs(specs, repo_root) -> list[str]` — returns list of issue strings for an extracted spec list.
   - Existing `parse_allowed_tools` becomes a thin wrapper: `extract → validate → return issues`.
2. Extract TASK-enforced tool entries from TOOL_POLICY.md:
   - Find the block between `^### TASK-enforced` and the next `^### ` or `^## ` or EOF.
   - Extract list items matching pattern: lines starting with `- ` whose body contains a backtick-quoted spec. Extract the backtick content.
3. Compare full specs as sets:
   - If `allowed-tools` absent from SKILL.md frontmatter: TASK-enforced subsection must contain zero backtick-quoted spec entries.
   - If `allowed-tools` present: TASK-enforced subsection specs == frontmatter specs (set equality on full spec strings).
4. On mismatch, report set-difference diagnostic.

**Failure messages:**
- `TOOL_POLICY.md: TASK-enforced subsection lists specs, but allowed-tools frontmatter is absent`
- `TOOL_POLICY.md: TASK-enforced subsection missing specs from allowed-tools: <spec1>, <spec2>`
- `TOOL_POLICY.md: TASK-enforced subsection has specs not in allowed-tools: <spec1>, <spec2>`

### Check #15 — Floor sections have meaningful content

The floor check distinguishes two cases because `## Allowed deterministic tools` always contains H3 scaffolding and italic descriptors that would trivially pass a simple "non-blank lines between H2s" check.

**Case A — `## Disallowed use` and `## Write boundary`:**
For each of these H2 sections:
1. Find the H2 heading line.
2. Extract lines until the next `^## ` or EOF.
3. Exclude blank lines + the heading line itself.
4. Confirm ≥1 remaining line.

**Case B — `## Allowed deterministic tools`:**
Under EACH H3 subsection (`### TASK-enforced` and `### Operationally invoked`):
1. Find the H3 heading line.
2. Extract lines until the next `^### ` or `^## ` or EOF.
3. Require ≥1 line starting with `- ` (markdown list item).

Rationale: in the canonical template, content under each H3 is always a list item — either a backtick-quoted tool spec or a `- None — ...` declaration. The italic descriptor line (`_Tools from the allowed-tools frontmatter..._`) is schema scaffolding, not content. The list-item requirement prevents ceremonial shells where only the scaffolding is present.

**Failure messages:**
- `TOOL_POLICY.md: section "## <name>" is empty or contains only whitespace`
- `TOOL_POLICY.md: H3 subsection "### <name>" has no list-item content (expected at least one "- " entry)`

---

## Helper refactoring

`parse_allowed_tools(raw_value, repo_root)` currently returns a list of issue strings. Check #14 needs access to the parsed specs themselves.

**Refactor:**
- Add `extract_allowed_tool_specs(raw_value: str) -> list[str]` — returns parsed full spec strings; returns `[]` when `raw_value` is empty or malformed.
- Rename existing validation logic to `validate_allowed_tool_specs(specs: list[str], repo_root: Path) -> list[str]` taking pre-extracted specs.
- Keep `parse_allowed_tools(raw_value, repo_root)` as a thin wrapper for backward compatibility with existing callers.

Same behavior for all existing callers; new helper available for Check #14.

---

## Sequencing

Single main-thread slice — no subagent orchestration needed (scope is too focused: one file, 4 checks, 1 helper refactor).

1. Helper refactor (extract/validate split)
2. Add Check #12 (H2 canonical set + order)
3. Add Check #13 (H3 presence)
4. Add Check #14 (full-spec set equality; uses refactored helper)
5. Add Check #15 (meaningful floor content)
6. Update docstring (checks 12-15 added to numbered list)
7. Verification — run validator on live skills, then temp-tree negative tests per check

Each step is additive; the validator runs successfully at every intermediate state because checks are new, not replacing existing ones.

---

## Files to Modify

- `tools/validation/validate_skill_metadata.py` — helper refactor + 4 new checks + docstring update

No other files change.

---

## Verification

### Live skills check (no regression)

```sh
python3 tools/validation/validate_skill_metadata.py skills
# Expected: 15 valid, 0 invalid, 15 checked (unchanged from current state)
```

Any FAIL here means the prior slice's TOOL_POLICY.md files are non-conforming under the new checks. Investigate each: either fix the file or narrow the check.

### Temp-tree negative tests (one per new check)

Each fixture lives in its own `mktemp -d` directory with enough structure to isolate the targeted check. Critically: stub `tools/` files exist where needed so upstream checks (especially Check #10 tool-path existence) pass, letting the new check be the first failure.

**Check #12 negative — non-canonical H2:**
```sh
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/test-skills/bad-h2"
cat > "$TMPDIR/test-skills/bad-h2/SKILL.md" <<'EOF'
---
name: bad-h2
description: Test skill
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---
# SKILL — bad-h2
EOF
cat > "$TMPDIR/test-skills/bad-h2/TOOL_POLICY.md" <<'EOF'
# bad-h2 — Tool Policy
## Tools Used
## Allowed deterministic tools
### TASK-enforced
- None
### Operationally invoked
- None
## Disallowed use
- none
## Write boundary
- none
EOF
python3 tools/validation/validate_skill_metadata.py "$TMPDIR/test-skills"
# Expected: FAIL with "non-canonical H2 heading 'Tools Used'"
rm -rf "$TMPDIR"
```

**Check #13 negative — missing H3:**
Similar fixture; omit `### TASK-enforced` from TOOL_POLICY.md. Expect "required H3 subheading '### TASK-enforced' missing".

**Check #14 negative — full-spec mismatch (with stub tool files):**
```sh
TMPDIR=$(mktemp -d)
# Create stub tool files so Check #10 passes
mkdir -p "$TMPDIR/tools"
touch "$TMPDIR/tools/x.py" "$TMPDIR/tools/y.py"
mkdir -p "$TMPDIR/test-skills/spec-mismatch"
cat > "$TMPDIR/test-skills/spec-mismatch/SKILL.md" <<'EOF'
---
name: spec-mismatch
description: Test skill
allowed-tools: python3 tools/x.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---
# SKILL — spec-mismatch
EOF
cat > "$TMPDIR/test-skills/spec-mismatch/TOOL_POLICY.md" <<'EOF'
# spec-mismatch — Tool Policy
## Allowed deterministic tools
### TASK-enforced
- `python3 tools/y.py:*`
### Operationally invoked
- None
## Disallowed use
- none
## Write boundary
- none
EOF
python3 tools/validation/validate_skill_metadata.py "$TMPDIR/test-skills"
# Expected: FAIL with set-difference (missing "python3 tools/x.py:*", extra "python3 tools/y.py:*")
# NOT expected: Check #10 tool-path-does-not-exist (x.py stub exists)
rm -rf "$TMPDIR"
```

**Check #15 negative — empty Disallowed use:**
Similar fixture with `## Disallowed use` section blank between it and next H2. Expect "section '## Disallowed use' is empty".

**Check #15 negative — H3 subsection with no list item:**
Similar fixture where `### TASK-enforced` contains only the italic descriptor line (no `- None` or `- <spec>`). Expect "H3 subsection '### TASK-enforced' has no list-item content".

### Spot-check on live files

```sh
# Verify Check #14 passes on skills with allowed-tools declared
python3 tools/validation/validate_skill_metadata.py skills 2>&1 | grep -E "(pdf2md|dependency-extract|estimate-snapshot|deliverable-consistency)"
# Expected: all PASS
```

---

## Out of Scope / Deferred

- **H3 position check** — verifying `### TASK-enforced` / `### Operationally invoked` are under `## Allowed deterministic tools` specifically. Presence check is sufficient for Tier 1.
- **Tier 2 semantic fidelity audit** — LLM-based checks that TOOL_POLICY.md prose (Operationally invoked, Disallowed use, Write boundary, Expected use of reasoning) accurately reflects SKILL.md (`audit-tool-policy` TASK skill pattern). Deferred per `docs/PLAN.md` §6.
- **R11 tool-contract validator** — `tools/REGISTRY.md` schema, idempotence posture, scope boundary. Separate tool-layer scope; deferred per `docs/PLAN.md` §6.
- **Content structure beyond floor** — specific subsection formatting, list-item structure within sections. Not warranted at this tier.
