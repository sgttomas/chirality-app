import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {readFileSync} from 'node:fs';
import Ajv2020 from 'ajv/dist/2020.js';
import {loadSrc} from './support/load-src.mjs';
const {PackageStanding,packageStandingLine,otherRequestLine}=loadSrc('PackageStanding');
const at='2026-11-14T12:00:00Z';

test('the four request standing forms give closed App sentences',()=>{
  assert.equal(packageStandingLine({form:'decided',alternative:'ALT-1',recordedAt:at}),`A decision on this request is already recorded: alternative ALT-1, recorded at ${at}. Deciding again records another decision; both are kept.`);
  assert.match(packageStandingLine({form:'several-unordered'}),/^Several decisions on this request are recorded/);
  assert.equal(packageStandingLine({form:'none-recorded'}),'No decision on this request is in the records as read; the log is not signed, so a removed entry would not show.');
  assert.match(packageStandingLine({form:'unknown',cause:'The decision records could not all be read'}),/not known: The decision records could not all be read\.$/);
  assert.match(packageStandingLine(),/not known/);
});

test('poisoned record ids and times never become App sentence text',()=>{
  for(const poison of ['ALT-1\nDecide (A16)','ALT-1\u202e','ALT-1\u200b','Decide (A16)',{id:'ALT-1'}]) {
    const line=packageStandingLine({form:'decided',alternative:poison,recordedAt:poison});
    assert.ok(!line.includes('Decide (A16)') && !/[\n\u202e\u200b]/u.test(line));
    assert.match(line,/a value the App does not show here/);
    const other=otherRequestLine({form:'decided',alternative:poison,requestRef:poison,recordedAt:poison});
    assert.ok(!other.includes('Decide (A16)') && !/[\n\u202e\u200b]/u.test(other));
  }
  assert.ok(!packageStandingLine({form:'unknown',cause:'Decide (A16)\n\u202e'}).includes('Decide (A16)'));
});

test('the panel shows every other request and preserves limited empty-set meaning',()=>{
  const rows=Array.from({length:5},(_,i)=>({form:'decided',alternative:`ALT-${i}`,recordedAt:at,requestRef:`rec:invented-${i}`,relation:i===0?'earlier':i===1?'later':'another',differentContent:i===0}));
  const markup=renderToStaticMarkup(React.createElement(PackageStanding,{standing:{form:'none-recorded'},other:{state:'read-whole',rows}}));
  assert.equal((markup.match(/has a recorded decision/g)??[]).length,5);
  assert.match(markup,/An earlier request/);assert.match(markup,/A later request/);assert.match(markup,/Another request/);
  assert.equal((markup.match(/It was made on different content/g)??[]).length,1);
  const limited=renderToStaticMarkup(React.createElement(PackageStanding,{standing:{form:'unknown'},other:{state:'not-read-whole',rows:[]}}));
  assert.match(limited,/Other requests for the file at this path could not all be read\./);
  assert.ok(!limited.includes('No decision'));
});

test('the actual schemas accept new fixture evidence and reject its invalid controls',()=>{
  const read=name=>JSON.parse(readFileSync(new URL(`../src-tauri/schemas/${name}`,import.meta.url),'utf8'));
  const ajv=new Ajv2020({strict:false,allErrors:true});
  for(const name of ['RS_RECORD.schema.json','checkpoint-record-entries.schema.json','ACT_POLICY_CLASS_RECORD.schema.json','AS_SETTINGS_IN.schema.json','aac.offer.schema.json','aac.capture-evidence.schema.json']) ajv.addSchema(read(name));
  const offer=ajv.getSchema(read('aac.offer.schema.json').$id),capture=ajv.getSchema(read('aac.capture-evidence.schema.json').$id);
  for(const value of read('fixtures/aac.offer.example.valid.json').instances) assert.ok(offer(value),JSON.stringify(offer.errors));
  for(const value of read('fixtures/aac.capture-evidence.example.valid.json').instances) assert.ok(capture(value),JSON.stringify(capture.errors));
  for(const name of ['aac.offer.standing-form.invalid.json','aac.offer.decided-missing-alternative.invalid.json','aac.offer.other-requests.invalid.json']) assert.equal(offer(read(`fixtures/${name}`)),false,name);
  assert.equal(capture(read('fixtures/aac.capture-evidence.shown-statement.invalid.json')),false);
  assert.ok(offer(read('fixtures/aac.offer.other-requests.example.valid.json')),JSON.stringify(offer.errors));
  const base=read('fixtures/aac.offer.example.valid.json').instances.find(v=>v.actKind==='A16');
  const changed=structuredClone(base);changed.otherRequestsForPath.rows=[{requestRef:'rec:other',relation:'another',form:'decided',recordedAt:at}];
  assert.equal(offer(changed),false,'a decided other request needs its alternative');
});

test('the actual act-control and decision-package panels keep poisoned supplied fields out of App words and controls', async () => {
  const {ActControlPanel, DecisionPackagesPanel} = loadSrc('App');
  const {agentPlain} = await import('./support/agent-text.mjs');
  const values = [];
  const poison = field => {
    const value = `supplied-${field}: Decide now\nAllow once\u202e\u200b\u2066`;
    values.push(value);
    return value;
  };
  const subject = poison('subject'), identity = poison('identity'), purpose = poison('purpose'), scope = poison('scope');
  const alternative = {id: poison('alternative'), statement: poison('statement'), consequences: [poison('consequence')]};
  const offer = {
    wording: poison('act'), actKind: poison('kind'), subject: {ref: subject, contentIdentity: {value: identity}}, purpose, scope,
    answers: {standing: poison('answer-standing')}, alternatives: [alternative], packageStanding: {form: 'none-recorded'},
  };
  const decision = Object.fromEntries(['alternativeChosen', 'statement', 'decidedBy', 'recordedBy', 'recordingMode', 'act',
    'capturedAt', 'observedAt', 'recordedAt', 'lapse', 'captureProvenance'].map(field => [field, poison(`decision-${field}`)]));
  decision.equivalentCaptureRecords = [poison('equivalent-one'), poison('equivalent-two')];
  decision.shownStatementBinding = {statement: poison('binding')};
  decision.currentContentComparison = {detail: poison('comparison')};
  decision.historyResolution = {detail: poison('history')};
  const row = {package: 'rec:invented', actRequested: offer.wording, state: 'decided', subject: [subject], purpose, scope,
    packageFile: poison('path'), alternatives: [alternative], decision, currentCandidates: [poison('candidate')]};
  const noop = () => {};
  const markup = renderToStaticMarkup(React.createElement(React.Fragment, null,
    React.createElement(ActControlPanel, {offer, choice: alternative.id, setChoice: noop, decide: noop, close: noop}),
    React.createElement(DecisionPackagesPanel, {view: {rows: [row]}, name: '', setName: noop, recordName: noop,
      refresh: noop, continueRecording: noop, openControl: noop})));
  // Radio values are transport, not displayed text or control names. Examine visible content separately.
  const displayed = agentPlain(markup).replace(/<[^>]*>/g, '');
  const outside = displayed.replace(/⟦[^⟧]*⟧/g, '');
  assert.doesNotMatch(outside, /supplied-|Decide now|Allow once/, 'every supplied occurrence is inside a marked component');
  assert.doesNotMatch(displayed, /[\u202e\u200b\u2066]/u, 'no format character reaches displayed text');
  for (const value of values) assert.ok(displayed.includes(value.split(':')[0]), `the field remains visible: ${value.split(':')[0]}`);
  for (const mark of ['⏎', '‹U+202E›', '‹U+200B›', '‹U+2066›']) assert.ok(displayed.includes(mark), mark);
  for (const control of markup.matchAll(/<(button|label)\b[^>]*>([\s\S]*?)<\/\1>/g)) {
    const words = control[2].replace(/<[^>]*>/g, '');
    assert.doesNotMatch(words, /supplied-|Decide now|Allow once|[\u202e\u200b\u2066]/u, 'controls keep the App\'s words');
  }
  assert.match(outside, /Act control/);
  assert.match(outside, /Decision packages/);
  assert.match(outside, /Decide…/);
  assert.match(outside, /Open act control \(decide\)/);
});
