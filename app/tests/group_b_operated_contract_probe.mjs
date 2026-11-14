// The required cases of the scenario contract (DEL-09-02), run against the real consumers with invented suppliers:
// the walk (walk.mjs run), replay.mjs and record_state.mjs. PR 351 stopped after six readings with two unresolved
// findings: a malformed scenario could reach an effect or a pass, and some thrown values left a run without a verdict
// or a log. Both are kept here as required cases, together with the sixth reader's probes and a sweep over every key of
// every committed scenario's steps. Nothing here starts an application or touches a screen.
//
//   node group_b_operated_contract_probe.mjs <operated folder> <rebound setup scenario.json> <views.json> <committed scenario.json>...
//
// It prints one JSON object of results; the Python test asserts their properties.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const [folder, scenarioPath, viewsPath, ...committed] = process.argv.slice(2);
const walk = await import(pathToFileURL(`${folder}/walk.mjs`).href);
const contract = await import(pathToFileURL(`${folder}/scenario.mjs`).href);
const original = JSON.parse(readFileSync(scenarioPath, 'utf8'));
const recorded = JSON.parse(readFileSync(viewsPath, 'utf8'));
const clone = value => structuredClone(value);
// A scenario through its one entry, as replay, the recorder and the operator give it: as text.
const validate = raw => contract.parseScenario(JSON.stringify(raw));
const EFFECTS = ['set_value', 'ordinary_click', 'summary_click', 'sheet_opener', 'press'];

// An invented supplier fed the recorded views. The effect at position `effect` throws `value` (mode 'throw') or returns
// it (mode 'return'); every supplier use after that is counted as a later call.
function supplier({ effect = -1, mode = '', value } = {}) {
  const texts = [recorded.views[0].text, recorded.views[0].text, ...recorded.views.map(view => view.text)];
  const seen = { uses: 0, later: 0, effects: 0 };
  let next = 0, broken = false;
  const touch = () => { seen.uses += 1; if (broken) seen.later += 1; };
  const act = () => {
    touch();
    if (seen.effects++ === effect) {
      broken = true;
      if (mode === 'throw') throw value;
      return value;
    }
    return undefined;
  };
  const sky = {
    async get_app_state() { touch(); if (next >= texts.length) throw new Error('no view left'); return { app: recorded.bundle, text: texts[next++] }; },
    async click() { return act(); },
    async set_value() { return act(); },
  };
  return { sky, seen };
}

const options = sky => ({ sky, app: recorded.app, home: recorded.home, bundle: recorded.bundle, project: recorded.project, pid: 41001,
  readWatch: () => ({ pid: 41001, running: true, at_ms: Date.now(), executable: `${recorded.bundle}/Contents/MacOS/chirality-app-v4`, children: [] }),
  readIdentification: () => ({ candidate_key: 'invented-key' }), sleep: async () => {} });

// A walk as a consumer makes it: the scenario validated by its only constructor, and the walk given only what that made
// (a refused scenario is given as it is, so that the walk's own refusal is what is seen).
async function walked(raw, given = {}) {
  const made = validate(raw);
  const { sky, seen } = supplier(given);
  let verdict = null, rejected = null, log = null;
  try {
    verdict = await walk.run({ ...options(sky), scenario: made.scenario ?? raw, onLog: delivered => { log = delivered; } });
  } catch (error) {
    rejected = 'the run rejected';
  }
  return { refusal: made.refusal ?? null, verdict, rejected, logged: log !== null, stopped: log?.stopped ?? null, uses: seen.uses, later: seen.later };
}

const results = { baseline: await walked(clone(original)) };

// The sixth reader's malformed scenarios, each a change to the valid setup scenario.
const MALFORMED = {
  duplicate_ids: s => { s.steps[1].id = s.steps[0].id; }, empty_steps: s => { s.steps = []; }, steps_object: s => { s.steps = {}; },
  steps_string: s => { s.steps = 'S1'; }, null_step: s => { s.steps[0] = null; }, array_step: s => { s.steps[0] = []; },
  object_id: s => { s.steps[0].id = { pass: true }; }, empty_id: s => { s.steps[0].id = ''; }, newline_id: s => { s.steps[0].id = 'S1\n'; },
  wrong_act: s => { s.steps[0].act = 'delete'; }, null_act: s => { s.steps[0].act = null; }, null_expect: s => { s.steps[0].expect = null; },
  empty_expect: s => { s.steps[0].expect = []; }, array_expectation: s => { s.steps[0].expect = [[]]; }, null_expectation: s => { s.steps[0].expect = [null]; },
  unknown_expectation: s => { s.steps[0].expect = [{ invented: 'x' }]; },
  wrong_no_text_value: s => { s.steps[4].expect = [{ no_text: { pressed: true } }]; },
  wrong_text_value: s => { s.steps[0].expect = [{ text: { pressed: true } }]; }, wrong_are_list: s => { s.steps[2].expect[1].are = 'wrong'; },
  missing_click_control: s => { delete s.steps[2].control; }, null_control: s => { s.steps[2].control = null; },
  wrong_control_kind: s => { s.steps[2].control.kind = 5; }, wrong_wait: s => { s.steps[0].wait_ms = '1'; }, negative_wait: s => { s.steps[0].wait_ms = -1; },
  null_state_id: s => { s.steps[0].state = null; }, object_state_id: s => { s.steps[0].state = {}; }, capture_array: s => { s.steps[0].capture = []; },
  wrong_capture: s => { s.steps[3].capture = { settings: {} }; }, wrong_capture_forms: s => { s.capture_forms = 5; }, null_root_states: s => { s.states = null; },
  wrong_state_lines: s => { s.states.S5 = {}; }, null_state_records: s => { s.state_records = null; }, wrong_sheets_object: s => { s.sheets = {}; },
  sheets_null_entry: s => { s.sheets = [null]; }, wrong_press_string: s => { s.steps[4].press = 'false'; },
  wrong_if_offered_type: s => { s.steps[2].if_offered = 'true'; }, window_wrong_type: s => { s.window = {}; }, window_holds_object: s => { s.window_holds = {}; },
  window_holds_null_entry: s => { s.window_holds = [null]; }, outcome_empty_list: s => { s.outcomes = { EFFECT: [] }; },
  outcome_wrong_list: s => { s.outcomes = { EFFECT: 'S1' }; }, outcomes_array: s => { s.outcomes = []; }, outcomes_null: s => { s.outcomes = null; },
  metadata_object: s => { s.scenario = { pass: true }; }, unknown_top_key: s => { s.invented = true; }, unknown_step_key: s => { s.steps[0].invented = true; },
  missing_type_value: s => { delete s.steps[1].value; }, missing_sheet: s => { delete s.steps[4].sheet; }, proto_key: s => { s.steps[0] = JSON.parse(`{"__proto__": {"x": 1}, ${JSON.stringify(s.steps[0]).slice(1)}`); },
  press_not_a_boolean_number: s => { s.steps[4].press = 1; }, is_not_of_its_kind: s => { s.steps[0].expect[1].is = 'on'; },
  selector_extra_key: s => { s.steps[2].expect[1].texts_from.invented = 1; }, record_extra_key: s => { s.state_records.S1.invented = 1; },
  record_for_unlisted_state: s => { s.state_records.S9 = clone(s.state_records.S1); }, from_state_unlisted: s => { s.steps[2].from_state = 'S9'; },
  capture_form_names_a_capture: s => { s.capture_forms.request = '{settings}/invented'; },
  capture_named_project: s => { s.steps[3].capture = { ...s.steps[3].capture, project: 'Settings folder' }; },
};
results.malformed = {};
for (const [name, change] of Object.entries(MALFORMED)) {
  const scenario = clone(original);
  change(scenario);
  results.malformed[name] = await walked(scenario);
}

// Roots that are not a scenario object at all, and options that cannot be read.
results.roots = {};
for (const [name, root] of [['null', null], ['undefined', undefined], ['false', false], ['zero', 0], ['string', 'pass'], ['array', []]]) {
  results.roots[name] = await walked(root);
}
results.unreadable_options = {};
for (const [name, given] of [['null', null], ['throwing', new Proxy({}, { get: () => { throw new Error('cannot read'); } })]]) {
  try { results.unreadable_options[name] = { verdict: await walk.run(given) }; } catch { results.unreadable_options[name] = { rejected: true }; }
}

// Every thrown or returned value of any shape, at each of the five effect positions.
const unreadable = { get message() { throw new Error('cannot read message'); } };
const hostile = new Proxy({}, { get: () => { throw new Error('cannot read anything'); }, getPrototypeOf: () => { throw new Error('no prototype'); } });
const VALUES = [['undefined', undefined], ['null', null], ['false', false], ['zero', 0], ['empty_string', ''], ['true', true], ['one', 1], ['text', 'ok'],
  ['object', {}], ['array', []], ['Error', new Error('invented')], ['symbol', Symbol('invented')], ['null_prototype', Object.create(null)],
  ['unreadable_message', unreadable], ['hostile_proxy', hostile], ['bigint', 10n]];
results.throws = {};
for (const mode of ['throw', 'return']) {
  for (const [position, effect] of EFFECTS.entries()) {
    for (const [label, value] of VALUES) {
      if (mode === 'return' && value === undefined) continue;
      results.throws[`${mode}_${effect}_${label}`] = await walked(clone(original), { effect: position, mode, value });
    }
  }
}

// The sweep: every key of every step of every committed scenario that validates, deleted and given a wrong type, a
// truthy string and null, and the same for each key of its control and its expectations.
results.sweep = [];
const SPOILS = [['deleted', undefined], ['a number', 5], ['a truthy string', 'false'], ['null', null]];
for (const path of committed) {
  const scenario = JSON.parse(readFileSync(path, 'utf8'));
  if (validate(scenario).refusal) continue;
  scenario.steps.forEach((step, n) => {
    const targets = [[[], step]];
    if (step.control) targets.push([['control'], step.control]);
    (step.expect ?? []).forEach((expectation, k) => targets.push([['expect', k], expectation]));
    for (const [where, object] of targets) {
      for (const key of Object.keys(object)) {
        for (const [spoil, value] of SPOILS) {
          const changed = clone(scenario);
          let at = changed.steps[n];
          for (const part of where) at = at[part];
          if (value === undefined) delete at[key]; else at[key] = value;
          const made = validate(changed);
          results.sweep.push({ scenario: path.split('/').pop(), step: step.id, key: [...where, key].join('.'), spoil, refusal: made.refusal ?? null });
        }
      }
    }
  });
}

// The walk of every sweep case on the setup scenario that validateScenario accepted: what it gives.
results.sweep_walked = {};
const SETUP_NAME = scenarioPath.split('/').pop().replace(/^rebound-/, '');
for (const row of results.sweep.filter(row => row.refusal === null && row.scenario === SETUP_NAME)) {
  // Rebuild the change on the rebound setup scenario, which the fixture views can pass.
  const changed = clone(original);
  const n = changed.steps.findIndex(step => step.id === row.step);
  const parts = row.key.split('.');
  let at = changed.steps[n];
  for (const part of parts.slice(0, -1)) at = at[part];
  const value = SPOILS.find(([spoil]) => spoil === row.spoil)[1];
  if (value === undefined) delete at[parts.at(-1)]; else at[parts.at(-1)] = value;
  results.sweep_walked[`${row.step}.${row.key} ${row.spoil}`] = await walked(changed);
}

// Consumers cannot be handed a raw scenario: a plain object, a copy of a validated one, an object made with a validated
// one's prototype, and a validated one changed after validation.
const valid = validate(clone(original)).scenario;
const raws = { plain: clone(original), spread_copy: { ...valid }, same_prototype: Object.assign(Object.create(Object.getPrototypeOf(valid)), clone(original)) };
results.raw = {};
for (const [name, raw] of Object.entries(raws)) {
  const { sky, seen } = supplier();
  let verdict = null, log = null;
  try { verdict = await walk.run({ ...options(sky), scenario: raw, onLog: delivered => { log = delivered; } }); } catch { verdict = 'rejected'; }
  results.raw[name] = {
    verdict, uses: seen.uses, stopped: log?.stopped ?? null,
    checkOne: walk.checkOne([], clone(original.steps[4].expect[2]), {}).found,
    sheetCheck: walk.sheetCheck('', clone(original.sheets[0]), {}, 'Chirality App v4 (development invented)').problems,
  };
}
let changedAfter = 'unchanged';
try { valid.steps[4].press = 'false'; } catch { changedAfter = 'refused'; }
results.frozen = { changedAfter, press: valid.steps[4].press ?? null, stillValid: contract.isValidScenario(valid) };

// THE INJECTED OPTIONS, one table (the first reading of PR 355, findings 3 and 4; App Agent 0's change: one adapter):
// each of the five options failing in each way, at its first reading and, where it is read more than once, at a later
// one. Each run must end inconclusive, never reject, deliver its attempt log, and make no supplier call after the
// failure. The walk's clock is its own and no longer injected (App Agent 0: no option without a consumer).
const { mkdtempSync, existsSync } = await import('node:fs');
const { tmpdir } = await import('node:os');
const logFolder = mkdtempSync(`${tmpdir()}/contract-options-`);
const FAILURES = {
  throw: () => () => { throw Object.create(null); },
  reject: () => () => Promise.reject(Object.create(null)),
  then_getter: () => () => ({ get then() { throw new Error('invented'); } }),
  wrong_kind: wrong => () => wrong,
  property_getter: () => () => ({ get pid() { throw new Error('invented'); }, running: true }),
};
const WRONG = { readWatch: 'invented text', readIdentification: 'invented text', sleep: 1, onLog: 'a value' };
const DATA = ['readWatch', 'readIdentification'];
results.options = {};
let runNumber = 0;
for (const name of ['readWatch', 'readIdentification', 'sleep', 'onLog']) {
  for (const [failure, make] of Object.entries(FAILURES)) {
    if (failure === 'property_getter' && !DATA.includes(name)) continue;
    for (const position of [0, 2]) {
      if (position > 0 && ['readIdentification', 'onLog'].includes(name)) continue;  // read once only
      const { sky, seen } = supplier();
      const base = options(sky);
      const real = { readWatch: base.readWatch, readIdentification: base.readIdentification,
        sleep: base.sleep, onLog: () => undefined };
      let reads = 0, usesAtFailure = null, logged = null;
      const failing = make(WRONG[name]);
      const injected = (...args) => {
        if (reads++ === position) { usesAtFailure = seen.uses; return failing(...args); }
        return real[name](...args);
      };
      const attemptLog = `${logFolder}/run-${runNumber++}.json`;
      const given = { ...base, ...real, scenario: validate(clone(original)).scenario, attemptLog, [name]: injected };
      if (name !== 'onLog') given.onLog = log => { logged = log; };
      let verdict = null, rejected = false;
      try { verdict = await walk.run(given); } catch { rejected = true; }
      results.options[`${name} ${failure} at reading ${position}`] = {
        verdict, rejected, failed: usesAtFailure !== null, later: usesAtFailure === null ? null : seen.uses - usesAtFailure,
        logFile: existsSync(attemptLog), logHanded: name === 'onLog' ? null : logged !== null,
        broken: existsSync(attemptLog) ? Boolean(JSON.parse(readFileSync(attemptLog, 'utf8')).broken) : null };
    }
  }
}

// FINALISATION: an asynchronous log is settled before the verdict is returned.
{
  const { sky } = supplier();
  let settled = false;
  const verdict = await walk.run({ ...options(sky), scenario: validate(clone(original)).scenario,
    onLog: async () => { await new Promise(resolve => setTimeout(resolve, 30)); settled = true; } });
  results.log_settles = { verdict, settled_before_return: settled };
}

// THE CAPTURE: the first reader's scenario (a capture named project, its form "{project}") is refused by the form, and
// the walk keeps supplied and captured values apart whatever the names (namesView).
const collision = clone(original);
collision.steps[0].capture = { project: 'Invented captured project' };
collision.capture_forms = { ...(collision.capture_forms ?? {}), project: '{project}' };
results.capture_collision = { refusal: validate(collision).refusal ?? null, walked: await walked(collision) };
// THE PARTS: registration by kind. The first reader's wrong parts (a map validated as states, or as capture forms,
// given as an expectation or a sheet) are refused; each kind's own parts are accepted.
const parted = clone(original);
parted.states.no_text = ['invented-absent'];
for (const key of ['id', 'opener', 'title', 'press', 'view', 'statement']) parted.states[key] = clone(original.sheets[0].view);
const madeParts = validate(parted).scenario;
results.parts = madeParts ? {
  states_as_expectation: walk.checkOne([], madeParts.states, {}).pass,
  capture_forms_as_expectation: walk.checkOne([], madeParts.capture_forms, {}).pass,
  states_as_sheet: walk.sheetCheck('', madeParts.states, {}, 'Chirality App v4 (development invented)').problems,
  own_expectation_accepted: !walk.checkOne([], madeParts.steps[4].expect[2], {}).found.startsWith('not an expectation'),
  own_sheet_accepted: !walk.sheetCheck('', madeParts.sheets[0], {}, 'Chirality App v4 (development invented)').problems.some(p => p.includes('is not a sheet')),
} : { refusal: validate(parted).refusal };

console.log(JSON.stringify(results));
