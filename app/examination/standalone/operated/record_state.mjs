#!/usr/bin/env node
/**
 * Make a recorded state from one captured whole view, and only when the scenario's own expectation of that step holds
 * on it (DEL-09-02 examination tooling).
 *
 *   node record_state.mjs <scenario.json> <step id> <scenario-result.json> --bundle <the launched .app> \
 *     --candidate-key <key> --project <path> [--settings <path>] [--account <path>] [--request <path>] [--from <label>]
 *
 * A recorded state is not acceptable merely because it was recorded: a capture shows fidelity, not correctness (the
 * INTERLOCUTOR, on PR 351). So, before it writes anything, the recorder judges the captured view against the step's
 * expectations as the scenario states them, written from the build's source and independently of any capture, using
 * the walk's own recognition and checks. A view that fails its step's stated expectations is a finding, not a new state: when any
 * expectation fails, or the step states none, or the view is not a whole view of the launched build, nothing is
 * written and it exits 2.
 *
 * It prints {state, record}. The state is the view with the values the walk fills made placeholders: the three paths
 * the App made (when given), the project, the App's name and a scroll bar's position. A view that fails its step's
 * STATED expectations is refused; a difference the expectations do not state is caught only by review of the recorded
 * state when it enters the repository. The record is kept beside the
 * state in the scenario (state_records) and says:
 * - recorded_on: the candidate key, the bundle identifier and the App's name of the build it was recorded on. The walk
 *   uses a state or template only when its record is usable for the launch (walk.mjs, recordUsable, through admission);
 * - from: the evidence it was recorded from, the step, and the view's sha256;
 * - judged: what it was compared against (the step's expectations, listed), by what (this tool), and the result.
 *
 * With --sheet <id> it records instead the judgment of the scenario's sheet template from a captured sheet (the
 * step's sheet_view): the sheet must agree, line for line, with the template filled for this build (the walk's own
 * sheetCheck; the template's statement is held equal to the build's source by a test). It writes no new template: it
 * prints {record} for sheet_records, and refuses when any line differs.
 */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { basename } from 'node:path';
import { APP_NAME, DEVELOPMENT_PREFIX, JUDGED, checkOne, recognise, sheetCheck } from './walk.mjs';

const PATH_FLAGS = ['settings', 'account', 'request'];

/**
 * The candidate key the record is bound to: the one in the identification record of the candidate folder that holds
 * the bundle (<candidate>/target/debug/bundle/macos/<name>.app), when it can be read; a key given as well must equal
 * it. Without that record, only a given key, and the record says which.
 */
function candidateKeyOf(bundle, given) {
  const folder = typeof bundle === 'string' ? bundle.replace(/\/target\/debug\/bundle\/macos\/[^/]+\.app$/, '') : '';
  const path = `${folder}/identification/candidate-identification.json`;
  if (folder && folder !== bundle && existsSync(path)) {
    let key = null;
    try { key = JSON.parse(readFileSync(path, 'utf8')).candidate_key; } catch { return { refusal: "the candidate's identification record could not be read" }; }
    if (typeof key !== 'string' || !key) return { refusal: "the candidate's identification record names no candidate key" };
    if (given !== undefined && given !== key) return { refusal: `the candidate key given (${given}) is not the identified candidate's (${key})` };
    return { key, from: 'the identification record of the candidate folder holding the bundle' };
  }
  if (typeof given !== 'string' || !given) return { refusal: 'no candidate key is given, and no identification record holds the bundle' };
  return { key: given, from: 'given; no identification record holds the bundle' };
}

export function recordSheet(scenario, stepId, result, options) {
  const refuse = why => ({ refusal: why });
  const sheet = (scenario?.sheets ?? []).find(candidate => candidate?.id === options.sheet);
  if (!sheet) return refuse(`the scenario has no sheet ${options.sheet}`);
  const captured = (result?.steps ?? []).find(candidate => candidate?.id === stepId);
  const text = captured?.sheet_view;
  if (typeof text !== 'string' || !text) return refuse(`the result holds no sheet captured at step ${stepId}`);
  const { bundle, candidateKey, project } = options;
  const appName = typeof bundle === 'string' && bundle.endsWith('.app') ? basename(bundle, '.app') : null;
  if (!appName || !APP_NAME.test(appName)) return refuse('the launched bundle is not named as a development build is');
  if (typeof result.app !== 'string' || !result.app.startsWith(DEVELOPMENT_PREFIX)) return refuse('the result does not name a development build');
  const keyed = candidateKeyOf(bundle, candidateKey);
  if (keyed.refusal) return refuse(keyed.refusal);
  if (typeof project !== 'string' || !project.startsWith('/')) return refuse('no absolute project path is given');
  const values = { identifier: result.app, home: result.home, app_data: `${result.home}/Library/Application Support/${result.app}`, project };
  for (const name of PATH_FLAGS) if (options[name] !== undefined) values[name] = options[name];
  const checked = sheetCheck(text, sheet, values, appName);
  if (checked.problems.length) return refuse(`the captured sheet does not agree with the template (${checked.problems.join('; ')})`);
  return {
    record: {
      recorded_on: { candidate_key: keyed.key, candidate_key_from: keyed.from, identifier: result.app, app_name: appName },
      from: { evidence: options.from ?? null, step: stepId, view_sha256: createHash('sha256').update(text).digest('hex') },
      judged: {
        by: 'record_state.mjs --sheet, with the walk\'s own sheetCheck',
        against: `the template of sheet ${sheet.id} in the scenario "${scenario.scenario}", its statement held equal to the build's source by a test`,
        result: JUDGED.sheet,
      },
    },
  };
}

export function record(scenario, stepId, result, options) {
  const refuse = why => ({ refusal: why });
  const step = (scenario?.steps ?? []).find(candidate => candidate?.id === stepId);
  if (!step) return refuse(`the scenario has no step ${stepId}`);
  const expectations = step.expect;
  if (!Array.isArray(expectations) || !expectations.length) return refuse(`step ${stepId} states no expectation of its view, so its view cannot be judged`);
  const captured = (result?.steps ?? []).find(candidate => candidate?.id === stepId);
  const text = captured?.returned;
  if (typeof text !== 'string' || !text) return refuse(`the result holds no view returned at step ${stepId}`);
  const { bundle, candidateKey, project } = options;
  const appName = typeof bundle === 'string' && bundle.endsWith('.app') ? basename(bundle, '.app') : null;
  if (!appName || !APP_NAME.test(appName)) return refuse('the launched bundle is not named as a development build is');
  if (typeof result.app !== 'string' || !result.app.startsWith(DEVELOPMENT_PREFIX)) return refuse('the result does not name a development build');
  const keyed = candidateKeyOf(bundle, candidateKey);
  if (keyed.refusal) return refuse(keyed.refusal);
  if (typeof project !== 'string' || !project.startsWith('/')) return refuse('no absolute project path is given');
  const { elements, refusal } = recognise(text, appName);
  if (refusal) return refuse(`the view is not a whole view of the launched build (${refusal})`);
  const home = result.home;
  const values = { identifier: result.app, home, app_data: `${home}/Library/Application Support/${result.app}`, project };
  for (const name of PATH_FLAGS) if (options[name] !== undefined) values[name] = options[name];
  const checks = expectations.map(expectation => checkOne(elements, expectation, values));
  const failed = checks.filter(check => !check.pass);
  if (failed.length) {
    return refuse(`the view does not meet step ${stepId}'s expectations (${JSON.stringify(failed[0].expectation)}: ${failed[0].found}); a view that fails its step's stated expectations is a finding, not a state`);
  }
  // The placeholders: longer paths first, so that a path holding another is replaced whole.
  let state = text;
  const counts = {};
  const sub = (old, placeholder) => {
    counts[placeholder] = state.split(old).length - 1;
    state = state.split(old).join(`{${placeholder}}`);
  };
  for (const name of PATH_FLAGS) if (options[name] !== undefined) sub(options[name], name);
  sub(project, 'project');
  sub(appName, 'app_name');
  state = state.replace(/(scroll bar \(settable, float\)) [0-9]+(?:\.[0-9]+)?$/gm, '$1 {~number}');
  for (const name of PATH_FLAGS) {
    if (options[name] !== undefined && !counts[name]) return refuse(`the path given as ${name} is nowhere in the view`);
  }
  if (!counts.app_name) return refuse("the App's name is nowhere in the view");
  return {
    state: state.split('\n'),
    record: {
      recorded_on: { candidate_key: keyed.key, candidate_key_from: keyed.from, identifier: result.app, app_name: appName },
      from: { evidence: options.from ?? null, step: stepId, view_sha256: createHash('sha256').update(text).digest('hex') },
      judged: {
        by: 'record_state.mjs, with the walk\'s own recognition and checks',
        against: `the expectations of step ${stepId} in the scenario "${scenario.scenario}", written from the build's source and independently of the capture`,
        expectations,
        result: JUDGED.state,
      },
    },
  };
}

function main(argv) {
  const [scenarioPath, stepId, resultPath, ...rest] = argv;
  const options = {};
  for (let n = 0; n < rest.length; n += 2) {
    const flag = rest[n], value = rest[n + 1];
    const name = { '--bundle': 'bundle', '--candidate-key': 'candidateKey', '--project': 'project', '--settings': 'settings',
      '--account': 'account', '--request': 'request', '--from': 'from', '--sheet': 'sheet' }[flag];
    if (!name || value === undefined) {
      process.stderr.write(`unknown or incomplete option: ${flag}\n`);
      return 2;
    }
    options[name] = value;
  }
  if (!scenarioPath || !stepId || !resultPath) {
    process.stderr.write('usage: node record_state.mjs <scenario.json> <step id> <scenario-result.json> --bundle <.app> --candidate-key <key> --project <path> [...]\n');
    return 2;
  }
  const make = options.sheet !== undefined ? recordSheet : record;
  const made = make(JSON.parse(readFileSync(scenarioPath, 'utf8')), stepId, JSON.parse(readFileSync(resultPath, 'utf8')), options);
  if (made.refusal) {
    process.stderr.write(`not recorded: ${made.refusal}\n`);
    return 2;
  }
  process.stdout.write(JSON.stringify(made, null, 2) + '\n');
  return 0;
}

if (import.meta.url === `file://${process.argv[1]}`) process.exitCode = main(process.argv.slice(2));
