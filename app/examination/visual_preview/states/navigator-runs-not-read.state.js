// Runs not read: the latest reading of the open project's recorded runs failed, so none is shown as current and the
// host's sentence says so; another listed project, unfolded here, is not open in this running App, so its runs are not
// read and its conversations are not opened from here; the API key home's conversations were not read (its Codex is
// not running); and the records store's registry was read only to its last complete line.
import { selfIssued, pressesAfterMount } from "./_commands.js";
import { stored, launched, project, navigatorAnswer, RUNS_FAILED, LIST_WORDS } from "./_navigator.js";
import { navigatorHost } from "./_navigator-host.js";

pressesAfterMount("navigator-runs-not-read", [doc => doc.querySelector('button[aria-label="Show this project\'s conversations"]')]);

const id = n => `019b2e1${n}-4a6c-7e8f-9a0b-1c2d3e4f5a6${n}`;
const pump = "/Users/example/Projects/pump-station";
const answer = navigatorAnswer([
  launched([stored(id(1), "Define the summary report", 2), stored(id(2), "Soundings check, north basin", 25)], { runsRead: { state: "not-read", reason: RUNS_FAILED, readAt: null, limits: [] } }),
  project(pump, { entries: [stored("019b2d01-1a2b-7c3d-8e4f-5a6b7c8d9e01", "Pump curves for the new duty point", 60 * 26, { projectRoot: pump }),
    stored("019b2d01-1a2b-7c3d-8e4f-5a6b7c8d9e02", "Wet well level settings", 60 * 49, { projectRoot: pump })] }),
], {
  conversations: [{ home: "account", list: LIST_WORDS, readAt: null, state: "read" },
    { home: "api-key", list: LIST_WORDS, readAt: null, state: "not-read", reason: "Codex is not running for this home, so its conversations were not read." }],
  registryLimits: ["The records store's list of project folders ends in an incomplete line, so only the folders before it are listed."],
});

export default {
  title: "Navigator: runs not read (a failed reading, a project not open), a home not read, a registry limit",
  host: navigatorHost(),
  commands: selfIssued({ navigator_read: answer }),
};
