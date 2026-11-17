// The scripted driver's judge: the first-use setup scenario's expectations, decided against a model of the page.
//
// It is a pure function of the model, so it is tested without a page, by the scripted driver's own test in the
// repository checks.
// page.js builds the model from the App's page; this file decides pass and fail. It mirrors walk.mjs's checks kind
// by kind, but against the page itself, not the supplier's accessibility text. It is plain JavaScript, so the test
// build evaluates it in the page unchanged, and node loads it through module.exports.
//
// THE MODEL is the page's visible elements in document order, each {kind, name, state}:
//   button   a <button>; state 'available' or 'unavailable' (disabled, or inside a disabled fieldset)
//   summary  a <summary>; state 'on' when its <details> is open, else 'off'
//   radio    an <input type=radio>; state 'chosen' when checked, else 'not chosen'
//   textbox  an <input> that takes text (no type, or text or search); state its value; 'unavailable' is kept apart
//            as the element's `unavailable` flag (disabled, or inside a disabled fieldset)
//   heading  an <h1> to <h6>
//   text     one run of words, as described below
// NAME RULE: an element's name is its aria-label when it has one; a radio's name is the words of its <label>;
//   otherwise the element's own words.
// WORDS RULE: the visible text nodes in document order, each kept as it is, joined directly when they share a parent
//   element and with one space where an element boundary or a <br> lies between them; then every run of white space
//   is made one space, and the ends are trimmed.
// TEXT RULE: one text is the words of one container: any element that is not an inline element (a, abbr, b, code,
//   em, i, kbd, mark, s, small, span, strong, sub, sup, u, br) or a button, together with its inline descendants'
//   words, and not descending into another container. A <label> is a container. A button's words are its name only
//   and make no text. A heading's and a summary's words also make a text, as in the supplier's view.
// VISIBLE RULE: an element counts only if it is rendered: it has a box on the page (getClientRects), and the
//   browser's checkVisibility says so where it exists. So the workspace the App keeps mounted under a hidden <div>
//   during first use, and the content of a closed <details>, are not in the model.
const ChiralityJudge = (() => {
  const fill = (text, values) => String(text).replace(/\{(\w+)\}/g, (whole, name) => (name in values ? values[name] : whole));
  const endsWithEllipsis = words => /(…|\.\.\.)\s*$/.test(words);

  /** Every element a selector {kind, label} names: its kind, and its name equal to the label whole. */
  const select = (model, selector) => model.filter(element => element.kind === selector.kind && element.name === selector.label);

  /** One expectation against the model: {expectation, pass, found}. Mirrors walk.mjs checkOne. */
  const judgeOne = (model, expectation, values) => {
    const result = (pass, found) => ({ expectation, pass, found });
    const one = (kind, label) => select(model, { kind, label: fill(label, values) });
    const count = found => (found.length === 1 ? 'present' : found.length ? `present ${found.length} times` : 'absent');
    const stateOf = found => (found.length === 1 ? found[0].state : found.length ? 'more than one' : 'absent');
    if ('text' in expectation) {  // exactly once
      const found = one('text', expectation.text);
      return result(found.length === 1, count(found));
    }
    if ('no_text' in expectation) {
      const found = one('text', expectation.no_text);
      return result(found.length === 0, found.length ? 'present' : 'absent');
    }
    if ('text_starts_one_of' in expectation) {  // exactly one text starts with one of these; which one is kept
      const starts = expectation.text_starts_one_of.map(start => fill(start, values));
      const found = model.filter(element => element.kind === 'text' && starts.some(start => element.name.startsWith(start)));
      return result(found.length === 1, found.length === 1 ? found[0].name : count(found));
    }
    if ('text_starts' in expectation) {
      const start = fill(expectation.text_starts, values);
      const found = model.filter(element => element.kind === 'text' && element.name.startsWith(start));
      return result(found.length === 1, found.length === 1 ? found[0].name : count(found));
    }
    if ('heading' in expectation) {
      const found = one('heading', expectation.heading);
      return result(found.length === 1, found.length ? 'present' : 'absent');
    }
    for (const kind of ['button', 'summary', 'radio', 'textbox']) {
      if (kind in expectation) {
        const state = stateOf(one(kind, expectation[kind]));
        const wanted = kind === 'textbox' ? fill(expectation.is, values) : expectation.is;  // a typed value names a path
        return result(state === wanted, state);
      }
    }
    if ('texts_from' in expectation) {  // every text from one element up to another, in order, and no other
      const from = select(model, expectation.texts_from), to = select(model, expectation.up_to);
      if (from.length !== 1 || to.length !== 1) return result(false, `the bounds were found ${from.length} and ${to.length} times`);
      const first = model.indexOf(from[0]), last = model.indexOf(to[0]);
      const texts = model.slice(first + 1, last).filter(element => element.kind === 'text').map(element => element.name);
      const wanted = expectation.are.map(text => fill(text, values));
      return result(first < last && JSON.stringify(texts) === JSON.stringify(wanted), texts);
    }
    if ('location' in expectation) {  // a named location whose path, the next element, lies under a folder
      const named = model.filter(element => element.kind === 'text' && element.name === expectation.location);
      if (named.length !== 1) return result(false, `the name is ${count(named)}`);
      const next = model[model.indexOf(named[0]) + 1];
      const path = next && next.kind === 'text' && next.name.startsWith('/') ? next.name : null;
      const under = fill(expectation.under, values);
      return result(path !== null && path.startsWith(under + '/') && !path.split('/').includes('..'), path ?? 'absent');
    }
    return result(false, 'an expectation of a kind this judge does not know');
  };

  /**
   * Which one element a step acts on, or why none. Exactly one element of the step's kind and words; never one the
   * scenario says is never clicked, never an unavailable button or textbox, and never one whose words end with an
   * ellipsis unless the scenario names it in `confirms` (the setup scenario names exactly one: desktop setup's own
   * confirmation, answered by the test build's stand-in).
   */
  const target = (model, step, scenario) => {
    const label = step.control.label;
    if ((endsWithEllipsis(label) && !(scenario.confirms ?? []).includes(label)) || (scenario.never_clicked ?? []).includes(label)) {
      return { verdict: 'inconclusive', why: `the control "${label}" is never clicked` };
    }
    const found = select(model, step.control);
    if (found.length !== 1) return { verdict: 'inconclusive', why: `the control to click was found ${found.length} times` };
    if (found[0].kind === 'button' && found[0].state === 'unavailable') return { verdict: 'fail', why: 'the control to click is unavailable' };
    if (found[0].kind === 'textbox' && found[0].unavailable) return { verdict: 'fail', why: 'the field to type into is unavailable' };
    return { index: model.indexOf(found[0]) };
  };

  /** The scenario's verdict from its steps' checks, and each outcome as walk.mjs names them. */
  const outcomes = (scenario, steps) => Object.fromEntries(Object.entries(scenario.outcomes ?? {}).map(([name, ids]) => {
    const found = ids.map(id => steps.find(step => step.id === id));
    const shown = found.every(step => step && step.checks.length > 0 && step.checks.every(check => check.pass));
    return [name, found.some(step => !step) ? 'not reached' : shown ? 'shown' : 'not shown'];
  }));

  return { fill, endsWithEllipsis, select, judgeOne, target, outcomes };
})();

if (typeof module !== 'undefined') module.exports = ChiralityJudge;
