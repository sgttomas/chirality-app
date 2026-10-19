import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {WorkflowRegistrationReview} = loadSrc('WorkflowRegistrationReview');
const {App,WorkflowRootPanel} = loadSrc('App');
const presentationSource = loadSrc('presentation');
const {canonicalJson,readablePaths,reviewDigest} = presentationSource;
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const reviews = container => container.querySelectorAll(node => node.getAttribute('aria-label') === 'Frozen workflow registration review');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
// Exclude expandable diagnostic copies: the ordinary reading surface must
// carry the text and metadata, rather than relying on escaped raw JSON.
const readingText = node => node.localName === 'details' ? '' : node.nodeType === 3 ? node.textContent : node.childNodes.map(readingText).join('');
function freeze(value) {
  if (value && typeof value === 'object') {Object.values(value).forEach(freeze);Object.freeze(value);}
  return value;
}
function strings(value) {
  return typeof value === 'string' ? [value] : value && typeof value === 'object' ? Object.values(value).flatMap(strings) : [];
}
let packet;
function actualReviewPacket() {
  if (packet) return packet;
  const cached = process.env.CHIRALITY_REGISTRATION_REVIEW_DTO_LOG ?? process.env.CHIRALITY_LIBRARY_ENTRIES_DTO_LOG;
  let output;
  if (cached) output = readFileSync(cached,'utf8');
  else {
    // Existing Rust producer, one offline check. No native confirmation,
    // supplier turn or new Rust fixture is needed for this display repair.
    const producer = 'runtime_session::workflow_root_tests::library_entries_tests::library_entries_real_observation_ordered_subset_to_existing_review_packet';
    const result = spawnSync('cargo',['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual Rust producer checks completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::library_entries_tests::library_entries_real_observation_ordered_subset_to_existing_review_packet/);
  const marker = 'LISTED_LIBRARY_ENTRIES_DTO:';
  const captured = output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  assert.equal(captured.length,1,'one actual Rust review packet');
  packet = freeze(captured[0]);
  return packet;
}
async function mount(Component,properties) {
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  const render = async next => React.act(() => root.render(React.createElement(Component,next)));
  await render(properties);
  return {container,render,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);}};
}
function assertActualReading(view,presentation) {
  const entries = labelled(view,'Reviewed workflow order');
  assert.equal(entries.childNodes.length,presentation.entries.length);
  assert.deepEqual(entries.childNodes.map(li => nodes(li,'h4')[0].textContent),presentation.entries.map(entry => entry.identity.name));
  assert.deepEqual(view.querySelectorAll(node => node.getAttribute('aria-label') === 'Frozen WORKFLOW.md text').map(node => node.textContent),presentation.entries.map(entry => entry.workflow_text));
  for (const value of strings(presentation)) assert.ok(readingText(view).includes(value),`ordinary reading surface retains ${value}`);
  assert.equal(nodes(view,'button').length,0,'the presentation component supplies no act control');
  const raw = nodes(view,'details').find(node => nodes(node,'summary')[0]?.textContent === 'Complete reported review (diagnostic JSON)');
  assert.equal(nodes(raw,'pre')[0].textContent,JSON.stringify(presentation,null,2),'diagnostic report keeps the exact complete DTO, including unknown fields');
}

test('real Rust frozen presentation is literal, ordered, complete and leaves canonical input unchanged',async () => {
  const source = actualReviewPacket(),review = source.reviewed.reviews.find(row => row.reference === source.reviewed.activeReview);
  assert.ok(review?.status.presentation);
  const presentation = review.status.presentation,before = canonicalJson(presentation),digest = await reviewDigest(presentation);
  const view = await mount(WorkflowRegistrationReview,{presentation});
  try {assertActualReading(reviews(view.container)[0],presentation);}
  finally {await view.close();}
  assert.equal(canonicalJson(presentation),before);
  assert.equal(await reviewDigest(presentation),digest);
});

test('both actual App placements consume the same frozen Rust presentation and native content withdraws without acts',async t => {
  const source = actualReviewPacket(),presentation = source.reviewed.reviews[0].status.presentation;
  const before = canonicalJson(presentation),digest = await reviewDigest(presentation);
  // The wrapper is source-grounded in a15_in_app/showing_in_app. Its digest
  // is computed here; this is no live native alert or Rust capture evidence.
  let rows = [{kind:'A15 complete review',digest,digestMethod:'sha-256 of the aac-offer-digest/0.1 canonical form',content:presentation,
    standing:'reading aid while a native confirmation is open; the host checks the binding at capture'}];
  const calls = [],hashInputs = [],hashes = [],previous = window.__TAURI_INTERNALS__;
  t.mock.timers.enable({apis:['setInterval']});
  t.mock.method(presentationSource,'reviewDigest',value => {hashInputs.push(value);const pending = reviewDigest(value);hashes.push(pending);return pending;});
  window.__TAURI_INTERNALS__ = {invoke:async (command,args) => {
    calls.push([command,args]);
    if (command === 'host_status') return {...source.host,workflowRoot:source.reviewed};
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return rows;
    assert.equal(command,'workflow_review_digest','only the existing read commands run');
    assert.equal(args.reviewRef,source.reviewed.activeReview);return {digest};
  }};
  let view;
  try {
    view = await mount(App,{});
    await React.act(async () => {await Promise.all(hashes);});
    assert.equal(reviews(view.container).length,2,'root and open-native surfaces use the shared component');
    for (const rendered of reviews(view.container)) assertActualReading(rendered,presentation);
    assert.ok(hashInputs.length >= 2);
    assert.ok(hashInputs.every(value => value === presentation),'existing digest paths receive the original presentation object');
    const open = labelled(view.container,'Content named by an open native confirmation');
    assert.ok(open.textContent.includes(digest));
    assert.ok(open.textContent.includes('This view recomputed the same digest'));
    assert.equal(nodes(open,'button').length,0);
    const register = nodes(view.container,'button').find(node => node.textContent === 'Register this review through native A15 confirmation…');
    assert.ok(register);assert.equal(props(register).disabled,false);
    const current = view.container.querySelectorAll(node => node.localName === 'article' && nodes(node,'h3').some(h => h.textContent === `Current review · ${source.reviewed.activeReview}`))[0];
    const orderedText = current.textContent;
    assert.ok(orderedText.indexOf(digest) < orderedText.indexOf('Read the complete review below before choosing Register'));
    assert.ok(orderedText.indexOf('Read the complete review below before choosing Register') < orderedText.indexOf(register.textContent));
    assert.ok(orderedText.indexOf(register.textContent) < orderedText.indexOf(presentation.entries[0].workflow_text));
    rows = [];
    await React.act(async () => {t.mock.timers.tick(1000);});
    assert.equal(labelled(view.container,'Content named by an open native confirmation'),undefined);
    assert.equal(reviews(view.container).length,1,'root review remains while the withdrawn native copy is removed');
    assert.equal(canonicalJson(presentation),before);
    assert.equal(await reviewDigest(presentation),digest);
    assert.ok(calls.every(([command]) => ['host_status','decision_view','native_confirmation_content','workflow_review_digest'].includes(command)));
  } finally {if (view) await view.close();window.__TAURI_INTERNALS__ = previous;}
});

test('native rendering requires the exact A15 kind and compatible entries; other content keeps its existing JSON view',async t => {
  const source = actualReviewPacket(),actual = source.reviewed.reviews[0].status.presentation;
  const contents = [
    {kind:'A16 alternative',content:{...actual,syntheticShapeProbe:'other native kind'}},
    {kind:'A15 complete review ',content:{...actual,syntheticShapeProbe:'near-match kind'}},
    {kind:'A15 complete review',content:{entries:[null],syntheticShapeProbe:'incompatible entry'}},
    {kind:'A15 complete review',content:{entries:'unavailable',syntheticShapeProbe:'incompatible entries'}},
  ];
  const rows = await Promise.all(contents.map(async row => ({...row,digest:await reviewDigest(row.content)})));
  const previous = window.__TAURI_INTERNALS__;
  t.mock.timers.enable({apis:['setInterval']});
  window.__TAURI_INTERNALS__ = {invoke:async command => {
    if (command === 'host_status') return {...source.host,workflowRoot:{...source.reviewed,reviews:[]}};
    if (command === 'decision_view') return {rows:[]};
    assert.equal(command,'native_confirmation_content');return rows;
  }};
  let view;
  try {
    view = await mount(App,{});
    const open = labelled(view.container,'Content named by an open native confirmation');
    assert.ok(open);assert.equal(reviews(open).length,0);
    assert.deepEqual(nodes(open,'pre').map(node => node.textContent),rows.map(row => JSON.stringify(readablePaths(row.content),null,2)));
  } finally {if (view) await view.close();window.__TAURI_INTERNALS__ = previous;}
});

test('source-grounded hand-built DS-2 and DS-8 variants retain full tuples, findings, limits, unknowns and literal text safely',async () => {
  // Hand-built display coverage, NOT live producer/capture evidence. Field
  // shapes follow workflow_library.rs compose_presentation/reconfirmation_view
  // and workflow_declaration.rs Declaration/Element. The actual DTO above
  // independently covers producer-to-consumer correspondence.
  const presentation = structuredClone(actualReviewPacket().reviewed.reviews[0].status.presentation);
  const entry = presentation.entries[0];
  const prior = {...entry.identity,revision:'prior-full-revision-aaaaaaaaaaaaaaaa',derived_from:null};
  const base = {...prior,revision:'base-full-revision-bbbbbbbbbbbbbbbb'};
  entry.disposition = 'new revision';entry.prior_revision = prior;entry.base = base;entry.stale_base = true;entry.lineage = base;
  entry.identity.derived_from = base;entry.message = 'Registers new revision in the project library; earlier revisions are kept';
  entry.reviewed_reference = `draft:project:${entry.identity.name}@${entry.content.value}`;
  entry.workflow_text = '# Frozen <script>globalThis.unwanted = true</script>\nKeep "quotes", \\slashes, tabs\tand Unicode Ω.\n';
  entry.prior_comparison = {identity:prior,files:structuredClone(entry.files),changes:[{path:'WORKFLOW.md',before:'prior-exact-file-sha256-cccccccccccc',after:entry.files[0].content.value}],limit:'comparison with stored bytes; old native origin not authenticated'};
  entry.base_comparison = {identity:base,comparison:'unavailable',reason:'Synthetic stored base bytes unavailable'};
  entry.declaration = {raw:{required_tools:[{kind:'synthetic-tool',value:'raw declaration prose\nsecond line'}]},reading:'invalid',
    categories:{required_tools:'invalid',expected_inputs:'declared_empty'},elements:{'tool:synthetic':{value:{name:'synthetic tool'},reading:'invalid',findings:['FB-4 synthetic element finding']}},findings:['FB-2 synthetic declaration finding','FB-5 another synthetic finding']};
  entry.hygiene = ['HY-4 synthetic reported finding'];
  entry.base_observation = {observed:{source:'App data folder',record:{base_recorded_by:'app'}},standing:'Synthetic App-kept observation; freshness evidence, not replay proof'};
  entry.evidence_limits.push('Synthetic source limit');
  entry.files[0].extra_manifest_field = 'Unknown manifest detail';
  entry.future_entry_field = {null_value:null,empty_list:[],empty_object:{},empty_string:'',zero:0,flag:false,unavailable:'Synthetic explicit unavailability'};
  const reconfirm = structuredClone(entry);
  reconfirm.disposition = 're-confirmation';reconfirm.identity = {...prior,name:'reconfirm-synthetic'};
  reconfirm.content = {method:reconfirm.identity.revision_method,value:reconfirm.identity.revision};
  reconfirm.prior_revision = {...entry.identity,name:reconfirm.identity.name};reconfirm.base = reconfirm.identity;reconfirm.lineage = null;
  reconfirm.reviewed_reference = `draft:project:${reconfirm.identity.name}@${reconfirm.content.value}`;
  reconfirm.prior_comparison.identity = reconfirm.prior_revision;
  reconfirm.base_comparison = {identity:reconfirm.base,files:structuredClone(reconfirm.files),changes:[],limit:entry.prior_comparison.limit};
  reconfirm.message = 'Identical to revision 7, registered earlier (not verified in this session). Re-confirm revision 7 for use in this App session; no new revision is registered';
  reconfirm.reconfirmation = {revision:prior.revision,sequence:7,reconfirms:{identity:reconfirm.identity,ledger_seq:9,sequence:7},standing:'LS-1 registered, as read (registered earlier; not verified in this session)',
    registered_earlier:{written_at:'synthetic earlier time',act:'synthetic act ref',label:'registered earlier; not verified in this session'},slot_latest:reconfirm.prior_revision,
    statement:'Re-confirm revision 7 for use in this App session. This registers no new revision.',limit:'Synthetic cold-read limit; earlier act is not replayed'};
  reconfirm.registration_notice = 'Re-confirming makes revision 7 available in this App session. It registers no new revision, and it is not a check that the workflow can run here.';
  reconfirm.workflow_text = null;delete reconfirm.files;
  presentation.entries = [entry,reconfirm];
  presentation.future_report_field = {source:'Synthetic unknown future source',limit:'Synthetic unknown future limit'};
  presentation.future_special_keys = JSON.parse('{"constructor":"Unknown constructor field","toString":"Unknown toString field","__proto__":"Unknown __proto__ field"}');
  presentation.library = {encoding:'unix_bytes',bytes:[47,116,109,112,47,255],future_path_field:'Unknown path detail'};
  freeze(presentation);
  const before = canonicalJson(presentation),digest = await reviewDigest(presentation);
  const view = await mount(WorkflowRegistrationReview,{presentation});
  try {
    const rendered = reviews(view.container)[0],text = readingText(rendered);
    for (const value of ['prior-full-revision-aaaaaaaaaaaaaaaa','base-full-revision-bbbbbbbbbbbbbbbb','prior-exact-file-sha256-cccccccccccc',entry.content.method,entry.content.value,
      entry.workflow_text,'Synthetic stored base bytes unavailable','FB-4 synthetic element finding','FB-2 synthetic declaration finding','FB-5 another synthetic finding',
      'HY-4 synthetic reported finding','Synthetic source limit','Unknown manifest detail','Synthetic unknown future source','Synthetic unknown future limit',
      entry.ledger_observation.standing,entry.registration_notice,reconfirm.registration_notice,reconfirm.reconfirmation.statement,
      presentation.same_name_elsewhere.standing,presentation.compatibility,'Reported null','Not reported','Reported empty list','Reported empty object','Reported empty string','false']) assert.ok(text.includes(value),value);
    assert.ok(text.includes('future_entry_field'));assert.ok(text.includes('future_report_field'));
    for (const [key,value] of Object.entries(presentation.future_special_keys)) {assert.ok(text.includes(key));assert.ok(text.includes(value));}
    assert.ok(rendered.textContent.includes('Unknown path detail'),'native path identity retains all original fields in its diagnostic copy');
    assert.ok(text.includes('path is not valid UTF-8'));
    assert.equal(nodes(rendered,'button').length,0);
    assert.equal(nodes(rendered,'script').length,0);
    const html = renderToStaticMarkup(React.createElement(WorkflowRegistrationReview,{presentation}));
    assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));
    assert.equal(globalThis.unwanted,undefined);
    const raw = nodes(rendered,'details').find(node => nodes(node,'summary')[0]?.textContent === 'Complete reported review (diagnostic JSON)');
    assert.equal(nodes(raw,'pre')[0].textContent,JSON.stringify(presentation,null,2));
    assert.equal(canonicalJson(presentation),before);assert.equal(await reviewDigest(presentation),digest);
  } finally {await view.close();}
});

test('current review stays first and retained presentations stay labelled with disabled native controls',async () => {
  const source = actualReviewPacket(),current = source.reviewed.reviews[0];
  // UI-only retained owner wrapper around the actual frozen presentation.
  const retained = {...current,reference:'synthetic-retained-review-owner'};
  const data = {...source.reviewed,reviews:[retained,current]},previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke:async command => {assert.equal(command,'workflow_review_digest');return {unavailable:'Synthetic digest reader outside native host'};}};
  let view;
  try {
    view = await mount(WorkflowRootPanel,{data,host:source.host,act:async () => {assert.fail('rendering sends no act');}});
    const owners = view.container.querySelectorAll(node => node.localName === 'article' && nodes(node,'h3').some(h => /^(Current|Retained) review ·/.test(h.textContent)));
    assert.deepEqual(owners.map(owner => nodes(owner,'h3')[0].textContent),[`Current review · ${current.reference}`,`Retained review · ${retained.reference}`]);
    assert.equal(props(nodes(owners[0],'button').find(node => node.textContent.startsWith('Register this review'))).disabled,false);
    assert.equal(props(nodes(owners[1],'button').find(node => node.textContent.startsWith('Register this review'))).disabled,true);
  } finally {if (view) await view.close();window.__TAURI_INTERNALS__ = previous;}
});
