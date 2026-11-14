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

The second regression run, 43528759059 on 13 November 2026, failed in the
proof step and passed the scenario. At its second try the proof's script read
the first heading as "Chirality", with 52 buttons: the App had not yet had its
first host read, so the page still showed the workspace, and the script then
stopped at the first heading present. That was a false fail. A wrong heading
could not make it pass, the scenario passed in the same run, and the counted
pass stands. Since then the proof waits for the expected heading itself
("The hosted proof", above).

**The further approval: the setup scenario.** The Inter-Project Agent 0
decided it under the owner's instruction of 13 November 2026 at 21:46 UTC,
and App Agent 0 took it up. It is recorded as that agent's decision, not
the owner's own word (`AGENTS.md`, "Continuing boundaries"). It covers a
second scripted-driver scenario on a hosted runner, in a test build with a
throwaway home and no credential. The scenario types a project path, confirms
setup through a test-build stand-in for the App's native confirmation, and
reads the state the next launch reaches. Two built attempts are allowed to
reach its pass. It is development evidence only and satisfies nothing in
criteria 1 and 2. Its conditions:

- the stand-in is for desktop setup's confirmation and no other; needing a
  second one stops the work;
- it records the sheet's exact words, and the scenario judges them;
- both answers are run, each with its own inventory;
- it is compiled only with the driver's flag, and release-free proves it
  absent from the release-features build on every run;
- every use of the result says the native confirmation was not exercised;
- no build carrying the flag is ever the candidate for the operator
  rehearsal, the owner's sign-in or the owner's sitting.

State: built attempts 0 of 2.

## How it is kept out of the shipped App

- **A cfg, not a feature.** `build.rs` compiles this crate alone with cfg
  `chirality_scripted_driver` when `CHIRALITY_SCRIPTED_DRIVER_BUILD` is exactly
  `1`. `Cargo.toml`, the lockfiles, `package.json` and the Tauri configuration
  are unchanged, so no packaging-notice input changes.
- **Refused with the release feature.** `build.rs` refuses the variable
  together with the release feature `distribution-successor` or with any
  publisher selection. `src/scripted_driver.rs` also carries a
  `compile_error!` for the same pairing.
- **Checked by a run.** `proof.py release-free` requires five things:
  - the marker string is present in the test binary;
  - the setup stand-in's own marker is present in the test binary;
  - both markers are absent from a build of the same revision with the
    release features;
  - the driver is refused with the release feature.

  A part that did not run is a failure.
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
any open in-page dialog. It clicks, types and changes nothing. It is read
again every half second, at most sixty times, until the first heading is the
expected one, "Welcome to Chirality". What the page shows before that depends
on when the App's first host read arrives: until it does, the page has shown
the workspace, whose own heading is "Chirality" (run 43528759059, below), and
it may show another heading or none. So the build waits for the expected
heading itself, never for whichever heading comes first. If it never comes,
the build ends itself with status 5 after the last try, and the report's
`heading_wait` says how many tries were made, every distinct heading read in
order, and the last: a wrong page and a slow one read differently. The build
then ends its own process. **Shown** means all of these:

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
the expected one (as above), the build evaluates `judge.js` and `page.js` in the page, and reads
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

## The setup scenario

`proof.py setup` runs `setup-complete.scenario.json` in the same test build:
three launches in one throwaway home on the runner. The runner makes an empty
project folder inside that home, and the system frameworks are pointed at the
home too.

1. **L1.** The project path is typed into "Project folder", setup is
   reviewed, and "Create settings and save for next launch…" is pressed. The
   stand-in answers "Leave setup unchanged", and the page must say nothing was
   saved.
2. **L2.** The same steps, answered with the create button. The page must say
   "You're set up", with the project.
3. **L3.** A relaunch. These are judged from visible elements: no welcome,
   the workspace heading, and the connection line saying whether Codex
   started. These come apart, from the App's state as the page's own status
   read gives it, and no person-visible element is judged for them: that
   setup is no longer required, the project, the launch state and Codex's
   state.

Every launch keeps every guard the first scenario has: the census, one window
and one web view, one process start, the exit status and the marker. Two
differences:

- On L3 the processes whose executable is the bundle's own Codex, by file
  identity, are allowed and recorded, with the network connections they held
  at each census as a fact. Anything else below the App or in its group still
  fails. What the App leaves in its group after it ends is seen too, and
  ended.
- After each launch, the inventory lists every name under the home without
  opening anything. It judges three things:
  - the saved request and the account homes, as the scenario says for that
    launch;
  - on L3, the account home's sign-in file absent by name;
  - nothing outside the App data folder, the project and the system's own
    folders named for this bundle.

**The stand-in.** In this test build only, `desktop_setup_prepare` answers
desktop setup's confirmation through `scripted_driver::setup_confirmation_stand_in`
instead of the native sheet. The stand-in records the sheet's title,
statement and buttons as a stage, and returns the scenario's answer for that
launch. With no answer left it answers nothing and refuses, so nothing is
saved. It is the only confirmation with a stand-in; the driver test pins
that. **The App's native confirmation is not exercised by this scenario.**
The real sheet is exercised by the operator rehearsal and by the owner. This
is not an examination of a shipped control under DEL-09-02's REQ-009, and
nothing it shows counts as one.

**Typing** sets the field's value as a script does and fires the page's
input event. It is not input from the system.

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
