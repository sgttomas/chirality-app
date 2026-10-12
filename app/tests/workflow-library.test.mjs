import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The library list's Select offer (WR §4.6 LS-1, SL-1) and the "newer revision
// ‹n› available" notice beside the selection (WR SL-2), in the host's shapes
// (workflow_library.rs registered_listing; runtime_session.rs newer_revision_view).
// The view sends only the person's press; the host selects and records.
installMiniDom();
const React = (await import('react')).default;
const {renderToStaticMarkup} = await import('react-dom/server');
const {RegisteredRevisions,NewerRevisionNotice,WorkflowRootPanel}=loadSrc('App');

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
  const tree=RegisteredRevisions({rows:[held,cold],busy:false,act:s.act});
  const rows=find(tree,n=>n.type==='li');
  assert.equal(rows.length,2);
  assert.deepEqual(buttons(rows[0]).map(text),['Select revision 1','Refine from the revision store…']);
  assert.deepEqual(buttons(rows[1]).map(text),['Refine from the revision store…'],'no Select without a result held here (RC-2)');
  assert.match(text(rows[1]),/registered — re-confirm to use in this App session/);
  buttons(rows[0])[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_select_listed',{name:'load-check',revision:'a'.repeat(64)}]]);
  assert.ok(buttons(RegisteredRevisions({rows:[held],busy:true,act:s.act})).every(b=>b.props.disabled));
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
