# R7 micro-rulings — V5 residuals (applied before the Wave-2 PR)

Integrator: HELP_HUMAN. Input: [V5](reviews/V5.md), candidate `2f42fba02`.
Verdict **MERGE AS DRAFTS**: 0 BLOCKING, 3 MAJOR and 8 MINOR items.

The rulings are applied **in place**, with no version bump. Each file records
them in its latest "Changes from …" table under an R7 ID. R1–R6 stand except
where amended here. No ruling changes a recomputed value in V5 §3.

## R7-1 ADAPTER GC-5 follows R6-1 (V5 MAJOR-1)

In the GC-5 HS-5 bullet, replace "or a kind (b)/(c) run halt other than an A5
constraint" with "or a kind (b)/(c) run halt whose held actions include any
App-side step. A run halt holding only host operations is HS-3, above; GC-3
covers A5." Correct the ADAPTER R6-1 change row to match.

## R7-2 SQ-02 asks about the widened host-held case (V5 MAJOR-2, m-7)

- Add SQ-02 sub-question **(f)**: "When a checkpoint arrives on an observed
  output or host outcome, will your route refuse that run's further host
  operations until the act, on each surface?"
- Rewrite the answer form with options **(i)–(iv)**, so that its labels cannot
  be confused with the question letters (a)–(f). Give (f) its own per-surface
  yes/no slot.
- Add the new case to SQ-02's "Depends" line: ACT `CP-L4`, AS F6d and ADAPTER
  GC-5.

## R7-3 Held actions of A5 and kind (a) checkpoints are derived (V5 MAJOR-3) — INTEGRATION

Option (a) is chosen. When the *held actions* element is absent:

- for an **A5** checkpoint, the held actions are the governed operation(s);
- for a **kind (a)** checkpoint, they are the held call.

The conservative default ("at least one App-side step", HS-5) applies only
when a kind (b)/(c) checkpoint has no held-actions element, or when its
declared held actions do not show host operations only.

**Reason.** EXEC §3.6 already defines held actions this way, and C V-GR1
already values `CP-grant` via X as *not established*. Option (b) would make
every legacy or carried declaration without the element *unsupported* for a
checkpoint whose held set is already fully known. Option (a) creates no hold
claim, because an HS-3 value today is *not established*.

**Files:**

- WD §4.3.1 states the derivation and the scope of the default.
- WD VC-43 and the WD-EX E8 row "L-WDEX-17 with its held-actions element
  absent" become HS-3 → *not established*. The workflow result for that row
  follows EXEC §3.5 precedence with the run's other checkpoints.
- EXEC HS-5 and GUIDE §2.14 echo this.

## R7-4 MINOR items (V5 m-1…m-8)

| # | Change |
|---|---|
| m-2 | RELAY SQ-31 "App assumes meanwhile" and the §3 map: HS-0 → **LH-0**. |
| m-3 | C V-GR1 (last sentence) and RS E7 add "; E1d's `CP-check` is *not enforceable*, so the run via X is *unsupported* (EXEC MT-16)". |
| m-4 | ACT §4.3 lapse bullet, CA S-14 and CA W14-06: qualify "the run stops at its next action" per R6-3. It stops only where the value is *enforced by the host loop*; otherwise the held host operations are refused, or the action is recorded as *action during hold*. |
| m-5 | EXEC §3.6, WD §4.3.8 and ACT §4.6 value tables, and XT F-10: "a constraint carried only as model-supplied" is qualified as "once SQ-02 is answered with no host-held route". |
| m-6 | EXEC U-E23 point of need and GUIDE §2.13 D6 row: "App-side workflow with a kind (b)/(c) run halt" becomes "a checkpoint with any App-side held action". |
| m-8 | EXEC and WD headers record the sibling inputs they read at the R7 working state. |
| m-1 | **Last.** Re-pin GUIDE's input table to the post-R7 sha256 of every other Design file, and refresh CC-11 (G-10 and G-11 closed). GUIDE cannot pin itself. |

## Observation carried (no change)

V5 §6: ACT `CP-L4` and AS F6d are counterparts. Add a one-line cross-reference
in each.
