# Retained-state B: native window exists, AX readiness failed

The single live retained-state/v1 attempt in
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-am98hzma` **FAILED**
AX readiness. It supplied a new fact: the owned main window existed on-screen
at the diagnostic instant, while the owned AX window references resolved to
the Application. It did not supply an initialized generation, LT23, supplier
settlement or joined V4-EXM-10/11/12 qualification.

The [archive](../Evidence/EXP/fdcf608fb5-23c6c3f22f5e/native-B-20261031T120630Z/archive-index.json)
maps 46 original files and hashes, including both invocation stages, the
source-bound inputs, diagnostic, cleanup and an offline CF fixture. All
originals remain retained. Archived Python/C sources are inert `.txt` evidence.
The index declares lossless gzip where used; decoded originals and archive
representations were independently hashed by the manager. `SHA256SUMS` covers
all archive files except itself. No opaque supplier-file content was archived.

## Identity and admission

App candidate remains `fdcf608fb5-23c6c3f22f5e`, built from
`fdcf608fb57c4f8299c7440ffc56519314046cff`, unsigned/unqualified development.
The controller source is integrated PR47 `684e046a`, tree equal to checked
`21bbb8a9`. This does not relabel the App to that source. Exact admission:
`2ab2e22b856fb4f43c5a347baa5481f8e005ac7a5c229da2553d42370715d1c1`;
retained-state basis:
`e67384fd18cb311c9da01912cd68c08e83edb4af39ff5a2ccf41e105c56a04bb`.
Saved A request, three-row typed ledger, absence of App ledger sidecars,
current namespace/supplier metadata and source/policy gates passed. The full
bundle inventory then passed without missing/extra/changed entries before
launch. No model, credentials, sign-in, network allowance, permission change,
state reset or candidate rebuild occurred.

The first invocation (execution35510) set its end before waiting for a slot.
It waited from 11:56:44Z until 12:00:32Z, then refused `invalid B interval`:
only about67 seconds remained to 12:01:39.748340Z, below the required90.
It returned1 without artifact-check/execution-start/actions or App launch;
that was a **prelaunch refusal**, not a native B failure or pass.

Parent separately authorized one re-armed invocation. A minimal recorded shim
checked its actual `t3_slot_run.sh` parent after slot acquisition, wrote its
295-second interval and exact argv/environment references exclusively, and
`execve`d the unchanged controller. The PID/parent relationship was preserved.
Two harmless mocked fixtures checked acquisition-time calculation (queue time
excluded), exact exec argv, and used-record/wrong-parent refusal. No deadline
was extended later. The old invocation/output/refusal hashes remained unchanged.

The acquired slot started at 12:06:28.755538Z; fixed end12:11:23.755538Z.
The original App Child started at 12:06:30.300212Z. Its initial AXWindows was
empty, then an Application self-reference. Readiness failed at
12:06:45.552254Z after the reviewed diagnostic; normal cleanup also could not
bind a source at 12:07:00.552896Z. No native Stop or controller Quit was sent.

## Observed WindowServer and AX distinction

The one read-only diagnostic ran 12:06:45.320292–12:06:45.551314Z. Before/after
original-Child WNOWAIT and kernel PID/parent/UID/birth/executable/hash checks
matched. WindowServer enumerated all rows but decoded/retained only this
verified owner's rows. Screen-capture access preflight returned true; no
permission request, screenshot or foreign-window content was retained.

The owned main-window row had layer0, bounds1100×800 at(106,32), on-screen true,
and title `Chirality App v4 — walking skeleton`. A second owned500×500 row
had empty title and absent on-screen value; its purpose is unestablished.
The main-window fact is sufficient to rule out “no native window existed” at
this instant; it does not establish rendered content or functional readiness.

Raw AXWindows, AXMainWindow and AXFocusedWindow each returned success0 with
CFArray/AXUIElement types as appropriate. Each returned element had the owned
PID, CFEqual-to-Application true and AXRole `AXApplication` (also success0).
AXChildren returned that self-reference plus an owned AXMenuBar. This is a
successful but unsuitable AX representation, not an observed API-disabled or
permission-denied error. The cause is not established by the discrepancy alone.

The diagnostic had an8-second inter-call deadline, per-element0.5-second AX
messaging timeouts, bounded nonrecursive references and no native UI actions.
WindowServer calls had no cancellation guarantee, and before/after identity
checks do not create an atomic snapshot. Actual completion was well inside the
budget. No further window-existence retry was performed or is justified here.

## Pre-authorized cleanup and resource closure

The delivered disposition already authorized one source/reservation/executable-
bound owned-menu Quit when ordinary same-source cleanup could not bind a
generation. The corrected bounded helper first recorded own-window and child-
path facts, then searched only the exact App menu, pruning cycles and non-menu
boundaries and treating menu items as leaves. The direct supplier path check
matched the bundled Codex executable; census is corroboration, not custody.

One enabled App-menu Quit AXPress returned0 at12:07:21.742579Z. No question
was confirmed; no claim is made of continuously observing transient questions.
The keeper then observed its original Child as CLD_EXITED/status0 and offered
the exact admission-bound administrative request. The agent, under the parent's
already-delivered selection, created that body as a private owned single-link
0600 file and atomically placed it once. No replacement/retry or numeric signal
occurred, and no frozen controller/dependency was modified.

The keeper's administrative result at12:07:56.785157Z records original-Child
wait0/reaped, `success:false`, null generation, supplier-settled false, no
post-reap errors and no guard reason. Independent guard/census/resource
observations remained freshly timestamped. Execution4133 and its wrapper
returned1 at12:07:56.810717Z; original refusal files were verified unchanged.
The slot wrapper recorded ENDrc1 for `cargo_job.lock` (slot1), marker
`run.59449` was absent, and the explicitly recorded known PID query returned
no rows. Shared memguard78827 remained running. Resource closure finished
within the fixed295-second interval, without overrun. Manager release notices
were sent to parent and SWB; those are communication statements outside the
archive. Known-process absence does not settle detached/escaped supplier scope.

## Receiving and next boundary

The retained state is now post-third-launch state, not the earlier three-row
admission basis. Do not relabel/reuse that basis or reset data. Original/successor
A, all failed B evidence and every prepared/refused input remain retained.
No further live launch is authorized. The [offline ABI audit](AX_REPRESENTATION_AUDIT.md)
separates supported client checks from unproved App/framework behavior and
identifies a narrow next diagnostic, not a product repair or qualification pass.
DEL01-01/01-02 contracts and DEL09-02 input/acceptance conditions are unchanged.
