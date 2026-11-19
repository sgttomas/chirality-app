// The person pressed the popover's sign-in: Codex reports the browser sign-in pending (runtime_session.rs, homeOAuth
// "source-observed" with hosting.rs account_oauth_observation phase "Pending"); the account read still reports no
// account. The account popover, opened by a press replayed after mount, says "Waiting for sign-in to complete."
import { readyHost, accountRead, historyEmpty, GEN } from "./_shared.js";
import { selfIssued, availableModels, pressesAfterMount } from "./_commands.js";

const pending = { state: "source-observed", accountConfirmation: "matched success still requires native account/read; no signed-in identity inferred",
  source: { generation: GEN, requestIdentity: 5, observationRef: "oauth-observation:1", mode: "Browser", phase: "Pending", cancelStatus: null,
    presentationAvailable: false, cancelAvailable: true, actualWriteObserved: true, standing: "source observation; no account/actor/policy authenticity or native adapter qualification" } };

pressesAfterMount("signing-in", [doc => doc.querySelector("nav .account-controls-row")]);
export default {
  title: "Signing in: waiting for the browser sign-in (account popover open)",
  host: readyHost({ ...accountRead(null), homeOAuth: pending, nativeHistory: historyEmpty() }),
  commands: selfIssued({ read_available_models: availableModels }),
};
