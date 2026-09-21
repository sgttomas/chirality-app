import { describe, expect, it } from 'vitest';
import { describeIpcSender, isAuthorizedSender } from '../../../electron/ipc-sender-policy';

/**
 * DEL-09-06-V3-01: the one sender-authorization policy shared by the
 * runtime-control and credential IPC handlers. Exact-origin equality on the
 * sending frame's URL; everything else fails closed.
 */

const RENDERER_ORIGIN = 'http://127.0.0.1:3000';

describe('electron/ipc-sender-policy', () => {
  it.each([
    ['same origin, root path', 'http://127.0.0.1:3000/'],
    ['same origin, nested path and query', 'http://127.0.0.1:3000/settings?tab=keys'],
    ['same origin, hash', 'http://127.0.0.1:3000/#/chat']
  ])('authorizes %s', (_name, url) => {
    expect(isAuthorizedSender({ senderFrame: { url } }, RENDERER_ORIGIN)).toBe(true);
  });

  it.each([
    ['no sender frame', {}],
    ['null sender frame', { senderFrame: null }],
    ['sender frame without url', { senderFrame: {} }],
    ['empty url', { senderFrame: { url: '' } }],
    ['unparseable url', { senderFrame: { url: 'not a url' } }],
    ['different host', { senderFrame: { url: 'http://localhost:3000/' } }],
    ['different port', { senderFrame: { url: 'http://127.0.0.1:3001/' } }],
    ['different scheme', { senderFrame: { url: 'https://127.0.0.1:3000/' } }],
    ['remote origin', { senderFrame: { url: 'https://attacker.example/' } }],
    ['file url', { senderFrame: { url: 'file:///Users/someone/index.html' } }],
    ['origin embedded in path', { senderFrame: { url: 'https://attacker.example/http://127.0.0.1:3000/' } }],
    ['origin as userinfo', { senderFrame: { url: 'http://127.0.0.1:3000@attacker.example/' } }]
  ])('rejects %s', (_name, event) => {
    expect(isAuthorizedSender(event, RENDERER_ORIGIN)).toBe(false);
  });

  it('never authorizes anything when the renderer origin is empty', () => {
    expect(isAuthorizedSender({ senderFrame: { url: 'http://127.0.0.1:3000/' } }, '')).toBe(false);
  });

  it('describes a sender by origin only, never by full url', () => {
    expect(describeIpcSender({ senderFrame: { url: 'https://attacker.example/steal?key=sk-secret' } }))
      .toBe('https://attacker.example');
    expect(describeIpcSender({})).toBe('no-sender-frame');
    expect(describeIpcSender({ senderFrame: null })).toBe('no-sender-frame');
    expect(describeIpcSender({ senderFrame: { url: 'not a url' } })).toBe('unparseable-sender-url');
  });
});
