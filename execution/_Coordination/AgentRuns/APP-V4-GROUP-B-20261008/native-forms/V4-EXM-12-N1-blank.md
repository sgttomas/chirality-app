# N-1 blank native-step form — V4-EXM-12

PREPARATION ONLY. No examination opened, record assigned, run attempted or observation recorded.
Blank fields are unobserved/unsupplied, not assertions of absence or not-applicability.

Preparation SHA-256 (canonical JSON): 3c1e16dab343aaf1d36f402a365b865a0e590365ec077201bb84e43c80969e40
Case: V4-EXM-12
Planned run label: RUN-B
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
| M12-1 | | | | | |
| M12-2 | | | | | |
| M12-3 | | | | | |
| M12-4 | | | | | |
| M12-5 | | | | | |
| M12-6 | | | | | |

## Close

- Steps not reached and why: __________
- Examiner statement that rows were written during the run, not reconstructed: __________

The statement above is blank; generation does not attest contemporaneous recording.
A row records what the person did, never an act on their behalf. Cite acts by their own records (EXP-R5).
When a real record is assigned, place its completed form at forms/<record_id>-N1.md beside records,
cite native_route.form_ref and digest the actual completed bytes in the record evidence.

## Case-definition guidance — expected, not observed

### M12-1

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A01
- **The person signs in** with ChatGPT in the App-owned home H-acct
- Sign-in completes; account reported; no credential in App records

### M12-2

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A02, DEL-01-02/EXECUTION_AND_RECOVERY.md#VC-R-15
- **The person enters an API key**; the App uses home H-key (L-1)
- Key held by Codex in H-key; two homes, one process each

### M12-3

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A03
- Configure an identified local model server
- Provider requested = reported; endpoint and model identity recorded

### M12-4

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-04/NATIVE_INTERACTION_RECEIVING.md#VC-NIR-12, DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A12
- Open a new conversation
- "No model selected" until the person chooses (DEC-4; no default)

### M12-5

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A04
- One conversation with each mode; switch between them
- Each starts; the other two stay configured and selectable

### M12-6

Counts in scenario: true
Stimuli: none listed
Supplier cases: DEL-01-05/ACCOUNT_AND_PROVIDER_ACCESS.md#VC-A13
- Inspect records and logs
- No credential anywhere (custody scan)

Full stimuli, prerequisites and missing inputs remain in the source-bound preparation.
This blank-form check cannot validate a completed form or establish N-1 execution, admission, qualification or acceptance.
