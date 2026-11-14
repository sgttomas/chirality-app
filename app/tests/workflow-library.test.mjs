import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The library list's Select offer (WR §4.6 LS-1, SL-1) and the "newer revision
// ‹n› available" notice beside the selection (WR SL-2), in the host's shapes
// (workflow_library.rs registered_listing; runtime_session.rs newer_revision_view).
// The view sends only the person's press; the host selects and records.
const document=installMiniDom();
const React = (await import('react')).default;
const {renderToStaticMarkup} = await import('react-dom/server');
const {createRoot} = await import('react-dom/client');
const {RegisteredRevisions,NewerRevisionNotice,ReviewSelectButtons,WorkflowRootPanel,App}=loadSrc('App');

const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const find=(node,match,found=[])=>{
  if(Array.isArray(node)){for(const n of node)find(n,match,found);return found;}
  if(!node||typeof node!=='object')return found;
  if(typeof node.type==='function')return find(node.type(node.props),match,found);
  if(match(node))found.push(node);
  find(node.props?.children,match,found);return found;
};
const text=n=>renderToStaticMarkup(n).replace(/<[^>]+>/g,'');
const buttons=tree=>find(tree,n=>n.type==='button');
const spy=()=>{const calls=[];return {calls,act:(c,a)=>{calls.push([c,a]);}};};

const held={name:'load-check',sequence:1,revision:'a'.repeat(64),label:'registered — selectable in this App session',selectable:true,offered:'Select; Refine (RF-1)'};
const cold={name:'load-check',sequence:2,revision:'b'.repeat(64),label:'registered — re-confirm to use in this App session',selectable:false,offered:'Refine (RF-1); Review a draft with its bytes (DS-8)'};

test('a held registered revision offers Select; one not held in this process keeps Refine only (LS-1)',()=>{
  const s=spy();
  const tree=RegisteredRevisions({library:'lib-1',rows:[held,cold],busy:false,act:s.act});
  const rows=find(tree,n=>n.type==='li');
  assert.equal(rows.length,2);
  assert.deepEqual(buttons(rows[0]).map(text),['Select revision 1','Refine from the revision store…']);
  assert.deepEqual(buttons(rows[1]).map(text),['Refine from the revision store…'],'no Select without a result held here (RC-2)');
  assert.match(text(rows[1]),/registered — re-confirm to use in this App session/);
  buttons(rows[0])[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_select_listed',{libraryRef:'lib-1',name:'load-check',revision:'a'.repeat(64)}]],'the press names the library whose list was shown');
  assert.ok(buttons(RegisteredRevisions({library:'lib-1',rows:[held],busy:true,act:s.act})).every(b=>b.props.disabled));
});

const selection=(newerRevision)=>({reference:'workflow-selection:1',identity:{name:'load-check',origin:'project',revision:'a'.repeat(64)},standing:'registered revision',runnable:true,newerRevision});

test('the newer-revision notice shows beside the selection and only the press follows it (SL-2, SL-4)',()=>{
  assert.equal(h(NewerRevisionNotice,{selection:selection(null),busy:false,act:()=>{throw new Error('no call');}}),'');
  assert.equal(h(NewerRevisionNotice,{selection:null,busy:false,act:()=>{}}),'');
  const newer={sequence:2,revision:'b'.repeat(64),notice:'newer revision 2 available',selectable:true,offered:'Select revision 2'};
  const html=h(NewerRevisionNotice,{selection:selection(newer),busy:false,act:()=>{throw new Error('rendering sends nothing');}});
  assert.match(html,/newer revision 2 available\. The selection stays on revision aaaaaaaaaaaa until you select another\./);
  const s=spy();
  const [button]=buttons(NewerRevisionNotice({selection:selection(newer),busy:false,act:s.act}));
  assert.equal(text(button),'Select revision 2');
  button.props.onClick();
  assert.deepEqual(s.calls,[['workflow_follow_newer_revision',{selectionRef:'workflow-selection:1',revision:'b'.repeat(64)}]]);
  // Registered in another process: shown, with the re-confirmation route, no button.
  const notHeld={...newer,selectable:false,offered:'registered — re-confirm to use in this App session: Review a draft with its bytes (DS-8), or Refine (RF-1) to make one'};
  const tree=NewerRevisionNotice({selection:selection(notHeld),busy:false,act:s.act});
  assert.equal(buttons(tree).length,0);
  assert.match(text(tree),/newer revision 2 available.*re-confirm to use in this App session/);
  assert.match(h(NewerRevisionNotice,{selection:selection({limit:'library busy; newer revisions not read now'}),busy:false,act:()=>{}}),/Newer revisions: library busy/);
});

test('the workflow panel keeps shared library offers but supplies no chat default',()=>{
  const data={selection:selection({sequence:2,revision:'b'.repeat(64),notice:'newer revision 2 available',selectable:true,offered:'Select revision 2'}),
    activeLibrary:'lib-1',libraries:[{reference:'lib-1',registered:[held,cold]}],reviews:[]};
  const html=h(WorkflowRootPanel,{data,host:{state:'ready',generation:{},threads:[]},act:async()=>{}});
  assert.doesNotMatch(html,/aria-label="Newer revision"/,'no chat has been chosen');
  assert.match(html,/No chat — inspect library content/);
  assert.match(html,/<button disabled="">Select revision 1<\/button>/);
});

// Review finding 1: the press names the library whose list was shown, so the
// host can refuse it once another library is active.
test('the panel sends the shown library with a list Select',async()=>{
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {ok:true};};
  const g={appSession:'invented-session',home:'invented-home',spawnCounter:1};
  const data={context:{sourceRef:'home:owned',generation:g,historyEpoch:0},selections:[],activeLibrary:'lib-2',libraries:[{reference:'lib-1',registered:[held]},{reference:'lib-2',registered:[{...held,sequence:3}]}],reviews:[]};
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);
  await React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host:{state:'ready',generation:g,workflowRoot:data,threads:[{generation:g,threadId:'chat-1'}]},act})));
  const props=el=>el[Object.keys(el).find(k=>k.startsWith('__reactProps$'))];
  assert.equal(container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Select revision 1').length,0,'only the active library is listed');
  const [b]=container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Select revision 3');
  assert.ok(b);
  const [chat]=container.querySelectorAll(e=>e.localName==='select'&&e.textContent.includes('No chat'));
  await React.act(()=>props(chat).onChange({target:{value:'chat-1'}}));
  const [selectedButton]=container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Select revision 3');
  await React.act(async()=>{props(selectedButton).onClick();await new Promise(r=>setTimeout(r,0));});
  assert.deepEqual(calls[0],['workflow_select_listed',{libraryRef:'lib-2',name:'load-check',revision:'a'.repeat(64),context:{sourceRef:'home:owned',generation:g,historyEpoch:0,threadId:'chat-1',selectionRef:null,inspectionRef:null,libraryRef:'lib-2'}}]);
  await React.act(()=>root.unmount());
});

// A retained review's Select is a "Select revision ‹n›" shortcut: it names the
// review and revision only, and the host resolves the revision store (WR SL-4).
test('a retained review offers Select revision ‹n› for what it registered, naming no folder',()=>{
  const s=spy();
  const id=revision=>({name:'load-check',origin:'project',source_root:'/p',revision});
  const review={reference:'review-1',status:{entries:[
    {state:'registered',identity:id('a'.repeat(64))},
    {state:'re-confirmed',identity:id('c'.repeat(64))},
    {state:'not completed',identity:id('d'.repeat(64))}]}};
  const tree=ReviewSelectButtons({review,libraries:[{reference:'lib-1',origin:'project',sourceRoot:'/p',registered:[held]}],busy:false,act:s.act});
  const shown=buttons(tree);
  assert.deepEqual(shown.map(text),['Select revision 1','Select revision cccccccccccc'],'sequence when listed, else the revision prefix; a not-completed entry offers nothing');
  shown[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_select_registered',{reviewRef:'review-1',revision:'a'.repeat(64)}]]);
  assert.doesNotMatch(h(ReviewSelectButtons,{review,libraries:[],busy:false,act:()=>{}}),/holding copy|…/,'no folder picker is implied');
});

// Review probe on #1300: identical content registered as sequence 1 in the project
// library and sequence 3 in the user library. The project review's label comes
// from the project library's own row, in either listing order.
test('a review button takes its sequence from the library holding its tuple',()=>{
  const revision='a'.repeat(64);
  const review={reference:'review-p',status:{entries:[{state:'registered',identity:{name:'load-check',origin:'project',source_root:'/proj',revision}}]}};
  const project={reference:'lib-p',origin:'project',sourceRoot:'/proj',registered:[{...held,sequence:1,revision}]};
  const user={reference:'lib-u',origin:'user',sourceRoot:'/home/u',registered:[{...held,sequence:3,revision}]};
  for(const libraries of [[user,project],[project,user]]){
    assert.deepEqual(buttons(ReviewSelectButtons({review,libraries,busy:false,act:()=>{}})).map(text),['Select revision 1']);
  }
  // Not listed in its own library (only elsewhere): the 12-character fallback, never another library's sequence.
  assert.deepEqual(buttons(ReviewSelectButtons({review,libraries:[user],busy:false,act:()=>{}})).map(text),['Select revision aaaaaaaaaaaa']);
});

test('quoted moved/foreign registration history exposes no action even with forged selectable data',()=>{
  const {RegistrationEvidence}=loadSrc('App');
  const old={identity:{origin:'project',source_root:'/old-library',name:'sample',revision:'same-content'},ledgerSequence:1,outcome:'registered',act:{record_id:'rec:old'},quoted:true,selectable:true,
    claims:[{boundSubject:["workflow revision original-source-tuple"],evidenceLimits:["full tuple relationship mismatched"],decisionActor:{osAccount:'recorded-person',identityVerified:false},installation:{reference:'chirality-installation:quoted',verification:'verified'}}]};
  const tree=RegistrationEvidence({evidence:{rows:[old],limits:[]}});
  assert.deepEqual(buttons(tree),[],'history cannot invoke Select, Refine or an act');
  const rendered=h(RegistrationEvidence,{evidence:{rows:[old],limits:[]}});
  assert.match(rendered,/Quoted registration history/);assert.match(rendered,/\/old-library/);assert.match(rendered,/unverified attribution/);
  assert.match(rendered,/original-source-tuple/);assert.match(rendered,/full tuple relationship mismatched/);
  assert.match(h(RegistrationEvidence,{evidence:{rows:[{...old,claims:[{decisionActor:{},installation:{reference:null}}]}],limits:[]}}),/Capturing installation unknown/);
});

test('records capability binding reports cold unknown and publication limits for the current generation',()=>{
  const {RecordsCapabilityBindings}=loadSrc('App');const generation={appSession:'current',home:'home',spawnCounter:1};
  const host={generation,threads:[{generation,threadId:'cold',recordsCapabilityBinding:{state:'unknown/unsupported',limit:'original receipt absent'}},{generation,threadId:'hot',recordsCapabilityBinding:{state:'bound in current generation',persistence:'memory-only',limit:'folder flush unconfirmed'}},{generation:{...generation,appSession:'old'},threadId:'stale',recordsCapabilityBinding:{state:'bound in old generation'}}]};
  assert.deepEqual(buttons(RecordsCapabilityBindings({host})),[]);
  const text=h(RecordsCapabilityBindings,{host});assert.match(text,/unknown\/unsupported/);assert.match(text,/original receipt absent/);assert.match(text,/memory-only/);assert.match(text,/folder flush unconfirmed/);assert.doesNotMatch(text,/stale/);
  assert.ok(text.includes('hot: bound in current generation.'),'a bound row whose basis is not stated is given no meaning it may not have');
  assert.ok(!text.includes('cold: unknown/unsupported ('),'the meaning is given only for a binding');
  const bound=(basis)=>h(RecordsCapabilityBindings,{host:{generation,threads:[{generation,threadId:'t',recordsCapabilityBinding:{state:'bound in current generation',basis}}]}});
  assert.ok(bound('receipt').includes('t: bound in current generation (a receipt held for this conversation; whether the project at its path is still the one it names is checked again on every read).'));
  assert.ok(bound('offer').includes('t: bound in current generation (offered to this conversation when it started in this generation, with no receipt held; whether the project at its path is still the one offered is checked again on every read).'));
  assert.ok(bound('fork of an offered conversation').includes('t: bound in current generation (admitted to this conversation as a fork of one offered it in this generation, with no receipt held; whether the project at its path is still the one offered is checked again on every read).'));
  for (const basis of ['receipt','offer','fork of an offered conversation']) assert.ok(!bound(basis).includes('validated'),'none says the project now there is validated');
});

test('the read log limit is shown whole with the records capability, with or without bound conversations (LIM-014)',()=>{
  const {RecordsCapabilityBindings}=loadSrc('App');const generation={appSession:'current',home:'home',spawnCounter:1};
  const sentence="This project's records capability cannot answer reads until its read log is set aside: rename /a/very/long/store/path/projects/key/reads/records-reads.jsonl, in the same folder, to exactly records-reads.jsonl.torn-2026-11-13T19-17-38.143Z. That file ends in a read that was not recorded completely, so this capability cannot record or answer another read; nothing already recorded is lost.";
  const alone=h(RecordsCapabilityBindings,{host:{generation,threads:[],recordsCapability:{readLogLimit:sentence}}});
  assert.ok(alone.includes(sentence.replace(/'/g,'&#x27;')),alone);
  assert.match(alone,/role="alert"/);
  assert.deepEqual(buttons(RecordsCapabilityBindings({host:{generation,threads:[],recordsCapability:{readLogLimit:sentence}}})),[]);
  assert.equal(h(RecordsCapabilityBindings,{host:{generation,threads:[],recordsCapability:{readLogLimit:null}}}),'');
});

test('one existing library entry goes from in-place review to an explicit native registration press',async()=>{
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {ok:true};};
  let data={selection:null,activeLibrary:'lib-one',libraries:[{reference:'lib-one',registered:[]}],reviews:[]};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  const props=el=>el[Object.keys(el).find(k=>k.startsWith('__reactProps$'))];
  const render=()=>root.render(React.createElement(WorkflowRootPanel,{data,host:{state:'ready',generation:{},threads:[]},act}));
  await React.act(render);
  const [name]=container.querySelectorAll(e=>e.localName==='input');
  await React.act(()=>props(name).onChange({target:{value:'sample'}}));
  const [review]=container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Review this unregistered in-place library entry');
  assert.ok(review);assert.equal(props(review).disabled,false);
  await React.act(async()=>{props(review).onClick();await new Promise(r=>setTimeout(r,0));});
  assert.deepEqual(calls,[['workflow_review',{names:['sample'],inPlace:true}]],'review requests no draft creation or act');
  data={...data,activeReview:'review-one',reviews:[{reference:'review-one',status:{state:'reviewed; native A15 not captured',presentation:{entries:[{disposition:'in place',message:'Synthetic in-place review'}]}}}]};
  await React.act(render);
  const [register]=container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Register this review through native A15 confirmation…');
  assert.ok(register);assert.equal(props(register).disabled,false);
  await React.act(async()=>{props(register).onClick();await new Promise(r=>setTimeout(r,0));});
  assert.deepEqual(calls[1],['workflow_register_native',{reviewRef:'review-one'}],'the press only opens host-owned native confirmation');
  await React.act(()=>root.unmount());
});

// Host shapes from WorkflowReviewContext::accept_result/advance and Root::snapshot.
// Exercise App's real handlers and refresh with an invented native invoke boundary.
test('native review actions end with the host presentation while original continuation and Select remain',async(t)=>{
  const presentationSource=loadSrc('presentation');
  const {reviewDigest,readablePaths}=presentationSource;
  const generation={appSession:'session-review',home:'home-review',spawnCounter:1};
  const identity={name:'load-check',origin:'project',source_root:'/synthetic',revision:'a'.repeat(64)};
  const props=el=>el[Object.keys(el).find(k=>k.startsWith('__reactProps$'))];
  const controls=article=>article.querySelectorAll(e=>e.localName==='button');
  const native=article=>controls(article).find(e=>/^(Register this review|Re-confirm this revision)/.test(e.textContent));
  for(const disposition of ['new workflow','re-confirmation']){
    const outcomes=[
      ['completed',{status:{state:'original registration attempt advanced',entries:[{state:disposition==='re-confirmation'?'re-confirmed':'registered',identity,actRef:'synthetic-act'}]}}],
      ['dismissed',{status:{state:'native confirmation dismissed; no capture/registration'}}],
      ['capture unavailable',{status:{state:'native review/capture unavailable; original owner state retained',limit:'synthetic refusal',registration:'not completed; no fabricated receipt or retry'}}],
      ['capture pending',{status:{state:'actual captured A15 record pending',captureId:'synthetic-capture',reason:'record write pending',registration:'not authorized until actual hot receipt'}}],
      ['transaction pending',{status:{state:'original registration attempt advanced',entries:[{state:'pending; not registered',identity,reason:'synthetic publication pending'}]}}],
      ['review lock pending',{state:'original native review interaction pending'}],
    ];
    for(const [outcome,resultRow] of outcomes){
      const presentation={entries:[{disposition,message:'Complete synthetic review',content:'workflow content',...(disposition==='re-confirmation'?{reconfirmation:{statement:'Synthetic re-confirmation statement'}}:{})}]};
      const fresh={reference:'review-native',status:{state:'reviewed; native A15 not captured',presentation}};
      const data={context:{sourceRef:'home:synthetic',generation,historyEpoch:0},activeLibrary:'lib-native',activeReview:fresh.reference,
        libraries:[{reference:'lib-native',origin:'project',sourceRoot:'/synthetic',registered:[held]}],reviews:[fresh]};
      let snapshot={state:'ready',generation,threads:[{generation,threadId:'chat-native'}],workflowRoot:data};
      const calls=[];
      const nativeDigestRelease=Promise.withResolvers(),viewDigestComputed=Promise.withResolvers();
      const digestRead=t.mock.method(presentationSource,'reviewDigest',content=>{
        const pending=reviewDigest(content);
        viewDigestComputed.resolve(pending);
        return pending;
      });
      const idle=installIdleNativeWaiting(async(command,args)=>{
        calls.push([command,args]);
        if(command==='host_status')return snapshot;
        if(command==='decision_view')return {rows:[]};
        if(command==='native_confirmation_content')return [];
        if(command==='workflow_review_digest'){
          const digest=await reviewDigest(presentation);
          await nativeDigestRelease.promise;
          return {digest};
        }
        if(command==='workflow_register_native'){
          snapshot={...snapshot,workflowRoot:{...data,reviews:[{reference:fresh.reference,...resultRow}]}};
          return resultRow.status??resultRow;
        }
        if(command==='workflow_continue_registration'||command==='workflow_select_registered')return {state:'synthetic original operation returned'};
        throw Error(`Unexpected native command: ${command}`);
      });
      const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
      const article=()=>container.querySelectorAll(e=>e.localName==='article'&&e.querySelectorAll(n=>n.localName==='h3'&&n.textContent==='Current review · review-native').length)[0];
      const body=()=>article().querySelectorAll(e=>e.localName==='pre')[0];
      try{
        await React.act(()=>root.render(React.createElement(App)));
        // Deliver the native reply inside act and await the view's real hash too:
        // neither one timer tick nor an independent expected hash waits for both.
        await React.act(async()=>{nativeDigestRelease.resolve();await viewDigestComputed.promise;});
        const reading=article().querySelectorAll(e=>e.getAttribute('aria-label')==='Frozen workflow registration review')[0];
        assert.ok(reading,'the current frozen presentation has a readable review');
        assert.ok(reading.textContent.includes('Complete synthetic review'));
        assert.equal(reading.querySelectorAll(e=>e.localName==='pre').at(-1).textContent,JSON.stringify(presentation,null,2),'the complete original presentation remains in its diagnostic report');
        const digest=await reviewDigest(presentation);assert.ok(article().textContent.includes(digest));
        assert.ok(article().textContent.includes(`Read the complete review below before choosing ${disposition==='re-confirmation'?'Re-confirm':'Register'}`),'fresh presentation retains the read-first action cue');
        const button=native(article());assert.ok(button);assert.equal(props(button).disabled,false);
        assert.ok(button.textContent.startsWith(disposition==='re-confirmation'?'Re-confirm':'Register'));
        assert.ok(!calls.some(([c])=>c==='workflow_register_native'),'rendering never opens confirmation');
        await React.act(async()=>{props(button).onClick();await new Promise(r=>setTimeout(r,0));});
        assert.deepEqual(calls.filter(([c])=>c==='workflow_register_native'),[['workflow_register_native',{reviewRef:fresh.reference}]],'one exact original command, no retry');
        assert.ok(!native(article()),`${disposition}: ${outcome} no longer supplies a native review action`);
        assert.equal(snapshot.workflowRoot.activeReview,fresh.reference,'original review stays active');
        assert.equal(body().textContent,JSON.stringify(readablePaths(resultRow.status??{reference:fresh.reference,...resultRow}),null,2),'complete reported result or pending row stays visible');
        assert.ok(article().textContent.includes(digest),'last shown digest evidence stays visible');
        assert.ok(article().textContent.includes('as last shown with the review'));
        assert.ok(!article().textContent.includes('Read the complete review below before choosing'),'result/pending status gets no forward registration cue');
        const continuation=controls(article()).find(e=>e.textContent==='Continue original captured registration');
        assert.ok(continuation);assert.equal(props(continuation).disabled,false);
        await React.act(async()=>{props(continuation).onClick();await new Promise(r=>setTimeout(r,0));});
        assert.deepEqual(calls.filter(([c])=>c==='workflow_continue_registration'),[['workflow_continue_registration',{reviewRef:fresh.reference}]],'Continue keeps original owner reference');
        const select=controls(article()).find(e=>e.textContent==='Select revision 1');
        if(outcome==='completed'){
          assert.ok(select);assert.equal(props(select).disabled,true,'selection still requires a workflow chat');
          const [chat]=container.querySelectorAll(e=>e.localName==='select'&&e.textContent.includes('No chat — inspect library content'));
          await React.act(()=>props(chat).onChange({target:{value:'chat-native'}}));
          const selectable=controls(article()).find(e=>e.textContent==='Select revision 1');assert.equal(props(selectable).disabled,false);
          await React.act(async()=>{props(selectable).onClick();await new Promise(r=>setTimeout(r,0));});
          assert.deepEqual(calls.filter(([c])=>c==='workflow_select_registered'),[['workflow_select_registered',{reviewRef:fresh.reference,revision:identity.revision,context:{sourceRef:'home:synthetic',generation,historyEpoch:0,threadId:'chat-native',selectionRef:null,inspectionRef:null,libraryRef:'lib-native'}}]]);
        }else assert.ok(!select,'incomplete attempts supply no Select result');
        assert.equal(calls.filter(([c])=>c==='workflow_register_native').length,1,'continuation/selection never reopens native capture');
      }finally{
        const renderedText=container.textContent;await React.act(()=>root.unmount());container.parentNode.removeChild(container);digestRead.mock.restore();idle.restore(renderedText);
      }
    }
  }
});

test('draft creation requires an explicit name and explains the current source/library/content prerequisite',async()=>{
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  const props=n=>n[Object.keys(n).find(k=>k.startsWith('__reactProps$'))];
  const nodes=tag=>c.querySelectorAll(n=>n.localName===tag);
  const create=()=>nodes('button').find(n=>n.textContent==='Create draft from inspected content');
  const input=()=>nodes('label').find(n=>n.textContent.startsWith('New draft name')).querySelectorAll(n=>n.localName==='input')[0];
  const guidance=()=>c.querySelectorAll(n=>n.getAttribute('id')==='workflow-draft-next-step')[0].textContent;
  let data={context:{sourceRef:'draft-source',generation:null},libraries:[],reviews:[],runs:[]};
  const host=()=>({generation:null,state:'not started',threads:[],workflowRoot:data});
  const show=()=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host:host(),act:async(command,args)=>{calls.push([command,args]);return {state:'controlled result'};}})));
  try {
    await show();assert.equal(props(input()).value,'');assert.match(guidance(),/Open a project or user/);assert.equal(props(create()).disabled,true);
    data={...data,activeLibrary:'lib',libraries:[{reference:'lib',origin:'user',sourceRoot:'/explicit-library',registered:[]}]};await show();assert.match(guidance(),/Inspect bundled content/);assert.match(c.textContent,/Draft destination: user library · \/explicit-library/);
    data={...data,inspection:{reference:'inspected',identity:{name:'different-method',origin:'project',revision:'exact'},standing:'inspected',runnable:false}};await show();
    assert.match(guidance(),/Enter a name/);assert.equal(props(input()).value,'','no name inferred from an example or inspected content');
    await React.act(()=>props(input()).onChange({target:{value:'   '}}));assert.equal(props(create()).disabled,true);
    await React.act(()=>props(input()).onChange({target:{value:' Exact chosen name '}}));assert.equal(props(create()).disabled,false);assert.match(guidance(),/does not register or run/);
    await React.act(async()=>props(create()).onClick());
    assert.equal(calls[0][0],'workflow_create_draft');assert.equal(calls[0][1].name,' Exact chosen name ','UI does not trim or normalize the exact submitted name');
    assert.equal(calls[0][1].context.inspectionRef,'inspected');assert.equal(calls[0][1].context.libraryRef,'lib');
    assert.deepEqual(calls.map(c=>c[0]),['workflow_create_draft','workflow_observe_drafts']);
    data={...data,context:null};await show();assert.equal(props(create()).disabled,true);assert.match(guidance(),/source is unavailable or changed/);
  } finally {await React.act(()=>root.unmount());document.body.removeChild(c);}
});

test('disk-consistency rows remain selectable and disclose unverified approval',()=>{
  const row={...cold,selectable:true,reconfirm:false,evidence:'disk-consistency',label:'registered — Disk consistency checked; approval authenticity unverified'};
  const s=spy();const tree=RegisteredRevisions({library:'lib-1',rows:[row],busy:false,act:s.act});
  assert.match(text(tree),/Disk consistency checked; approval authenticity unverified/);
  buttons(tree)[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_select_listed',{libraryRef:'lib-1',name:row.name,revision:row.revision}]]);
});

const setting=(over={})=>({level:'robust',policy:'Require verified approval',source:'Stored in this App\'s settings',
  verification:{state:'unavailable on this build',available:false,detail:'This is an unsigned or development build.'},
  storage:"Stored in this App's settings file, outside any project. Until keychain protection is set up, an agent able to write that file could change this setting.",
  robustWithoutVerification:'Session confirmation required; persistent verification unavailable',
  lowering:'Choosing "Allow disk records" needs your native confirmation; no command or project file lowers it.',
  protect:{offered:false,reason:'This is an unsigned or development build. Keychain protection needs the signed App with its selected signing identity (team, access group); development file keys are never used for it.'},...over});

test('approval setting shows the policy, verification availability and the disclosed file gap',()=>{
  const {WorkflowAssuranceSetting}=loadSrc('App');
  const html=renderToStaticMarkup(React.createElement(WorkflowAssuranceSetting,{setting:setting(),act:()=>{throw Error('rendering changes nothing');}}));
  assert.match(html,/Workflow approval: Require verified approval/);
  assert.match(html,/Keychain verification: <strong>unavailable on this build/);
  assert.match(html,/Session confirmation required; persistent verification unavailable/);
  assert.match(html,/an agent able to write that file could change this setting/);
  assert.match(html,/Allow disk records \(native confirmation\)/);
  assert.match(html,/Protect registered workflows with your keychain: unavailable\. This is an unsigned or development build/);
  assert.doesNotMatch(html,/Protect registered workflows with your keychain…/);
});

test('approval setting offers keychain protection and recovery only where they apply',()=>{
  const {WorkflowAssuranceSetting}=loadSrc('App');
  const offered=renderToStaticMarkup(React.createElement(WorkflowAssuranceSetting,{setting:setting({verification:{state:'not set up',available:false,detail:'Keychain protection is not set up.'},protect:{offered:true}}),act:()=>{}}));
  assert.match(offered,/Protect registered workflows with your keychain…/);
  const recovery=renderToStaticMarkup(React.createElement(WorkflowAssuranceSetting,{setting:setting({verification:{state:'recovery required',available:false,detail:'keychain locked. Verified approval is required until recovered; nothing is relaxed automatically.'},storage:'Stored in your keychain.',protect:{offered:false,reason:'Recover the protected policy first.'}}),act:()=>{}}));
  assert.match(recovery,/Restore verified approval in your keychain/);
  assert.match(recovery,/Check keychain again/);
  assert.match(recovery,/nothing is relaxed automatically/);
  const relaxed=renderToStaticMarkup(React.createElement(WorkflowAssuranceSetting,{setting:setting({level:'relaxed',policy:'Allow disk records'}),act:()=>{}}));
  assert.match(relaxed,/Workflow approval: Allow disk records/);
  assert.doesNotMatch(relaxed,/Session confirmation required/);
});

test('approval evidence labels never infer evidence from registered standing',()=>{
  const {workflowAssurance}=loadSrc('workflowSelection');
  assert.equal(workflowAssurance({requested_policy:'relaxed',admission_evidence:'disk-consistency'}),'Disk consistency checked; approval authenticity unverified. Policy: Allow disk records.');
  assert.equal(workflowAssurance({requested_policy:'robust',admission_evidence:'keychain-verified approval'}),'Approval verified by keychain seal. Policy: Require verified approval.');
  assert.equal(workflowAssurance({requested_policy:'robust',admission_evidence:'in-process A15'}),'Approved in this App session (native A15). Policy: Require verified approval.');
  assert.equal(workflowAssurance(undefined),'Approval evidence unknown (not recorded).');
  assert.equal(workflowAssurance('in-process A15'),'Approval evidence unknown (not recorded).');
});

// Review of pull request 241: a press the view refuses before any host command
// (its conversation is no longer loaded) was neither failed nor settled, so
// the guide said nothing and the only message sat in the closed studio.
test('a press refused before any host command is said under the Run guide\'s Next line with the studio closed',async()=>{
  const g={home:'account',appSession:'s1',spawnCounter:1};
  const data={context:{sourceRef:'src',generation:g},projectLibraryAvailable:true,activeLibrary:null,libraries:[],selections:[],runs:[],reviews:[],drafts:{drafts:[]}};
  const host=threads=>({state:'ready',generation:g,workflowRoot:data,threads,serverRequests:[]});
  const loaded=[{generation:g,threadId:'T1',model:'invented-model',status:{type:'idle'}}];
  const c=document.createElement('div');const root=createRoot(c);const calls=[];
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const show=threads=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host:host(threads),view:'run',act:async(command,args)=>{calls.push([command,args]);return {state:'controlled result'};}})));
  await show(loaded);
  const guide=()=>c.querySelectorAll(n=>n.getAttribute('aria-label')==='Run a workflow')[0];
  const select=guide().querySelectorAll(n=>n.localName==='select')[0];
  await React.act(async()=>props(select).onChange({target:{value:'T1'}}));
  await show([]); // same source and generation; the chosen conversation is no longer loaded
  const press=guide().querySelectorAll(n=>n.localName==='button').find(n=>n.textContent==="Show this project's workflows");
  assert.equal(!!props(press).disabled,false,'the button is offered');
  await React.act(async()=>props(press).onClick());
  assert.deepEqual(calls,[],'no host command was issued');
  const result=c.querySelectorAll(n=>n.getAttribute('aria-label')==='Run a workflow — last result')[0];
  assert.ok(result,'the refusal is shown in the guide');
  assert.equal(result.getAttribute('role'),'alert');
  assert.match(result.textContent,/^Couldn't show this project's workflows: the conversation chosen here is no longer open in this view, so nothing was done\. Choose the conversation again/);
  const studio=c.querySelectorAll(n=>n.getAttribute('id')==='workflow-studio')[0];
  assert.notEqual(props(studio).open,true,'the studio is closed');
  for(let node=result;node;node=node.parentNode)assert.notEqual(node,studio,'the result is outside the studio');
  await React.act(async()=>root.unmount());
});

// Whether what the panel shows may be from before the last command is the App's
// to say (hostReads.ts: tests/host-reads.test.mjs has its order, the commands
// that mark and the mounted App). The panel hands that to both guides and
// keeps no marker of its own, so a command issued outside it withholds them too.
test('the panel shows its guides only when the App says the view follows the last command, and passes a failed read through',async()=>{
  const g={home:'account',appSession:'s1',spawnCounter:1};
  const prepared={reference:'run-1',conversation:'T1',home:'account',generation:g,preparationOrder:0,workflow:{name:'invented-flow'},lifecycle:{state:'prepared; not a run until its start turn is observed'},status:{}};
  const data={context:{sourceRef:'src',generation:g},projectLibraryAvailable:true,activeLibrary:null,libraries:[],reviews:[],drafts:{drafts:[]},
    selections:[{sourceRef:'src',threadId:'T1',selection:{state:'selected',reference:'sel',runnable:true,identity:{name:'invented-flow',origin:'project',revision:'rev-1-0123456789'}}}],runs:[prepared]};
  const host={state:'ready',generation:g,workflowRoot:data,threads:[{generation:g,threadId:'T1',model:'invented-model',status:{type:'idle'}}],serverRequests:[]};
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const WITHHELD=/Next: What this view showed may be from before the App's last operation finished\./,CACHED=/Ready to start|has not been sent|Nothing has been sent yet|Ready to run/;
  for(const [view,label,offerComposer] of [['run','Run a workflow',undefined],['make','Make a workflow from your work',()=>{}]]){
    const c=document.createElement('div');const root=createRoot(c);const calls=[];
    const show=over=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host,view,offerComposer,act:async(command,args)=>{calls.push([command,args]);return {};},...over})));
    const guide=()=>c.querySelectorAll(n=>n.getAttribute('aria-label')===label)[0];
    await show({});
    if(view==='run')await React.act(async()=>props(guide().querySelectorAll(n=>n.localName==='select')[0]).onChange({target:{value:'T1'}}));
    assert.doesNotMatch(guide().textContent,WITHHELD,`${view}: no marker, the steps are shown`);
    if(view==='run')assert.match(guide().textContent,CACHED);
    await show({viewStale:true});
    assert.match(guide().textContent,WITHHELD,`${view}: withheld on the App's word`);assert.doesNotMatch(guide().textContent,CACHED);
    assert.deepEqual(guide().querySelectorAll(n=>n.localName==='button').filter(n=>!/Show the conversation/.test(n.textContent)),[],`${view}: nothing from before the command is offered`);
    assert.doesNotMatch(guide().textContent,/The last read failed/);
    await show({viewStale:true,readFailure:'Error: invented status failure'});
    assert.match(guide().textContent,/The last read failed: Error: invented status failure/,`${view}: the failed read is said in the guide`);
    // A failed read with nothing marked withholds nothing; both guides say it above their steps.
    await show({viewStale:false,readFailure:'Error: invented status failure'});
    assert.doesNotMatch(guide().textContent,WITHHELD);
    assert.match(guide().textContent,/The App's last read of its state failed \(Error: invented status failure\)\. What is shown here was read before that\./,`${view}: a failed read is said above the steps`);
    await show({viewStale:false,readFailure:null});
    assert.doesNotMatch(guide().textContent,/read of its state failed/);
    assert.doesNotMatch(guide().textContent,WITHHELD,`${view}: a later read applied, the steps return`);
    assert.deepEqual(calls,[],`${view}: showing or withholding issues no command`);
    await React.act(async()=>root.unmount());
  }
});
// The included-workflows chooser's tests run with this file, which the web
// suite's script and both hosted presentation steps already list. The script
// itself is not changed: app/package.json's bytes are pinned by the notices basis.
await import('./included-workflows.test.mjs');
// Reading a workflow's own text in Run a workflow, run here for the same reason.
await import('./workflow-text.test.mjs');
