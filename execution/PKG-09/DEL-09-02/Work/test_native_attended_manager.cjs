// Offline tool orchestration fixture. No T3 tool, process, native API or network.
const fs=require('node:fs');const assert=require('node:assert/strict');
const source=fs.readFileSync(__dirname+'/native_attended_manager.js','utf8');
const manager=eval(source);
const managerHash=require('node:crypto').createHash('sha256').update(manager.toString()).digest('hex');
async function scenario(failure=false) {
 const root='/invented/root',entry='/invented/native_attended_entry.py',run_id='invented-run';
 const parent='0f35714c-46fb-45d8-9c97-c927c6587c1e';
 const manifest={controller_root:root,entry_source:entry,run_id,candidate:'invented',manager_function_sha256:managerHash};
 const body={run_id,candidate:'invented',event_id:'0001',completion_offer:{actual_owner_reply:'Cancelled'}};
 const event={event:'attended-manager-forward',run_id,event_id:'0001',event_path:root+'/bridge/0001.event.json',parent_thread:parent};
 const calls=[],notifications=[];
 const tools={
  exec_command:async({cmd})=>{
   calls.push(cmd);
   if(cmd.includes('import hashlib,sys;print'))return {exit_code:0,output:managerHash};
   if(cmd.includes(' record-start '))return {exit_code:0,output:''};
   if(cmd.includes(' check '))return {exit_code:0,output:JSON.stringify(manifest)};
   if(cmd.includes(' execute '))return {session_id:9,output:JSON.stringify({event:'owned_window_ready_for_agent_read'})+'\n'+JSON.stringify(event)+'\n'};
   if(cmd.includes('record-delivery'))return {exit_code:0,output:''};
   if(cmd.includes('native_attended_bridge import read'))return {exit_code:0,output:JSON.stringify(body)};
   throw new Error('unexpected command '+cmd);
  },
  write_stdin:async()=>({exit_code:1,output:JSON.stringify(event)+'\n'}),
  mcp__t3_code__t3_thread_send:async(args)=>{
   calls.push('T3-send');assert.equal(args.threadId,parent);assert(args.message.includes('invented-run'));
   if(failure)throw new Error('invented transport failed');
   return {structuredContent:{threadId:parent,messageId:'invented-message',delivery:'steered'}};
  }
 };
 const result=await manager({tools,root,entry,preparedSha256:'a'.repeat(64),startAuthorized:true,startRecord:{run_id,prepared_sha256:'a'.repeat(64),parent_start_message_id:'invented-start',resource_concurrence_message_id:'invented-resource'},notify:x=>notifications.push(x)});
 assert.equal(result.exit_code,1);assert.equal(calls.filter(x=>x==='T3-send').length,1);
 const receipt=notifications.find(x=>x.event_id==='0001');assert.equal(receipt.T3_transport_accepted,!failure);
 assert.equal(receipt.owner_read_or_completion_proved,false);assert.equal(receipt.receipt_written,true);
 assert(calls.findIndex(x=>x==='T3-send')<calls.findIndex(x=>x.includes(' record-delivery ')&&!x.includes('import hashlib,sys;print')));
}
async function errorsAndShapes() {
 const root='/invented/root',entry='/invented/native_attended_entry.py',run_id='run';
 for(const mode of ['poll-error','unknown-launch','both-session-and-null-exit','notify-error','bad-json']) {
  let polls=0,recovered=0;
  const event={event:'attended-manager-forward',run_id,event_id:'0001',event_path:root+'/bridge/0001.event.json',parent_thread:'0f35714c-46fb-45d8-9c97-c927c6587c1e'};
  const tools={exec_command:async({cmd})=>{
    if(cmd.includes('import hashlib,sys;print'))return {exit_code:0,output:managerHash};
    if(cmd.includes(' record-start '))return {exit_code:0,output:''};
    if(cmd.includes(' check '))return {exit_code:0,output:JSON.stringify({controller_root:root,entry_source:entry,run_id,candidate:'invented',manager_function_sha256:managerHash})};
    if(cmd.includes(' execute ')) {
      if(mode==='unknown-launch')return {process_id:123};
      if(mode==='both-session-and-null-exit')return {session_id:9,exit_code:null};
      return {session_id:9,output:mode==='bad-json'?JSON.stringify(event)+'\n':''};
    }
    if(cmd.includes('native_attended_bridge import read'))return {exit_code:0,output:'not JSON'};
    throw Error('unexpected');
   },
   write_stdin:async()=>{polls++;if(mode==='poll-error'&&polls===1)throw Error('invented poll error');return {exit_code:1,output:''};},
   mcp__t3_code__t3_thread_send:async()=>({structuredContent:{messageId:'invented'}})
  };
  const result=await manager({tools,root,entry,preparedSha256:'a'.repeat(64),startAuthorized:true,startRecord:{run_id,prepared_sha256:'a'.repeat(64),parent_start_message_id:'invented-start',resource_concurrence_message_id:'invented-resource'},
    notify:()=>{if(mode==='notify-error')throw Error('notify failed');},
    recoverSession:async proof=>{recovered++;return {...proof,session_id:9,tool_record_id:'invented actual tool record'};}});
  assert.equal(result.exit_code,1);assert(polls>=1);
  if(mode==='poll-error')assert.equal(polls,2);
  if(mode==='unknown-launch')assert.equal(recovered,1);
 }
}
(async()=>{await assert.rejects(manager({startAuthorized:false}),/No coordinated start/);await scenario();await scenario(true);await errorsAndShapes();console.log('manager bridge: 8 offline cases passed');})().catch(e=>{console.error(e);process.exitCode=1});
