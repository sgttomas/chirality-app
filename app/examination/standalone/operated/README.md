# Operating a development build's window

This is how an agent reads and clicks the window of an identified development
build of the App during an examination. It uses the supplier's own computer-use
service, reached from inside a Codex session. Reaching it runs binaries inside
ChatGPT.app (the operator's node runtime and its host, and a Codex app-server),
and the service itself is installed under the owner's Codex home
(`~/.codex/computer-use/`) (see "What the route starts").

It is development tooling. What it yields is what an agent saw and did in a
development build. It is never evidence that the product does something for a
person, and it is never the person-operated observation a release criterion
asks for.

## What the route starts, and the owner's answer

A walk's first call starts two things outside the throwaway home, and the owner
has accepted them as they are. What is known of each, marked as read, observed
(by the examination lane, from process names, parents, arguments and start
times, on 13 November 2026), observed by App Agent 0, or not examined:

- **A Codex app-server.** `codex app-server --listen stdio://`, run from inside
  ChatGPT.app (`/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex`).
  Its parent was ChatGPT.app's `node_repl` (observed, twice), a binary inside
  ChatGPT.app (observed by App Agent 0) and a child of the provider's Codex.
  Those observers took that `node_repl` for the process that runs the `js`
  tool; they did not look at which process holds the tool's own files, or
  whether `node_repl` has children of its own. A later observation did (step
  10, "The operator's node runtime and its host"): the tool runs in a node
  kernel whose parent is `node_repl`. Its parent has been the host (observed
  in A2's fifth to eighth attempts). When the import and the first view were
  made in one block (A2's second, third and fifth attempts), it started
  within the same second as that block (observed, three times). When the
  import was a call of its own (the sixth, seventh and eighth), it started
  within the same second as the import returned, before any view (observed,
  three times). Inter-Project reported the same of its own delegates'
  imports on 13 November, with or without a view after them (observed by
  Inter-Project; the lane saw two such helpers, started at 20:43 and 20:44
  UTC). Left alone, it outlives the walk and the delegate that imported the
  service (observed in the second and third attempts, and by Inter-Project). It runs
  with CODEX_HOME set to the owner's own Codex home, `~/.codex`, and HOME the
  account's real home (observed by App Agent 0).
- **The window service.** `SkyComputerUseService`, from
  `~/.codex/computer-use/Codex Computer Use.app`, started by launchd within the
  same second as the first view when it is not already running (observed in
  A2's second, third and fifth to eighth attempts; in the sixth to eighth,
  where the import was a call of its own, at the first view and not at the
  import). Each of the two started in the second and third attempts was
  later found no longer running, without the lane or App Agent 0 having
  signalled it (observed: absent at a
  later check; when it ended, and why, not known).
- **Not examined:** which files the app-server reads, whether it uses a
  credential (such as a sign-in held under `~/.codex`), and what it or the
  service sends. The supplier's documentation for the service says nothing
  about a Codex app-server, a Codex home or a native pipe (read).
- **The start-up failure, and its cause.** A walk's first view failed with
  "Sky Computer Use native pipe startup failed" within about five seconds in
  A2's second, third, fifth, sixth and seventh attempts, each time with a
  freshly started service and app-server (observed). The cause, established
  by App Agent 0 with Inter-Project on 13 November and confirmed by its
  remedy: the provider's Codex then running (started 12 November) ran an
  executable that had been replaced on disk, and the window service refused
  it as unauthenticated. The replacement predates all five: before the third
  attempt, at 07:55:55 UTC, `stray.py` already listed that process as one
  whose executable had been removed (the lane's record before that attempt,
  `a2-third-preconditions.txt` in its evidence folder), and the file was
  replaced again at about 15:52 UTC. The owner's restart of T3 Code at about 20:42 UTC
  started the provider again from the executable on disk; a delegate's view
  worked at 20:45 UTC, and A2's eighth attempt passed. This explains the
  native-pipe failures only. A2's first attempt stopped at identification's
  check (the operator's Python had no jsonschema), and its fourth was refused
  at the runtime check before any call; neither reached a view. The lane's
  provider check at the go tests for that one condition before every walk
  ("At the go").

The owner's answer, 13 November 2026, to a question App Agent 0 put in a
dialog. The question: "Agent-operated walks of the App are held because the
supplier's computer-use helper starts a second Codex using your real ~/.codex
home (not a scratch one), and it also failed to start cleanly once ("native
pipe startup failed"). How do you want me to proceed with that route?" The
owner chose "Permit as it is", whose description read: "Allow walks now,
accepting that the helper's Codex runs against your real ~/.codex. Agents still
never open that folder, sign in, or answer a macOS prompt. The start-up failure
remains unexplained." That is the whole of the authorisation. App Agent 0
applies it to walks of the first-use setup scenario by the route as found;
everything in "When it may be used" below still holds, and a scenario that
confirms setup, types anything or starts the App's own Codex needs its own
question to the owner.

The owner's words permit the route despite its unexamined behaviour. They
establish neither that a credential is used nor that it is untouched. App Agent
0's operating rule, which is App Agent 0's and not the owner's: established
reading or use of the owner's credentials by anything a walk starts stops the
walk, one under way included, and returns the question to the owner. Proving
that no credential is accessed is not a prerequisite for a walk, and nobody
inspects the protected home to find out.

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
- A walk by this route starts the helper's Codex app-server on `~/.codex` and
  the window service, as the owner has accepted (see "What the route starts").
  After every walk, attributable walk processes are ended; unresolved ones are reported, and a walk with an unresolved process has not been recovered (steps 10 and 11). Neither may already be
  running when the operator looks, before the walk's import and first call;
  if one is, no walk is made (step 10). No agent opens or reads
  anything under `~/.codex` or `~/.codex-hub` (process listings name paths
  there, and that is all), signs in, copies a sign-in or sees a credential's
  value. The operator runs no Codex binary of any kind itself and no binary
  inside `/Applications/ChatGPT.app`; its `js` tool runs there, which is the
  route. Nothing is downloaded.
- The App itself starts no Codex in the first-use setup scenario. Launches
  that start the App's real Codex through the launcher remain closed.

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
purpose: no setup confirmed, nothing typed, no Codex started by the App, no macOS prompt
answered (see "Running a scenario"). The governing text does not enlarge the
exception the owner accepted, and App Agent 0 decided, for its live runs.

## Three cautions

1. **Launch through the launcher, and confirm the process is running, before
   any state call.** A state call for an application that is not running
   starts it through the system's launch service: outside the launcher, with
   the account's real home. See "A view of an application that is not
   running" below for what remains of this once a walk is under way.
2. **Address the build by its bundle identifier in every call, and never call
   `list_apps`.** An application name can match another application.
3. **The walk starts a Codex on the owner's own Codex home.** The helper's
   app-server outlives the walk unless it is ended. By whatever path the walk
   ended, attributable walk processes are ended; unresolved ones are reported, and a walk with an unresolved process has not been recovered (steps 10 and 11).

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
  `candidate_key` is the key the assignment names; the check does not print the
  key, so read it:

  ```sh
  <python> -c "import json,sys; print(json.load(open(sys.argv[1]))['candidate_key'])" \
    <candidate folder>/identification/candidate-identification.json
  ```

  The path the `ls` prints is the bundle; it is needed again below. The lane keeps that bundle unchanged
  from identification through recovery: no rebuild, replacement, renaming or
  added link (see "The condition of the exception").
- **The homes root.** The launcher makes each launch folder under the lane's
  homes root, which must already exist; it never creates it. If it does not
  exist the launcher refuses and says so. The lane makes it, once.
- **The evidence folder.** Outside every checkout, made new by the lane at App
  Agent 0's go, because the lane keeps its own look and its sample of the
  service's socket folder there (step 10, "The look"; "The lane's sample of
  the service's socket folder"). The assignment names it. Before anything
  else in it, the operator confirms it holds only the lane's files (names
  beginning `lane-`, and `socket-folder-sample.txt`, which grows while the
  walk runs) and leaves them alone; anything else in it means no walk.
  Everything else the method writes there is the operator's.
- **The checkout**, a clean checkout of main at a revision the assignment
  names, from whose root every command here is run and which `<repository>`
  means below. With the interpreter, before it begins, the operator confirms
  `git rev-parse HEAD` prints that revision and `git status --short` prints nothing; if not,
  it stops. It uses no other checkout, its own included.
- **App Agent 0's go for the walk**, its time, and the acts it allows.

An assignment gives these, the role to load, the bounds in words and how to
return; this method gives everything else.

## At the go (the lane)

At App Agent 0's go, before the operator is delegated, the lane's agent makes
these from its own shell, in this order, and keeps each output in the new
evidence folder under a name beginning `lane-`. Each opens nothing under
`~/.codex` and signals nothing.

1. **The provider check, first.** The provider is the Codex the operators'
   sessions run under: the process whose command is a `codex` executable
   with the one argument `app-server`, and whose parent is the process of the
   application that runs the delegates (on this host,
   `/Applications/T3 Code (Beta).app/Contents/MacOS/T3 Code (Beta)`). It is
   found in the process table at the go, never by a number remembered from
   before. Exactly one such process must exist, and its start must be later
   than the modification time of its executable on disk. If none is found
   (on another host, or after an update that moves or renames the
   delegates' application or the provider), or more than one, that is not
   exactly one: no walk, and it comes to App Agent 0, who corrects this
   description; it is never worked around by picking a process:

   ```sh
   ps -axo pid=,ppid=,command=                 # find it: parent the delegates' application, command `<path>/codex app-server`
   ps -o lstart= -p <its number>               # its start (local time)
   stat -L -f %m <its executable>              # the executable's modification time (seconds)
   ```

   with the start converted to seconds as step 10 shows. The number,
   parent, start and modification time (both also in UTC), the executable and
   the verdict go into `lane-provider-check.txt`, and the number into
   `lane-provider.pid`. If there is not exactly one, or its start is not
   later, no walk is made and nothing else is done: the lane tells App
   Agent 0, and restarting the provider is the owner's act. This tests for
   the one condition found to have made the first views fail (a provider
   running an executable replaced on disk; see "What the route starts").
   When it passes, that condition is absent, and nothing more: it does not
   show that the service will accept the call.
2. **`stray.py`** on the candidate's bundle (step 11 shows the command): it
   exits 0 with no remaining candidate process, or no walk is made.
3. **The lane's look**: the first `ps` command of step 10, kept whole in
   `lane-look.txt`. A running window service, or a running process whose
   command contains `app-server --listen`, whatever its parent, means no
   walk, and the lane tells App Agent 0. An exited entry (state `Z`,
   `<defunct>`) is recorded with its number, parent and state and is not a
   bar: it has exited and can do nothing.
4. **The sample of the service's socket folder** ("Running a scenario"),
   started so that it outlives the shell call that starts it: through
   `detached.py` with the name `lane-socket`, running the loop with
   `/bin/sh -c '<the loop>'`. It ends by itself at its stated stop; step 11
   leaves it alone.

Then the lane delegates the operator.

## A walk, in order (the operator)

The operator does these and nothing else, in this order. Each names where
this method says how.

1. Confirm the interpreter, the checkout, the candidate and its key, and that
   the evidence folder holds only the lane's files ("What the operator is
   given").
2. Identify its node runtime and its host with the marker, and record them in
   `runtime.txt` in the evidence folder (step 10, "The operator's node
   runtime and its host").
3. The environment check, then the launcher (step 1).
4. Confirm the App's process (step 2) and take the identifier (step 3).
5. Start the watch ("Running a scenario", "In a window").
6. Recheck its two identities and make its look, the last things before the
   import, both kept whole in `look.txt` (step 10, "The look").
7. The import, a `js` call of its own; then wait at least ten seconds; then
   the record after the import, `after-import.txt` ("In a window").
8. The walk's call, once ("In a window"). Steps 5 and 6 below say what its
   views and clicks are; the operator makes no view or click of its own
   outside it.
9. Record (step 7); end the launch (step 8); then steps 9 and 10, judging
   each of the route's processes by the rule for its kind.
10. Close the marker, and return ("The operator's return").

Wherever this method says no walk is made, or the walk stops, the operator
keeps what it has, ends what it started (steps 8 and 10), closes the marker
if it was opened, and returns. Step 11 and the sample of the socket folder
are the lane's; the operator neither makes nor waits for them.

**Recovery.** The lane is the recovery owner. If the operator stops, fails,
is cut off or writes no result, the lane acts from the evidence folder's
`*.started.json` files, `runtime.txt`, `look.txt`, `after-import.txt` and its
own step 11, without waiting. So the operator writes every started file
where this method says, keeps `runtime.txt` and `look.txt` in the evidence
folder as it makes them, and moves or removes nothing there.

**When this method does not say.** If it is not enough to go on, or the
service returns something it does not describe, or the walk stops: keep that
result as it is and stop. No extra or exploratory view or import, no test
of which process starts what, no changed expectation, no edited scenario or
script, no retry, no workaround. A
service call that throws has not been shown to have had no effect: record it
as an exception, keep the error whole, and stop. Guidance the operator
needed and this method did not give is a finding about the method; it goes in
the return.

## The operator's return

It leads with the walk's summary as printed (the verdict, the four outcomes
and any "caused by:" lines), or with "no walk" and why. Then:

- its two recorded identities (the runtime and the host: number, start in
  UTC, executable), their relationship, and the host's parent; its Codex
  version as "not known", with the host's parent's executable and that
  file's modification time beside it;
- the recheck and the look, whole; the import's time; `after-import.txt`,
  whole; the walk call's time;
- the evidence folder's path, the launch folder's path (or that none was
  made), and the launch record's outcome line;
- the raw result or error, whole, for any step that did not pass;
- every deviation from this method, however small, and every place it did
  not say what to do;
- what it started (from the started files), what it ended, and how it
  confirmed each gone (`ps -p`, `pgrep -g`);
- each of the route's processes: number, start in UTC, command and actual
  parent; the rule it was judged by and which test of it, if any, it failed
  (for the helper, which recorded identity its parent is); and whether it was
  ended (with the recheck before the signal and `ps -o stat=` after) or left
  as unresolved;
- the marker: not opened; closed (and kept); or closure unconfirmed, and why;
- its model and reasoning effort, and that this method and its assignment
  were its only instructions.

Its last line is the verdict, or "no walk", and the evidence folder.

## The steps

1. **Launch.** Before this step, the operator identifies its node runtime
   and its host by the marker (step 10, "The operator's node runtime and its
   host"); if they are not identified, no walk is made and nothing has been
   launched. Then confirm that a start of the build by the system's launch
   service would be given none of the App's eleven configuration variables (why:
   "A view of an application that is not running", below):

   ```sh
   <python> -B app/examination/standalone/operated/session_env.py "<the bundle>"
   ```

   It asks the login session's launch domain and the bundle's own Info.plist,
   and prints each name with "absent", "present" (empty included) or "could
   not be established" and why; never a value. It exits 0 only when all eleven
   are absent. Any other result, "could not be established" included, means
   no walk is made: stop, record what it printed, and the lane tells App
   Agent 0.
   Then, from the root of a clean checkout of main, with the walk's evidence
   folder, start the launcher on
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

   It must be this dynamic import inside that tool, made as a call of its own
   (see "In a window"). Whether the import alone starts anything was not known
   when it and the first call were made in one block; a walk now records what
   is running after the import and before the first view.
5. **A view.**

   ```js
   var state = await sky.get_app_state({app: '<bundle identifier>'});
   var whole = await sky.get_app_state({app: '<bundle identifier>', disableDiff: true});
   ```

   The first form, with the application alone, is how the views that worked
   on 13 November asked; a walk's first view asks so. The second asks for the
   whole window, and every later view of a walk asks so. The result gives the application's path, a reference to a screenshot, and
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
   seconds; wait at most sixty, since the launcher lists the real Library
   about five and again about ten seconds after the App exits, before it
   writes the outcome, so fifteen is the normal case), then confirm that neither process remains
   (`ps -p` on each number prints no process). If no outcome comes within
   sixty seconds, or a process remains, the recovery is incomplete: the
   operator records it, tells the lane in its return, and goes on with the
   other checks of step 10. This method authorises no stronger signal. The launch record then says the launcher
   received the signal and attempted to pass a termination to the App, and
   the outcome is "failed": that is the truthful record of a launch ended
   from outside, not a defect. The launch record's outcome describes how the
   launch ended; it is not the walk's verdict, which is the walk's result
   file's.
9. **What stays.** The launch folder with its record, and the evidence
   folder. Nobody opens the home.
10. **What is ended.** The launcher, the App and the watch are ended. Of the
    route's own processes (see "What the route starts"), those attributable to
    the walk are ended; unresolved ones are reported, and a walk with an
    unresolved process has not been recovered. The operator ends what it started: the
    launcher as in step 8, which ends the App, and the watch, which ends by
    itself when the App does and is otherwise ended by its process number
    (`kill <the watch's process number>`). It then confirms, for the launcher,
    the watch and the App, that `ps -p <number>` shows no process, and that
    the App's process group is gone (`pgrep -g <the App's process number>`
    prints nothing).
    Then the route's processes. Each is identified before it is signalled, its
    identity is checked again immediately before the signal, and each is
    recorded with its number, start time (in UTC), parent and command. Of
    them, attributable walk processes are ended; unresolved ones are reported, and a walk with an unresolved process has not been recovered.

    ```sh
    ps -axo pid=,ppid=,lstart=,command=      # every process: number, parent, start time (local), command
    ps -o lstart=,ppid=,command= -p <number> # one process, again, just before it is signalled
    date -u -r "$(date -j -f '%a %b %e %T %Y' '<lstart as ps printed it>' +%s)" +%FT%TZ   # that start time in UTC
    lsof -t "<evidence folder>/runtime.marker"   # the process holding the operator's marker open
    kill <number>                            # an ordinary termination
    ps -o stat= -p <number>                  # nothing, or a state beginning with Z: it has ended
    ```

    - **The operator's node runtime and its host**, identified before step
      1, after the operator's prerequisites and its confirmation of the
      evidence folder ("What the operator is given"), so that a runtime that
      is not the one expected costs no launch. The operator makes one call in
      its `js` tool that opens a marker file in the evidence folder and keeps
      it open,
      `globalThis.runtimeMarker = await (await import('node:fs')).promises.open('<evidence folder>/runtime.marker', 'w');`,
      and then asks which process holds it (`lsof -t`, above). That one
      process is its runtime, and the runtime's parent is its host. Each is
      recorded as an identity, by its process number, start time (and that
      start in UTC, by the `date` line above) and executable (`ps -o
      lstart=,ppid=,command=` on each), and so is the relationship between
      them: the runtime's parent is the host. The host's parent is recorded
      the same way, with its executable's modification time in UTC (`TZ=UTC
      stat -f '%Sm' -t '%FT%TZ' <that executable>`) beside its start, and the
      operator's Codex version is recorded as "not known": it runs no Codex
      binary to find out, and neither the path nor the time establishes
      which version a running process is. All of this goes into `runtime.txt`
      in the evidence folder, the first thing the operator records about
      itself. Wherever
      this method speaks of the runtime or the host, it means these two
      recorded identities, never any process that merely has the same name.
      What is expected is what was observed on 13 November 2026 at 16:48 UTC,
      and again in every attempt since: the runtime was
      ChatGPT.app's node
      (`/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node`)
      running a `kernel.js` with a session identifier, and its host was
      ChatGPT.app's `node_repl`
      (`/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node_repl`),
      a child of the provider's Codex: the host's parent is the process the
      lane's provider check named at the go (its number is in
      `lane-provider.pid`; "At the go"); if that file is missing, or names
      another process, it is not. If `lsof` names none or more than one,
      or the runtime or its host is anything other than that, the runtime is
      not identified and no walk is made: nothing has been launched, and the
      operator closes the marker and returns. That call imports only the
      standard library and invokes no computer-use method; whether it starts
      anything has not been tried. The marker stays open, held by the
      runtime, through the launch and the watch until the walk ends. At a walk
      the operator uses its `js` tool for four things and nothing else: this
      marker call; the import of the service, a call of its own; the walk's
      call; and the marker's close. A walk refused before the import uses two
      (the marker call and its close), and one refused after the import and
      before the walk's call uses three (the marker call, the import and the
      close). App Agent 0 held that tool, and narrows
      its hold for the marker call alone, not for any other agent or use.
      The marker file is in the operator's evidence folder, never under
      either Codex home. When the walk ends, and whenever a walk is refused
      after the marker was opened while its runtime is still available (the
      runtime or its host is not the one expected, the identities differ at
      the look or at the recheck before the walk's call, the import throws,
      the look finds a process, or the two looks disagree), the
      operator closes it (`await runtimeMarker.close()`) and it is kept, not
      removed. The identification worked on its first trial (A2's fourth
      attempt, below); if it fails, that is "no walk", recorded as a finding
      about this method.
    - **The look, before the import and before the first call.** Then, after
      the launcher and the watch, as the last things before the `js` call
      that imports the service ("Running a scenario"), the operator checks
      its two identities again and looks. The check: `lsof -t` on the marker
      names the same one process as before, and the second `ps` command above,
      on the runtime and on the host, shows for each the same number, start
      time and executable as recorded, with the runtime's parent still the
      host. A runtime replaced between the marker call and the import would
      otherwise leave the identification stale. The look: the first `ps`
      command above, for a window service (by its command, below) and for
      any process whose command is the app-server's, whatever its parent.
      Both are kept whole in `look.txt` in the evidence folder, whose first
      line is the time of the look in UTC (`date -u +%FT%TZ`). An exited
      entry (state `Z`, `<defunct>`) is not a running process and is not a
      bar; it is recorded as it is found.
      Any difference in the check, or any such process running, means no walk
      is made: what was found is recorded (a process with its number, start
      time and parent), the operator ends what it started (steps 8 and 10),
      closes the marker and returns, and it comes to App Agent 0. A helper
      left by an earlier attempt blocks the walk in the same way; who owns it
      is decided from that attempt's evidence, never by assigning it to the
      new walk. The lane also looks, from its own shell, at App Agent 0's go,
      with the same command, and keeps what it finds in the evidence folder as
      its own record. The operator's look decides; if the two disagree, no
      walk is made, and it comes to App Agent 0.
    - **The walk's app-server** is a process whose command is exactly
      `/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex app-server --listen stdio://`
      (the whole command, compared as text, not a part of it); whose parent
      is one of the two recorded identities, the operator's runtime or its
      host (the parent's number and start time those recorded); and whose
      start, in UTC, is no earlier than the look and no later than the walk's
      end. A process meeting all three is ended. The look's time is the first
      line of `look.txt`; the walk's end is the result file's `finished`, or,
      where there is no result file, the time the operator records when the
      walk stopped, on every path that stops it. Where either is missing, no
      endpoint is inferred: the route's processes are unresolved. In A2's fifth attempt the
      helper's parent was the host (observed, once); the earlier record saw
      `node_repl` as its parent too, before anyone looked for the kernel below
      it. The rule accepts either, since once is not always. Whether the
      walk's first call succeeds or fails, each route process is recorded
      with its number, start time, command and parent, so a walk records the
      helper's actual parent. One with that command whose parent is neither
      recorded identity, or that fails the interval, is unresolved: it is
      recorded, left and reported, and the walk has not been recovered. The
      rule is not extended during a walk.
    - **The walk's window service** is a process whose command is exactly
      `$HOME/.codex/computer-use/Codex Computer Use.app/Contents/MacOS/SkyComputerUseService` (with `$HOME` as the account's home, compared as text),
      whose parent is launchd (process 1), and whose start, in UTC, is no
      earlier than the look and no later than the walk's end; and the look
      found none, and the route was used by this operator alone. Then it is
      ended. Where its attribution is conflicting or uncertain (more than one
      such process, a look not made or not recorded, the two looks in
      disagreement), it is left, recorded, and reported, and the recovery is
      incomplete.
    - **Before every signal**, the second `ps` command shows the same start
      time, parent and command as when the process was identified; if not, it
      is not signalled, and it is reported.
    - **What the look cannot rule out.** Something else could start a window
      service between the look and the walk's first call. It would lie inside
      the interval, be taken for the walk's and be ended. The look cannot rule
      that out; one operator at a time across this project and the others on
      this machine is what makes it unlikely. This is a limit of attribution:
      it gives no permission to disregard contrary evidence or known desktop
      activity. If anything says a service is not the walk's, it is
      unresolved, whatever its start time.
    - An ended process may stay listed with a state beginning with `Z` until
      its parent collects it; that is ended. A state containing `E` (often
      `?E` straight after the signal) is a process still exiting, not yet
      ended: check again after five seconds, up to three times. If it is then
      still listed and not `Z`, it is recorded as not confirmed ended, the
      recovery is incomplete and is reported in the return, and no stronger
      signal is sent. No process that predates the
      walk is ever signalled. The operator signals nothing else: not the node
      runtime or its host; not the provider's Codex or any of its other
      children (its `codex-code-mode-host`, and other sessions' `node_repl`
      and kernel processes, whatever their names); nothing the lane's look or
      the operator's look found; not a process group. None of these
      commands opens anything under `~/.codex`.
    The lane's agent, not the operator, then confirms the same from its own
    shell after every run: the launcher's and the watch's process numbers are
    in the evidence folder's `*.started.json` files, and the App's is `pid` in
    the launch record (or, if the launcher wrote none, the operator's record
    of step 2). If an operator ends half-way, or the starter exits 3, some of
    these numbers may never have been recorded; step 11 is then how what was
    left is found and ended. A launch left without its operator is ended, not
    continued by someone else.
11. **The lane looks for what remains.** The lane's agent, not the operator,
    makes this from its own shell after every run, by whatever path the run
    ended: a normal end, a walk stopped because the watch no longer showed
    the build running, a starter that exited 3, or an operator that failed or
    was lost before it returned. It does not wait for step 10's observations,
    which on some of those paths were never made. In order:

    1. For each `*.started.json` in the evidence folder other than the lane's
       own (`lane-*.started.json`, which end by themselves): if `ps -o command= -p
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
    4. The route's processes, identified as step 10 says, from the operator's
       records of its runtime, its host and its look (where there are none, nothing is
       attributable): attributable walk processes are ended; unresolved ones are reported, and a walk with an unresolved process has not been recovered. Each is recorded with its number, start
       time, parent and command, and whether the operator or the lane ended it.
    5. The launch record's Library comparison (`real_library` in
       `record/launch-record.json` in the launch folder) is read. The
       launcher lists the real Library's places named for the build before
       the launch, and again about five and about ten seconds after the App
       exits, and compares those listings; it does not watch in between, and
       nothing is listed after its last listing. Where the launcher wrote no
       record, there is no comparison, and that is said.
    6. What steps 1 to 5 found, and what could not be done, is reported by
       the lane to App Agent 0 within the hour.

    The search finds the bundle's one executable and says nothing about Codex;
    that a stray start of the App starts no Codex rests on what step 1 checks,
    and the search does not establish it. It looks at nothing in the real Library;
    nothing under the real Library is removed by any agent. This step is part
    of the condition of the exception stated in the next section.

## A view of an application that is not running

This is one way the method can act outside the throwaway home, and it is not
closed. It is not the only one: the route's own Codex app-server and window
service act outside it on every call (see "What the route starts").

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
    is given none of the App's eleven configuration variables
    (`CHIRALITY_CODEX_BIN` and the others `session_env.py` names), neither
    from the login session's environment nor from the bundle's own
    Info.plist. Read in the App's source: when any of them is present, empty
    included, the App takes its configuration from the environment and does
    not look for a saved request at all, and with a usable configuration it
    starts Codex (`lib.rs`, `explicit_environment_launch`;
    `desktop_startup.rs`, `resolve`). The eleventh, `CHIRALITY_APP_DATA`,
    is read only by a development run (`lib.rs`, `build_input`), where it
    selects the environment route by itself. `tauri::is_dev()` is
    `!cfg!(feature = "custom-protocol")` in the pinned Tauri 2.11.1, and
    `build_candidate.py` builds a candidate with `--features custom-protocol`,
    so a candidate is not a development run and does not read it (read in
    the source, not observed); `session_env.py` asks for it regardless.
    On this host all ten were absent on 13
    November (`session_env.py`, against the candidate built from cfc22efd);
    step 1 asks again before every walk and stops on anything but absent.
  - It opens at first-use setup: no setup has been saved for a build with a
    new identifier (read in the App's source: with no configuration from the
    environment and no saved request the launch is "setup-required").
  - The App so started starts no Codex: it starts Codex only when it has a
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
- **The condition of the exception.** Before every walk, the eleven names are
  absent in the login session and in the bundle's own launch environment
  (step 1, `session_env.py`), or the walk is refused. After every run, by
  whatever path it ended, the lane ends what the started files show,
  searches for remaining candidate processes by the executable's file, ends
  what it finds, ends the route's processes that step 10 attributes to the walk
  and reports any it cannot attribute (a walk with an unresolved process has
  not been recovered), reads the launch record's Library comparison (or
  records that the launcher wrote none), and reports the same hour (step 11). A run
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
  - What is permitted under `~/.codex`, as the owner accepted it (see "What
    the route starts"): the launch service executing the window service's
    bundle under `~/.codex/computer-use/`, and the helper's Codex running
    with `~/.codex` as its home. The two conditions below bite on anything
    beyond that.
  - What ends the exception until the owner is asked again, without a further
    word from anyone: evidence that this guarded scenario (the App, and
    anything a walk of it starts, the route's helper and window service
    included) reaches the owner's credentials (App Agent 0's operating rule
    in "What the route starts"), the installed v3 or the keychain, reaches
    `~/.codex` beyond what is permitted above, or sends application or user
    content; or that an agent opened or read anything under `~/.codex` or
    `~/.codex-hub`, signed in, saw a credential's value or answered a macOS
    prompt. Then the walk stops, nothing is retried, the lane tells App Agent
    0, and no walk follows until the owner has answered.
  - What stops walks until App Agent 0 has said: anything else newly learned
    about the route, such as what the helper or the service reads, uses or
    sends short of the above. It is told to App Agent 0 at once; a walk under
    way stops; App Agent 0 decides whether it is a matter for the owner.

## Running a scenario

A scenario is a file of steps and expected states, walked by a script the
operator loads. There are three. Two of them, `signed-out-setup.scenario.json`
and `signed-out-relaunch.scenario.json`, type the project path and confirm
setup, and see the launch after it. They are run only under "The App's own
setup confirmation, and the typed path" below. What follows here is about the
first, `first-use-setup.scenario.json`, "first-use setup without a project,
new settings". It is the opening of the first-use setup page
up to, and not including, the App's own confirmation. Its acts are views and
clicks; nothing is typed, no file or folder is chosen, no confirmation is
answered and no setup is confirmed. The App starts no Codex in it and it needs
no sign-in; a walk of it by this route does start the helper's Codex app-server (see "What the route starts").
These prohibitions are narrower than the governing text on purpose (see "What
governs it"). Its controls (a project choice, two settings choices, "Review
setup", "Change my choices" and two disclosures) are none of the act controls
REQ-009 names, so it makes no synthetic capture and the examination-name
requirement does not arise in it.

**When the page changes, the scenario is run again.** When a merge to main
changes the first-use setup page, or what it shows or when it opens, the
scenario is run again on a candidate built from that main, by a walk under
this method or by the scripted driver once it has passed
(`app/examination/scripted_driver/`), before that change is relied on. The
lane notices such a merge by the files it touches, at least these (the list
is not exclusive): `app/src/FirstUse.tsx`; in `app/src/App.tsx`, the branch
that renders `FirstUseSetup` and decides that setup is required;
`app/src/DailyWorkspace.tsx`, which holds the page's styles;
`app/src/hostReads.ts`, through which the page reads the App's state; in
`app/src-tauri/src/lib.rs`, `host_status` and the `desktop_setup_*`
commands; and `app/src-tauri/src/desktop_startup.rs`, which decides that
setup is required and builds what the page reviews. A merge that touches one
of these is read to decide whether it bears on the page; where it is not
clear, the scenario is run.

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
setup completed nor a person's observation. A pass records the checks on views
returned by the supplier's client; that client is part of the trusted
examination tooling (its limit is stated beside `failure` in `walk.mjs`).

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

**The lane's sample of the service's socket folder.** From App Agent 0's go, the
lane's agent (not the operator) samples, from its own shell, the names and times
in the window service's socket folder once a second, until the walk's result
file exists and fifteen seconds more, or thirty minutes at most. Names and times
only: no file there is opened, read, connected to or removed, and nothing is
written there. The output goes in the walk's evidence folder:

```sh
F="$HOME/Library/Group Containers/2DC432GLL2.com.openai.sky.CUAService/IPC"
end=; stop=$(( $(date +%s) + 1800 ))
while [ "$(date +%s)" -lt "$stop" ]; do
  now=$(date -u +%FT%TZ)
  if out=$(ls -laT "$F" 2>&1); then
    if printf '%s\n' "$out" | grep -q ' computeruse\.sock$'; then seen='LISTED: computeruse.sock present'
    else seen='LISTED: no computeruse.sock among the names'; fi
    printf '%s %s\n%s\n' "$now" "$seen" "$out"
  else
    printf '%s NOT EXAMINED: ls exited %s: %s\n' "$now" "$?" "$out"
  fi
  [ -z "$end" ] && [ -e "<evidence folder>/scenario-result.json" ] && end=$(( $(date +%s) + 15 ))
  [ -n "$end" ] && [ "$(date +%s)" -ge "$end" ] && break
  sleep 1
done > "<evidence folder>/socket-folder-sample.txt"
```

Why this folder: the supplier's client for the service, read where it lies
inside ChatGPT.app (nothing copied into this repository, nothing run), first
tries the service's socket in that folder for a fraction of a second; if
nothing answers, it asks for the service to be started, then tries the socket
again for up to five seconds, connecting and asking for a reply. "Sky Computer
Use native pipe startup failed" is what it reports when those five seconds pass
without an answer. Each sample says one of two things: the folder was listed,
and whether a name `computeruse.sock` was among its entries; or it was NOT
EXAMINED, with the listing's exit status and message. A sample not examined
is not a sample that saw no socket. The sample shows whether the socket was
present at each moment the folder was listed, about a second apart, against
the walk's first call. What
happens between two samples (a socket present for less than a second, for
instance) is not seen, and it cannot show why anything happened.

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

Then the operator checks its runtime and host again and makes its look for
route processes (step 10, "The look"), as the last things before the import;
if either fails, no walk. (Its runtime and host were identified before step
1: step 10, "The operator's node runtime and its host".)

**Two calls.** The import is a call of its own, and the walk's first view
asks with the application alone (`walk.mjs` asks every later view for the
whole window, and still requires each view before any click to come back
whole). This is the form of the views that worked on 13 November, and the
form in which A2's eighth attempt passed. It was adopted while the failures
were unexplained; their cause turned out to be another (see "What the route
starts"), and whether the import and the first view in one block would also
work has not been tried since.

First, in the operator's `js` tool, the import alone, printing the time it
returned:

```js
var sky = (await import('@oai/sky')).sky;
nodeRepl.write(new Date().toISOString());
```

If it throws, the error is kept whole, no walk is made, and the operator ends
what it started (steps 8 and 10), closes the marker and returns. Then the
operator waits until at least ten seconds have passed since the time the
import printed. Then, from the operator's shell, as the last thing before the
walk's call, the record after the import, into the evidence folder:

```sh
{ date -u +%FT%TZ
  lsof -t "<evidence folder>/runtime.marker"
  ps -o pid=,ppid=,lstart=,command= -p <the runtime's number>,<the host's number>
  ps -axo pid=,ppid=,lstart=,command= | grep -F 'CodexCLI.app/Contents/MacOS/codex app-server' | grep -v grep || echo 'no app-server'
  ps -axo pid=,ppid=,lstart=,command= | grep -F 'SkyComputerUseService' | grep -v grep || echo 'no window service'
} > "<evidence folder>/after-import.txt"
```

It holds two things, read differently:

- **The recheck of the operator's identities, which can stop the walk.** As at
  the look: `lsof` names the same one process, and the runtime and the host
  show the same numbers, start times and executables as recorded, with the
  runtime's parent still the host. A change, or an identity that cannot be
  examined (`lsof` naming none or more than one, a process not listed), is no
  walk: the operator ends what it started (steps 8 and 10), closes the marker
  and returns, and it comes to App Agent 0.
- **Whether a helper app-server or a window service exists after the import,
  which is a record and not a refusal.** A helper or a service started by the
  import is what it records; neither stops the walk here.

Its first line is a time at least ten seconds after the time the import
printed, and the operator records both. If the recheck holds, the walk's call
follows at once, in the operator's `js` tool, with the values filled in:

```js
var fs = await import('node:fs');
var walk = await import('file://<repository>/app/examination/standalone/operated/walk.mjs');
var scenario = JSON.parse(fs.readFileSync('<repository>/app/examination/standalone/operated/first-use-setup.scenario.json', 'utf8'));
var report = await walk.run({sky, scenario, app: '<bundle identifier>', home: '<launch folder>/home',
  bundle: '<the bundle, the path of the .app folder>',
  pid: <the App's process number>, watch: '<evidence folder>/watch.json'});
// A scenario with a `type` step also gives project: '<launch folder>/project'.
fs.writeFileSync('<evidence folder>/scenario-result.json', JSON.stringify(report, null, 2));
nodeRepl.write(walk.summary(report));
```

Nothing else changes: no retry inside the walk, no second view after a
failure, the same scenario and acts.

- The loading forms above were tried in a Codex session's node runtime with a
  stand-in for the service: the file imports work, bindings last from one call
  to the next, and `process` does not exist there, which is why the watch file
  does.
- The script refuses, before any call, an application not named by a
  development build's bundle identifier, and a process the watch file does not
  show running, with its executable inside the bundle, within the last three
  seconds. It reads the watch file again before every click, set-value, press
  and view, and after every wait.
  It makes views and clicks, and only where a scenario names them one
  set-value and one press on the App's own setup confirmation ("The App's own
  setup confirmation, and the typed path" below), and nothing else. It clicks only a control a step
  names, found by its words whole: a control whose words merely begin the
  same way is not it, and a control whose words end with an ellipsis is never
  clicked by a click step. The one exception is the control that opens the App's
  own setup confirmation, clicked only by the one sheet step that names it.
- It stops, and says where, if a view holds anything that is not the
  scenario's page. The rule is what a view may hold, not a list of things it
  may not: the view must say it is of the bundle; at the top it holds the
  App's one window and the menu bar and nothing else; directly inside the
  window it holds only what the scenario lists, and nowhere below the window,
  at any depth, a window, sheet, dialog, alert or popover. One kind of alert is
  allowed outside the sheet step: one inside the page's web content (below
  "HTML content") that holds only words, with nothing a person can operate.
  The App writes its refusals that way. Only the page's own content can put
  an element there. An alert holding a control, or any alert outside the web
  content, stops the walk. A sheet, a dialog,
  an alert, a second window, or a kind of thing nobody named, stops it; the one
  exception is the sheet a scenario's one `confirm_sheet` step names, checked
  whole before its one press, and a sheet still there after that press stops
  it and is not pressed again. It also stops
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
- **Whole views, or nothing.** Before any click the script asks for two
  views, one after the other, and both must come back whole. The first asks
  with the application alone; the first view of an application was seen to be
  whole without asking, and it counts only if what it returned is whole. The
  second asks for the whole window, and only it shows that asking is
  honoured. Whether a view is whole is read from what it returned, never from
  how it was asked. If either of them, or any later view, comes back as
  differences, the walk stops there. The result records how each view was
  asked. That view, and the window rebuilt from it, are kept in the result for
  reading; no check is credited from a rebuilt view and no click is made from
  one, because how differences place what they add has not been established.
- The App starts no process in this scenario. If the watch file shows the App
  with a child process, the script stops and the result is a failure. (The
  route's own processes are not the App's children; see "What the route
  starts".)
- A watch file that is missing, cannot be read, is for another process, says
  the process has gone, names an executable outside the bundle, or was last
  written more than three seconds ago is read as the build not running: the
  script refuses before any call, or stops. It is never read as "no child
  process"; a step whose watch file could not be used records its child
  processes as not known.
- `nodeRepl.write` joins what successive calls write without a separator, so
  write the summary once.
- The result file holds every call made and every view's returned text whole,
  with one exception: a view whose reply names another bundle is kept only as
  an error naming that bundle; its returned text is not kept. When a view
  fails, it also holds the failure as messages only, in `view_error`; when a
  click fails, in `click_error`, and the walk stops there, inconclusive, with
  nothing further called (a click that throws has not been shown to have had
  no effect). Each holds where it failed, the error's own message, and each cause the
  error carries, in order and whole (at most eight); the summary prints the
  causes under the line that says where the walk stopped. The causes are
  diagnostic evidence supplied by the supplier's client, not causes
  established independently. Nothing else of the
  error is kept: a message is kept only when it is text, anything else is
  named for what it is, and a part that cannot be read is said to be so.
  What it cannot do: reading an error's message and cause can run code the
  error carries, in the same runtime as the walk. The error comes from the
  supplier's client, which runs there too and could change anything the walk
  holds without throwing at all; so the walk's result rests on that client, as
  every call does, not on how a failure is read.
  The operator adds the times of its own calls and what it saw outside the
  script (a prompt appearing, or the focus leaving the build) to its own
  record.
- Then step 8: end the launch, confirm that neither process remains, and keep
  the launch record with the result.

## The App's own setup confirmation, and the typed path

The owner, 14 November 2026, relayed by the Inter-Project Agent 0, on an agent
pressing the App's own setup confirmation: "yes that's a permissible act and
doesn't loosen the rule." The rule stands: no agent answers a macOS
permission, licence or sign-in prompt. The bounds below are App Agent 0's.

This extends this method with the supplier's own window-service methods,
set-value and click, on the development build's own window. It is not new
native tooling and adds no driver. A walk that uses it runs on a build without
the scripted driver: `launch.py`'s kept-home commands refuse a build carrying
either driver marker.

- **The typed path.** Only the project path is typed, because the alternative
  is the system's folder panel, which no agent operates. The scenario names
  the one field in `typed_fields`, and its one `type` step's value is
  `{project}`. Before any call, the walk refuses:
  - a scenario that types more than once, types anything else, or names a
    second field;
  - a project that is not exactly the launch folder's own `project`, beside
    its `home`: the home must end in `/home` with no empty, `.` or `..` part,
    and the project must be the same path ending in `/project`.

  The walk sets the value once, by the field's element index from the latest
  view. The field must be empty and exactly as the view gives it: the named
  label and the placeholder the scenario names (the App's own, from
  `FirstUse.tsx`), and nothing more. It must come directly after the page's
  label text for it, at the same depth, and be found once. That checks how the
  field is presented, not the page's own tie between the field and its label;
  the view does not show that tie. A field inside an alert, a sheet or a dialog
  is not reached, since any of those stops the walk first. It judges by what the page then does, not by the value the field
  shows.
- **The sheet.** The scenario names one sheet in `sheets`: the control that
  opens it, its title, its three buttons, the button to press, and the
  complete statement. The statement uses the exact locations the page showed
  one step earlier, kept by that step's `capture`. The one `confirm_sheet`
  step does this, in order:
  1. It is not taken if any earlier check failed.
  2. It clicks the opener once, waits, and views.
  3. Before any press, it checks the view, the App's own element tree:
     - the view says it is of the bundle;
     - at the top it holds the one window and the menu bar;
     - directly inside the window it holds what the scenario lists and
       exactly one thing more, a sheet;
     - below the window, at any depth, there is no other window, sheet,
       dialog, alert or popover, the page's own alerts included;
     - directly inside the sheet, and nothing deeper, are exactly the named
       buttons, the named title once, and the statement's text. An image (the
       App's icon) is allowed and recorded. Anything else in the sheet is a
       difference;
     - the statement's text equals the complete statement. Line breaks, in
       whatever form the view gives them (a new element, a new line, or
       written as `\n`), become one space, and each line is trimmed at its
       ends. Nothing else is changed, so every word and every path is
       compared exactly, and nothing may be added.

     So its paths are exactly the locations the page named, and the previous
     step checked that each lies under the App data folder in the home. Any
     of these differences stops the walk, and nothing is pressed.
  4. It reads the watch file again just before the press. If the build is
     not shown running, it stops without pressing.
  5. The App shows the statement whole within 30 lines and 1,500 characters,
     and otherwise a digest of it. For the walk's paths it is whole. A
     statement too long for the captured paths, or a digest, stops the walk.
  6. It presses the named button once, by its index, waits and views. If the
     sheet, or anything else that is not the page, is still there, the walk
     stops and does not press again.
- **What the tree does not show.** The view is the development build's own
  tree. A window of another application, or of the system, over the build is
  not in it, and the walk cannot see one. The operator stops if one appears in
  what the view returns or in the screenshot it refers to, and if anything
  but the build asks for an answer.
- **A walk that sees the next launch.** `launch` makes a new home each time.
  A walk that must see the launch after setup uses one kept folder, with the
  same environment and every network block unchanged:
  - `launch.py keep-make --candidate <candidate folder>` makes it and prints
    its path;
  - `launch.py keep-launch --folder <kept folder> --candidate <candidate
    folder>` launches the App in it, once for each launch, with one numbered
    launch record each. It is refused 12 hours after the folder was made, or
    while a candidate process is running;
  - `launch.py keep-remove --folder <kept folder> --candidate <candidate
    folder>` removes it whole. It first makes keep-launch's checks of the
    candidate (admitted, identified, without the driver's markers, and the one
    the kept record names) and of the folder, and refuses while a candidate
    process is running. It is not refused for age. It empties the folder
    through the handle it holds on the directory the record names, with
    `record/` last. Then it removes the emptied folder by name, if that name
    still names that directory; otherwise it removes nothing at that name and
    refuses. A removal that is interrupted can be run again while
    `record/kept.json` remains. If it was interrupted after that, what is left
    is the folder holding at most what remained of `record/`, and it is
    removed by hand by exact path. Between the last check and the removal by name, another
    process could put an empty directory in the folder's place. That is not
    ruled out, and only an empty directory is at stake.

  `keep-launch` is run through `detached.py`, as `launch` is.
- **The record.** It says that an agent pressed the confirmation, by the
  supplier's click on the sheet's button by element index. The records the App
  writes will say that setup was confirmed. It is development evidence and
  meets no criterion.

## What the calls take

Read in the supplier's own documentation of its window service, and given here
only as far as the steps need it:

- A view takes the application and, optionally, the request for the whole
  window as text on every call.
- A click takes the application and the index of an element from the latest
  view.
- A set-value takes the application, the index of a settable field from the
  latest view, and the value. The walk uses it once at most, in a scenario's
  one `type` step, for the project path.
- The service also has methods that type, press keys, scroll, drag, paste and
  list applications. None is used unless the scenario and App Agent 0's go for
  the walk name the act, and `list_apps` is never used.

## What was observed on 13 November 2026

On a development candidate built from main, in two windows the owner gave:

- The import in step 4 returned the service with its methods.
- No computer-use service was running beforehand. The first view started one,
  through the system's launch service; the supplier's desktop application was
  not running. That it also started a Codex app-server on `~/.codex` is
  inferred (the same route and call; see below), not observed: nobody listed
  processes for it.
- No call reported a macOS prompt.
- A view returned within seconds, with the first-use setup page as about fifty
  elements. Later views, made without `disableDiff`, returned differences.
- Clicks by index worked on a disclosure, a button and a radio button.
- Not yet observed: `disableDiff` (the supplier's guidance says it returns a
  fresh whole view; a walk's second view observes it); any method other
  than a view and a click.
- The launcher on main at that time could not launch on that host, because
  macOS refused a listing of two Library folders it watched. The launches were
  made with those two names removed; the launcher's own change followed.
- Walk A2's first attempt stopped at identification's check: the operator's
  `python3` had no jsonschema. The lane's preparation and the operator's
  shell used different interpreters, so preparation that passes for the lane
  shows nothing about the operator's environment.
- Walk A2's second and third attempts, each by a fresh operator from this
  method alone, reached the walk's first call. Each call failed within about
  five seconds with "Sky Computer Use native pipe startup failed"; nothing was
  clicked (observed). Why is not established. The walk then kept only that
  message and dropped the causes the supplier's client attaches to it; it now
  keeps them (`view_error`).
- Each of those calls started, within the same second, a Codex app-server
  (`codex app-server --listen stdio://` from inside ChatGPT.app, a child of
  the operator's node runtime, which is itself inside ChatGPT.app) and a window
  service (from `~/.codex/computer-use/`, under launchd) (observed). The
  app-servers ran with CODEX_HOME set to `~/.codex` and HOME the real home
  (observed by App Agent 0). They outlived the walks, and App Agent 0 ended
  them. Which files they read, whether they used a credential, and what they
  sent is not established. The two occasions that made no call (A2's first
  attempt and a rehearsal of the shell half) started neither (observed).
- Walk A2's fourth attempt, at 16:45 UTC, by a fresh operator, made no walk:
  it was refused at the runtime check, before the look, the import and any
  call, because its assignment expected the marker's holder to be `node_repl`
  itself. The marker, held open and asked of by `lsof`, named one process: ChatGPT.app's
  `cua_node/bin/node` running a `kernel.js` with a session identifier,
  started at 16:48:29 UTC, whose parent was ChatGPT.app's
  `cua_node/bin/node_repl`, started at 16:46:08 UTC, a child of the
  provider's Codex (observed). The `node_repl` that the second and third
  attempts' records call the operator's node runtime is that parent; nobody
  then looked below it. No service import or computer-use call occurred, and
  no helper or window service remained in the recovery checks (the
  operator's at 16:50:21 UTC and the lane's at 16:52:38 UTC, each kept in
  the walk's evidence; App Agent 0 reported the same from its own shell at
  16:53:40 UTC, a reading not kept in that evidence). The marker's identification and
  its closing worked. The launch, ended from outside, left the Library
  comparison unchanged and no candidate process. No product outcome was
  examined.
- Walk A2's fifth attempt, at 17:18 UTC, by a fresh operator under the
  corrected identification, reached its first view at 17:22:56 UTC, in the
  same block as the import and asking for the whole window. The view failed
  within about five seconds with "Sky Computer Use native pipe startup
  failed", with no cause attached; nothing was clicked (observed). The view
  started a helper app-server whose parent was the recorded host, and a
  window service; the operator ended both by their rules, and none remained
  in the recovery checks (observed). A `computeruse.sock` pathname was listed
  in the service's socket folder at every sample from 17:22:57 to 17:23:17
  UTC and none at the samples before; a pathname does not establish a
  listening, responsive service. The one-minute load near the call was about
  two. Set beside the two calls that worked, from the records only, the
  failing first views differ in two things the operator's `js` tool does:
  the import and the first view in one block, and the first view asking for
  the whole window ("Two calls", under
  "In a window").
- Walk A2's sixth attempt, at 18:13 UTC, was made in that form: the import
  as a call of its own, the first view about fifty seconds later asking with
  the application alone. The import started the helper within the same
  second it returned; the first view started the window service and failed
  within about five seconds with "Sky Computer Use native pipe startup
  failed", with no cause attached; nothing was clicked (observed). The
  operator ended both route processes by their rules.
- Walk A2's seventh attempt, at 18:56 UTC, was made the same way, while the
  owner was asked to watch the screen for a macOS prompt during its call. It
  failed the same way, at the first view (observed). The owner's answer was
  "I wasn't watching then": the observation the call was made for was not
  made, and whether a prompt appears is not known. App Agent 0 then closed
  the route for A2.
- The cause of the native-pipe failures, and the remedy, are under "The
  start-up failure, and its cause" ("What the route starts"). The provider
  check at the go ("At the go") was added after it.
- After the owner's restart of T3 Code, at 20:57 UTC, two helper
  app-servers that Inter-Project's delegates had imported and that
  Inter-Project had ended were still listed, each as an exited entry (state
  `Z`, `<defunct>`) under its delegate's `node_repl`, not yet collected
  (observed). The look matches commands and does not count such an entry,
  and it is not a bar ("At the go"; step 10, "The look"). The eighth
  attempt's own helper was left the same way after the operator ended it
  (observed).
- Walk A2's eighth attempt, at 21:01 UTC, on a candidate built from main
  5fbebec6 and by a fresh operator, passed: every outcome shown, in ten views
  and seven clicks (observed). No prompt was reported to the operator by the
  walk or its tools; nobody watched the screen. The
  provider check found the provider started after its executable's
  modification. The import returned at 21:06:05.959 UTC and the helper
  started within that second, with the host as its parent; the walk's call
  ran from 21:06:45.089 to 21:06:52.773 UTC, and the window service started
  at 21:06:45. The operator ended both by their rules, and the lane's step
  11 found nothing remaining and the Library comparison unchanged. The
  launch record's outcome was "failed", from the termination the method
  sends (step 8). The assignment for that walk carried procedure and
  diagnosis that this method did not then carry; the steps in "A walk, in
  order", the provider check and the operator's return were moved into this
  method after it.
- The lane's sample of the socket folder listed a `computeruse.sock` name at
  every sample of the eighth attempt, from 21:01:34 UTC, before the import
  (observed). A name in that folder does not show that a service is running;
  the process table showed none until the walk's first view.
- Walk A3, at 21:49 UTC, on a candidate built from main 345b56ff (after this
  method's order, provider check and return were added), by a fresh operator
  given only a 41-line assignment of the run's parameters, the role, the
  bounds and how to return, passed: every outcome shown, in ten views and
  seven clicks (observed). The operator asked nothing and reported no
  deviation from this method and no missing guidance; this method and that
  assignment were its only instructions (its own statement). It ended the
  helper and the window service by their rules, and the lane's step 11
  found nothing remaining and the Library comparison unchanged. Both route
  processes read `?E` straight after their signal; the operator did not count
  that as ended and checked again, which this method now says to do. No
  prompt was reported to the operator by the walk or its tools; nobody
  watched the screen.
- A4 was judged by App Agent 0 to be shown by A3, by the first clause of
  the pilot's text for it, which reads: "the unchanged scenario is run by a
  worker who is not its author on a later candidate, meaning one built from a
  descendant of A2's main revision that contains a merged change to the App;
  or a repair on that page is verified by it. No change is manufactured to
  obtain a second candidate." (the pilot's own text, as Inter-Project gave it
  to App Agent 0 on 13 November 2026). Between A2's main and A3's only this
  README differed under `app/examination/standalone`, so the scenario file
  and `walk.mjs` were the ones A2 ran; A3's main held two merged changes to
  the App. Two limits: neither change was to the first-use page, so this
  shows the scenario still passing on a changed App, not the scenario
  catching a change to that page; and the pilot's second clause, a repair on
  that page verified by the scenario, is unexercised. "When the page
  changes, the scenario is run again" ("Running a scenario") is the standing
  rule that follows.
