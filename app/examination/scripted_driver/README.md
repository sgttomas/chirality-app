# The scripted driver (test build only)

A script, evaluated inside a test build's own web view after its page loads,
reads the App's page and reports what it read. The code that does this is
compiled only into a test build. It is never part of a release build.

## What is approved, and its state

The owner approved one bounded step on 13 November 2026, in these words
(recorded in `AGENTS.md`, "Continuing boundaries"):

> First a hosted run showing a test build can run a trivial script in its
> window on the runner the App already uses. Then the one first-use setup
> scenario end to end. Dropped and reported if the hosted run is not shown
> within two runs, or the scenario does not pass within two built attempts.
> Nothing in the shipped build. Development evidence only: it satisfies
> nothing in criteria 1 and 2 and does not replace your own use. No later
> scenario, chooser, typing or confirmation is covered.

**State:**

- (a) Step one, the hosted proof: **shown on hosted run 1 of 2**, 13 November
  2026, run 43490769105.
- (b) Step two, the scenario end to end: **shown on built attempt 1 of 2**,
  13 November 2026, run 43508391064.

Both results are shown and the approved step is complete. The two built
attempts were attempts to reach the scenario's pass; with a pass shown, later
hosted runs of the scenario are regression runs, not attempts (App Agent 0,
stated before attempt 1's result). The first, run 43520740915 on 13 November
2026, also passed.

## How it is kept out of the shipped App

- **A cfg, not a feature.** `build.rs` compiles this crate alone with cfg
  `chirality_scripted_driver` when `CHIRALITY_SCRIPTED_DRIVER_BUILD` is exactly
  `1`. `Cargo.toml`, the lockfiles, `package.json` and the Tauri configuration
  are unchanged, so no packaging-notice input changes.
- **Refused with the release feature.** `build.rs` refuses the variable
  together with the release feature `distribution-successor` or with any
  publisher selection. `src/scripted_driver.rs` also carries a
  `compile_error!` for the same pairing.
- **Checked by a run.** `proof.py release-free` requires three things: the
  marker string is present in the test binary; it is absent from a build of
  the same revision with the release features; and the driver is refused with
  the release feature. A part that did not run is a failure.
  `app/tests/group_b_scripted_driver_test.py` pins that the cfg is named in no
  manifest or configuration, and that the release route unsets compiler flags.

## The hosted proof (step one)

`proof.py build` makes a debug test bundle with the overlay beside this file.
The overlay sets its own identifier and turns the window's background
throttling off. `proof.py run` launches it once with:

- an environment built from nothing;
- `HOME` a new folder;
- the App as exactly the launched process, held awake by a separate
  `caffeinate -di -w <the App's number>` that is outside the App's tree and
  process group.

It then reads what the build wrote. The build writes one line per stage as it
happens, so a run that stops says where:

1. process started;
2. page load started;
3. page load finished;
4. script evaluated.

The script reads the page title, the first heading, the number of buttons and
any open in-page dialog. It clicks, types and changes nothing. The build then
ends its own process. **Shown** means all of these:

- the script ran, and the heading is "Welcome to Chirality";
- exactly one window and one web view were created, and one window is open;
- no in-page dialog is open;
- the build started once and finished on its main thread (below);
- no other process was seen below the App or in its process group, and
  every census was taken;
- the build ended itself with status 0.

The job is `.github/workflows/app-scripted-driver.yml`. It runs on the macOS
runner the App's workflow already uses and reads the repository only. It
uploads its two reports (`report.json`, `scenario-report.json`) and nothing
else, and saves no cache.

## The scenario (step two)

`proof.py scenario` launches the same test build once more. It puts the
maintained scenario file
(`app/examination/standalone/operated/first-use-setup.scenario.json`,
unchanged) and its values (the identifier, the home and the App data folder
under it) beside the stages, as `scenario.json`. Once the first heading is
present, the build evaluates `judge.js` and `page.js` in the page, and reads
the walk's progress until it is done:

- **`page.js`** walks the steps. For each click it finds the step's one
  control and clicks it with `element.click()`. That is a click by the page's
  own element, not input from the system. It then waits the step's time
  (600 ms when the step names none), and builds the page's model again.
- **`judge.js`** decides each expectation against that model. It is a pure
  function, tested with each of the eight expectation kinds the scenario uses
  shown failing on a wrong state. Its rules are stated at its top: what is
  visible, an element's name, its words, and what one text is.

A pass needs all of these:

- the walk's own verdict is pass;
- exactly one window and one web view were created (below), and one window
  was open at every poll;
- the build started once;
- no other process was seen below the App or in its process group, and
  every census was taken;
- the build ended itself with status 0.

**What is counted, and what is sampled.**

- **Windows and web views:** counted in Tauri's creation notifications, in
  the one process the runner launched, from before its first window. A
  second of either ends the run at once, in that notification. The final
  count, stage and exit are made on the main thread, after any notification
  already queued. A window made outside Tauri (a native sheet, alert or
  dialog) passes through no such notification and is unseen.
- **Other processes:** at each census, about every half second (each census
  is followed by a half-second pause) while the App runs, every process below
  the App and every other member of its process group is recorded. This holds
  in both runs, and none is allowed. A process that starts and ends between
  two censuses, that starts after the last census before the App ends, or
  that leaves the App's process group for another session, is not seen. A
  census that cannot be taken (a listing command that fails, which is never
  read as "no process"), or a run with no census at all, prevents a pass.
- **Process starts:** a run whose stages show the build started more than
  once does not pass.

It types nothing, chooses no file, answers nothing, and never clicks a control
the scenario says is never clicked, or one whose words end with an ellipsis.

**Why "visible only".** During first use the App keeps its whole workspace
mounted and hidden: `App.tsx` renders the first-use page and, beside it, the
workspace inside `<div hidden={setupRequired}>`. That is why step one's
script counted 202 buttons locally and 347 on the runner, against the
handful the first-use page shows. The judge's model holds only rendered
elements. Each scenario report also counts the page's buttons three ways (in
the document, under a hidden element, visible), at the start and at the end.
Why the two totals differ between this Mac and the runner is not
established. On the runner they also differ between runs: attempt 1 counted
347 buttons in the document at the start and the first regression run 202,
with 3 visible in both and 346 in both at the end, so the hidden workspace
can still be mounting when the walk starts. The verdict rests on visible
elements only, so this does not bear on it.

## What it does not establish

Every report states these limits:

- It is development evidence about a test build. It satisfies nothing in
  release criteria 1 and 2, is not an operator's or a person's observation,
  and does not replace the owner's own use.
- A script inside the page sees the page only. Native sheets, alerts, the
  window's own buttons and the menu bar are unseen, and there is no second
  reading through the accessibility tree.
- The scenario is judged against a model of the page built by stated rules,
  not against the supplier's accessibility text. Whether the two readings
  agree is not established.
- Every click is `element.click()` on the page's own element, not input from
  the system.
