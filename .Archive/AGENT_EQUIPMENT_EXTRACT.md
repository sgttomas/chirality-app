---
description: "Extracts discrete physical equipment and package information from Knowledge Artifact files within a single DOMAIN Knowledge Type folder"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — EQUIPMENT_EXTRACT (Type 2 Task • KA→Equipment Extraction)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that reads all **Knowledge Artifact** (`KA-*.md`) files within a single assigned **DOMAIN Knowledge Type** folder and extracts every discrete physical equipment item mentioned — vessels, compressors, pumps, exchangers, valves, tanks, instruments, filters, meters, heaters, scrubbers, columns, control valves, PSVs, ESDVs, metering devices, and any other physically instantiated device.

The agent produces one **per-KTY equipment extract file** (`{KTY_ID}_Equipment_Extract.md`) in the shared output folder. Each extract lists every equipment item with its tag (when stated), name, package/module assignment (when documented), and source KA traceability.

**Important:** This agent is **read-only** on Knowledge Type folders. It extracts what exists; it does not modify KA files or infer equipment that is not mentioned.

**The human does not read this document. The human has a conversation with ORCHESTRATOR. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_EQUIPMENT_EXTRACT.md`); use the role name (e.g., `EQUIPMENT_EXTRACT`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | `{OUTPUT_ROOT}` only (`{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/`); read-only on all KTY folders |
| **BLOCKING** | never (but may return FAILED_INPUTS to ORCHESTRATOR) |
| **PRIMARY_OUTPUTS** | `{KTY_ID}_Equipment_Extract.md` |

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and interaction rules
2. **SPEC** — validity requirements (pass/fail)
3. **STRUCTURE** — allowed artifacts and schemas (what to write)
4. **RATIONALE** — intent / value hierarchy (how to interpret ambiguity)

If any instruction appears to conflict with ORCHESTRATOR's brief, **do not silently reconcile**. Report the conflict and proceed only if safety rules allow.

---

## Runtime parameters (provided by ORCHESTRATOR; do not hard-code)

| Parameter | Meaning | Default |
|---|---|---|
| `KTY_PATH` | Path to the Knowledge Type folder to extract from | **Required** |
| `KTY_ID` | The Knowledge Type ID (e.g., `KTY-04-01`) | **Required** |
| `OUTPUT_ROOT` | Path to `{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/` | **Required** |
| `DECOMP_VARIANT` | Must be `DOMAIN` | `DOMAIN` |
| `REPORT_TO` | Where to report run outcome | ORCHESTRATOR |

---

## Non-negotiable invariants

- **Read-only on KTY folders.** Never modify `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `Scoping.md`, or any `KA-*.md` file.
- **No invention.** Only extract equipment that is explicitly mentioned in the KA files. Do not infer equipment that might logically exist.
- **Exact tags.** Equipment tags must be exact matches from the source text. Do not infer or construct tag numbers.
- **Sourced package assignments.** Package/module names must come from the KA text or be marked `(indicated)` when contextually implied but not formally assigned. Use `N/A` when no package context exists.
- **Complete coverage.** Every `KA-*.md` file in the folder must be read. Missing KA files must be reported.
- **Null results documented.** KTYs with zero physical equipment still receive an extract file documenting the null result with explanation.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions & Safety Checks

**Action:**
1. Validate that `DECOMP_VARIANT` is `DOMAIN`. If not: return `RUN_STATUS=UNSUPPORTED_VARIANT` to ORCHESTRATOR.
2. Validate that `KTY_PATH` exists and is a directory. If not: return `RUN_STATUS=FAILED_INPUTS` with evidence.
3. Validate that `OUTPUT_ROOT` exists or can be resolved. If not: return `RUN_STATUS=FAILED_INPUTS` with evidence.

---

### Step 1 — Read KTY Context

**Action:**
1. Read `{KTY_PATH}/_CONTEXT.md` (best-effort).
   - Extract: KnowledgeType ID, name, parent Category ID and name.
   - If `_CONTEXT.md` is missing or ambiguous, fall back to the `KTY_ID` parameter and folder name for identity. Record the fallback in the output Package Notes.
2. Record the KTY identity fields for use in the output file metadata block and table rows.

**Output:** Internal understanding of KTY identity (ID, name, Category).

---

### Step 2 — Read Scoping and Enumerate KA Files

**Action:**
1. Read `{KTY_PATH}/Scoping.md` (best-effort) to obtain the artifact plan — the ordered list of KA files and their Subject mappings.
2. Enumerate all `KA-*.md` files present in the KTY folder by filesystem listing.
3. Reconcile the Scoping artifact plan against the filesystem enumeration:
   - If a KA file exists on disk but is not in Scoping: include it (record in Notes).
   - If a KA file is listed in Scoping but not on disk: record as missing in Package Notes; do not fail.
4. Build the ordered KA read list (prefer Scoping order; append any filesystem-only files at the end).

**Output:** Ordered list of KA files to read.

---

### Step 3 — Extract Equipment from Each KA

**Action:**
For each KA file in the read list:

1. Read the full text of the KA file.
2. Identify every discrete physical equipment item mentioned. Include:
   - Vessels, separators, drums, columns, towers
   - Compressors, pumps, blowers, fans
   - Heat exchangers, coolers, heaters, reboilers, condensers
   - Tanks, storage vessels
   - Filters, strainers, coalescers, scrubbers
   - Control valves, PSVs, ESDVs, shutdown valves, blowdown valves
   - Instruments, meters (flow meters, analyzers, transmitters when named as discrete devices)
   - Motors and drivers (when described as discrete tagged/named equipment)
   - Any other physically instantiated, discrete named/tagged device

3. For each equipment item, extract:
   - **Equipment Tag**: exact tag from source text (e.g., `V-1600-2`, `TK-6930-2`, `PCV-1601-2`). If no tag is stated, record `No tag`.
   - **Equipment Name**: descriptive name as stated in the KA, including key attributes in parentheses where the source provides them (e.g., type, sparing, configuration).
   - **Package Name**: module or package assignment if documented. Rules:
     - If a formal package/module name or number is stated (e.g., `Module 570 — TEG Regeneration Module`): use it exactly.
     - If equipment is contextually associated with a named unit or package but no formal assignment is stated: use the contextual name with `(indicated)` suffix.
     - If no package context exists: use `N/A`.
   - **Notes**: any qualifying information — sparing, scope uncertainties, conflicts, TBDs.

4. **Exclusion rules — do not list:**
   - Virtual machines or software instances (but document the null result if the entire KTY is virtual)
   - Buildings or structures themselves (but include equipment housed within them)
   - Documents, procedures, specifications
   - Non-physical items (data points, software licenses, network addresses)

5. If a KA file contains zero physical equipment items, record that observation internally for the Package Notes section.

**Output:** Per-KA equipment item list with tag, name, package, notes, and KA source reference.

---

### Step 4 — Assemble Equipment Table

**Action:**
1. Combine all per-KA equipment items into a single ordered table.
2. Assign sequential row numbers (`#` column) starting at 1.
3. Populate each row with:
   - `#` — sequential row number
   - `CAT` — parent Category ID (e.g., `CAT-004`)
   - `KTY` — Knowledge Type ID (e.g., `KTY-04-01`)
   - `KA Source` — the KA file identifier or filename from which the item was extracted
   - `Equipment Tag` — exact tag or `No tag`
   - `Equipment Name` — descriptive name
   - `Package Name` — formal name, contextual name `(indicated)`, or `N/A`
   - `Notes` — qualifying information
4. Order rows by KA source (following the read list order from Step 2), then by order of appearance within each KA.

**Output:** Complete equipment table ready for the output file.

---

### Step 5 — Write Package Notes

**Action:**
1. Write contextual observations about module/package groupings found across the KTY's KA files:
   - Whether formal package/module numbers were assigned or only implied.
   - Notable groupings (e.g., all items in a single named module, items split across packages).
   - Scope boundary notes (items where ownership or scope is ambiguous).
   - Items excluded with rationale (e.g., coalescing filter described as part of a stage rather than standalone).
   - References to active conflicts or TBDs that affect equipment identification.
2. For KTYs with zero physical equipment: explain why (e.g., all items are virtual machines, KTY covers documentation only).

**Output:** Package Notes section content.

---

### Step 6 — Write Output File

**Action:**
1. Write the output file to `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md`.
2. The file must follow the schema defined in STRUCTURE.
3. For KTYs with zero physical equipment:
   - The Equipment Table contains a single explanatory row or an empty table with a note.
   - An informational inventory may be included (e.g., virtual machines) for traceability, clearly marked as excluded from the equipment count.
   - The equipment count footer reads `0` with a parenthetical explanation.
4. Return `RUN_STATUS=OK` to ORCHESTRATOR with the output file path and the equipment count.

**Output:** `{KTY_ID}_Equipment_Extract.md` written to `{OUTPUT_ROOT}`.

---

### Step 7 — Report to ORCHESTRATOR

**Action:**
Return to the invoking agent:
- `RUN_STATUS` (`OK` | `WARNINGS` | `FAILED_INPUTS`)
- Output file path
- Equipment count (integer)
- Any warnings (missing KA files, parse issues, scope ambiguities)
- List of KA files read

[[END:PROTOCOL]]

---

### QA Contract

After completing extraction, EQUIPMENT_EXTRACT verifies:

| Check | Validation |
|-------|-----------|
| All KA files read | Every `KA-*.md` in the folder was read (or absence reported) |
| Equipment traceable | Every table row cites a specific KA source file |
| No invention | No equipment items appear that are not in the KA source text |
| Tags exact | Equipment tags are verbatim from source (not inferred) |
| Package assignments sourced | Package names are from source text, marked `(indicated)`, or `N/A` |
| Output file complete | Title, metadata, Equipment Table, Package Notes, count footer all present |
| KTY folder unmodified | No files in `{KTY_PATH}` were written or modified |
| Null result documented | KTYs with zero equipment have an extract file with explanation |

---

[[BEGIN:SPEC]]
## SPEC

An EQUIPMENT_EXTRACT run is valid when:

- Exactly one output file `{KTY_ID}_Equipment_Extract.md` is written to `{OUTPUT_ROOT}`.
- The output file contains all required sections: title, metadata block, Equipment Table, Package Notes, equipment count footer.
- Every `KA-*.md` file in the KTY folder was read (or its absence was reported).
- Every equipment item in the table is traceable to a specific KA source file.
- No equipment items were invented — only items explicitly mentioned in the KA files are listed.
- Equipment tags are exact matches from source text (not inferred or constructed).
- Package assignments are sourced from KA text, marked `(indicated)` when contextually implied, or `N/A` when absent.
- No files in the KTY folder were modified.
- KTYs with zero physical equipment have an extract file documenting the null result.

Invalid when:
- any file in the KTY folder is modified,
- equipment items are listed that do not appear in the KA source files,
- tags are inferred rather than extracted from source text,
- KA files in the folder are skipped without reporting,
- or the output file is missing required sections.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Input/Output contract

| | Description |
|---|---|
| **Inputs** | `KTY_PATH`, `KTY_ID`, `OUTPUT_ROOT` |
| **Reads** | `{KTY_PATH}/_CONTEXT.md`, `{KTY_PATH}/Scoping.md`, all `{KTY_PATH}/KA-*.md` files |
| **Writes** | `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md` |
| **Does not modify** | Any file in `{KTY_PATH}` — `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `Scoping.md`, `KA-*.md`, or any other file |

### Output file schema

The per-KTY extract file contains these sections in order:

1. **Title**: `# Equipment Extract — {KTY_ID} {KTY Name}`
2. **Metadata block**: Category, Knowledge Type, Source KA files, Extraction date
3. **Equipment Table**: markdown table with columns `#`, `CAT`, `KTY`, `KA Source`, `Equipment Tag`, `Equipment Name`, `Package Name`, `Notes`
4. **Package Notes**: bulleted contextual observations about package/module groupings, exclusions, and scope notes
5. **Equipment count footer**: `**{KTY_ID} Equipment Count: {N}**`

### Equipment Table column definitions

| Column | Content |
|---|---|
| `#` | Sequential row number (1-based) |
| `CAT` | Parent Category ID (e.g., `CAT-004`) |
| `KTY` | Knowledge Type ID (e.g., `KTY-04-01`) |
| `KA Source` | KA file identifier or filename from which the item was extracted |
| `Equipment Tag` | Exact tag from source text, or `No tag` |
| `Equipment Name` | Descriptive name with key attributes in parentheses |
| `Package Name` | Formal package name, contextual name with `(indicated)`, or `N/A` |
| `Notes` | Qualifying information: sparing, TBDs, conflicts, scope notes |

### Scope inclusion/exclusion

**IN scope (extract these):**
- Vessels, separators, drums, columns, towers
- Compressors, pumps, blowers, fans
- Heat exchangers, coolers, heaters, reboilers, condensers
- Tanks, storage vessels
- Filters, strainers, coalescers, scrubbers
- Control valves, PSVs, ESDVs, shutdown valves, blowdown valves
- Instruments, meters, analyzers (when named as discrete devices)
- Motors and drivers (when described as discrete tagged/named equipment)
- Any other physically instantiated, discrete named/tagged device

**OUT of scope (do not extract):**
- Virtual machines, software instances
- Buildings or structures (but include equipment housed within them)
- Documents, procedures, specifications
- Non-physical items (data points, software licenses, network addresses)

### Downstream consumer

This agent does **not** produce the consolidated `Equipment_Master_List.csv`. That is a separate assembly step (typically run by ORCHESTRATOR or AGGREGATION after all per-KTY extracts are complete) that concatenates the per-KTY extract tables into a single CSV register.

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Equipment identification is a cross-cutting concern in facility design. A single Knowledge Type describes a process subsystem, but equipment items within it must also be tracked as a flat register for procurement, tagging, modularization, and construction planning.

EQUIPMENT_EXTRACT bridges the per-KTY document structure and the facility-wide equipment register by:
- reading the production documents (KA files) that contain the ground-truth equipment descriptions,
- extracting every discrete physical device into a normalized table with source traceability,
- preserving package/module context so downstream assembly can group equipment by physical location,
- and producing a null-result file for KTYs without physical equipment, so the master list assembly step can confirm complete coverage without re-reading every KTY.

The agent is deliberately narrow: one KTY in, one extract file out. This keeps each invocation bounded and parallelizable — ORCHESTRATOR can spawn one EQUIPMENT_EXTRACT per in-scope KTY simultaneously. The consolidation into `Equipment_Master_List.csv` is a separate, deterministic assembly step that does not require re-reading KA files.

The "(indicated)" convention for package names preserves the distinction between formal assignments (engineer-designated module numbers) and contextual associations (equipment described within a named process unit but not formally tagged to a module). This distinction is critical for modularization planning: formally assigned packages can be used directly, while indicated packages require engineering confirmation.

[[END:RATIONALE]]
