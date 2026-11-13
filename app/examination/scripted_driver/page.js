// The scripted driver's walk of one scenario, evaluated in the test build's own page after judge.js.
//
// It builds the model judge.js describes (visible elements only; the rules are stated there), clicks each step's one
// control with element.click(), waits, builds the model again and has the judge decide each expectation. It types
// nothing, chooses no file, answers nothing, and never clicks a control the scenario says is never clicked. Its
// progress is kept in window.__chiralityDriver, which the test build reads until it is done.
//
// What it cannot see, stated in every report: native sheets, alerts and other windows, the window's own buttons and
// the menu bar; and there is no second reading of the page through the accessibility tree.
(() => {
  const J = ChiralityJudge;
  const INLINE = new Set(['A', 'ABBR', 'B', 'CODE', 'EM', 'I', 'KBD', 'MARK', 'S', 'SMALL', 'SPAN', 'STRONG', 'SUB', 'SUP', 'U', 'BR']);

  const visible = element => element instanceof Element && element.getClientRects().length > 0
    && (typeof element.checkVisibility !== 'function' || element.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }));

  /** The words rule (judge.js), not descending into an element for which stop() is true. */
  const wordsOf = (root, stop) => {
    let out = '', previous = null, gap = false;
    const visit = node => {
      for (const child of node.childNodes) {
        if (child.nodeType === Node.TEXT_NODE) {
          if (!child.data || !visible(child.parentElement)) continue;
          if (previous !== null && (gap || child.parentElement !== previous)) out += ' ';
          out += child.data;
          previous = child.parentElement;
          gap = false;
        } else if (child.nodeType === Node.ELEMENT_NODE) {
          if (child.tagName === 'BR' || (stop && stop(child))) { gap = true; continue; }
          visit(child);
        }
      }
    };
    visit(root);
    return out.replace(/\s+/g, ' ').trim();
  };

  const isButton = element => element.tagName === 'BUTTON' || (element.getAttribute('role') === 'button' && element.tagName !== 'SUMMARY');
  const isContainer = element => !INLINE.has(element.tagName) && !isButton(element) && element.tagName !== 'INPUT';
  const ownWords = element => wordsOf(element, child => isContainer(child) || isButton(child));
  const labelOf = input => input.closest('label') || (input.id && document.querySelector(`label[for="${CSS.escape(input.id)}"]`));
  const nameOf = element => {
    const aria = element.getAttribute('aria-label');
    if (aria) return aria.replace(/\s+/g, ' ').trim();
    if (element.tagName === 'INPUT' && element.type === 'radio') { const label = labelOf(element); return label ? wordsOf(label) : ''; }
    return wordsOf(element);
  };

  /** The model and, beside it, the node each entry came from (for the click). */
  const build = () => {
    const model = [], nodes = [];
    const add = (entry, node) => { model.push(entry); nodes.push(node); };
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
    for (let element = walker.currentNode; element; element = walker.nextNode()) {
      if (!visible(element) || element.closest('button')?.contains(element) && element.tagName !== 'BUTTON') continue;
      if (isButton(element)) {
        const unavailable = element.matches(':disabled') || element.getAttribute('aria-disabled') === 'true';
        add({ kind: 'button', name: nameOf(element), state: unavailable ? 'unavailable' : 'available' }, element);
        continue;
      }
      if (element.tagName === 'SUMMARY') add({ kind: 'summary', name: nameOf(element), state: element.parentElement?.open ? 'on' : 'off' }, element);
      else if (element.tagName === 'INPUT' && element.type === 'radio') add({ kind: 'radio', name: nameOf(element), state: element.checked ? 'chosen' : 'not chosen' }, element);
      else if (/^H[1-6]$/.test(element.tagName)) add({ kind: 'heading', name: nameOf(element) }, element);
      if (isContainer(element)) {
        const words = ownWords(element);
        if (words) add({ kind: 'text', name: words }, element);
      }
    }
    const dialogs = [...document.querySelectorAll('dialog[open], [role="dialog"], [role="alertdialog"]')].filter(visible).length;
    return { model, nodes, dialogs };
  };

  /** The page's buttons: every one in the document, and those rendered, so a report says what the model left out. */
  const census = () => ({
    buttons_in_document: document.querySelectorAll('button').length,
    buttons_under_a_hidden_element: document.querySelectorAll('[hidden] button').length,
    buttons_visible: [...document.querySelectorAll('button')].filter(visible).length,
  });

  window.__chiralityDriverRun = async ({ scenario, values }) => {
    const state = window.__chiralityDriver = { done: false, started_ms: Date.now(), steps: [], verdict: null, stopped: null,
      census_at_start: census() };
    const settle = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
    const finish = (verdict, stopped = null) => {
      Object.assign(state, { verdict, stopped, outcomes: J.outcomes(scenario, state.steps), census_at_end: census(),
        finished_ms: Date.now(), done: true });
    };
    const failedSoFar = () => state.steps.some(step => step.checks.some(check => !check.pass));
    try {
      for (const step of scenario.steps) {
        const entry = { id: step.id, act: step.act, says: step.says, checks: [] };
        state.steps.push(entry);
        if (step.act === 'click') {
          const { model, nodes } = build();
          const chosen = J.target(model, step, scenario);
          if (chosen.index === undefined) {
            return finish(chosen.verdict === 'fail' || failedSoFar() ? 'fail' : 'inconclusive', `stopped at ${step.id}: ${chosen.why}`);
          }
          entry.control = step.control;
          entry.clicked_ms = Date.now();
          nodes[chosen.index].click();
          await settle(step.wait_ms ?? 600);
        } else if (step.act !== 'view') {
          return finish('inconclusive', `stopped at ${step.id}: an act this driver does not perform`);
        }
        const { model, dialogs } = build();
        entry.viewed_ms = Date.now();
        entry.model_size = model.length;
        if (dialogs) return finish('inconclusive', `stopped at ${step.id}: an open dialog in the page; no agent answers a dialog`);
        entry.checks = step.expect.map(expectation => J.judgeOne(model, expectation, values));
      }
      return finish(state.steps.every(step => step.checks.every(check => check.pass)) ? 'pass' : 'fail');
    } catch (error) {
      return finish('inconclusive', `stopped: the driver threw (${String(error && error.message || error)})`);
    }
  };
})();
