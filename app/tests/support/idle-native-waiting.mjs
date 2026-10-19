import assert from 'node:assert/strict';

// The actual App always mounts its native waiting reader. Existing action
// fixtures have no pending menu selection: model only that exact read-only
// transport, keeping their original action dispatcher and assertions intact.
export function installIdleNativeWaiting(invoke) {
  const previous = window.__TAURI_INTERNALS__;
  const previousEvents = window.__TAURI_EVENT_PLUGIN_INTERNALS__;
  const callbacks = new Map(), listeners = new Map(), detached = new Set();
  const calls = [], checkpoints = new Map();
  let next = 0;
  window.__TAURI_EVENT_PLUGIN_INTERNALS__ = {
    unregisterListener(event, eventId) {
      assert.equal(event, 'chirality-native-waiting');
      assert.ok(listeners.has(eventId), 'unregister only an installed waiting listener');
      assert.ok(!detached.has(eventId), 'waiting listener unregisters once');
      detached.add(eventId);
      callbacks.delete(eventId);
    },
  };
  window.__TAURI_INTERNALS__ = {
    transformCallback(handler, once = false) {
      assert.equal(typeof handler, 'function');
      assert.equal(once, false, 'waiting subscription is not a one-shot callback');
      const id = ++next;
      callbacks.set(id, handler);
      return id;
    },
    async invoke(command, args) {
      if (command === 'plugin:event|listen') {
        assert.deepEqual(Object.keys(args).sort(), ['event', 'handler', 'target']);
        assert.equal(args.event, 'chirality-native-waiting');
        assert.deepEqual(args.target, {kind: 'AnyLabel', label: 'main'});
        assert.ok(callbacks.has(args.handler), 'listen uses its registered callback');
        assert.ok(!listeners.has(args.handler), 'callback is installed once');
        calls.push({command, args});
        listeners.set(args.handler, args.event);
        return args.handler;
      }
      if (command === 'checkpoint_native_waiting_ui') {
        assert.deepEqual(Object.keys(args).sort(), ['consumer', 'revision']);
        assert.equal(typeof args.consumer, 'string');
        assert.ok(args.consumer.length > 0);
        assert.ok(Number.isSafeInteger(args.revision) && args.revision >= 0);
        assert.ok(!checkpoints.has(args.consumer) || checkpoints.get(args.consumer) <= args.revision,
          'UI checkpoint publication cannot move backwards');
        checkpoints.set(args.consumer, args.revision);
        calls.push({command, args});
        return null; // Acknowledge UI metadata only; no menu intent exists.
      }
      if (command === 'claim_native_waiting_intent') {
        assert.deepEqual(Object.keys(args), ['consumer']);
        assert.equal(typeof args.consumer, 'string');
        assert.ok(args.consumer.length > 0);
        assert.ok(checkpoints.has(args.consumer), 'claim follows an acknowledged UI checkpoint');
        calls.push({command, args});
        return null; // No native menu intent; never manufacture navigation.
      }
      if (command === 'plugin:event|unlisten') {
        assert.deepEqual(Object.keys(args).sort(), ['event', 'eventId']);
        assert.equal(args.event, listeners.get(args.eventId));
        assert.ok(detached.delete(args.eventId), 'Tauri unregisters the callback before unlisten');
        listeners.delete(args.eventId);
        calls.push({command, args});
        return null;
      }
      // In particular, finish/open/send/resume/answer are not idle transport.
      // Every other command goes through the fixture's original strict peer.
      return invoke(command, args);
    },
  };
  return {
    calls,
    assertClean(container) {
      assert.doesNotMatch(container.textContent, /Waiting menu listener unavailable|Waiting menu UI checkpoint unavailable|Waiting-request navigation unavailable/,
        'idle waiting transport must not pollute the App status with unexpected-command errors');
    },
    restore(renderedText) {
      try {
        assert.doesNotMatch(renderedText, /Waiting menu listener unavailable|Waiting menu UI checkpoint unavailable|Waiting-request navigation unavailable/,
          "idle transport leaves no unexpected-command error in the App status");
        assert.equal(listeners.size, 0, 'App unmount removes every waiting listener');
        assert.equal(callbacks.size, 0, 'App unmount unregisters every waiting callback');
        assert.equal(detached.size, 0, 'App unmount completes every unlisten');
      } finally {
        window.__TAURI_INTERNALS__ = previous;
        window.__TAURI_EVENT_PLUGIN_INTERNALS__ = previousEvents;
      }
    },
  };
}
