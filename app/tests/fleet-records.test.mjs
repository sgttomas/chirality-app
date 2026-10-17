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
  assert.match(html,/No current graph established/);
  assert.equal(packet.workspace.undertakings.every(v=>v.graph===null),true,'historical unsupported selectors remain unselected');
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

test('actual private native receipt to persisted reader packet to panel preserves source-qualified links',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','conversation_roles::tests::native_links_actual_fork_dispatch_receipt_tick_store_copy_and_reader_dto','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('NATIVE_LINK_DTO:'));assert.ok(line);
  const actual=JSON.parse(line.slice(line.indexOf('NATIVE_LINK_DTO:')+'NATIVE_LINK_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:actual,error:'',busy:false,refresh:()=>{}}));
  const row=actual.coordination.nativeRelationships[0];
  assert.equal(actual.coordination.nativeRelationships.length,1);
  assert.match(html,/Recorded native conversation links/);assert.match(html,/forked from/);
  for(const id of [row.record.observationId,row.record.body.source.threadId,row.record.body.thread.threadId,row.record.body.rpc.requestRef,row.record.body.nativeHome.homeId])assert.ok(html.includes(id));
  assert.match(html,/does not activate a conversation/);assert.match(html,/0.1 undertaking fields establish no native join/);
  assert.doesNotMatch(html,/<button[^>]*>.*(?:Dispatch|Restore role|Integrate|Select undertaking)/);
});

test('actual mixed-profile packet keeps mechanical outcomes separate from its sole native relationship',()=>{
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::tests::fleet_reader_native_links_mixed_profile_keeps_legacy_quoted_and_mechanical_separate','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('NATIVE_LINK_MIXED_DTO:'));assert.ok(line);
  const actual=JSON.parse(line.slice(line.indexOf('NATIVE_LINK_MIXED_DTO:')+'NATIVE_LINK_MIXED_DTO:'.length));
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:actual,error:'',busy:false,refresh:()=>{}}));
  assert.equal(actual.coordination.nativeRelationships.length,1);assert.equal(actual.coordination.recordingEvents.length,1);
  assert.match(html,/Native link recording outcomes/);assert.match(html,/recording_limit/);assert.match(html,/Invented copy failure; native success unchanged/);
  assert.match(html,/quoted 0.1 compatibility record/);assert.match(html,/undertaking\/thread fields establish no native conversation relationship/);
});


test('actual native workspace reconstructs returns and waiting identically in separate processes',()=>{
  const read=()=>{
    const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','fleet_records::views::tests::fleet_views_native_adapter_preserves_return_review_integration_and_rebuild','--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'},
    });
    assert.equal(proc.status,0,proc.stderr+proc.stdout);
    const line=proc.stdout.split('\n').find(line=>line.includes('FLEET_WORKSPACE_DTO:'));assert.ok(line);
    return JSON.parse(line.slice(line.indexOf('FLEET_WORKSPACE_DTO:')+'FLEET_WORKSPACE_DTO:'.length));
  };
  const first=read(),second=read();assert.deepEqual(first,second,'process state is not coordination authority');
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:{...packet,workspace:first},error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Fleet coordination workspace/);assert.match(html,/Current graph/);assert.match(html,/fl:graph/);
  assert.match(html,/Return-review queue/);assert.match(html,/Selected work and waiting causes/);
  assert.match(html,/integration recorded/);assert.match(html,/Owner: executor/);assert.match(html,/current human-act standing/);
  assert.match(html,/Reconstruction limits/);assert.match(html,/no dispatch observed/);
});

test('qualified readiness and incomplete queues stay qualified in the rendered category and cause',()=>{
  const workspace={standing:'quoted fixture',graphIdentityMethod:'fixture',limits:[],undertakings:[{
    undertaking:'invented',graph:'fl:graph',revision:1,currentGraphEstablished:false,queueComplete:false,queue:[],notes:['incomplete source'],
    waiting:[{item:'W1',outcome:'invented result',owner:'recorded owner',category:'ready (qualified)',readinessQualified:true,causes:['dispatch may be unrecorded'],needs:[],sources:{}}],
  }]};
  const html=renderToStaticMarkup(React.createElement(FleetRecordsPanel,{packet:{...packet,workspace},error:'',busy:false,refresh:()=>{}}));
  assert.match(html,/Last readable graph; currentness unknown/);assert.match(html,/Return-review queue \(incomplete\)/);
  assert.match(html,/<strong>ready \(qualified\)<\/strong>/);assert.match(html,/dispatch may be unrecorded/);
  assert.doesNotMatch(html,/No recorded returns await/);
});
