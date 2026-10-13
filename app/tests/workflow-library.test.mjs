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
const {RegisteredRevisions,NewerRevisionNotice,ReviewSelectButtons,WorkflowRootPanel}=loadSrc('App');

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

test('the workflow panel places the list offers and the notice',()=>{
  const data={selection:selection({sequence:2,revision:'b'.repeat(64),notice:'newer revision 2 available',selectable:true,offered:'Select revision 2'}),
    activeLibrary:'lib-1',libraries:[{reference:'lib-1',registered:[held,cold]}],reviews:[]};
  const html=h(WorkflowRootPanel,{data,host:{state:'ready',generation:{},threads:[]},act:async()=>{}});
  assert.match(html,/aria-label="Newer revision"[^>]*>newer revision 2 available/);
  assert.match(html,/<button>Select revision 2<\/button>/);
  assert.match(html,/<button>Select revision 1<\/button>/);
});

// Review finding 1: the press names the library whose list was shown, so the
// host can refuse it once another library is active.
test('the panel sends the shown library with a list Select',async()=>{
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {ok:true};};
  const data={selection:null,activeLibrary:'lib-2',libraries:[{reference:'lib-1',registered:[held]},{reference:'lib-2',registered:[{...held,sequence:3}]}],reviews:[]};
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);
  await React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host:{state:'ready',generation:{},threads:[]},act})));
  const props=el=>el[Object.keys(el).find(k=>k.startsWith('__reactProps$'))];
  assert.equal(container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Select revision 1').length,0,'only the active library is listed');
  const [b]=container.querySelectorAll(e=>e.localName==='button'&&e.textContent==='Select revision 3');
  assert.ok(b);
  await React.act(async()=>{props(b).onClick();await new Promise(r=>setTimeout(r,0));});
  assert.deepEqual(calls[0],['workflow_select_listed',{libraryRef:'lib-2',name:'load-check',revision:'a'.repeat(64)}]);
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
