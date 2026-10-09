import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const sourceUrl = new URL('../src/ConnectorRoutePanel.tsx', import.meta.url);
const compiled = ts.transpileModule(readFileSync(sourceUrl, 'utf8'), {compilerOptions: {module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX}});
const reconstructionUrl=new URL('../src/ConnectorReconstruction.tsx',import.meta.url);
const reconstructionCode=ts.transpileModule(readFileSync(reconstructionUrl,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}}).outputText;
const reconstructionExports={};new Function('require','exports',reconstructionCode)(createRequire(reconstructionUrl),reconstructionExports);
const connectedRequire=name=>name==='./ConnectorReconstruction'?reconstructionExports:createRequire(sourceUrl)(name);
const exports = {};
new Function('require', 'exports', compiled.outputText)(connectedRequire, exports);
const {ConnectorRoutePanel, routeReadTransition, emptyRouteRead} = exports;
const fixture = JSON.parse(readFileSync(new URL('./fixtures/connector-route-source-walk.json', import.meta.url), 'utf8'));
const labels = {question:'Question',trigger:'Trigger',sources:'Sources and revisions',facts:'Anchored facts',gaps:'Gaps, effects and responsibility',conclusions:'Supported, unsupported and prohibited conclusions',duties:'Duties',recorder:'Recorder',written_at:'Written time',written_at_source:'Time provenance'};
function account(value=fixture, path='a.json') {
  return {questionText:value.question.text,gaps:value.gaps,duties:value.duties,relativePath:path,accountId:value.account_id,bindingText:'{"inode":18446744073709551615}',accountText:JSON.stringify(value),sourceCount:value.sources.length,sections:Object.entries(labels).map(([key,label])=>({label,text:JSON.stringify(value[key])??'Not recorded'}))};
}
function render(view, availability={enabled:true}, state={busy:false,view,error:null}) {
  return renderToStaticMarkup(React.createElement(ConnectorRoutePanel,{availability,state,onRead(){throw Error('render must not perform reads');}}));
}
const observed = (accounts=[account()]) => ({status:'observed',directoryAbsent:false,enumerationComplete:true,accounts,issues:[],byAccountId:{}});
const escape = text => text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#x27;');
test('selected manual walk: every recorded field is rendered unchanged for four constructed triggers',()=>{
  for (const trigger of ['absent','stale','partial','failing']) {
    const value=structuredClone(fixture);
    if(trigger!=='absent') value.trigger.why=`CONSTRUCTED ${trigger} trigger`;
    assert.deepEqual(value.question,fixture.question); assert.deepEqual(value.facts,fixture.facts);
    const html=render(observed([account(value)]));
    for(const key of Object.keys(labels)) assert.ok(html.includes(escape(JSON.stringify(value[key]))),key);
    assert.match(html,/recorded claims/); assert.match(html,/not resolved against a separately held prior reference/);
    assert.match(html,/18446744073709551615/);
  }
});
test('all duty states, missing metadata, zero-source gaps, and conflicting claims remain literal',()=>{
  for(const standing of ['outstanding','prepared','performed','not_required']) {
    const value=structuredClone(fixture); value.sources=[]; value.facts=[]; value.conclusions.supported=[];
    value.duties=[{duty:'locate_compare',actor_role:'agent',standing,reason:'recorded only',...(standing==='performed'?{actor:'recorded actor',evidence:'literal evidence'}:{})}];
    delete value.written_at_source;
    const html=render(observed([account(value)]));
    assert.match(html,/No sources are recorded/); assert.ok(html.includes(standing));
    assert.match(html,/Not recorded/); assert.match(html,/Missing metadata remains missing/);
    assert.ok(html.includes('NOT READY')); assert.ok(html.includes('unsupported'));
  }
});
test('duplicate IDs retain separate cards without winner, all discovery issues and incomplete state',()=>{
  const view=observed([account(fixture,'a.json'),account(fixture,'b.json')]);
  view.byAccountId={[fixture.account_id]:['a.json','b.json']}; view.enumerationComplete=false;
  view.issues=['DuplicateIdentity','InvalidAccount','UnsupportedFormat','UnsafeEntry','TemporaryLeftover','IncompleteDiscovery'].map(kind=>({kind,relative_path:kind+'.json',detail:'observed problem'}));
  const html=render(view);
  assert.equal((html.match(/<article>/g)||[]).length,2); assert.match(html,/No winner selected/); assert.match(html,/Enumeration is incomplete/);
  for(const issue of view.issues) assert.ok(html.includes(issue.kind));
});
test('absent, empty, unavailable, and open failure are distinct; absent project disables read',()=>{
  assert.match(render({...observed([]),directoryAbsent:true}),/canonical account directory is absent/);
  assert.match(render(observed([])),/No valid accounts were observed/);
  assert.match(render({status:'project_open_failed',error:{kind:'Io'}}),/could not be opened/);
  for(const status of ['no_project','unknown_association','invalid_association','association_mismatch']) {
    const html=render(null,{enabled:false,status,reason:'refused'});
    assert.match(html,/<button disabled=""/); assert.ok(html.includes(status));
  }
});
test('untrusted text stays escaped and source paths are not opened; exact large-number text survives',()=>{
  const a=account(); a.sections[0].text='<script>alert("x")</script> & 9007199254740993';
  const html=render(observed([a]));
  assert.ok(html.includes('&lt;script&gt;')); assert.ok(!html.includes('<script>')); assert.match(html,/9007199254740993/);
  assert.ok(!html.includes('<a ')); assert.ok(!html.includes('<input'));
});
test('refresh clears old observation immediately and failure cannot retain stale success',()=>{
  const old={busy:false,view:observed(),error:null};
  const pending=routeReadTransition(old,{type:'start'}); assert.equal(pending.view,null); assert.equal(pending.busy,true);
  const failed=routeReadTransition(pending,{type:'failure',error:'read failure'}); assert.equal(failed.view,null);
  assert.match(render(null,{enabled:true},failed),/Previous results have been cleared/);
  assert.equal(routeReadTransition(old,{type:'clear'}),emptyRouteRead);
  assert.equal(routeReadTransition(pending,{type:'success',view:old.view}).view,old.view);
});

test('parsed representation and numeric limitations are visible without implying original bytes',()=>{
  const html=render(observed());
  assert.match(html,/host-parsed fields/); assert.match(html,/Full host-parsed account/);
  assert.match(html,/not original file bytes/); assert.match(html,/normalize formatting and may round large integers or high-precision decimals/);
  assert.match(html,/cannot recover precision already lost by the host parser/);
  assert.match(html,/binding hash identifies bytes observed by the host/);
  assert.match(html,/does not verify those bytes or certify the precision/);
  assert.ok(!html.includes('exact recorded fields')); assert.ok(!html.includes('Complete recorded account'));
});
test('format0.3 cold draft shows typed responsibility and cannot promote compact receipts or interpretations',()=>{
 const a=account();a.formatVersion='0.3';a.standing='source_evidence_draft';a.draftSources=[{source_id:'source',path:'literal.txt',revision:'commit',role:'Caller purpose',sha256:'blob-hash',provenance:{side:'at',blob:'blob-id',verification:'same_engine_object_id_consistency'},excerpts:[{excerpt_id:'excerpt',anchor:'L1',byte_start:0,byte_end:4,text:'<hostile>excerpt',standing:'exact_byte_inclusion_only'}]}];a.interpretations=[{interpretation_id:'interpretation',statement:'Visible unreviewed statement',asserted_by:'Asserted identity',attribution_standing:'caller_asserted_identity',standing:'unreviewed_caller_interpretation',source_ids:['source'],excerpt_ids:['excerpt']}];a.gaps=[{gap:'Recorded failure',effect:'No source',responsible:{standing:'unassigned',identity:null}},{gap:'Caller gap',effect:'Unreviewed',responsible:{standing:'caller_assigned',identity:'<script>caller</script>'}}];a.sections.push({label:'Compact evidence receipt and limits',text:'{"device":"18446744073709551617","custody_limit":"stored_receipt_not_hot_capability_or_independent_reverification"}'},{label:'Unreviewed caller interpretations',text:'{"asserted_by":"Caller identity","standing":"unreviewed_caller_interpretation"}'});
 const html=render(observed([a]));for(const text of ['Source-evidence draft','not a reconstructed answer','Unassigned','caller assigned, unverified','18446744073709551617','pre-read allocation','Unreviewed caller interpretations','Caller identity','Visible unreviewed statement','Asserted identity','blob-id','exact_byte_inclusion_only'])assert.ok(html.includes(text),text);assert.ok(!html.includes('<script>'));assert.ok(html.includes('&lt;script&gt;caller'));
});
test('0.4 keeps mechanical evidence, attributed claims and reported performance distinct and escaped',()=>{
 const a=JSON.parse(readFileSync(new URL('../src-tauri/resources/connector_route/record_reconstruction_v04.fixture.json',import.meta.url),'utf8'));
 a.claims[0].statement='<script>the work is complete</script>';a.contribution_reports[0].reported_actor='<img onerror=run>';
 const dto={...account(a),formatVersion:'0.4',standing:a.standing,draftSources:a.sources,reconstruction:a};const html=render(observed([dto]));
 for(const label of ['Mechanical observations','different_excerpt_bytes','not verified truth','unverified_contribution_report','performance not_established','does not change actual duty standing','None reported; absence not proved',a.sources[0].sha256,a.sources[1].sha256,'f-since','f-at'])assert.ok(html.includes(label),label);
 assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));assert.ok(html.includes('&lt;img'));
 a.sources=[];a.facts=[];a.comparisons=[];a.claims=[];a.contribution_reports=[];const empty=render(observed([{...account(a),formatVersion:'0.4',reconstruction:a}]));assert.ok(!empty.includes('the work is complete'));assert.ok(empty.includes('No sources are recorded'));
});
test('answer-only view consumes actual filesystem read-backend projection and preserves recorded-only standing',async()=>{
 const {mkdtempSync,rmSync}=await import('node:fs');const {tmpdir}=await import('node:os');const {join}=await import('node:path');const {spawnSync}=await import('node:child_process');const {fileURLToPath}=await import('node:url');
 const dir=mkdtempSync(join(tmpdir(),'ao-view-'));const output=join(dir,'projection.json');
 try{
  const result=spawnSync('cargo',['test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--lib','connector_answer_only_actual_read_projection_and_write_barrier'],{cwd:fileURLToPath(new URL('..',import.meta.url)),env:{...process.env,CARGO_NET_OFFLINE:'true',CARGO_INCREMENTAL:'0',CHIRALITY_SKIP_CODEX:'1',CHIRALITY_AO_VIEW_EXPORT:output},encoding:'utf8',timeout:120000});
  assert.equal(result.status,0,result.stderr||result.error?.message);const projected=JSON.parse(readFileSync(output,'utf8'));const ao=projected.accounts.find(a=>a.formatVersion==='0.5');assert.ok(ao,'actual constructed files were admitted by the backend');
  const html=render({...projected,accounts:[ao]});for(const text of ['Recorded answer-only account','Internally consistent receipt strings can be fabricated','Manager review and integration outstanding','Human responsibilities remain separate','900719925474099312345','known exact','post-acquisition','Original account text observed by the host'])assert.ok(html.toLowerCase().includes(text.toLowerCase()),text);
  assert.ok(html.includes('&lt;script&gt;Recorded answer&lt;/script&gt;'));assert.ok(!html.includes('<script>'));assert.ok(html.includes(ao.recordedAnswerAccount.base_account.sha256));assert.ok(!html.includes('No sources are recorded'));assert.ok(!html.includes('Recorded duties'));assert.ok(html.includes(ao.answerOnly.answer.claims[0].claim_id));
 }finally{rmSync(dir,{recursive:true,force:true});}
});
