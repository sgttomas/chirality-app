// Offline tool orchestration fixture. No T3 tool, process, native API or network.
const fs=require('node:fs');const assert=require('node:assert/strict');
const source=fs.readFileSync(__dirname+'/native_attended_manager.js','utf8');
const manager=eval(source);
async function scenario(failure=false) {
 const root='/invented/root',entry='/invented/native_attended_entry.py',run_id='invented-run';
 const parent='0f35714c-46fb-45d8-9c97-c927c6587c1e';
 const manifest={controller_root:root,entry_source:entry,run_id,candidate:'invented'};
 const body={run_id,candidate:'invented',event_id:'0001',completion_offer:{actual_owner_reply:'Cancelled'}};
 const event={event:'attended-manager-forward',run_id,event_id:'0001',event_path:root+'/bridge/0001.event.json',parent_thread:parent};
 const calls=[],notifications=[];
 const tools={
  exec_command:async({cmd})=>{
   calls.push(cmd);
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
 const result=await manager({tools,root,entry,preparedSha256:'a'.repeat(64),startAuthorized:true,notify:x=>notifications.push(x)});
 assert.equal(result.exit_code,1);assert.equal(calls.filter(x=>x==='T3-send').length,1);
 const receipt=notifications.find(x=>x.event_id==='0001');assert.equal(receipt.T3_transport_accepted,!failure);
 assert.equal(receipt.owner_read_or_completion_proved,false);assert.equal(receipt.receipt_written,true);
 assert(calls.findIndex(x=>x==='T3-send')<calls.findIndex(x=>x.includes('record-delivery')));
}
(async()=>{await assert.rejects(manager({startAuthorized:false}),/No coordinated start/);await scenario();await scenario(true);console.log('manager bridge: 3 offline cases passed');})().catch(e=>{console.error(e);process.exitCode=1});
