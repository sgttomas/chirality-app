import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
const {RecordsStorePanel}=loadSrc('App');
const store=retention=>({state:'available',root:'/invented/store',placement:'test',project:{attachment:{projectId:'invented-project',limits:[]},reading:'records store',retention,notes:[]}});
const render=retention=>renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:store(retention),act:async()=>{}}));
test('closed held project keeps export and native hold release but offers no disposal',()=>{
 const html=render({closed:true,legalHold:true,disposition:'kept'});
 assert.match(html,/Export project records/);assert.match(html,/Release legal hold/);assert.match(html,/Reopen project/);assert.doesNotMatch(html,/Dispose of records after verified export/);
});
test('closed unheld records offer explicit verified disposal and active project offers closure',()=>{
 assert.match(render({closed:true,legalHold:false,disposition:'kept'}),/Dispose of records after verified export/);
 const active=render({closed:false,legalHold:false,disposition:'kept'});assert.match(active,/Close project/);assert.doesNotMatch(active,/Dispose of records after verified export/);
});
test('incomplete disposal offers recovery while disposed records offer no new mutations',()=>{
 const partial=render({closed:true,legalHold:false,disposition:'disposal incomplete'});assert.match(partial,/Finish disposal/);assert.doesNotMatch(partial,/Reopen project|Export project records|Import|Give this folder a new identity/);
 const done=render({closed:true,legalHold:false,disposition:'disposed'});assert.match(done,/Records: disposed/);assert.doesNotMatch(done,/Finish disposal|Reopen project|Dispose of records after verified export|Export project records/);
});
test('unattached missing, moved and duplicate links retain identity repair controls',()=>{
 for (const refusal of ['link missing; not attached','this folder moved; adopt or give a new identity','duplicated project identity']){
  const value=store(undefined);value.project.attachment={projectId:null,refusal,limits:[]};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.match(html,/This folder is that project/);assert.match(html,/Give this folder a new identity/);assert.match(html,/Restore the project file/);assert.doesNotMatch(html,/Dispose of records after verified export/);
 }
});
test('uncertain completion publication retains a reconciliation offer',()=>{
 const html=render({closed:true,legalHold:false,disposition:'completion durability uncertain'});
 assert.match(html,/Finish disposal/);assert.doesNotMatch(html,/Reopen project|Dispose of records after verified export/);
});
test('an incomplete disposal can be legally held and cannot finish while held',()=>{
 const pending=render({closed:true,legalHold:false,disposition:'disposal incomplete'});assert.match(pending,/Set legal hold/);assert.match(pending,/Finish disposal/);
 const held=render({closed:true,legalHold:true,disposition:'disposal incomplete'});assert.match(held,/Release legal hold/);assert.match(held,/Legal hold blocks further disposal/);assert.doesNotMatch(held,/>Finish disposal</);
});

const buttons=node=>{
 if (!node || typeof node!=='object') return [];
 if (node.type==='button') return [node];
 return [node.props?.children].flat(Infinity).flatMap(buttons);
};
test('foreign or unattached project offers separate path-free package import',async()=>{
 const value=store(undefined);value.project.attachment={projectId:null,refusal:'records were kept in another store',limits:[]};
 value.project.notImported=2;
 const calls=[];
 const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
 const html=renderToStaticMarkup(panel);
 assert.match(html,/Import verified package/);assert.match(html,/identity already named by this folder/);
 assert.match(html,/Exact bytes and the original identity are retained/);assert.match(html,/conflicting files are refused/);
 assert.match(html,/Unsigned package content stays quoted evidence/);
 assert.match(html,/This folder is that project/);
 const button=buttons(panel).find(node=>node.props.children==='Import verified package');
 assert.ok(button);await button.props.onClick();
 assert.deepEqual(calls,[['records_store_import_package',{action:'import'}]]);
});
test('interrupted package import offers only its recovery among project mutations',async()=>{
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.project.notImported=2;value.project.attachment.refusal='publication incomplete';
 value.packageImport={state:'incomplete',importId:'invented-import',packageIdentity:'invented-hash',limit:'publication durability uncertain'};
 const calls=[];
 const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
 const html=renderToStaticMarkup(panel);
 assert.match(html,/Project records remain unavailable until it is finished/);
 assert.match(html,/Finish package import/);assert.match(html,/publication durability uncertain/);
 assert.match(html,/invented-import/);assert.match(html,/invented-hash/);
 assert.doesNotMatch(html,/Import verified package|Export project records|Import 2 record|Close project|Set legal hold|This folder is that project|Give this folder a new identity/);
 const button=buttons(panel).find(node=>node.props.children==='Finish package import');
 assert.ok(button);await button.props.onClick();
 assert.deepEqual(calls,[['records_store_import_package',{action:'resume'}]]);
});
test('unknown package import status remains unavailable without offering a guessed recovery',()=>{
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.packageImport={state:'unavailable',limit:'intent cannot be read'};
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(html,/Package import status is unavailable/);assert.match(html,/intent cannot be read/);
 assert.doesNotMatch(html,/Import verified package|Finish package import|Export project records|Close project/);
 assert.match(html,/Verify an exported package/);
});
test('completed package import preserves normal controls and legacy import remains distinct',async()=>{
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.project.notImported=2;value.packageImport={state:'complete',importId:'invented-complete'};
 const calls=[];
 const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
 const html=renderToStaticMarkup(panel);
 assert.match(html,/Import verified package/);assert.match(html,/Import 2 record file/);assert.match(html,/Close project/);
 assert.match(html,/Package import: complete/);assert.match(html,/invented-complete/);
 const legacy=buttons(panel).find(node=>Array.isArray(node.props.children)&&node.props.children[0]==='Import ');
 assert.ok(legacy);await legacy.props.onClick();
 assert.deepEqual(calls,[['records_store_import']]);
});
test('terminal disposal never offers a new package import',()=>{
 for (const disposition of ['disposed','disposal incomplete','completion durability uncertain']) {
  assert.doesNotMatch(render({closed:true,legalHold:false,disposition}),/Import verified package/);
 }
});
test('unavailable retention keeps package recovery offered without guessing its history',()=>{
 const value=store({disposition:'unavailable',limit:'administrative event is missing'});
 value.project.attachment.refusal='retention state unavailable';
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(html,/Import verified package/);assert.match(html,/administrative event is missing/);
 assert.match(html,/Retention state unavailable\. Project closure and legal hold are unknown/);
 assert.doesNotMatch(html,/Project open\.|Legal hold: not set/);
 assert.doesNotMatch(html,/Close project|Set legal hold|Export project records|This folder is that project|Give this folder a new identity/);
});

test('linkless and startup identity projects offer native-validated identity restoration',async()=>{
 for (const attachment of [
  {projectId:null,refusal:'project link is missing',limits:[]},
  {projectId:'invented-startup-Q',limits:[]},
 ]) {
  const value=store(undefined);value.project.attachment=attachment;
  const calls=[];
  const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
  const html=renderToStaticMarkup(panel);
  assert.match(html,/Restore project from package/);assert.match(html,/The App checks whether/);
  assert.match(html,/unused identity created at startup/);
  assert.match(html,/refuses to replace an identity with records, a legal hold, closure or disposal/);
  assert.match(html,/retains existing bytes/);
  const button=buttons(panel).find(node=>node.props.children==='Restore project from package');
  assert.ok(button);await button.props.onClick();
  assert.deepEqual(calls,[['records_store_import_package',{action:'restore'}]]);
 }
});
test('displayed identity alone makes no promise that native restoration will replace it',()=>{
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.project.reading='records store';value.project.attachment.projectId='invented-used-Q';
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(html,/Restore project from package/);assert.match(html,/The App checks whether/);
 assert.match(html,/refuses to replace an identity with records/);
 assert.doesNotMatch(html,/identity can be replaced|identity is unused/);
});
test('missing package controls offer repair only on explicit native capability',async()=>{
 for (const state of ['unavailable','incomplete']) {
  const value=store({disposition:'unavailable',limit:'administrative history is unreadable'});
  value.packageImport={state,canRepair:true,needsPackage:true,reason:'original package must be selected again'};
  const calls=[];
  const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
  const html=renderToStaticMarkup(panel);
  assert.match(html,/Repair package controls/);assert.match(html,/original package must be selected again/);
  assert.match(html,/Original package needed for repair: yes/);assert.match(html,/native selector will ask you to choose it again/);
  assert.match(html,/original native intent and retained evidence/);assert.match(html,/missing original act keep recovery held/);
  assert.match(html,/Package claims stay quoted evidence and grant no authority to replay acts/);
  assert.doesNotMatch(html,/Restore project from package|Import verified package|This folder is that project/);
  const button=buttons(panel).find(node=>node.props.children==='Repair package controls');
  assert.ok(button);await button.props.onClick();
  assert.deepEqual(calls,[['records_store_import_package',{action:'repair'}]]);
 }
 for (const canRepair of [undefined,false,'true']) {
  const value=store(undefined);value.packageImport={state:'unavailable',canRepair,reason:'intent.json is missing'};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.match(html,/intent.json is missing/);assert.doesNotMatch(html,/Repair package controls/);
 }
});
test('interrupted association retains Finish with absent or startup link',async()=>{
 for (const projectId of [null,'invented-startup-Q']) {
  const value=store(undefined);value.project.attachment={projectId,limits:[]};
  value.packageImport={state:'incomplete',canRepair:false,needsPackage:false,reason:'identity association is unfinished'};
  const calls=[];
  const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
  const html=renderToStaticMarkup(panel);
  assert.match(html,/Finish package import/);assert.match(html,/identity association is unfinished/);
  assert.match(html,/Original package needed for repair: no/);
  assert.doesNotMatch(html,/Restore project from package|Repair package controls|Import verified package/);
  const button=buttons(panel).find(node=>node.props.children==='Finish package import');
  assert.ok(button);await button.props.onClick();
  assert.deepEqual(calls,[['records_store_import_package',{action:'resume'}]]);
 }
});
test('terminal disposal and unavailable store never offer restoration or control repair',()=>{
 for (const disposition of ['disposed','disposal incomplete','completion durability uncertain']) {
  const value=store({closed:true,legalHold:false,disposition});
  value.packageImport={state:'unavailable',canRepair:true};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.doesNotMatch(html,/Restore project from package|Repair package controls|Import verified package/);
 }
 const value=store(undefined);value.state='unavailable';value.packageImport={state:'unavailable',canRepair:true};
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.doesNotMatch(html,/Restore project from package|Repair package controls|Import verified package/);
});
test('native repairReason explains capability refusal or package selection without duplicate diagnostics',()=>{
 const value=store({disposition:'unavailable'});
 value.packageImport={state:'unavailable',canRepair:false,repairReason:'Original native intent is missing; recovery stays held.'};
 const refusal=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(refusal,/Package repair: Original native intent is missing; recovery stays held\./);
 assert.doesNotMatch(refusal,/Repair package controls|Restore project from package/);
 value.packageImport={state:'unavailable',canRepair:true,needsPackage:true,repairImports:['invented-import'],repairReason:'Select the exact original package to restore private custody.'};
 const recovery=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(recovery,/Repair package controls/);assert.match(recovery,/Package repair: Select the exact original package/);
 assert.match(recovery,/Original package needed for repair: yes/);
 for (const diagnostics of [
  {reason:'Repeated repair diagnostic.',repairReason:'Repeated repair diagnostic.'},
  {limit:'Repeated repair diagnostic.',repairReason:'Repeated repair diagnostic.'},
  {reason:'Repeated repair diagnostic.',limit:'Repeated repair diagnostic.',repairReason:'Repeated repair diagnostic.'},
 ]) {
  value.packageImport={state:'unavailable',canRepair:false,...diagnostics};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.equal(html.split('Repeated repair diagnostic.').length-1,1);
 }
});
