import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {loadSrc} from './support/load-src.mjs';
const {FleetRecordsPanel,readFleetPacket}=loadSrc('FleetRecordsPanel');
let packet;
test('native selected-workspace adapter response is presented in full with provenance and limits',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::tests::fleet_reader_native_adapter_full_response','--','--exact','--nocapture','--test-threads=1'],{
    cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'},
  });
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('FLEET_DTO:'));
  assert.ok(line,'the actual native adapter emitted its invented response fixture');
  packet=JSON.parse(line.slice(line.indexOf('FLEET_DTO:')+'FLEET_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet,error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Refresh fleet records/);assert.match(html,/Complete fleet packet, sources and provenance/);
  assert.match(html,/graph-content identity method is unselected\/unsupported/);
  assert.match(html,/protected-store order/);assert.match(html,/claimed|Claimed/);
  for(const row of [...packet.briefs,...packet.graphs,...packet.coordination.projectRecords,...packet.coordination.appObservations]){
    assert.ok(html.includes(row.record.recordId),'no returned record is hidden by a state projection');
  }
  assert.match(html,/No work state or current graph is selected here/);
  assert.doesNotMatch(html,/<button[^>]*>.*(?:Dispatch|Select graph|Write record|Register)/);
});
test('only an explicit refresh invokes the path-free native read command',async()=>{
  const calls=[];
  const invoke=async(...args)=>{calls.push(args);return packet;};
  const refresh=()=>readFleetPacket(invoke);
  const element=FleetRecordsPanel({packet:null,error:'',busy:false,refresh});
  assert.equal(calls.length,0);
  const findButton=node=>{
    if(!node || typeof node!=='object')return null;
    if(node.type==='button')return node;
    const children=node.props?.children;
    return (Array.isArray(children)?children:[children]).flat(Infinity).map(findButton).find(Boolean);
  };
  await findButton(element).props.onClick();
  assert.deepEqual(calls,[['read_fleet_records']]);
});
test('busy and failed source reads remain explicit without a fabricated empty packet',()=>{
  const busy=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:null,error:'',busy:true,refresh:()=>{}}));
  assert.match(busy,/disabled/);assert.match(busy,/Reading fleet records/);
  const failed=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:null,error:'selected project unavailable',busy:false,refresh:()=>{}}));
  assert.match(failed,/role="alert"/);assert.match(failed,/Fleet read failed: selected project unavailable/);
  assert.doesNotMatch(failed,/0 brief record/);
});
