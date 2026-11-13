# Operating a development build's window

This is how an agent reads and clicks the window of an identified development
build of the App during an examination. It uses the supplier's own computer-use
service, reached from inside a Codex session.

It is development tooling. What it yields is what an agent saw and did in a
development build. It is never evidence that the product does something for a
person, and it is never the person-operated observation a release criterion
asks for.

## When it may be used

All of these hold, every time:

- The owner has given a window of time for it, and the acts used are the ones
  the owner's word for that window names (a view; a click; anything further,
  such as typing, a native file dialog or the App's own quit, only if named).
- One operator at a time: a Codex delegate whose assignment carries these
  terms. No other agent imports the service or calls any of its methods.
- Only the App's development build, addressed by its own bundle identifier.
  Never the installed application, never another application.
- No agent answers a macOS prompt or an App confirmation dialog, types a
  password or dismisses the lock screen. If one appears, the operator stops and
  reports its application name and the permission it asks for; the owner
  answers it.
- No Codex is started unless launches that start a real Codex are open for the
  lane.

## Two cautions

1. **Launch through the launcher, and confirm the process is running, before
   any state call.** A state call for an application that is not running
   starts it through the system's launch service: outside the launcher, with
   the account's real home.
2. **Address the build by its bundle identifier in every call, and never call
   `list_apps`.** An application name can match another application.

## The steps

1. **Launch.** From the root of a clean checkout of main, with a new, empty
   evidence folder of your own outside every checkout, start the launcher on
   the identified candidate so that it outlives the shell call that starts it
   (an agent's shell ends what it started when a call returns, so `&` is not
   enough):

   ```sh
   python3 -B app/examination/standalone/operated/detached.py <evidence folder> launcher -- \
     python3 -B app/examination/standalone/launch.py launch --candidate <candidate folder>
   ```

   It prints the launcher's process number and returns, and writes
   `launcher.started.json` in the evidence folder with that number and the
   command. It starts exactly the command given, with no shell reading it,
   and does not watch or end it. The launcher's first
   line, in `<evidence folder>/launcher.err`, names the launch folder; the home
   is `home/` in it and the project folder is `project/`. The launcher stays
   until the App ends, then publishes the launch record in `record/` and
   prints the outcome into `<evidence folder>/launcher.out`. If it refuses,
   `launcher.out` or `launcher.err` says so within seconds and no App is
   running: that refusal is the result. Record it and stop.
2. **Confirm.** The App is the launcher's one child process:

   ```sh
   pgrep -P <the launcher's process number>     # the App's process number
   ps -o comm= -p <the App's process number>    # its executable: inside the candidate's bundle
   pgrep -P <the App's process number>          # its child processes: prints nothing
   ```

   If the first prints nothing, or the executable is not inside the candidate
   folder, stop: nothing is to be viewed.
3. **The identifier.** Take it from the candidate's identification record,
   not from a name on screen:

   ```sh
   python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['bundle']['identifier'])" \
     <candidate folder>/identification/candidate-identification.json
   ```
4. **The service.** In the operator's Codex session, in the node runtime's
   `js` tool:

   ```js
   var sky = (await import('@oai/sky')).sky;
   ```

   It must be this dynamic import inside that tool. This step touches nothing
   on the desktop.
5. **A view.**

   ```js
   var state = await sky.get_app_state({app: '<bundle identifier>', disableDiff: true});
   ```

   The result gives the application's path, a reference to a screenshot, and
   the window as text: one line for each element, with its index, its kind
   (button, text, radio button, heading and so on) and its words or value;
   indentation shows what contains what. A disabled control says so. Without
   `disableDiff`, a later view returns only what changed since the one before.
6. **A click.**

   ```js
   await sky.click({app: '<bundle identifier>', element_index: N});
   ```

   `N` is the element's index in the most recent view. Take a view after every
   click: indices change. Click only a control whose effect is known from its
   words and is among the acts the window allows; if it is not, take a view and
   stop there.
7. **Record.** Keep every call as it was sent and every returned text whole,
   with the time of each. What a step shows is the text a view returned, in the
   page's own words; nothing is claimed beyond it. Words on the page about a
   dialog are page text, not a dialog.
8. **End.** When the App's own quit is not among the allowed acts, send a
   termination to the launcher; it passes it to the App:

   ```sh
   kill -TERM <the launcher's process number>
   ```

   Wait until `<evidence folder>/launcher.out` holds the outcome (about fifteen
   seconds), then confirm that neither process remains (`ps -p` on each
   number prints no process). The launch record then says a termination was
   passed to the App, and the outcome is "failed": that is the truthful record
   of a launch ended from outside, not a defect.
9. **What stays.** The launch folder with its record, and the evidence
   folder. Nobody opens the home.
10. **Nothing is left running.** The operator ends what it started: the
    launcher as in step 8, which ends the App, and the watch, which ends by
    itself when the App does and is otherwise ended by its process number
    (`kill <the watch's process number>`). It then confirms, for the launcher,
    the watch and the App, that `ps -p <number>` shows no process, and that
    the App's process group is gone (`pgrep -g <the App's process number>`
    prints nothing).
    The lane's agent, not the operator, then confirms the same from its own
    shell after every run, from the process numbers in the evidence folder's
    `*.started.json` files. If an operator ends half-way, those files are how
    what it left is found: the lane's agent ends the launcher with a
    termination, as in step 8, ends the watch by its number, confirms all
    three are gone, and records that it did so and why. A launch left without
    its operator is ended, not continued by someone else.

## Running a scenario

A scenario is a file of steps and expected states, walked by a script the
operator loads. There is one: `first-use-setup.scenario.json`, "first-use setup
without a project, new settings". It is the opening of the first-use setup page
up to, and not including, the App's own confirmation. Its acts are views and
clicks; nothing is typed, no file or folder is chosen and no confirmation is
answered. It starts no Codex and needs no sign-in.

What it shows when it passes:

- **SETUP CHOICES REVIEWED.** After "Continue without a project" the page reads
  "Ready to review. Nothing is created or saved until you confirm."; "Review
  setup" shows "What setup will do" with its five lines and the control
  "Create settings and save for next launch…", which is never clicked; "Exact
  locations" shows three locations under the App's data folder in the throwaway
  home.
- **Two refusals.** "Review setup" is unavailable, with its reason, before any
  choice; and again with "Use my existing Codex settings" selected and nothing
  chosen.
- **The starting state.** "Technical details" says setup is required and gives
  the App's data folder under the throwaway home.

It is agent-operated development evidence on a development build. It is neither
setup completed nor a person's observation.

**Before a window: the same walk on recorded views.** No application and no
screen are involved.

```sh
cd app/examination/standalone/operated
node replay.mjs first-use-setup.scenario.json ../../../tests/group_b_operated_fixtures/first-use-setup/views.json
node replay.mjs first-use-setup.scenario.json ../../../tests/group_b_operated_fixtures/first-use-setup/views.json \
  ../../../tests/group_b_operated_fixtures/first-use-setup/wrong.review-available-before-any-choice.json
```

The first prints PASS with every outcome shown and exits 0. The second makes one
known wrong state in the recorded views (Review setup available before any
choice) and must print FAIL, naming the step and what was found, and exit 1.
The other `wrong.*.json` files beside it do the same for three more states.
This is the check rejecting a wrong state; it says nothing about a build.

**In a window.** Steps 1 to 3 above first: the launcher running, the App's
process number confirmed, the identifier taken from the identification record.
Then start the watch, in the same way as the launcher. It keeps a small file
saying whether that process is running and what child processes it has, which
the script reads because the node runtime cannot ask the system itself:

```sh
python3 -B app/examination/standalone/operated/detached.py <evidence folder> watch -- \
  python3 -B app/examination/standalone/operated/watch.py <the App's process number> <evidence folder>/watch.json
```

The watch ends by itself when the App does.

Then, in the operator's `js` tool, with the values filled in:

```js
var fs = await import('node:fs');
var walk = await import('file://<repository>/app/examination/standalone/operated/walk.mjs');
var scenario = JSON.parse(fs.readFileSync('<repository>/app/examination/standalone/operated/first-use-setup.scenario.json', 'utf8'));
var sky = (await import('@oai/sky')).sky;
var report = await walk.run({sky, scenario, app: '<bundle identifier>', home: '<launch folder>/home',
  pid: <the App's process number>, watch: '<evidence folder>/watch.json'});
fs.writeFileSync('<evidence folder>/scenario-result.json', JSON.stringify(report, null, 2));
nodeRepl.write(walk.summary(report));
```

- The loading forms above were tried in a Codex session's node runtime with a
  stand-in for the service: the file imports work, bindings last from one call
  to the next, and `process` does not exist there, which is why the watch file
  does.
- The script refuses, before any call, an application not named by a
  development build's bundle identifier, and a process the watch file does not
  show running within the last five seconds. It makes views and clicks and
  nothing else, and clicks only the controls the scenario's steps name.
- It stops, and says where, if a view holds a sheet, a dialog or an alert, if
  the view is not of the App's own window, or if the watch file stops showing
  the build running. A result that stopped this way is inconclusive, not a
  pass: report it as it is.
- This scenario starts no process. If the watch file shows the App with a
  child process, the script stops and the result is a failure.
- A watch file that is missing, cannot be read, is for another process, says
  the process has gone, or was last written more than five seconds ago is read
  as the build not running: the script refuses before any call, or stops
  between steps. It is never read as "no child process"; a step whose watch
  file could not be used records its child processes as not known.
- `nodeRepl.write` joins what successive calls write without a separator, so
  write the summary once.
- The result file holds every call made and every view's returned text whole.
  The operator adds the times of its own calls and what it saw outside the
  script (a prompt, the pointer or the focus moving) to its own record.
- Then step 8: end the launch, confirm that neither process remains, and keep
  the launch record with the result.

## What the calls take

Read in the supplier's own documentation of its window service, and given here
only as far as the steps need it:

- A view takes the application and, optionally, the request for the whole
  window as text on every call.
- A click takes the application and the index of an element from the latest
  view.
- The service also has methods that type, set a field's value, press keys,
  scroll, drag, paste and list applications. None is used unless the owner's
  word for the window names the act, and `list_apps` is never used.

## What was observed on 13 November 2026

On a development candidate built from main, in two windows the owner gave:

- The import in step 4 returned the service with its methods.
- No computer-use service was running beforehand. The first view started one,
  through the system's launch service; the supplier's desktop application was
  not running.
- No call reported a macOS prompt.
- A view returned within seconds, with the first-use setup page as about fifty
  elements. Later views, made without `disableDiff`, returned differences.
- Clicks by index worked on a disclosure, a button and a radio button.
- Not yet observed: `disableDiff`; any method other than a view and a click.
- The launcher on main at that time could not launch on that host, because
  macOS refused a listing of two Library folders it watched. The launches were
  made with those two names removed; the launcher's own change followed.
