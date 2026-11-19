// The signed-out relaunch (signed-out.state.js) with the account popover opened by a press replayed after mount: the
// state, the workspace line's sentence and its one action, the sign-in (AccountControls.tsx).
import signedOut from "./signed-out.state.js";
import { pressesAfterMount } from "./_commands.js";

pressesAfterMount("signed-out-account", [doc => doc.querySelector("nav .account-controls-row")]);
export default { ...signedOut, title: "Relaunch, not signed in (account popover open)" };
