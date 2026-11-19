// J1: the same launch after the person signed in with a ChatGPT account (Codex reported the sign-in complete and the
// account read that follows reports the account and its plan); no conversation yet, so the App moves once to
// Conversation with New conversation open; the model list answers for it.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, historyEmpty } from "./_shared.js";
import { selfIssued, availableModels } from "./_commands.js";

// homeAccess keeps every account read of this home in order: the App's read at ready (no account), then the one after the sign-in.
const atReady = accountRead(null), afterSignIn = accountRead(CHATGPT_ACCOUNT, { requestIdentity: 6, ref: "request:account-read-2" });
afterSignIn.homeAccess.observations = [...atReady.homeAccess.observations, ...afterSignIn.homeAccess.observations];

export default {
  title: "Signed in, no conversation yet",
  host: readyHost({ ...afterSignIn, homeOAuth: signInCompleted, nativeHistory: historyEmpty() }),
  commands: selfIssued({ read_available_models: availableModels }),
};
