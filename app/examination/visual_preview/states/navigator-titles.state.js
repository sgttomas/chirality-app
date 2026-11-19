// Titles: two conversations Codex supplies no title for ("Untitled chat" with each one's time), two with the same
// title at different minutes (their times shown to the minute), two with the same title in the same minute (told
// apart by entry number in their accessible descriptions), a title longer than the panel (shortened with an
// ellipsis) and one whose name holds a line break (shown as a mark).
import { selfIssued } from "./_commands.js";
import { stored, launched, navigatorAnswer } from "./_navigator.js";
import { navigatorHost } from "./_navigator-host.js";

const id = n => `019b2e2${n}-4a6c-7e8f-9a0b-1c2d3e4f5a7${n}`;
const answer = navigatorAnswer([launched([
  stored(id(1), null, 4, { titleSource: "none" }),
  stored(id(2), "Pump sizing", 30),
  stored(id(3), "Pump sizing", 31),
  stored(id(4), "Valve list", 60 * 6),
  stored(id(5), "Valve list", 60 * 6),
  stored(id(6), "A summary of every sounding taken in the north basin since the survey began", 60 * 30),
  stored(id(7), "Section 1\nSection 2", 60 * 40),
  stored(id(8), null, 60 * 24 * 9, { titleSource: "none" }),
])]);

export default {
  title: "Navigator: untitled conversations and equal titles",
  host: navigatorHost(),
  commands: selfIssued({ navigator_read: answer }),
};
