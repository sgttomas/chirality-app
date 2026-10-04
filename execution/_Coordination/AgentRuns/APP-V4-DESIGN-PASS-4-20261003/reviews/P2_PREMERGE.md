# P2 — independent pre-merge review, design pass 4, tranche 2

- **Reviewer:** P2. Type 2 TASK (Claude Opus 5.5, `claude-opus-5-5`),
  dispatched by HELP_HUMAN for run `APP-V4-DESIGN-PASS-4-20261003`. No
  delegation. I authored none of the reviewed work.
- **Candidate:** commit `c7f9fe4073` on `claude/app-v4-design-pass-4-t2`
  (worktree clean). Its merge base with `origin/main` is `75604b3c49`, which
  is also the local `origin/main` ref (not fetched). 41 commits, 327 changed
  files (287 added, 40 modified).
- **Method:** `coordinated-knowledge-work` §3 and §6. I checked only what
  the unit reviews (RV2, RV3) did not establish. I did not re-review units
  already confirmed READY.
- **Tools and limits:** read-only git; no network. Every prototype and CI
  check ran in a scratch clone of the candidate (`git clone --shared` into
  `$TMPDIR/p2pm-t2/clone`, checked out at `c7f9fe4073`), never in the
  worktree. Paths below are relative to `projects/chirality-app-v4/execution`
  (E). `RUN/` is this run folder. `PKG-*/1_Working/` is dropped.
- **Write record:** this file only.

## Verdict: **HOLD**

There is 1 BLOCKING finding, 2 MAJOR, 5 MINOR and 12 NOTEs.

- **P2-F1 (BLOCKING).** At the candidate, `check_rp.py` on the committed
  fixture FX-RP1-6 gives **98/99**, not the recorded 99/99. The candidate's
  last commit appended R23-54/55 to `R23_RESOLUTIONS.md`, and the fixture
  pins that file's whole-file hash. The repair is mechanical, and I have
  verified it (below).
- **P2-F2 and P2-F3 (MAJOR)** are in owner-facing text and are one-paragraph
  fixes. I recommend making them in the same repair commit.

After the repair commit, the merge needs only a rerun of `check_rp.py`
(99/99) on that commit. No unit needs re-review.

Everything else holds:
- the fences;
- hygiene;
- the vendored copies;
- the closeout re-pins;
- the mechanical rounds (ACT-POLICY-v0.11, RA-v0.2, DA-v0.3, FV10-R9, N8,
  the GUIDE re-pin);
- the CI local equivalents;
- every other prototype count.

## Findings

### P2-F1 — BLOCKING — `check_rp.py` fails A-14 on the committed FX-RP1-6 at the candidate (98/99)

**Evidence.**
- I ran `python3 -B check_rp.py` (RUN/F) on the committed fixture. It gives
  `FAILS A-14 basis excerpts: listed sha256 holds; each equals its source
  lines at the source's current sha256` and **98/99 expectations held**.
- **The cause.** `FX-RP1-6/packet/basis-excerpts.md` heads two excerpts with
  `R23_RESOLUTIONS.md … (sha256 f0055836aa961a57…)`.
  - That file's hash is `f0055836…` at `158c0b2859` and at `161f8a0d0d`.
  - At `c7f9fe4073` it is `02f4fa663a937821…`, because the commit appended
    R23-54/55 (append-only, verified).
  - The excerpted lines (391–408, 617–632) are unchanged.
- **The recorded result is out of date.** DISPATCH row 139 records "RP
  99/99". That was true at `158c0b2859`, but it is not true at the candidate.
- **The repair, as I ran it.** I ran the documented build order in the
  clone (`build_aa.py --at 122c5abcf5`, `build_ca.py --at 122c5abcf5
  --archives`, `pvlib.py --at b2fbfdbac8`, `build_fx_rp1.py`).
  - AA, CA and PV rebuilt byte-identical.
  - `build_fx_rp1.py` rewrote five FX-RP1-6 files. Each change is a hash
    field: the excerpt headers in `basis-excerpts.md`, then the hashes that
    chain from it in the packet manifest, the package `subject`, the
    disposition's `package_file` and `MANIFEST.sha256`.
  - `check_rp.py` then gives **99/99**.
  - So the README's "same bytes on every run" holds only while
    `R23_RESOLUTIONS.md` is unchanged.

**Consequence.**
- The merge policy requires validation on the actual candidate, and one of
  the deliverable's own checks fails on it.
- The same failure will recur on every later R23 append, including any
  ruling made about this review.

**Repair.**
1. Make the last R23 append for this candidate first.
2. Then run `build_fx_rp1.py`, rerun `check_rp.py` (99/99), and commit the
   five fixture files with a one-line record (O-F.md or DISPATCH).
3. Alternatively, HELP_HUMAN rules that 98/99 stands, records why, and
   corrects the count.

Later, bind the excerpts to a commit, or report movement of an append-only
source as a NOTICE (as RA-v0.2 did for H-1).

### P2-F2 — MAJOR — the position statement leaves out two inventory gaps that rest with the person, and lists one confirmation of the person's as agent work

**Evidence.**
- **What R23-55.2 requires.** "The P60 inventory's Part C gaps go into the
  owner-facing position statement …, sorted by who closes them".
- **What the statement cites.** `POSITION_STATEMENT.md` cites G-01…G-14,
  G-16…G-22 and G-24…G-31 (counted by grep). It never cites **G-15** or
  **G-23**, and the word "amendment" does not appear in it.
- **G-15 is missing.** It is the register-level one-sided joins: F-RA1,
  mirror rows, DEP-09-01-027 and others. Its evidence is "the register
  UPDATE at the next amendment", and accepting an amendment is reserved to
  the person (OWNER_DECISIONS.md, "Scope of owner questions", Effect).
- **G-23 is missing.** It is the implementation-time design items. The
  inventory says "whether 60% requires them is the owner's reading".
- **G-25 is in the wrong list.** Its row reads "… to you or to an agent,
  **for you to confirm**". It sits under the heading "A. Design agents,
  with no decision from you". It is not repeated in B.

**Consequence.**
- "A short set of your own decisions" (B) understates what is reserved to
  the person. Two of those items do not appear in the statement at all.
- The statement is the person's basis for the 60% judgment.

**Repair.**
- Add G-15 (the next amendment's acceptance) and G-23 (whether 60% needs
  them) to B, or state where they sit.
- Move G-25's confirmation into B, leaving its drafting in A.

### P2-F3 — MAJOR — the tranche-2 receipt says the deliverables were "designed to the 60% level"

**Evidence.**
- RECEIPT.md L108–109: "Thirteen deliverables were designed to the 60% level
  and reviewed".
- R23-55.1: the tranche "does not claim the 60% position".
- The statement answers "Not yet".
- Inventory C.3 names four tranche-2 deliverables as thinner than their
  obligations:
  - G-18: DEL-08-01 §6–§8 "outline";
  - G-19: DEL-09-10 dossier "outline";
  - G-20: DEL-10-01 VERs not run "before … the 60% review";
  - G-21: DEL-10-02 VER-005/007 open.

**Consequence.** The receipt's first sentence contradicts the ruling and the
statement on the central question the person will judge.

**Repair.** Write, for example, "Thirteen deliverables were designed and
reviewed in the 60% design phase; the 60% position is not claimed (R23-55)".

### P2-F4 — MINOR — RTD says ACT-POLICY-v0.11 "added … a claim-connector check"; it did not

**Evidence.**
- RESEARCH_TO_DESIGN.md L33 says "v0.11 added a DEL-10-03 receiver row and a
  claim-connector check (checked by grep at this pin)".
- `git diff 75604b3c49 c7f9fe4073` of `ACT_AND_POLICY_CONTRACT.md` changes
  exactly three things: the label line, the added v0.11 note and the §10.3
  DEL-10-03 row.
- The check is DEL-06-01's `fleet_store.py`, as O-A's correction says
  (DISPATCH row 134; BRIEFS_AS_SENT L2715). That correction reached O-A and
  O-C. RTD carries HELP_HUMAN's earlier wording (BRIEFS_AS_SENT L2614).

**Consequence.** It misstates a supplier. Nothing RTD relies on is
affected: §2.1, the alias exclusion and §14 F-2 are unchanged.

**Repair.** Correct the sentence at RTD's next revision.

### P2-F5 — MINOR — CW and DRC disagree on what IA-1/IA-2 are

**Evidence.**
- CONNECTOR_WITNESS.md L37 reads "IA-1 PEC with Domains absent… IA-3 both
  absent (IA-2 rehearsed in EU-D1)".
- DOMAINS_RECEIVING.md L82 and `RUN/D/eud1.py` L478 define **IA-2** as "PEC
  adopted-current + Domains absent".
- So CW gives IA-1 the combination that DRC and the rehearsal call IA-2, and
  IA-1's real combination is stated nowhere.

**Consequence.** The IA-1/IA-3 rehearsal (CW L105, "Next unit") has no
consistent definition.

**Repair.** State all three IA combinations once and cite them from the
other side.

### P2-F6 — MINOR — records still name `RUN/D/build/` after the EUD1-R9 rename

**Evidence.**
- **VENDOR.json** (`DEL-06-01/Design/prototype/fixtures/vendored/EU-D1/`):
  the `source` for PR-P1, P3 and P6 is `…/D/build/records/…`.
  - `build/` was never in git (`.gitignore` `**/build/`), and it is now
    `D/evidence/`.
  - The bytes are equal: the `D/evidence/records/` copies hash to
    `b9cd7cce…`, `fcacb91a…` and `98aa1d8e…`.
- **FLEET_VIEWS.md, VER-006 row (L241).** It says the cases read "O-D's
  example records (`RUN/D/build/records/`, read as they are)". In fact
  `run_views.py` reads the vendored copies through
  `fleet_store.vendored()`.
- **FLEET_RECORDS.md L290 and VENDOR.json.** Both cite reader-input manifest
  `e68154c6…`, which existed only under `build/`. The committed
  `D/evidence/reader_input/MANIFEST.sha256` (`0ec2ed26…`, 20/20 OK) lists
  the same three hashes.

**Consequence.** Every hash still verifies, but someone reading from a clean
checkout is pointed at paths that do not exist.

**Repair.** At the next PKG-06 touch, add the `evidence/` path. VENDOR.json
is itself pinned (`VENDOR_SHA256 d02ffe5d…`, verified), so any edit to it
needs that pin changed too.

### P2-F7 — MINOR — "owner" names agents in owner-facing and Design text

**Evidence.**
- **RECEIPT.md, tranche 2:**
  - L138, "Cross-owner rows";
  - L153, "Owners now break each rule";
  - L158, "re-pinned by their owners".

  All three mean O-A…O-F.
- **QUALIFICATION_DOSSIER.md L161:** "This was decided by the owner, not
  re-pinned by script". This was O-C's decision.
- **LOCAL_HOST_QUALIFICATION.md L414:** "decided by its owner".

**Consequence.**
- The brief's rule, the inventory's convention ("'Owner' means the
  person") and PV2-N2 all reserve the word for the person.
- Read later, DOS L161 attributes a pin decision to the person.

**Repair.** Write "design agent" or "O-C" instead.

### P2-F8 — MINOR — the statement presents four separate early units as "one connected path end to end"

**Evidence.**
- POSITION_STATEMENT.md L44–48: "It then took one connected path end to end
  and had it read cold:", then four items.
- Only the decision-package path was carried end to end (WORK_GRAPH L27–36;
  RECEIPT tranche 1, "The early path").
- The connector standing, the execution basis and the replacement packet
  were separate early units, each read by its own isolated reader (RR-EUD1,
  RR-EB1, RR-EUF1/2/3).

**Consequence.** This slightly overstates how connected the evidence is.

**Repair.** Write, for example, "carried one decision package end to end;
three other early units were each read cold".

### Notes

- **P2-N1 — where PV1-R8 is carried.** RECEIPT L188 lists "EXP's
  `activity: validation` (PV1-R8)" under "Carried to the next amendment".
  PV §7 U-PV-4 and DISPATCH row 131 assign it to DEL-09-01's next design
  revision.
  - The carried one-sided items are disclosed as required:
    - U-PV-3: PV §2 O-3 and §7, DISPATCH row 136, the RECEIPT, statement
      G-12;
    - U-PV-4/PV1-R8: PV §7, DISPATCH row 131;
    - F-RA1: RA §3.4, ACT §10.3 row, the RECEIPT.
- **P2-N2 — RA-v0.2 S-6 row, last column (L50).** It still ends "**Request
  to O-A, not an edit by O-E**", while §2.3 records the mapping as done.
  - ACT §10.3's row names "RA-v0.1".
  - Both sides name the same sections: §2.1, §3 and §8 (with §8.2 and §8.4).
    The join agrees.
- **P2-N3 — `dag_reach.py` exit codes.** DA §5 says "exits 2 for
  SCC-forming and 0 otherwise".
  - The script also exits 2 for a self-arc, which is a cycle, so that is
    consistent.
  - It also exits 2 for an argparse usage error, and 1 for a missing named
    DAG version, so a caller cannot tell a usage error from SCC-forming.
  - The self-test is 5/5. I checked the arc direction by reading `arcs()`
    and `verdict()`: a proposed C → S is a cycle iff C ∈ reach(S), exactly
    as DA §5 says.
- **P2-N4 — the GUIDE pin check script is not committed.** It rests on
  B8's `pins.py` (sha256 `b943319d…5423`, as GUIDE L75 cites), which exists
  only in session scratch and hard-codes one worktree path. I ran a copy
  with its root set to my clone: **25/25**.
- **P2-N5 — superseded bytes that were never committed.** The supersession
  hashes of PRC-v0.1 `1a8acc85…`, CFB-v0.1 `ae49d654…`, CW-v0.1
  `f836c746…`, EB-v0.1 `e24101b2…` (RR-EB1's read), RP-v0.1 `1a06262b…` and
  EU-D1 v0.1 (`589f2c5d…` and the three records) are in no git object. I
  searched every execution blob in the commits since 2026-09-25.
  - The files disclose this ("never committed"; "cannot be restaged").
  - It predates R23-41. It affects provenance only.
- **P2-N6 — DISPATCH rendering.** The rows after the capability table
  (L102–142) have no table header, so they do not render as a table.
- **P2-N7 — one lane, two names.** CA names the Piping lane "SWBPIPE
  (`projects/chirality-piping`)"; RA X-1 and AA say "Piping". The path is
  the same, and `check_ca.py` passes. This is terminology only.
- **P2-N8 — "RTD ↔ PRC" has nothing to compare.**
  - RTD cites no PRC.
  - Neither `Dependencies.csv` (DEL-08-02, DEL-07-01) holds a row to the
    other.
  - DRC states "PEC's state plays no part in admission".
- **P2-N9 — path tokens that are not home paths.**
  - `/private/tmp/cvx-eud1*/codex-home` in `RUN/D/probe/results*/` is a
    synthetic probe home and carries no user name.
  - `/Users/` occurs only in the home-path detection regexes of
    `RUN/F/{aa,ca,pv}` and as `<name>`/`<owner>` placeholders.
- **P2-N10 — the statement's text about this review and the Q-9 quote.**
  - The statement says the last mechanical rounds "are covered by the
    pre-merge review". This file now covers them, with the findings above.
  - Its quote "hold unless you confirm the mapping" trims SCA3
    `OWNER_ITEMS.md` L76 ("**Hold** unless you confirm the mapping now").
    That is recommendation text, not the owner's words.
- **P2-N11 — CI that runs and was not run here.** The App and PEC plans
  select full coverage, because app-v4 paths match no registered rule.
  - "App Runtime integration" and "PEC workspace tests" were not run locally
    (Node toolchain).
  - No file in this diff is an input to either.
- **P2-N12 — merge with a merge commit, as P1-N3 said.** The documented
  builds read git at fixed commits: `build_aa.py`/`build_ca.py --at
  122c5abcf5`, `pvlib.py --at b2fbfdbac8`, and RV citations of
  `25054b04df`, `0bd6e4b4e9` and `caed56b8ea`. A squash or rebase merge
  would leave them unreachable from `main` once the branch is deleted, and
  those builds would fail.

## What I checked, and how

### C1 — placement and fences (brief item 1)

- **Placement.** `git diff --name-only 75604b3c49 c7f9fe4073` gives 327
  files, all under `projects/chirality-app-v4/execution/`.
- **Governed records.** No ScopeOfWork, `Dependencies.csv`, `_DEPENDENCIES`,
  register, `_DAG/`, `_Decomposition/` or Open_Issues path is in the diff.
  The same holds from `13b07065e1` (the start of pass 4), which supports
  the statement's "in pass 4".
- **Instructions.** No Root, `docs/`, `agents/` or other-project file
  changed.
- **Pinned and append-only run records.**
  - `RUN/OWNER_DECISIONS.md` is unchanged.
  - `R23_RESOLUTIONS.md`, `OWNER_DECISIONS_2.md` and `DISPATCH.md` are
    pure appends: the base bytes are a byte prefix of the candidate (`cmp`).
  - The RECEIPT title and one O-A heading changed in place. Both are run
    records.
- **Closed tranche manifests.** I extracted every
  `projects/chirality-app-v4/…` path from the 151 manifests under
  `docs/governance_harness/tranche_manifests/`. None is in the diff.
  `ROOT-DGOV52-APPLICATION-20261004.yaml` cites `OWNER_DECISIONS_2.md` as
  custody of "I approve A1 and B1, go ahead". That text is present and
  unchanged.
- **Lifecycle.** All 41 `_STATUS.md` read `IN_PROGRESS`. The 13 tranche-2
  transitions each cite R23-31.9, R23-32 or R23-34.9 and the consultation
  `9ae4bea25bd9`, which equals the sha256 of `agents/AGENT_WORKING_ITEMS.md`.

### C2 — hygiene (brief item 2)

- **Home paths.** I grepped all 327 files at the candidate for
  `/Users/`, `/private/tmp/`, `-Users-`, `/home/`, the account name, `claude-501` and
  `ai-env`. The only hits are those in P2-N9 and BRIEFS_AS_SENT's
  placeholders and `~/` form.
- **Ignored files.** `git status --ignored` lists nothing under
  `projects/chirality-app-v4`.
- **Committed records that point at ignored paths.** Only `D/build/`
  references (P2-F6), and history in O-D.md and the RR-EUD1 record. Every
  reader account is committed:
  - RR-EB1 `018ebe7b…`;
  - RR-EUF1 `b7570e01…`;
  - RR-EUF2 `0d53d089…`;
  - RR-EUD1 `3b31e598…`.

  These equal the hashes DISPATCH records.
- **Record manifests (`shasum -c`):**
  - `F/aa/records` 2/2, `F/ca/records` 2/2, `F/pv/records` 3/3;
  - `D/evidence/reader_input` 20/20;
  - FX-RP1…FX-RP1-6: 8, 9, 11, 11, 12 and 12, all OK;
  - `E/fixtures/FX-DP1` 6/6.

### C3 — pins and vendored copies (brief item 3)

**Method.**
- I indexed the sha256 of every blob under `execution/` in the 282 commits
  since 2026-09-25, plus every tracked file at the candidate.
- I extracted 64-hex values, and 8–16-hex prefixes in pin context, from
  every Design file changed on the branch.
- I classified each hit as current, historic or unresolved. I read the line
  of every historic or unresolved hit on a line new to the branch.

**Changed Design files: 352 current, 161 commit ids, 139 historic, 157
unresolved.**
- **Historic hits on new lines.** Each is a supersession or "re-pinned
  from" note:
  - ACT, GUIDE, RTD, DAC, RRM, RA, CA, RP, PV, AA, EB, UC, DA, PRC and LHQ
    headers or change rows;
  - a dated read set (IS-EB1-1, UC L55);
  - or a stated keep. LHQ L10 pins ACT-v0.9, RS-v0.9 and EXEC-v0.7 at
    `cec590c5c3`, and DOS L9 and TOP L7 pin RS-v0.9, each under R23-21
    item 3.
- **The ruled exception.** LHQ L10's GUIDE-v0.7 `a656682e…` (DISPATCH O-C
  closeout row). The GUIDE diff since then is L26 (the ACT row) and L75–76
  (the note) only, so HC-7.3 and HC-7.9 are untouched.
- **Unresolved hits.** Most resolve to current files outside `execution/`:
  - project `docs/`;
  - Root `AGENTS.md` `f96feb19…`;
  - `workflows/`, `.agents/` and `tools/`;
  - the D-GOV-52 manifest and notices;
  - the export manifest.

  The rest are:
  - placeholder hashes (`1111…`, `2222…`, `3333…`) in DOS examples;
  - `pins.py` (P2-N4);
  - the never-committed bytes in P2-N5 and P2-F6;
  - a git tree id (CA L67);
  - pre-existing pass-3 or tranche-1 history lines.
- **No stale pin was found**, apart from the descriptive error in P2-F4.

**Pins in first-increment and pass-3 Design files to files changed here.**
- A full 12-hex search finds the base-version hashes of the 21 modified
  Design files only in the changed files' own supersession lines and in LHQ
  L10. Those files are ACT, GUIDE, FR, FV, the fleet schema and prototypes,
  DAC, LHQ, DOS, TOP, RRM, and the CIR and dossier examples.
- An 8-hex search confirms that DAC L141/L176 (`15e25a24…`) and RRM L15/L222
  (`b2ffba71…`) are history notes.
- The unchanged files' 38 hits on these files are all to ACT v0.3–v0.9 or
  GUIDE v0.1–v0.5, in dated "read at" lines, so none was made stale by this
  branch.

**The closeout re-pins resolve to current bytes:**
- DAC:12, RRM:19 and RTD to ACT `597f13bd…`;
- DAC:141 to FV `8c4e8378…`;
- RRM:15 to DOS `b4de982f…`;
- DOS:9, TOP:7 and RP:26 to LHQ `d59a1ea0…`;
- DOS:7 to the CIR schema `3fb8f586…`;
- RTD, PRC, DRC and CW to CFB `69c1f10e…`;
- FR, FV and RTD to the standing schema `bf4cef4d…`;
- RTD to DRC `7bfa7fc4…`;
- CA, AA and VENDOR to RA `811c868c…`.

O-C's closeout commit `18d6eae3e4` changed only pin lines, their change
rows and LHQ's CI-5 sentence. Each "replaced" final line was the trailing
blank line, so no row was lost.

**Vendored copies:**
- **RUN/F/vendor/VENDOR.json:** 8/8 entries. Each vendored copy equals its
  pin, equals `git show <source_commit>:<source>`, and equals the live
  source.
- **RUN/F/ca/vendor:** RA `811c868c…` at `ce64a97a2a`, 1/1.
- **DEL-06-01 `fixtures/vendored/EU-D1`:**
  - `VENDOR.json` hashes to `d02ffe5d…`, which equals `VENDOR_SHA256` in
    `fleet_store.py`;
  - the schema equals `git show 25054b04df:` of DEL-07-02's;
  - PR-P1/P3/P6/P8 equal `D/evidence/records/` and the committed manifest.
- **The RP fixtures' vendored LHQ schema and examples:** the `lhq_*` rows
  above, plus the FX-RP1-6 supplied CA-1 and AA-1 hand-overs. Those equal
  `F/ca/records/CA-1.handoff.json` and `F/aa/records/AA-1.status.json`
  byte for byte.

### C4 — cross-owner interfaces changed in tranche 2 (brief item 4)

| Join | Both sides read | Result |
|---|---|---|
| AA ↔ RA (X-1) | RA L59 X-1 "Root, Runtime, App v3 and Piping"; AA I-1 and RN-2 the same four; PEC "not a DEP-006 consumer" | Agree |
| CA ↔ AA, RA | CA I-1 X-1 (lane label: P2-N7); CA I-3 and FX-RP1-6 carry AA-1 v2's status, byte-equal; CA notes AA-1 is unchanged under AA-v0.3 | Agree |
| RP ↔ CA, AA, PV | RP I-4 first-cut `$defs/practitioner_standing`; PV §2 O-3 states the differences (format, `arrangement_ref`, `is_replacement_condition`), and `check_pv.py` K-12 recomputes them; S-6 hand-overs equal | One-sided by design; U-PV-3 disclosed |
| RTD ↔ CFB, DRC, PRC | RTD pins CFB `69c1f10e…`, the standing schema and DRC `7bfa7fc4…` at current bytes, and `check_rtd.py` P-0 enforces this | Agree; no PRC join (P2-N8); P2-F4 |
| CW ↔ DRC | CW §1 QD = DRC §5 QD; OC-1 agrees | IA labels disagree (P2-F5) |
| FV, FR ↔ standing vocabulary | Schema enums: envelope {adopted, not_adopted, outside_coverage, unknown}; condition {current, stale, partial, failing, absent, unknown}; claim_tier per connector; `fleet_store.py` reads these facets by name, validates each standing against the vendored schema, and maps condition `unknown` → *unknown* (CS-R5) | Agree |
| LHQ ↔ DOS, TOP, RRM, RP | All four pin LHQ or DOS at current bytes; each notes that v0.1 → v0.2 changed only §3 | Agree |
| ACT §10.3 ↔ RA §2 | ACT row: §2.1, §3, §8 (§8.2, §8.4); RA S-6: §2.1, §3, §8 | Agree (P2-N2) |
| DA §5 ↔ `dag_reach.py` | Arc test, version print, `--dag`, self-test pinned to DAG-004 | Agree (P2-N3 on exit codes) |

### C5 — mechanical rounds no unit reviewer confirmed (brief item 5)

- **ACT-POLICY-v0.11.**
  - `git diff 75604b3c49 c7f9fe4073` changes the label line, the added
    v0.11 note and the §10.3 DEL-10-03 row, and nothing else.
  - The file went `1bf0ce8e…` → `597f13bd…`.
  - `validate_policy.py` gives 6 PASS.
- **RA-v0.2.** The v0.1 → v0.2 hunks are the header, S-6 (L50), §2.3
  ("done"), F-RA1 §3.4 ("MIRROR (SR-6)"), the VER-006 row and the changes
  rows.
  - **RA1-R1 is confirmed.**
  - **RA1-R2 is confirmed:** the re-pin, the mapping recorded, and H-1 now
    reports drift as a NOTICE. `--strict` and `--self-test` cover both
    ways.
  - The residual wording is P2-N2.
  - `ra_check`: 31/0; `--strict` 31/0; `--self-test` 5 detected.
- **DA-v0.3.** **DA2-R1 is confirmed:** the CASE-004 row (L164) quotes the
  lineage section. **The RV3 note is confirmed:** the script prints the
  version it read, and the self-test is pinned to DAG-004 and skips with a
  NOTICE if it is absent. `dag_reach --self-test` gives 5/5.
- **FV10-R9.** `fleet_store.py` gained one branch, inside the
  record-supports-reliance loop and before the per-claim reliance test: a
  claim tagged with another connector is listed as unrelied. The need is
  then *unknown* unless the record names a route.
  - `run_fleet.py` case P8x tests exactly this.
  - The result is 46/46.
- **dos_check N8.** The code reads `sys.exit(1 if bad else 2 if unchecked
  else 0)`, and the docstring states the same. DOS quotes the current
  `c845bed8…`.
- **O-C's closeout re-pins.** See C3 for `18d6eae3e4` and for the targets'
  current bytes.
- **O-A's GUIDE re-pin.** `48df7404c7` changes L26 and adds L75–76 only.
  The pin check gives 25/25.

### C6 — every prototype rerun at the candidate (brief item 6)

All ran in the scratch clone with `PYTHONDONTWRITEBYTECODE=1`, and every
output went under `$TMPDIR/p2pm-t2`. After all runs, the only change in the
clone was FX-RP1-6, from `build_fx_rp1.py` (P2-F1). I restored it before
running `check_rp.py` again on the committed fixture.

| Owner | Check (command source) | Recorded | At `c7f9fe4073` |
|---|---|---|---|
| O-A | `run_fleet.py <scratch>` | 46/46 | 46/46 (committed FX-FL1 rebuilds identically) |
| O-A | `run_views.py <scratch>` | 36/36 | 36/36 |
| O-A | `validate_policy.py` | 6 PASS | 6 PASS |
| O-D | `D/run_d.py <scratch>` (D/README) | 297/297 | 297/297, including B-2 |
| O-D | `prototype/check_rtd.py` | 19/19 | 19/19 |
| O-D | `D/compare_sensitivity.py RR-EUD1/ACCOUNT.json D/key/EUD1_KEY.json` | 19/19 | 19/19 |
| O-E | `ra_check.py` | 31/0 | 31/0 |
| O-E | `dag_reach.py --self-test` | 5/5 | 5/5 (DAG-004, 212 arcs) |
| O-E (added) | `eb1_check.py --post-dispatch RUN/RR-EB1/SUPPLIED.sha256` | 125/0 (O-E.md L357) | 125/0. Default mode gives 120/3, the expected post-read drift of EB, R23 and WORK_GRAPH |
| O-F | `build_aa.py --at 122c5abcf5` then `check_aa.py` (F/README) | 47/47 | 47/47 (records rebuild byte-identical) |
| O-F | `build_ca.py --at 122c5abcf5 --archives` then `check_ca.py` | 37/37 | 37/37 (byte-identical) |
| O-F | `pvlib.py --at b2fbfdbac8` then `check_pv.py` | 38/38 | 38/38 (byte-identical) |
| O-F | `check_rp.py` | 99/99 | **98/99 on the committed fixture (A-14)**; 99/99 after `build_fx_rp1.py` (P2-F1) |
| O-C | `fw04_check.py`, DAC's documented command (FX-DP1, observation, EXP schema, RS and AS Design, ScopeOfWork) | 22/0 | 22/0 |
| O-C | RRM `run_standing_check.py` | 19/0 | 19 cases, 0 unexpected |
| O-C | `dos_check --outcomes` valid / without `--outcomes` valid / `--outcomes` schema-invalid / `--outcomes` DX | 0 / 2 / 0 / 1 | 0 / 2 / 0 / 1 (DX without outcomes: 1) |
| O-C | `cir_check` valid / CI-5 violations | 0 / 1 | 0 / 1 (schema-invalid file: 0, as designed) |
| O-C | `top_check` valid / CB-1 violations | 0 / 1 | 0 / 1 |
| C1 | DEL-09-06 `run_w14_rehearsals.py --out <scratch>` | 44/0 | 44 PASS, "ALL CHECKS HOLD" |
| C2 | B8 `pins.py`, check mode | 25/25 | 25/25 |
| DA §5 | `shasum -a 256 -c _DAG/DAG-004/SOURCE_MANIFEST.sha256` from E | 128/130 | 128/130; the failures are DEL-01-03 `Dependencies.csv` and `_DEPENDENCIES.md` |

### C7 — owner-facing records (brief item 7)

- **Owner quotes.**
  - The RECEIPT's three tranche-2 quotes are exact against
    `OWNER_DECISIONS_2.md`, including the double space in "acceptable.  It's".
  - R23-54's "You have substantial guidance … and axiology" is exact
    against `RUN/OWNER_DECISIONS.md` L86–92, apart from the line wrapping.
  - R23-54 quotes L-7, "the App implementation owner is the owner",
    correctly from the pass-3 file L183. That line is HELP_HUMAN's
    **Effects** record of option A ("That is you"), which the owner chose
    with "I will go with your recommendations". R23-54 presents it as the
    record, not as the owner's words, which is correct.
  - R23-55 quotes LOOP_INIT L153 exactly.
  - The statement's "not now" is L-6 option A's label ("A. Not now").
- **Overclaim.** Neither text claims anything built, qualified or observed
  ("Nothing is built, signed or qualified"; G-30, G-31). Exceptions: P2-F3
  (the 60% level) and P2-F8 (the connected path).
- **The other claims, as checked:**
  - 41/41 deliverables are IN_PROGRESS and have Design files;
  - 8 + 13 = 21 deliverables were designed in pass 4;
  - the version labels in "What landed" match each file's Contribution
    line;
  - PRs #1077 and #1079 match `git log`;
  - "three observed situations" matches R23-50/53;
  - R23-31…R23-55 are contiguous;
  - DAG-004 is 128/130;
  - D-GOV-52 is adopted by App v4 and delivered, with no receiving decision,
    for App v3 and Runtime (AA §4).
- **Sorting.** I checked the three lists against the inventory's cited
  evidence lines.
  - **A is design-agent work**, except G-25's confirmation (P2-F2).
  - **B is reserved to the person:**
    - G-21 "reserved to the owner";
    - G-26;
    - G-01 Q-9;
    - G-02 SPEC §5.4;
    - G-03;
    - G-04 and G-08, both shared with SWB.
  - **C.** The host joins and Q-7 are at a host join deferred by DECISION-3,
    and SCA3 LEDGER L188 says so. Also in C: PEC and Domains, and the Codex
    observations.
  - **Missing:** G-15 and G-23 (P2-F2).
- **"Owner".** The statement and R23-54/55 use it for the person, or quote
  it as a role label. Exceptions are P2-F7.

### C8 — CI (brief item 8)

`.github/workflows` has four workflows that run on every PR:
`governance-harness`, `harness-premerge`, `pec-tests` and
`piping-desktop-e2e`. I ran their local equivalents in the clone, with
base `75604b3c49`.

- **governance-harness:**
  - `validate_agent_instructions` exit 0;
  - `validate_workflow_metadata` exit 0;
  - `validate_conflict_markers` PASS;
  - `validate_run_record_leaks`: "249 changed run-record file(s) scanned; 0
    possible credential(s)";
  - G0–G3 exit 0 (G3 PASS);
  - G4 `--added-manifests-only`: 0 paths on the instruction surface;
  - `tools/run_affected_tests.py --base 75604b3c49`: selects `practitioner_harness` and `validation`,
    which gave 1156 passed.
- **harness-premerge and pec-tests:** `hosted_ci.py plan` selects **full**
  App and PEC coverage, because every path is unmatched. These are Node
  builds, and I did not run them (P2-N11).
- **piping-desktop-e2e:** `e2e_plan.py` gives `not-applicable`.

## What I did not check

- **Unit content.** I did not re-review any unit that RV2 or RV3 confirmed
  READY.
- **The CI Node jobs.** I did not run the App Runtime integration or the
  PEC workspace tests.
- **Pin labels.** I did not check, pin by pin, that each "current" pin's
  label names the file whose hash it carries. I read the lines of the
  closeout pins and of every historic or unresolved pin on a new line.
- **The `docs/` pins.** For pins resolved to current files outside
  `execution/` (project `docs/`, Root, workflows), I matched the hash only,
  not the cited sections.
- **BRIEFS_AS_SENT.md.** I checked its count and verbatim claims only as far
  as RV3-UC1 did; I relied on its placeholders.
- **The inventory's Part A rows.** I checked them only where the statement
  or the RECEIPT relies on them.
