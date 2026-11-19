// The three-region frame (WorkspaceShell.tsx, Navigator.tsx) on constructed host snapshots only: what the navigator
// lists and marks, when "Needs answer" and the live dot show, the right panel's tabs and how a reveal selects one, the
// status strip's four cases, and that the frame keeps nothing beyond the session. No supplier, model or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {loadSrc} from './support/load-src.mjs';
import {choiceLists, chosenIn, chooseIn} from './support/choices.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const {navigatorEntries, folderName} = loadSrc('Navigator');
const {RIGHT_PANEL_TABS, turnPhase, shellLayout} = loadSrc('WorkspaceShell');
const {choiceLabels} = loadSrc('AgentText');
const {threadChoices} = loadSrc('presentation');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const earlier = {...g, spawnCounter:0};
const key = id => JSON.stringify([g, id]);
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const byId = (c, id) => c.querySelectorAll(n => n.getAttribute('id') === id)[0];
const labelled = (c, label) => c.querySelectorAll(n => n.getAttribute('aria-label') === label)[0];
const shown = e => { for (let n = e; n; n = n.parentNode) if (props(n)?.hidden) return false; return true; };
const thread = (id, type = 'idle', generation = g) => ({generation, threadId:id, model:'invented-model', status:{type}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const request = (identity, threadId, over = {}) => ({recordKind:'server-request-entry', generation:g, requestIdentity:identity, method:'item/tool/requestUserInput', classification:'known-answerable', originClass:'person-input',
  nativeParameters:{threadId, turnId:'t', itemId:'i', isBlocking:false, questions:[{id:'q', header:'Scope', question:`Which folder for ${threadId}?`, isOther:false, isSecret:false, options:[{label:'reports/', description:'Reports'}]}]},
  state:'outstanding', replyWriteResult:'not-attempted', acknowledgmentObservation:{status:'not-observed'}, ...over});
const nativePath = path => ({encoding:'unix_bytes', bytes:[...new TextEncoder().encode(path)]});
const project = '/invented/projects/pump-station';
const withProject = host => ({...host, currentAppProjectContext:{reference:project}, currentAppProjectContextLimit:null,
  attachmentSelections:{launchAppProjectObservation:{source:'explicit App launch CHIRALITY_WORKSPACE', nativeRoot:nativePath(project)}}});
const baseHost = (over = {}) => ({state:'ready', generation:g, threads:[thread('T1'), thread('T2', 'active'), thread('T3'), thread('OLD', 'idle', earlier)],
  roleLimits:{account:{roles:[]}}, homeRouting:{activeModeHomeClass:'account'}, serverRequests:[],
  workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[], drafts:{drafts:[]}}, ...over});

async function mountApp(host, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [], revealed = [];
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => { revealed.push(id); return c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null; };
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return structuredClone(host);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content' || command === 'request_answer_companions') return [];
    if (command === 'open_waiting_requests') return {modeHomeClass:args.modeHomeClass, generation:args.generation, threadId:args.threadId, threadLoaded:true, standing:'invented'};
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await check({c, calls, revealed});
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById;
  }
}
const navigator = c => labelled(c, 'Workspace Navigator');
const rows = c => nodes(navigator(c), 'button').filter(b => (b.getAttribute('class') ?? '').split(' ').includes('woven-navigator-session'));
const row = (c, id) => rows(c).find(b => b.getAttribute('data-session-id') === id);
const needsAnswer = (c, id) => row(c, id).parentNode.childNodes.find(b => b.localName === 'button' && b.textContent === 'Needs answer');
const tabs = c => nodes(c, 'button').filter(b => b.getAttribute('role') === 'tab');
const selectedTab = c => tabs(c).find(b => b.getAttribute('aria-selected') === 'true')?.textContent;
const conversationChosen = c => chosenIn(choiceLists(byId(c, 'conversation'))[0]);
const strip = c => labelled(c, 'Activity status');

test('the navigator lists the loaded conversations of the current generation, titled as the conversation view names them', () => {
  const host = baseHost();
  const entries = navigatorEntries(host, new Set());
  assert.deepEqual(entries.map(e => e.threadId), ['T1', 'T2', 'T3'], 'only the current generation, in the host\'s order');
  const current = host.threads.filter(t => JSON.stringify(t.generation) === JSON.stringify(g));
  assert.deepEqual(entries.map(e => e.title), choiceLabels(threadChoices(current, t => JSON.stringify([t.generation, t.threadId]))), 'the chooser\'s own words, no other title');
  assert.deepEqual(entries.map(e => e.key), ['T1', 'T2', 'T3'].map(key));
  assert.deepEqual(navigatorEntries({...host, threads:undefined}, new Set()), [], 'no rows, no entries');
  assert.equal(folderName('/invented/projects/pump-station'), 'pump-station');
  assert.equal(folderName('/invented/projects/pump-station/'), 'pump-station');
});

test('the live dot shows only while the conversation\'s status type is "active"; "Needs answer" only where the waiting set holds it', () => {
  const entries = navigatorEntries(baseHost({threads:[thread('A', 'active'), thread('B', 'idle'), thread('C', 'notLoaded'), thread('D', 'systemError')]}), new Set(['B']));
  assert.deepEqual(entries.map(e => [e.threadId, e.live, e.needsAnswer]), [['A', true, false], ['B', false, true], ['C', false, false], ['D', false, false]]);
});

test('the status strip speaks for the conversation shown: waiting first, then working, idle, else nothing', () => {
  assert.equal(turnPhase(thread('A', 'active'), false), 'working');
  assert.equal(turnPhase(thread('A', 'active'), true), 'waiting', 'a request waiting for the person takes precedence');
  assert.equal(turnPhase(thread('A', 'idle'), true), 'waiting');
  assert.equal(turnPhase(thread('A', 'idle'), false), 'idle');
  assert.equal(turnPhase(thread('A', 'notLoaded'), false), null);
  assert.equal(turnPhase(thread('A', 'systemError'), false), null);
  assert.equal(turnPhase(null, false), null, 'no conversation selected');
  assert.equal(turnPhase(null, true), null);
});

test('the regions\' widths: 3.0.1\'s defaults, the right region at 480, a stacked layout below 960, collapse and expansion', () => {
  const s = {navigatorWidth:292, navigatorCollapsed:false, rightWidth:480, rightCollapsed:false, rightExpanded:false};
  assert.deepEqual(shellLayout(1440, s), {stacked:false, left:292, right:480, rightMax:704, columns:'292px 12px minmax(420px, 1fr) 12px 480px'});
  assert.equal(shellLayout(1440, {...s, rightCollapsed:true}).columns, '292px 12px minmax(420px, 1fr) 12px 56px');
  assert.equal(shellLayout(1440, {...s, navigatorCollapsed:true, rightExpanded:true}).columns, '56px 12px minmax(420px, 1fr) 12px 864px');
  assert.equal(shellLayout(1000, s).columns, '276px 12px minmax(420px, 1fr) 12px 280px', 'a narrower window keeps the centre at least 420 wide');
  assert.equal(shellLayout(959, s).stacked, true); assert.equal(shellLayout(959, s).columns, null);
  assert.equal(shellLayout(960, s).stacked, false);
});

test('the frame keeps widths, collapse and the selected tab in memory only', () => {
  for (const name of ['WorkspaceShell.tsx', 'Navigator.tsx']) {
    const source = readFileSync(new URL(`../src/${name}`, import.meta.url), 'utf8');
    assert.doesNotMatch(source, /localStorage|sessionStorage|indexedDB|invoke\(/, `${name} writes nothing anywhere`);
  }
});

test('mounted: the folder section names the project and counts its conversations; the selected entry carries the current mark', async () => {
  await mountApp(withProject(baseHost()), async ({c, calls}) => {
    const heading = navigator(c).querySelectorAll(n => (n.getAttribute('class') ?? '').includes('woven-chat-section-heading--folder'))[0];
    assert.ok(heading, 'a folder heading');
    assert.equal(heading.textContent, '▱ pump-station3', 'the folder\'s name and its count');
    assert.equal(heading.localName, 'div', 'the folder\'s name is not the App\'s words, so the heading is not a control');
    assert.equal(heading.getAttribute('title'), null);
    assert.deepEqual(rows(c).map(b => b.getAttribute('data-session-id')), ['T1', 'T2', 'T3']);
    assert.ok(rows(c).every(b => b.getAttribute('aria-pressed') === 'false'), 'none selected yet');
    const before = calls.length;
    await React.act(async () => props(row(c, 'T3')).onClick());
    assert.equal(conversationChosen(c), key('T3'), 'pressing an entry chooses it in the conversation view');
    assert.equal(row(c, 'T3').getAttribute('aria-pressed'), 'true', 'and marks it');
    assert.ok(rows(c).filter(b => b.getAttribute('data-session-id') !== 'T3').every(b => b.getAttribute('aria-pressed') === 'false'));
    // Choosing in the conversation view moves the mark too: one choice, two places.
    await React.act(async () => chooseIn(choiceLists(byId(c, 'conversation'))[0], key('T1')));
    assert.equal(row(c, 'T1').getAttribute('aria-pressed'), 'true');
    assert.deepEqual(calls.slice(before).filter(x => !['host_status', 'decision_view', 'request_answer_companions'].includes(x.command)), [], 'choosing issues no command');
  });
  // A project folder the App has not established: the entries, without a heading.
  await mountApp(baseHost(), async ({c}) => {
    assert.equal(navigator(c).querySelectorAll(n => (n.getAttribute('class') ?? '').includes('woven-chat-section-heading')).length, 0);
    assert.equal(rows(c).length, 3);
  });
});

test('mounted: the live dot and "Needs answer" show only where the host status backs them; pressing it opens that conversation\'s requests', async () => {
  const host = baseHost({serverRequests:[request('q1', 'T3'), request('q2', 'T1', {state:'settling'}), request('q3', 'T1', {originClass:'named-service'}), request('q4', 'T2', {classification:'unknown'})]});
  await mountApp(host, async ({c, calls, revealed}) => {
    const dots = id => row(c, id).querySelectorAll(n => (n.getAttribute('class') ?? '') === 'woven-navigator-session-dot');
    assert.equal(dots('T2').length, 1, 'the active conversation has the live dot');
    assert.equal(dots('T1').length, 0); assert.equal(dots('T3').length, 0);
    assert.ok(needsAnswer(c, 'T3'), 'an outstanding answerable request');
    assert.equal(needsAnswer(c, 'T1'), undefined, 'a request being sent, or one the App answers, is not the person\'s to answer');
    assert.equal(needsAnswer(c, 'T2'), undefined, 'a request not offered for an answer');
    const before = calls.length;
    await React.act(async () => { await props(needsAnswer(c, 'T3')).onClick(); });
    assert.deepEqual(calls.slice(before).filter(x => !['host_status', 'decision_view', 'request_answer_companions'].includes(x.command)), [{command:'open_waiting_requests', args:{modeHomeClass:'account', generation:g, threadId:'T3'}}], 'the same opening as "Waiting on you"; nothing is answered');
    assert.equal(conversationChosen(c), key('T3'), 'that conversation is chosen');
    assert.ok(revealed.some(id => id.startsWith('request-')), 'its request card is revealed');
  });
  // Without a request waiting, no "Needs answer" and the strip does not say waiting.
  await mountApp(baseHost(), async ({c}) => {
    assert.ok(['T1', 'T2', 'T3'].every(id => !needsAnswer(c, id)));
  });
});

test('mounted: the status strip speaks only for the conversation chosen in the centre', async () => {
  const host = baseHost({serverRequests:[request('q1', 'T3')]});
  await mountApp(host, async ({c}) => {
    const status = () => strip(c).querySelectorAll(n => n.getAttribute('role') === 'status')[0];
    assert.equal(status().textContent, '', 'no conversation chosen: nothing');
    assert.equal(strip(c).getAttribute('data-turn-phase'), null);
    for (const [id, words, phase] of [['T2', 'Working', 'working'], ['T1', 'Idle', 'idle'], ['T3', 'Waiting for you', 'waiting']]) {
      await React.act(async () => props(row(c, id)).onClick());
      assert.equal(status().textContent, words, id); assert.equal(strip(c).getAttribute('data-turn-phase'), phase);
    }
    assert.equal(nodes(strip(c), 'button').length + nodes(strip(c), 'a').length, 0, 'no control in the strip');
  });
});

test('mounted: the right panel\'s five tabs show the App\'s other views, all mounted; a reveal selects the tab that holds its target', async () => {
  await mountApp(baseHost(), async ({c, calls}) => {
    assert.deepEqual(tabs(c).map(t => t.textContent), ['Run a workflow', 'Workflows', 'Make a workflow', 'History', 'Settings & tools']);
    assert.deepEqual(RIGHT_PANEL_TABS.map(t => t.label), tabs(c).map(t => t.textContent));
    assert.equal(selectedTab(c), 'Run a workflow', 'at launch, with nothing to move for');
    const views = {'Run a workflow':'view-run', 'Workflows':'view-library', 'Make a workflow':'view-make', 'History':'view-history', 'Settings & tools':'workspace-tools'};
    for (const tab of tabs(c)) {
      await React.act(async () => props(tab).onClick());
      assert.equal(selectedTab(c), tab.textContent);
      assert.equal(byId(c, 'right-view-content').getAttribute('aria-labelledby'), tab.getAttribute('id'));
      for (const [label, id] of Object.entries(views)) assert.equal(shown(byId(c, id)), label === tab.textContent, `${tab.textContent}: ${label}`);
      assert.ok(shown(byId(c, 'view-conversation')), 'the conversation stays shown beside every tab');
    }
    // A reveal in the conversation leaves the right panel as it is.
    const {revealWorkspaceTarget} = loadSrc('DailyWorkspace');
    await React.act(async () => revealWorkspaceTarget('workspace-start', true));
    assert.equal(selectedTab(c), 'Settings & tools');
    // A reveal in another view selects its tab, opening the right region if it was collapsed.
    await React.act(async () => props(labelled(c, 'Collapse right panel')).onClick());
    assert.ok(!shown(labelled(c, 'Right panel')), 'collapsed'); assert.ok(byId(c, 'workspace-tools'), 'every view stays mounted while collapsed');
    await React.act(async () => revealWorkspaceTarget('workspace-history', true));
    assert.ok(shown(labelled(c, 'Right panel')), 'opened by the reveal'); assert.equal(selectedTab(c), 'History');
    assert.ok(shown(byId(c, 'workspace-history')));
    // Arrow keys move between tabs, as in 3.0.1.
    const tablist = labelled(c, 'Right panel views');
    await React.act(async () => props(tablist).onKeyDown({key:'ArrowRight', preventDefault() {}}));
    assert.equal(selectedTab(c), 'Settings & tools');
    await React.act(async () => props(tablist).onKeyDown({key:'Home', preventDefault() {}}));
    assert.equal(selectedTab(c), 'Run a workflow');
    assert.deepEqual(calls.filter(x => !['host_status', 'decision_view', 'native_confirmation_content', 'request_answer_companions'].includes(x.command)), [], 'the frame issues no command');
  });
});

test('mounted: closing the right panel collapses its region, and the toggle there opens it again; expand widens it and returns', async () => {
  await mountApp(baseHost(), async ({c}) => {
    const workspace = c.querySelectorAll(n => (n.getAttribute('class') ?? '').split(' ').includes('woven-workspace'))[0];
    const columns = () => props(workspace).style.gridTemplateColumns;
    assert.equal(columns(), '292px 12px minmax(420px, 1fr) 12px 480px');
    await React.act(async () => props(labelled(c, 'Expand panel')).onClick());
    assert.equal(columns(), '56px 12px minmax(420px, 1fr) 12px 864px', 'wider, with the navigator collapsed');
    assert.ok(labelled(c, 'Collapsed chat navigation'));
    await React.act(async () => props(labelled(c, 'Return panel')).onClick());
    assert.equal(columns(), '292px 12px minmax(420px, 1fr) 12px 480px', 'returned as it was');
    await React.act(async () => props(labelled(c, 'Collapse right panel')).onClick());
    assert.equal(columns(), '292px 12px minmax(420px, 1fr) 12px 56px');
    const label = c.querySelectorAll(n => n.getAttribute('class') === 'woven-collapsed-label')[0];
    assert.equal(label.textContent, 'Run a workflow', 'the collapsed region names the selected tab');
    await React.act(async () => props(labelled(c, 'Open right panel')).onClick());
    assert.equal(columns(), '292px 12px minmax(420px, 1fr) 12px 480px');
    assert.equal(labelled(c, 'Open right panel'), undefined);
    // The navigator closes and opens again; its collapsed form keeps New chat and Settings & tools.
    await React.act(async () => props(labelled(c, 'Close Navigator')).onClick());
    assert.equal(navigator(c), undefined);
    const strip = labelled(c, 'Collapsed chat navigation');
    assert.ok(labelled(strip, 'New chat')); assert.ok(labelled(strip, 'Settings & tools'));
    await React.act(async () => props(labelled(c, 'Open Navigator')).onClick());
    assert.ok(navigator(c));
    // The handles resize by keyboard, within 3.0.1's bounds.
    const handle = labelled(c, 'Resize Navigator');
    await React.act(async () => props(handle).onKeyDown({key:'End', shiftKey:false, preventDefault() {}}));
    assert.equal(columns(), '360px 12px minmax(420px, 1fr) 12px 480px');
    await React.act(async () => props(labelled(c, 'Resize right panel')).onKeyDown({key:'ArrowLeft', shiftKey:true, preventDefault() {}}));
    assert.equal(columns(), '360px 12px minmax(420px, 1fr) 12px 520px');
  });
});

test('mounted: New chat reveals New conversation; the account row selects Settings & tools', async () => {
  await mountApp(baseHost(), async ({c, revealed}) => {
    const start = byId(c, 'workspace-start'); start.open = false;
    const summary = start.childNodes.find(n => n.localName === 'summary'); let focused = 0; summary.focus = () => { focused++; };
    await React.act(async () => props(nodes(navigator(c), 'button').find(b => b.textContent === '＋ New chat')).onClick());
    assert.equal(start.open, true, 'New conversation is open'); assert.equal(focused, 1, 'and focused');
    assert.equal(selectedTab(c), 'Run a workflow', 'the right panel is left as it is');
    await React.act(async () => props(labelled(navigator(c), 'Settings & tools')).onClick());
    assert.equal(selectedTab(c), 'Settings & tools'); assert.ok(revealed.includes('workspace-tools'));
    assert.ok(shown(byId(c, 'workspace-tools')));
  });
});

test('mounted: the removed navigation and heading are gone; their links\' targets still reveal', async () => {
  await mountApp(baseHost(), async ({c}) => {
    assert.equal(labelled(c, 'Workspace navigation'), undefined);
    assert.doesNotMatch(c.textContent, /Workflow workspace|Make, try, review and refine workflows through conversation\./);
    assert.equal(nodes(c, 'h1').filter(h => h.textContent === 'Chirality').length, 0);
    assert.equal(nodes(c, 'header').filter(h => h.getAttribute('class') === 'woven-navigator-brand' && h.textContent === 'Chirality').length, 1, 'the brand, in the navigator');
    const main = nodes(c, 'main')[0];
    assert.equal(main.getAttribute('class'), 'shell shell--workspace shell--stone');
    for (const [target, tab] of [['view-make', 'Make a workflow'], ['workspace-tools', 'Settings & tools'], ['view-run', 'Run a workflow'], ['workspace-history', 'History'], ['conversation', 'History']]) {
      const a = document.createElement('a'); a.setAttribute('href', `#${target}`); main.appendChild(a);
      let prevented = false;
      await React.act(async () => props(main).onClick({target:a, currentTarget:main, preventDefault:() => { prevented = true; }}));
      main.removeChild(a);
      assert.equal(prevented, true, target); assert.equal(selectedTab(c), tab, target);
    }
  });
});
