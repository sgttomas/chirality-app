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
