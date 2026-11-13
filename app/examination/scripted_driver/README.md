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

**State:** step one (the hosted proof) is in progress. Hosted runs made: 0 of
2. The scenario has not been started. This section is updated with each
hosted run, and says when the stop point is reached or both results are shown.

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
- `caffeinate -di`.

It then reads what the build wrote. The build writes one line per stage as it
happens, so a run that stops says where:

1. process started;
2. page load started;
3. page load finished;
4. script evaluated.

The script reads the page title, the first heading, the number of buttons and
any open in-page dialog. It clicks, types and changes nothing. The build then
ends its own process. **Shown** means all of these:

- the script ran;
- the heading is "Welcome to Chirality";
- the App has one window;
- no in-page dialog is open;
- the build ended itself with status 0.

The job is `.github/workflows/app-scripted-driver.yml`. It runs on the macOS
runner the App's workflow already uses, reads the repository only, and
uploads the report and nothing else.

## What it does not establish

Every report states these limits:

- It is development evidence about a test build. It satisfies nothing in
  release criteria 1 and 2, is not an operator's or a person's observation,
  and does not replace the owner's own use.
- A script inside the page sees the page only. Native sheets, alerts, the
  window's own buttons and the menu bar are unseen, and there is no second
  reading through the accessibility tree.
