// Current real Host LT23 publication + independent legacy/current schema controls.
// All peers/data are invented fixtures; no native person/supplier qualification.
import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import Ajv2020 from 'ajv/dist/2020.js';
const app=new URL('../',import.meta.url);
const design=new URL('../execution/PKG-01/DEL-01-01/Design/',app);
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const current=load(new URL('hosting.lifecycle-event.v0.10.schema.json',design));
const legacy=load(new URL('hosting.lifecycle-event.schema.json',design));
const ajv=new Ajv2020({strict:false,allErrors:true});
const validate=ajv.compile(current),old=ajv.compile(legacy);
const out=mkdtempSync(`${tmpdir()}/custody-json-`);after(()=>rmSync(out,{recursive:true}));
let actual;
test('actual Host unknown census survives current publication and JSON presentation',()=>{
 execFileSync('cargo',['test','--offline','--locked','--lib','process_group_custody_unknown_census_is_null_in_actual_current_publish_readback','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_TEST_OUTPUT_DIRECTORY:out},stdio:'inherit'});
 actual=load(`${out}/process-group-custody-current.json`);
 assert.equal(actual.state,'read');assert.equal(actual.evidence.lifecycle.format,'lifecycle-event.s1.v0.10');
 const row=actual.evidence.lifecycle.legacy_event;assert.ok(validate(row),JSON.stringify(validate.errors));
 assert.deepEqual(row.descendants.checked,false);assert.equal(row.descendants.surviving,null);
 // App's raw native-view presentation performs this JSON serialization, with
 // no replacement of absent counts by zero. Test its actual producer result.
 const appSource=readFileSync(new URL('src/App.tsx',app),'utf8');
 assert.match(appSource,/JSON\.stringify\(\{ current: host\?\.nativeView/);
 const displayed=JSON.stringify({current:{distributionEvidence:actual}},null,2);
 assert.match(displayed,/"surviving": null/);assert.match(displayed,/unavailable: invented partial owned-group inventory/);
 assert.doesNotMatch(displayed,/"surviving": 0/);assert.match(displayed,/original reserved process group only; detached\/escaped descendants unobserved/);
});
test('current profile keeps exact counts separate from unavailable; legacy unchanged',()=>{
 const row=structuredClone(actual.evidence.lifecycle.legacy_event);
 for(const descendants of [{checked:true,surviving:0},{checked:true,surviving:2},{checked:false,surviving:null,handling:'unavailable: source error'}]){row.descendants=descendants;assert.ok(validate(row),JSON.stringify(validate.errors));}
 for(const descendants of [{checked:true,surviving:null},{checked:true,surviving:-1},{checked:false,surviving:0},{checked:false,surviving:null},{checked:false,surviving:null,handling:'none surviving'}]){row.descendants=descendants;assert.equal(validate(row),false);}
 row.descendants={checked:false,surviving:0};assert.ok(old(row),'legacy unchecked integer remains readable');
 const envelope=load(new URL('distribution-s1/lifecycle-event.s1.v0.10.schema.json',design));const wrapper=ajv.compile(envelope);const dto=structuredClone(actual.evidence.lifecycle);assert.ok(wrapper(dto));dto.format='lifecycle-event.future';assert.equal(wrapper(dto),false);
});
