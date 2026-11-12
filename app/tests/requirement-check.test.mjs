import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// DEL-02-03 REQ-001 / AC-001: the chosen workflow's required-tool check in the
// "Run a workflow" guide, before the start. Controlled host views only (the
// shapes the host's CK-1 view carries); no native App, supplier or model.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {RequirementCheck} = loadSrc('RequirementCheck');
const {RunWorkflowGuide} = loadSrc('RunJourney');

const tool = (name, over) => ({name, purpose:`Use ${name}.`, necessity:'required', stages:['Method'], ...over});
const harness = (name, capability, over = {}) => tool(name, {class:'harness_capability', capability, ...over});
const declared = tools => ({reading:'recognized', findings:[], categories:{required_tools:tools.length ? 'recognized' : 'declared_empty'},
  elements:{required_tools:tools.map(value => ({value, reading:'recognized', findings:[]}))}});
const view = (declaration, rows, result) => ({preparation:{declaration, requirements:rows.map(([outcome, reason]) => ({outcome, reason})),
  check:{result, tools:[]}, basis:{acting_pin:'App Codex 0.167.0', surface:'X'}}, statement:'requirement check …', advisory:true});
const ENGINEERING = /CK-\d|R14|surface X|generation|spawn|NPTD|multiAgentVersion|multi_agent|harness|host_operation|not_established|compatible|will run|\{|\}/;

async function render(selection) {
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(RequirementCheck, {selection})));
  const region = label => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
  const items = label => region(label) ? region(label).querySelectorAll(node => node.localName === 'li').map(li => li.textContent) : [];
  return {text:c.textContent, region, items, close:() => React.act(async () => root.unmount())};
}

test('an undeclared workflow reads as not declared, never as needing none or as a fault', async () => {
  const undeclared = {reading:'undeclared', findings:[], categories:{}, elements:{}};
  for (const selection of [{declaration:undeclared}, {declaration:undeclared, compatibility:view(undeclared, [], 'not_established')}, {}]) {
    const r = await render(selection);
    assert.match(r.text, /required tools aren't declared, so the App can't say which tools it needs/);
    assert.match(r.text, /isn't a fault, and it doesn't mean the workflow needs none\. You can still start it\./);
    assert.doesNotMatch(r.text, /needs no tools|passed|Available|Missing/);
    assert.doesNotMatch(r.text, ENGINEERING);
    assert.deepEqual(r.items('Required tools'), [], 'nothing inferred from prose');
    await r.close();
  }
  // An empty declared list is the workflow's own statement, and reads differently.
  const empty = await render({compatibility:view(declared([]), [], 'compatible')});
  assert.match(empty.text, /declares that it needs no tools/);
  await empty.close();
});

test('declared tools read available, missing or could not be established with why, required apart from optional', async () => {
  const tools = [harness('delegate', 'agent-delegation', {purpose:'Hand the review to a sub-agent.'}),
    harness('run-checks', 'shell-command'),
    harness('second-opinion', 'agent-delegation', {necessity:'optional', fallback:'Review in the same conversation.'})];
  const declaration = declared(tools);
  const cases = [
    [[['present', ''], ['not_established', 'no adopted supplier availability account at acting pin'], ['present', '']], 'not_established',
      [/^delegate — Hand the review to a sub-agent\. Available\.$/, /^run-checks — Use run-checks\. Couldn't be established: at the Codex version this App runs, the App has no confirmed way to tell whether Codex offers it\.$/],
      /Requirement check not established: the App couldn't tell whether one required tool is available\. You can still start the run\./],
    [[['missing', "the conversation's model reports multiAgentVersion disabled (NPTD §7.1 (1))"], ['not_established', 'no adopted supplier availability account at acting pin'], ['missing', 'the effective configuration sets features.multi_agent = false (NPTD §7.1 (2))']], 'unsupported',
      [/delegate — .* Missing: this conversation's model doesn't offer sub-agents\.$/, /run-checks — .* Couldn't be established/],
      /Requirement check not passed: one required tool is missing\. You can still start the run; the agent may be unable to do the steps that use it\./],
    [[['not_established', 'delegation signals not read for this conversation'], ['present', ''], ['not_established', 'x']], 'not_established',
      [/delegate — .* Couldn't be established: the App hasn't yet read whether this conversation's model offers sub-agents/, /run-checks — .* Available\.$/],
      /Requirement check not established/],
    [[['present', ''], ['present', ''], ['missing', 'the effective configuration sets features.multi_agent = false (NPTD §7.1 (2))']], 'compatible',
      [/Available\.$/, /Available\.$/],
      /Requirement check passed: every required tool was available to this conversation when the App checked\. This says what the App could see, not that the run will succeed\./],
  ];
  for (const [rows, result, required, summary] of cases) {
    const r = await render({compatibility:view(declaration, rows, result)});
    assert.match(r.text, summary);
    const shown = r.items('Required tools');
    assert.equal(shown.length, 2, shown.join('\n'));
    required.forEach((pattern, i) => assert.match(shown[i], pattern));
    const optional = r.items('Optional tools');
    assert.equal(optional.length, 1);
    assert.match(optional[0], /^second-opinion — Use second-opinion\. (Available\.|Missing: your Codex settings turn sub-agents off\.|Couldn't be established: .*) Without it: Review in the same conversation\.$/);
    assert.match(r.text, /Checked for this conversation with Codex 0\.167\.0\./);
    assert.doesNotMatch(r.text, ENGINEERING, r.text);
    await r.close();
  }
});

test('a host operation with no connected application never reads available', async () => {
  const declaration = declared([tool('read-supports', {class:'host_operation', operation:'OP-C1', versions:['v1']})]);
  const r = await render({compatibility:view(declaration, [['not_established', 'catalog unreadable or not read']], 'not_established')});
  const [row] = r.items('Required tools');
  assert.match(row, /^read-supports — Use read-supports\. Couldn't be established: it belongs to a connected application, and this App isn't connected to one, so it can't see what that application offers\.$/);
  assert.doesNotMatch(r.text, /Available/);
  assert.doesNotMatch(r.text, ENGINEERING);
  await r.close();
  // With no evaluation at all, nothing reads available either.
  const none = await render({declaration, compatibility:{preparation:null, state:'no evaluation', limit:'invented limit'}});
  assert.match(none.text, /The App couldn't check this workflow's tools for this conversation\. You can still start it\./);
  assert.match(none.items('Required tools')[0], /Couldn't be established: the App made no check for it\./);
  await none.close();
});

test('the guide shows the check in the Workflow step, before Inputs, and never disables the start for it', async () => {
  const g = {home:'account', appSession:'s1', spawnCounter:1};
  const declaration = declared([harness('delegate', 'agent-delegation')]);
  const host = {state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}}, threads:[{threadId:'T1', generation:g, status:{type:'idle'}}], serverRequests:[]};
  const data = {context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib',
    libraries:[{reference:'lib', origin:'project', registered:[{name:'review', sequence:1, revision:'rev-1', selectable:true}]}],
    selections:[{sourceRef:'src', threadId:'T1', selection:{state:'selected', reference:'sel', runnable:true, identity:{name:'review', origin:'project', revision:'rev-1'},
      declaration, compatibility:view(declaration, [['missing', "the conversation's model reports multiAgentVersion disabled (NPTD §7.1 (1))"]], 'unsupported')}}],
    runs:[], reviews:[]};
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(RunWorkflowGuide, {data, host, thread:'T1', busy:false, text:'', chooseThread:() => {}, setText:() => {}, act:async () => {}})));
  const steps = c.querySelectorAll(node => node.localName === 'li' && node.getAttribute('aria-labelledby')?.startsWith('run-'));
  const workflow = steps.find(node => node.getAttribute('aria-labelledby') === 'run-workflow-heading');
  assert.ok(workflow.querySelectorAll(node => node.getAttribute('aria-label') === 'Tools this workflow needs').length === 1);
  assert.match(workflow.textContent, /Missing: this conversation's model doesn't offer sub-agents\./);
  const order = steps.map(node => node.getAttribute('aria-labelledby'));
  assert.ok(order.indexOf('run-workflow-heading') < order.indexOf('run-inputs-heading'));
  const prepare = c.querySelectorAll(node => node.localName === 'button' && node.textContent === 'Prepare this run')[0];
  const props = prepare[Object.keys(prepare).find(k => k.startsWith('__reactProps$'))];
  assert.equal(!!props.disabled, false, 'a missing tool never blocks the start');
  await React.act(async () => root.unmount());
});
