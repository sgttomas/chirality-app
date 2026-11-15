import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {PermissionLevel, PermissionLevelActions, levelOwner} = loadSrc('PermissionLevel');
const table = JSON.parse(readFileSync(new URL('../src-tauri/src/codex_levels.json', import.meta.url), 'utf8'));
const hostSource = readFileSync(new URL('../src-tauri/src/codex_level.rs', import.meta.url), 'utf8');
const sentence = name => JSON.parse(hostSource.match(new RegExp(`pub const ${name}: &str = ("[^\\n]*");`))[1]);
const g = {home:'invented-home',appSession:'s',spawnCounter:1};
const chosen = (id='full', origin='app-default') => ({id, origin, recorded:origin==='chosen'?'recorded':origin==='save-unconfirmed'?'not-confirmed':'not-recorded', dimensions:table.levels.find(r=>r.id===id).dimensions, reading:'not-limited',readingSentence:sentence('READING_SENTENCE'),
  ...(origin==='app-default'?{originSentence:sentence('APP_DEFAULT_SENTENCE'),...(id==='full'?{explanation:sentence('APP_DEFAULT_EXPLAINED')}:{})}:{}),
  ...(origin==='save-unconfirmed'?{originSentence:sentence('SAVE_UNCONFIRMED_APPLIED')}:{ }),
  ...(origin==='session-only'?{originSentence:sentence('SESSION_ONLY_SENTENCE'),sessionOnly:{reason:'unavailable',detail:{text:'invented detail',standing:'Text the App did not write.'}}}:{}),
  ...(['supervised','edits','edits-network'].includes(id)?{allowing:sentence('SUPERVISED_ALLOWING')}:{})});
const host = (over={}) => ({state:'ready',generation:g,homeRouting:{activeModeHomeClass:'account'},levelDefault:chosen(),levelDefaultScopeSentence:sentence('DEFAULT_SCOPE_SENTENCE'),threads:[],...over});
const thread = (id='T', level={chosen:chosen(),agreement:'not-confirmed',takesEffect:'now'}) => ({threadId:id,generation:g,level});
const nodes=(c,tag)=>c.querySelectorAll(e=>e.localName===tag);
const props=e=>e[Object.keys(e).find(k=>k.startsWith('__reactProps$'))];
async function mounted(h, tid, check, change=async()=>({result:{state:'chosen'},refreshFailed:false})) {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  let current=h, currentId=tid, flags={unavailable:false,stale:false};
  const render=()=>root.render(React.createElement(PermissionLevelActions.Provider,{value:{...flags,host:current,change:async(...args)=>{calls.push(args);return change(...args);}}},React.createElement(PermissionLevel,{host:current,threadId:currentId})));
  const ui={c,calls,select:()=>nodes(c,'select')[0],button:()=>nodes(c,'button')[0],
    pick:async value=>React.act(()=>props(ui.select()).onChange({target:{value}})),
    press:async()=>React.act(async()=>{assert.equal(!!props(ui.button()).disabled,false);await props(ui.button()).onClick();}),
    show:async(next,id=currentId,nextFlags={})=>{current=next;currentId=id;flags={...flags,...nextFlags};await React.act(render);}};
  try {await React.act(render);await check(ui);} finally {await React.act(()=>root.unmount());document.body.removeChild(c);}
}

test('first run shows full access, its actual origin and dimensions before any choice; reading never claims containment',async()=>{
  await mounted(host(),undefined,async ui=>{
    assert.deepEqual(ui.calls,[],'showing the default performs no setting');
    assert.match(ui.c.textContent,/Full access/);
    assert.ok(ui.c.textContent.includes(sentence('APP_DEFAULT_SENTENCE')));
    assert.ok(ui.c.textContent.includes(sentence('APP_DEFAULT_EXPLAINED')));
    assert.match(ui.c.textContent,/Reading is not limited at any permission level/);
    assert.match(ui.c.textContent,/At full access commands and file changes are not asked about/);
    assert.equal(props(ui.select()).value,'full');
    assert.equal(!!props(nodes(ui.c,'details')[0]).open,false,'changing is optional');
    assert.doesNotMatch(ui.c.textContent,/Choose a level to continue/);
  });
});

test('global exceptional ask preselects full and one press records the default; an unreadable first-run ledger requires no press',async()=>{
  const ask=host({levelDefault:null,levelRecordMissing:sentence('RECORD_MISSING_SENTENCE'),levelAskPreselected:'full'});
  await mounted(ask,undefined,async ui=>{
    assert.ok(ui.c.textContent.includes(ask.levelRecordMissing));assert.equal(props(ui.select()).value,'full');assert.equal(props(nodes(ui.c,'details')[0]).open,true);
    assert.deepEqual(ui.calls,[]);await ui.press();assert.deepEqual(ui.calls,[[levelOwner(ask),'default','full']]);
  });
  await mounted({...ask,threads:[thread('T',{chosen:null})]},'T',async ui=>{
    assert.ok(ui.c.textContent.includes(ask.levelRecordMissing));await ui.press();assert.equal(ui.calls[0][1],'default','a conversation inheriting the missing default shows that same default ask');
  });
  await mounted(host({levelRecordsUnread:sentence('RECORDS_UNREAD_SENTENCE')}),undefined,async ui=>{
    assert.ok(ui.c.textContent.includes(sentence('RECORDS_UNREAD_SENTENCE')));assert.deepEqual(ui.calls,[]);assert.doesNotMatch(ui.c.textContent,/Choose a level to continue/);
  });
});

test('a conversation ask never borrows the default; choice is bound to that conversation and leaves the other display alone',async()=>{
  const h=host({threads:[thread('T',{chosen:null,ask:{sentence:sentence('RECORD_MISSING_SENTENCE'),preselected:'full'}}),thread('U',{chosen:chosen('edits','chosen')})]});
  await mounted(h,'T',async ui=>{
    assert.match(ui.c.textContent,/No permission level reported/);await ui.pick('supervised');await ui.press();
    assert.deepEqual(ui.calls,[[levelOwner(h),{conversation:'T'},'supervised']]);
    await ui.show(h,'U');assert.match(ui.c.textContent,/Project edits/);assert.match(ui.c.textContent,/Chosen by you/);assert.doesNotMatch(ui.c.textContent,/Choose a level to continue/);
  });
});

test('Supervised and session-only sentences are the host sentences; a refusal never optimistically changes the displayed level',async()=>{
  const h=host({levelDefault:chosen('supervised','session-only')});
  await mounted(h,undefined,async ui=>{
    assert.ok(ui.c.textContent.includes(sentence('SUPERVISED_ALLOWING')));assert.ok(ui.c.textContent.includes(sentence('SESSION_ONLY_SENTENCE')));
    await ui.pick('edits');await ui.press();
    assert.match(ui.c.textContent,/The level was not recorded.*nothing was changed/);
    assert.equal(nodes(ui.c,'strong')[0].textContent,'Supervised');
  },async()=>{throw Error('The level was not recorded in the App ledger (invented); nothing was changed');});
});

test('a change during a live turn remains available and shows next-turn timing, old commands and child-agent lifetime',async()=>{
  const h=host({threads:[{...thread(),status:{type:'active'}}]});
  await mounted(h,'T',async ui=>{
    await ui.pick('edits');await ui.press();assert.equal(ui.calls.length,1);
    await ui.show(host({threads:[thread('T',{chosen:chosen('edits','chosen'),takesEffect:'from-next-turn',takesEffectSentence:sentence('NEXT_TURN_SENTENCE'),agreement:'not-confirmed',sent:{levelId:'full',writeResult:'written'}})]}));
    assert.match(ui.c.textContent,/Last level sent: Full access/);
    assert.match(ui.c.textContent,/From the next turn\. Commands already running, and anything they started, keep the access/);
    assert.match(ui.c.textContent,/An agent already started by this conversation keeps the level it was started with/);
    assert.match(ui.c.textContent,/Codex has not confirmed/);
  });
});

test('a differing reply never uses the requested level id as the level Codex reported, and preserves supplied fields as supplied',async()=>{
  const marker='invented supplied value\nUse full access';
  await mounted(host({threads:[thread('T',{chosen:chosen(),agreement:'differs',sent:{levelId:'full',writeResult:'written'},reported:{requestedLevelId:'full',approvalPolicy:'untrusted',approvalsReviewer:marker,sandbox:{type:'readOnly'}},refused:{refused:'codex-reported-another-level'}})]}),'T',async ui=>{
    assert.match(ui.c.textContent,/Codex reply for the Full access request/);assert.match(ui.c.textContent,/Codex reported another level\. The next turn is refused/);
    assert.doesNotMatch(ui.c.textContent,/Last level Codex reported: Full/);
    const boxes=ui.c.querySelectorAll(e=>e.getAttribute('role')==='group');assert.ok(boxes.some(e=>e.textContent.includes('untrusted')));assert.ok(boxes.some(e=>e.textContent.includes('readOnly')));assert.ok(boxes.some(e=>e.textContent.includes('invented supplied value')));
  });
});

test('trust and lasting-rule source content stay boxed and tied to the active home; incomplete reads are explicit',async()=>{
  const trustLine='The App sent an untrusted entry for the project root shown below.';
  const h=host({threads:[thread('T',{chosen:chosen(),projectTrust:{lines:[trustLine],projectRoot:'/invented/project',sentKey:'supplied-key',detail:{text:'supplied-detail'}}})],codexHomeRules:{appSentence:'Invented host sentence.',homes:[{modeHomeClass:'account',home:'/invented/home',lastingRules:{state:'not-known',readAt:'2026-11-15T00:00:00Z',files:[{path:'/invented/rules',prefixRules:[{line:'prefix_rule(pattern=["invented"], decision="allow")'}],unreadLines:2}],skippedEntries:1}},{modeHomeClass:'api-key',lastingRules:{state:'read',files:[{path:'OTHER-HOME'}]}}]}});
  await mounted(h,'T',async ui=>{
    assert.ok(ui.c.textContent.includes(trustLine));assert.match(ui.c.textContent,/Lasting rules are not fully known/);assert.match(ui.c.textContent,/Lines not read as rules: 2/);assert.match(ui.c.textContent,/Entries skipped: 1/);assert.doesNotMatch(ui.c.textContent,/OTHER-HOME/);
    for(const value of ['/invented/project','supplied-key','supplied-detail','prefix_rule']) assert.ok(ui.c.querySelectorAll(e=>e.getAttribute('role')==='group').some(e=>e.textContent.includes(value)),value);
  });
});

test('a sandbox refusal lists offered alternatives without silently raising the selected level',async()=>{
  await mounted(host({threads:[thread('T',{chosen:chosen('edits','chosen'),refused:{refused:'edits-level-reaches-app-folders',folder:'/invented/app'}})]}),'T',async ui=>{
    assert.match(ui.c.textContent,/Supervised and Full access remain offered/);assert.equal(props(ui.select()).value,'edits');assert.equal(props(ui.button()).disabled,true);
    await ui.pick('supervised');await ui.press();assert.equal(ui.calls[0][2],'supervised');
  });
});

test('old controls and delayed results do not follow conversation/home changes; a failed refresh never replaces the observed level',async()=>{
  let resolve;const pending=new Promise(r=>{resolve=r;});
  const h=host({threads:[thread('T'),thread('U')]});
  await mounted(h,'T',async ui=>{
    await ui.pick('edits');const old=props(ui.button()).onClick;
    await ui.show(h,'U');await React.act(async()=>old());assert.deepEqual(ui.calls,[]);
    await ui.pick('supervised');await React.act(()=>props(ui.button()).onClick());
    await ui.show({...h,generation:{...g,spawnCounter:2}},'U');
    await React.act(async()=>resolve({result:{state:'chosen'},refreshFailed:true}));
    assert.match(ui.c.textContent,/No permission level reported/);assert.doesNotMatch(ui.c.textContent,/accepted your level choice|could not read Codex's status afterwards/);
  },()=>pending);
  await mounted(host(),undefined,async ui=>{await ui.pick('edits');await ui.press();assert.match(ui.c.textContent,/could not read Codex's status afterwards/);assert.equal(nodes(ui.c,'strong')[0].textContent,'Full access');},async()=>({result:{state:'chosen'},refreshFailed:true}));
});

test('the real App shows the default before Start and wires its plain setting through a status refresh',async()=>{
  const {App}=loadSrc('App');const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  let current=host({roleLimits:{account:{roles:[]}},serverRequests:[]});
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});if(command==='host_status')return structuredClone(current);
    if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    if(command==='set_level'){current={...current,levelDefault:chosen(args.levelId,'chosen')};return {state:'chosen'};}
    throw Error(`Unexpected ${command}`);
  });
  try {
    await React.act(async()=>root.render(React.createElement(App)));
    const start=c.querySelectorAll(e=>e.getAttribute('id')==='workspace-start')[0];
    assert.ok(start.textContent.indexOf('Permission level')<start.textContent.indexOf('Start thread'));
    assert.equal(calls.filter(x=>x.command==='set_level').length,0);
    assert.ok(start.textContent.includes(sentence('APP_DEFAULT_SENTENCE')));
    assert.ok(start.textContent.includes(sentence('APP_DEFAULT_EXPLAINED')));
    assert.ok(start.textContent.includes(sentence('DEFAULT_SCOPE_SENTENCE')));
    const panel=start.querySelectorAll(e=>e.getAttribute('aria-label')==='Permission level for new conversations')[0];
    await React.act(()=>props(nodes(panel,'select')[0]).onChange({target:{value:'edits'}}));
    await React.act(async()=>props(nodes(panel,'button')[0]).onClick());
    assert.deepEqual(calls.filter(x=>x.command==='set_level'),[{command:'set_level',args:{scope:'default',levelId:'edits'}}]);
    assert.match(panel.textContent,/Project edits/);assert.match(panel.textContent,/Chosen by you/);
  } finally {const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);}
});

test('each prepared Send shows its actual destination level, including an ask there, while a different source stays selected',async()=>{
  const {DelegatedTrialComposerView,BringBackComposerView,conversationKey}=loadSrc('TrialComposer');
  const {ContinueAsPanel}=loadSrc('ConversationRoles');
  for(const kind of ['delegated','bring-back','continue-as']) {
    const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
    let destination=thread('destination',{chosen:chosen('supervised','chosen'),agreement:'not-confirmed',takesEffect:'now'});
    const source=thread('source');
    const pending={reference:'trial:1',id:'bring:1',sequence:1,draftName:'invented',card:'Invented trial',text:'invented',transcript:'invented'};
    const common={pending,conversations:[source,destination],message:'inputs',prompt:'inputs',setMessage:()=>{},setPrompt:()=>{},target:conversationKey(destination),setTarget:()=>{},outcome:{state:'unsent'},setOutcome:()=>{},busy:false,ready:true,act:async(command,args)=>{calls.push([command,args]);return {};}};
    const render=()=>{
      const h=host({threads:[source,destination]});
      const composer=kind==='delegated'?React.createElement(DelegatedTrialComposerView,common):kind==='bring-back'?React.createElement(BringBackComposerView,common):React.createElement(ContinueAsPanel,{handoff:{id:'handoff:1',sourceThread:'source',sourceRoleLabel:'HELP_HUMAN',targetRole:'WORKING_ITEMS',draft:{state:'drafted'},draftText:'invented',started:{threadId:'destination',generation:g}},entries:[],homeClass:'account',generation:g,busy:false,ready:true,start:async()=>({ok:true}),send:async text=>{calls.push(['handoff-send',{text,threadId:'destination'}]);return {state:'sent'};},open:()=>{},dismiss:()=>{}});
      root.render(React.createElement(PermissionLevelActions.Provider,{value:{host:h,unavailable:false,stale:false,change:async(owner,scope,levelId)=>{calls.push(['set_level',{scope,levelId}]);return {result:{state:'chosen'},refreshFailed:false};}}},
        React.createElement(PermissionLevel,{host:h,threadId:'source'}),composer));
    };
    try {
      await React.act(render);
      const label=kind==='delegated'?'Trial composer':kind==='bring-back'?'Bring back composer':'Continue as';
      const composer=()=>c.querySelectorAll(e=>e.getAttribute('aria-label')===label)[0];
      const panel=()=>composer().querySelectorAll(e=>e.getAttribute('aria-label')==='Conversation permission level')[0];
      assert.equal(nodes(panel(),'strong')[0].textContent,'Supervised',kind);
      assert.equal(nodes(c,'strong')[0].textContent,'Full access','source is still selected with a different level');
      const send=nodes(composer(),'button').find(b=>b.textContent===(kind==='continue-as'?'Send this message to the new conversation':'Send'));
      assert.ok(send);assert.equal(!!props(send).disabled,false);
      await React.act(async()=>props(send).onClick());
      assert.equal(calls[0][1].threadId,'destination',kind);
      destination=thread('destination',{chosen:null,ask:{sentence:sentence('RECORD_MISSING_SENTENCE'),preselected:'full'}});
      await React.act(render);
      assert.ok(panel().textContent.includes(sentence('RECORD_MISSING_SENTENCE')),kind);
      await React.act(async()=>props(nodes(panel(),'button')[0]).onClick());
      assert.deepEqual(calls.at(-1),['set_level',{scope:{conversation:'destination'},levelId:'full'}],kind);
    } finally {await React.act(()=>root.unmount());document.body.removeChild(c);}
  }
});

test('the real App keeps a setting refusal and a simultaneous refresh failure, without changing the displayed level',async()=>{
  const {App}=loadSrc('App');const {REFRESH_FAILED}=loadSrc('statusRefresh');
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  const h=host({roleLimits:{account:{roles:[]}},serverRequests:[]});let refused=false;
  const message='The level was not recorded in the App ledger (invented failure); nothing was changed';
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){if(refused)throw Error('private refresh diagnostic');return structuredClone(h);}
    if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    if(command==='set_level'){refused=true;throw message;}
    throw Error(`Unexpected ${command}`);
  });
  try {
    await React.act(async()=>root.render(React.createElement(App)));
    const panel=c.querySelectorAll(e=>e.getAttribute('aria-label')==='Permission level for new conversations')[0];
    await React.act(()=>props(nodes(panel,'select')[0]).onChange({target:{value:'edits'}}));
    await React.act(async()=>props(nodes(panel,'button')[0]).onClick());
    assert.ok(panel.textContent.includes(message),'the host refusal is unchanged');
    assert.ok(panel.textContent.includes(REFRESH_FAILED),'the failed read is not lost on rejection');
    assert.doesNotMatch(panel.textContent,/private refresh diagnostic|The App is reading the current permission level/);
    assert.equal(nodes(panel,'strong')[0].textContent,'Full access');
    assert.equal(calls.filter(c=>c.command==='set_level').length,1,'no automatic retry');
  } finally {const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);}
});

test('asking levels carry their consequence, and reading and timing sentences come from the host',async()=>{
  for(const id of ['supervised','edits','edits-network','edits-no-asking','full'])await mounted(host({levelDefault:chosen(id,'chosen')}),undefined,async ui=>{
    assert.ok(ui.c.textContent.includes(sentence('READING_SENTENCE')),id);
    assert.equal(ui.c.textContent.includes(sentence('SUPERVISED_ALLOWING')),['supervised','edits','edits-network'].includes(id),id);
    await ui.show(host({levelDefault:{...chosen(id,'chosen'),readingSentence:'Invented closed host reading sentence.'}}));
    assert.match(ui.c.textContent,/Invented closed host reading sentence/);
    assert.doesNotMatch(ui.c.textContent,/Reading is not limited at any permission level/);
  });
  await mounted(host({threads:[thread('T',{chosen:chosen(),takesEffect:'from-next-turn',takesEffectSentence:'Invented closed timing sentence.'})]}),'T',async ui=>{
    assert.match(ui.c.textContent,/Invented closed timing sentence/);assert.doesNotMatch(ui.c.textContent,/Commands already running/);
  });
});

test('read and inheritance failures preserve host sentences and mark raw details',async()=>{
  const h=host({levelRecordsUnread:sentence('RECORDS_UNREAD_SENTENCE'),levelLaunchRead:{reason:sentence('RECORDS_UNAVAILABLE'),homeState:{state:'unknown',detail:{text:'invented metadata detail'}}},levelSessionOnlyOffered:{detail:{text:'invented ledger detail'}},threads:[thread('T',{chosen:chosen(),inheritancePersistence:{state:'not-confirmed',sentence:sentence('INHERITANCE_NOT_RECORDED'),detail:{text:'invented association detail'}}})]});
  await mounted(h,'T',async ui=>{
    for(const key of ['RECORDS_UNAVAILABLE','RECORDS_UNREAD_SENTENCE','INHERITANCE_NOT_RECORDED'])assert.ok(ui.c.textContent.includes(sentence(key)),key);
    for(const detail of ['invented metadata detail','invented ledger detail','invented association detail'])assert.ok(ui.c.querySelectorAll(e=>e.getAttribute('role')==='group').some(e=>e.textContent.includes(detail)),detail);
    assert.doesNotMatch(ui.c.textContent,/no level is in force|Choose a level to continue/);
    await ui.show({...h,threads:[thread('T',{chosen:chosen(),inheritancePersistence:{state:'pending'}})]});
    assert.ok(!ui.c.textContent.includes(sentence('INHERITANCE_NOT_RECORDED')),'pending is not a failed write');
  });
});

// The real App, its shipped controls and command/refresh wrapper; only the native host is simulated.
async function appWithLevels(initial,change,check){
  const {App}=loadSrc('App');const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  let current=initial;
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});if(command==='host_status')return structuredClone(current);
    if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    if(command==='set_level'){current=change(current,args);if(current.levelChoiceSave?.applied===false)throw current.levelChoiceSave.sentence;return current.levelChoiceSave ?? {state:'chosen'};}
    throw Error(`Unexpected ${command}`);
  });
  try{await React.act(async()=>root.render(React.createElement(App)));await check(c,calls,()=>current);}
  finally{const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);}
}

test('the real App changes one conversation without changing the default or another conversation',async()=>{
  await appWithLevels(host({roleLimits:{account:{roles:[]}},serverRequests:[],threads:[thread('T'),thread('U')]}),
    (h,args)=>({...h,threads:h.threads.map(t=>t.threadId===args.scope.conversation?{...t,level:{...t.level,chosen:chosen(args.levelId,'chosen')}}:t)}),async(c,calls,current)=>{
      const radio=nodes(c,'input').find(e=>props(e).name==='current-conversation'&&props(e).value===JSON.stringify([g,'T']));assert.ok(radio,'shipped conversation chooser');
      await React.act(()=>props(radio).onChange());
      const panel=()=>c.querySelectorAll(e=>e.getAttribute('aria-label')==='Conversation permission level')[0];
      assert.ok(panel().textContent.includes(sentence('APP_DEFAULT_SENTENCE')));
      await React.act(()=>props(nodes(panel(),'select')[0]).onChange({target:{value:'supervised'}}));
      await React.act(async()=>props(nodes(panel(),'button')[0]).onClick());
      assert.deepEqual(calls.filter(x=>x.command==='set_level'),[{command:'set_level',args:{scope:{conversation:'T'},levelId:'supervised'}}]);
      assert.equal(nodes(panel(),'strong')[0].textContent,'Supervised');assert.ok(panel().textContent.includes(sentence('SUPERVISED_ALLOWING')));
      assert.equal(current().levelDefault.id,'full');assert.equal(current().threads[1].level.chosen.id,'full');
    });
});

test('the real App exceptional ask preselects full and one press continues through set_level',async()=>{
  const ask='Invented host case: the recorded choice is unusable. Choose a level to continue.';
  await appWithLevels(host({roleLimits:{account:{roles:[]}},serverRequests:[],levelDefault:null,levelRecordMissing:ask,levelAskPreselected:'full'}),
    (h,args)=>({...h,levelDefault:chosen(args.levelId,'chosen'),levelRecordMissing:null}),async(c,calls)=>{
      const panel=c.querySelectorAll(e=>e.getAttribute('aria-label')==='Permission level for new conversations')[0];
      assert.ok(panel.textContent.includes(ask));assert.equal(props(nodes(panel,'select')[0]).value,'full');assert.equal(calls.filter(x=>x.command==='set_level').length,0);
      const button=nodes(panel,'button')[0];assert.equal(button.textContent,'Use selected level and continue');assert.equal(!!props(button).disabled,false);
      await React.act(async()=>props(button).onClick());
      assert.deepEqual(calls.filter(x=>x.command==='set_level'),[{command:'set_level',args:{scope:'default',levelId:'full'}}]);
      assert.equal(nodes(panel,'strong')[0].textContent,'Full access');assert.match(panel.textContent,/Chosen by you/);assert.ok(!panel.textContent.includes(ask));
    });
});

test('shipped default control separates each saving outcome from the current level and its scope',async()=>{
  for(const variant of ['recorded','no-store','applied-unconfirmed','not-applied-unconfirmed']) {
    const applied=variant!=='not-applied-unconfirmed';
    const origin=variant==='recorded'?'chosen':variant==='no-store'?'session-only':'save-unconfirmed';
    const recorded=variant==='recorded'?'recorded':variant==='no-store'?'not-recorded':'not-confirmed';
    const key=variant==='no-store'?'SESSION_ONLY_SENTENCE':variant==='applied-unconfirmed'?'SAVE_UNCONFIRMED_APPLIED':variant==='not-applied-unconfirmed'?'SAVE_UNCONFIRMED_NOT_APPLIED':null;
    await appWithLevels(host({roleLimits:{account:{roles:[]}},serverRequests:[],threads:[thread('other')]}),
      (h,args)=>({...h,levelDefault:applied?chosen(args.levelId,origin):h.levelDefault,levelChoiceSave:{scope:args.scope,levelId:args.levelId,applied,recorded,state:applied?'chosen':undefined,...(key?{sentence:sentence(key)}:{}),...(recorded==='not-confirmed'?{writeFailure:{text:'invented raw save diagnostic',standing:'Text the App did not write.'}}:{})}}),
      async(c,calls,current)=>{
        const panel=()=>c.querySelectorAll(e=>e.getAttribute('aria-label')==='Permission level for new conversations')[0];
        assert.ok(panel().textContent.includes(sentence('DEFAULT_SCOPE_SENTENCE')),variant);
        await React.act(()=>props(nodes(panel(),'select')[0]).onChange({target:{value:'edits'}}));
        await React.act(async()=>props(nodes(panel(),'button')[0]).onClick());
        assert.equal(nodes(panel(),'strong')[0].textContent,applied?'Project edits':'Full access',variant);
        const save=panel().querySelectorAll(e=>e.getAttribute('aria-label')==='Latest permission-level save attempt')[0];
        assert.ok(save,variant);assert.match(save.textContent,new RegExp(recorded==='recorded'?'Latest choice save: Recorded':recorded==='not-recorded'?'Latest choice save: Not recorded':'Latest choice save: Not confirmed'));
        if(key)assert.ok(save.textContent.includes(sentence(key)),variant);
        assert.equal(panel().textContent.includes(sentence('SESSION_ONLY_SENTENCE')),variant==='no-store',variant);
        if(recorded==='not-confirmed')assert.ok(save.querySelectorAll(e=>e.getAttribute('role')==='group').some(e=>e.textContent.includes('invented raw save diagnostic')));
        assert.ok(!panel().textContent.includes(sentence('INHERITANCE_NOT_RECORDED')),'explicit choice never borrows inheritance fallback');
        assert.equal(current().threads[0].level.chosen.id,'full');
        const radio=nodes(c,'input').find(e=>props(e).name==='current-conversation'&&props(e).value===JSON.stringify([g,'other']));
        await React.act(()=>props(radio).onChange());
        const other=c.querySelectorAll(e=>e.getAttribute('aria-label')==='Conversation permission level')[0];
        assert.equal(other.querySelectorAll(e=>e.getAttribute('aria-label')==='Latest permission-level save attempt').length,0,'default saving outcome never follows a conversation');
        assert.equal(calls.filter(x=>x.command==='set_level').length,1);
      });
  }
});

test('conversation saving outcome belongs only to its scope and a later host read clears it',async()=>{
  const save={scope:{conversation:'T'},levelId:'full',applied:false,recorded:'not-confirmed',sentence:sentence('SAVE_UNCONFIRMED_NOT_APPLIED'),writeFailure:{text:'T raw failure'}};
  const h=host({threads:[thread('T',{chosen:chosen('supervised','chosen')}),thread('U')],levelChoiceSave:save});
  await mounted(h,'T',async ui=>{
    assert.equal(nodes(ui.c,'strong')[0].textContent,'Supervised');assert.ok(ui.c.textContent.includes(save.sentence));
    await ui.show(h,'U');assert.ok(!ui.c.textContent.includes(save.sentence));assert.ok(!ui.c.textContent.includes('T raw failure'));
    await ui.show(h,'T');assert.ok(ui.c.textContent.includes(save.sentence));
    await ui.show({...h,levelChoiceSave:null});assert.ok(!ui.c.textContent.includes(save.sentence));
  });
  await mounted(h,undefined,async ui=>assert.ok(!ui.c.textContent.includes(save.sentence),'conversation save never follows the default control'));
});

test('failed trust writes show requested entry and key without any confirmed-send claim',async()=>{
  for(const requested of ['trusted','untrusted']) {
    const line=`The App tried to send ${requested==='trusted'?'a trusted':'an untrusted'} entry for the project root shown below.`;
    const trust={case:requested==='trusted'?'trusted':'unmarked',requested,requestedKey:'/invented/requested-key',sent:null,sentKey:null,projectRoot:'/invented/project',lines:[line]};
    await mounted(host({threads:[thread('T',{chosen:chosen(),sent:{levelId:'full',writeResult:'not-established'},projectTrust:trust})]}),'T',async ui=>{
      assert.ok(ui.c.textContent.includes(line));assert.match(ui.c.textContent,/Writing it to Codex is not established/);
      assert.match(ui.c.textContent,/Trust entry requested/);assert.match(ui.c.textContent,/Settings key requested/);
      assert.doesNotMatch(ui.c.textContent,/Trust entry sent:|Settings key sent:|Written to Codex\./);
      assert.ok(ui.c.querySelectorAll(e=>e.getAttribute('role')==='group').some(e=>e.textContent.includes(trust.requestedKey)));
      await ui.show(host({threads:[thread('T',{chosen:chosen(),sent:{levelId:'full',writeResult:'written'},projectTrust:{...trust,sent:requested,sentKey:trust.requestedKey,lines:[line.replace('tried to send','sent')]}})]}));
      assert.match(ui.c.textContent,/Trust entry sent:|Settings key sent:/);assert.doesNotMatch(ui.c.textContent,/tried to send/);
    });
  }
});
