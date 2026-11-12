import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import './support/rust-prebuild.mjs';
const document=installMiniDom();
const {createRoot}=await import('react-dom/client');
const {DelegatedWorkView,UNREAD,createDelegatedWorkReader,useDelegatedWork,DELEGATED_WORK_REREAD_MS}=loadSrc('DelegatedWork');
const {WORKSPACE_VIEWS}=loadSrc('DailyWorkspace');
const {DecisionPackagesPanel}=loadSrc('App');
// The Delegated work view as the App mounts it, for one read of a packet.
const FleetRecordsPanel=({packet,error='',busy=false})=>React.createElement(DelegatedWorkView,{
  read:{...UNREAD,reading:busy,readAt:packet||error?1:null,fleet:packet,fleetError:error,decisions:{rows:[],limits:[]}},
  readNow:()=>{},decisionPackages:()=>null});
let packet;
test('native selected-workspace adapter response is presented in full with provenance and limits',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::tests::fleet_reader_native_adapter_full_response','--','--exact','--nocapture','--test-threads=1'],{
    cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'},
  });
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('FLEET_DTO:'));
  assert.ok(line,'the actual native adapter emitted its invented response fixture');
  packet=JSON.parse(line.slice(line.indexOf('FLEET_DTO:')+'FLEET_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet,error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Read again now/);assert.match(html,/Complete fleet packet, sources and provenance/);
  assert.match(html,/graph-content identity method is unselected\/unsupported/);
  assert.match(html,/protected-store order/);assert.match(html,/claimed|Claimed/);
  for(const row of [...packet.briefs,...packet.graphs,...packet.coordination.projectRecords,...packet.coordination.appObservations]){
    assert.ok(html.includes(row.record.recordId),'no returned record is hidden by a state projection');
  }
  assert.match(html,/No current graph established/);
  assert.equal(packet.workspace.undertakings.every(v=>v.graph===null),true,'historical unsupported selectors remain unselected');
  assert.doesNotMatch(html,/<button[^>]*>.*(?:Dispatch|Select graph|Write record|Register)/);
});
test('a read sends only the two path-free read-only commands, and rendering sends none',async()=>{
  const calls=[];
  const invoke=async(...args)=>{calls.push(args);return args[0]==='read_fleet_records'?packet:{rows:[],limits:[]};};
  let readNow=0;
  const element=DelegatedWorkView({read:UNREAD,readNow:()=>{readNow++;},decisionPackages:()=>null});
  renderToStaticMarkup(element);
  const findButton=node=>{
    if(!node || typeof node!=='object')return null;
    if(node.type==='button')return node;
    const children=node.props?.children;
    return (Array.isArray(children)?children:[children]).flat(Infinity).map(findButton).find(Boolean);
  };
  findButton(element).props.onClick();assert.equal(readNow,1,'the manual re-read is the view reader');
  assert.equal(calls.length,0);
  const reader=createDelegatedWorkReader({invoke,publish:()=>{},timers:{set:()=>'t',clear:()=>{}}});
  await reader.readNow();
  assert.deepEqual(calls,[['read_fleet_records'],['decision_view']]);
});
test('busy and failed source reads remain explicit without a fabricated empty packet',()=>{
  const busy=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:null,error:'',busy:true,refresh:()=>{}}));
  assert.match(busy,/disabled/);assert.match(busy,/Reading the project&#x27;s delegated work/);
  const failed=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:null,error:'selected project unavailable',busy:false,refresh:()=>{}}));
  assert.match(failed,/role="alert"/);assert.match(failed,/Fleet read failed: selected project unavailable/);
  assert.doesNotMatch(failed,/0 brief record/);
});

test('actual private native receipt to persisted reader packet to panel preserves source-qualified links',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','conversation_roles::tests::native_links_actual_fork_dispatch_receipt_tick_store_copy_and_reader_dto','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('NATIVE_LINK_DTO:'));assert.ok(line);
  const actual=JSON.parse(line.slice(line.indexOf('NATIVE_LINK_DTO:')+'NATIVE_LINK_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:actual,error:'',busy:false,refresh:()=>{}}));
  const row=actual.coordination.nativeRelationships[0];
  assert.equal(actual.coordination.nativeRelationships.length,1);
  assert.match(html,/Recorded native conversation links/);assert.match(html,/forked from/);
  for(const id of [row.record.observationId,row.record.body.source.threadId,row.record.body.thread.threadId,row.record.body.rpc.requestRef,row.record.body.nativeHome.homeId])assert.ok(html.includes(id));
  assert.match(html,/does not activate a conversation/);assert.match(html,/0.1 undertaking fields establish no native join/);
  assert.doesNotMatch(html,/<button[^>]*>.*(?:Dispatch|Restore role|Integrate|Select undertaking)/);
});

test('actual mixed-profile packet keeps mechanical outcomes separate from its sole native relationship',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::tests::fleet_reader_native_links_mixed_profile_keeps_legacy_quoted_and_mechanical_separate','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('NATIVE_LINK_MIXED_DTO:'));assert.ok(line);
  const actual=JSON.parse(line.slice(line.indexOf('NATIVE_LINK_MIXED_DTO:')+'NATIVE_LINK_MIXED_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:actual,error:'',busy:false,refresh:()=>{}}));
  assert.equal(actual.coordination.nativeRelationships.length,1);assert.equal(actual.coordination.recordingEvents.length,1);
  assert.match(html,/Native link recording outcomes/);assert.match(html,/recording_limit/);assert.match(html,/Invented copy failure; native success unchanged/);
  assert.match(html,/quoted 0.1 compatibility record/);assert.match(html,/undertaking\/thread fields establish no native conversation relationship/);
});


test('actual native workspace reconstructs returns and waiting identically in separate processes',()=>{
  const read=()=>{
    const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::views::tests::fleet_views_native_adapter_preserves_return_review_integration_and_rebuild','--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'},
    });
    assert.equal(proc.status,0,proc.stderr+proc.stdout);
    const line=proc.stdout.split('\n').find(line=>line.includes('FLEET_WORKSPACE_DTO:'));assert.ok(line);
    return JSON.parse(line.slice(line.indexOf('FLEET_WORKSPACE_DTO:')+'FLEET_WORKSPACE_DTO:'.length));
  };
  const first=read(),second=read();assert.deepEqual(first,second,'process state is not coordination authority');
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:{...packet,workspace:first},error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Fleet coordination workspace/);assert.match(html,/Current graph/);assert.match(html,/fl:graph/);
  assert.match(html,/Return-review queue/);assert.match(html,/Selected work and waiting causes/);
  assert.match(html,/integration recorded/);assert.match(html,/Owner: executor/);assert.match(html,/current human-act standing/);
  assert.match(html,/Reconstruction limits/);assert.match(html,/no dispatch observed/);
});

test('actual Rust brief attribution reaches each visible return row without changing preparer routing',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::views::tests::fleet_views_native_adapter_examination_attribution_','--','--nocapture','--test-threads=1'],{
    cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'},
  });
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const dto=marker=>{
    const line=proc.stdout.split('\n').find(line=>line.includes(marker));assert.ok(line,marker);
    return JSON.parse(line.slice(line.indexOf(marker)+marker.length));
  };
  const {before,after}=dto('FLEET_ATTRIBUTION_DTO:');
  const limits=dto('FLEET_ATTRIBUTION_LIMITS_DTO:');
  const visibleRow=(actual,reference)=>{
    const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:actual,error:'',busy:false,refresh:()=>{}}));
    const queue=html.split('<h4>Return-review queue')[1].split('</section>')[0];
    const row=queue.match(/<li>[\s\S]*?<\/li>/g).find(row=>row.includes(`Return: ${reference}.`));
    assert.ok(row,`visible return ${reference}`);
    return row.split('<details>')[0]; // Packet JSON in disclosure cannot satisfy display assertions.
  };
  for(const actual of [before,after]){
    const named=visibleRow(actual,'fl:named-return');
    assert.match(named,/Who examines: original preparer \(prepared the brief\)/);
    assert.match(named,/Brief preparer source: return&#x27;s named brief brief:original\./);
    assert.doesNotMatch(named,/return does not name a brief/);
    assert.match(named,/awaiting review/);assert.match(named,/No review recorded/);
  }
  const oldGraph=visibleRow(before,'fl:optional-return'),newGraph=visibleRow(after,'fl:optional-return');
  assert.match(oldGraph,/Who examines: original preparer \(prepared the brief\)/);
  assert.match(oldGraph,/current graph&#x27;s brief brief:original; return does not name a brief/);
  assert.match(newGraph,/Who examines: current preparer \(prepared the brief\)/);
  assert.match(newGraph,/current graph&#x27;s brief brief:replacement; return does not name a brief/);
  for(const [name,actual] of Object.entries(limits)){
    const named=visibleRow(actual,'fl:named-return'),optional=visibleRow(actual,'fl:optional-return');
    assert.match(named,/Brief preparer source: return&#x27;s named brief brief:named\./,name);
    assert.doesNotMatch(named,/last readable graph|currentness unknown/,name);
    if(name==='duplicate' || name==='duplicate-no-graph-brief')assert.equal(actual.workspace.undertakings[0].currentGraphEstablished,false,name);
    if(name==='no-graph-brief' || name==='duplicate-no-graph-brief'){
      if(name==='no-graph-brief')assert.match(named,/Who examines: named preparer \(prepared the brief\)/);
      else assert.match(named,/Who examines: examiner not established/);
      assert.match(optional,/Who examines: examiner not established/);
      if(name==='no-graph-brief')assert.match(optional,/return does not name a brief; current graph has no brief for this item/);
      else{
        assert.match(optional,/return does not name a brief; last readable graph has no brief for this item \(currentness unknown\)/);
        assert.doesNotMatch(optional,/current graph/);
      }
    }else{
      assert.match(named,/Who examines: examiner not established/,name);
      assert.match(named,/No preparer established from the named brief/,name);
      assert.doesNotMatch(named,/Who examines: (?:current preparer|executor|conflicting preparer)/,name);
      assert.match(optional,/Who examines: current preparer \(prepared the brief\)/,name);
      if(name==='duplicate'){
        assert.match(optional,/last readable graph&#x27;s brief brief:current \(currentness unknown\); return does not name a brief/);
        assert.doesNotMatch(optional,/current graph/);
      }else assert.match(optional,/current graph&#x27;s brief brief:current; return does not name a brief/,name);
    }
  }
});

test('qualified readiness and incomplete queues stay qualified in the rendered category and cause',()=>{
  const workspace={standing:'quoted fixture',graphIdentityMethod:'fixture',limits:[],undertakings:[{
    undertaking:'invented',graph:'fl:graph',revision:1,currentGraphEstablished:false,queueComplete:false,queue:[],notes:['incomplete source'],
    waiting:[{item:'W1',outcome:'invented result',owner:'recorded owner',category:'ready (qualified)',readinessQualified:true,causes:['dispatch may be unrecorded'],needs:[],sources:{}}],
  }]};
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:{...packet,workspace},error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Last readable graph; currentness unknown/);assert.match(html,/Return-review queue \(incomplete\)/);
  assert.match(html,/<strong>ready \(qualified\)<\/strong>/);assert.match(html,/dispatch may be unrecorded/);
  assert.doesNotMatch(html,/No recorded returns await/);
});

// The Delegated work view (DEL-06-02) on invented packets and decision views.

const who = 'invented executor';
const inventedPacket = (undertaking, over = {}) => ({
  format: 'invented', formatVersion: '0', standing: 'invented', project: {canonicalRoot: '/invented/project'},
  briefs: [], graphs: [], limits: [], nativeRecording: 'invented recording note',
  coordination: {projectRecords: [], governingStoreRecords: [], appObservations: [], protected: {state: 'invented store'}},
  workspace: {standing: 'Derived from invented files.', graphIdentityMethod: 'invented', limits: ['invented reconstruction limit'], undertakings: [{
    undertaking, graph: 'fl:invented-graph', revision: 2, currentGraphEstablished: true, queueComplete: true, notes: [],
    waiting: [
      {item: 'W-alpha', outcome: 'Alpha summary written', owner: who, category: 'waiting', causes: ['item W-beta: outstanding (no integration of the current return or external result recorded)'], needs: [], next: 'write the alpha summary', sources: {}},
      {item: 'W-beta', outcome: 'Beta table checked', owner: who, category: 'returned', causes: ['awaiting review'], needs: [], next: 'review the beta table', sources: {}},
    ],
    queue: [{item: 'W-beta', outcome: 'Beta table checked', returnRef: 'fl:return-beta', state: 'awaiting review', returnedBy: 'invented child', recordedBy: 'invented manager',
      examines: 'invented manager (prepared the brief)', examiner: null, examinesProvenance: {basis: 'return-brief', briefId: 'brief:beta', briefSource: {}},
      returned: [{kind: 'file', ref: 'outputs/beta-table.csv'}, {kind: 'file', ref: 'outputs/beta-notes.md'}], evidence: [], sources: []}],
    ...over,
  }]},
});
const inventedDecisions = (actKind, over = {}) => ({limits: [], writerStatus: null, rows: [{
  package: 'pkg:invented-choice', packageFile: 'decisions/invented-choice.json', actRequested: actKind, state: 'pending — awaiting the person\'s decision',
  subject: ['the invented layout'], purpose: 'choose how the invented tables are laid out', scope: 'invented report',
  alternatives: [{id: 'alt-wide', statement: 'Lay the tables out wide', consequences: ['the report needs landscape pages']}, {id: 'alt-long', statement: 'Lay the tables out long', consequences: []}],
  decision: null, limits: [], ...over,
}]});
const panel = view => React.createElement(DecisionPackagesPanel, {view, name: '', setName() {}, recordName() {}, refresh: async () => {}, continueRecording: async () => {}, openControl: async () => {}});
const render = read => renderToStaticMarkup(React.createElement(DelegatedWorkView, {read: {...UNREAD, readAt: Date.UTC(2026, 10, 12, 9), ...read}, readNow() {}, decisionPackages: panel}));
const section = (html, start, end) => html.split(start)[1].split(end)[0];

test('the view is reached from the workspace navigation by its own name', () => {
  const entry = WORKSPACE_VIEWS.find(view => view.id === 'delegated');
  assert.deepEqual({...entry}, {id: 'delegated', label: 'Delegated work', target: 'view-delegated'});
});

test('one read shows the selected work, the return queue and the decision packages, each readable without raw records', () => {
  const html = render({fleet: inventedPacket('U-invented'), decisions: inventedDecisions('A16')});
  assert.match(html, /Last read at [^<]+: complete\./);
  const undertaking = section(html, '<h3>Undertaking U-invented</h3>', '</section>');
  assert.match(undertaking, /Current graph: fl:invented-graph, revision 2/);
  const work = section(undertaking, '<h4>Selected work and waiting causes</h4>', '<h4>Return-review queue');
  for (const text of ['W-alpha: Alpha summary written', '<strong>waiting</strong>', `Owner: ${who}. Next: write the alpha summary.`, 'item W-beta: outstanding', 'W-beta: Beta table checked', '<strong>returned</strong>'])
    assert.ok(work.includes(text), text);
  const visible = work.replace(/<details>[\s\S]*?<\/details>/g, '');
  for (const text of ['Alpha summary written', 'write the alpha summary', 'item W-beta: outstanding (no integration', 'review the beta table']) assert.ok(visible.includes(text), `${text} is outside the raw-record disclosure`);
  const queue = section(undertaking, '<h4>Return-review queue (complete for the read packet)</h4>', '</section>').replace(/<details>[\s\S]*?<\/details>/g, '');
  for (const text of ['W-beta: Beta table checked</b> — awaiting review', 'Returned by invented child; recorded by invented manager.', 'Who examines: invented manager (prepared the brief).', 'No review recorded.', 'file: <code>outputs/beta-table.csv</code>', 'file: <code>outputs/beta-notes.md</code>'])
    assert.ok(queue.includes(text), text);
  const packages = section(html, 'id="delegated-decisions"', '</details>');
  for (const text of ['pkg:invented-choice — decide (A16) — pending', 'Lay the tables out wide', 'the report needs landscape pages', 'Lay the tables out long', 'Open act control (decide)', 'Subject: the invented layout'])
    assert.ok(packages.includes(text), text);
  assert.match(html, /id="delegated-sources"[\s\S]*Complete fleet packet, sources and provenance/);
  assert.doesNotMatch(html, /<button[^>]*>[^<]*(?:Dispatch|Integrate|Mark reviewed|Record|Select graph)/, 'the view offers no act on the work');
});

test('an incomplete queue and an unestablished current graph are stated where the rows are', () => {
  const html = render({fleet: inventedPacket('U-partial', {currentGraphEstablished: false, queueComplete: false}), decisions: inventedDecisions('A16')});
  const undertaking = section(html, '<h3>Undertaking U-partial</h3>', '</section>');
  assert.match(undertaking, /<strong>Limit:<\/strong> Last readable graph; currentness unknown: fl:invented-graph/);
  assert.match(undertaking, /Return-review queue \(incomplete\)<\/h4><p><strong>Limit:<\/strong> Not every record was read or established, so this queue may not be the whole\./);
  assert.match(html, /Last read at [^<]+: incomplete\./);
  assert.match(html, /the current graph of undertaking U-partial is not established/);
  assert.match(html, /the return-review queue of undertaking U-partial is incomplete/);
  const none = render({fleet: inventedPacket('U-none', {graph: null, revision: null, currentGraphEstablished: false, queueComplete: false, waiting: [], queue: [], notes: ['no current graph selected; no empty-work conclusion']}), decisions: inventedDecisions('A16')});
  const empty = section(none, '<h3>Undertaking U-none</h3>', '</section>');
  assert.match(empty, /<strong>Limit:<\/strong> No current graph established/);
  assert.match(empty, /No readable queued return shown; more work may be unrecorded or unread\./);
  assert.doesNotMatch(empty, /No recorded returns await/);
});

test('a failed read is shown and clears the earlier reading', async () => {
  const published = [];
  let failFleet = false, failDecisions = false;
  const invoke = async command => {
    if (command === 'read_fleet_records') { if (failFleet) throw new Error('fleet folder unreadable'); return inventedPacket('U-earlier'); }
    if (failDecisions) throw new Error('records store locked');
    return inventedDecisions('A16');
  };
  let clock = 0;
  const reader = createDelegatedWorkReader({invoke, publish: read => published.push(read), now: () => ++clock, timers: {set: () => 't', clear() {}}});
  await reader.readNow();
  const good = published.at(-1);
  assert.ok(render(good).includes('U-earlier'));
  failFleet = true; failDecisions = true;
  await reader.readNow();
  const bad = published.at(-1);
  assert.equal(bad.fleet, null); assert.equal(bad.decisions, null); assert.equal(bad.readAt, 2);
  const html = render(bad);
  assert.match(html, /Last read at [^<]+: failed\./);
  assert.match(html, /<div role="alert"><p>This read is not complete:/);
  assert.match(html, /<p role="alert">Fleet read failed: Error: fleet folder unreadable\. No earlier reading of the work and returns is shown\.<\/p>/);
  assert.match(html, /<p role="alert">Decision read failed: Error: records store locked\. No earlier reading of the decision packages is shown\.<\/p>/);
  for (const earlier of ['U-earlier', 'W-alpha', 'fl:return-beta', 'pkg:invented-choice', 'Complete fleet packet']) assert.ok(!html.includes(earlier), `${earlier} is not left looking current`);
});

test('a package asking for acceptance reads accept and nowhere approve', () => {
  const html = render({fleet: inventedPacket('U-invented'), decisions: inventedDecisions('A5', {package: 'pkg:invented-proposal'})});
  const packages = section(html, 'id="delegated-decisions"', '</details>');
  assert.match(packages, /pkg:invented-proposal — accept \(A5\) — pending/);
  assert.doesNotMatch(packages, /approv/i);
  assert.doesNotMatch(html, /approv/i);
});

test('the view reads when shown, re-reads on an interval without overlapping, and stops when hidden', async () => {
  const timers = new Map(); let next = 0;
  const fake = {set: (run, ms) => { const id = ++next; timers.set(id, {run, ms}); return id; }, clear: id => timers.delete(id)};
  const fire = () => { const [[id, timer]] = [...timers]; timers.delete(id); timer.run(); };
  const calls = []; const pending = [];
  const invoke = command => { calls.push(command); return new Promise(resolve => pending.push(() => resolve(command === 'decision_view' ? inventedDecisions('A16') : inventedPacket('U-invented')))); };
  const settle = async () => { while (pending.length) pending.shift()(); for (let i = 0; i < 5; i++) await Promise.resolve(); };
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  function Probe({shown}) { useDelegatedWork(shown, invoke, {timers: fake}); return null; }
  const show = shown => React.act(() => root.render(React.createElement(Probe, {shown})));

  await show(false);
  assert.equal(calls.length, 0, 'a hidden view reads nothing');
  await show(true);
  assert.deepEqual(calls, ['read_fleet_records', 'decision_view'], 'showing the view reads it');
  assert.equal(timers.size, 0, 'no second read is scheduled while one is in flight');
  await React.act(settle);
  assert.equal(timers.size, 1); assert.equal([...timers.values()][0].ms, DELEGATED_WORK_REREAD_MS);
  await React.act(async () => { fire(); });
  assert.equal(calls.length, 4, 'the interval re-reads while shown');
  await React.act(settle);
  await show(false);
  assert.equal(timers.size, 0, 'hiding the view cancels the next read');
  const before = calls.length;
  await show(false);
  assert.equal(calls.length, before, 'no read while hidden');
  await show(true);
  assert.equal(calls.length, before + 2, 'showing again reads at once');
  await React.act(settle);
  await React.act(() => root.unmount());
  assert.equal(timers.size, 0, 'unmounting leaves no scheduled read');
});
