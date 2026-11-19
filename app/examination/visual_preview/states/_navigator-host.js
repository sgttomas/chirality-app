// A signed-in, ready host for the navigator's own states, with the requests a state names waiting on the person
// (a question the agent asks, item/tool/requestUserInput; an approval, item/commandExecution/requestApproval) in the
// register "Waiting on you" reads. Not a state.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, waitingOverview, threadRow, GEN, PROJECT } from "./_shared.js";

export const question = (identity, threadId) => ({ recordKind: "server-request-entry", requestIdentity: identity, generation: GEN, method: "item/tool/requestUserInput", classification: "known-answerable",
  originClass: "person-input", nativeParameters: { threadId, turnId: "019b2f60-0000-7000-8000-000000000001", itemId: `item-question-${identity}`, isBlocking: true,
    questions: [{ id: "datum", header: "Datum", question: "Which vertical datum should the soundings be reduced to?", isOther: true, isSecret: false,
      options: [{ label: "Chart datum", description: "As the harbour charts use" }, { label: "Mean sea level", description: "As the tide gauge reports" }] }] },
  receiptPosition: 60 + identity, state: "outstanding", replyWriteResult: "not-attempted", acknowledgmentObservation: { status: "not-observed" } });
export const approval = (identity, threadId) => ({ recordKind: "server-request-entry", requestIdentity: identity, generation: GEN, method: "item/commandExecution/requestApproval", classification: "known-answerable",
  originClass: "a14", nativeParameters: { threadId, turnId: "019b2f60-0000-7000-8000-000000000002", itemId: `item-command-${identity}`, command: "curl -O https://example.com/soundings.csv", cwd: PROJECT },
  receiptPosition: 60 + identity, state: "outstanding", replyWriteResult: "not-attempted", acknowledgmentObservation: { status: "not-observed" } });
/** A conversation loaded in this running App, under its own thread id. */
export const loadedRow = (threadId, name, status = { type: "idle" }) => ({ ...threadRow({ status, name }), threadId });

export function navigatorHost({ requests = [], threads = [], over = {} } = {}) {
  return readyHost({ ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted, threads, serverRequests: requests, waitingRequests: waitingOverview(requests), ...over });
}
