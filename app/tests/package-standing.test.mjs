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
  assert.equal(packageStandingLine({form:'none-recorded'}),'No decision on this request is recorded.');
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
