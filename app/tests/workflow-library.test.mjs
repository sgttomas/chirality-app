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
        assert.equal(body().textContent,JSON.stringify(readablePaths(fresh.status),null,2),'complete current review stays visible');
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
