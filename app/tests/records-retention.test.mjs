import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
const {RecordsStorePanel}=loadSrc('RecordsStorePanel');
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
// The host names the fault and the acts that resolve it (records_store.rs,
// Attachment::resolutions); the cases are the ones its tests establish.
const RESTORE=/>Restore the project file</, ADOPT=/>This folder is the project its file names</, FRESH=/>Give this folder a new identity</;
const identityCases=[
 {fault:'link missing',resolutions:['restore-link','new-identity'],recordedHere:'invented-P',says:/project file is missing/},
 {fault:'link unreadable',resolutions:['restore-link','new-identity'],recordedHere:'invented-P',says:/project file cannot be read/},
 {fault:'link changed',resolutions:['restore-link','adopt','new-identity'],recordedHere:'invented-P',linkedIdentity:'invented-Q',says:/names a different project than the one recorded for this folder/},
 {fault:'link changed',resolutions:['restore-link','new-identity'],recordedHere:'invented-P',linkedIdentity:'invented-Q',says:/names a different project/},
 {fault:'moved',resolutions:['adopt','new-identity'],linkedIdentity:'invented-Q',says:/recorded for another folder/},
 {fault:'duplicated',resolutions:['new-identity'],linkedIdentity:'invented-Q',says:/treated as a copy/,one:true},
 {fault:'another store',resolutions:['adopt','new-identity'],linkedIdentity:'invented-Q',says:/kept in another records store/},
 {fault:'several identities',resolutions:['new-identity'],says:/recorded for more than one project/,one:true},
 {fault:'link names another store',resolutions:['restore-link'],recordedHere:'invented-P',linkedIdentity:'invented-P',says:/names another records store than this one, so its records are not attached/,one:true},
];
test('an unattached project offers exactly the acts that resolve its fault, in plain words',async()=>{
 for (const item of identityCases){
  const value=store(undefined);value.project.attachment={projectId:null,refusal:`${item.fault}; not attached`,limits:[],...item};
  const calls=[];
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async(...args)=>{calls.push(args);}}));
  assert.match(html,item.says);assert.match(html,item.one?/Nothing is recorded for this project until you do this/:/Nothing is recorded for this project until you choose one of these/);
  for (const [action,button] of [['restore-link',RESTORE],['adopt',ADOPT],['new-identity',FRESH]]){
   if (item.resolutions.includes(action)) assert.match(html,button,`${item.fault} offers ${action}`);
   else assert.doesNotMatch(html,button,`${item.fault} does not offer ${action}`);
  }
  assert.doesNotMatch(html,/Dispose of records after verified export|Export project records|Close project/);
 }
});
test('each identity control sends only its offered action and says what it does to the records',async()=>{
 const value=store(undefined);
 value.project.attachment={projectId:null,refusal:'link changed; not attached',limits:[],fault:'link changed',resolutions:['restore-link','adopt','new-identity'],recordedHere:'invented-P',linkedIdentity:'invented-Q'};
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(html,/written again to name the project recorded for this folder \(invented-P\)/);
 assert.match(html,/attached to the project its file names \(invented-Q\)/);
 assert.match(html,/records of invented-P stay in the store under that identity and are no longer attached to this folder/);
 assert.match(html,/takes none of the records kept in the store under an earlier identity/);assert.doesNotMatch(html,/starts with no records/);
 for (const [label,action] of [['Restore the project file','restore-link'],['This folder is the project its file names','adopt'],['Give this folder a new identity','new-identity']]){
  const calls=[];
  const group=buttons(loadSrc('RecordsStorePanel').IdentityResolution({attachment:value.project.attachment,act:async(...args)=>{calls.push(args);}}));
  const button=group.find(node=>node.props.children===label);
  assert.ok(button,label);await button.props.onClick();
  assert.deepEqual(calls,[['records_store_identity',{action}]]);
 }
});
test('an attached project with no fault is offered no identity act',()=>{
 const plain=store({closed:false,legalHold:false,disposition:'kept'});
 assert.doesNotMatch(renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:plain,act:async()=>{}})),/Restore the project file|This folder is the project|Give this folder a new identity/);
});
test('an adoption that stopped part-way is offered to complete, without saying recording is refused',()=>{
 const value=store(undefined);
 value.project.attachment={projectId:null,how:'none',limits:[],fault:'no folder recorded',resolutions:['adopt'],linkedIdentity:'invented-Q'};
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.match(html,/holds the project this folder’s file names and has no folder recorded for it/);
 assert.match(html,ADOPT);assert.doesNotMatch(html,RESTORE);assert.doesNotMatch(html,FRESH);
 assert.doesNotMatch(html,/Nothing is recorded for this project until/);
});
test('with a disposal standing only the project file can be restored, and an unfinished own import withholds every identity act',()=>{
 for (const disposition of ['disposal incomplete','disposed','completion durability uncertain']){
  const value=store({closed:true,legalHold:false,disposition});
  value.project.attachment={projectId:null,refusal:'link changed; not attached',limits:[],fault:'link changed',resolutions:['restore-link','adopt','new-identity'],recordedHere:'invented-P',linkedIdentity:'invented-Q'};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.match(html,RESTORE,disposition);assert.doesNotMatch(html,ADOPT,disposition);assert.doesNotMatch(html,FRESH,disposition);
  assert.match(html,/Nothing is recorded for this project until you do this/);
 }
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.project.attachment={projectId:null,refusal:'link changed; not attached',limits:[],fault:'link changed',resolutions:['restore-link','adopt','new-identity']};
 // Review round 2, finding 4: with the link changed, finishing the import is
 // refused by its preparation, so the host says it cannot be finished here.
 value.packageImport={state:'incomplete',importId:'invented-import',canFinish:false,finishReason:'The project file differs from the one this import recorded.'};
 const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
 assert.doesNotMatch(html,RESTORE);assert.doesNotMatch(html,ADOPT);assert.doesNotMatch(html,FRESH);assert.doesNotMatch(html,/Finish package import/);
 assert.match(html,/cannot be finished from here now: The project file differs from the one this import recorded/);
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
 const value=store(undefined);value.project.attachment={projectId:null,refusal:'records were kept in another store',limits:[],fault:'another store',resolutions:['adopt','new-identity'],linkedIdentity:'invented-Q'};
 value.project.notImported=2;
 const calls=[];
 const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
 const html=renderToStaticMarkup(panel);
 assert.match(html,/Import verified package/);assert.match(html,/identity already named by this folder/);
 assert.match(html,/Exact bytes and the original identity are retained/);assert.match(html,/conflicting files are refused/);
 assert.match(html,/Unsigned package content stays quoted evidence/);
 assert.match(html,/This folder is the project its file names/);
 const button=buttons(panel).find(node=>node.props.children==='Import verified package');
 assert.ok(button);await button.props.onClick();
 assert.deepEqual(calls,[['records_store_import_package',{action:'import'}]]);
});
test('interrupted package import offers only its recovery among project mutations',async()=>{
 const value=store({closed:false,legalHold:false,disposition:'kept'});
 value.project.notImported=2;value.project.attachment.refusal='publication incomplete';
 value.packageImport={state:'incomplete',importId:'invented-import',packageIdentity:'invented-hash',limit:'publication durability uncertain',canFinish:true};
 const calls=[];
 const panel=RecordsStorePanel({store:value,act:async(...args)=>{calls.push(args);}});
 const html=renderToStaticMarkup(panel);
 assert.match(html,/Project records remain unavailable until it is finished/);
 assert.match(html,/Finish package import/);assert.match(html,/publication durability uncertain/);
 assert.match(html,/invented-import/);assert.match(html,/invented-hash/);
 assert.doesNotMatch(html,/Import verified package|Export project records|Import 2 record|Close project|Set legal hold|This folder is the project its file names|Give this folder a new identity/);
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
 assert.doesNotMatch(html,/Close project|Set legal hold|Export project records|This folder is the project its file names|Give this folder a new identity/);
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
  assert.doesNotMatch(html,/Restore project from package|Import verified package|This folder is the project its file names/);
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
  value.packageImport={state:'incomplete',canRepair:false,needsPackage:false,reason:'identity association is unfinished',canFinish:true};
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

// Review round 2, finding 4: no control is offered whose current precondition
// cannot hold.
test('Finish package import is offered only when the host says its preparation can hold',()=>{
 for (const [canFinish,offered] of [[true,true],[false,false],[undefined,false],['true',false]]){
  const value=store({closed:false,legalHold:false,disposition:'kept'});
  value.packageImport={state:'incomplete',importId:'invented-import',canFinish,finishReason:canFinish===false?'This import belongs to the project folder /invented/elsewhere; finish it from there.':null};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  if (offered) assert.match(html,/>Finish package import</,String(canFinish));
  else assert.doesNotMatch(html,/Finish package import/,String(canFinish));
  if (canFinish===false) assert.match(html,/finish it from there/);
 }
});
test('Finish disposal is not offered while the folder is unattached; restoring the project file is',()=>{
 for (const disposition of ['disposal incomplete','completion durability uncertain']){
  const value=store({closed:true,legalHold:false,disposition});
  value.project.attachment={projectId:null,refusal:'link changed; not attached',limits:[],fault:'link changed',resolutions:['restore-link','adopt','new-identity'],recordedHere:'invented-P',linkedIdentity:'invented-Q'};
  const html=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:value,act:async()=>{}}));
  assert.doesNotMatch(html,/>Finish disposal</,disposition);
  assert.match(html,/can be finished once this folder is attached to its records again; restore the project file first/,disposition);
  assert.match(html,RESTORE,disposition);
 }
});
// Review round 2, findings 6 and 7.
test('an interrupted adoption and an unknown association say so and offer only what can succeed',()=>{
 const kept=store(undefined);
 kept.project.reading="records kept in the records store under the identity this folder's file names, not attached to this folder";
 kept.project.attachment={projectId:null,refusal:'records kept, not attached',limits:[],fault:'no folder recorded',resolutions:['adopt'],linkedIdentity:'invented-Q'};
 const one=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:kept,act:async()=>{}}));
 assert.match(one,/holds the project this folder’s file names/);assert.match(one,/reading records kept in the records store/);assert.match(one,ADOPT);assert.doesNotMatch(one,/no records yet/);
 const unknown=store(undefined);
 unknown.registry='the records store’s registry of project folders (roots.jsonl) was not read whole';
 unknown.project.attachment={projectId:null,refusal:'association not known; not attached',limits:[],fault:'association not known',resolutions:[],registry:unknown.registry};
 const two=renderToStaticMarkup(React.createElement(RecordsStorePanel,{store:unknown,act:async()=>{}}));
 assert.match(two,/was not read whole/);
 assert.doesNotMatch(two,RESTORE);assert.doesNotMatch(two,ADOPT);assert.doesNotMatch(two,FRESH);
});
