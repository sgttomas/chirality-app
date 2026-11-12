import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
const {LiveWorkNotice,conversationStateWords,interruptedTurnNote,interruptedTurnWords}=loadSrc('LiveWorkNotice');

// Invented rows in the host status shape (hosting.rs threads, conversationTurns, serverRequests; interrupted_work.rs).
const G={appSession:'s',home:'h',spawnCounter:1};
const thread=(threadId,extra={})=>({generation:G,threadId,model:'m',...extra});
const applied=status=>({status,statusSource:{method:'thread/status/changed',receiptPosition:9}});
const host=(threads,extra={})=>({state:'ready',generation:G,threads,...extra});
const render=h=>renderToStaticMarkup(React.createElement(LiveWorkNotice,{host:h,showConversation(){},findInHistory(){}}));

test('a conversation reads working, waiting or in error only from what Codex and the host report',()=>{
 const rows=[thread('idle',applied({type:'idle'})),thread('active',applied({type:'active',activeFlags:[]})),thread('asks',applied({type:'active',activeFlags:['waitingOnApproval']})),
  thread('error',applied({type:'systemError'})),thread('admitted',{status:{type:'idle'}}),thread('turn',{status:{type:'idle'}}),thread('request',applied({type:'idle'})),thread('unknown',{...applied(null)})];
 const h=host(rows,{conversationTurns:[{generation:G,threadId:'turn',nativeTurn:{status:'inProgress'}},{generation:G,threadId:'idle',nativeTurn:{status:'inProgress'},terminalEventObserved:false}],
  serverRequests:[{generation:G,state:'outstanding',nativeParameters:{threadId:'request'}}]});
 const words=id=>conversationStateWords(h,rows.find(r=>r.threadId===id));
 assert.equal(words('idle'),'','Codex’s own idle report stands over a turn row the host has not seen end');
 assert.equal(words('active'),'working');assert.equal(words('asks'),'waiting for your answer');assert.equal(words('error'),'Codex reported a system error');
 assert.equal(words('admitted'),'');assert.equal(words('turn'),'working','before any status report, a turn seen starting and not ending');
 assert.equal(words('request'),'waiting for your answer');assert.equal(words('unknown'),'','a status of unknown shape says nothing');
});

test('a stopped or replaced Codex establishes no state',()=>{
 const live=thread('t',applied({type:'active',activeFlags:[]}));
 assert.equal(conversationStateWords(host([live]),live),'working');
 assert.equal(conversationStateWords(host([live],{generationClosed:true}),live),'');
 assert.equal(conversationStateWords(host([live],{state:'exited-unexpectedly'}),live),'');
 assert.equal(conversationStateWords(host([live],{generation:{...G,spawnCounter:2}}),live),'','a row of an earlier generation');
 const ended=thread('t',{status:null,lastObservedStatus:{type:'active',activeFlags:[]},statusObservationEnded:true,statusSource:{method:'thread/status/changed',receiptPosition:9}});
 assert.equal(conversationStateWords(host([ended]),ended),'','the last status seen is not a current reading');
 assert.equal(render(host([ended])),'');assert.equal(render(null),'');assert.equal(render(host([thread('quiet',applied({type:'idle'}))])),'');
});

test('work in progress is named with a way to show it',()=>{
 const html=render(host([thread('a',applied({type:'active',activeFlags:[]})),thread('b',applied({type:'idle'}))]));
 assert.match(html,/<section aria-label="Work in progress and interrupted work" role="status">/);
 assert.match(html,/<li><strong>Conversation 1 · m<\/strong> is working\. <button>Show it<\/button><\/li>/);
 assert.equal(html.match(/<li>/g).length,1);
});

const left=(threadId,priorSessionEnd,turn)=>({threadId,home:'H-acct',priorSession:'app-session:earlier',priorSessionEnd,turns:[{turnId:'u',...turn}]});
test('after a relaunch the notice says what was in progress and only what Codex’s history said of it',()=>{
 const h=host([thread('open')],{interruptedWork:{conversations:[left('gone','ended-without-record',{reading:'read',codexStatus:'interrupted'}),left('open','quit-with-live-work',{reading:'not-read-yet'})]}});
 const html=render(h);
 assert.match(html,/When the App last ran, a conversation \(<code>gone<\/code>\) had a turn in progress; the App ended without a normal quit\. <span>Codex&#x27;s history now reports that turn as interrupted\. <\/span>Nothing was resumed or resent\. <button>Find it in History to continue it<\/button>/);
 assert.match(html,/When the App last ran, <strong>Conversation 1 · m<\/strong> had a turn in progress; you quit the App while it was in progress\. <span>The App has not read it back from Codex yet\. <\/span>Nothing was resumed or resent\. <button>Show it<\/button>/);
 assert.doesNotMatch(html,/is working/);
});

test('an outcome that was not read is said as unknown, never as an ending',()=>{
 assert.equal(interruptedTurnWords({reading:'read',codexStatus:'completed'}),'Codex\'s history now reports that turn as completed.');
 assert.equal(interruptedTurnWords({reading:'read',codexStatus:'inProgress'}),'Codex\'s history still lists that turn as in progress; whether it finished is unknown.');
 assert.equal(interruptedTurnWords({reading:'not-in-history'}),'That turn is not in Codex\'s history; what became of it is unknown.');
 assert.equal(interruptedTurnWords({reading:'unavailable',reason:'Codex did not answer'}),'The App could not read it back from Codex (Codex did not answer); what became of it is unknown.');
 for(const turn of [{reading:'not-established'},{reading:'read'},{reading:'read',codexStatus:7},{},null]) assert.equal(interruptedTurnWords(turn),'What became of it is not established.');
 const h=host([],{interruptedWork:{conversations:[left('t','system-terminated',{reading:'read',codexStatus:'failed'})]}});
 assert.equal(interruptedTurnNote(h,'t','u'),'This turn was in progress when the App last ran; the system ended the App. Codex\'s history now reports that turn as failed. Nothing was resumed or resent.');
 assert.equal(interruptedTurnNote(h,'t','other'),null);assert.equal(interruptedTurnNote(h,'other','u'),null);assert.equal(interruptedTurnNote(host([]),'t','u'),null);
});
