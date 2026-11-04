import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// J2 guided path: the App composes a draft request for the person to send;
// finding, trial, review and registration stay on existing host commands.
// Controlled host views only: no native App, supplier, model or person act.
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {MakeWorkflowGuide, validWorkflowName, draftFolder, draftRequestText} = loadSrc('MakeJourney');
const {ConversationPanel} = loadSrc('App');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const path = text => ({encoding:'unix_bytes', bytes:[...new TextEncoder().encode(text)]});
const key = threadId => JSON.stringify([g, threadId]);
const host = (over = {}) => ({state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}},
  threads:[{threadId:'T1', generation:g, model:'invented-model'}, {threadId:'T2', generation:g, model:'invented-model'}], ...over});
const data = (over = {}) => ({context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib:project',
  libraries:[{reference:'lib:project', origin:'project', root:path('/invented/project'), registered:[{name:'taken-name', sequence:1, revision:'r', selectable:true}]}],
  drafts:{drafts:[]}, ...over});

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => all(c, 'button').find(node => node.textContent === label);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const next = c => region(c, 'Make a workflow from your work').textContent.match(/Next: ([^]*?)(?=Where you did the work)/)?.[1] ?? '';

async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = []; const offers = [];
  const opened = [];
  const render = () => root.render(React.createElement(MakeWorkflowGuide, {data:view.data, host:view.host, busy:!!view.busy,
    act:async (command, args) => { calls.push({command, args}); }, offerComposer:(threadKey, text) => offers.push({threadKey, text}), openPreparedMessage:item => opened.push(item),
    showConversation:view.navigate ? id => opened.push({shown:id}) : undefined}));
  await React.act(async () => render());
  return {c, calls, offers, opened, rerender:async next => { Object.assign(view, next); await React.act(async () => render()); },
    choose:async value => React.act(async () => props(all(c, 'select')[0]).onChange({target:{value}})),
    name:async value => React.act(async () => props(all(c, 'input')[0]).onChange({target:{value}})),
    press:async label => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); }};
}

test('the name rule and draft folder follow the host', () => {
  for (const name of ['spacing-check', 'a', 'v2-report', 'x'.repeat(64)]) assert.equal(validWorkflowName(name), true, name);
  for (const name of ['', 'Spacing', 'two--hyphens', '-lead', 'trail-', 'with space', 'under_score', 'x'.repeat(65)]) assert.equal(validWorkflowName(name), false, name);
  assert.equal(draftFolder('/invented/project/', 'spacing-check'), '/invented/project/.chirality/workflow-drafts/spacing-check');
  const request = draftRequestText('/invented/project/.chirality/workflow-drafts/spacing-check', 'spacing-check');
  assert.match(request, /\/invented\/project\/\.chirality\/workflow-drafts\/spacing-check\/WORKFLOW\.md starts with front matter holding only `name: spacing-check`/);
  assert.match(request, /Only write inside that folder\. Don't register it/);
});

test('a request is composed for the chosen conversation only once each prerequisite is met, and nothing is sent', async () => {
  const ui = await mount({host:host(), data:data()});
  assert.match(next(ui.c), /Choose the conversation where you did the work/);
  await ui.choose(key('T1'));
  assert.match(next(ui.c), /Name the workflow/);
  await ui.name('Bad Name'); assert.match(next(ui.c), /lowercase letters and digits only/);
  await ui.name('taken-name'); assert.match(next(ui.c), /already registered in this library; a new draft with that name would be refused/);
  assert.equal(props(button(ui.c, 'Put the request in the conversation')).disabled, true);
  await ui.name('spacing-check');
  assert.match(region(ui.c, 'Make a workflow from your work').textContent, /It will be written to \/invented\/project\/\.chirality\/workflow-drafts\/spacing-check\./);
  await ui.press('Put the request in the conversation');
  assert.deepEqual(ui.offers, [{threadKey:key('T1'), text:draftRequestText('/invented/project/.chirality/workflow-drafts/spacing-check', 'spacing-check')}]);
  assert.deepEqual(ui.calls, [], 'composing the request issues no host command');
  await ui.press('Look for drafts in this library');
  assert.deepEqual(ui.calls, [{command:'workflow_observe_drafts', args:{}}]);
  assert.match(region(ui.c, 'Make a workflow from your work').textContent, /No draft named spacing-check has been seen yet/);
});

test('each draft state names its own next step; registration is never claimed before the host reports it', async () => {
  const ui = await mount({host:host(), data:data()});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  const cases = [
    [{state:'not valid', findings:['HY-2: front-matter name "x" differs from the folder name "spacing-check"']}, /not valid for registration.*HY-2.*Ask the agent to fix the findings/, '#conversation'],
    [{state:'draft'}, /draft — not registered.*Only your confirmation registers it/, '#workflow-drafts'],
    [{state:'under review', content:{value:'abcdef0123456789'}}, /under review.*confirm registration in the App's dialog/, '#workflow-reviews'],
    [{state:'changed since review'}, /changed since review.*Review again before registering/, '#workflow-drafts'],
    [{state:'registered, unchanged since'}, /registered, unchanged since.*use it from Run a workflow/, '#run-workflow'],
  ];
  for (const [draft, words, href] of cases) {
    await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', ...draft}]}})});
    const status = region(ui.c, 'Draft status');
    assert.match(status.textContent, words, draft.state); assert.ok(all(status, 'a').some(a => a.getAttribute('href') === href), `${draft.state} → ${href}`);
    if (draft.state !== 'registered, unchanged since') assert.doesNotMatch(status.textContent, /Registered\. You can now use it/, draft.state);
    assert.match(next(ui.c), /A draft named spacing-check already exists\. Continue it below/);
    assert.equal(props(button(ui.c, 'Put the request in the conversation')).disabled, true, 'an existing draft is continued, not requested again');
  }
});

test('unfinished drafts are listed for return after reopening and Continue only fills the local name', async () => {
  const drafts = [{name:'half-done', state:'draft'}, {name:'needs-fix', state:'not valid', findings:['HY-1: no WORKFLOW.md']}, {name:'finished-one', state:'registered, unchanged since'}, {name:'gone', state:'removed'}];
  const ui = await mount({host:host(), data:data({drafts:{drafts}})});
  const list = region(ui.c, 'Unfinished drafts').textContent;
  assert.match(list, /half-done/); assert.match(list, /needs-fix/); assert.doesNotMatch(list, /finished-one|gone/);
  assert.match(list, /still here after you quit and reopen the App.*reading one there doesn't continue it/);
  await ui.press('Continue needs-fix');
  assert.equal(props(all(ui.c, 'input')[0]).value, 'needs-fix');
  assert.match(region(ui.c, 'Draft status').textContent, /HY-1: no WORKFLOW\.md/);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

test('no library, stale source and busy states issue nothing', async () => {
  const ui = await mount({host:host(), data:data({activeLibrary:null})});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  assert.match(next(ui.c), /Show this project's workflows so the draft has a place to go/);
  await ui.press('Show this project\'s workflows');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_open_project_library', args:{}});
  ui.calls.length = 0;
  await ui.rerender({host:host({workflowRoot:{context:{sourceRef:'other', generation:g}}}), data:data()});
  assert.match(next(ui.c), /out of date/);
  for (const label of ['Put the request in the conversation', 'Look for drafts in this library']) {
    const node = button(ui.c, label); assert.equal(props(node).disabled, true, label); await React.act(async () => props(node).onClick());
  }
  assert.equal(props(all(ui.c, 'select')[0]).disabled, true);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

test('an offered request fills only an empty composer of its conversation, keeps unsent text, and is never sent', async () => {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const sends = []; const noop = async () => {};
  const panelHost = {state:'ready', generation:g, roleLimits:{account:{roles:[]}}, threads:[{generation:g, threadId:'T1', futureGuidanceNotices:[]}, {generation:g, threadId:'T2', futureGuidanceNotices:[]}]};
  const show = (threadKey, composerOffer) => React.act(async () => root.render(React.createElement(ConversationPanel, {host:panelHost, threadKey, composerOffer, setThreadKey:() => {},
    answer:noop, runAct:noop, send:async (...args) => { sends.push(args); }, steer:noop, submitAttachments:noop, interrupt:noop, checkPlanMode:noop, codexBusy:false})));
  const textarea = () => all(container, 'textarea').find(node => node.parentNode.textContent.startsWith('Text '));
  const revealed = [];
  document.getElementById = id => { revealed.push(id); return container.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null; };
  await show(key('T1'), null);
  await show(key('T1'), {sequence:1, threadKey:key('T2'), text:'for T2'});
  assert.equal(props(textarea()).value, '', 'another conversation\'s request waits for that conversation');
  await show(key('T1'), {sequence:2, threadKey:key('T1'), text:'Please write the draft'});
  assert.equal(props(textarea()).value, 'Please write the draft');
  await React.act(async () => props(textarea()).onChange({target:{value:'my own unsent words'}}));
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  assert.equal(props(textarea()).value, 'my own unsent words', 'unsent text is never replaced by an offer');
  assert.match(region(container, 'Prepared workflow request').textContent, /Your unsent text is kept/);
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  await React.act(async () => props(button(container, 'Replace my text with the request')).onClick());
  assert.equal(props(textarea()).value, 'A newer request');
  assert.equal(region(container, 'Prepared workflow request'), undefined);
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  await React.act(async () => props(textarea()).onChange({target:{value:''}}));
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  assert.equal(props(textarea()).value, '', 'a handled offer is applied once');
  assert.deepEqual(sends, [], 'nothing is sent by an offer');
  assert.deepEqual(revealed, ['conversation', 'conversation'], 'each applied or held offer reveals the conversation once');
  await React.act(async () => root.unmount());
});

test('after reopening, the library comes first so unfinished drafts appear before any conversation is chosen', async () => {
  const ui = await mount({host:host(), data:data({activeLibrary:null})});
  assert.match(next(ui.c), /Show this project's workflows so the draft has a place to go, and to see unfinished drafts/);
  await ui.press('Show this project\'s workflows');
  await ui.rerender({data:data({drafts:{drafts:[{name:'half-done', state:'draft'}]}})});
  assert.match(region(ui.c, 'Unfinished drafts').textContent, /half-done/);
  assert.match(next(ui.c), /Choose the conversation where you did the work/);
});

test('a listed draft is tried and reviewed with the draft list\'s own commands and the guide\'s conversation', async () => {
  const ui = await mount({host:host(), data:data({drafts:{drafts:[{name:'spacing-check', state:'draft'}]}})});
  await ui.name('spacing-check');
  assert.equal(props(button(ui.c, 'Try it with the agent in this conversation')).disabled, true, 'a delegated trial needs the conversation');
  await ui.choose(key('T1'));
  await ui.press('Try it with the agent in this conversation');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_trial_prepare', args:{name:'spacing-check', kind:'delegated', generation:g, threadId:'T1'}});
  await ui.press('Try it in a fresh conversation');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_trial_prepare', args:{name:'spacing-check', kind:'clean', generation:g, threadId:'T1'}});
  await ui.press('Review it for registration…');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_review_draft', args:{name:'spacing-check'}});
  assert.match(region(ui.c, 'Try or review this draft').textContent, /only your confirmation in the App's dialog registers it/);
  const delegated = {draftName:'spacing-check', sequence:1, reference:'p1', authoring:{generation:g, threadId:'T1'}};
  await ui.rerender({host:host({threads:[{threadId:'T1', generation:g, model:'m', delegation:{reading:'missing', reason:'invented: no sub-agent tool'}}, {threadId:'T2', generation:g, model:'m'}]}),
    data:data({drafts:{drafts:[{name:'spacing-check', state:'changed since review', tryLimit:'invented try limit', reviewLimit:'invented review limit'}]}})});
  const actions = region(ui.c, 'Try or review this draft');
  assert.equal(button(ui.c, 'Try it with the agent in this conversation'), undefined, 'missing delegation hides the delegated trial');
  assert.match(actions.textContent, /isn't available in this conversation: invented: no sub-agent tool/);
  for (const label of ['Try it in a fresh conversation', 'Review it for registration…']) assert.equal(props(button(ui.c, label)).disabled, true, label);
  assert.match(actions.textContent, /invented try limit.*invented review limit/);
  await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  assert.equal(region(ui.c, 'Try or review this draft'), undefined, 'an open review is continued in the review, not reopened here');
  await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', state:'not valid', findings:['HY-1: no WORKFLOW.md']}]}})});
  assert.equal(region(ui.c, 'Try or review this draft'), undefined, 'an invalid draft is fixed first');
  const withPending = host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g},
    pendingTrials:[{kind:'delegated', ...delegated}, {kind:'clean', draftName:'spacing-check', sequence:2, reference:'p2'}, {kind:'delegated', draftName:'other-draft', sequence:3, reference:'p3', authoring:{generation:g, threadId:'T1'}}]}});
  await ui.rerender({host:withPending, data:data({drafts:{drafts:[{name:'spacing-check', state:'draft'}]}})});
  const ready = region(ui.c, 'Try or review this draft').textContent;
  assert.match(ready, /Trial 1 is ready to send/); assert.match(ready, /Trial 2 is ready to send\. Read and send it in the new-trial message box/);
  const {cleanTrialAnchor} = loadSrc('TrialComposer');
  assert.equal(region(ui.c, 'Try or review this draft').querySelectorAll(n => n.localName === 'a').find(a => a.textContent === 'Read and send it in the new-trial message box').getAttribute('href'), `#${cleanTrialAnchor('p2')}`, 'the link goes to that trial\'s own composer');
  assert.doesNotMatch(ready, /Trial 3/, 'another draft\'s trial is not offered here');
  const before = ui.calls.length;
  await ui.press('Read and send trial 1');
  assert.equal(ui.opened.length, 1); assert.equal(ui.opened[0].kind, 'delegated'); assert.equal(ui.opened[0].pending.reference, 'p1');
  assert.equal(ui.calls.length, before, 'opening a prepared trial issues no command and sends nothing');
});

test('with App navigation, an invalid draft shows its conversation instead of a bare scroll link', async () => {
  const ui = await mount({navigate:true, host:host(), data:data({drafts:{drafts:[{name:'spacing-check', state:'not valid', findings:['HY-1: no WORKFLOW.md']}]}})});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  await ui.press('Show the conversation');
  assert.deepEqual(ui.opened, [{shown:'T1'}]);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

test('the guide shows the draft\'s trials and brings one back to its conversation with the draft list\'s command, then opens the prepared results', async () => {
  const trials = [
    {reference:'t1', sequence:1, kind:'delegated', time:'2026-11-04 10:00', authoringConversation:{generation:g, threadId:'T1'}, broughtBack:[{time:'2026-11-04 10:30', to:{generation:g, threadId:'T1'}}]},
    {reference:'t2', sequence:2, kind:'clean', time:'2026-11-04 11:00', authoringConversation:{generation:g, threadId:'T1'}, trialConversation:{generation:g, threadId:'T2'}, broughtBack:[]},
    {reference:'t3', sequence:3, kind:'clean', time:'2026-11-04 11:30', trialConversation:{generation:g, threadId:'T9'}, live:true, broughtBack:[]},
    {kind:'earlier attachment trial', content:{value:'abc'}},
  ];
  const draft = {name:'spacing-check', state:'draft', trials};
  const ui = await mount({host:host(), data:data({drafts:{drafts:[draft]}})});
  await ui.name('spacing-check');
  const shown = () => region(ui.c, 'Trials of this draft').textContent;
  assert.match(shown(), /^Trials so farTrial 3 · in a fresh conversation \(a conversation that isn't loaded now\)/, 'latest first; an unloaded conversation is said so');
  assert.match(shown(), /Trial 2 · in a fresh conversation \(.+\) · 2026-11-04 11:00Not brought back yet\./);
  assert.match(shown(), /Trial 1 · with the agent in .+ · 2026-11-04 10:00Brought back to .+\./);
  assert.doesNotMatch(shown(), /attachment/);
  assert.equal(props(button(ui.c, 'Bring trial 2 back')).disabled, true, 'no conversation chosen, no bring-back');
  await ui.choose(key('T1'));
  const bring = all(ui.c, 'button').find(node => node.textContent.startsWith('Bring trial 2 back to '));
  assert.ok(bring); assert.equal(props(bring).disabled, false);
  const before = ui.calls.length;
  await React.act(async () => props(bring).onClick());
  assert.deepEqual(ui.calls.slice(before), [{command:'workflow_trial_bring_back', args:{reference:'t2', generation:g, threadId:'T1', includeNative:false}}], 'exactly the draft list\'s command; nothing is sent');
  const live = all(ui.c, 'button').find(node => node.textContent.startsWith('Bring trial 3 back'));
  assert.equal(props(live).disabled, true); assert.match(shown(), /waits until no turn is live/);
  const feedback = {id:'bb-1', trial:'t2', sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, prompt:'Here is how trial 2 went', transcript:'…', textIdentity:{value:'aa'}, includeNative:false, shortenings:[]};
  await ui.rerender({host:host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g}, pendingBringBacks:[feedback, {...feedback, id:'bb-other', draftName:'other-draft'}]}})});
  assert.match(shown(), /Trial 2's results are ready to send in .+\./);
  assert.equal(all(ui.c, 'button').filter(node => node.textContent.startsWith('Read and send trial')).length, 1, 'another draft\'s results are not offered here');
  const calls = ui.calls.length;
  await ui.press('Read and send trial 2\'s results');
  assert.equal(ui.opened.at(-1).kind, 'bring-back'); assert.equal(ui.opened.at(-1).pending.id, 'bb-1');
  assert.equal(ui.calls.length, calls, 'opening issues no command and sends nothing');
});
