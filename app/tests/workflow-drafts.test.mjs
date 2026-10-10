import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';

const load=name=>{
  const url=new URL(`../src/${name}.tsx`,import.meta.url);
  const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX}});
  const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;
};
const {WorkflowDraftsView,DraftRow,draftStateWords,attributionWords}=load('WorkflowDrafts');

// Drafts in the host shape (WorkflowRootSession::drafts_view over
// registration::drafts::observe_drafts in the Rust host).
const content={method:'chirality.app.workflow-package.sha256/v1',value:'0123456789abcdef0123'};
const key={draft_location:'project',draft_root:'/p/.chirality/workflow-drafts',name:'load-check'};
const draft=(extra={})=>({name:'load-check',state:'draft',content,fileCount:2,findings:[],base:null,
  baseLimit:'no App-recorded base: a draft the agent or person wrote (WR §3, U-WR-12)',attribution:{kind:'not observed'},
  reference:{draft:key},slot:{registeredRevisions:0,identicalTo:null},tryLimit:null,reviewLimit:null,trials:[],
  standing:'draft — not a registered workflow; no workflow identity (EXEC TR-1)',...extra});
const attachments={ownerRef:'attachment-owner:1',listRevision:3};
const buttons=(node,found=[])=>{
  if(Array.isArray(node)){for(const n of node)buttons(n,found);return found;}
  if(!node||typeof node!=='object')return found;
  if(node.type==='button')found.push(node);
  if(typeof node.type==='function')return buttons(node.type(node.props),found);
  buttons(node.props?.children,found);return found;
};
const press=(d,label,atts=attachments)=>{const calls=[];const tree=DraftRow({draft:d,attachments:atts,busy:false,act:async(c,a)=>{calls.push([c,a]);}});
  const b=buttons(tree).find(b=>renderToStaticMarkup(b).includes(label));assert.ok(b,`button ${label}`);return {disabled:b.props.disabled,press:()=>{b.props.onClick();return calls;}};};
const html=(d,atts=attachments)=>renderToStaticMarkup(React.createElement(DraftRow,{draft:d,attachments:atts,busy:false,act:async()=>{}}));

test('each WR §5.1 state reads in the NIR §7 words, never as acceptance or checking',()=>{
  assert.equal(draftStateWords('draft'),'draft — not registered');
  assert.equal(draftStateWords('not valid'),'draft — not valid for registration');
  assert.equal(draftStateWords('changed since review'),'changed since review — review again before registering');
  assert.match(draftStateWords('under review',content),/under review \(reviewed content 0123456789ab\)/);
  assert.match(draftStateWords('registered, unchanged since'),/^registered, unchanged since/);
  assert.match(draftStateWords('future-state'),/reported as “future-state”/);
  for(const s of ['draft','not valid','under review','changed since review','registered, unchanged since'])
    assert.doesNotMatch(draftStateWords(s,content),/accept|approv|check(ed)?\b|reli|verified/i);
});

test('attribution reads "not observed" unless the host observed a file change item or an App action (D-3)',()=>{
  assert.equal(attributionWords({kind:'not observed'}),'not observed');
  assert.equal(attributionWords(undefined),'not observed');
  assert.equal(attributionWords({kind:'guessed'}),'not observed');
  assert.match(attributionWords({kind:'file change item',thread:'T',item:'fc-1'}),/file-change item fc-1 \(conversation T\)/);
  assert.match(attributionWords({kind:'app action'}),/written by this App/);
  assert.match(html(draft()),/Attribution: not observed\./);
});

test('Try in a conversation only pre-fills the attachment list; nothing is sent by the App (TT-3, AT-8)',()=>{
  const t=press(draft(),'Try in a conversation');
  assert.equal(t.disabled,false);
  assert.deepEqual(t.press(),[['workflow_try_draft',{ownerRef:'attachment-owner:1',listRevision:3,name:'load-check'}]]);
  const h=html(draft());
  assert.match(h,/sends nothing/);
  assert.match(h,/not a workflow run, not registration/);
  assert.equal(press(draft({tryLimit:'cannot be tried: content identity not established (HY-3)'}),'Try in a conversation').disabled,true);
  assert.equal(press(draft(),'Try in a conversation',{state:'unavailable'}).disabled,true,'no attachment list, no pre-fill');
});

test('a draft is reviewed by its listed name and a refused draft shows its refusal',()=>{
  assert.deepEqual(press(draft(),'Review for registration').press(),[['workflow_review_draft',{name:'load-check'}]]);
  const refused=draft({state:'not valid',findings:['HY-4: operating-system entry .DS_Store'],reviewLimit:'cannot be reviewed for registration (DS-5): HY-4: operating-system entry .DS_Store'});
  assert.equal(press(refused,'Review for registration').disabled,true);
  const h=html(refused);
  assert.match(h,/HY-4: operating-system entry .DS_Store/);
  assert.match(h,/DS-5/);
  assert.match(h,/separate A15 act through the native confirmation/,'registration stays the person’s act');
});

test('trial pointers and bases are shown as the host reported them',()=>{
  const tried=draft({base:{name:'load-check',revision:'abcdef012345678',origin:'project'},
    trials:[{conversation:'thread-a',time:'2026-10-10T00:00:00Z',content,contentNow:'changed since it was tried',standing:'draft tried in conversation; not a run of any workflow identity'}]});
  const h=html(tried);
  assert.match(h,/App-recorded base: load-check revision abcdef012345/);
  assert.match(h,/Tried in conversation thread-a at 2026-10-10T00:00:00Z with content 0123456789ab \(changed since it was tried\)\. draft tried in conversation; not a run of any workflow identity\./);
  assert.match(html(draft()),/no App-recorded base/);
});

test('the list offers the project library, refresh and observed changes',()=>{
  const data={library:'workflow-library:1',observedAt:'2026-10-10T00:00:01Z',limit:null,standing:'observed by this App when listed',drafts:[draft(),draft({name:'site-visit'})],
    transitions:[{time:'t1',draft:{name:'load-check'},event:'written',from:'absent',to:'draft',attribution:{kind:'not observed'}}]};
  const h=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data,attachments,workspace:true,busy:false,act:async()=>{}}));
  assert.match(h,/Open this App project’s workflow library/);
  assert.match(h,/Refresh draft list/);
  assert.match(h,/aria-label="Draft load-check"/);
  assert.match(h,/aria-label="Draft site-visit"/);
  assert.match(h,/load-check: written \(absent → draft\); attribution not observed/);
  const none=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:undefined,attachments,workspace:false,busy:false,act:async()=>{}}));
  assert.match(none,/No explicit App project is configured/);
  assert.match(none,/Open a library to list its drafts/);
  const empty=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:{...data,drafts:[],transitions:[]},attachments,workspace:true,busy:false,act:async()=>{}}));
  assert.match(empty,/No drafts in this library/);
});

test('damaged trial pointers and non-conforming transitions are shown, not hidden',()=>{
  const data={library:'l',observedAt:'t',drafts:[],transitions:[],transitionLimits:['draft x: changed transition not reported: WR draft_transition refused']};
  const h=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data,attachments,workspace:true,pointerLimits:['trial pointer malformed: /a/damaged.json: missing field'],busy:false,act:async()=>{}}));
  assert.match(h,/role="alert" aria-label="Draft workspace limits"/);
  assert.match(h,/trial pointer malformed: \/a\/damaged.json/);
  assert.match(h,/changed transition not reported/);
  const clean=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:{...data,transitionLimits:[]},attachments,workspace:true,pointerLimits:[],busy:false,act:async()=>{}}));
  assert.doesNotMatch(clean,/Draft workspace limits/);
});
