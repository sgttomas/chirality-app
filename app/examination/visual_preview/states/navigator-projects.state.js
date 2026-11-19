// The navigator from its read (navigator_read): several projects with runs. The launched project is open, each of its
// conversations with its latest run in another state (working, an approval waiting, the agent says it is finished,
// ended, a state not known while an operation is in progress, the turn ended in a run left open); two more projects
// the records store lists are folded with their counts, and two conversations belong to no project. A question waits
// on one conversation and an approval on another, as "Waiting on you" counts them.
import { GEN } from "./_shared.js";
import { selfIssued } from "./_commands.js";
import { stored, run, launched, project, navigatorAnswer, RUN_PENDING } from "./_navigator.js";
import { navigatorHost, question, approval, loadedRow } from "./_navigator-host.js";

const id = n => `019b2e1${n}-4a6c-7e8f-9a0b-1c2d3e4f5a6${n}`;
const working = loadedRow(id(1), "Define the summary report", { type: "active", activeFlags: [] });
const entries = [
  stored(id(1), "Define the summary report", 2, { live: "running", open: { kind: "loaded", generation: GEN, threadId: id(1) }, run: run("open"), runCount: 1 }),
  stored(id(6), "Which datum do the soundings use?", 9, { live: "idle" }),
  stored(id(2), "Soundings check, north basin", 25, { live: "idle", run: run("open"), runCount: 3 }),
  stored(id(3), "Draft section 2: depth changes", 70, { live: "idle", run: run("open", { finishedReported: true }), runCount: 1 }),
  stored(id(7), "Survey vessel schedule", 60 * 20, { run: run("open"), runCount: 1 }),
  stored(id(4), "Tide gauge notes", 60 * 30, { run: run("ended"), runCount: 2 }),
  stored(id(5), "Review pack for the port authority", 60 * 50, { live: "unknown", run: run("unknown", { stateReason: RUN_PENDING }), runCount: 1 }),
];
const pump = "/Users/example/Projects/pump-station", depot = "/Users/example/Projects/depot-renewal";
const answer = navigatorAnswer([
  launched(entries),
  project(pump, { entries: [stored("019b2d01-1a2b-7c3d-8e4f-5a6b7c8d9e01", "Pump curves for the new duty point", 60 * 26, { projectRoot: pump }),
    stored("019b2d01-1a2b-7c3d-8e4f-5a6b7c8d9e02", "Wet well level settings", 60 * 49, { projectRoot: pump }),
    stored("019b2d01-1a2b-7c3d-8e4f-5a6b7c8d9e03", null, 60 * 75, { projectRoot: pump, titleSource: "none" })] }),
  project(depot, { entries: [stored("019b2c01-1a2b-7c3d-8e4f-5a6b7c8d9e04", "Roof drainage options", 60 * 24 * 12, { projectRoot: depot })] }),
], { unassigned: [stored("019b2b01-1a2b-7c3d-8e4f-5a6b7c8d9e05", "Unit conversions for flow", 60 * 5, { projectRoot: null, projectSource: "reported-folder" }),
  stored("019b2b01-1a2b-7c3d-8e4f-5a6b7c8d9e06", "Quick question about PDFs", 60 * 30, { projectRoot: null, projectSource: "reported-folder" })] });

export default {
  title: "Navigator: several projects, the open one with runs in each state, a question and an approval waiting",
  host: navigatorHost({ threads: [working], requests: [question(1, id(6)), approval(2, id(2))] }),
  commands: selfIssued({ navigator_read: answer }),
};
