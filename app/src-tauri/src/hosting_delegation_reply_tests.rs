// NPTD §7.1 delegation reads whose reply arrives after the reading stopped
// waiting: the reply's result body is kept nowhere (journal, request evidence,
// reply channel), whatever ended the wait. The pipe peer is `/bin/cat` (or a
// closed pipe for a failed write); replies are injected.
use super::*;
use std::process::{Child, Command, Stdio};

const BODY: &str = "delegation-private-catalogue-body";

fn g() -> Value { json!({"appSession":"delegation-session","home":"delegation-home","spawnCounter":1}) }
fn host() -> Arc<Host> {
    let host = Arc::new(Host::new());
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = g();
        i.threads.push(json!({"generation":g(),"threadId":"thread","model":"selected","modelProvider":"selected-provider"}));
    }
    host
}
/// A pipe whose reader accepts every write.
fn open_pipe(host: &Host) -> Child {
    let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();
    *host.stdin.lock().unwrap() = child.stdin.take();
    child
}
fn close_pipe(host: &Host, mut child: Child) {
    *host.stdin.lock().unwrap() = None;
    assert!(child.wait().unwrap().success());
}
fn model_list_id(host: &Host) -> Value {
    let i = host.inner.0.lock().unwrap();
    i.source_requests.values().find(|e| e.request.frame["method"] == "model/list").map(|e| e.request.request_id().clone()).expect("model/list was registered")
}
fn source(host: &Host, id: &Value) -> SourceRequest { host.inner.0.lock().unwrap().source_requests[&id.to_string()].request.clone() }
fn late_reply(host: &Host, id: &Value) {
    host.on_line(&serde_json::to_vec(&json!({"jsonrpc":"2.0","id":id,"result":{"data":[{"model":"selected","description":BODY}]}})).unwrap(), &g());
}
fn assert_no_body(host: &Host) {
    let journal = serde_json::to_string(&host.journal()).unwrap();
    assert!(!journal.contains(BODY), "journal keeps the result body: {journal}");
    assert!(journal.contains("resultWithheld"), "the reply is journalled as its outcome: {journal}");
    let (_, kept) = host.kept_replies();
    assert!(!kept.contains(BODY), "request evidence keeps the result body: {kept}");
}
/// The reading stops at model/list's wait limit; nothing further is sent.
fn read_until_silent(host: &Host) {
    let signals = host.delegation_signals_read_within(&g(), "thread", json!({"kind":"person-directed"}), Duration::from_millis(40));
    assert!(signals["limits"].to_string().contains("no response to"), "{signals}");
}

#[test]
fn a_reply_after_the_wait_timed_out_keeps_no_body_in_journal_evidence_or_channel() {
    let host = host();
    let child = open_pipe(&host);
    read_until_silent(&host);
    let id = model_list_id(&host);
    let request = source(&host, &id);
    assert_eq!(request.evidence()["waitingEnded"], true);
    late_reply(&host, &id);
    assert_no_body(&host);
    // The reply channel the request holds has the reduced form only.
    let queued = request.receiver.lock().unwrap().try_recv().expect("the late reply reached the channel");
    assert!(!queued.to_string().contains(BODY), "channel keeps the result body: {queued}");
    assert_eq!(queued["outcome"], "result");
    // The evidence says the reply is reduced, and reads its outcome honestly.
    let evidence = request.evidence();
    assert_eq!(evidence["responseReduced"], true);
    assert!(evidence["frameEvidence"].as_str().unwrap().contains("reduced to its outcome"), "{evidence}");
    assert_eq!(evidence["outcome"], "response-observed-result");
    close_pipe(&host, child);
}

#[test]
fn a_reply_after_the_generation_closed_keeps_no_body() {
    let host = host();
    let child = open_pipe(&host);
    read_until_silent(&host);
    let id = model_list_id(&host);
    { let mut i = host.inner.0.lock().unwrap(); Host::close_generation(&mut i); }
    late_reply(&host, &id);
    assert_eq!(host.journal().last().unwrap()["class"], "closed-generation-frame");
    assert_no_body(&host);
    close_pipe(&host, child);
}

#[test]
fn a_failed_write_ends_the_wait_and_a_later_reply_keeps_no_body() {
    let host = host();
    // A pipe whose reader has gone: every write fails.
    let mut gone = Command::new("/usr/bin/true").env_clear().stdin(Stdio::piped()).stdout(Stdio::null()).stderr(Stdio::null()).spawn().unwrap();
    let stdin = gone.stdin.take();
    assert!(gone.wait().unwrap().success());
    *host.stdin.lock().unwrap() = stdin;
    let signals = host.delegation_signals_read_within(&g(), "thread", json!({"kind":"person-directed"}), Duration::from_secs(2));
    assert!(signals["limits"].to_string().contains("write failed"), "{signals}");
    let id = model_list_id(&host);
    let request = source(&host, &id);
    assert_eq!(request.evidence()["writeResult"], "write-failed");
    assert_eq!(request.evidence()["waitingEnded"], true, "any failure ends the wait");
    late_reply(&host, &id);
    assert_eq!(host.journal().last().unwrap()["class"], "uncorrelated-response");
    assert_no_body(&host);
    *host.stdin.lock().unwrap() = None;
}

#[test]
fn a_reduced_reply_keeps_only_what_codex_sent_and_reads_its_outcome() {
    let result = delegation_withheld(&json!({"id":7,"result":{"description":BODY}}));
    assert!(result.get("error").is_none(), "no error where Codex sent none: {result}");
    assert!(!result.to_string().contains(BODY));
    assert_eq!(observed_response_outcome(&result), "response-observed-result");
    let error = delegation_withheld(&json!({"id":7,"error":{"code":-32600,"message":"refused"}}));
    assert_eq!(error["error"]["code"], -32600);
    assert_eq!(observed_response_outcome(&error), "response-observed-error");
    // An ordinary reply is read as received.
    assert_eq!(observed_response_outcome(&json!({"id":7,"result":{}})), "response-observed-result");
    assert_eq!(observed_response_outcome(&json!({"id":7,"error":{}})), "response-observed-error");
}
