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
const OVERLAY = /^(sheet|dialog|system dialog|alert)\b/;

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

/** Every element a selector names. A selector is {kind, label} where kind is button, summary, radio, heading or text. */
export function select(elements, selector) {
  const { kind, label } = selector;
  return elements.filter(({ content }) => {
    if (kind === 'button') return content === `button ${label}` || content === `button (disabled) ${label}`;
    if (kind === 'summary') return content.startsWith(`summary ${label}, Value: `);
    if (kind === 'radio') return /^radio button Value: [01], /.test(content) && content.slice(content.indexOf(', ') + 2).startsWith(label);
    if (kind === 'heading') return content === `heading ${label}` || content.startsWith(`heading ${label}, `);
    if (kind === 'text') return content === `text ${label}`;
    return false;
  });
}

/** One expectation against one view's elements: {expectation, pass, found}. */
export function checkOne(elements, expectation, values) {
  const result = (pass, found) => ({ expectation, pass, found });
  const one = (kind, label) => select(elements, { kind, label: fill(label, values) });
  if ('text' in expectation) {
    const found = one('text', expectation.text);
    return result(found.length >= 1, found.length ? 'present' : 'absent');
  }
  if ('no_text' in expectation) {
    const found = one('text', expectation.no_text);
    return result(found.length === 0, found.length ? 'present' : 'absent');
  }
  if ('text_starts' in expectation) {
    const start = 'text ' + fill(expectation.text_starts, values);
    const found = elements.filter(({ content }) => content.startsWith(start));
    return result(found.length >= 1, found.length ? found[0].content.slice(5) : 'absent');
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
  if ('location' in expectation) {  // a named location whose path, the next element, lies under a folder
    const at = elements.findIndex(({ content }) => content === `text ${expectation.location}`);
    const next = at >= 0 ? elements[at + 1] : undefined;
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
 *   pid       the running App's process number, confirmed from the shell
 *   watch     the path of the file watch.py keeps while that process runs; the walk reads it before the first view
 *             and at every step, since the node runtime cannot ask the system about a process itself
 *   readWatch optional: () => the parsed watch file, or null (default: reads `watch`)
 *   sleep     optional: (milliseconds) => a promise (default: a timer)
 *   now       optional: () => the time as text (default: the UTC time)
 * Returns {scenario, app, home, verdict, outcomes, steps, calls, stopped}. verdict is 'pass', 'fail' or
 * 'inconclusive'; a refusal before any call is 'inconclusive' with nothing called.
 */
export async function run({ sky, scenario, app, home, pid, watch, readWatch, sleep, now }) {
  if (!readWatch && typeof watch === 'string') {
    const fs = await import('node:fs');
    readWatch = () => { try { return JSON.parse(fs.readFileSync(watch, 'utf8')); } catch { return null; } };
  }
  // The build is running when the watch file is for this process, says so, and was written in the last five seconds.
  const watched = () => {
    const seen = readWatch ? readWatch() : null;
    const running = !!seen && seen.pid === pid && seen.running === true && Math.abs(Date.now() - seen.at_ms) <= 5000;
    return { running, children: running ? (seen.children ?? []) : [] };
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
  if (!Number.isInteger(pid) || pid <= 1 || !watched().running) {
    return finish('inconclusive', 'refused before any call: the watch file does not show the build running, and a view of an application that is not running would start it outside the launcher');
  }
  let elements = [];
  const view = async () => {
    calls.push({ at: now(), call: 'get_app_state', app });
    const state = await sky.get_app_state({ app, disableDiff: true });
    const text = String(state?.text ?? '');
    if (text.startsWith(DIFFERENCE) || text.startsWith(NO_CHANGE)) elements = applyDifference(elements, text);
    else elements = parseView(text);
    return text;
  };
  for (const step of scenario.steps) {
    const entry = { id: step.id, at: now(), act: step.act, says: step.says, checks: [] };
    report.steps.push(entry);
    const before = watched();
    if (!before.running) return finish('inconclusive', `stopped at ${step.id}: the watch file no longer shows the build running`);
    if (scenario.starts_no_process && before.children.length) {
      return finish('fail', `stopped at ${step.id}: the App has a child process (${before.children.length}), and this scenario starts none`);
    }
    if (step.act === 'click') {
      const label = step.control.label;
      if (label.endsWith('…') || label.endsWith('...')) return finish('inconclusive', `stopped at ${step.id}: a control whose words end with an ellipsis is never clicked`);
      const found = select(elements, step.control);
      entry.control = step.control;
      if (found.length !== 1) return finish(report.steps.some(s => s.checks.some(c => !c.pass)) ? 'fail' : 'inconclusive',
        `stopped at ${step.id}: the control to click was found ${found.length} times in the latest view`);
      if (found[0].content.startsWith('button (disabled) ')) return finish('fail', `stopped at ${step.id}: the control to click is unavailable`);
      entry.element_index = found[0].index;
      calls.push({ at: now(), call: 'click', app, element_index: found[0].index });
      await sky.click({ app, element_index: found[0].index });
      if (step.wait_ms) await sleep(step.wait_ms);
    } else if (step.act !== 'view') {
      return finish('inconclusive', `stopped at ${step.id}: an act this script does not perform`);
    }
    let text;
    try {
      text = await view();
    } catch (error) {
      entry.error = String(error?.message ?? error);
      return finish('inconclusive', `stopped at ${step.id}: the view failed`);
    }
    entry.returned = text;
    const overlay = elements.find(({ content }) => OVERLAY.test(content));
    if (overlay) return finish('inconclusive', `stopped at ${step.id}: the view holds something that is not the page (${overlay.content.split(' ')[0]}); no agent answers it`);
    if (scenario.window && !elements.some(({ depth, content }) => depth === 0 && content.startsWith(`standard window ${scenario.window}`))) {
      return finish('inconclusive', `stopped at ${step.id}: the view is not of the window "${scenario.window}"`);
    }
    entry.checks = (step.expect ?? []).map(expectation => checkOne(elements, expectation, values));
    const after = watched();
    entry.child_processes = after.running ? after.children.length : 'not known: the watch file does not show the build running';
    if (scenario.starts_no_process && after.children.length) {
      return finish('fail', `stopped after ${step.id}: the App has a child process (${after.children.length}), and this scenario starts none`);
    }
  }
  return finish(report.steps.every(step => step.checks.every(check => check.pass)) ? 'pass' : 'fail');
}

/** The result as the few lines a reader wants first. */
export function summary(report) {
  const lines = [`${report.scenario} (version ${report.version}): ${String(report.verdict).toUpperCase()}`];
  for (const [name, state] of Object.entries(report.outcomes ?? {})) lines.push(`  ${name}: ${state}`);
  if (report.stopped) lines.push(`  ${report.stopped}`);
  for (const step of report.steps) {
    for (const check of step.checks.filter(check => !check.pass)) {
      lines.push(`  ${step.id} expected ${JSON.stringify(check.expectation)}, found: ${check.found}`);
    }
  }
  lines.push(`  calls made: ${report.calls.filter(c => c.call === 'get_app_state').length} views, ${report.calls.filter(c => c.call === 'click').length} clicks`);
  return lines.join('\n');
}
