import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, readdirSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The renderer's list of the host's refusals of a start made before anything is dispatched (App.tsx
// START_REFUSED_BEFORE_DISPATCH), read against the host's own source: a refusal there pauses nothing, so each sentence
// must be one the host writes in a function that runs only before thread_start dispatches, and every literal refusal
// those functions can return must be listed. A changed or moved sentence, a new literal refusal, or a listed function
// called after dispatch fails here. Source text only: nothing is built or run.
installMiniDom();
const {START_REFUSED_BEFORE_DISPATCH, startRefusedBeforeDispatch} = loadSrc('App');
const HOST = new URL('../src-tauri/src/', import.meta.url);
const read = file => readFileSync(new URL(file, HOST), 'utf8');
/** The end of the block that opens at `start` (a "{"), skipping string literals. */
function blockEnd(text, start) {
  let depth = 0;
  for (let i = start; i < text.length; i++) {
    const c = text[i];
    const raw = c === 'r' && /^r#*"/.exec(text.slice(i, i + 8));
    if (raw && !/\w/.test(text[i - 1] ?? '')) { const close = '"' + '#'.repeat(raw[0].length - 2); i = text.indexOf(close, i + raw[0].length) + close.length - 1; continue; }
    if (c === '"') { for (i++; i < text.length && text[i] !== '"'; i++) if (text[i] === '\\') i++; continue; }
    if (c === "'" && text[i + 2] === "'") { i += 2; continue; }
    if (c === "'" && text[i + 1] === '\\' && text[i + 3] === "'") { i += 3; continue; }
    if (c === '/' && text[i + 1] === '/') { i = text.indexOf('\n', i); continue; }
    if (c === '{') depth++;
    else if (c === '}' && --depth === 0) return i;
  }
  throw Error('unbalanced block');
}
// Host source without its tests: the *_tests.rs files are left out, and in each file every module under a test
// configuration is blanked (offsets kept).
const productSource = file => {
  let text = read(file);
  for (const m of text.matchAll(/#\[cfg\((?:all\()?test[^\]]*\]\s*(?:pub(?:\([a-z]+\))?\s+)?mod\s+\w+\s*\{/g)) {
    const open = m.index + m[0].length - 1;
    // A test module the scan cannot close is cut with all that follows it: only product source is searched.
    let end; try { end = blockEnd(text, open); } catch { text = text.slice(0, open); break; }
    text = text.slice(0, open) + ' '.repeat(end - open + 1) + text.slice(end + 1);
  }
  return text;
};
const productFiles = readdirSync(HOST).filter(f => f.endsWith('.rs') && !f.endsWith('_tests.rs'));

/** The body of the first `fn name(` in a file's product source: from its opening brace to the matching one, skipping string literals. */
function body(file, name) {
  const text = productSource(file);
  const at = text.search(new RegExp(`\\bfn ${name}\\s*[<(]`));
  assert.ok(at >= 0, `${file}: fn ${name} is found`);
  const start = text.indexOf('{', text.indexOf('(', at));
  const end = blockEnd(text, start);
  return {text: text.slice(start, end + 1), offset: start};
}
/** Every literal refusal written in a piece of source: Err("…"), .ok_or("…"), .ok_or_else(|| "…"), .map_err(|_| "…"). */
const literals = text => [...text.matchAll(/(?:\bErr\(|\.ok_or\(|\.ok_or_else\(\|\|\s*|\.map_err\(\|_\|\s*)"((?:[^"\\]|\\.)*)"/g)].map(m => m[1].replace(/\\"/g, '"').replace(/\\'/g, "'"));
const DISPATCH = '*dispatch_invoked=true;';
const preDispatch = () => { const inner = body('lib.rs', 'start_conversation_inner'); const cut = inner.text.indexOf(DISPATCH); assert.ok(cut > 0, 'start_conversation_inner sets dispatch_invoked'); return {before: inner.text.slice(0, cut), after: inner.text.slice(cut)}; };
const where = START_REFUSED_BEFORE_DISPATCH.map(row => ({...row, file: row.at.split(' ')[0], fn: row.at.split(' ')[1]}));
const functions = [...new Map(where.map(row => [row.at, row])).values()];

test('each listed sentence is written in its host function and nowhere else in the host product source', () => {
  for (const row of where) {
    const piece = row.fn === 'start_conversation_inner' ? preDispatch().before : body(row.file, row.fn).text;
    assert.ok(piece.includes(`"${row.sentence.replace(/"/g, '\\"')}"`), `${row.at} writes "${row.sentence}"`);
    for (const file of productFiles) {
      const text = productSource(file);
      let at = text.indexOf(`"${row.sentence.replace(/"/g, '\\"')}"`);
      while (at >= 0) {
        const inListed = where.filter(w => w.sentence === row.sentence && w.file === file).some(w => { const b = body(file, w.fn); return at >= b.offset && at < b.offset + b.text.length; });
        assert.ok(inListed, `"${row.sentence}" also appears in ${file} at ${at}, outside the listed functions`);
        at = text.indexOf(`"${row.sentence}"`, at + 1);
      }
    }
  }
});

// Literals in those functions that are not refusals they return, each with where it goes instead.
const NOT_RETURNED = {
  'App data unavailable': 'lib.rs start_conversation_inner passes it to child_roles::prepare as the App data reading, and goes on',
};
test('every literal refusal the listed functions can return, and every one in thread_start before dispatch, is listed', () => {
  const listed = new Set([...START_REFUSED_BEFORE_DISPATCH.map(row => row.sentence), ...Object.keys(NOT_RETURNED)]);
  assert.ok(preDispatch().before.includes('Err("App data unavailable".into()),&instruction_root'), NOT_RETURNED['App data unavailable']);
  for (const row of functions) {
    const piece = row.fn === 'start_conversation_inner' ? preDispatch().before : body(row.file, row.fn).text;
    for (const sentence of literals(piece)) assert.ok(listed.has(sentence), `${row.at} can return "${sentence}", which is not classed`);
  }
});

test('the listed functions run only before thread_start dispatches', () => {
  const start = body('lib.rs', 'start_conversation').text;
  const {before, after} = preDispatch();
  const outer = start.slice(0, start.indexOf('start_conversation_inner('));
  const calls = (text, fn) => new RegExp(`(?:\\.|::|\\b)${fn}\\s*\\(`).test(text);
  // Reached from start_conversation before it calls the inner start, or from the inner start before dispatch.
  const reached = {check_start_source: 'start_source', entry: 'entry', start_source: 'start_source', home_class: 'home_class', endpoint_checkpoint: 'invalidate_endpoint_edits',
    new_explicit: 'new_explicit', choose_start_entry: 'choose_start_entry', choose: 'choose_start_entry', start_params: 'start_params', claim_start: 'claim_start'};
  for (const row of functions) {
    if (row.fn === 'start_conversation_inner') continue;
    const via = reached[row.fn];
    assert.ok(via, `${row.at}: how it is reached is recorded`);
    assert.ok(calls(outer, via) || calls(before, via), `${row.at} is reached (through ${via}) before dispatch`);
    // After dispatch, neither the inner start nor what it calls to dispatch, wait and finish reaches it.
    for (const [file, fn] of [['access_provider.rs', 'thread_start_with_role_dispatch'], ['runtime_session.rs', 'finalize_start_attempt']])
      assert.ok(!calls(body(file, fn).text, row.fn) && !calls(body(file, fn).text, via), `${fn} does not reach ${row.fn}`);
    assert.ok(!calls(after, row.fn) && !calls(after, via), `start_conversation_inner does not reach ${row.fn} after dispatch`);
  }
  assert.ok(calls(body('access.rs', 'choose_start_entry').text, 'choose'), 'choose_start_entry reaches choose');
  assert.ok(calls(body('runtime_session.rs', 'start_source').text, 'check_start_source') && calls(start, 'entry'), 'start_source checks the source; start_conversation reads the entry');
});

test('a listed refusal is a refusal as the host returns it, with its suffix; anything else, or the words elsewhere, is not', () => {
  const OBSERVATION = '; role supply observation: {"state":"written"}';
  for (const {sentence} of START_REFUSED_BEFORE_DISPATCH) {
    assert.equal(startRefusedBeforeDispatch(Error(`${sentence}${OBSERVATION}`)), true, sentence);
    assert.equal(startRefusedBeforeDispatch(Error(sentence)), true, sentence);
  }
  assert.equal(startRefusedBeforeDispatch(Error('Native start remains "unknown" (write "written"); no automatic retry')), false);
  assert.equal(startRefusedBeforeDispatch(Error(`Native start dispatched; original role preparation failed: thread start in progress`)), false, 'the words after another sentence are not the refusal');
  assert.equal(startRefusedBeforeDispatch(Error('thread start in progressive')), false, 'a sentence is matched whole');
});
