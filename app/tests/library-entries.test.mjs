import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {WorkflowRootPanel} = loadSrc('App');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const button = (container,label) => nodes(container,'button').find(node => node.textContent === label);
let packet;
function actualListingPacket() {
  if (packet) return packet;
  let output;
  if (process.env.CHIRALITY_LIBRARY_ENTRIES_DTO_LOG) output = readFileSync(process.env.CHIRALITY_LIBRARY_ENTRIES_DTO_LOG,'utf8');
  else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib','runtime_session::workflow_root_tests::library_entries_tests','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual Rust library-entry checks completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::library_entries_tests::/);
  const captured = marker => output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  const main = captured('LISTED_LIBRARY_ENTRIES_DTO:'),refusals = captured('LISTED_LIBRARY_ENTRIES_REFUSALS_DTO:');
  assert.equal(main.length,1,'one actual opened-library review evidence packet');
  assert.equal(refusals.length,1,'one actual stale observation refusal packet');
  packet = {...main[0],refusals:refusals[0].refusals};
  return packet;
}
async function press(container,label) {
  const control = button(container,label);assert.ok(control,label);assert.equal(!!props(control).disabled,false,label);
  await React.act(async () => {await props(control).onClick();});
}
async function pick(container,name,checked = true) {
  const control = labelled(container,`Review entry ${name}`);assert.ok(control,name);assert.equal(!!props(control).disabled,false,name);
  await React.act(() => props(control).onChange({target:{checked}}));
}
async function mount(data,act,hostOverrides = {}) {
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  const render = async next => React.act(() => root.render(React.createElement(WorkflowRootPanel,{data:next,host:{state:'not started',generation:null,threads:[],...hostOverrides,workflowRoot:next},act})));
  await render(data);
  return {container,render,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);}};
}

async function mountActual(data,host,route) {
  const calls = [],readCalls = [],previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke:async (command,args) => {
    readCalls.push([command,args]);assert.equal(command,'workflow_review_digest','the actual review offers no automatic native capture');
    return {unavailable:'Native digest display outside this mounted fixture'};
  }};
  function Panel() {
    const [current,setCurrent] = React.useState(data);
    const act = async (command,args) => {
      calls.push([command,structuredClone(args)]);
      const response = await route(command,args);
      if (response.root) setCurrent(response.root);
      if (Object.hasOwn(response,'error')) throw response.error;
      return response.result;
    };
    return React.createElement(WorkflowRootPanel,{data:current,host:{...host,workflowRoot:current},act});
  }
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  await React.act(() => root.render(React.createElement(Panel)));
  return {container,calls,readCalls,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}};
}

const listed = {reference:'listing:synthetic-a',libraryRef:'library:a',observedAt:'synthetic observation',state:'observed',
  source:{origin:'project',sourceRoot:'/synthetic/project-a',root:{encoding:'unix_bytes',bytes:[47,115,121,110,116,104,101,116,105,99,47,112,114,111,106,101,99,116,45,97]}},
  entries:[
    {reference:'entry:first',name:'first-method',state:'present without registration record',reviewable:true,content:{method:'synthetic-method',value:'first-content'},fileCount:2,bytes:120,findings:[]},
    {reference:'entry:second',name:'second-method',state:'present without registration record',reviewable:true,content:{method:'synthetic-method',value:'second-content'},fileCount:1,bytes:80,findings:[]},
    {reference:'entry:invalid',name:'broken-method',state:'not valid',reviewable:false,content:null,findings:['HY-1: WORKFLOW.md missing'],limit:'cannot review a package without WORKFLOW.md'},
  ],limits:[],standing:'Observed files only; not registration or selection'};
const initial = {context:{sourceRef:'source:a',generation:null,historyEpoch:null},activeLibrary:'library:a',libraries:[
  {reference:'library:a',origin:'project',sourceRoot:'/synthetic/project-a',registered:[],entryListing:listed}],reviews:[],runs:[]};
const libraryIn = (root,reference) => {
  const library = root.libraries.find(row => row.reference === reference);assert.ok(library,`actual library ${reference}`);return library;
};
const contextFor = root => ({sourceRef:root.context.sourceRef,generation:root.context.generation,historyEpoch:root.context.historyEpoch ?? null,
  threadId:null,selectionRef:null,inspectionRef:root.inspection?.reference ?? null,libraryRef:root.activeLibrary ?? null});

test('opened-library entries are visible without a running conversation and explicit picks preserve review order', async () => {
  const calls = [];const view = await mount(initial,async (...args) => {calls.push(args);return {};});
  try {
    const section = labelled(view.container,'Library entries available for review');
    assert.ok(section,'the opened library exposes its observed entries');
    assert.match(section.textContent,/project.*\/synthetic\/project-a/);
    assert.match(section.textContent,/first-method/);assert.match(section.textContent,/second-method/);
    assert.match(section.textContent,/HY-1: WORKFLOW.md missing/);
    assert.equal(!!props(labelled(section,'Review entry broken-method')).disabled,true);
    assert.equal(!!props(button(section,'Review chosen entries…')).disabled,true);
    assert.deepEqual(calls,[],'mounting a cached observation neither scans nor opens a review');
    await pick(section,'second-method');await pick(section,'first-method');
    assert.deepEqual(nodes(labelled(section,'Entry review order'),'li').map(row => row.textContent),['second-method','first-method']);
    assert.deepEqual(calls,[],'choosing entries is not a review or registration');
    await press(section,'Review chosen entries…');
    assert.deepEqual(calls,[['workflow_review_library_entries',{libraryRef:'library:a',listingRef:listed.reference,entryRefs:['entry:second','entry:first'],context:{sourceRef:'source:a',generation:null,historyEpoch:null,threadId:null,selectionRef:null,inspectionRef:null,libraryRef:'library:a'}}]]);
    assert.ok(!nodes(section,'button').some(row => /Select|Register|confirmation/.test(row.textContent)),'file presence creates no native act or selection control');
  } finally {await view.close();}
});

test('explicit refresh blocks concurrent picks and review and a new observation clears the old choices', async () => {
  const deferred = Promise.withResolvers(),calls = [];
  const view = await mount(initial,async (...args) => {calls.push(args);return deferred.promise;});
  try {
    let section = labelled(view.container,'Library entries available for review');
    await pick(section,'first-method');
    const refresh = props(button(section,'Refresh library entries')).onClick;
    let first,second;
    await React.act(async () => {first = refresh();second = refresh();await Promise.resolve();});
    assert.equal(calls.length,1,'two presses before a response do not start parallel observations');
    assert.deepEqual(calls[0],['workflow_library_entries_refresh',{libraryRef:'library:a',context:{sourceRef:'source:a',generation:null,historyEpoch:null,threadId:null,selectionRef:null,inspectionRef:null,libraryRef:'library:a'}}]);
    assert.ok(nodes(section,'button').every(row => !!props(row).disabled));
    assert.ok(nodes(section,'input').every(row => !!props(row).disabled));
    await React.act(async () => {deferred.resolve({});await Promise.all([first,second]);});
    const refreshed = {...initial,libraries:[{...initial.libraries[0],entryListing:{...listed,reference:'listing:synthetic-refreshed'}}]};
    await view.render(refreshed);
    section = labelled(view.container,'Library entries available for review');
    assert.equal(labelled(section,'Entry review order'),undefined,'a new host observation does not inherit picks from another listing');
    assert.equal(!!props(button(section,'Review chosen entries…')).disabled,true);
    assert.equal(calls.length,1,'receiving a new observation performs no additional read or review');
  } finally {await view.close();}
});

test('a retained review press keeps its original library and listing after the current library changes', async () => {
  const calls = [];const view = await mount(initial,async (...args) => {calls.push(args);throw 'Original displayed library changed; refresh before review';});
  try {
    let section = labelled(view.container,'Library entries available for review');
    await pick(section,'second-method');
    const retained = props(button(section,'Review chosen entries…')).onClick;
    const other = {...initial,activeLibrary:'library:b',libraries:[...initial.libraries,{reference:'library:b',origin:'user',sourceRoot:'/synthetic/user',registered:[],entryListing:{...listed,reference:'listing:b',libraryRef:'library:b',source:{origin:'user',sourceRoot:'/synthetic/user'},entries:[]}}]};
    await view.render(other);
    assert.deepEqual(calls,[],'switching libraries neither reviews old picks nor chooses replacements');
    section = labelled(view.container,'Library entries available for review');
    assert.match(section.textContent,/user.*\/synthetic\/user/);
    assert.equal(labelled(section,'Entry review order'),undefined);
    await React.act(async () => {await retained();});
    assert.deepEqual(calls,[['workflow_review_library_entries',{libraryRef:'library:a',listingRef:listed.reference,entryRefs:['entry:second'],context:{sourceRef:'source:a',generation:null,historyEpoch:null,threadId:null,selectionRef:null,inspectionRef:null,libraryRef:'library:a'}}]],'the original callback cannot substitute the newly opened library or same-named entry');
    assert.match(view.container.textContent,/Original displayed library changed; refresh before review/);
    assert.equal(labelled(section,'Entry review order'),undefined);
  } finally {await view.close();}
});

test('unobserved, absent and unavailable lists remain distinct and permit only explicit refresh', async () => {
  const calls = [];
  for (const listing of [undefined,{state:'not observed',entries:[],limits:[]},{...listed,entries:[],state:'observed'},{...listed,entries:[],state:'absent'},{...listed,entries:[],state:'unavailable',limits:['Synthetic library read denied']}]) {
    const view = await mount({...initial,libraries:[{...initial.libraries[0],entryListing:listing}]},async (...args) => {calls.push(args);return {};});
    try {
      const section = labelled(view.container,'Library entries available for review');
      assert.match(section.textContent,new RegExp(`Listing: ${listing?.state ?? 'not observed'}`));
      if (!listing || listing.state === 'not observed') {
        assert.match(section.textContent,/Open or refresh this library/);
        assert.doesNotMatch(section.textContent,/not bound to this opened library/,'an unobserved cache is a normal initial state');
      }
      if (listing?.state === 'observed') assert.match(section.textContent,/No library entries were observed/);
      if (listing?.state === 'unavailable') assert.match(section.textContent,/Synthetic library read denied/);
      if (listing?.state === 'absent') assert.match(section.textContent,/no workflow entries folder/);
      assert.equal(!!props(button(section,'Review chosen entries…')).disabled,true);
      const before = calls.length;await press(section,'Refresh library entries');assert.equal(calls.length,before+1);
    } finally {await view.close();}
  }
  assert.ok(calls.every(([command]) => command === 'workflow_library_entries_refresh'));
});

test('actual opened-library observation reaches the existing owned review in the person’s pick order without selecting or registering', async () => {
  const source = actualListingPacket(),selection = source.selection;
  const original = libraryIn(source.initial,selection.libraryRef),refreshed = libraryIn(source.refreshed,selection.libraryRef);
  assert.ok(original.entryListing.entries.some(row => row.reviewable === true),'the explicit library open actually observed existing unregistered files');
  assert.equal(refreshed.entryListing.reference,selection.listingRef);
  assert.ok(selection.entryRefs.length >= 2,'the actual path includes an ordered multi-entry review');
  const picked = selection.entryRefs.map(reference => {
    const entry = refreshed.entryListing.entries.find(row => row.reference === reference);
    assert.equal(entry?.reviewable,true);assert.ok(entry.content?.value);return entry;
  });
  const review = source.reviewed.reviews.find(row => row.reference === source.reviewed.activeReview);
  assert.ok(review?.status.presentation,'the host opened the existing native-owned review');
  assert.deepEqual(review.status.presentation.entries.map(row => row.identity.name),picked.map(row => row.name));
  assert.deepEqual(review.status.presentation.entries.map(row => row.content),picked.map(row => row.content),'each review remains bound to the observed package content');
  assert.ok(review.status.presentation.entries.every(row => row.disposition === 'in place'));
  assert.deepEqual(source.reviewed.selections,source.refreshed.selections);
  assert.deepEqual(source.reviewed.runs,source.refreshed.runs);
  assert.deepEqual(libraryIn(source.reviewed,selection.libraryRef).registered,refreshed.registered,'opening a review registers no revision');
  const view = await mountActual(source.initial,source.host,async (command,args) => {
    if (command === 'workflow_library_entries_refresh') {
      assert.deepEqual(args,{libraryRef:selection.libraryRef,context:contextFor(source.initial)});
      return {root:source.refreshed,result:source.refreshed};
    }
    assert.equal(command,'workflow_review_library_entries');
    assert.deepEqual(args,{...selection,context:contextFor(source.refreshed)});
    return {root:source.reviewed,result:source.reviewed};
  });
  try {
    let section = labelled(view.container,'Library entries available for review');
    assert.deepEqual(view.calls,[]);assert.deepEqual(view.readCalls,[],'mounting the actual opened library performs no further host read');
    assert.ok(section.textContent.includes(original.entryListing.source.sourceRoot));
    assert.equal(button(view.container,'Register this review through native A15 confirmation…'),undefined);
    await press(section,'Refresh library entries');
    section = labelled(view.container,'Library entries available for review');
    for (const entry of refreshed.entryListing.entries) {
      const checkbox = labelled(section,`Review entry ${entry.name}`);
      assert.ok(checkbox,entry.name);
      assert.equal(!!props(checkbox).disabled,entry.reviewable !== true,'the renderer follows actual host eligibility without deriving registration from presence');
      if (entry.limit) assert.ok(section.textContent.includes(entry.limit));
    }
    for (const entry of picked) await pick(section,entry.name);
    assert.deepEqual(nodes(labelled(section,'Entry review order'),'li').map(row => row.textContent),picked.map(row => row.name));
    assert.equal(view.calls.length,1,'picks remain local until the separate review press');
    await press(section,'Review chosen entries…');
    assert.equal(view.calls.length,2);
    assert.deepEqual(view.calls[1],['workflow_review_library_entries',{...selection,context:contextFor(source.refreshed)}]);
    const native = button(view.container,'Register this review through native A15 confirmation…');
    assert.ok(native,'the existing A15 control appears only after the actual review opens');
    assert.equal(!!props(native).disabled,false);
    assert.ok(view.container.textContent.includes('native A15 not captured'));
    assert.ok(view.readCalls.every(([command]) => command === 'workflow_review_digest'),'review display performs only the existing digest read, never native confirmation or registration');
    assert.ok(!view.calls.some(([command]) => /select|register|send|prepare_run/.test(command)),'discovery and review imply no workflow use, human act or supplier send');
  } finally {await view.close();}
});

test('actual changed entry, source, active library and refreshed observation refusals stay named without review or retarget', async () => {
  const source = actualListingPacket();
  const changes = ['content','entry replacement','library replacement','library switch','refresh'];
  const refusals = source.refusals.filter(row => changes.includes(row.change));
  assert.deepEqual(refusals.map(row => row.change).sort(),[...changes].sort());
  for (const refusal of refusals) {
    const library = libraryIn(refusal.before,refusal.selection.libraryRef);
    const picked = refusal.selection.entryRefs.map(reference => {
      const entry = library.entryListing.entries.find(row => row.reference === reference);assert.equal(entry?.reviewable,true);return entry;
    });
    assert.equal(refusal.after.activeReview,null,'the actual refused host path owns no new A15 offer');
    assert.deepEqual(refusal.after.reviews,[]);
    const view = await mountActual(refusal.before,refusal.host,async (command,args) => {
      assert.equal(command,'workflow_review_library_entries');
      assert.deepEqual(args,{...refusal.selection,context:contextFor(refusal.before)});
      return {root:refusal.after,error:refusal.error};
    });
    try {
      const section = labelled(view.container,'Library entries available for review');
      assert.deepEqual(view.calls,[]);assert.deepEqual(view.readCalls,[]);
      for (const entry of picked) await pick(section,entry.name);
      await press(section,'Review chosen entries…');
      assert.ok(view.container.textContent.includes(refusal.error),`the ${refusal.change} refusal keeps its actual cause`);
      assert.equal(view.calls.length,1,'a refusal never falls back to another entry, refreshes, opens review or performs an act');
      assert.deepEqual(view.readCalls,[],'no review digest or native confirmation exists after refusal');
      assert.equal(button(view.container,'Register this review through native A15 confirmation…'),undefined);
      if (refusal.change === 'library switch') {
        const current = libraryIn(refusal.after,refusal.after.activeLibrary);
        assert.ok(labelled(view.container,'Library entries available for review').textContent.includes(current.sourceRoot));
        assert.equal(labelled(view.container,'Entry review order'),undefined,'no old pick follows into the newly opened library');
      }
    } finally {await view.close();}
  }
});
