import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const url=new URL('../src/PlanMode.tsx',import.meta.url);
const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);
const {PlanModeControl}=exports;
const render=props=>renderToStaticMarkup(React.createElement(PlanModeControl,{planMode:null,requested:null,ready:true,busy:false,hasText:true,check(){},send(){},...props}));

test('no plan control unless Codex listed a plan preset (EX-3)',()=>{
  const unchecked=render({planMode:{state:'not-checked'}});
  assert.ok(unchecked.includes('Check plan mode availability'));assert.ok(!unchecked.includes('Send in plan mode'));
  const refused=render({planMode:{state:'not-offered',reason:'Codex listed no plan preset'}});
  assert.ok(refused.includes('not offered — Codex listed no plan preset'));assert.ok(!/<button/.test(refused));
});

test('offered plan mode is labelled experimental and carrying out is ordinary input',()=>{
  const html=render({planMode:{state:'offered'},requested:{mode:'plan',standing:'requested by this App on turn/start; Codex keeps it on later turns until another mode is sent'}});
  assert.ok(html.includes('Send in plan mode (experimental)'));assert.ok(html.includes('Send in default mode (carry out / leave plan mode)'));
  assert.ok(html.includes('not an approval'));assert.ok(html.includes('Plan mode stays on until you leave it'));
  assert.ok(html.includes('Last mode this App requested for this conversation: <b>plan</b>'));
  assert.equal((render({planMode:{state:'offered'},hasText:false}).match(/disabled=""/g)??[]).length,2,'no empty sends');
});
