import { createHash } from 'node:crypto';
// Walks one scenario file on a running development build and checks each view against the scenario's
// expected states. An operator loads this inside the node runtime's js tool and gives it the supplier's
// window service; replay.mjs gives it a stand-in that returns recorded views. See README.md beside it.
//
// It makes views (get_app_state) and clicks by element index, and, only where a scenario names them, two more: one
// set-value into a field the scenario names in `typed_fields` (the path typed because the alternative is the system's
// folder panel, which no agent operates), and one press on the App's own confirmation sheet the scenario names in
// `sheets`, only when its view equals the recorded view of it. It clicks only controls a scenario step names, found by kind and
// words in the latest view. It never lists applications, types keys, presses a key, scrolls, drags or pastes, and any
// sheet but the one named stops it as before.
//
// What its verdict establishes: that views returned by the service held the expected elements, or did not. It is
// development evidence about a development build. It is not evidence that a person saw or did anything.

export const DEVELOPMENT_PREFIX = 'dev.chirality.app-v4.candidate.';
const ELEMENT = /^([~+]?)(\t*)(\d+) (.*)$/;
const DIFFERENCE = 'The following is a diff from the previous accessibility tree';
const NO_CHANGE = 'There has been no change in the accessibility tree';

// A whole view is recognised line for line, or it is not acted on. Words hold no control character and no line or
// paragraph separator; an index is at most 15 digits with no leading zero, so it reads as one exact number and two
// different texts never name the same number.
const WORDS = '[^\\p{Cc}\\u2028\\u2029]';
const INDEX = '(0|[1-9][0-9]{0,14})';
const ELEMENT_LINE = new RegExp(`^(\\t*)${INDEX} (${WORDS}+)$`, 'u');
const WINDOW_LINE = new RegExp(`^Window: "${WORDS}*", App: ${WORDS}+\\.$`, 'u');
const FOCUSED_LINE = new RegExp(`^The focused UI element is ${INDEX} (${WORDS}+)$`, 'u');
const FURTHER_LINE = new RegExp(`^${WORDS}+$`, 'u');  // a text element's further lines: no tab can begin one
export const UNADDRESSED = 'the view gives the same element index to more than one element, so it cannot be addressed';

/**
 * A whole view as the walk recognises it: {elements: [{index, depth, content}], refusal}. The view is the supplier's
 * window line; then element lines, each perhaps followed by further lines of its own words; then, at most, one blank
 * line and, after it, at most the focused-element line, naming an element of the view. Each element index names one
 * element. Anything else is a refusal, and nothing is done from the view.
 */
// The App window's own menu bar, with which every whole view of the App ends (see anchored, below).
const MENU_ITEMS = ['File', 'Edit', 'View', 'Window', 'Help'];
const WAITING = '(0|[1-9][0-9]*)';  // the one free part of the block: a non-negative integer, in plain decimal
// The window line, whole: a title holding no quote, the App's name, and nothing after.
const WINDOW_PARTS = new RegExp(`^Window: "([^"]*)", App: (${WORDS}+)\\.$`, 'u');

export function recognise(text, launchedName) {
  const lines = String(text).split('\n'), elements = [], seen = new Set();
  const refuse = why => ({ elements, refusal: why });
  if (!WINDOW_LINE.test(lines[0])) return refuse("its first line is not the supplier's window line");
  let previous = 'window', last = lines.length - 1;  // last: the view's last line before its blank line, if any
  for (let n = 1; n < lines.length; n++) {
    const line = lines[n], element = ELEMENT_LINE.exec(line);
    if (line === '') {
      last = n - 1;
      const rest = lines.slice(n + 1);
      if (rest.length === 0) break;
      const focused = rest.length === 1 ? FOCUSED_LINE.exec(rest[0]) : null;
      if (!focused) return refuse(`line ${n + 2} is not one the walk recognises after the view's blank line`);
      if (!seen.has(focused[1])) return refuse('the focused-element line names no element of the view');
      // It must repeat that element's own words, as every focused line recorded does, not only its index.
      if (elements.find(element => String(element.index) === focused[1])?.content !== focused[2]) {
        return refuse("the focused-element line does not repeat its element's words");
      }
      break;
    }
    if (element) {
      if (seen.has(element[2])) return refuse(UNADDRESSED);
      seen.add(element[2]);
      elements.push({ index: Number(element[2]), depth: element[1].length, content: element[3] });
      previous = 'element';
    } else if (previous !== 'window' && FURTHER_LINE.test(line)) {
      previous = 'further';
    } else {
      return refuse(`line ${n + 1} is not one the walk recognises`);
    }
  }
  return anchored(lines, last, elements, launchedName) ?? { elements, refusal: null };
}

/**
 * The view's shape, which acceptance needs whole (the anchor). Every whole view of the App the supplier has returned
 * (the recorded views of 14 November 2026) ends with the App window's own menu bar: an element "menu bar" at the top
 * level, then exactly the App's name, File, Edit, View, Window, Help and "Waiting requests (n)" one level in, and
 * nothing after them but the blank line and the focused-element line. Page content comes before the window's own
 * controls and that menu bar. So:
 * - the k-th element line must carry index k: a line imitating an element, carried by text inside an element, appears
 *   straight after that element, where it breaks this order or repeats an index;
 * - the view's last eight lines (before its blank line) must equal, line for line and whole, the block built from the
 *   App's name in the window line and the menu bar's index, with only the number in "Waiting requests (n)" free. It is
 *   one comparison, not a check of pieces: an extra line of any kind (a further line, a well-formed element line), a
 *   missing line or an altered line inside the block refuses, and so does a view without the block;
 * - that block's menu bar is the view's only one, and the view's top level is exactly element 0 and that menu bar;
 * - the window line must be whole: `Window: "<title>", App: <name>.`, a title holding no quote, nothing after; <name>
 *   must be exactly the launched build's name (its bundle's, as the walk was given it), and the block is built from it;
 * - so every index the walk may act on is one the view assigns, in order, each once, and an index it does not assign
 *   is refused here, before any call. Refusal is the default: a view lacking any part of this shape is not acted on.
 */
function anchored(lines, last, elements, launchedName) {
  const refuse = why => ({ elements, refusal: why });
  for (let k = 0; k < elements.length; k++) {
    if (elements[k].index !== k) return refuse(`the element lines are not in index order from 0 (element ${k + 1} carries ${elements[k].index})`);
  }
  const windowParts = WINDOW_PARTS.exec(lines[0]);
  if (!windowParts) return refuse('its first line is not a whole window line (a title holding no quote, the App\'s name, nothing after)');
  // The App's name is bound to the build the launcher started (its bundle's name), not only to the line checked: a
  // window line and block that agree with each other but name another App are refused.
  if (typeof launchedName !== 'string' || !launchedName) return refuse("the launched build's name is not given");
  if (windowParts[2] !== launchedName) return refuse("the window line's App is not the launched build");
  const name = launchedName, k = elements.length - 8;
  const block = lines.slice(last - 7, last + 1);
  const expected = [`${k} menu bar`, `\t${k + 1} ${name}`, ...MENU_ITEMS.map((item, i) => `\t${k + 2 + i} ${item}`)];
  const waiting = new RegExp(`^\\t${k + 7} Waiting requests \\(${WAITING}\\)$`);
  if (k < 0 || last - 7 < 1 || block.length !== 8 || expected.some((line, i) => block[i] !== line) || !waiting.test(block[7])) {
    return refuse('it does not end with the App window\'s own menu bar, line for line (menu bar; the window line\'s App name, File, Edit, View, Window, Help, "Waiting requests (n)")');
  }
  // That block is the view's only menu bar, and the view holds nothing else at its top level: exactly two top-level
  // elements, element 0 (the App's window, or a sheet) and the menu bar that begins the block, as every whole view
  // recorded has (35 of 35 on 14 November 2026). A second menu bar, inside the block or anywhere before it, or another
  // top-level element, refuses.
  const top = elements.filter(element => element.depth === 0);
  if (top.length !== 2 || top[0].index !== 0 || top[1].index !== k) return refuse('its top level is not exactly its first element and the menu bar');
  if (elements.filter(element => element.content === 'menu bar').length !== 1) return refuse('it holds more than one menu bar');
  return null;
}

/** The elements of a whole view: [{index, depth, content}] in the order returned (none if it is not recognised). */
export function parseView(text, launchedName) {
  const { elements, refusal } = recognise(text, launchedName);
  return refusal ? [] : elements;
}

/** A view that came back as differences, applied to the elements of the view before it. */
export function applyDifference(previous, text) {
  let elements = previous.map(element => ({ ...element }));
  if (String(text).startsWith(NO_CHANGE)) return elements;
  let pointer = -1;
  for (const line of String(text).split('\n')) {
    if (line.startsWith('Removed element IDs:')) {
      const gone = new Set();
      for (const part of line.slice(line.indexOf(':') + 1).split(',')) {
        const [from, to] = part.trim().split('-').map(Number);
        for (let index = from; index <= (to ?? from); index++) gone.add(index);
      }
      const first = elements.findIndex(element => gone.has(element.index));
      elements = elements.filter(element => !gone.has(element.index));
      if (first >= 0) pointer = first - 1;
      continue;
    }
    const match = ELEMENT.exec(line);
    if (!match || !match[1]) continue;
    const element = { index: Number(match[3]), depth: match[2].length, content: match[4] };
    if (match[1] === '~') {
      const at = elements.findIndex(candidate => candidate.index === element.index);
      if (at < 0) throw new Error(`a changed element is not in the view before it: ${element.index}`);
      elements[at] = element;
      pointer = at;
    } else {
      elements.splice(pointer + 1, 0, element);
      pointer += 1;
    }
  }
  return elements;
}

const fill = (text, values) => String(text).replace(/\{(\w+)\}/g, (whole, name) => (name in values ? values[name] : whole));

/**
 * Every element a selector names. A selector is {kind, label} where kind is button, summary, radio, heading, text,
 * link, or text field (a settable text field; its value and placeholder, after the label, are not part of the label).
 * The label is the control's words whole: a control whose words merely begin with the label is not it.
 */
export function select(elements, selector) {
  const { kind, label } = selector;
  return elements.filter(({ content }) => {
    if (kind === 'button') return content === `button ${label}` || content === `button (disabled) ${label}`;
    if (kind === 'summary') return content === `summary ${label}, Value: on` || content === `summary ${label}, Value: off`;
    if (kind === 'radio') return content === `radio button Value: 0, ${label}` || content === `radio button Value: 1, ${label}`;
    if (kind === 'heading') return content.startsWith(`heading ${label}`) && /^(, Value: \d+)?$/.test(content.slice(`heading ${label}`.length));
    if (kind === 'text') return content === `text ${label}`;
    // An empty settable field, exactly as the view gives it: its label and, when the selector names one, its
    // placeholder, and nothing more. A field that already holds a value is not this one.
    if (kind === 'text field') return content === `text field (settable) ${label}` + (selector.placeholder ? `, Placeholder: ${selector.placeholder}` : '');
    if (kind === 'link') return content === `link ${label}` || content === `link ${label}, Visited`;
    return false;
  });
}

const endsWithEllipsis = words => /(…|\.\.\.)\s*$/.test(words);

// Kinds of element that are a window, or something modal in one. One of them anywhere below the App's window, at any
// depth, is not the page.
const MODAL = /^(sheet|dialog|alert|system dialog|popover|drawer|standard window|floating window|window)(,| |$)/;

/**
 * What in a view is not the scenario's page, or null. The rule is what a view may hold, not a list of things it may
 * not: at the top, the one window the scenario names and the menu bar; directly inside that window, only the
 * entries the scenario lists; and nowhere below it, at any depth, a window, sheet, dialog, alert or popover. Anything
 * else unlisted is not the page.
 */
// What an alert of the page's own may hold: words, and the containers and lists that hold them; nothing a person can
// operate.
const READ_ONLY = /^(text(?! field)|container|group|heading|list marker|content list|list|description list)( |,|$)/;

/**
 * The positions of a view's elements that are a window or something modal. An alert inside the page's own web
 * content (below "HTML content") that holds only words is a region of the page, as the App writes its refusals; it
 * is not counted when `strict` is false. Any other alert (outside the web content, or holding a control), and a
 * sheet, dialog, popover or window anywhere, is modal; with `strict`, every alert is.
 */
function modalAt(elements, from, strict = false) {
  const found = [];
  let web = null;  // the depth of the web content being walked, or null
  for (let at = from; at < elements.length && elements[at].depth > 0; at++) {
    const { depth, content } = elements[at];
    if (web !== null && depth <= web) web = null;
    if (web === null && content.startsWith('HTML content')) { web = depth; continue; }
    if (!MODAL.test(content)) continue;
    if (!strict && web !== null && /^alert(,| |$)/.test(content)) {
      let inside = at + 1;
      while (inside < elements.length && elements[inside].depth > depth && READ_ONLY.test(elements[inside].content)) inside++;
      if (inside >= elements.length || elements[inside].depth <= depth) continue;  // words only: the page's own
    }
    found.push(at);
  }
  return found;
}

export function notThePage(elements, scenario) {
  const title = `standard window ${scenario.window}`;
  const isWindow = ({ content }) => content === title || content.startsWith(title + ', ');
  const top = elements.filter(({ depth }) => depth === 0);
  const other = top.find(element => !isWindow(element) && element.content !== 'menu bar');
  if (other) return `the view holds something beside the window "${scenario.window}" (${other.content})`;
  if (top.filter(isWindow).length !== 1) return `the view is not of exactly one window "${scenario.window}"`;
  const start = elements.findIndex(isWindow);
  for (let at = start + 1; at < elements.length && elements[at].depth > 0; at++) {
    if (elements[at].depth === 1 && !scenario.window_holds.includes(elements[at].content)) {
      return `the window holds something that is not the page (${elements[at].content})`;
    }
  }
  const modal = modalAt(elements, start + 1);
  if (modal.length) return `the window holds something that is not the page (${elements[modal[0]].content})`;
  const underMenu = inMenuBar(elements).find(at => MODAL.test(elements[at].content));
  if (underMenu !== undefined) return `the menu bar holds something that is not the page (${elements[underMenu].content})`;
  return null;
}

/** The positions of every element inside the menu bar, at any depth. */
function inMenuBar(elements) {
  const found = [];
  elements.forEach((element, at) => {
    if (element.depth !== 0 || element.content !== 'menu bar') return;
    for (let inside = at + 1; inside < elements.length && elements[inside].depth > 0; inside++) found.push(inside);
  });
  return found;
}

/**
 * The App's own confirmation sheet against the scenario's recorded view of it, before anything is pressed. The view
 * must equal the template line for line: each element line in its depth and its words, every other line exactly. The
 * template is filled only with the captured paths (through the statement), the sheet's title, and the App's name, which
 * is the candidate bundle's own folder name; the identifier is inside the paths. Element indices are not compared, since
 * a view numbers its elements as it goes; the view is uniquely addressed (view() refuses one that is not), and the
 * press goes to the index the view gives the element in the template's place for the named button. The focused-element
 * line must name, by that mapping, the element the template's names. Anything else is a difference, and nothing is
 * pressed. A view of the same sheet in another shape (another macOS or supplier version) stops the walk until the
 * template is recorded again from a real observation and read again.
 */
export const APP_NAME = /^Chirality App v4 \(development [A-Za-z0-9.-]+\)$/;
const NUMBER = '{~number}';  // in a template's element words: a decimal number (a scroll bar's position) and nothing else

/**
 * A view against a recorded view, line for line: {differs, at}. Each element line must equal the template's in its
 * depth and its words, where the template's only allowance is {~number} for a decimal number; every other line must
 * equal it exactly; the focused-element line must name, by the indices in the same places, the element the
 * template's names. at maps each template index to the view's index for the element in the same place.
 */
export function compareView(wanted, text) {
  const seen = String(text).split('\n');
  const at = new Map();
  const differs = [];
  const sameWords = (template, words) => (template.includes(NUMBER)
    ? new RegExp('^' + template.split(NUMBER).map(part => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('[0-9]+(?:\\.[0-9]+)?') + '$', 'u').test(words)
    : template === words);
  if (seen.length !== wanted.length) differs.push(`the view has ${seen.length} lines and the recorded view ${wanted.length}`);
  for (let n = 0; !differs.length && n < wanted.length; n++) {
    const w = n > 0 && ELEMENT_LINE.exec(wanted[n]), s = n > 0 && ELEMENT_LINE.exec(seen[n]);
    const wf = FOCUSED_LINE.exec(wanted[n]), sf = FOCUSED_LINE.exec(seen[n]);
    if (w) {
      if (!s || s[1] !== w[1] || !sameWords(w[3], s[3])) differs.push(`line ${n + 1} is not the recorded view's`);
      else at.set(Number(w[2]), Number(s[2]));
    } else if (wf) {
      if (!sf || sf[2] !== wf[2] || !at.has(Number(wf[1])) || Number(sf[1]) !== at.get(Number(wf[1]))) differs.push(`line ${n + 1}, the focused element, is not the recorded view's`);
    } else if (seen[n] !== wanted[n]) {
      differs.push(`line ${n + 1} is not the recorded view's`);
    }
  }
  return { differs, at };
}

/** Whether a view is the listed state the scenario names, filled with the run's values: the reasons it is not. */
export function stateCheck(text, lines, values, appName) {
  if (!APP_NAME.test(appName)) return [`the candidate bundle's name is not of the development build's form: ${JSON.stringify(appName)}`];
  if (!Array.isArray(lines) || !lines.length) return ['the scenario gives no recorded view of this state'];
  const wanted = fill(lines.join('\n'), { ...values, app_name: appName }).split('\n');
  if (wanted.some(line => /\{\w+\}/.test(line))) return ['the recorded view names a value this walk does not have'];
  const template = recognise(wanted.join('\n'), appName);
  if (template.refusal) return [`the recorded view, filled, is not a view the walk recognises (${template.refusal})`];
  return compareView(wanted, text).differs;
}

/**
 * Whether a record (of a recorded state, kind 'state', in state_records; or of the sheet template, kind 'sheet', in
 * sheet_records) may be used on this launch. It must have been judged before it was recorded (judged.result), and it
 * must be for this build: the record's candidate key must be the candidate key of the identified candidate this
 * launch's bundle belongs to, and its bundle identifier and App name this launch's. The candidate key is the revision
 * and the first 12 hex digits of the bundle tree's sha256 (candidate_identity/identify.py); the launcher checks the
 * bundle's bytes against that identification before it launches, and the method keeps the bundle unchanged from then.
 * Returns null when it may be used, or why not. It is used only by admission, below.
 */
export const JUDGED = { state: 'every expectation held', sheet: 'every line agreed with the template' };
export function recordUsable(scenario, kind, id, app, appName, candidateKey) {
  const records = kind === 'state' ? scenario?.state_records : kind === 'sheet' ? scenario?.sheet_records : undefined;
  const what = kind === 'sheet' ? `sheet template ${id}` : `recorded state ${id}`;
  const record = records?.[id];
  if (!record?.recorded_on) return `the ${what} has no record of the build it was recorded on`;
  if (typeof candidateKey !== 'string' || !candidateKey) return `the candidate this launch's bundle belongs to is not identified, so no ${what} can be used`;
  if (record.recorded_on.candidate_key !== candidateKey || record.recorded_on.identifier !== app || record.recorded_on.app_name !== appName) {
    return `the ${what} was recorded on another build (${record.recorded_on.candidate_key}, ${record.recorded_on.app_name})`;
  }
  if (record.judged?.result !== JUDGED[kind]) return `the ${what} was not judged before it was recorded`;
  return null;
}

/**
 * The one admission. What a step's verdict, an act and the press rest on is admitted here and nowhere else: the record
 * of the state or template is judged and usable for this launch (recordUsable), and the view equals what it names line
 * for line (stateCheck for a state, sheetCheck for the sheet). Returns {admitted: true} (and, for the sheet, the press
 * index and the comparison record), or {admitted: false, unusable or difference}.
 */
export function admission(scenario, kind, id, text, values, app, appName, candidateKey) {
  const unusable = recordUsable(scenario, kind, id, app, appName, candidateKey);
  if (unusable) return { admitted: false, unusable };
  if (kind === 'state') {
    const differs = Array.isArray(scenario.states?.[id]) ? stateCheck(text, scenario.states[id], values, appName) : [`the scenario holds no recorded state ${id}`];
    return differs.length ? { admitted: false, difference: differs[0] } : { admitted: true };
  }
  const sheet = (scenario.sheets ?? []).find(candidate => candidate?.id === id);
  const checked = sheet ? sheetCheck(text, sheet, values, appName) : { problems: [`the scenario names no sheet ${id}`], record: {} };
  if (checked.problems.length) return { admitted: false, difference: checked.problems.join('; '), first_difference: checked.record.first_difference ?? null };
  return { admitted: true, press: checked.press, record: checked.record };
}

export function sheetCheck(text, sheet, values, appName) {
  const problems = [], record = { compared_with: 'the recorded view of the sheet' };
  // The name guards against a mistaken build: it must be of the development build's form before the template is made.
  if (!APP_NAME.test(appName)) {
    problems.push(`the candidate bundle's name is not of the development build's form: ${JSON.stringify(appName)}`);
    return { problems, record, press: null };
  }
  const statement = (sheet.statement ?? []).map(line => fill(line, values)).join('\n');
  record.statement_wanted = statement;
  // The App shows the statement whole only within 30 lines and 1,500 characters; beyond that it shows a digest.
  if (statement.split('\n').length > 30 || [...statement].length > 1500) problems.push('for these paths the statement is longer than the App shows whole');
  if (!Array.isArray(sheet.view) || !sheet.view.length) {
    problems.push('the scenario gives no recorded view of the sheet');
    return { problems, record, press: null };
  }
  const wanted = fill(sheet.view.join('\n'), { ...values, title: sheet.title, statement, app_name: appName }).split('\n');
  // The filled template must itself be a recognised view whose indices each name one element.
  const template = recognise(wanted.join('\n'), appName);
  if (template.refusal) {
    problems.push(`the recorded view, filled, is not a view the walk recognises (${template.refusal})`);
    return { problems, record, press: null };
  }
  const { differs, at } = compareView(wanted, text);
  problems.push(...differs);
  record.first_difference = differs[0] ?? null;
  const named = wanted.slice(1).map(line => ELEMENT_LINE.exec(line)).filter(m => m && m[3].startsWith(`button ${sheet.press}, ID: `));
  if (named.length !== 1) problems.push(`the recorded view holds the button to press, "${sheet.press}", ${named.length} times`);
  const press = named.length === 1 && !differs.length ? at.get(Number(named[0][2])) : null;
  if (!problems.length && !Number.isInteger(press)) problems.push('the button to press has no index in the view');
  return { problems, record, press: problems.length ? null : press };
}

/** One expectation against one view's elements: {expectation, pass, found}. */
export function checkOne(elements, expectation, values) {
  const result = (pass, found) => ({ expectation, pass, found });
  const one = (kind, label) => select(elements, { kind, label: fill(label, values) });
  const count = found => (found.length === 1 ? 'present' : found.length ? `present ${found.length} times` : 'absent');
  if ('text' in expectation) {  // exactly once in the view
    const found = one('text', expectation.text);
    return result(found.length === 1, count(found));
  }
  if ('no_text' in expectation) {
    const found = one('text', expectation.no_text);
    return result(found.length === 0, found.length ? 'present' : 'absent');
  }
  if ('text_starts' in expectation) {
    const start = 'text ' + fill(expectation.text_starts, values);
    const found = elements.filter(({ content }) => content.startsWith(start));
    return result(found.length === 1, found.length === 1 ? found[0].content.slice(5) : count(found));
  }
  if ('heading' in expectation) {
    const found = one('heading', expectation.heading);
    return result(found.length === 1, found.length ? 'present' : 'absent');
  }
  if ('button' in expectation) {
    const found = one('button', expectation.button);
    const state = found.length === 0 ? 'absent' : found.length > 1 ? 'more than one'
      : found[0].content.startsWith('button (disabled) ') ? 'unavailable' : 'available';
    return result(state === expectation.is, state);
  }
  if ('summary' in expectation) {
    const found = one('summary', expectation.summary);
    const state = found.length === 1 ? found[0].content.slice(found[0].content.lastIndexOf('Value: ') + 7) : found.length ? 'more than one' : 'absent';
    return result(state === expectation.is, state);
  }
  if ('radio' in expectation) {
    const found = one('radio', expectation.radio);
    const state = found.length === 1 ? (found[0].content.startsWith('radio button Value: 1, ') ? 'chosen' : 'not chosen') : found.length ? 'more than one' : 'absent';
    return result(state === expectation.is, state);
  }
  if ('texts_from' in expectation) {  // every text element from one element up to another, in order, and no other
    const from = select(elements, expectation.texts_from), to = select(elements, expectation.up_to);
    if (from.length !== 1 || to.length !== 1) return result(false, `the bounds were found ${from.length} and ${to.length} times`);
    const first = elements.indexOf(from[0]), last = elements.indexOf(to[0]);
    const texts = elements.slice(first + 1, last).filter(({ content }) => content.startsWith('text ')).map(({ content }) => content.slice(5));
    const wanted = expectation.are.map(text => fill(text, values));
    return result(first < last && JSON.stringify(texts) === JSON.stringify(wanted), texts);
  }
  if ('location' in expectation) {  // a named location whose path, the next element, lies under a folder
    const named = elements.filter(({ content }) => content === `text ${expectation.location}`);
    if (named.length !== 1) return result(false, `the name is ${count(named)}`);
    const at = elements.indexOf(named[0]);
    const next = elements[at + 1];
    const path = next && next.content.startsWith('text /') ? next.content.slice(5) : null;
    const under = fill(expectation.under, values);
    return result(path !== null && path.startsWith(under + '/') && !path.split('/').includes('..'), path ?? 'absent');
  }
  return result(false, 'an expectation of a kind this script does not know');
}

/**
 * Walk the scenario. Options:
 *   sky       the supplier's window service (or a stand-in with get_app_state, click and, for a scenario that types,
 *             set_value)
 *   scenario  the parsed scenario file
 *   app       the development build's bundle identifier
 *   home      the throwaway home the launcher made for this launch (launch folder + /home)
 *   bundle    the candidate's bundle, the path of its .app folder: the watched process's executable must be inside
 *             it, and every view must be of it
 *   pid       the running App's process number, confirmed from the shell
 *   watch     the path of the file watch.py keeps while that process runs; the walk reads it before the first view
 *             and at every step, since the node runtime cannot ask the system about a process itself
 *   readWatch optional: () => the parsed watch file, or null (default: reads `watch`)
 *   attemptLog optional: a file path; the attempt log (not a result) is written there when the walk ends
 *   onLog     optional: (log) => anything; given the attempt log when the walk ends
 *   readIdentification optional: () => the candidate's identification record, or null (default: reads
 *             identification/candidate-identification.json in the candidate folder that holds the bundle,
 *             <candidate>/target/debug/bundle/macos/<name>.app). Its candidate_key binds the records used.
 *   sleep     optional: (milliseconds) => a promise (default: a timer)
 *   now       optional: () => the time as text (default: the UTC time)
 *   project   the invented project folder beside the home, for a scenario with a `type` step: the one value it types
 * Returns the walk's one result, its verdict (verdictAt): one of SCENARIO_VERDICTS, derived by position over the
 * scenario's required steps. The attempt log (ATTEMPT_LOG_NOTE), which is not a result, goes to attemptLog and onLog:
 * the calls, each step's attempts and their returns, the views captured, where the walk stopped, and any failure's
 * message and causes. A scenario that is not well formed is refused before any call, "inconclusive".
 */
/**
 * A failed call, as messages only: the error's own message and then each cause it carries, in order, whole. A message
 * is kept only when it is a string; a thrown string or other primitive is kept as its text; anything else is named
 * for what it is. At most eight causes; a cause seen before ends the chain. An exception raised while reading the
 * error is caught and the part said to be unreadable.
 *
 * What it cannot do: reading an error's message and cause can run code the error carries (a getter, a Proxy), and
 * that code runs in this runtime. The error comes from the supplier's client, which runs in the same runtime as the
 * walk and could change anything the walk holds without throwing at all; so the walk's verdict rests on that client,
 * as every call does, and not on how a failure is read. Nothing here defends against it.
 */
export function readFailure(where, error) {
  try {
    return failure(where, error);
  } catch {
    return { where, message: '(the failure could not be read)', causes: [] };
  }
}

export function failure(where, error) {
  const text = value => {
    try {
      if (value === null || (typeof value !== 'object' && typeof value !== 'function')) return String(value);
      const message = value.message;
      return typeof message === 'string' ? message : '(a thrown object with no message text)';
    } catch {
      return '(a thrown value that could not be read)';
    }
  };
  const causes = [];
  const seen = new Set([error]);
  let current = error;
  while (causes.length < 8) {
    let cause;
    try {
      if (current === null || (typeof current !== 'object' && typeof current !== 'function')) break;
      cause = current.cause;
    } catch {
      causes.push('(a cause that could not be read)');
      break;
    }
    if (cause == null || seen.has(cause)) break;
    seen.add(cause);
    causes.push(text(cause));
    current = cause;
  }
  return { where, message: text(error), causes };
}

export async function run({ sky, scenario, app, home, bundle, pid, watch, readWatch, readIdentification, sleep, now, project, attemptLog, onLog }) {
  const logFile = typeof attemptLog === 'string' ? (await import('node:fs')) : null;
  if (!readWatch && typeof watch === 'string') {
    const fs = await import('node:fs');
    readWatch = () => { try { return JSON.parse(fs.readFileSync(watch, 'utf8')); } catch { return null; } };
  }
  if (!readIdentification && typeof bundle === 'string' && /\/target\/debug\/bundle\/macos\/[^/]+\.app$/.test(bundle)) {
    const fs = await import('node:fs');
    const candidate = bundle.replace(/\/target\/debug\/bundle\/macos\/[^/]+\.app$/, '');
    readIdentification = () => { try { return JSON.parse(fs.readFileSync(`${candidate}/identification/candidate-identification.json`, 'utf8')); } catch { return null; } };
  }
  const identified = readIdentification ? readIdentification() : null;
  const candidateKey = typeof identified?.candidate_key === 'string' && /^[A-Za-z0-9-]+$/.test(identified.candidate_key) ? identified.candidate_key : null;
  // The build is running when the watch file is for this process, says so, names an executable inside the bundle, and
  // was written in the last three seconds. That is a sample, not custody: see README.md.
  const watched = () => {
    const seen = readWatch ? readWatch() : null;
    const running = !!seen && seen.pid === pid && seen.running === true && typeof seen.executable === 'string'
      && seen.executable.startsWith(bundle + '/Contents/MacOS/') && Math.abs(Date.now() - seen.at_ms) <= 3000
      && Array.isArray(seen.children);
    return { running, children: running ? seen.children : [] };
  };
  // Every reading of the watch file is made through this one gate, and every one of them decides: the build gone
  // stops the walk, and a child process, in a scenario that starts none, stops it and fails it. A reading is never
  // taken and then set aside. Returns the finished report, or null to go on.
  let lastChildren = null;  // the number of child processes the latest reading showed, as it showed them
  const gate = where => {
    const seen = watched();
    lastChildren = seen.running ? seen.children.length : null;
    if (!seen.running) return finish('inconclusive', `stopped ${where}: the watch file no longer shows the build running`);
    if (scenario.starts_no_process && seen.children.length) {
      return finish('fail', `stopped ${where}: the App has a child process (${seen.children.length}), and this scenario starts none`);
    }
    return null;
  };
  sleep ??= milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
  now ??= () => new Date().toISOString();
  const values = { identifier: app, home, app_data: `${home}/Library/Application Support/${app}`, ...(project ? { project } : {}) };
  const calls = [];
  // The attempt log: everything the walk did and saw, which is not a result (ATTEMPT_LOG_NOTE). The walk's one result,
  // its verdict, is made only by verdictAt, from the steps' judgments by position, when the walk ends.
  const report = { note: ATTEMPT_LOG_NOTE, scenario: scenario.scenario, version: scenario.version, app, home, started: now(), steps: [], calls, stopped: null };
  // The steps' judgments by position, kept apart from the attempt log: only verdictAt reads them.
  const marks = [];
  // Every return of the walk is its verdict alone. The attempt log goes apart: to the attemptLog file and to onLog.
  const finish = (verdict, stopped = null) => {
    report.stopped = stopped;
    report.finished = now();
    const result = verdictAt(scenario, marks, verdict);
    if (logFile) logFile.writeFileSync(attemptLog, JSON.stringify(report, null, 2) + '\n');
    if (typeof onLog === 'function') onLog(report);
    return result;
  };
  // Refusals before any call. First, the scenario's shape: a scenario that is not well formed is refused whole.
  const malformed = scenarioProblem(scenario);
  if (malformed) return finish('inconclusive', `refused before any call: the scenario is not well formed (${malformed})`);
  if (typeof app !== 'string' || !app.startsWith(DEVELOPMENT_PREFIX) || !/^[A-Za-z0-9.-]+$/.test(app)) {
    return finish('inconclusive', 'refused before any call: the application is not named by a development build\'s bundle identifier');
  }
  if (typeof home !== 'string' || !home.startsWith('/') || home.endsWith('/')) {
    return finish('inconclusive', 'refused before any call: the home is not an absolute path');
  }
  if (typeof bundle !== 'string' || !bundle.startsWith('/') || !bundle.endsWith('.app')) {
    return finish('inconclusive', 'refused before any call: the bundle is not the absolute path of an .app folder');
  }
  const typing = (scenario?.steps ?? []).filter(step => step?.act === 'type');
  const pressing = (scenario?.steps ?? []).filter(step => step?.act === 'confirm_sheet');
  if (typing.length > 1 || pressing.length > 1 || (scenario?.typed_fields ?? []).length > 1 || (scenario?.sheets ?? []).length > 1
      || typing.some(step => step.value !== '{project}')) {
    return finish('inconclusive', 'refused before any call: a scenario types once at most, the project path into one named field, and presses one named sheet once at most');
  }
  if (typing.length && (!home.endsWith('/home') || home.split('/').some((part, n) => n > 0 && ['', '.', '..'].includes(part))
      || project !== home.slice(0, -'home'.length) + 'project')) {
    return finish('inconclusive', 'refused before any call: the project to type is not the launch folder\'s own project folder, beside its home');
  }
  const steps = Array.isArray(scenario?.steps) ? scenario.steps : [];
  // The walk acts only in a listed state: every step that acts names the recorded view it acts from, and that view is
  // in the scenario's states (App Agent 0, 14 November 2026).
  const acting = steps.filter(step => ['type', 'click', 'confirm_sheet'].includes(step?.act));
  const unlisted = acting.find(step => !Array.isArray(scenario?.states?.[step.from_state]) || !scenario.states[step.from_state].length);
  if (unlisted) {
    return finish('inconclusive', `refused before any call: step ${unlisted.id} acts, and names no listed state it acts from; the walk acts only in a listed state`);
  }
  // What the views will show that the lane supplies must be plain text: no line break, tab, control character, or
  // line or paragraph separator, so that it can never make a line of its own in a view.
  const supplied = { home, bundle, identifier: app, ...(project ? { project } : {}) };
  const unplain = Object.entries(supplied).find(([, value]) => /[\p{Cc}\u2028\u2029]/u.test(String(value)));
  if (unplain) {
    return finish('inconclusive', `refused before any call: the ${unplain[0]} holds a line break, a tab, a control character or a line or paragraph separator`);
  }
  if (typeof scenario?.window !== 'string' || !Array.isArray(scenario.window_holds) || !steps.length
      || steps.some(step => !Array.isArray(step.expect) || !step.expect.length)
      || Object.values(scenario.outcomes ?? {}).some(ids => !ids.length || ids.some(id => !steps.some(step => step.id === id)))) {
    return finish('inconclusive', 'refused before any call: the scenario names no window and what it holds, has no steps, has a step with nothing expected, or has an outcome naming no such step');
  }
  if (!Number.isInteger(pid) || pid <= 1) {
    return finish('inconclusive', 'refused before any call: the process number is not one');
  }
  // The first reading of the watch, like every other, is the gate's: a view of an application that is not running
  // would start it outside the launcher.
  const atStart = gate('before any call');
  if (atStart) return atStart;
  let elements = [], latest = null;
  const appName = bundle.slice(bundle.lastIndexOf('/') + 1, -'.app'.length);
  // Before any act: the latest view must be the listed state the step acts from, line for line.
  // An effect, in the attempt log, as an attempt and its return, written in two steps round the call: what was sent,
  // then when it returned or what it threw. It is not a result: whether the step held is said only by its verdict.
  const attempt = async (entry, act, element_index, call, extra = {}) => {
    const record = { act, element_index, ...extra, sent_at: now() };
    entry.attempts.push(record);
    // An explicit discriminator, and every caller tests it (ok), never the truthiness of what came back.
    // The supplier's contract (the @oai/sky declarations, types/window/Click.d.ts and SetValue.d.ts): click and
    // set_value each return Promise<void>, and a failure is a rejection. The press is a click. So the one positive
    // success is a call that resolves with no value. Any throw, whatever its value (null, false, 0, '' and undefined
    // included), and any resolve with a value the contract does not give, stops the walk, inconclusive, with the effect
    // uncertain. A call that resolved is not thereby a completed effect: whether the App acted is shown only by the next
    // view, admitted or not.
    try {
      const value = await call();
      if (value !== undefined) {
        record.returned_at = now();
        record.effect = 'uncertain: the call returned a value its contract (Promise<void>) does not give';
        return { ok: false, error: new Error('the supplier returned a value its contract does not give') };
      }
      record.returned_at = now();
      return { ok: true };
    } catch (error) {
      record.threw = String(error?.message ?? error);
      record.effect = 'uncertain: the call threw, and whether it acted is not known';
      return { ok: false, error };
    }
  };
  // Every act (the click, the set-value, the sheet opener) is made only from an admitted view: the latest view admitted
  // against the recorded state the step acts from, by the one admission.
  const notListed = (step, act) => {
    if (latest === null) return finish('inconclusive', `stopped at ${step.id}: the view is not the listed state ${step.from_state} (the latest view was not recognised); nothing was ${act}`);
    const admitted = admission(scenario, 'state', step.from_state, latest, values, app, appName, candidateKey);
    if (admitted.admitted) return null;
    return finish('inconclusive', `stopped at ${step.id}: the view is not the listed state ${step.from_state} (${admitted.unusable ?? admitted.difference}); nothing was ${act}`);
  };
  // A view is whole, or the walk stops there. One that comes back as differences is kept, with the view rebuilt from
  // it, for reading only: no check is credited from a rebuilt view and no click is made from one. Whether a view is
  // whole is read from what it returned, never assumed from what was asked.
  // The first view asks with the application alone, as the calls that worked on 13 November did; every later view
  // asks for the whole window (disableDiff). That the first view's form matters is not established (README.md).
  const view = async ({ plain = false } = {}) => {
    const asked = plain ? { app } : { app, disableDiff: true };
    calls.push({ at: now(), call: 'get_app_state', ...asked });
    const state = await sky.get_app_state(asked);
    if (state?.app !== bundle) throw new Error(`the view does not say it is of the bundle; it names: ${state?.app}`);
    const text = String(state?.text ?? '');
    if (text.startsWith(DIFFERENCE) || text.startsWith(NO_CHANGE)) {
      let rebuilt = null;
      try {
        rebuilt = applyDifference(elements, text).map(({ index, depth, content }) => '\t'.repeat(depth) + index + ' ' + content).join('\n');
      } catch { /* shown as not rebuilt */ }
      return { whole: false, text, rebuilt };
    }
    // The first property of a view the walk acts on, beside being whole: it is recognised line for line, and each
    // element index names one element. A view that is not is kept, and nothing is done from it.
    const recognised = recognise(text, appName);
    elements = recognised.refusal ? [] : recognised.elements;
    latest = recognised.refusal ? null : text;
    return { whole: true, refusal: recognised.refusal, text };
  };
  // What was asked, said truly for each view: the first is a plain view of an identifier not viewed before in this
  // walk; every later view asked for the whole window.
  const unaddressed = (id, refusal) => `stopped at ${id}: ${refusal}; nothing is clicked, typed or pressed from it`;
  const asDifferences = (id, plain = false) => `stopped at ${id}: the view came back as differences although ${plain
    ? 'it was the first view of this build in the walk, asked with the application alone'
    : 'the whole window was asked for'}; nothing is checked or clicked from a rebuilt view`;
  // Before any click: two whole views, one after the other. The first asks with the application alone; the first view
  // of an application was seen to be whole without asking, and it counts only if it came back whole. The second asks
  // for the whole window, and only it shows that asking is honoured. Either coming back as differences stops the walk.
  report.whole_views_before_any_click = [];
  for (const ordinal of ['first', 'second']) {
    const beforeView = gate(`before the ${ordinal} view before any click`);
    if (beforeView) return beforeView;
    let seen;
    try {
      seen = await view({ plain: ordinal === 'first' });
    } catch (error) {
      report.view_error = readFailure(`the ${ordinal} view before any click`, error);
      return finish('inconclusive', `stopped at the ${ordinal} view before any click: the view failed (${report.view_error.message})`);
    }
    report.whole_views_before_any_click.push({ at: now(), whole: seen.whole, returned: seen.text, ...(seen.whole ? {} : { rebuilt_for_reading: seen.rebuilt }) });
    if (!seen.whole) return finish('inconclusive', asDifferences(`the ${ordinal} view before any click`, ordinal === 'first'));
    if (seen.refusal) return finish('inconclusive', unaddressed(`the ${ordinal} view before any click`, seen.refusal));
    const stray = notThePage(elements, scenario);
    if (stray) return finish('inconclusive', `stopped at the ${ordinal} view before any click: ${stray}; no agent answers a prompt or a dialog`);
    const afterView = gate(`after the ${ordinal} view before any click`);
    if (afterView) return afterView;
  }
  for (const step of scenario.steps) {
    // A step's expectations are kept as failures only (unmet), in its judgment by position, which only verdictAt
    // reads. unmet is absent until the step's view has been evaluated.
    const entry = { id: step.id, at: now(), act: step.act, intended: step.says, attempts: [] };
    report.steps.push(entry);
    const mark = { position: marks.length };
    marks.push(mark);
    const before = gate(`at ${step.id}`);
    if (before) return before;
    if (step.act === 'click') {
      if (endsWithEllipsis(step.control.label)) return finish('inconclusive', `stopped at ${step.id}: a control whose words end with an ellipsis is never clicked`);
      const found = select(elements, step.control);
      entry.control = step.control;
      if (found.some(({ content }) => endsWithEllipsis(content))) return finish('inconclusive', `stopped at ${step.id}: the control found has words that end with an ellipsis, and such a control is never clicked`);
      const unlistedClick = notListed(step, 'clicked');
      if (unlistedClick) return unlistedClick;
      // A button the scenario presses only if the App offers it: absent or unavailable, it is recorded as not
      // offered and not pressed, and the step's view and checks are made as for any other step.
      if (step.if_offered === true && step.control.kind !== 'button') return finish('inconclusive', `stopped at ${step.id}: only a button is pressed if offered`);
      // Absent means the words are on nothing at all in the view: words on a control of another kind, or in any other
      // element, stop the walk rather than count as not offered.
      const elsewhere = found.length === 0 && elements.some(({ content }) => content.includes(step.control.label));
      if (step.if_offered === true && elsewhere) return finish('inconclusive', `stopped at ${step.id}: the words of the button to press if offered are on something that is not that button`);
      const notOffered = step.if_offered === true
        && (found.length === 0 || (found.length === 1 && found[0].content.startsWith('button (disabled) ')));
      if (notOffered) entry.not_offered = found.length ? 'unavailable' : 'absent';
      else {
      if (found.length !== 1) return finish(marks.some(s => s.unmet?.length) ? 'fail' : 'inconclusive',
        `stopped at ${step.id}: the control to click was found ${found.length} times in the latest view`);
      if (found[0].content.startsWith('button (disabled) ')) return finish('fail', `stopped at ${step.id}: the control to click is unavailable`);
      calls.push({ at: now(), call: 'click', app, element_index: found[0].index });
      const clickFailed = await attempt(entry, 'click', found[0].index, () => sky.click({ app, element_index: found[0].index }));
      if (!clickFailed.ok) {
        // Kept as a view's failure is, and the walk stops: a click that throws has not been shown to have had no
        // effect, so nothing further is called and the verdict is inconclusive.
        report.click_error = readFailure(step.id, clickFailed.error);
        entry.error = report.click_error.message;
        return finish('inconclusive', `stopped at ${step.id}: the click failed (${entry.error})`);
      }
      if (step.wait_ms) await sleep(step.wait_ms);
      }
      const beforeView = gate(`at ${step.id}, before its view`);  // read again immediately before the view
      if (beforeView) return beforeView;
    } else if (step.act === 'type') {
      // One set-value into one field the scenario names; nothing else is typed in a walk.
      if (step.control?.kind !== 'text field' || !(scenario.typed_fields ?? []).includes(step.control.label)) {
        return finish('inconclusive', `stopped at ${step.id}: the scenario names no such field to type into`);
      }
      const unlistedType = notListed(step, 'typed');
      if (unlistedType) return unlistedType;
      const found = select(elements, step.control);
      entry.control = step.control;
      if (found.length !== 1) return finish('inconclusive', `stopped at ${step.id}: the field was found ${found.length} times in the latest view`);
      // The field is the one the page labels: the element before it in the view is its label's text, alone.
      const label = elements[elements.indexOf(found[0]) - 1];
      if (!label || label.content !== `text ${step.control.label}` || label.depth !== found[0].depth) {
        return finish('inconclusive', `stopped at ${step.id}: the field is not directly after its label "${step.control.label}"`);
      }
      if (report.calls.some(call => call.call === 'set_value')) return finish('inconclusive', `stopped at ${step.id}: a walk sets one value once`);
      const value = fill(step.value, values);
      calls.push({ at: now(), call: 'set_value', app, element_index: found[0].index, value });
      const setFailed = await attempt(entry, 'set_value', found[0].index, () => sky.set_value({ app, element_index: found[0].index, value }), { value });
      if (!setFailed.ok) {
        report.set_value_error = readFailure(step.id, setFailed.error);
        entry.error = report.set_value_error.message;
        return finish('inconclusive', `stopped at ${step.id}: setting the field's value failed (${entry.error})`);
      }
      if (step.wait_ms) await sleep(step.wait_ms);
      const beforeView = gate(`at ${step.id}, before its view`);
      if (beforeView) return beforeView;
    } else if (step.act === 'confirm_sheet') {
      // The App's own confirmation: click the control that opens it, view the sheet and check it whole, press the
      // named button once, and view again. Any difference stops the walk before the press; a press with no visible
      // effect is not pressed again.
      const sheet = (scenario.sheets ?? []).find(named => named.id === step.sheet);
      if (!sheet || step.control?.kind !== 'button' || step.control?.label !== sheet.opener) return finish('inconclusive', `stopped at ${step.id}: the scenario names no such sheet`);
      if (marks.some(earlier => earlier.unmet?.length)) {
        return finish('fail', `stopped at ${step.id}: an earlier check failed, so the sheet is not opened`);
      }
      const unlistedOpener = notListed(step, 'clicked or pressed');
      if (unlistedOpener) return unlistedOpener;
      const opener = select(elements, step.control);
      entry.control = step.control;
      if (opener.length !== 1) return finish('inconclusive', `stopped at ${step.id}: the control that opens the sheet was found ${opener.length} times`);
      if (opener[0].content.startsWith('button (disabled) ')) return finish('fail', `stopped at ${step.id}: the control that opens the sheet is unavailable`);
      calls.push({ at: now(), call: 'click', app, element_index: opener[0].index });
      const openFailed = await attempt(entry, 'click', opener[0].index, () => sky.click({ app, element_index: opener[0].index }));
      if (!openFailed.ok) {
        report.click_error = readFailure(step.id, openFailed.error);
        entry.error = report.click_error.message;
        return finish('inconclusive', `stopped at ${step.id}: the click failed (${entry.error})`);
      }
      await sleep(step.sheet_wait_ms ?? 2000);
      const beforeSheet = gate(`at ${step.id}, before the sheet's view`);
      if (beforeSheet) return beforeSheet;
      let shown;
      try {
        shown = await view();
      } catch (error) {
        report.view_error = readFailure(step.id, error);
        entry.error = report.view_error.message;
        return finish('inconclusive', `stopped at ${step.id}: the sheet's view failed (${entry.error})`);
      }
      entry.sheet_view = shown.text;
      entry.sheet_view_sha256 = sha256(shown.text);
      // A sheet step with "press": false captures the sheet and ends the walk there, whatever the sheet says: it has no
      // press. It records a sheet from a new build before any walk presses it (the setup walk's re-recording).
      if (step.press === false) return finish('inconclusive', `stopped at ${step.id}: the sheet is captured, and this step has no press`);
      if (!shown.whole) return finish('inconclusive', asDifferences(step.id));
      if (shown.refusal) return finish('inconclusive', `${unaddressed(step.id, shown.refusal)}; nothing was pressed`);
      // The press, by the one admission: the sheet template's record judged and usable for this launch, and the sheet
      // equal to it line for line. A refused press leaves only the refusal (and the difference found, if any): never a
      // record that reads as a comparison that agreed.
      const checked = admission(scenario, 'sheet', sheet.id, shown.text, values, app, appName, candidateKey);
      // In the attempt log the sheet is a capture (above) and, when it was not admitted, the difference: whether it
      // agreed is said only by the step's verdict.
      if (checked.unusable) {
        entry.sheet_difference = checked.unusable;
        return finish('inconclusive', `stopped at ${step.id}: ${checked.unusable}; nothing was pressed`);
      }
      if (!checked.admitted) {
        entry.sheet_difference = checked.first_difference ? `${checked.difference} (${checked.first_difference})` : checked.difference;
        return finish('inconclusive', `stopped at ${step.id}: the sheet is not the one named (${checked.difference}); nothing was pressed`);
      }
      entry.sheet_observation = 'the sheet matched the template when it was compared (an observation, not a press)';
      const beforePress = gate(`at ${step.id}, before the press`);
      if (beforePress) return beforePress;
      calls.push({ at: now(), call: 'click', app, element_index: checked.press });
      const pressFailed = await attempt(entry, 'press', checked.press, () => sky.click({ app, element_index: checked.press }), { button: sheet.press });
      if (!pressFailed.ok) {
        report.click_error = readFailure(step.id, pressFailed.error);
        entry.error = report.click_error.message;
        return finish('inconclusive', `stopped at ${step.id}: the press on the sheet failed (${entry.error})`);
      }
      if (step.wait_ms) await sleep(step.wait_ms);
      const afterPress = gate(`at ${step.id}, after the press`);
      if (afterPress) return afterPress;
    } else if (step.act !== 'view') {
      return finish('inconclusive', `stopped at ${step.id}: an act this script does not perform`);
    } else if (step.wait_ms) {
      await sleep(step.wait_ms);
      const afterWait = gate(`at ${step.id}, after its wait`);
      if (afterWait) return afterWait;
    }
    let seen;
    try {
      seen = await view();
    } catch (error) {
      report.view_error = readFailure(step.id, error);
      entry.error = report.view_error.message;
      return finish('inconclusive', `stopped at ${step.id}: the view failed (${entry.error})`);
    }
    entry.returned = seen.text;
    entry.returned_sha256 = sha256(seen.text);
    if (!seen.whole) {
      entry.rebuilt_for_reading = seen.rebuilt;
      return finish('inconclusive', asDifferences(step.id));
    }
    if (seen.refusal) return finish('inconclusive', unaddressed(step.id, seen.refusal));
    const stray = notThePage(elements, scenario);
    if (stray && step.act === 'confirm_sheet') return finish('inconclusive', `stopped at ${step.id}: after the one press, ${stray}; it is not pressed again`);
    if (stray) return finish('inconclusive', `stopped at ${step.id}: ${stray}; no agent answers a prompt or a dialog`);
    // Unmet expectations: in the step's judgment as codes with the condition's own parameters (its index and kind); in
    // the attempt log, what was found.
    const failedChecks = (step.expect ?? []).map((expectation, index) => ({ ...checkOne(elements, expectation, values), index }))
      .filter(check => !check.pass);
    mark.unmet = failedChecks.map(({ expectation, index }) => ({ code: 'expectation-unmet', index, kind: Object.keys(expectation)[0] }));
    if (failedChecks.length) entry.expectations_not_found = failedChecks.map(({ index, expectation, found }) => ({ index, expectation, found }));
    // Paths the scenario captures for a later step (the sheet's statement names them): a named location's path.
    for (const [name, location] of Object.entries(step.capture ?? {})) {
      const named = elements.filter(element => element.content === `text ${location}`);
      const next = named.length === 1 ? elements[elements.indexOf(named[0]) + 1] : null;
      values[name] = next && next.content.startsWith('text /') ? next.content.slice(5) : undefined;
      if (values[name] === undefined) return finish('inconclusive', `stopped at ${step.id}: the location "${location}" could not be read`);
      // The App makes these paths itself: each must be of the form the scenario gives, under the App data folder.
      const form = scenario.capture_forms?.[name];
      const pattern = typeof form === 'string' ? new RegExp('^' + fill(form, values).split('{~uuid}').map(part => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}') + '$', 'u') : null;
      if (!pattern || !pattern.test(values[name])) return finish('inconclusive', `stopped at ${step.id}: the location "${location}" is not of the form the App makes`);
    }
    // The step's one verdict, after its captures (a state can name a path captured at this step), made by the one
    // admission: "admitted" when the record of the state it names is judged and usable for this launch, its view equals
    // that state line for line, and no expectation is unmet; "failed" when an expectation is unmet or the view differs;
    // "captured, not judged" when it names no state. A record not usable for this launch says nothing of this build:
    // the walk stops there, and the step has no verdict. Every affirmative output is derived from these verdicts.
    if (step.state !== undefined) {
      entry.state_named = step.state;
      const admitted = admission(scenario, 'state', step.state, seen.text, values, app, appName, candidateKey);
      if (admitted.unusable) return finish('inconclusive', `stopped at ${step.id}: ${admitted.unusable}; its view is not admitted`);
      if (!admitted.admitted) {
        mark.unmet.push({ code: 'view-differs-from-state', state: step.state });
        entry.state_difference = admitted.difference;
      }
      mark.verdict = mark.unmet.length ? 'failed' : 'admitted';
    } else {
      mark.verdict = mark.unmet.length ? 'failed' : 'captured, not judged';
    }
    const after = gate(`after ${step.id}`);
    entry.child_processes = lastChildren ?? 'not known: the watch file does not show the build running';
    if (after) return after;
  }
  return finish('end');
}

/**
 * Every affirmative output is derived from the steps' verdicts, which only admission makes (App Agent 0 and the
 * INTERLOCUTOR, after the third independent reading of PR 351): nothing affirmative is computed anywhere else.
 * - The scenario's verdict: "pass" when every step's verdict is "admitted"; "fail" when any step's is "failed";
 *   otherwise "captured, not judged". A walk that stops early takes "inconclusive" where it stops (finish).
 * - An outcome line: "shown" when every step it names was admitted; "not reached" when one was not reached; "not shown"
 *   when one failed or has no verdict; otherwise "captured, not judged".
 * Expectations are failures only (unmet): an expectation alone can never make "pass" or "shown".
 */
// The attempt log's first line, and the README's: what the log is not.
export const ATTEMPT_LOG_NOTE = 'ATTEMPT LOG. This is not a result: it holds what the walk did and saw (attempts and their returns, captures, the scenario\'s intended text). The walk\'s one result is its verdict.';
export const SCENARIO_VERDICTS = ['pass', 'fail', 'inconclusive', 'captured, not judged'];
const STEP_ID = /^[A-Za-z0-9_-]{1,40}$/;
const ACTS = ['view', 'click', 'type', 'confirm_sheet'];

function sha256(text) {
  return createHash('sha256').update(String(text)).digest('hex');
}

/**
 * Why the scenario is not well formed, or null. The walk reads these of a scenario's shape and checks each: steps, a
 * non-empty list of objects; each step's id, a string of the fixed pattern, the ids unique; its act, one of the four;
 * its state and from_state, when given, ids of the same pattern; its expect, when given, a list of objects; its control,
 * when given, an object with a string kind and label; its wait_ms and sheet_wait_ms, when given, non-negative numbers;
 * its capture, when given, an object of strings. What admission reads (states, state_records, sheets, sheet_records)
 * it checks itself where it reads it.
 */
export function scenarioProblem(scenario) {
  const steps = scenario?.steps;
  if (!Array.isArray(steps) || !steps.length) return 'its steps are not a non-empty list';
  const seen = new Set();
  for (const [n, step] of steps.entries()) {
    const where = `step ${n + 1}`;
    if (!step || typeof step !== 'object' || Array.isArray(step)) return `${where} is not an object`;
    if (typeof step.id !== 'string' || !STEP_ID.test(step.id)) return `${where}'s id is not a string of the step id form`;
    if (seen.has(step.id)) return `${where}'s id repeats an earlier step's`;
    seen.add(step.id);
    if (!ACTS.includes(step.act)) return `${where}'s act is not one the walk makes`;
    for (const key of ['state', 'from_state']) {
      if (step[key] !== undefined && (typeof step[key] !== 'string' || !STEP_ID.test(step[key]))) return `${where}'s ${key} is not a state id`;
    }
    if (step.expect !== undefined && (!Array.isArray(step.expect) || step.expect.some(e => !e || typeof e !== 'object' || Array.isArray(e)))) return `${where}'s expect is not a list of objects`;
    if (step.control !== undefined && (!step.control || typeof step.control !== 'object' || typeof step.control.kind !== 'string' || typeof step.control.label !== 'string')) return `${where}'s control is not an object with a kind and a label`;
    for (const key of ['wait_ms', 'sheet_wait_ms']) {
      if (step[key] !== undefined && !(typeof step[key] === 'number' && Number.isFinite(step[key]) && step[key] >= 0)) return `${where}'s ${key} is not a non-negative number`;
    }
    if (step.capture !== undefined && (!step.capture || typeof step.capture !== 'object' || Object.values(step.capture).some(v => typeof v !== 'string'))) return `${where}'s capture is not an object of strings`;
  }
  return null;
}

/**
 * The walk's one result, its verdict, derived BY POSITION over every step the scenario requires: each required step's
 * judgment is the mark made at its position, and a step with no mark was not reached. A walk that stopped keeps the
 * verdict it stopped with (fail or inconclusive); only a walk that reached its end is given the derived verdict, and
 * only that can be "pass".
 */
export function verdictAt(scenario, marks, verdict) {
  if (verdict !== 'end') return verdict === 'fail' ? 'fail' : 'inconclusive';
  const required = Array.isArray(scenario?.steps) ? scenario.steps : [];
  return verdictOf(required.map((_, position) => {
    const mark = marks[position];
    if (!mark || mark.position !== position) return { verdict: 'not reached' };
    return { verdict: ['admitted', 'failed', 'captured, not judged'].includes(mark.verdict) ? mark.verdict : 'no verdict' };
  }));
}

export function verdictOf(steps) {
  if (steps.some(step => step.verdict === 'failed')) return 'fail';
  if (!steps.length || steps.some(step => !['admitted', 'captured, not judged'].includes(step.verdict))) return 'inconclusive';
  return steps.every(step => step.verdict === 'admitted') ? 'pass' : 'captured, not judged';
}

/** The summary: the verdict, and nothing beyond it. */
export function summary(verdict) {
  return `verdict: ${SCENARIO_VERDICTS.includes(verdict) ? verdict : 'inconclusive'}`;
}
