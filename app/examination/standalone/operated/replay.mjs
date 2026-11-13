#!/usr/bin/env node
// Runs walk.mjs against recorded views instead of a running App: no application, no screen, no service.
//   node replay.mjs <scenario.json> <views.json> [<wrong-state.json>]
// A wrong-state file names replacements to make in the recorded views first, so that the unchanged walk and its
// unchanged checks can be shown rejecting a state that is known to be wrong. Prints the result as JSON; exits 0
// when the verdict is pass, 1 when it is fail, 2 when it is inconclusive or the inputs cannot be used.
import { readFileSync } from 'node:fs';
import { run, summary } from './walk.mjs';

const [scenarioPath, viewsPath, wrongPath] = process.argv.slice(2);
if (!scenarioPath || !viewsPath) {
  console.error('usage: node replay.mjs <scenario.json> <views.json> [<wrong-state.json>]');
  process.exit(2);
}
const scenario = JSON.parse(readFileSync(scenarioPath, 'utf8'));
const recorded = JSON.parse(readFileSync(viewsPath, 'utf8'));
const texts = recorded.views.map(view => view.text);
if (wrongPath) {
  for (const { view, from, to } of JSON.parse(readFileSync(wrongPath, 'utf8')).replace) {
    if (!texts[view].includes(from)) { console.error(`the recorded view ${view} does not hold: ${from}`); process.exit(2); }
    texts[view] = texts[view].replace(from, to);
  }
}
texts.unshift(texts[0], texts[0]);  // the two whole views the walk asks for before any click
let next = 0;
const made = [];
const standIn = {  // every other method of the service is absent here, so a call to one would throw
  async get_app_state(input) {
    made.push(['get_app_state', input]);
    if (next >= texts.length) throw new Error('no recorded view is left');
    return { app: recorded.bundle, screenshot: null, text: texts[next++] };
  },
  async click(input) { made.push(['click', input]); },
};
const running = () => ({ pid: process.pid, running: true, at_ms: Date.now(), executable: recorded.bundle + '/Contents/MacOS/chirality-app-v4', children: [] });  // stands in for watch.py's file
const report = await run({ sky: standIn, scenario, app: recorded.app, home: recorded.home, bundle: recorded.bundle, pid: process.pid, readWatch: running, sleep: async () => {} });
report.replayed = { views: viewsPath, wrong_state: wrongPath ?? null, calls_received: made.length };
console.log(JSON.stringify(report, null, 2));
console.error(summary(report));
// The status is set and the process left to end by itself: exiting at once can cut a long result short in a pipe.
process.exitCode = report.verdict === 'pass' ? 0 : report.verdict === 'fail' ? 1 : 2;
