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

- App Agent 0 has said go for this walk, and the acts used are the ones the
  scenario names and that go allows (a view; a click; anything further, such
  as typing, a native file dialog or the App's own quit, only if both name
  it). Leave for the screen is not asked: the owner, 13 November 2026, "I'm
  AFK, no need to ask for leave. Also that MacBook Pro machine is dedicated
  to this agentic dev session. I do my personal work on other machines. So
  no need to ask permission to use the computer or screen."
- One operator at a time, across this project and the others on this
  machine: a Codex delegate whose assignment carries these terms. App Agent 0
  tells the other projects before a walk starts, and no walk runs during an
  announced exclusive measuring run; so a walk is asked of App Agent 0, never
  started on the lane's own word. No other agent imports the service or
  calls any of its methods.
- Only the App's development build, addressed by its own bundle identifier.
  Never the installed application, never another application.
- No agent answers a macOS prompt, ever, types a password or dismisses the
  lock screen. If one appears, the operator stops and reports its application
  name and the permission it asks for; the owner answers it. An App
  confirmation is operated only where a scenario names it and the governing
  text below allows it; the first-use setup scenario names none.
- No Codex is started unless launches that start a real Codex are open for the
  lane.

## What governs it

Agent-operated examination is governed by the release target's Testing
paragraph (`docs/RELEASE_TARGET_4.0.0.md`) and DEL-09-02's REQ-009, REQ-010,
AC-003 and VER-003 (`execution/PKG-09/DEL-09-02/ScopeOfWork.md`); this method
does not restate them and does not contradict them. In short:

- Solely for synthetic development examination on examination material, the
  examining agent operates every shipped control the named examinations
  need, including those at which the candidate captures an act. Sign-in, key
  entry and criterion 8's keychain acts are the owner's and never an
  agent's. The exception reaches examination material only.
- A synthetic capture needs the App's name set to an examination name and
  verified before every capture and again after every restart; it stays
  within the identified examination material; what is a finding, and that a
  step whose conditions cannot be established is blocked, are as REQ-009
  states; the human-positive cases read as not examined.
- Each step's record says who operated it and by what means, names the
  preparation and observation done outside the controls, and notes where
  completing it needed knowledge the interface did not give (REQ-010; step 7
  below).

A scenario may be narrower than that, and the first-use setup scenario is, on
purpose: no setup confirmed, nothing typed, no Codex started, no macOS prompt
answered (see "Running a scenario"). The governing text does not enlarge the
exception the owner accepted, and App Agent 0 decided, for its live runs.

## Two cautions

1. **Launch through the launcher, and confirm the process is running, before
   any state call.** A state call for an application that is not running
   starts it through the system's launch service: outside the launcher, with
   the account's real home. See "A view of an application that is not
   running" below for what remains of this once a walk is under way.
2. **Address the build by its bundle identifier in every call, and never call
   `list_apps`.** An application name can match another application.

## What the operator is given

- **The Python, written `<python>` in every command below.** A Python 3 that
  has the repository's checking dependencies (jsonschema and PyYAML, as the
  repository checks install them), named by the assignment by its full path.
  Put that path wherever a command here shows `<python>`, including the
  launcher's own command line and both `detached.py` lines, where it appears
  twice. Identification's check and the launcher need jsonschema, and a
  `python3` found on the operator's own path may not have it. On a
  development host the lane names an interpreter that already has both;
  nothing is installed or downloaded for a walk. The operator's first act,
  before anything else, is to confirm it:

  ```sh
  <python> -c "import jsonschema, yaml"
  ```

  It exits 0. If it does not, or the assignment names no interpreter, stop:
  the assignment named the wrong interpreter.
- **The candidate folder.** The operator does not build one. A candidate folder
  is made beforehand by the lane with `app/examination/candidate_identity`:
  `build_candidate.py` builds an unsigned development bundle from a named
  revision into a new folder, and `identify.py record` writes its
  identification record in `identification/` there. The assignment names the
  folder and its candidate key. The operator confirms it is the one meant:

  ```sh
  <python> -B app/examination/candidate_identity/identify.py check \
    --record <candidate folder>/identification/candidate-identification.json \
    --app "$(ls -d <candidate folder>/target/debug/bundle/macos/*.app)"
  ```

  It exits 0 when the bundle is the one the record identifies, and the record's
  `candidate_key` is the key the assignment names. The path the `ls` prints is
  the bundle; it is needed again below. The lane keeps that bundle unchanged
  from identification through recovery: no rebuild, replacement, renaming or
  added link (see "The condition of the exception").
- **The homes root.** The launcher makes each launch folder under the lane's
  homes root, which must already exist; it never creates it. If it does not
  exist the launcher refuses and says so. The lane makes it, once.
- **App Agent 0's go for the walk**, and the acts it allows.

## The steps

1. **Launch.** First confirm that a start of the build by the system's launch
   service would be given none of the App's ten configuration variables (why:
   "A view of an application that is not running", below):

   ```sh
   <python> -B app/examination/standalone/operated/session_env.py "<the bundle>"
   ```

   It asks the login session's launch domain and the bundle's own Info.plist,
   and prints each name with "absent", "present" (empty included) or "could
   not be established" and why; never a value. It exits 0 only when all ten
   are absent. Any other result, "could not be established" included, means
   no walk is made: stop, record what it printed, and the lane tells App
   Agent 0.
   Then, from the root of a clean checkout of main, with a new, empty
   evidence folder of your own outside every checkout, start the launcher on
   the identified candidate so that it outlives the shell call that starts it
   (an agent's shell ends what it started when a call returns, so `&` is not
   enough):

   ```sh
   <python> -B app/examination/standalone/operated/detached.py <evidence folder> launcher -- \
     <python> -B app/examination/standalone/launch.py launch --candidate <candidate folder>
   ```

   It prints the launcher's process number and returns, and writes
   `launcher.started.json` in the evidence folder with that number and the
   command. It starts exactly the command given, with no shell reading it,
   and does not watch or end it. Once the launcher has made the launch
   folder, the first line of `<evidence folder>/launcher.err` names it; the
   home is `home/` in it and the project folder is `project/`. A refusal made
   before that names no folder. The launcher stays
   until the App ends, then publishes the launch record in `record/` and
   prints the outcome into `<evidence folder>/launcher.out`. If it refuses,
   `launcher.out` or `launcher.err` says so within seconds and no App is
   running: that refusal is the result. Record it and stop. If the starter
   itself exits 3, it could not write its record: it has tried to end the
   launcher and says in `command_gone` whether the launcher is gone, and it
   cannot say what the launcher had started. Record what it printed, stop,
   and tell the lane at once; the lane makes step 11.
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
   <python> -c "import json,sys; print(json.load(open(sys.argv[1]))['bundle']['identifier'])" \
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
   words and is among the acts the scenario names and the go allows; if it is not, take a view and
   stop there.
7. **Record.** Keep every call as it was sent and every returned text whole,
   with the time of each. What a step shows is the text a view returned, in the
   page's own words; nothing is claimed beyond it. Words on the page about a
   dialog are page text, not a dialog. The operator's record also says, for
   the run and for any step that differs (REQ-010): who operated it (the
   operator, an agent, by its model) and by what means (the supplier's
   computer-use service, views and clicks by element index, through
   `walk.mjs` when a scenario is run); the preparation and observation done
   outside the controls (identification, `session_env.py`, the launcher, the
   watch, and afterwards the lane's step 11); and where completing a step
   needed knowledge the interface did not give. In a scenario every click's
   control is named by the scenario file, which is such knowledge: the walk
   is not evidence that the interface alone led to each step. The result file
   `walk.mjs` writes carries none of this; the operator's record does.
8. **End.** When the App's own quit is not among the allowed acts, send a
   termination to the launcher; it passes it to the App:

   ```sh
   kill -TERM <the launcher's process number>
   ```

   Wait until `<evidence folder>/launcher.out` holds the outcome (about fifteen
   seconds), then confirm that neither process remains (`ps -p` on each
   number prints no process). The launch record then says the launcher
   received the signal and attempted to pass a termination to the App, and
   the outcome is "failed": that is the truthful record of a launch ended
   from outside, not a defect.
9. **What stays.** The launch folder with its record, and the evidence
   folder. Nobody opens the home.
10. **What is ended, and what is left.** The launcher, the App and the watch
    are ended; the supplier's window service, which the first view starts, is
    left as it is, its state is recorded, and what becomes of it is the
    owner's. The operator ends what it started: the
    launcher as in step 8, which ends the App, and the watch, which ends by
    itself when the App does and is otherwise ended by its process number
    (`kill <the watch's process number>`). It then confirms, for the launcher,
    the watch and the App, that `ps -p <number>` shows no process, and that
    the App's process group is gone (`pgrep -g <the App's process number>`
    prints nothing).
    The lane's agent, not the operator, then confirms the same from its own
    shell after every run: the launcher's and the watch's process numbers are
    in the evidence folder's `*.started.json` files, and the App's is `pid` in
    the launch record (or, if the launcher wrote none, the operator's record
    of step 2). If an operator ends half-way, or the starter exits 3, some of
    these numbers may never have been recorded; step 11 is then how what was
    left is found and ended. A launch left without its operator is ended, not
    continued by someone else.
    The operator records whether a process named `SkyComputerUseService` is
    running at the end, with its start time, and the lane reports that.
11. **The lane looks for what remains.** The lane's agent, not the operator,
    makes this from its own shell after every run, by whatever path the run
    ended: a normal end, a walk stopped because the watch no longer showed
    the build running, a starter that exited 3, or an operator that failed or
    was lost before it returned. It does not wait for step 10's observations,
    which on some of those paths were never made. In order:

    1. For each `*.started.json` in the evidence folder: if `ps -o command= -p
       <its pid>` still shows the recorded command, end it as step 10 does
       (the launcher by a termination, the watch by its number) and confirm
       it is gone.
    2. The search:

       ```sh
       <python> -B app/examination/standalone/operated/stray.py "<the bundle>"
       ```

       It ends nothing and opens nothing, and runs on macOS only (elsewhere it
       looks for nothing and exits 2). It prints the remaining candidate
       processes: every process of this user running the bundle's executable,
       decided by the file's identity however its path is spelled. It exits 0
       when it found none, 1 when it found one or more, and 2 when it could
       not look, which includes a process it could not tie to a file, a
       bundle executable with more than one name, and a change to it the
       search detected; 2 is not "found none", and the run is reported as one whose
       check could not be completed. Processes for which the system gives no
       path at all are listed by number and not counted; why, and when that
       holds, is in `stray.py`.
    3. Each remaining candidate process is ended (`kill <number>`), confirmed
       gone, and recorded with its number and start time. Where it came from
       is not known from the search: the launcher's App not yet ended and a
       start the launcher did not make look the same to it, and it does not
       tell the home or environment either was started with. Only step 10's
       records, where they exist, can say more.
    4. The launch record's Library comparison (`real_library` in
       `record/launch-record.json` in the launch folder) is read. The
       launcher lists the real Library's places named for the build before
       the launch, and again about five and about ten seconds after the App
       exits, and compares those listings; it does not watch in between, and
       nothing is listed after its last listing. Where the launcher wrote no
       record, there is no comparison, and that is said.
    5. What steps 1 to 4 found, and what could not be done, is reported by
       the lane to App Agent 0 within the hour.

    The search finds the bundle's one executable and says nothing about Codex;
    that a stray start starts no Codex rests on what step 1 checks, and the
    search does not establish it. It looks at nothing in the real Library;
    nothing under the real Library is removed by any agent. This step is part
    of the condition of the exception stated in the next section.

## A view of an application that is not running

This is the one way the method can act outside the throwaway home, and it is
not closed.

- **What happens.** A view of an application that is not running starts it:
  the service launches it in the background through the system's launch
  service. Read in the supplier's own guidance for this service on the Mac,
  which presents it as intended, and seen once on 8 to 9 November. A build
  started that way is outside the launcher: it has the login session's
  environment (the system's documented behaviour for an application the
  launch service starts, not observed here) and the account's real home.
- **No refusing route was found by reading.** On the Mac the service has one
  way to read a window, addressed by the application's identifier or name; it
  takes no option that refuses when the application is not running, and no
  call addresses a process by its number. Its call that lists applications
  says whether each appears to be running, and is never used here. What the
  reading does not say: whether a click also starts an absent application.
- **How it can arise in a walk.** The watch says the build is running, the
  build ends by itself, and the next view is made. The script reads the watch
  immediately before every click and every view and refuses on anything older
  than three seconds, which narrows the interval to about a second and does
  not close it. A walk makes about seventeen calls.
- **What a stray start can and cannot do in this scenario.**
  - Both of the next two hold only while a start by the launch service
    is given none of the App's ten configuration variables
    (`CHIRALITY_CODEX_BIN` and the others `session_env.py` names), neither
    from the login session's environment nor from the bundle's own
    Info.plist. Read in the App's source: when any of them is present, empty
    included, the App takes its configuration from the environment and does
    not look for a saved request at all, and with a usable configuration it
    starts Codex (`lib.rs`, `explicit_environment_launch`;
    `desktop_startup.rs`, `resolve`). On this host all ten were absent on 13
    November (`session_env.py`, against the candidate built from cfc22efd);
    step 1 asks again before every walk and stops on anything but absent.
  - It opens at first-use setup: no setup has been saved for a build with a
    new identifier (read in the App's source: with no configuration from the
    environment and no saved request the launch is "setup-required").
  - It starts no Codex: the App starts Codex only when it has a
    configuration, which setup required does not give (read).
  - The walk never confirms setup, and stops as soon as the watch shows the
    launcher's build gone, so it does not go on to operate the stray build
    (read in the script; a click or view already under way is not recalled).
  - What it writes under the real Library before any choice: the App's own
    code writes nothing there. With no saved request it returns before it
    takes or creates its data folder, which is first made at the confirmation
    (read: the start asks only whether the request file exists; the review
    computes paths and creates nothing; the consumers that would use the
    data folder are not given one while setup is required; the page's script
    stores nothing at a first start). What appears is what the system's web
    view makes for any application that opens one: folders named for the
    build's executable under `WebKit` and `Caches`. Every development build
    has the same executable name, so these are shared with earlier builds:
    on this host `WebKit/chirality-app-v4` and `Caches/chirality-app-v4`
    exist from 20 October and were last changed on 12 November, by an earlier
    build launched under the real home, after which no Application Support
    folder for it existed (seen by names and times only). A stray start
    would change those folders rather than make new ones. What
    else the system records for a newly seen application has not been read.
  - It reads the owner's real home as any application the owner starts
    would. It makes no sign-in, no model request and no conversation: none
    exists before setup (read). Whether the system's web view or the
    operating system sends anything on its behalf was not examined.
- **How it is found and ended.** Step 11.
- **The condition of the exception.** Before every walk, the ten names are
  absent in the login session and in the bundle's own launch environment
  (step 1, `session_env.py`), or the walk is refused. After every run, by
  whatever path it ended, the lane ends what the started files show,
  searches for remaining candidate processes by the executable's file, ends
  what it finds, reads the launch record's Library comparison (or records
  that the launcher wrote none), and reports the same hour (step 11). A run
  after which any of that was not done is a breach, reported to App Agent 0
  as one; it is not an inconclusive run. Throughout, the lane keeps the
  identified bundle unchanged: no rebuild, replacement, renaming or added
  link, from identification through recovery. The search's comparisons of
  the bundle's executable detect a change; they do not prove the file
  stayed unchanged.
  What the two checks do not see: a stray start that began after the
  launcher's last listing and ended by itself before the search is seen by
  neither. **Neither a clean process search nor an unchanged Library
  comparison establishes that no stray start occurred.**
- **The owner's decision, 13 November 2026, relayed by App Agent 0.** This
  exposure is accepted for the scenario "first-use setup without a project,
  new settings" and for no other. The question as it was put to the owner:
  when an agent test-drives the App through computer use there is a roughly
  one-second gap per step in which, if the App crashed, the computer-use
  service would relaunch the development build under the owner's real home;
  such a stray start opens at first-use setup, starts no Codex, sends
  nothing, and the App's own code writes nothing under the real Library
  before setup is confirmed (the system's web view makes its own cache
  folders); it is checked for after every run, ended and reported within the
  hour; there is no way to prevent it on the Mac; "Do you accept this risk
  for the first-use setup scenario (17 steps per walk)?" The owner selected
  "Accept it (Recommended)", described as: "Live walks of the first-use setup
  scenario may go ahead on this Mac once the tool is reviewed and I have your
  leave for the screen. The exception covers this one scenario only; I ask
  again before any scenario that confirms setup or starts Codex."
  - Leave for the screen, which it names, is no longer asked: see the owner's
    words of the same day under "When it may be used". A walk runs on App
    Agent 0's go.
  - It rests on the facts in this section as they are stated. If one of them
    is found to be wrong, no walk is made until the owner has been asked
    again.
  - Its condition is stated once, above, under "The condition of the
    exception".
  - A scenario that confirms setup, starts a Codex or types anything is not
    covered: the question is put again with that scenario's own extent.
- **App Agent 0's decision on the corrected account, 13 November 2026.**
  "Decided by App Agent 0, 13 November 2026, under the project grant in
  AGENTS.md. Two of the facts given to the owner with the question were
  corrected after the owner's answer: that a stray start starts no Codex
  holds only while none of the ten CHIRALITY_ variables is present in the
  environment the launch service gives the build; and that it 'sends
  nothing' was more than was read. The owner then said, in the Inter-Project
  thread on 13 November: 'I'm AFK, no need to ask for leave. Also that
  MacBook Pro machine is dedicated to this agentic dev session. I do my
  personal work on other machines. So no need to ask permission to use the
  computer or screen.' On that authorisation and the grant, Agent 0 decides
  that the exception stands on the corrected account, for the first-use
  setup scenario only. This is Agent 0's decision; it is not recorded as the
  owner having accepted the corrections. What is established, by reading the
  App's source: before setup is confirmed there is no sign-in, no model
  request and no conversation. What is not examined: what macOS or its web
  view sends for an application that opens one. The owner may reverse
  this."
  - Its condition is the one stated above, under "The condition of the
    exception". The rule that a fact found wrong means no walk until the
    owner is asked again also stands.
  - What ends the exception without a further word from anyone: evidence
    that this guarded scenario reaches the owner's credentials, the
    installed v3, the keychain or `~/.codex`, or sends application or user
    content. Then the walk stops, nothing is retried, and the lane tells App
    Agent 0.

## Running a scenario

A scenario is a file of steps and expected states, walked by a script the
operator loads. There is one: `first-use-setup.scenario.json`, "first-use setup
without a project, new settings". It is the opening of the first-use setup page
up to, and not including, the App's own confirmation. Its acts are views and
clicks; nothing is typed, no file or folder is chosen, no confirmation is
answered and no setup is confirmed. It starts no Codex and needs no sign-in.
These prohibitions are narrower than the governing text on purpose (see "What
governs it"). Its controls (a project choice, two settings choices, "Review
setup", "Change my choices" and two disclosures) are none of the act controls
REQ-009 names, so it makes no synthetic capture and the examination-name
requirement does not arise in it.

What it shows when it passes:

- **SETUP CHOICES REVIEWED.** After "Continue without a project" the page reads
  "Ready to review. Nothing is created or saved until you confirm."; "Review
  setup" shows "What setup will do" with exactly its five lines, in order and
  no other, and the control "Create settings and save for next launch…", which
  is never clicked; "Exact locations" shows three locations under the App's
  data folder in the throwaway home.
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
The other `wrong.*.json` files beside it do the same for more states: a line
of "What setup will do" missing, a sixth line added, a location outside the
home, Review setup available with existing settings; and one where a control
has other words that begin the same way, which the walk does not click (it
stops, inconclusive, exit 2). This is the check rejecting wrong states; it
says nothing about a build.

**In a window.** Steps 1 to 3 above first: the launcher running, the App's
process number confirmed, the identifier taken from the identification record.
Then start the watch, in the same way as the launcher. It keeps a small file
saying whether that process is running, what its executable is and what child
processes it has, which the script reads because the node runtime cannot ask
the system itself:

```sh
<python> -B app/examination/standalone/operated/detached.py <evidence folder> watch -- \
  <python> -B app/examination/standalone/operated/watch.py <the App's process number> <evidence folder>/watch.json
```

The watch ends by itself when the App does.

Then, in the operator's `js` tool, with the values filled in:

```js
var fs = await import('node:fs');
var walk = await import('file://<repository>/app/examination/standalone/operated/walk.mjs');
var scenario = JSON.parse(fs.readFileSync('<repository>/app/examination/standalone/operated/first-use-setup.scenario.json', 'utf8'));
var sky = (await import('@oai/sky')).sky;
var report = await walk.run({sky, scenario, app: '<bundle identifier>', home: '<launch folder>/home',
  bundle: '<the bundle, the path of the .app folder>',
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
  show running, with its executable inside the bundle, within the last three
  seconds. It reads the watch file again before every click and every view.
  It makes views and clicks and nothing else. It clicks only a control a step
  names, found by its words whole: a control whose words merely begin the
  same way is not it, and a control whose words end with an ellipsis is never
  clicked.
- It stops, and says where, if a view holds anything that is not the
  scenario's page. The rule is what a view may hold, not a list of things it
  may not: the view must say it is of the bundle; at the top it holds the
  App's one window and the menu bar and nothing else; directly inside the
  window it holds only what the scenario lists. A sheet, a dialog, an alert,
  a second window, or a kind of thing nobody named, stops it. It also stops
  if the watch file stops showing the build running, at the last step as at
  any other. A result that stopped this way is inconclusive, not a pass:
  report it as it is.
- An expected text is expected exactly once in the view, and a named location
  exactly once; a second copy is a failure, not a pass.
- **What the watch file is, and is not.** It is a sample taken once a second.
  The build can end between a reading and the call that follows it; what a
  view made then does, and how it is found, is the section "A view of an
  application that is not running" above. Nothing in this scenario ends the
  App, and the operator ends it only after the walk. A process the App started
  that has been given another parent, or that came and went between samples,
  is not seen as a child.
- **Whole views, or nothing.** Before any click the script asks for two whole
  views, one after the other; the first view of an application was seen to be
  whole without asking, so only the second shows that asking is honoured. If
  either of them, or any later view, comes back as differences, the walk stops
  there. That view, and the window rebuilt from it, are kept in the result for
  reading; no check is credited from a rebuilt view and no click is made from
  one, because how differences place what they add has not been established.
- This scenario starts no process. If the watch file shows the App with a
  child process, the script stops and the result is a failure.
- A watch file that is missing, cannot be read, is for another process, says
  the process has gone, names an executable outside the bundle, or was last
  written more than three seconds ago is read as the build not running: the
  script refuses before any call, or stops. It is never read as "no child
  process"; a step whose watch file could not be used records its child
  processes as not known.
- `nodeRepl.write` joins what successive calls write without a separator, so
  write the summary once.
- The result file holds every call made and every view's returned text whole.
  The operator adds the times of its own calls and what it saw outside the
  script (a prompt appearing, or the focus leaving the build) to its own
  record.
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
  scroll, drag, paste and list applications. None is used unless the scenario
  and App Agent 0's go for the walk name the act, and `list_apps` is never
  used.

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
- Not yet observed: `disableDiff` (the supplier's guidance says it returns a
  fresh whole view; a walk's first two calls observe it); any method other
  than a view and a click.
- The launcher on main at that time could not launch on that host, because
  macOS refused a listing of two Library folders it watched. The launches were
  made with those two names removed; the launcher's own change followed.
- Walk A2's first attempt stopped at identification's check: the operator's
  `python3` had no jsonschema. The lane's preparation and the operator's
  shell used different interpreters, so preparation that passes for the lane
  shows nothing about the operator's environment.
