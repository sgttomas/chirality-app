import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {ObserverAttachment} = loadSrc('ObserverAttachment');
const g = {appSession:'synthetic-session', home:'account-home', spawnCounter:1};
const other = {...g, home:'key-home'};
const snapshot = (generation, high, floor, extra = {}) => ({state:'ready', generation, generationClosed:false,
  observerRetention:{generation,deliveredThrough:high,omittedThrough:floor},...extra});
const reply = (generation, position, gap = true) => ({generation,position,gap});
function mounted(observe) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  return {container, show:host => React.act(async () => {root.render(React.createElement(ObserverAttachment,{host,observe}));}),
    close:() => React.act(() => root.unmount())};
}

test('a window attaches without a cursor, advances from received status and repairs an expired cursor once', async () => {
  const calls = [];
  const observe = async (...args) => {calls.push(args);return reply(g,calls.length === 1 ? 10 : 20);};
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,10,0));
    assert.deepEqual(calls,[[g,null,0]],'current source is independent from the absent cursor');
    assert.match(view.container.textContent,/Earlier events are outside/);
    await view.show(snapshot(g,12,0));
    await view.show(snapshot(g,12,0));
    assert.equal(calls.length,1,'ordinary received status advances coverage without another full-snapshot RPC');
    await view.show(snapshot(g,20,13));
    assert.deepEqual(calls,[[g,null,0],[g,g,12]],'expired cursor is repaired in its actual source');
    await view.show(snapshot(g,21,13));
    assert.equal(calls.length,2);
  } finally {await view.close();}
});

test('late replies from a different home cannot replace the selected source; revisiting can attach again', async () => {
  let complete;
  const calls = [];
  const observe = async (...args) => {
    calls.push(args);
    if (calls.length === 1) return new Promise(resolve => {complete = resolve;});
    return reply(args[0],4,false);
  };
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,4,0));
    await view.show(snapshot(other,4,0));
    assert.match(view.container.textContent,/Window replay is current/);
    await React.act(async () => {complete(reply(g,4,true));});
    assert.match(view.container.textContent,/Window replay is current/);
    assert.doesNotMatch(view.container.textContent,/Earlier events are outside/);
    await view.show(snapshot(g,4,0));
    assert.equal(calls.length,3,'an ignored old reply does not leave a permanent pending/attempt fence');
    assert.deepEqual(calls.map(call => call[0]),[g,other,g]);
  } finally {await view.close();}
});

test('non-ready sources and unsafe positions do not trigger reads; each new generation has its own cursor', async () => {
  const calls = [];
  const observe = async (...args) => {calls.push(args);return reply(args[0],3);};
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,3,0,{state:'handshaking'}));
    await view.show(snapshot(g,3,0,{state:'stopping'}));
    await view.show(snapshot(g,Number.MAX_SAFE_INTEGER + 1,0));
    assert.equal(calls.length,0);
    assert.match(view.container.textContent,/coverage is unavailable/);
    await view.show(snapshot(g,3,0));
    const successor = {...g,spawnCounter:2};
    await view.show(snapshot(successor,3,0));
    assert.deepEqual(calls,[[g,null,0],[successor,null,0]],'previous generation never supplies a current cursor');
  } finally {await view.close();}
});

test('late rejected attachment from a different home does not block revisiting its source', async () => {
  let reject;
  const calls = [];
  const observe = async (...args) => {
    calls.push(args);
    if (calls.length === 1) return new Promise((_, fail) => {reject = fail;});
    return reply(args[0],4,false);
  };
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,4,0));
    await view.show(snapshot(other,4,0));
    await React.act(async () => {reject(new Error('synthetic old source read failed'));});
    assert.match(view.container.textContent,/Window replay is current/);
    await view.show(snapshot(g,4,0));
    assert.deepEqual(calls.map(call => call[0]),[g,other,g],'late refusal retires only the obsolete attempt, allowing reattachment');
    assert.match(view.container.textContent,/Window replay is current/);
  } finally {await view.close();}
});

test('a trusted same-source attachment ahead of the last status waits for status without a duplicate snapshot', async () => {
  const calls = [];
  const view = mounted(async (...args) => {calls.push(args);return reply(g,calls.length === 1 ? 12 : 15,false);});
  try {
    await view.show(snapshot(g,10,0));
    assert.equal(calls.length,1,'a newer actual attachment cut is not a future cursor supplied by a caller');
    await view.show(snapshot(g,11,0));
    await view.show(snapshot(g,12,0));
    assert.equal(calls.length,1,'older status must neither roll back the trusted cursor nor trigger another full snapshot');
    await view.show(snapshot(g,15,13));
    assert.deepEqual(calls.map(call => call[2]),[0,12],'genuinely expired coverage still repairs');
  } finally {await view.close();}
});

test('coverage that expires while attachment is pending is checked again after that reply', async () => {
  let complete;
  const calls = [];
  const observe = async (...args) => {
    calls.push(args);
    if (calls.length === 1) return new Promise(resolve => {complete = resolve;});
    return reply(g,10);
  };
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,3,0));
    await view.show(snapshot(g,10,5));
    assert.equal(calls.length,1,'one pending attachment per source');
    await React.act(async () => {complete(reply(g,3));});
    assert.deepEqual(calls,[[g,null,0],[g,g,3]],'an old reply cannot establish coverage past the newer omission floor');
    await view.show(snapshot(g,11,5));
    assert.equal(calls.length,2);
  } finally {await view.close();}
});

test('partial history displays actual coverage and failures without claiming current activity or complete reconstruction', async () => {
  const observe = async () => reply(g,3);
  const view = mounted(observe);
  try {
    await view.show(snapshot(g,3,1,{observerRebuild:{generation:g,status:'partial',targets:[
      {threadId:'known-thread',status:'partial',readAt:'synthetic time',metadata:{thread:{id:'known-thread',preview:'Recorded preview'}},turns:{data:[{id:'earlier-turn',status:'completed'}],nextCursor:null}},
      {threadId:'unread-thread',status:'unavailable',limit:'supplier-history-error'}]}}));
    const text = view.container.textContent;
    assert.match(text,/earlier-turn · completed · recovered from Codex/);
    assert.match(text,/partial history/);
    assert.match(text,/Item history remains unloaded/);
    assert.match(text,/does not establish current activity/);
    assert.match(text,/Codex could not read this conversation’s history/);
    assert.doesNotMatch(text,/supplier-history-error/,'the product explains the read limit in ordinary language');
    assert.equal(view.container.querySelectorAll(element => element.localName === 'button').length,0,'recovered rows grant no controls');
    await view.show(snapshot(other,3,0,{observerRebuild:{generation:g,status:'partial',targets:[{threadId:'old-source',status:'partial'}]}}));
    assert.doesNotMatch(view.container.textContent,/old-source/,'another source cannot fill the selected history panel');
  } finally {await view.close();}
});

test('an unavailable attachment is not retried by ordinary same-cut polling', async () => {
  let calls = 0;
  const view = mounted(async () => {calls++;return {sourceUnavailable:true,generation:g};});
  try {
    await view.show(snapshot(g,3,0));
    await view.show(snapshot(g,4,0));
    assert.equal(calls,1);
    assert.match(view.container.textContent,/attachment was unavailable/);
  } finally {await view.close();}
});
