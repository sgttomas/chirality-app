# N-1 blank native-step form — V4-EXM-11

PREPARATION ONLY. No examination opened, record assigned, run attempted or observation recorded.
Blank fields are unobserved/unsupplied, not assertions of absence or not-applicability.

Preparation SHA-256 (canonical JSON): 3c1e16dab343aaf1d36f402a365b865a0e590365ec077201bb84e43c80969e40
Case: V4-EXM-11
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
| S11-1 | | | | | |
| S11-2 | | | | | |
| S11-3 | | | | | |
| S11-4 | | | | | |
| S11-5 | | | | | |
| S11-6 | | | | | |

## Close

- Steps not reached and why: __________
- Examiner statement that rows were written during the run, not reconstructed: __________

The statement above is blank; generation does not attest contemporaneous recording.
A row records what the person did, never an act on their behalf. Cite acts by their own records (EXP-R5).
When a real record is assigned, place its completed form at forms/<record_id>-N1.md beside records,
cite native_route.form_ref and digest the actual completed bytes in the record evidence.

## Case-definition guidance — expected, not observed

### S11-1

Counts in scenario: true
Stimuli: ST-4
Supplier cases: DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-02, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-10, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14
- During J-2's tool-heavy turn, with the delegated child active (ST-4)
- The person stops the turn
- Turn ends interrupted (NIR-v0.3 TO-4, including a turn carrying `Turn.error` at 0.160.0); nothing shown done that was not observed; the child observed active is reported, not marked done

### S11-2

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-01, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-05, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14
- During J-7's run, with a tool-permission request waiting
- Close the window; reopen
- Work continued; the request is still listed; closing an observer is not stopping work

### S11-3

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-04, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-03, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14
- J-7, first request
- **Deny** it on its card
- Denial settled with its origin; not a human act

### S11-4

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-03, DEL-02-01/WORKFLOW_DECLARATION.md#VC-28, DEL-01-03/NATIVE_PLANS_TOOLS_DELEGATION.md#NV-07, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14
- J-7, a later request
- **Grant** it
- Grant settled; tool success is not an act

### S11-5

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-06, DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-11, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14
- During J-8's try conversation, while the agent's turn is live and a tool-permission request waits
- Quit the App (confirming the question); relaunch
- Quit question lists live work; relaunch reads *quit-with-live-work*; the waiting request rebuilt as interrupted by quit

### S11-6

Counts in scenario: true
Stimuli: ST-4, ST-5
Supplier cases: DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-04, DEL-01-03/NATIVE_PLANS_TOOLS_DELEGATION.md#NV-04, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-14, DEL-01-01/HOSTING_BOUNDARY.md#X-09, DEL-01-01/HOSTING_BOUNDARY.md#X-10
- After relaunch
- Continue **J-8's try conversation** (the one live at quit), then carry J-8 to registration
- Provider vs rendered state; primary-turn completion vs the child still active (ST-4); settlement vs received acknowledgment (ST-5); unknown stays unknown

Full stimuli, prerequisites and missing inputs remain in the source-bound preparation.
This blank-form check cannot validate a completed form or establish N-1 execution, admission, qualification or acceptance.
