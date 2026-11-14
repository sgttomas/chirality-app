/**
 * The scenario's one closed form, and its only constructor (DEL-09-02 examination tooling).
 *
 * PR 351 stopped after six readings with two unresolved findings. The first was that a scenario's form was checked only
 * in part, so a malformed scenario could reach an effect or a pass. This module is the boundary that replaces that
 * check. Every consumer of a scenario (the walk in walk.mjs, replay.mjs and record_state.mjs) takes only what
 * validateScenario made. A scenario they are handed in any other way is refused before anything in it is read. The
 * test is membership in a set private to this module, which nothing else can add to. It is not a check a caller must
 * remember to make.
 *
 * parseScenario(text), the one entry, parses a scenario file's text and gives it to validateScenario(raw), which:
 * - first copies raw once into plain data (JSON), so that nothing read later can differ from what was checked;
 * - then refuses the copy unless every part of it is of the form below: unknown keys are refused at every level, and
 *   every value has the type its consumer reads;
 * - then freezes the copy deeply and registers the scenario, and each of its parts in the set of its own kind (a step,
 *   an expectation, a selector, a control, a sheet, a record), never in another's.
 * It never throws. It returns { scenario } or { refusal }.
 */

const VALID_SCENARIOS = new WeakSet();
// The parts, registered BY KIND: each set holds only parts validated as that kind, so a helper that takes one kind
// cannot be given a part of another (the first reading of PR 355, finding 2).
const KINDS = { step: new WeakSet(), expectation: new WeakSet(), selector: new WeakSet(), control: new WeakSet(),
  sheet: new WeakSet(), record: new WeakSet() };
const member = (kind, value) => value !== null && typeof value === 'object' && KINDS[kind].has(value);

/** True only for a scenario validateScenario made. */
export function isValidScenario(value) {
  return value !== null && typeof value === 'object' && VALID_SCENARIOS.has(value);
}

/** True only for an expectation validated as one, in a scenario validateScenario made. */
export const isExpectation = value => member('expectation', value);
/** True only for a sheet validated as one. */
export const isSheet = value => member('sheet', value);
/** True only for a step validated as one. */
const isStep = value => member('step', value);
/** True only for a record validated as one. */
const isRecord = value => member('record', value);
/** True only for a selector (texts_from, up_to) validated as one. */
const isSelector = value => member('selector', value);

// The names a capture may carry: the three paths the App makes and the sheet's statement names. They are disjoint
// from every value the walk supplies (walk.mjs, SUPPLIED_NAMES), which the walk also checks before any call.
export const CAPTURE_NAMES = ['settings', 'account', 'request'];
// What a capture form may be filled from: the values the walk supplies for the launch, and the App's own {~uuid}.
const FORM_NAMES = ['identifier', 'home', 'app_data', 'project', '~uuid'];

const ID = /^[A-Za-z0-9_-]{1,40}$/;
const ACTS = ['view', 'click', 'type', 'confirm_sheet'];
// The kinds of control each act may name, as select() in walk.mjs finds them.
const CLICKED = ['button', 'summary', 'radio'];
// The kinds a selector inside an expectation may name (texts_from, up_to).
const SELECTED = ['button', 'summary', 'radio', 'heading', 'text', 'text field'];
// Each expectation's kind, and its companions with their types. Every expectation holds exactly one kind and exactly
// its companions.
const EXPECTATIONS = {
  text: {},
  no_text: {},
  text_starts: {},
  heading: {},
  button: { is: ['available', 'unavailable', 'absent'] },
  summary: { is: ['on', 'off', 'absent'] },
  radio: { is: ['chosen', 'not chosen', 'absent'] },
  texts_from: { up_to: 'selector', are: 'strings' },
  location: { under: 'string' },
};
const SELECTOR_VALUED = ['texts_from'];

const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const isString = value => typeof value === 'string';
const isStrings = (value, nonEmpty = false) => Array.isArray(value) && (!nonEmpty || value.length > 0) && value.every(isString);
const isWait = value => typeof value === 'number' && Number.isFinite(value) && value >= 0;
const has = (object, key) => Object.prototype.hasOwnProperty.call(object, key);

/** The first key outside the form, or a required key missing, as a refusal; or null. */
function keysProblem(object, required, optional, where) {
  for (const key of required) if (!has(object, key)) return `${where} has no ${key}`;
  for (const key of Object.keys(object)) {
    if (!required.includes(key) && !optional.includes(key)) return `${where} holds ${JSON.stringify(key)}, which is not part of its form`;
  }
  return null;
}

function selectorProblem(selector, where) {
  if (!isObject(selector)) return `${where} is not a selector object`;
  const keys = keysProblem(selector, ['kind', 'label'], selector.kind === 'text field' ? ['placeholder'] : [], where);
  if (keys) return keys;
  if (!SELECTED.includes(selector.kind)) return `${where}'s kind is not one a selector names`;
  if (!isString(selector.label)) return `${where}'s label is not text`;
  if (has(selector, 'placeholder') && !isString(selector.placeholder)) return `${where}'s placeholder is not text`;
  return null;
}

function expectationProblem(expectation, where) {
  if (!isObject(expectation)) return `${where} is not an object`;
  const kinds = Object.keys(expectation).filter(key => has(EXPECTATIONS, key));
  if (kinds.length !== 1) return `${where} does not hold exactly one kind of expectation`;
  const [kind] = kinds;
  const companions = EXPECTATIONS[kind];
  const keys = keysProblem(expectation, [kind, ...Object.keys(companions)], [], where);
  if (keys) return keys;
  if (SELECTOR_VALUED.includes(kind)) {
    const problem = selectorProblem(expectation[kind], `${where}'s ${kind}`);
    if (problem) return problem;
  } else if (!isString(expectation[kind])) return `${where}'s ${kind} is not text`;
  for (const [name, type] of Object.entries(companions)) {
    const value = expectation[name];
    if (Array.isArray(type) ? !type.includes(value) : type === 'string' ? !isString(value)
      : type === 'strings' ? !isStrings(value) : selectorProblem(value, `${where}'s ${name}`) !== null) {
      return `${where}'s ${name} is not of its form`;
    }
  }
  return null;
}

function recordProblem(record, where) {
  if (!isObject(record)) return `${where} is not an object`;
  const keys = keysProblem(record, ['recorded_on', 'judged'], ['from'], where);
  if (keys) return keys;
  const on = record.recorded_on;
  if (!isObject(on)) return `${where}'s recorded_on is not an object`;
  const onKeys = keysProblem(on, ['candidate_key', 'identifier', 'app_name'], ['candidate_key_from'], `${where}'s recorded_on`);
  if (onKeys) return onKeys;
  if (!Object.values(on).every(isString)) return `${where}'s recorded_on holds a value that is not text`;
  if (has(record, 'from')) {
    const from = record.from;
    if (!isObject(from)) return `${where}'s from is not an object`;
    const fromKeys = keysProblem(from, ['evidence', 'step', 'view_sha256'], [], `${where}'s from`);
    if (fromKeys) return fromKeys;
    if (!(from.evidence === null || isString(from.evidence)) || !isString(from.step) || !isString(from.view_sha256)) return `${where}'s from holds a value of the wrong type`;
  }
  const judged = record.judged;
  if (!isObject(judged)) return `${where}'s judged is not an object`;
  const judgedKeys = keysProblem(judged, ['result'], ['by', 'against', 'expectations'], `${where}'s judged`);
  if (judgedKeys) return judgedKeys;
  for (const key of ['result', 'by', 'against']) if (has(judged, key) && !isString(judged[key])) return `${where}'s judged ${key} is not text`;
  if (has(judged, 'expectations')) {
    if (!Array.isArray(judged.expectations)) return `${where}'s judged expectations are not a list`;
    for (const [n, expectation] of judged.expectations.entries()) {
      const problem = expectationProblem(expectation, `${where}'s judged expectation ${n + 1}`);
      if (problem) return problem;
    }
  }
  return null;
}

function sheetProblem(sheet, where) {
  if (!isObject(sheet)) return `${where} is not an object`;
  const keys = keysProblem(sheet, ['id', 'opener', 'title', 'press', 'view', 'statement'], ['view_recorded', 'statement_form'], where);
  if (keys) return keys;
  if (!isString(sheet.id) || !ID.test(sheet.id)) return `${where}'s id is not of the id form`;
  for (const key of ['opener', 'title', 'press', 'view_recorded', 'statement_form']) if (has(sheet, key) && !isString(sheet[key])) return `${where}'s ${key} is not text`;
  if (!isStrings(sheet.view, true)) return `${where}'s view is not a non-empty list of lines`;
  if (!isStrings(sheet.statement)) return `${where}'s statement is not a list of lines`;
  return null;
}

const STEP_COMMON_REQUIRED = ['id', 'act', 'expect'];
const STEP_COMMON_OPTIONAL = ['says', 'state', 'capture', 'wait_ms'];
const STEP_FORMS = {
  view: { required: [], optional: [] },
  click: { required: ['control', 'from_state'], optional: ['if_offered'] },
  type: { required: ['control', 'from_state', 'value'], optional: [] },
  confirm_sheet: { required: ['control', 'from_state', 'sheet'], optional: ['press', 'sheet_wait_ms'] },
};

function stepProblem(step, where, scenario) {
  if (!isObject(step)) return `${where} is not an object`;
  if (!isString(step.id) || !ID.test(step.id)) return `${where}'s id is not a string of the step id form`;
  if (!ACTS.includes(step.act)) return `${where}'s act is not one the walk makes`;
  const form = STEP_FORMS[step.act];
  const keys = keysProblem(step, [...STEP_COMMON_REQUIRED, ...form.required], [...STEP_COMMON_OPTIONAL, ...form.optional], `${where} (${step.act})`);
  if (keys) return keys;
  if (has(step, 'says') && !isString(step.says)) return `${where}'s says is not text`;
  if (!Array.isArray(step.expect) || !step.expect.length) return `${where} expects nothing`;
  for (const [n, expectation] of step.expect.entries()) {
    const problem = expectationProblem(expectation, `${where}'s expectation ${n + 1}`);
    if (problem) return problem;
  }
  const states = scenario.states ?? {};
  for (const key of ['state', 'from_state']) {
    if (has(step, key) && (!isString(step[key]) || !ID.test(step[key]) || !has(states, step[key]))) return `${where}'s ${key} is not a state the scenario lists`;
  }
  for (const key of ['wait_ms', 'sheet_wait_ms']) if (has(step, key) && !isWait(step[key])) return `${where}'s ${key} is not a non-negative number`;
  if (has(step, 'capture')) {
    if (!isObject(step.capture) || !Object.values(step.capture).every(isString)) return `${where}'s capture is not an object of text`;
    const named = Object.keys(step.capture).find(name => !CAPTURE_NAMES.includes(name));
    if (named !== undefined) return `${where} captures ${JSON.stringify(named)}, which is not one of the names a capture may carry`;
    const forms = scenario.capture_forms ?? {};
    const unformed = Object.keys(step.capture).find(name => !has(forms, name));
    if (unformed !== undefined) return `${where} captures ${JSON.stringify(unformed)}, which has no form in capture_forms`;
  }
  if (step.act === 'view') return null;
  const control = step.control;
  if (!isObject(control)) return `${where}'s control is not an object`;
  if (step.act === 'click') {
    const controlKeys = keysProblem(control, ['kind', 'label'], [], `${where}'s control`);
    if (controlKeys) return controlKeys;
    if (!CLICKED.includes(control.kind) || !isString(control.label)) return `${where}'s control is not a button, summary or radio with text for its label`;
    if (has(step, 'if_offered') && step.if_offered !== true && step.if_offered !== false) return `${where}'s if_offered is not true or false`;
    if (step.if_offered === true && control.kind !== 'button') return `${where} presses a control that is not a button if offered`;
  }
  if (step.act === 'type') {
    const controlKeys = keysProblem(control, ['kind', 'label'], ['placeholder'], `${where}'s control`);
    if (controlKeys) return controlKeys;
    if (control.kind !== 'text field' || !isString(control.label) || (has(control, 'placeholder') && !isString(control.placeholder))) return `${where}'s control is not a text field named by text`;
    if (!(scenario.typed_fields ?? []).includes(control.label)) return `${where} types into a field the scenario does not name in typed_fields`;
    if (step.value !== '{project}') return `${where} types something other than the project path`;
  }
  if (step.act === 'confirm_sheet') {
    const controlKeys = keysProblem(control, ['kind', 'label'], [], `${where}'s control`);
    if (controlKeys) return controlKeys;
    const sheet = (scenario.sheets ?? []).find(candidate => candidate.id === step.sheet);
    if (!isString(step.sheet) || !sheet) return `${where}'s sheet is not one the scenario names`;
    if (control.kind !== 'button' || control.label !== sheet.opener) return `${where}'s control is not the button that opens its sheet`;
    if (has(step, 'press') && step.press !== true && step.press !== false) return `${where}'s press is not true or false`;
  }
  return null;
}

const TOP_REQUIRED = ['scenario', 'version', 'window', 'window_holds', 'steps'];
const TOP_OPTIONAL = ['what_it_is', 'starting_state', 'acts', 'limit', 'states_recorded', 'never_clicked', 'starts_no_process',
  'typed_fields', 'sheets', 'states', 'state_records', 'sheet_records', 'capture_forms', 'outcomes'];

/** Why the plain scenario is not of the closed form, or null. */
function formProblem(scenario) {
  if (!isObject(scenario)) return 'the scenario is not an object';
  const keys = keysProblem(scenario, TOP_REQUIRED, TOP_OPTIONAL, 'the scenario');
  if (keys) return keys;
  if (!isString(scenario.scenario)) return "the scenario's name is not text";
  if (!Number.isInteger(scenario.version) || scenario.version < 1) return "the scenario's version is not a positive whole number";
  if (!isString(scenario.window)) return "the scenario's window is not text";
  if (!isStrings(scenario.window_holds)) return "the scenario's window_holds is not a list of text";
  for (const key of ['what_it_is', 'starting_state', 'acts', 'limit', 'states_recorded']) if (has(scenario, key) && !isString(scenario[key])) return `the scenario's ${key} is not text`;
  if (has(scenario, 'never_clicked') && !isStrings(scenario.never_clicked)) return "the scenario's never_clicked is not a list of text";
  if (has(scenario, 'starts_no_process') && typeof scenario.starts_no_process !== 'boolean') return "the scenario's starts_no_process is not true or false";
  if (has(scenario, 'typed_fields') && (!isStrings(scenario.typed_fields) || scenario.typed_fields.length > 1)) return "the scenario's typed_fields is not a list of at most one field name";
  if (has(scenario, 'sheets')) {
    if (!Array.isArray(scenario.sheets) || scenario.sheets.length > 1) return "the scenario's sheets is not a list of at most one sheet";
    for (const [n, sheet] of scenario.sheets.entries()) {
      const problem = sheetProblem(sheet, `sheet ${n + 1}`);
      if (problem) return problem;
    }
  }
  if (has(scenario, 'states')) {
    if (!isObject(scenario.states)) return "the scenario's states is not an object";
    for (const [id, lines] of Object.entries(scenario.states)) {
      if (!ID.test(id)) return `the state ${JSON.stringify(id)} is not named in the id form`;
      if (!isStrings(lines, true)) return `the state ${id} is not a non-empty list of lines`;
    }
  }
  for (const [key, names] of [['state_records', Object.keys(scenario.states ?? {})], ['sheet_records', (scenario.sheets ?? []).map(sheet => sheet.id)]]) {
    if (!has(scenario, key)) continue;
    if (!isObject(scenario[key])) return `the scenario's ${key} is not an object`;
    for (const [id, record] of Object.entries(scenario[key])) {
      if (!names.includes(id)) return `the scenario's ${key} holds a record for ${JSON.stringify(id)}, which it does not list`;
      const problem = recordProblem(record, `the record of ${id}`);
      if (problem) return problem;
    }
  }
  if (has(scenario, 'capture_forms') && (!isObject(scenario.capture_forms) || !Object.values(scenario.capture_forms).every(isString))) return "the scenario's capture_forms is not an object of text";
  if (has(scenario, 'capture_forms') && Object.keys(scenario.capture_forms).some(name => !CAPTURE_NAMES.includes(name))) return "the scenario's capture_forms names something that is not one of the names a capture may carry";
  // A capture form may be filled only from values the walk supplies (and the {~uuid} the App makes), never from a
  // captured value, so that what a capture is checked against cannot depend on another capture.
  if (has(scenario, 'capture_forms') && Object.values(scenario.capture_forms).some(form => [...form.matchAll(/\{(~?\w+)\}/g)].some(([, name]) => !FORM_NAMES.includes(name)))) return "a capture form names something other than the values the walk supplies";
  const steps = scenario.steps;
  if (!Array.isArray(steps) || !steps.length) return 'its steps are not a non-empty list';
  const seen = new Set();
  for (const [n, step] of steps.entries()) {
    const problem = stepProblem(step, `step ${n + 1}`, scenario);
    if (problem) return problem;
    if (seen.has(step.id)) return `step ${n + 1}'s id repeats an earlier step's`;
    seen.add(step.id);
  }
  if (steps.filter(step => step.act === 'type').length > 1 || steps.filter(step => step.act === 'confirm_sheet').length > 1) {
    return 'the scenario types more than once or presses more than one sheet';
  }
  if (has(scenario, 'outcomes')) {
    if (!isObject(scenario.outcomes)) return "the scenario's outcomes is not an object";
    for (const [name, ids] of Object.entries(scenario.outcomes)) {
      if (!isStrings(ids, true) || ids.some(id => !seen.has(id))) return `the outcome ${JSON.stringify(name)} is not a non-empty list of the scenario's step ids`;
    }
  }
  return null;
}

function freeze(value) {
  if (value === null || typeof value !== 'object') return;
  for (const part of Object.values(value)) freeze(part);
  Object.freeze(value);
}

/** Each part into the set of its own kind, as formProblem validated it, and into no other. */
function registerKinds(scenario) {
  const expectation = item => {
    KINDS.expectation.add(item);
    if (has(item, 'texts_from')) { KINDS.selector.add(item.texts_from); KINDS.selector.add(item.up_to); }
  };
  for (const step of scenario.steps) {
    KINDS.step.add(step);
    step.expect.forEach(expectation);
    if (has(step, 'control')) KINDS.control.add(step.control);
  }
  for (const sheet of scenario.sheets ?? []) KINDS.sheet.add(sheet);
  for (const record of [...Object.values(scenario.state_records ?? {}), ...Object.values(scenario.sheet_records ?? {})]) {
    KINDS.record.add(record);
    (record.judged.expectations ?? []).forEach(expectation);
  }
}

/** The only constructor of a validated scenario. Never throws: { scenario } or { refusal }. */
function validateScenario(raw) {
  let plain;
  try {
    const text = JSON.stringify(raw);
    if (typeof text !== 'string') return { refusal: 'the scenario is not data' };
    plain = JSON.parse(text);
  } catch {
    return { refusal: 'the scenario could not be read as plain data' };
  }
  let problem;
  try {
    problem = formProblem(plain);
  } catch {
    problem = 'the scenario could not be checked';
  }
  if (problem) return { refusal: problem };
  freeze(plain);
  registerKinds(plain);
  VALID_SCENARIOS.add(plain);
  return { scenario: plain };
}

/** A scenario file's text, parsed and validated. Never throws. */
export function parseScenario(text) {
  let raw;
  try {
    raw = JSON.parse(text);
  } catch {
    return { refusal: 'the scenario file is not JSON' };
  }
  return validateScenario(raw);
}
