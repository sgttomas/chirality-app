// Codex is ready, and the App's own account read at ready came back as an error: Codex didn't say whether anyone is
// signed in (AccountStatus.tsx accountReading "failed", one of DIDNT_SAY). The row says "Sign-in unknown"; the account
// popover, opened here by a press replayed after mount, offers Check again and shows Codex's own message, marked.
import { readyHost, accountRead, historyEmpty, GEN } from "./_shared.js";
import { selfIssued, availableModels, pressesAfterMount } from "./_commands.js";

const read = accountRead(null);
const row = read.homeAccess.observations[0];
// hosting.rs SourceRequest::evidence for an account/read Codex answered with a well-formed JSON-RPC error: outcome
// "response-observed-error" (completed_client_response, which keeps the error's code and message in the client
// record; access_provider_tests.rs "native-error"), the shape valid (on_line's auth_shape for an error with a code and
// a message), and auth_rpc.rs typed_observation's error reading. The message is invented for this preview.
const error = { code: -32603, message: "Internal error (invented for this preview)" };
row.source = { ...row.source, outcome: "response-observed-error", authResponseShapeValid: true, response: { id: row.source.requestIdentity, error },
  lastClientObservation: { ...row.source.lastClientObservation, outcome: "response-observed-error", error } };
row.accountObservation = { state: "native error observed; diagnostic redacted", code: error.code, credentialValidity: "unknown", identityVerified: false };

pressesAfterMount("account-unknown", [doc => doc.querySelector("nav .account-controls-row")]);
export default {
  title: "Codex didn't say whether you're signed in (account popover open)",
  host: readyHost({ homeAccess: read.homeAccess, accountObservation: null, nativeHistory: historyEmpty(), generation: GEN }),
  commands: selfIssued({ read_available_models: availableModels }),
};
