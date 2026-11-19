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
import { conversationView, chatInput } from './support/conversation-view.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const {navigatorEntries, navigatorProjects, folderName} = loadSrc('Navigator');
const {RIGHT_PANEL_TABS, MORE_VIEWS, RightPanel, turnPhase, shellLayout} = loadSrc('WorkspaceShell');
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
    if (command === 'host_status') return structuredClone(typeof host === 'function' ? host(calls) : host);
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
// More's list and the view chosen from it (WorkspaceShell.tsx MoreList, MoreBack).
const moreEntries = c => nodes(c, 'button').filter(b => b.getAttribute('data-more-view'));
const chooseMore = (c, view) => React.act(async () => props(moreEntries(c).find(b => b.getAttribute('data-more-view') === view)).onClick());
const pressTab = (c, label) => React.act(async () => props(tabs(c).find(t => t.textContent === label)).onClick());
const conversationChosen = c => chosenIn(choiceLists(conversationView(c))[0]);
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
  // Each conversation's row says it works in the project's folder, as a conversation started there does.
  const inProject = baseHost(); inProject.threads = inProject.threads.map(t => ({...t, cwd:project}));
  await mountApp(withProject(inProject), async ({c, calls}) => {
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
    await React.act(async () => chooseIn(choiceLists(conversationView(c))[0], key('T1')));
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
    for (const [id, words, phase] of [['T2', 'Working', 'working'], ['T1', 'Idle', 'idle'], ['T3', 'Needs answer', 'waiting']]) {
      await React.act(async () => props(row(c, id)).onClick());
      assert.equal(status().textContent, words, id); assert.equal(strip(c).getAttribute('data-turn-phase'), phase);
    }
    assert.equal(nodes(strip(c), 'button').length + nodes(strip(c), 'a').length, 0, 'no control in the strip');
  });
});

test('mounted: the right panel\'s tabs show the App\'s other views, all mounted; a reveal selects the tab that holds its target', async () => {
  await mountApp(baseHost(), async ({c, calls}) => {
    assert.deepEqual(tabs(c).map(t => t.textContent), ['Run', 'Workflows', 'Settings & tools', 'More']);
    assert.deepEqual(RIGHT_PANEL_TABS.map(t => t.label), tabs(c).map(t => t.textContent));
    assert.equal(selectedTab(c), 'Workflows', 'at launch, with nothing to move for');
    const more = tabs(c).find(t => t.textContent === 'More');
    assert.equal(more.childNodes.length, 1, 'More is quiet: its word and nothing beside it'); assert.equal(more.getAttribute('class'), null);
    const views = {'Run':'view-current-run', 'Workflows':'view-library', 'Settings & tools':'workspace-tools', 'More':'view-more'};
    const under = ['view-make', 'view-history', 'view-conversation-tools'];
    for (const tab of tabs(c)) {
      await React.act(async () => props(tab).onClick());
      assert.equal(selectedTab(c), tab.textContent);
      assert.equal(byId(c, 'right-view-content').getAttribute('aria-labelledby'), tab.getAttribute('id'));
      for (const [label, id] of Object.entries(views)) assert.equal(shown(byId(c, id)), label === tab.textContent, `${tab.textContent}: ${label}`);
      for (const id of under) assert.equal(shown(byId(c, id)), false, `${tab.textContent}: ${id} is shown only when chosen under More`);
      assert.ok(shown(byId(c, 'view-conversation')), 'the conversation stays shown beside every tab');
    }
    // A reveal in the conversation leaves the right panel as it is.
    const {revealWorkspaceTarget} = loadSrc('DailyWorkspace');
    await React.act(async () => revealWorkspaceTarget('workspace-start', true));
    assert.equal(selectedTab(c), tabs(c).at(-1).textContent, 'the tab last chosen stays selected');
    // A reveal in another view selects its tab, opening the right region if it was collapsed.
    await React.act(async () => props(labelled(c, 'Collapse right panel')).onClick());
    assert.ok(!shown(labelled(c, 'Right panel')), 'collapsed'); assert.ok(byId(c, 'workspace-tools'), 'every view stays mounted while collapsed');
    await React.act(async () => revealWorkspaceTarget('workspace-history', true));
    assert.ok(shown(labelled(c, 'Right panel')), 'opened by the reveal'); assert.equal(selectedTab(c), 'More', 'History is under More');
    assert.ok(shown(byId(c, 'workspace-history')));
    // Arrow keys move between tabs, as in 3.0.1.
    const tablist = labelled(c, 'Right panel views');
    await React.act(async () => props(tablist).onKeyDown({key:'ArrowLeft', preventDefault() {}}));
    assert.equal(selectedTab(c), 'Settings & tools');
    await React.act(async () => props(tablist).onKeyDown({key:'Home', preventDefault() {}}));
    assert.equal(selectedTab(c), 'Run', 'the first tab');
    // Revealing the new conversation shows the empty conversation, whose settings are the new conversation's: with Codex
    // ready the App reads the model list itself, once (a catalogue read; nothing is chosen or started).
    assert.deepEqual(calls.filter(x => x.command === 'read_available_models').map(x => x.args.atPersonPress), [false]);
    assert.deepEqual(calls.filter(x => !['host_status', 'decision_view', 'native_confirmation_content', 'request_answer_companions', 'read_available_models'].includes(x.command)), [], 'the frame issues no command');
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
    assert.equal(label.textContent, 'Workflows', 'the collapsed region names the selected tab');
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

test('mounted: New chat shows the empty conversation with its message box focused; the account row selects Settings & tools', async () => {
  await mountApp(baseHost(), async ({c, revealed}) => {
    const field = chatInput(c); let focused = 0; field.focus = () => { focused++; };
    await React.act(async () => props(nodes(navigator(c), 'button').find(b => b.textContent === '＋ New chat')).onClick());
    assert.equal(conversationChosen(c), '', 'no conversation is chosen'); assert.ok(byId(c, 'workspace-start'), 'the settings line is the new conversation\'s');
    assert.equal(focused, 1, 'the message box is focused');
    assert.equal(selectedTab(c), 'Workflows', 'the right panel is left as it is');
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
    for (const [target, tab] of [['view-make', 'More'], ['workspace-tools', 'Settings & tools'], ['view-library', 'Workflows'], ['workspace-history', 'More'], ['conversation', 'More']]) {
      const a = document.createElement('a'); a.setAttribute('href', `#${target}`); main.appendChild(a);
      let prevented = false;
      await React.act(async () => props(main).onClick({target:a, currentTarget:main, preventDefault:() => { prevented = true; }}));
      main.removeChild(a);
      assert.equal(prevented, true, target); assert.equal(selectedTab(c), tab, target);
    }
  });
});

// ---- After the independent review of the frame ----
test('a conversation is listed under the App\'s project only where Codex reports it working there', () => {
  const entry = (threadId, folder) => ({key:threadId, threadId, title:threadId, live:false, needsAnswer:false, folder});
  const placed = navigatorProjects('/p/pump-station', [entry('A', '/p/pump-station/'), entry('B', '/p/harbour'), entry('C', null), entry('D', '/p/harbour'), entry('E', '/p/pump-station\\')]);
  assert.deepEqual(placed.map(p => [p.folder, p.entries.map(e => e.threadId)]), [['/p/pump-station', ['A']], [null, ['B', 'C', 'D', 'E']]],
    'only the App\'s established project has a heading; a reported path alone establishes none, and a folder whose name ends in a backslash is another folder');
  assert.deepEqual(navigatorProjects(null, [entry('B', '/p/harbour')]).map(p => p.folder), [null], 'with no App project, a reported folder gets no heading');
  assert.deepEqual(navigatorProjects('/p/pump-station', []).map(p => [p.folder, p.entries.length]), [['/p/pump-station', 0]], 'the App\'s project is listed even when empty');
  assert.deepEqual(navigatorProjects(null, [entry('A', null)]).map(p => p.folder), [null], 'no project folder established: no heading');
  const rows = navigatorEntries({generation:g, threads:[{...thread('T1'), cwd:'/p/harbour'}, thread('T2')]}, new Set());
  assert.deepEqual(rows.map(r => r.folder), ['/p/harbour', null], 'the folder is the one the conversation\'s row carries');
});

test('mounted: a conversation continued from another folder is not counted under the App\'s project', async () => {
  const host = withProject(baseHost({threads:[{...thread('T1'), cwd:project}, {...thread('T2'), cwd:'/invented/projects/harbour'}]}));
  await mountApp(host, async ({c}) => {
    const headings = navigator(c).querySelectorAll(n => (n.getAttribute('class') ?? '').includes('woven-chat-section-heading--folder')).map(n => n.textContent);
    assert.deepEqual(headings, ['▱ pump-station1'], 'the other conversation is listed, under no heading');
    assert.deepEqual(rows(c).map(b => b.getAttribute('data-session-id')), ['T1', 'T2']);
  });
});

test('mounted: a delegated agent\'s request marks the conversation it descends from and opens the agent\'s own', async () => {
  const host = baseHost({serverRequests:[request('q9', 'C1')], nativeView:{home:'account', generation:g, items:[], turns:[], turnRecords:[], revisions:[],
    descendants:[{threadId:'C1', parentThreadId:'T1', parentSource:'collabAgentToolCall.senderThreadId', guidance:'not-known', nativeThread:{id:'C1'}}]}});
  await mountApp(host, async ({c, calls}) => {
    assert.ok(needsAnswer(c, 'T1'), 'marked on the root, as "Waiting on you" groups it');
    await React.act(async () => chooseIn(choiceLists(conversationView(c))[0], key('T1')));
    assert.equal(strip(c).textContent, 'Needs answer', 'the strip speaks for the root conversation shown');
    const before = calls.length;
    await React.act(async () => { await props(needsAnswer(c, 'T1')).onClick(); });
    assert.deepEqual(calls.slice(before).find(x => x.command === 'open_waiting_requests')?.args, {modeHomeClass:'account', generation:g, threadId:'C1'}, 'the request\'s own conversation is the one opened');
  });
});

test('mounted: after a status read fails, the frame claims no turn under way from the retained status', async () => {
  let fail = false;
  const snapshot = baseHost({serverRequests:[request('q1', 'T3')]});
  await mountApp(() => { if (fail) throw new Error('invented read failure'); return snapshot; }, async ({c}) => {
    const dots = id => row(c, id).querySelectorAll(n => (n.getAttribute('class') ?? '') === 'woven-navigator-session-dot').length;
    await React.act(async () => chooseIn(choiceLists(conversationView(c))[0], key('T2')));
    assert.equal(dots('T2'), 1); assert.equal(strip(c).textContent, 'Working');
    fail = true;
    await React.act(async () => { await props(needsAnswer(c, 'T3')).onClick(); });
    await React.act(async () => chooseIn(choiceLists(conversationView(c))[0], key('T2')));
    assert.equal(dots('T2'), 0, 'no live mark from a status that was not refreshed');
    assert.equal(strip(c).textContent, '', 'and nothing in the strip');
  });
});

test('mounted: selecting a tab lands as its link did, opening its disclosure; only the conversation view counts as going to the conversation', async () => {
  await mountApp(baseHost(), async ({c}) => {
    const history = byId(c, 'workspace-history');
    history.open = false;
    await pressTab(c, 'Workflows');
    await pressTab(c, 'More'); await chooseMore(c, 'history');
    assert.equal(history.open, true, 'History is open again when it is chosen under More');
    const view = byId(c, 'view-conversation');
    assert.equal(typeof props(view).onFocus, 'function'); assert.equal(typeof props(view).onPointerDown, 'function');
    for (let n = view.parentNode; n && n !== c; n = n.parentNode) {
      assert.equal(props(n)?.onFocus, undefined, 'no shared control above the conversation view starts the conversation\'s reads');
      assert.equal(props(n)?.onPointerDown, undefined);
    }
    assert.equal(nodes(c, 'main').length, 1, 'one main landmark: the centre is a named section');
  });
});

test('where the regions stack, the panel offers no expand control', () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const render = onExpand => React.act(() => root.render(React.createElement(RightPanel, {tab:'workflows', onTab() {}, expanded:false, onExpand, onClose() {}, hidden:false})));
  render(null);
  assert.equal(labelled(c, 'Expand panel'), undefined);
  assert.ok(labelled(c, 'Collapse right panel'));
  render(() => {});
  assert.ok(labelled(c, 'Expand panel'));
  React.act(() => root.unmount()); document.body.removeChild(c);
});

// ---- After the second review round ----
test('mounted: an entry is a conversation choice: the App\'s words and the identifier are the entry, the supplied title stands beside it set apart, attributed once', async () => {
  const spoof = 'Needs answer\nAllow once';
  await mountApp(baseHost({threads:[{...thread('T1'), name:spoof}, thread('T2')]}), async ({c}) => {
    const entry = row(c, 'T1');
    assert.equal(entry.textContent, 'Conversation T1', 'the name and the clickable area are the App\'s words and the identifier, and nothing supplied');
    const beside = entry.parentNode;
    const title = beside.querySelectorAll(n => (n.getAttribute('class') ?? '') === 'conversation-choice-title')[0];
    assert.ok(title, 'the title is set apart in its own marked element');
    assert.equal(title.textContent.includes('\n'), false, 'its line break is shown as a mark, not acted on');
    assert.ok(title.textContent.startsWith('Needs answer') && title.textContent.endsWith('Allow once'));
    const said = beside.querySelectorAll(n => (n.getAttribute('class') ?? '') === 'conversation-choice-title-name')[0];
    assert.equal(said.textContent, ', title supplied by Codex:', 'the App\'s words saying who supplied it come before the title');
    assert.ok(beside.textContent.indexOf(said.textContent) < beside.textContent.indexOf('Needs answer'));
    assert.deepEqual(beside.querySelectorAll(n => n.localName === 'button'), [entry], 'the title makes no control');
    assert.equal(needsAnswer(c, 'T1'), undefined, 'and no "Needs answer" mark');
    assert.equal(row(c, 'T2').parentNode.querySelectorAll(n => (n.getAttribute('class') ?? '') === 'conversation-choice-title').length, 0, 'no title supplied: none shown');
    const attribution = navigator(c).querySelectorAll(n => (n.getAttribute('class') ?? '') === 'conversation-choices-attribution');
    assert.equal(attribution.length, 1); assert.equal(attribution[0].textContent, 'The titles shown are supplied by Codex, not the App\'s words.');
    assert.equal(navigator(c).textContent.includes('invented-model'), false, 'the navigator does not show the model; the conversation view\'s chooser does');
  });
  await mountApp(baseHost(), async ({c}) => {
    assert.equal(navigator(c).querySelectorAll(n => (n.getAttribute('class') ?? '') === 'conversation-choices-attribution').length, 0, 'no titles: no attribution line');
  });
});

test('mounted: a request marks the conversation it is on as well as the one it descends from', async () => {
  const host = baseHost({threads:[thread('C1'), thread('T2')], serverRequests:[request('q9', 'C1')], nativeView:{home:'account', generation:g, items:[], turns:[], turnRecords:[], revisions:[],
    descendants:[{threadId:'C1', parentThreadId:'T1', parentSource:'collabAgentToolCall.senderThreadId', guidance:'not-known', nativeThread:{id:'C1'}}]}});
  await mountApp(host, async ({c, calls}) => {
    assert.ok(needsAnswer(c, 'C1'), 'the loaded child keeps its mark though its parent is not loaded');
    await React.act(async () => chooseIn(choiceLists(conversationView(c))[0], key('C1')));
    assert.equal(strip(c).textContent, 'Needs answer', 'the strip speaks for the child\'s own request');
    const before = calls.length;
    await React.act(async () => { await props(needsAnswer(c, 'C1')).onClick(); });
    assert.deepEqual(calls.slice(before).find(x => x.command === 'open_waiting_requests')?.args, {modeHomeClass:'account', generation:g, threadId:'C1'});
  });
});

test('mounted: moving along the tabs by the arrow keys opens nothing; a link that leads away is not going to the conversation', async () => {
  await mountApp(baseHost(), async ({c, calls}) => {
    const history = byId(c, 'workspace-history');
    history.open = false;
    const list = c.querySelectorAll(n => n.getAttribute('role') === 'tablist')[0];
    await pressTab(c, 'Run');
    for (let i = 0; i < tabs(c).length && selectedTab(c) !== 'More'; i++) await React.act(async () => props(list).onKeyDown({key:'ArrowRight', preventDefault() {}}));
    assert.equal(selectedTab(c), 'More', 'the arrow keys reach More');
    assert.ok(shown(byId(c, 'view-more')), 'which shows its list'); assert.equal(shown(byId(c, 'view-history')), false);
    assert.equal(history.open, false, 'and leave closed what the person closed');
    await chooseMore(c, 'history');
    assert.equal(history.open, true, 'choosing History under More opens it');
    const view = byId(c, 'view-conversation');
    const link = {tagName:'A', parentNode:view};
    const before = calls.length;
    await React.act(async () => props(view).onFocus({target:link}));
    await React.act(async () => props(view).onPointerDown({target:link}));
    assert.deepEqual(calls.slice(before).map(x => x.command).filter(x => x !== 'host_status'), [], 'nothing is read for a link that leads elsewhere');
  });
});

// ---- More: the views still in their earlier form, behind one quiet tab ----
test('mounted: More shows a short list of its three views, each a button with one line; choosing one shows it with a way back to the list', async () => {
  await mountApp(baseHost(), async ({c, calls}) => {
    await pressTab(c, 'More');
    assert.ok(shown(byId(c, 'view-more')), 'the list');
    assert.deepEqual(moreEntries(c).map(b => b.childNodes[0].textContent), ['Make a workflow', 'History', 'Conversation tools']);
    assert.deepEqual(moreEntries(c).map(b => b.childNodes[1].textContent), MORE_VIEWS.map(v => v.line), 'one line each of what is there');
    const ids = {make:'view-make', history:'view-history', 'conversation-tools':'view-conversation-tools'};
    const before = calls.length;
    for (const [view, id] of Object.entries(ids)) {
      await chooseMore(c, view);
      assert.equal(selectedTab(c), 'More', `${view}: More stays the selected tab`);
      assert.equal(shown(byId(c, 'view-more')), false, `${view}: the list gives way to the view`);
      for (const other of Object.values(ids)) assert.equal(shown(byId(c, other)), other === id, `${view}: ${other}`);
      const back = nodes(c, 'button').find(b => b.textContent === '‹ More' && shown(b));
      assert.ok(back, `${view}: the way back`);
      await React.act(async () => props(back).onClick());
      assert.ok(shown(byId(c, 'view-more')), `${view}: back at the list`);
      for (const other of Object.values(ids)) assert.equal(shown(byId(c, other)), false);
    }
    // Pressing the More tab while a view under it is shown goes back to the list.
    await chooseMore(c, 'history'); await pressTab(c, 'More');
    assert.ok(shown(byId(c, 'view-more'))); assert.equal(shown(byId(c, 'view-history')), false);
    assert.deepEqual(calls.slice(before).filter(x => !['host_status', 'decision_view', 'native_confirmation_content', 'request_answer_companions', 'read_available_models'].includes(x.command)), [], 'choosing issues no command');
  });
});

// One reveal for each kind of target inside More: each selects More, shows the view that holds it and reveals it.
const runRow = {reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:'ended', end:{cause:'completed'}}, workflow:{name:'invented-flow', origin:'project', revision:'r'}, status:{}};
for (const [kind, target, view] of [
  ['the conversation\'s permission level', 'conversation-level', 'view-conversation-tools'],
  ['the conversation tools (prepared messages and trials are drawn there)', 'conversation-tools-content', 'view-conversation-tools'],
  ['history and recovery', 'workspace-history', 'view-history'],
  ['a draft', 'workflow-drafts', 'view-make'],
  ['a review', 'workflow-reviews', 'view-make'],
  ['the workflow studio', 'workflow-studio', 'view-make'],
  ['a run\'s recorded evidence', 'run-evidence', 'view-make'],
  ['a recorded run reopened from project records', 'reopened-evidence', 'view-make'],
]) test(`mounted: a reveal of ${kind} selects More and shows its view`, async () => {
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const host = baseHost();
  host.workflowRoot = {...host.workflowRoot, runs:[runRow], reopened:{standing:'invented', runs:[{run:'rec-1', conversation:null, state:'ended'}]}};
  const id = target === 'run-evidence' ? runEvidenceAnchor('run-1') : target === 'reopened-evidence' ? runEvidenceAnchor('rec-1') : target;
  await mountApp(host, async ({c}) => {
    await pressTab(c, 'Run');
    assert.ok(byId(c, id), `${id} is mounted`);
    const {revealWorkspaceTarget} = loadSrc('DailyWorkspace');
    await React.act(async () => revealWorkspaceTarget(id, true));
    assert.equal(selectedTab(c), 'More', kind);
    assert.ok(shown(byId(c, view)), `${kind}: ${view} is shown`);
    assert.equal(shown(byId(c, 'view-more')), false, 'not the list');
    for (let n = byId(c, id); n && n !== c; n = n.parentNode) if (n.localName === 'details') assert.equal(n.open, true, `${kind}: its disclosures are opened`);
  });
});

test('mounted: the Run tab and the Workflows tab show none of the workflow studio; it is under More with Make a workflow', async () => {
  const host = baseHost();
  host.workflowRoot = {...host.workflowRoot, runs:[runRow], reopened:{standing:'invented', runs:[]}};
  await mountApp(host, async ({c}) => {
    const studio = ['Read recorded workflow supply (durable, read-only)', 'Reopen recorded workflow runs (read-only)'];
    const studioShown = () => nodes(c, 'button').filter(b => studio.includes(b.textContent) && shown(b)).length + (shown(byId(c, 'workflow-studio')) ? 1 : 0)
      + c.querySelectorAll(n => n.localName === 'h3' && n.textContent === 'Recorded runs (reopened from project records)' && shown(n)).length;
    for (const tab of ['Run', 'Workflows', 'Settings & tools']) { await pressTab(c, tab); assert.equal(studioShown(), 0, tab); }
    await pressTab(c, 'More'); await chooseMore(c, 'make');
    assert.equal(nodes(c, 'button').filter(b => studio.includes(b.textContent) && shown(b)).length, 2, 'the record reads are with the studio');
    assert.ok(shown(byId(c, 'workflow-studio')));
  });
});
