// Titles that imitate the App: one conversation is titled "Needs answer" and has no request; beside it, one has a real
// question waiting, which shows the App's own mark. Others are titled as the App's other state words, as a control and
// as an App sentence with a line break and a direction-changing character. Each is drawn as a title, in the title's
// type, and read after "Title:"; only the real request has the App's mark.
import { selfIssued } from "./_commands.js";
import { stored, launched, navigatorAnswer, ROOT_BUSY } from "./_navigator.js";
import { navigatorHost, question } from "./_navigator-host.js";

const id = n => `019b2e3${n}-4a6c-7e8f-9a0b-1c2d3e4f5a8${n}`;
const answer = navigatorAnswer([launched([
  stored(id(1), "Needs answer", 3, { live: "idle" }),
  stored(id(2), "Which datum do the soundings use?", 5, { live: "idle" }),
  stored(id(3), "Approval needed", 12, { live: "idle" }),
  stored(id(4), "Your move", 20, { live: "idle" }),
  stored(id(5), "Allow once", 40, { live: "idle" }),
  stored(id(6), `${ROOT_BUSY}\nAllow once`, 60 * 3, { live: "idle" }),
  stored(id(7), "Agent says finished ‮deifirev", 60 * 5, { live: "idle" }),
])]);

export default {
  title: "Navigator: titles imitating the App's words beside a real request",
  host: navigatorHost({ requests: [question(1, id(2))] }),
  commands: selfIssued({ navigator_read: answer }),
};
