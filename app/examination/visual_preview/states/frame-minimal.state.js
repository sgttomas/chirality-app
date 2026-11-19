// The smallest ready snapshot the front-end tests use (tests/first-view.test.mjs, base()). It shows
// the frame only: fields a real host always sends are absent, so it is for layout work, never for a picture.
const generation = { appSession: "s", home: "h", spawnCounter: 1 };
export default {
  title: "Frame only (minimal test snapshot; not a reachable state)",
  host: { state: "ready", generationClosed: false, generation, threads: [], roleLimits: { account: { roles: [] } },
    homeRouting: { activeModeHomeClass: "account", entries: [{ modeHomeClass: "account" }] }, serverRequests: [] },
  commands: { native_confirmation_content: [] },
};
