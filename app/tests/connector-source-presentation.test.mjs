import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const url=new URL('../src/ConnectorSourcePanel.tsx',import.meta.url);
const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);
const {SourceObservationView,ConnectorSourcePanel,sourceUiTransition,emptySourceUi}=exports;
const question={id:'Q-fixture',text:'What can be read?',askedRevision:'typed-commit',sinceRevision:'typed-since'};
const view={question,trigger:{kind:'absent',standing:'constructed caller context'},operation:'observed',gaps:[{reason:'Revision unverified',effect:'No source/account',responsible:null}],limits:['No continuous pathname guarantee','No coherent historical revision'],dutiesStanding:'Unperformed/outstanding; no duty authored',observation:{reference:'opaque',question,historical:false,read:{displayPath:'fixture.txt',selectedPath:{encoding:'fixture'},openedFileIdentity:{inode:'18446744073709551615'},text:'<script>do not run</script>\r\né\n',sha256:'host-buffer-hash',byteLength:32,lineCount:2,observedAt:'fixture-time',timeProvenance:'fixture-only',mechanism:'injected picker fixture, not person evidence',mutationLimit:'Transient writes can evade metadata checks'},revision:{kind:'unavailable',limit:'No revision evidence supplied'},anchors:[{reference:'anchor-id',anchor:'L1',byteStart:0,byteEnd:3,interval:'zero-based half-open',text:'é\n',sha256:'excerpt-hash',standing:'Inclusion only, not truth'}]}};
const state=(v=view)=>({view:v,busy:false,error:null,draftChanged:false});
const render=s=>renderToStaticMarkup(React.createElement(SourceObservationView,{state:s}));
test('source content, anchors, read limits and gaps remain escaped and separate',()=>{
 const html=render(state());
 for(const text of ['Q-fixture','typed-commit','typed-since','Revision unverified','Unassigned','Transient writes','No coherent historical revision','host-buffer-hash','excerpt-hash','[0, 3)','Inclusion only','18446744073709551615'])assert.ok(html.includes(text),text);
 assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));assert.ok(!html.includes('<a '));assert.ok(html.includes('\\r\\n'));
 assert.match(html,/Git verification is unavailable/);assert.match(html,/No source entry or saved route account is produced/);
});
test('every revision treatment retains unverified provenance and typed hashes cannot promote it',()=>{
 for(const kind of ['unavailable','caller_assertion','source_text_located']){
  const v=structuredClone(view);v.observation.revision={kind,label:'0123456789abcdef',callerInterpretation:'Caller meaning',limit:'Unverified assertion; not Git evidence',...(kind==='source_text_located'?{anchor:{anchor:'L1'}}:{})};
  const html=render(state(v));assert.ok(html.includes(kind));assert.match(html,/not Git evidence/);assert.match(html,/working-tree coincidence does not establish a Git revision/);
 }
});
test('cancel, pending, failure and edited question label old snapshot historical with unchanged read time',()=>{
 for(const change of [{view:{...view,operation:'cancelled',observation:{...view.observation,historical:true}}},{busy:true},{error:'read failed'},{draftChanged:true}]){
  const html=render({...state(),...change});assert.match(html,/Prior\/historical observation/);assert.match(html,/fixture-time/);assert.match(html,/Frozen question: Q-fixture/);
 }
 const next=sourceUiTransition(state(),{type:'prepare'});assert.equal(next.view,null);
 const fail=sourceUiTransition(sourceUiTransition(state(),{type:'start'}),{type:'failure',error:'failure'});assert.equal(fail.view,view);assert.match(render(fail),/prior\/historical/);
 assert.equal(sourceUiTransition(state(),{type:'edit'}).draftChanged,true);
 assert.equal(sourceUiTransition(emptySourceUi,{type:'success',view}).draftChanged,false);
});
test('constructed trigger variants preserve question and gaps; assignments are never performed duties',()=>{
 for(const kind of ['absent','stale','partial','failing']){
  const v=structuredClone(view);v.trigger.kind=kind;v.gaps[0].responsible='Caller assigned manager';
  const html=render(state(v));assert.match(html,/What can be read\?/);assert.match(html,/Revision unverified/);assert.match(html,/caller assignment, not performed responsibility/);assert.match(html,/Unperformed\/outstanding/);
 }
});
test('unavailable association disables preparation/selection and exposes no file path/body input',()=>{
 const html=renderToStaticMarkup(React.createElement(ConnectorSourcePanel,{availability:{enabled:false,reason:'No explicit project'},command(){throw Error('render must not invoke');}}));
 assert.match(html,/No explicit project/);assert.ok((html.match(/<button disabled=""/g)||[]).length>=2);
 assert.ok(!html.includes('type="file"'));assert.ok(!html.includes('name="path"'));assert.match(html,/262144/);assert.match(html,/no NUL or symlink descendants/);
});

test('historical excerpts retain separately labeled unresolved read and excerpt causes',()=>{
 const v=structuredClone(view);v.operation='failed';v.observation.historical=true;
 v.gaps.push({kind:'Selection/read',reason:'DISTINCT_READ_FAILURE',effect:'No new source observation',responsible:null},{kind:'Excerpt',reason:'Expected excerpt mismatch',effect:'No new anchor',responsible:null});
 const html=render(state(v));for(const value of ['Selection/read gap','DISTINCT_READ_FAILURE','Excerpt gap','Expected excerpt mismatch','No new source observation','No new anchor'])assert.ok(html.includes(value),value);
 assert.match(html,/Prior\/historical observation/);assert.match(html,/fixture-time/);
});
