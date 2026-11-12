import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {loadSrc} from './support/load-src.mjs';
import './support/rust-prebuild.mjs';
const {DecisionPackagesPanel}=loadSrc('App');

// The decision view an actual reader case prints: an invented act record that
// names its recorder as the decision actor. DEL-06-02 Decision row: such a
// record is listed as a claim and decides nothing.
function actualView(test='decision_view::tests::decision_view_a_record_naming_its_recorder_as_actor_is_listed_as_a_claim',marker='DECISION_VIEW_CLAIM_DTO:'){
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib',test,'--','--exact','--nocapture','--test-threads=1'],{
    cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr);
  const line=proc.stdout.split('\n').find(line=>line.includes(marker));assert.ok(line);
  return JSON.parse(line.slice(line.indexOf(marker)+marker.length));
}
const decode=html=>html.replace(/&#x27;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const render=view=>decode(renderToStaticMarkup(React.createElement(DecisionPackagesPanel,{view,name:'',setName:()=>{},recordName:()=>{},refresh:async()=>{},continueRecording:async()=>{},openControl:async()=>{}})));

test('a record that cannot decide is shown under a heading that says claims decide nothing, with its origin, recorder, actor, choice and identity',()=>{
  const view=actualView();
  const row=view.rows[0];
  const claim=row.claims.find(c=>c.recordId==='rec:a1');assert.ok(claim);
  const html=render(view);
  assert.match(html,/Claims — these decide nothing/);
  assert.match(html,/None of them decides this package or changes its standing/);
  for(const text of ['Record rec:a1',claim.origin,'names its recorder','agent:invented-manager','alternative it chose: ALT-2']) assert.ok(html.includes(text),text);
  assert.doesNotMatch(html,/— decided</);
});

test('every kind of claim the reader lists is rendered, including what it claimed to correct',()=>{
  const view={rows:[{package:'rec:r1',actRequested:'A16',state:'ambiguous current standing',requests:['rec:r1'],alternatives:[],contenders:[],limits:[],
    claims:[{recordId:'rec:fix',origin:"legacy-imported copy of a project file (quoted evidence)",reason:"legacy-imported copy of a project file (quoted evidence)",claimedToCorrect:'rec:a2',recordedBy:{role:'App interface',identity:'writer:fix'},actor:'Invented (identity not verified)',alternativeChosen:'ALT-9'},
      {recordId:'rec:lapse',origin:'project-file claim',reason:'project-file claim',claimedToObserve:'rec:a1',recordedBy:{role:'App writer',identity:'writer:lapse'},actor:null,alternativeChosen:null}]}],limits:[]};
  const html=render(view);
  assert.match(html,/Record rec:fix · origin: legacy-imported copy of a project file \(quoted evidence\)/);
  assert.match(html,/claimed to correct rec:a2/);
  assert.match(html,/Record rec:lapse · origin: project-file claim/);
  assert.match(html,/claimed a lapse of rec:a1/);
  assert.match(html,/actor it names: none named/);
});

test('a row resting only on an imported request says so, and that the request supplies none of the facts a decision rests on',()=>{
  const view=actualView('decision_view::tests::decision_view_a_row_resting_only_on_an_imported_request_says_so','DECISION_VIEW_REQUEST_CLAIM_DTO:');
  assert.equal(view.rows[0].restsOnClaimRequest,true);
  const html=render(view);
  assert.match(html,/This row rests only on a request that is a claim \(legacy-imported copy of a project file \(quoted evidence\)\)/);
  assert.match(html,/supplies none of the facts a decision rests on/);
  assert.match(html,/that request's claim; a decision is read from the act and the package file's own current bytes/);
});

test('claims that cite no package are listed at view level, and an unknown past with matching content is said both ways',()=>{
  const view={rows:[{package:'rec:r1',actRequested:'A16',state:'decided',requests:['rec:r1'],alternatives:[],contenders:[],limits:[],claims:[],
    decision:{act:'rec:a1',alternativeChosen:'ALT-2',lapse:'not lapsed',lapseShown:'the current content is what was decided; whether it lapsed in between is not known',captureProvenance:'recorded claim'}}],
    claims:[{recordId:'rec:stray',origin:'project-file claim',reason:'project-file claim',request:'rec:unknown',recordedBy:{role:'agent',identity:'agent:x'},actor:null,alternativeChosen:'ALT-1'}],limits:[]};
  const html=render(view);
  assert.match(html,/the current content is what was decided; whether it lapsed in between is not known/);
  assert.doesNotMatch(html,/>not lapsed ·/);
  assert.match(html,/They cite no package shown here and decide nothing/);
  assert.match(html,/Record rec:stray · origin: project-file claim/);
});
