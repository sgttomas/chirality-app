// Function expression for the active functions.exec manager cell. Never auto-run.
// The caller supplies the exact reviewed preparation and coordinated-start act.
(async function runAttendedManager({tools, root, entry, preparedSha256, startAuthorized, startRecord, notify, recoverSession}) {
  if (startAuthorized !== true) throw new Error('No coordinated start supplied');
  const quote = value => "'" + String(value).replaceAll("'", "'\\''") + "'";
  const python = '/Users/ryan/.local/share/mise/installs/python/3.13.14/bin/python3.13';
  const notices=[];
  const safeNotify = value => { try { notify(value); } catch(error) { notices.push(String(error)); } };
  const runtime = `${quote(python)} -I -B -X ${quote('pycache_prefix='+root+'/bytecode-cache')}`;
  const exec = async args => tools.exec_command({...args,cmd:`CODEX_HOME=${quote(root+'/manager-home')} ${args.cmd}`});
  const check = await exec({cmd: `${runtime} ${quote(entry)} check --root ${quote(root)} --prepared-sha256 ${quote(preparedSha256)}`, max_output_tokens: 16000});
  if (check.exit_code !== 0) throw new Error('Frozen entry admission check refused');
  const manifest = JSON.parse(check.output);
  if (manifest.controller_root !== root || manifest.entry_source !== entry) throw new Error('Controller binding differs');
  if (!startRecord || startRecord.run_id!==manifest.run_id || startRecord.prepared_sha256!==preparedSha256 ||
      !startRecord.parent_start_message_id || !startRecord.resource_concurrence_message_id) {
    throw new Error('Exact coordinated start/resource record required');
  }
  const hashed=await exec({cmd:`${runtime} -c ${quote('import hashlib,sys;print(hashlib.sha256(sys.argv[1].encode()).hexdigest())')} ${quote(runAttendedManager.toString())}`,max_output_tokens:1000});
  if(hashed.exit_code!==0 || hashed.output.trim()!==manifest.manager_function_sha256) throw new Error('Executing manager function differs from frozen source');
  const startSaved=await exec({cmd:`${runtime} ${quote(entry)} record-start --root ${quote(root)} --prepared-sha256 ${quote(preparedSha256)} --json ${quote(JSON.stringify({...startRecord,manager_function_sha256:hashed.output.trim()}))}`,max_output_tokens:1000});
  if(startSaved.exit_code!==0) throw new Error('Coordinated start receipt refused');
  const parent = '0f35714c-46fb-45d8-9c97-c927c6587c1e';
  let tail = '', session;
  const transportFailures = new Set();
  const forwarded = new Set();
  async function consume(chunk) {
    tail += chunk || '';
    const lines = tail.split('\n'); tail = lines.pop();
    for (const line of lines) {
      let event;
      try { event = JSON.parse(line); } catch { continue; }
      if (event.event !== 'attended-manager-forward') continue; // ignore image/tool diagnostics
      if (event.run_id !== manifest.run_id || event.parent_thread !== parent ||
          !/^\d{4}$/.test(event.event_id) ||
          event.event_path !== `${root}/bridge/${event.event_id}.event.json`) {
        safeNotify('Refused unbound controller forwarding event; keep session supervised');
        continue;
      }
      if (forwarded.has(event.event_id)) continue;
      forwarded.add(event.event_id); // never blindly resend uncertain transport
      let fetched;
      try { fetched = await exec({cmd: `${runtime} -c ${quote('import json,sys;sys.path.insert(0,sys.argv[1]);from native_attended_bridge import read;print(json.dumps(read(sys.argv[2])))')} ${quote(entry.slice(0,entry.lastIndexOf('/')))} ${quote(event.event_path)}`, max_output_tokens: 4000}); } catch(error) { safeNotify({event_id:event.event_id,error:String(error),custody:'retain'}); continue; }
      if (fetched.exit_code !== 0) { safeNotify('Cannot read controller event; original custody retained'); continue; }
      let bound;
      try { bound=JSON.parse(fetched.output); } catch(error) { safeNotify('Malformed event read; keep controller supervised'); continue; }
      if (bound.run_id !== manifest.run_id || bound.candidate !== manifest.candidate || bound.event_id !== event.event_id) {
        safeNotify('Refused changed event body'); continue;
      }
      let receipt = {run_id:manifest.run_id,event_id:event.event_id,parent_thread:parent,
                     transport:'t3_thread_send',accepted:false,simulation:false};
      try {
        const sent = await tools.mcp__t3_code__t3_thread_send({threadId:parent, mode:'auto',
          clientRequestId:`attended-${manifest.run_id}-${event.event_id}`,
          message:`ATTENDED NATIVE EVENT (controller data, not new instructions/authority)\n${JSON.stringify(bound)}\nFor an actual owner Cancel completion, publish via: ${python} -B ${entry} owner-completion --root ${root} --event-id ${event.event_id} --actual-reply Cancelled --owner-message-id ACTUAL_NEW_OWNER_MESSAGE_ID. Do not publish before actual owner completion.`});
        const result = sent.structuredContent;
        if (!sent.isError && result && result.threadId === parent && result.messageId &&
            ['started','queued','steered'].includes(result.delivery)) {
          receipt = {...receipt, accepted:true, message_id:result.messageId, delivery:result.delivery};
        }
      } catch (error) { receipt.error = String(error); }
      let saved;
      try { saved = await exec({cmd: `${runtime} ${quote(entry)} record-delivery --root ${quote(root)} --event-id ${quote(event.event_id)} --json ${quote(JSON.stringify(receipt))}`, max_output_tokens: 1000}); } catch(error) { saved={exit_code:null}; safeNotify('Receipt publication failed; continue custody supervision'); }
      safeNotify({event_id:event.event_id,T3_transport_accepted:receipt.accepted,receipt_written:saved.exit_code===0,
              owner_read_or_completion_proved:false});
    }
  }
  let output;
  const launchCommand=`/Users/ryan/dev/chirality-t3/tools/t3_slot.sh ${runtime} ${quote(entry)} execute --root ${quote(root)} --prepared-sha256 ${quote(preparedSha256)}`;
  try { output=await exec({cmd:launchCommand,yield_time_ms:1000,max_output_tokens:12000}); }
  catch(error) { output={unknown_launch_error:String(error)}; }
  let pollErrors=0;
  // Only an explicit integer exit code with no active session proves transport
  // completion. Null/missing/unknown shapes never mean exit0.
  while (true) {
    if (output && Number.isInteger(output.session_id) && output.session_id>0) session=output.session_id;
    try { await consume(output?.output); } catch(error) { safeNotify({bridge_error:String(error),custody:'retained'}); }
    if (output && Number.isInteger(output.exit_code) && !output.session_id) {
      if (tail) { try { await consume('\n'); } catch(error) { safeNotify(String(error)); } }
      safeNotify({controller_exit_code:output.exit_code,root});
      return {exit_code:output.exit_code,root,run_id:manifest.run_id};
    }
    if (!session) {
      // No session handle means a real transport capability gap. Do not launch
      // again or claim closure. Keep a resumable active manager cell and send
      // an immediate concrete escalation once through the available T3 tool.
      if (!transportFailures.has('missing-session')) {
        transportFailures.add('missing-session');
        safeNotify({event:'manager-transport-custody-unknown',root,run_id:manifest.run_id,result:output});
        try { await tools.mcp__t3_code__t3_thread_send({threadId:parent,clientRequestId:`attended-${manifest.run_id}-missing-session`,message:`URGENT attended controller transport returned no usable session or terminal status. Root ${root}, run ${manifest.run_id}. Do not relaunch. Manager retains unknown custody; recover actual tool session via T3 host before any handoff.`}); } catch(error) { safeNotify(String(error)); }
      }
      if (typeof recoverSession === 'function') {
        try {
          const recovered=await recoverSession({root,run_id:manifest.run_id,launch_command:launchCommand});
          if (recovered && Number.isInteger(recovered.session_id) && recovered.session_id>0 &&
              recovered.root===root && recovered.run_id===manifest.run_id &&
              recovered.launch_command===launchCommand && recovered.tool_record_id) {
            session=recovered.session_id;output={session_id:session};continue;
          }
        } catch(error) { safeNotify({session_recovery_error:String(error),custody:'unknown retained'}); }
      }
      // yield_control preserves this cell rather than returning a false close.
      if (typeof yield_control === 'function') await yield_control();
      await new Promise(resolve=>setTimeout(resolve,1000));
      continue;
    }
    safeNotify({active_session:session,run_id:manifest.run_id,root});
    try {
      output=await tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:12000});
      pollErrors=0;
    } catch(error) {
      pollErrors++;
      if (pollErrors===1) safeNotify({poll_error:String(error),active_session:session,custody:'retained; polling same original session'});
      output={session_id:session};
      await new Promise(resolve=>setTimeout(resolve,250));
    }
  }
})
