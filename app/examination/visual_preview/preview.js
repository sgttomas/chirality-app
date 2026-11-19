// Stand-in for the host: answers the web view's commands from one constructed state, chosen by
// ?state=<name>. Nothing here runs the App, a candidate or Codex. A command with no stand-in
// rejects, as an unavailable host command would, and is named in the console.
import { states } from "./states/index.js";

const name = new URLSearchParams(location.search).get("state") ?? "starting";
const state = states[name];
if (!state) throw new Error(`preview: no state "${name}"; known: ${Object.keys(states).join(", ")}`);
const clone = value => (value === undefined ? undefined : structuredClone(value));
const unanswered = new Set();
let callbacks = 0;

window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener() {} };
window.__TAURI_INTERNALS__ = {
  transformCallback() { return ++callbacks; },
  unregisterCallback() {},
  async invoke(command, args) {
    // The waiting-menu transport with no menu selection pending.
    if (command === "plugin:event|listen") return args.handler;
    if (command === "plugin:event|unlisten") return null;
    if (command === "checkpoint_native_waiting_ui" || command === "claim_native_waiting_intent") return null;
    const answer = state.commands?.[command];
    if (typeof answer === "function") return clone(await answer(args ?? {}, state));
    if (answer !== undefined) return clone(answer);
    if (command === "host_status" && state.host !== undefined) return clone(state.host);
    if (!unanswered.has(command)) { unanswered.add(command); console.warn(`preview: no stand-in for ${command}`, args); }
    throw new Error(`The preview's stand-in host has no answer for ${command}.`);
  },
};
window.__PREVIEW__ = { state: name, states: Object.keys(states), unanswered };
await import("/src/main.tsx");
