// The busy rule's sentence: every reading has found Chirality working on the open project's runs (the workflow root
// was held by a reading of its records), so after three readings in a row the panel says so, whole, and shows no run
// line as current. The conversations are this answer's.
import { selfIssued } from "./_commands.js";
import { stored, launched, navigatorAnswer, ROOT_BUSY } from "./_navigator.js";
import { navigatorHost } from "./_navigator-host.js";

const id = n => `019b2e1${n}-4a6c-7e8f-9a0b-1c2d3e4f5a6${n}`;
const busy = { state: "not-read", reason: ROOT_BUSY, readAt: null, limits: [] };
const answer = navigatorAnswer([launched([stored(id(1), "Define the summary report", 2), stored(id(2), "Soundings check, north basin", 25), stored(id(4), "Tide gauge notes", 60 * 30)], { runsRead: busy })]);

export default {
  title: "Navigator: Chirality working on the open project's runs for three readings in a row",
  host: navigatorHost(),
  commands: selfIssued({ navigator_read: answer }),
};
