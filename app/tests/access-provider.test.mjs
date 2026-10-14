// Actual private Host/refusal publication -> the maintained visible consumers.
// Invented peer/files only; no supplier/model/human-act qualification.
import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {tmpdir} from 'node:os';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
const app=new URL('../',import.meta.url),out=mkdtempSync(`${tmpdir()}/access-provider-private-`);
after(()=>rmSync(out,{recursive:true}));
const url=new URL('src/ConversationRoles.tsx',app),compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const canary='INVENTED_PRIVATE_PROVIDER_CANARY_481';
test('actual refusal stays safe in current source JSON and quoted role history',()=>{
 execFileSync('cargo',['test','--offline','--locked','--lib','access_provider_actual_private_refusal_output_has_only_safe_public_consumers','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CHIRALITY_TEST_OUTPUT_DIRECTORY:out},stdio:'inherit'});
 const packet=JSON.parse(readFileSync(`${out}/access-provider-private.json`,'utf8'));
 assert.match(packet.refusal,/credential element; no thread\/start sent/);
 assert.equal(packet.roleSupplyRecord.state,'written');assert.ok(packet.quotedRole.observations.length>0);
 const html=h(exports.RoleSupplyHistory,{view:packet.quotedRole})+h(exports.SupplyStatus,{supply:{state:'refused-before-send',reason:packet.refusal,roleSupplyRecord:packet.roleSupplyRecord}});
 assert.match(html,/credential element/);assert.doesNotMatch(html,new RegExp(canary));
 const raw=JSON.stringify({lifecycle:packet.snapshot.lifecycle,clientRequests:packet.snapshot.clientRequests,journal:packet.snapshot.journal,recordedRecovery:packet.recordedRecovery});
 assert.doesNotMatch(raw,new RegExp(canary));assert.match(raw,/private provider configuration outcome projection/);
 assert.equal(packet.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);

});
test('shared Start and Continue-as fields explain actual entry/provider refusal and preserve input',()=>{
 const html=h(exports.ModelProviderFields,{model:'chosen-model',modelProvider:'nonloopback-anonymous',setModel:()=>{},setModelProvider:()=>{}});
 assert.match(html,/cloud entries use built-in OpenAI/);assert.match(html,/configured Responses provider without credentials/);assert.match(html,/unavailable definition prevents Start/);
 assert.match(html,/value="nonloopback-anonymous"/);assert.match(html,/value="chosen-model"/);
});
