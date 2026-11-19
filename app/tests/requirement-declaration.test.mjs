import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// DEL-02-03 REQ-001: the host's reading of declared against undeclared, which a
// catalogue entry carries at the moment of picking (requirementDeclaration),
// and the conversation's requirement check never disagree. The cases are the
// table the host's own tests recompute from the same workflow texts
// (tests/fixtures/requirement_declaration_cases.json); here each case's
// declaration, as the selection row carries it, is drawn by RequirementCheck
// and its sentence is set beside the host's state. Controlled values only.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {RequirementCheck} = loadSrc('RequirementCheck');
const {cases} = JSON.parse(readFileSync(new URL('./fixtures/requirement_declaration_cases.json', import.meta.url), 'utf8'));

async function drawn(selection) {
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(RequirementCheck, {selection})));
  const text = c.textContent;
  const items = c.querySelectorAll(node => node.localName === 'li').map(li => li.textContent);
  await React.act(async () => root.unmount());
  return {text, items};
}
const SENTENCES = {
  undeclared: /required tools aren't declared, so the App can't say which tools it needs/,
  declared_empty: /declares that it needs no tools/,
  not_read: /couldn't read this workflow's declared tools/,
};
/** Which of the check's four readings a drawing is: one of the three sentences, or a list of declared tools. */
function checkSays({text, items}) {
  const said = Object.entries(SENTENCES).filter(([, words]) => words.test(text)).map(([state]) => state);
  assert.ok(said.length <= 1, `one reading at a time: ${text}`);
  if (said.length === 1) { assert.deepEqual(items, [], 'no tool is listed beside that sentence'); return said[0]; }
  assert.ok(items.length > 0, `a declared workflow lists its tools: ${text}`);
  return 'declared';
}

test('the table covers each of the four states', () => {
  assert.deepEqual([...new Set(cases.map(c => c.state))].sort(), ['declared', 'declared_empty', 'not_read', 'undeclared']);
  for (const c of cases) assert.equal(c.requirementDeclaration.state, c.state, c.name);
});

for (const c of cases) test(`the check and the entry's reading agree: ${c.name} (${c.state})`, async () => {
  // The conversation's check, from the selection row's own declaration.
  assert.equal(checkSays(await drawn({declaration: c.declaration})), c.state);
  // An undeclared or unreadable part is never said as needing none, and the reverse.
  const text = (await drawn({declaration: c.declaration})).text;
  if (c.state !== 'declared_empty') assert.doesNotMatch(text, /needs no tools/);
  if (c.state !== 'undeclared') assert.doesNotMatch(text, /aren't declared/);
});

test('a declared entry\'s cut-down declaration draws the same tools as the selection\'s whole one', async () => {
  const declared = cases.filter(c => c.state === 'declared');
  assert.ok(declared.length >= 2);
  for (const c of declared) {
    const whole = await drawn({declaration: c.declaration});
    const cut = await drawn({declaration: c.requirementDeclaration.declaration});
    assert.deepEqual(cut.items, whole.items, c.name);
    assert.equal(cut.text, whole.text, c.name);
    assert.deepEqual(Object.keys(c.requirementDeclaration.declaration).sort(), ['categories', 'elements', 'reading'], c.name);
  }
});

test('only a declared entry carries a declaration, and only an unread one a reason', () => {
  for (const c of cases) {
    const keys = Object.keys(c.requirementDeclaration).sort();
    assert.deepEqual(keys, c.state === 'declared' ? ['declaration', 'state'] : c.state === 'not_read' ? ['reason', 'state'] : ['state'], c.name);
  }
});
