import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const sourceUrl = new URL('../src/ConnectorRoutePanel.tsx', import.meta.url);
const compiled = ts.transpileModule(readFileSync(sourceUrl, 'utf8'), {compilerOptions: {module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX}});
const exports = {};
new Function('require', 'exports', compiled.outputText)(createRequire(sourceUrl), exports);
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
