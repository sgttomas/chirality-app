// Function expression for the active functions.exec manager cell. Never auto-run.
// The caller supplies the exact reviewed preparation and coordinated-start act.
(async function runAttendedManager({tools, root, entry, preparedSha256, startAuthorized, notify}) {
  if (startAuthorized !== true) throw new Error('No coordinated start supplied');
  const quote = value => "'" + String(value).replaceAll("'", "'\\''") + "'";
  const python = '/Users/ryan/.local/share/mise/installs/python/3.13.14/bin/python3.13';
  const exec = async args => tools.exec_command(args);
  const check = await exec({cmd: `${quote(python)} -B ${quote(entry)} check --root ${quote(root)} --prepared-sha256 ${quote(preparedSha256)}`, max_output_tokens: 16000});
  if (check.exit_code !== 0) throw new Error('Frozen entry admission check refused');
  const manifest = JSON.parse(check.output);
  if (manifest.controller_root !== root || manifest.entry_source !== entry) throw new Error('Controller binding differs');
  const parent = '0f35714c-46fb-45d8-9c97-c927c6587c1e';
  let tail = '', session;
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
        notify('Refused unbound controller forwarding event; keep session supervised');
        continue;
      }
      if (forwarded.has(event.event_id)) continue;
      forwarded.add(event.event_id); // never blindly resend uncertain transport
      const fetched = await exec({cmd: `${quote(python)} -B -c ${quote('import json,sys;sys.path.insert(0,sys.argv[1]);from native_attended_bridge import read;print(json.dumps(read(sys.argv[2])))')} ${quote(entry.slice(0,entry.lastIndexOf('/')))} ${quote(event.event_path)}`, max_output_tokens: 4000});
      if (fetched.exit_code !== 0) { notify('Cannot read controller event; original custody retained'); continue; }
      const bound = JSON.parse(fetched.output);
      if (bound.run_id !== manifest.run_id || bound.candidate !== manifest.candidate || bound.event_id !== event.event_id) {
        notify('Refused changed event body'); continue;
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
      const saved = await exec({cmd: `${quote(python)} -B ${quote(entry)} record-delivery --root ${quote(root)} --event-id ${quote(event.event_id)} --json ${quote(JSON.stringify(receipt))}`, max_output_tokens: 1000});
      notify({event_id:event.event_id,T3_transport_accepted:receipt.accepted,receipt_written:saved.exit_code===0,
              owner_read_or_completion_proved:false});
    }
  }
  let output = await exec({cmd: `/Users/ryan/dev/chirality-t3/tools/t3_slot.sh ${quote(python)} -B ${quote(entry)} execute --root ${quote(root)} --prepared-sha256 ${quote(preparedSha256)}`, yield_time_ms:1000,max_output_tokens:4000});
  session=output.session_id;
  if (session) notify({active_session:session,run_id:manifest.run_id,root});
  await consume(output.output);
  while (output.session_id) {
    // This is active live custody supervision, not polling a PR or delegate.
    output=await tools.write_stdin({session_id:session,chars:'',yield_time_ms:1000,max_output_tokens:4000});
    await consume(output.output);
  }
  if (tail) await consume('\n');
  notify({controller_exit_code:output.exit_code,root});
  return {exit_code:output.exit_code,root,run_id:manifest.run_id};
})
