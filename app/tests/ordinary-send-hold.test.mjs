// Ordinary sends without a native acknowledgement (native J2 baseline, main
// 9248a36e: an unknown outcome rendered like a refusal and Send stayed
// enabled, so one press could duplicate a turn). Mounted ConversationPanel with
// a controlled send; invented conversations. No supplier, model or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {ConversationPanel} = loadSrc('App');
const g = {appSession:'s', home:'account', spawnCounter:1};
const g2 = {...g, spawnCounter:2};
const thread = (threadId, generation = g) => ({generation, threadId, model:'invented-model', appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const hostFor = (generation = g) => ({state:'ready', generation, roleLimits:{account:{roles:[]}}, threads:[thread('thread-a', generation), thread('thread-b', generation)]});
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const noop = async () => {};

async function mounted(reply, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const sends = [];
  let current = {host:hostFor(), threadKey:JSON.stringify([g, 'thread-a'])};
  const render = async next => { current = {...current, ...next}; await React.act(() => root.render(React.createElement(ConversationPanel, {...current, setThreadKey:() => {}, answer:noop, runAct:noop,
    send:async (...args) => { sends.push(args); return reply(args, sends.length); }, steer:noop, submitAttachments:noop, interrupt:noop, checkPlanMode:noop, codexBusy:false}))); };
  const settle = () => React.act(async () => { for (let i = 0; i < 10; i++) await Promise.resolve(); });
  const field = () => nodes(c, 'textarea').find(node => node.getAttribute('id') === 'ordinary-composer-text');
  const ui = {c, sends, render, settle, field,
    type:async value => React.act(async () => { props(field()).onChange({target:{value}}); }),
    send:() => button(c, 'Send text'),
    readiness:() => c.querySelectorAll(node => node.getAttribute('id') === 'ordinary-send-readiness')[0].textContent,
    notices:() => c.querySelectorAll(node => node.getAttribute('aria-label') === 'Unconfirmed messages')[0]};
  try { await render({}); await check(ui); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
}

test('an unacknowledged ordinary send keeps its text, holds that conversation for every send control and is lifted only by an explicit acknowledgement', async () => {
  await mounted((args, n) => { if (n === 1) throw 'invented: no response from Codex'; return {id:1, result:{turn:{id:'t'}}}; }, async ui => {
    await ui.type('Please summarise the report');
    const retained = props(ui.send()).onClick;
    const proto = Object.getPrototypeOf(document.createElement('div')); const focused = []; const previousFocus = proto.focus;
    proto.focus = function () { focused.push(this); };
    try { await React.act(async () => { retained(); }); await ui.settle(); } finally { proto.focus = previousFocus; }
    assert.equal(ui.sends.length, 1);
    assert.equal(focused.at(-1)?.getAttribute('role'), 'alert', 'the new unconfirmed record takes the focus');
    assert.equal(props(ui.field()).value, 'Please summarise the report', 'the text is not cleared without a native acknowledgement');
    assert.match(ui.notices().textContent, /Your message to this conversation may have been sent\..*isn't resent and its text was not cleared.*held until you've read it.*Please summarise the report.*Reported: invented: no response from Codex/);
    assert.equal(props(ui.send()).disabled, true, 'Send is held');
    assert.match(ui.readiness(), /An earlier message to this conversation wasn't confirmed and may have been sent/);
    await React.act(async () => { retained(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'a retained Send control issues nothing');
    await ui.type('A different message');
    assert.equal(props(ui.send()).disabled, true, 'an edit does not lift the hold');
    // Another conversation is not held, and does not inherit the record's authority.
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    assert.equal(props(ui.send()).disabled, false);
    assert.match(ui.notices().textContent, /Your message to Conversation 1 · invented-model may have been sent/, 'the record stays listed by where it went');
    // A Codex restart keeps the hold for the same conversation ID, described plainly.
    await ui.render({host:hostFor(g2), threadKey:JSON.stringify([g2, 'thread-a'])});
    assert.equal(props(ui.send()).disabled, true, 'held for the same conversation ID after a restart');
    assert.match(ui.notices().textContent, /Your message to conversation thread-a in a Codex session that isn't loaded now may have been sent\..*The conversation shown now has the same ID, so sending to it is held too/);
    const before = ui.sends.length;
    await React.act(async () => { props(button(ui.notices(), 'I\'ve read that conversation — allow sending again')).onClick(); });
    assert.equal(ui.sends.length, before, 'acknowledging sends nothing');
    assert.match(ui.notices().textContent, /You've said you read that conversation.*Reported: invented: no response from Codex/, 'the original record stays');
    assert.equal(props(ui.send()).disabled, false);
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2, 'the person\'s separate new intent sends once');
    assert.equal(props(ui.field()).value, '', 'an acknowledged send clears its own text');
  });
});

test('a send that resolves without a result is not an acknowledgement: nothing is cleared and the conversation is held', async () => {
  await mounted(() => null, async ui => {
    await ui.type('Draft that may have gone');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(props(ui.field()).value, 'Draft that may have gone');
    assert.match(ui.notices().textContent, /may have been sent.*Reported: The host did not report this send's outcome; it may or may not have been sent\./);
    assert.equal(props(ui.send()).disabled, true);
    assert.doesNotMatch(ui.c.textContent, /Native turn\/start response received/, 'no acknowledgement is claimed');
  });
});

// Parent source review of #123 1f54e4ab: a Send captured before an unconfirmed
// attempt (or before a newer conversation, text or model) must never send, even
// after the acknowledgement; only a fresh press of the current view does.
test('a Send captured before the unconfirmed attempt or a newer choice issues nothing after the acknowledgement; a fresh press sends the current text once', async () => {
  await mounted((args, n) => { if (n === 1) throw 'invented: no reply'; return {id:n}; }, async ui => {
    await ui.type('text one for A');
    const capturedA = props(ui.send()).onClick;
    await React.act(async () => { capturedA(); }); await ui.settle();
    assert.equal(ui.sends.length, 1);
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    await ui.type('text two for B');
    await React.act(async () => { props(button(ui.notices(), 'I\'ve read that conversation — allow sending again')).onClick(); });
    await React.act(async () => { capturedA(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'the captured A control issues nothing after the acknowledgement and a new choice');
    await ui.render({threadKey:JSON.stringify([g, 'thread-a'])});
    await React.act(async () => { capturedA(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'not even with A shown again');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2, 'a fresh press sends once');
    assert.deepEqual([ui.sends[1][1], ui.sends[1][2]], ['thread-a', 'text two for B'], 'with the current conversation and current text');
  });
  await mounted((args, n) => { if (n === 1) throw 'invented: no reply'; return {id:n}; }, async ui => {
    await ui.type('before the restart');
    const captured = props(ui.send()).onClick;
    await React.act(async () => { captured(); }); await ui.settle();
    await ui.render({host:hostFor(g2), threadKey:JSON.stringify([g2, 'thread-a'])});
    await React.act(async () => { props(button(ui.notices(), 'I\'ve read that conversation — allow sending again')).onClick(); });
    await React.act(async () => { captured(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'a control from the earlier Codex session issues nothing');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2);
    assert.deepEqual(ui.sends[1][0], g2, 'the fresh press uses the current generation');
  });
});

test('a request the App puts into the draft, or that replaces it, records where it was written, so moving to another conversation says where it goes', async () => {
  await mounted(() => ({id:1}), async ui => {
    await ui.render({composerOffer:{sequence:1, threadKey:JSON.stringify([g, 'thread-a']), text:'Please turn this into a workflow draft'}});
    assert.equal(props(ui.field()).value, 'Please turn this into a workflow draft');
    const note = () => ui.c.querySelectorAll(node => node.getAttribute('aria-label') === 'Where your text goes')[0];
    assert.equal(note(), undefined, 'written for the conversation shown');
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    assert.match(note().textContent, /written while another conversation was shown\. It is kept; if you send it now it goes to Conversation 2 · invented-model\./);
    // An offer for B while B's draft is kept, then the explicit replacement.
    await ui.render({composerOffer:{sequence:2, threadKey:JSON.stringify([g, 'thread-b']), text:'The request for B'}});
    assert.equal(props(ui.field()).value, 'Please turn this into a workflow draft', 'unsent text is not overwritten');
    await React.act(async () => { props(button(ui.c, 'Replace my text with the request')).onClick(); });
    assert.equal(props(ui.field()).value, 'The request for B');
    assert.equal(note(), undefined, 'the replacement belongs to the conversation shown');
    await ui.render({threadKey:JSON.stringify([g, 'thread-a'])});
    assert.match(note().textContent, /it goes to Conversation 1 · invented-model/, 'after moving, the note names the real destination');
  });
});

test('with nothing else changed, a Send captured before an unconfirmed attempt still issues nothing after the acknowledgement', async () => {
  await mounted((args, n) => { if (n === 1) throw 'invented: no reply'; return {id:n}; }, async ui => {
    await ui.type('same text');
    const captured = props(ui.send()).onClick;
    await React.act(async () => { captured(); }); await ui.settle();
    await React.act(async () => { props(button(ui.notices(), 'I\'ve read that conversation — allow sending again')).onClick(); });
    await React.act(async () => { captured(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'the acknowledgement enables a fresh press, not the earlier control');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2);
  });
});

// A definite refusal started nothing (hosting.rs TurnStartFailure): the host
// rejects with a structured value naming its class. Defect reproduced on stock
// Codex 0.167.0: Codex answered turn/start with a JSON-RPC error and the App
// showed it as an unconfirmed send and held the conversation.
const nativeRefusal = {code:-32600, data:{currentModelProvider:'invented_current', modelProvider:'invented_chat', type:'modelProviderMismatch'}, message:'This chat uses invented_chat, but your current provider is invented_current. Switch to invented_chat to continue.'};
// `nativeErrorText` is the host's own serialization; here it carries an integer JavaScript cannot hold exactly, as the host's text would.
const NATIVE_TEXT = '{\n  "code": -32600,\n  "data": {\n    "limit": 9007199254740993\n  },\n  "message": "as serialized by the host"\n}';
const codexRefusal = {sendOutcome:'refused-by-codex', nativeError:nativeRefusal, nativeErrorText:NATIVE_TEXT, carriedEndNotice:false};
const refusedNotice = ui => ui.c.querySelectorAll(node => node.getAttribute('aria-label') === 'Message refused by Codex')[0];

test('Codex\'s definite refusal shows its own message and error data, keeps the text and model choice, adds no unconfirmed record and leaves Send usable', async () => {
  await mounted((args, n) => { if (n === 1) throw codexRefusal; return {id:n, result:{turn:{id:'t'}}}; }, async ui => {
    await ui.type('Please summarise the report');
    const model = () => nodes(ui.c, 'input').find(node => props(node)['aria-describedby'] === 'ordinary-model-help');
    await React.act(async () => { props(model()).onChange({target:{value:'invented-chosen-model'}}); });
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 1);
    assert.match(refusedNotice(ui).textContent, /Codex refused this message and started no turn\./);
    assert.ok(refusedNotice(ui).textContent.includes(`Codex's message: ${codexRefusal.nativeError.message}`), 'Codex\'s message as received');
    assert.ok(refusedNotice(ui).textContent.includes(NATIVE_TEXT), 'the error is shown from the host\'s serialized text');
    assert.ok(refusedNotice(ui).textContent.includes('9007199254740993'), 'an integer the window cannot hold exactly is not rounded');
    assert.ok(!refusedNotice(ui).textContent.includes(JSON.stringify(nativeRefusal, null, 2)), 'and never rebuilt from the decoded value');
    assert.match(refusedNotice(ui).textContent, /This attempt added no hold on sending and cleared neither your text nor your model choice\./);
    assert.doesNotMatch(refusedNotice(ui).textContent, /you can send again|Nothing is held|end notice/);
    assert.equal(ui.notices(), undefined, 'no unconfirmed record');
    assert.doesNotMatch(ui.c.textContent, /may have been sent/);
    assert.equal(props(ui.field()).value, 'Please summarise the report', 'the text is kept');
    assert.equal(props(model()).value, 'invented-chosen-model', 'the model choice is kept');
    assert.equal(props(ui.send()).disabled, false, 'Send is not held');
    assert.match(ui.readiness(), /Ready to send text/);
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2, 'sending again is not held');
    assert.equal(ui.sends[1][4], 'invented-chosen-model');
    assert.equal(refusedNotice(ui), undefined, 'the acknowledged send replaces the refusal');
  });
});

test('a refusal before anything was written shows the App\'s reason and holds nothing', async () => {
  await mounted((args, n) => { if (n === 1) throw {sendOutcome:'refused-before-write', reason:'invented: conversation is not loaded in this home generation'}; return {id:n}; }, async ui => {
    await ui.type('Kept text');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    const notice = ui.c.querySelectorAll(node => node.getAttribute('aria-label') === 'Message not sent')[0];
    assert.match(notice.textContent, /Not sent: the App refused this message before writing anything to Codex\. This attempt added no hold on sending and cleared neither your text nor your model choice\..*The App's reason: invented: conversation is not loaded in this home generation/);
    assert.doesNotMatch(notice.textContent, /you can send again|Nothing is held/);
    assert.equal(ui.notices(), undefined);
    assert.equal(props(ui.field()).value, 'Kept text');
    assert.equal(props(ui.send()).disabled, false);
  });
});

test('anything other than the host\'s well-formed definite refusal is still an unknown outcome and holds the conversation', async () => {
  const lookalikes = [
    'turn/start native error: {"code":-32600,"message":"refused"}',
    {sendOutcome:'refused-by-codex'},
    {sendOutcome:'refused-by-codex', nativeError:{code:1, message:'the earlier two-key form'}},
    {...codexRefusal, nativeError:{message:'no code'}},
    {...codexRefusal, nativeError:{code:'1', message:'string code'}},
    {...codexRefusal, nativeErrorText:''},
    {...codexRefusal, nativeErrorText:{code:1}},
    {...codexRefusal, carriedEndNotice:'yes'},
    {...codexRefusal, extra:true},
    {sendOutcome:'refused-before-write', reason:''},
    {sendOutcome:'not-a-class', reason:'x'},
    new Error('invented: write failed'),
  ];
  for (const rejection of lookalikes) {
    await mounted(() => { throw rejection; }, async ui => {
      await ui.type('Draft that may have gone');
      await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
      assert.match(ui.notices().textContent, /Your message to this conversation may have been sent\./, JSON.stringify(String(rejection)));
      assert.equal(refusedNotice(ui), undefined);
      assert.equal(props(ui.send()).disabled, true, 'held');
      assert.equal(props(ui.field()).value, 'Draft that may have gone');
    });
  }
});

test('a refusal that carried a run\'s end notice says so, and that the App does not send the notice again', async () => {
  await mounted((args, n) => { if (n === 1) throw {...codexRefusal, carriedEndNotice:true}; return {id:n, result:{turn:{id:'t'}}}; }, async ui => {
    await ui.type('Text sent with the notice');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.match(refusedNotice(ui).textContent, /Codex refused this message and started no turn\..*This message also carried a workflow run's end notice, which Codex refused with it\. The App does not send that notice again\./);
    assert.equal(ui.notices(), undefined, 'a refusal Codex made is not an unknown outcome');
    assert.equal(props(ui.send()).disabled, false);
  });
});

// The notice stays on screen across navigation and a Codex stop, so it says
// only what the refused attempt did; the composer says whether sending is possible now.
test('the refusal notice claims nothing about sending now: another conversation\'s hold and a stopped Codex are the composer\'s to say', async () => {
  await mounted((args, n) => { if (n === 1) throw 'invented: no response from Codex'; if (n === 2) throw codexRefusal; return {id:n}; }, async ui => {
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    await ui.type('Unknown in B');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(props(ui.send()).disabled, true, 'B is held after its unknown outcome');
    await ui.render({threadKey:JSON.stringify([g, 'thread-a'])});
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.match(refusedNotice(ui).textContent, /Codex refused this message and started no turn\./);
    assert.equal(props(ui.send()).disabled, false, 'A is not held by its definite refusal');
    // Back in B: the notice may remain, B stays held, and nothing on the page says B can be sent to.
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    assert.equal(props(ui.send()).disabled, true, 'B is still held');
    assert.doesNotMatch(ui.c.textContent, /you can send again|Nothing is held/);
    assert.match(ui.readiness(), /wasn't confirmed and may have been sent/);
    // Codex stops: the notice still says only what the attempt did.
    await ui.render({host:{...hostFor(), state:'exited-unexpectedly', generationClosed:true}, threadKey:JSON.stringify([g, 'thread-a'])});
    assert.equal(props(ui.send()).disabled, true, 'nothing can be sent to a stopped Codex');
    assert.doesNotMatch(ui.c.textContent, /you can send again|Nothing is held/);
  });
});
