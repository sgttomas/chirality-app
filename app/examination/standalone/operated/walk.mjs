// Walks one scenario file on a running development build and checks each view against the scenario's
// expected states. An operator loads this inside the node runtime's js tool and gives it the supplier's
// window service; replay.mjs gives it a stand-in that returns recorded views. See README.md beside it.
//
// It makes two kinds of call and no others: a view (get_app_state) and a click by element index. It clicks only
// controls a scenario step names, found by their kind and words in the latest view. It never lists applications,
// types, sets a value, presses a key, scrolls, drags or pastes.
//
// What its result establishes: that views returned by the service held the expected elements, or did not. It is
// development evidence about a development build. It is not evidence that a person saw or did anything.

export const DEVELOPMENT_PREFIX = 'dev.chirality.app-v4.candidate.';
const ELEMENT = /^([~+]?)(\t*)(\d+) (.*)$/;
const DIFFERENCE = 'The following is a diff from the previous accessibility tree';
const NO_CHANGE = 'There has been no change in the accessibility tree';

/** The elements of a whole view: [{index, depth, content}] in the order returned. */
export function parseView(text) {
  const elements = [];
  for (const line of String(text).split('\n')) {
    const match = ELEMENT.exec(line);
    if (match && !match[1]) elements.push({ index: Number(match[3]), depth: match[2].length, content: match[4] });
  }
  return elements;
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
 * Every element a selector names. A selector is {kind, label} where kind is button, summary, radio, heading or text.
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
    return false;
  });
}

const endsWithEllipsis = words => /(…|\.\.\.)\s*$/.test(words);

/**
 * What in a view is not the scenario's page, or null. The rule is what a view may hold, not a list of things it may
 * not: at the top, the one window the scenario names and the menu bar; directly inside that window, only the
 * entries the scenario lists. A sheet, a dialog, an alert, a second window or anything else unlisted is not the page.
 */
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
  return null;
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
 *   sky       the supplier's window service (or a stand-in with get_app_state and click)
 *   scenario  the parsed scenario file
 *   app       the development build's bundle identifier
 *   home      the throwaway home the launcher made for this launch (launch folder + /home)
 *   bundle    the candidate's bundle, the path of its .app folder: the watched process's executable must be inside
 *             it, and every view must be of it
 *   pid       the running App's process number, confirmed from the shell
 *   watch     the path of the file watch.py keeps while that process runs; the walk reads it before the first view
 *             and at every step, since the node runtime cannot ask the system about a process itself
 *   readWatch optional: () => the parsed watch file, or null (default: reads `watch`)
 *   sleep     optional: (milliseconds) => a promise (default: a timer)
 *   now       optional: () => the time as text (default: the UTC time)
 * Returns {scenario, app, home, verdict, outcomes, steps, calls, stopped, view_error when a view failed}. verdict is 'pass', 'fail' or
 * 'inconclusive'; a refusal before any call is 'inconclusive' with nothing called.
 */
/**
 * A failed call, as messages only: the error's own message and then each cause it carries, in order, whole. Nothing
 * else of the error object is kept. At most eight causes; a cause seen before ends the chain.
 */
export function failure(where, error) {
  const text = value => String(value?.message ?? value);
  const causes = [];
  const seen = new Set([error]);
  for (let cause = error?.cause; cause != null && causes.length < 8 && !seen.has(cause); cause = cause?.cause) {
    seen.add(cause);
    causes.push(text(cause));
  }
  return { where, message: text(error), causes };
}

export async function run({ sky, scenario, app, home, bundle, pid, watch, readWatch, sleep, now }) {
  if (!readWatch && typeof watch === 'string') {
    const fs = await import('node:fs');
    readWatch = () => { try { return JSON.parse(fs.readFileSync(watch, 'utf8')); } catch { return null; } };
  }
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
  const values = { identifier: app, home, app_data: `${home}/Library/Application Support/${app}` };
  const calls = [];
  const report = { scenario: scenario.scenario, version: scenario.version, app, home, started: now(), steps: [], calls, stopped: null };
  const finish = (verdict, stopped = null) => {
    report.stopped = stopped;
    report.verdict = verdict;
    report.finished = now();
    report.outcomes = Object.fromEntries(Object.entries(scenario.outcomes ?? {}).map(([name, ids]) => {
      const steps = ids.map(id => report.steps.find(step => step.id === id));
      const shown = steps.every(step => step && step.checks.length > 0 && step.checks.every(check => check.pass));
      return [name, steps.some(step => !step) ? 'not reached' : shown ? 'shown' : 'not shown'];
    }));
    return report;
  };
  // Refusals before any call.
  if (typeof app !== 'string' || !app.startsWith(DEVELOPMENT_PREFIX) || !/^[A-Za-z0-9.-]+$/.test(app)) {
    return finish('inconclusive', 'refused before any call: the application is not named by a development build\'s bundle identifier');
  }
  if (typeof home !== 'string' || !home.startsWith('/') || home.endsWith('/')) {
    return finish('inconclusive', 'refused before any call: the home is not an absolute path');
  }
  if (typeof bundle !== 'string' || !bundle.startsWith('/') || !bundle.endsWith('.app')) {
    return finish('inconclusive', 'refused before any call: the bundle is not the absolute path of an .app folder');
  }
  const steps = Array.isArray(scenario?.steps) ? scenario.steps : [];
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
  let elements = [];
  // A view is whole, or the walk stops there. One that comes back as differences is kept, with the view rebuilt from
  // it, for reading only: no check is credited from a rebuilt view and no click is made from one.
  const view = async () => {
    calls.push({ at: now(), call: 'get_app_state', app });
    const state = await sky.get_app_state({ app, disableDiff: true });
    if (state?.app !== bundle) throw new Error(`the view does not say it is of the bundle; it names: ${state?.app}`);
    const text = String(state?.text ?? '');
    if (text.startsWith(DIFFERENCE) || text.startsWith(NO_CHANGE)) {
      let rebuilt = null;
      try {
        rebuilt = applyDifference(elements, text).map(({ index, depth, content }) => '\t'.repeat(depth) + index + ' ' + content).join('\n');
      } catch { /* shown as not rebuilt */ }
      return { whole: false, text, rebuilt };
    }
    elements = parseView(text);
    return { whole: true, text };
  };
  const asDifferences = id => `stopped at ${id}: the view came back as differences although the whole window was asked for; nothing is checked or clicked from a rebuilt view`;
  // Before any click: two whole views, one after the other. The first view of an application was seen to be whole
  // without asking; only a second one shows that asking for the whole window is honoured.
  report.whole_views_before_any_click = [];
  for (const ordinal of ['first', 'second']) {
    const beforeView = gate(`before the ${ordinal} view before any click`);
    if (beforeView) return beforeView;
    let seen;
    try {
      seen = await view();
    } catch (error) {
      report.view_error = failure(`the ${ordinal} view before any click`, error);
      return finish('inconclusive', `stopped at the ${ordinal} view before any click: the view failed (${report.view_error.message})`);
    }
    report.whole_views_before_any_click.push({ at: now(), whole: seen.whole, returned: seen.text, ...(seen.whole ? {} : { rebuilt_for_reading: seen.rebuilt }) });
    if (!seen.whole) return finish('inconclusive', asDifferences(`the ${ordinal} view before any click`));
    const stray = notThePage(elements, scenario);
    if (stray) return finish('inconclusive', `stopped at the ${ordinal} view before any click: ${stray}; no agent answers a prompt or a dialog`);
    const afterView = gate(`after the ${ordinal} view before any click`);
    if (afterView) return afterView;
  }
  for (const step of scenario.steps) {
    const entry = { id: step.id, at: now(), act: step.act, says: step.says, checks: [] };
    report.steps.push(entry);
    const before = gate(`at ${step.id}`);
    if (before) return before;
    if (step.act === 'click') {
      if (endsWithEllipsis(step.control.label)) return finish('inconclusive', `stopped at ${step.id}: a control whose words end with an ellipsis is never clicked`);
      const found = select(elements, step.control);
      entry.control = step.control;
      if (found.some(({ content }) => endsWithEllipsis(content))) return finish('inconclusive', `stopped at ${step.id}: the control found has words that end with an ellipsis, and such a control is never clicked`);
      if (found.length !== 1) return finish(report.steps.some(s => s.checks.some(c => !c.pass)) ? 'fail' : 'inconclusive',
        `stopped at ${step.id}: the control to click was found ${found.length} times in the latest view`);
      if (found[0].content.startsWith('button (disabled) ')) return finish('fail', `stopped at ${step.id}: the control to click is unavailable`);
      entry.element_index = found[0].index;
      calls.push({ at: now(), call: 'click', app, element_index: found[0].index });
      await sky.click({ app, element_index: found[0].index });
      if (step.wait_ms) await sleep(step.wait_ms);
      const beforeView = gate(`at ${step.id}, before its view`);  // read again immediately before the view
      if (beforeView) return beforeView;
    } else if (step.act !== 'view') {
      return finish('inconclusive', `stopped at ${step.id}: an act this script does not perform`);
    }
    let seen;
    try {
      seen = await view();
    } catch (error) {
      report.view_error = failure(step.id, error);
      entry.error = report.view_error.message;
      return finish('inconclusive', `stopped at ${step.id}: the view failed (${entry.error})`);
    }
    entry.returned = seen.text;
    if (!seen.whole) {
      entry.rebuilt_for_reading = seen.rebuilt;
      return finish('inconclusive', asDifferences(step.id));
    }
    const stray = notThePage(elements, scenario);
    if (stray) return finish('inconclusive', `stopped at ${step.id}: ${stray}; no agent answers a prompt or a dialog`);
    entry.checks = (step.expect ?? []).map(expectation => checkOne(elements, expectation, values));
    const after = gate(`after ${step.id}`);
    entry.child_processes = lastChildren ?? 'not known: the watch file does not show the build running';
    if (after) return after;
  }
  return finish(report.steps.every(step => step.checks.every(check => check.pass)) ? 'pass' : 'fail');
}

/** The result as the few lines a reader wants first. */
export function summary(report) {
  const lines = [`${report.scenario} (version ${report.version}): ${String(report.verdict).toUpperCase()}`];
  for (const [name, state] of Object.entries(report.outcomes ?? {})) lines.push(`  ${name}: ${state}`);
  if (report.stopped) lines.push(`  ${report.stopped}`);
  for (const cause of report.view_error?.causes ?? []) lines.push(`    caused by: ${cause}`);
  for (const step of report.steps) {
    for (const check of step.checks.filter(check => !check.pass)) {
      lines.push(`  ${step.id} expected ${JSON.stringify(check.expectation)}, found: ${JSON.stringify(check.found)}`);
    }
  }
  lines.push(`  calls made: ${report.calls.filter(c => c.call === 'get_app_state').length} views, ${report.calls.filter(c => c.call === 'click').length} clicks`);
  return lines.join('\n');
}
