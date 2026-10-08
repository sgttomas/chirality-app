# N-1 blank native-step form — V4-EXM-10

PREPARATION ONLY. No examination opened, record assigned, run attempted or observation recorded.
Blank fields are unobserved/unsupplied, not assertions of absence or not-applicability.

Preparation SHA-256 (canonical JSON): 3c1e16dab343aaf1d36f402a365b865a0e590365ec077201bb84e43c80969e40
Case: V4-EXM-10
Planned run label: RUN-A
Candidate slot: one_same_candidate (unassigned)

## Header

- Record id: __________
- Candidate revision: __________
- Build identity: __________
- Package record if any: __________
- Codex pin: __________
- WKWebView / WebKit version: __________
- OS version: __________
- Person operating: __________
- Examiner recording: __________
- Date: __________
- Time zone: __________

## Step table

| Step | Time (local, with offset) | Action and who did it | Observed | Captures (path, sha256) | Deviation or limit |
|---|---|---|---|---|---|
| J-1 | | | | | |
| J-2 | | | | | |
| J-3 | | | | | |
| J-4 | | | | | |
| J-5 | | | | | |
| J-6 | | | | | |
| J-7 | | | | | |
| J-8 | | | | | |
| J-8R | | | | | |
| J-9 | | | | | |
| J-9R | | | | | |

## Close

- Steps not reached and why: __________
- Examiner statement that rows were written during the run, not reconstructed: __________

The statement above is blank; generation does not attest contemporaneous recording.
A row records what the person did, never an act on their behalf. Cite acts by their own records (EXP-R5).
When a real record is assigned, place its completed form at forms/<record_id>-N1.md beside records,
cite native_route.form_ref and digest the actual completed bytes in the record evidence.

## Case-definition guidance — expected, not observed

### J-1

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-03/NATIVE_PLANS_TOOLS_DELEGATION.md#NV-01, DEL-01-03/NATIVE_PLANS_TOOLS_DELEGATION.md#NV-02, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-01
- From an empty project folder, plan with the agent and revise the plan
- Plan revisions (plan items if plan mode is on, K-5 of pass 3)

### J-2

Counts in scenario: true
Stimuli: ST-4
Supplier cases: DEL-01-03/NATIVE_PLANS_TOOLS_DELEGATION.md#NV-03, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-01, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-10, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-03
- Execute with substantive real tool use in an ordinary conversation; the agent also delegates one bounded sub-task (ST-4)
- Tool outcomes as Codex reports them; request cards; the delegated child

### J-3

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-02, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-08, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-14
- Turn the work into a workflow draft
- Draft listed with content identity; hygiene

### J-4

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-09
- Try the draft in a conversation (not a run, K-7)
- No run record; draft not selectable for a run

### J-5

Counts in scenario: true
Stimuli: ST-2
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-03, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-05, DEL-02-01/WORKFLOW_DECLARATION.md#VC-13
- Review the draft; the same-name entry placed in another origin (ST-2) is present
- Declared inputs, tools, checkpoints, outputs, evidence; the other-origin notice (WR SP-5); nothing overwritten

### J-6

Counts in scenario: true
Stimuli: ST-3
Supplier cases: DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-08, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-13, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-07, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-03, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-16, DEL-04-03/RECORD_SEMANTICS.md#VC-37, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-12, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-05
- **The person registers it** at the act control (A15), after the unperformed-act negatives (ST-3)
- Direct-capture record, actor ≠ recorder, bound bytes; no A15 from silence, timeout, the agent's claim or tool success

### J-7

Counts in scenario: true
Stimuli: ST-2
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-06, DEL-02-03/EXECUTION_COMPATIBILITY.md#VC-E-18, DEL-04-03/RECORD_SEMANTICS.md#VC-40
- Select the registered revision (an unqualified name offers both origins, ST-2) and run it on new inputs
- Source-qualified identity; no rebinding to the other origin; per-run supply

### J-8

Counts in scenario: true
Stimuli: ST-1, ST-3
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-01, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-12, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-08, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-13, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-03
- Refine (revision 2): draft from base, **try**, review, **register** (ST-3 negatives again)
- Second registered revision; ST-1: J-7's selection and run record still name revision 1, whose bytes are unchanged

### J-8R

Counts in scenario: false
Stimuli: none listed
Supplier cases: DEL-02-03/EXECUTION_COMPATIBILITY.md#VC-E-17
- *(added; not counted)* Run revision 2 on new inputs
- Run record
Scope note: Run of revision 2 on new inputs: WR TT-7 (PROPOSED), not V4-EXM-10's words; recorded, not aggregated

### J-9

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-01, DEL-02-02/WORKSPACE_AND_REGISTRATION.md#WR-VC-12, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-08, DEL-01-04/APP_ACT_CONTROL.md#VC-AAC-13
- Refine again (revision 3): draft, try, review, register
- Third registered revision; exactly two refinements

### J-9R

Counts in scenario: false
Stimuli: none listed
Supplier cases: DEL-02-03/EXECUTION_COMPATIBILITY.md#VC-E-17
- *(added; not counted)* Run revision 3
- Run record
Scope note: Run of revision 3: WR TT-7 (PROPOSED); recorded, not aggregated

Full stimuli, prerequisites and missing inputs remain in the source-bound preparation.
This blank-form check cannot validate a completed form or establish N-1 execution, admission, qualification or acceptance.

## Exact input preparation attachment

PREPARATION ONLY. This attachment is not an EXP result binding or an observation.
The candidate slot remains unassigned. All original form fields remain blank.
No examination, workflow installation, collision registration, trial, review or A15 occurred.
J-1 starts in an empty project. These are examiner examples for later drafting;
they do not replace the person’s plan or later native work. Changed actual drafts need fresh exact binding.

Exact selection SHA-256: a07350bc32b6deb0c6f91d2c479496218241be9cdb3df5b172733d2b1e1db134
Exact plan-file SHA-256: 899cdf6b2549d53fbd43585b2781b2e8c772a080d94af0b33aaf4756a0789434
Source-pins SHA-256: e12b994ce886c7fae13fd162a68a841e7875a51692a494f889ffb4b30d87f9d0
Preparation wrapper pins SHA-256: 5909d3b3b3eb73b41168b927f96a163f58d0b7eb0a2d0bb565f5d43dad849daa
Selected support method: EXP-SUPPORT-BINDING-v1
Selected support declaration SHA-256: c5937e66510f51aece2f51e56a9a22d179e4288e7f765472d27be62471e6c248
EXP version: EXP-v0.2
EXP prototype SHA-256: f7e11fc7cd9dd3126ccbe49db907c2feb69612dd185b56cc0d21560119d71210
EXP result schema ID: urn:chirality:app-v4:del-09-01:exam-result-record:0.2
EXP review schema ID: urn:chirality:app-v4:del-09-01:exam-review-record:0.2
EXP change schema ID: urn:chirality:app-v4:del-09-01:exam-change-impact:0.2

Selected support is source correspondence only; producer use and result-consumer adoption are unverified.
All existing missing inputs remain in the exact plan and selection.

| Maintained fixture role | Repository-relative source | SHA-256 |
|---|---|---|
| revision_1_workflow | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-1/invented-pipe-inventory/WORKFLOW.md | 4e80c92e011d47ac5ebd0514266701aa6e697e2ab2d4c76f9a4a86cbd1ef3fb1 |
| revision_1_tool | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-1/invented-pipe-inventory/tally.py | 030d9e5f4ce80a77d977cdee978395221ace984b47fd59d47295d3ee4cb43897 |
| revision_2_workflow | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-2/invented-pipe-inventory/WORKFLOW.md | e6f63268b22d7f3b2ef2ee6f12cdc1e0b5d7114ac8710b686564b8d0870de9d8 |
| revision_2_tool | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-2/invented-pipe-inventory/tally.py | 41cc47e00889f31b1afb7f3891d94271511a6ec3d5098bb176e17854a5a3ef1e |
| revision_3_workflow | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-3/invented-pipe-inventory/WORKFLOW.md | 4a559bd1bc5e5427435f51d6cd3f448dcf2e6c96bba94c08ff55691f41e5eccf |
| revision_3_tool | projects/chirality-app-v4/app/examination/standalone/fixtures/revision-3/invented-pipe-inventory/tally.py | 57a83df469eec4b4fcf5add1221f2ea64a21313a22f76ea1f227e38b504c153c |
| collision_workflow | projects/chirality-app-v4/app/examination/standalone/fixtures/user-collision/invented-pipe-inventory/WORKFLOW.md | d4f16033331b16d00285829d80ff7f7b785a33e46917a229c8dda68e8276ac3c |
| collision_tool | projects/chirality-app-v4/app/examination/standalone/fixtures/user-collision/invented-pipe-inventory/tally.py | e81b36590fc6f438b838319711c44f4858d71591f6dbe7a094168c9b9151573e |
| initial_input | projects/chirality-app-v4/app/examination/standalone/fixtures/inputs/initial.csv | 0fbee944c7bfb763f440e712eff28853da19cc34e171c2450d3d147848e0b844 |
| reuse_input | projects/chirality-app-v4/app/examination/standalone/fixtures/inputs/reuse.csv | c45cf5efb99246bca123405992e1ad17c7509d38c9343885ad4ba6cec7c7081b |
| refinement_2_input | projects/chirality-app-v4/app/examination/standalone/fixtures/inputs/refinement-2.csv | 75dfe90d012a77897a88340912fdc968c2dc9e692a15c9730341a6d55974bdbd |
| refinement_3_input | projects/chirality-app-v4/app/examination/standalone/fixtures/inputs/refinement-3.csv | b0f887268f401cffab28dc80cf2d0ec641aa3ad5d97af6fcc6651126a1bca086 |
| duplicate_negative_input | projects/chirality-app-v4/app/examination/standalone/fixtures/inputs/duplicate-negative.csv | 91b77746e5172194ae79af9b9db9a20d800775cd31bd9d1f442e49fca35ce8ec |

Fixture hashes identify unregistered invented material, not selected runnable revisions or installed origins.
A passing blank check proves preparation fidelity only; completed/edited forms refuse this check.
