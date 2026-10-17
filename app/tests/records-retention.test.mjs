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
