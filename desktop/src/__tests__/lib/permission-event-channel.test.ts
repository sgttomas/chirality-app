import { afterEach, describe, expect, it } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import {
  PermissionEventChannelRegistry,
  SessionPermissionChannel,
  getPermissionEventChannel,
  resetPermissionEventChannelForTests
} from '../../lib/harness/permission-event-channel';

afterEach(() => {
  resetPermissionEventChannelForTests();
});

function evt(id: string): HarnessEvent {
  return {
    schemaVersion: 1,
    eventId: id,
    sessionId: 's1',
    timestamp: '2026-06-18T00:00:00.000Z',
    type: 'tool.permission',
    data: { behavior: 'ask', toolUseId: id }
  };
}

describe('SessionPermissionChannel', () => {
  it('delivers a published event to a waiter that is already parked', async () => {
    const channel = new SessionPermissionChannel();
    const pending = channel.next();
    channel.publish(evt('a'));
    await expect(pending).resolves.toEqual({ value: evt('a'), done: false });
  });

  it('buffers events published before they are consumed, preserving order', async () => {
    const channel = new SessionPermissionChannel();
    channel.publish(evt('a'));
    channel.publish(evt('b'));
    await expect(channel.next()).resolves.toMatchObject({ value: { eventId: 'a' }, done: false });
    expect(channel.drain().map((event) => event.eventId)).toEqual(['b']);
  });

  it('resolves a parked next() as done on close and ignores later publishes', async () => {
    const channel = new SessionPermissionChannel();
    const pending = channel.next();
    channel.close();
    await expect(pending).resolves.toEqual({ value: undefined, done: true });
    channel.publish(evt('a'));
    await expect(channel.next()).resolves.toEqual({ value: undefined, done: true });
  });
});

describe('PermissionEventChannelRegistry', () => {
  it('routes publishes only to the open session channel', async () => {
    const registry = new PermissionEventChannelRegistry();
    const channel = registry.open('s1');
    const pending = channel.next();

    registry.publish('other', evt('x')); // no channel — dropped
    registry.publish('s1', evt('a'));

    await expect(pending).resolves.toMatchObject({ value: { eventId: 'a' }, done: false });

    registry.close('s1');
    await expect(channel.next()).resolves.toEqual({ value: undefined, done: true });
  });

  it('closes a pre-existing same-session channel when re-opened, releasing its waiter', async () => {
    const registry = new PermissionEventChannelRegistry();
    const first = registry.open('s1');
    const firstParked = first.next();

    // Re-opening the same session must close the stale channel (DESIGN §5.3 item c)...
    const second = registry.open('s1');
    await expect(firstParked).resolves.toEqual({ value: undefined, done: true });

    // ...and publishes now route only to the live channel, not the closed one.
    const secondParked = second.next();
    registry.publish('s1', evt('a'));
    await expect(secondParked).resolves.toMatchObject({ value: { eventId: 'a' }, done: false });
  });

  it('close(sessionId, channel) does not evict a newer channel that replaced it', async () => {
    const registry = new PermissionEventChannelRegistry();
    const stale = registry.open('s1');
    const fresh = registry.open('s1'); // replaces stale; stale is now closed
    const freshParked = fresh.next();

    // A stale turn's teardown passes its own (already-closed) instance: it must NOT
    // close+delete the newer registered channel (DESIGN §5.3 identity guard).
    registry.close('s1', stale);

    registry.publish('s1', evt('a'));
    await expect(freshParked).resolves.toMatchObject({ value: { eventId: 'a' }, done: false });
  });

  it('close(sessionId, channel) evicts when the instance still owns the slot', async () => {
    const registry = new PermissionEventChannelRegistry();
    const channel = registry.open('s1');
    const parked = channel.next();

    registry.close('s1', channel);
    await expect(parked).resolves.toEqual({ value: undefined, done: true });
    // Slot is freed: a later open starts fresh.
    expect(registry.open('s1')).not.toBe(channel);
  });

  it('exposes a resettable process-wide singleton', () => {
    const first = getPermissionEventChannel();
    expect(getPermissionEventChannel()).toBe(first);
    resetPermissionEventChannelForTests();
    expect(getPermissionEventChannel()).not.toBe(first);
  });
});
