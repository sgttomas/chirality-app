use super::*;
use std::collections::VecDeque;
use std::io::{BufRead, BufReader};
use std::sync::mpsc::{channel, Receiver, Sender};

enum Reply {
    Frame(Value),
    Uncorrelated(Value),
    Silent,
    Held(Value, Sender<()>, Receiver<()>),
}
struct Peer {
    host: Arc<Host>,
    wire: Arc<Mutex<Vec<Value>>>,
    replies: Arc<Mutex<VecDeque<Reply>>>,
    child: std::process::Child,
    worker: Option<std::thread::JoinHandle<()>>,
}
fn generation() -> Value {
    json!({"appSession":"continuation-test","home":"continuation-home","spawnCounter":1})
}
fn thread() -> Value {
    json!({"id":"stored","cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/invented","ephemeral":false,"modelProvider":"fixture","preview":"stored work","projectId":null,"sessionId":"fixture-session","source":"appServer","status":{"type":"idle"},"turns":[]})
}
fn resume() -> Value {
    json!({"thread":thread(),"model":"fixture","modelProvider":"fixture","cwd":"/invented","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":[]})
}
fn turns(ids: &[&str], next: Value) -> Value {
    json!({"data":ids.iter().map(|id|json!({"id":id,"status":"completed","items":[],"itemsView":"summary","error":null})).collect::<Vec<_>>(),"nextCursor":next,"backwardsCursor":"turn-back"})
}
fn items(turn: &str, next: Value) -> Value {
    json!({"data":[
    {"turnId":turn,"item":{"id":"message","type":"agentMessage","text":"Prior readable message"}},
    {"turnId":turn,"item":{"id":"plan","type":"plan","text":"Prior native plan"}},
    {"turnId":turn,"item":{"id":"command","type":"commandExecution","command":"inspect sample","cwd":"/invented","source":"agent","status":"completed","exitCode":0,"aggregatedOutput":"Prior substantive output","commandActions":[]}}
],"nextCursor":next,"backwardsCursor":"item-back","nativeExtra":"unchanged"})
}
impl Peer {
    fn new(extra: Vec<Reply>) -> Self {
        let host = Arc::new(Host::new());
        {
            let mut i = host.inner.0.lock().unwrap();
            i.state = "ready".into();
            i.generation = generation();
            i.journal.begin_generation(generation());
        }
        let mut child = Command::new("/bin/cat")
            .env_clear()
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let wire = Arc::new(Mutex::new(Vec::new()));
        let replies = Arc::new(Mutex::new(VecDeque::from([
            Reply::Frame(json!({"result":{"data":[thread()],"nextCursor":null}})),
            Reply::Frame(json!({"result":resume()})),
        ])));
        replies.lock().unwrap().extend(extra);
        let (h, w, r) = (Arc::clone(&host), Arc::clone(&wire), Arc::clone(&replies));
        let worker = std::thread::spawn(move || {
            for line in BufReader::new(stdout).lines() {
                let Ok(line) = line else { break };
                let frame: Value = serde_json::from_str(&line).unwrap();
                w.lock().unwrap().push(frame.clone());
                let reply = r.lock().unwrap().pop_front().unwrap_or(Reply::Silent);
                let (response, correlated) = match reply {
                    Reply::Silent => (None, true),
                    Reply::Frame(v) => (Some(v), true),
                    Reply::Uncorrelated(v) => (Some(v), false),
                    Reply::Held(v, started, release) => {
                        let _ = started.send(());
                        let _ = release.recv();
                        (Some(v), true)
                    }
                };
                if let Some(mut response) = response {
                    if correlated {
                        response["id"] = frame["id"].clone();
                    }
                    h.on_line(&serde_json::to_vec(&response).unwrap(), &generation());
                }
            }
        });
        Self {
            host,
            wire,
            replies,
            child,
            worker: Some(worker),
        }
    }
    fn receive(&self, history: &mut NativeHistory, query: &HistoryQuery) -> HistoryDispatch {
        let dispatch = self.host.history_dispatch(query).unwrap();
        let e = self
            .host
            .history_wait(&dispatch, Duration::from_secs(2))
            .unwrap();
        history
            .receive(
                query,
                "continuation-home",
                &generation(),
                &e["response"]["result"],
            )
            .unwrap();
        dispatch
    }
    fn admit(&self) -> (NativeHistory, String) {
        let mut history = NativeHistory::new("continuation-home", generation()).unwrap();
        let list = history.list_threads(None, Direction::Desc).unwrap();
        self.receive(&mut history, &list);
        history.select("stored").unwrap();
        let query = history.continue_query().unwrap();
        let dispatch = self.receive(&mut history, &query);
        assert_eq!(
            query.params(),
            &json!({"threadId":"stored","excludeTurns":true})
        );
        let admission = self.host.history_admit_resume(&history, &dispatch).unwrap();
        (
            history,
            admission["resumeRequestRef"].as_str().unwrap().into(),
        )
    }
    fn context(&self) -> Value {
        self.host.snapshot()["continuationContexts"][0].clone()
    }
    fn read(&self) -> usize {
        self.host
            .continuation_context_reads(Duration::from_millis(40))
    }
    fn action(
        &self,
        reference: &str,
        revision: u64,
        action: &str,
        cursor: Option<&str>,
        direction: Direction,
        turn: Option<&str>,
    ) -> Result<Value, String> {
        self.host.continuation_context_action(
            &generation(),
            "stored",
            reference,
            revision,
            action,
            cursor,
            direction,
            turn,
        )
    }
}
impl Drop for Peer {
    fn drop(&mut self) {
        *self.host.stdin.lock().unwrap() = None;
        let _ = self.child.wait();
        if let Some(worker) = self.worker.take() {
            worker.join().unwrap();
        }
    }
}

#[test]
fn private_continue_admission_returns_before_bounded_context_pair_and_keeps_pages_out_of_live_authority(
) {
    let p = Peer::new(vec![
        Reply::Frame(json!({"result":turns(&["newest","older"],json!("more-turns"))})),
        Reply::Frame(json!({"result":items("newest",json!("more-items"))})),
    ]);
    let (mut browser, reference) = p.admit();
    assert_eq!(
        p.wire.lock().unwrap().len(),
        2,
        "admission did not wait on context IO"
    );
    assert_eq!(p.context()["state"], "queued");
    assert_eq!(
        p.host.snapshot()["threads"][0]["resumeRequestRef"],
        reference
    );
    let custody = p.host.recovery_custody().snapshot();
    // The person's unrelated browser choice cannot retarget the admitted owner.
    browser.select("stored").unwrap();
    assert_eq!(browser.selection_epoch(), 2);
    assert_eq!(p.read(), 2);
    let c = p.context();
    assert_eq!(c["state"], "partial");
    assert_eq!(c["revision"], 1);
    assert_eq!(c["admissionSelectionEpoch"], 1);
    assert_eq!(c["selectedTurnId"], "newest");
    assert_eq!(c["history"]["selectionEpoch"], 1);
    assert_eq!(
        c["history"]["selected"]["itemsPage"],
        items("newest", json!("more-items"))
    );
    assert_eq!(c["history"]["selected"]["appRole"]["standing"], "unknown");
    assert_eq!(c["fullHistoryRebuilt"], false);
    assert_eq!(c["durableNativeData"], false);
    assert!(c["receipts"]
        .as_array()
        .unwrap()
        .iter()
        .all(|r| r["writeResult"] == "written"
            && r["outcome"] == "response-observed-result"
            && r["receiptPosition"].as_u64().unwrap() > 0
            && r.get("response").is_none()));
    let wire = p.wire.lock().unwrap();
    assert_eq!(
        wire[2]["params"],
        json!({"threadId":"stored","itemsView":"summary","sortDirection":"desc","limit":20})
    );
    assert_eq!(
        wire[3]["params"],
        json!({"threadId":"stored","turnId":"newest","sortDirection":"desc","limit":50})
    );
    assert!(!wire.iter().any(|f| matches!(
        f["method"].as_str(),
        Some("turn/start" | "turn/steer" | "thread/start")
    )));
    drop(wire);
    assert_eq!(p.read(), 0, "no auto page draining or repeat");
    assert_eq!(p.host.snapshot()["conversationTurns"], json!([]));
    assert_eq!(
        p.host.recovery_custody().snapshot(),
        custody,
        "context pages do not take CV custody transitions"
    );
    let mut runtime = crate::runtime_session::RuntimeSession::default();
    let received = runtime.receive(&p.host.observe(&generation(), 0));
    assert_eq!(
        received["nativeView"]["items"],
        json!([]),
        "context native responses do not populate the canonical native view"
    );
}

#[test]
fn empty_turn_page_stops_without_item_read_and_unknown_or_foreign_controls_cannot_create_an_owner()
{
    let p = Peer::new(vec![Reply::Frame(json!({"result":turns(&[],Value::Null)}))]);
    assert!(p
        .action("invented", 1, "turns", None, Direction::Desc, None)
        .is_err());
    let (_, reference) = p.admit();
    assert_eq!(p.read(), 1);
    assert_eq!(p.context()["state"], "empty");
    assert!(p.context()["history"]["selected"]["itemsPage"].is_null());
    for (r, v, a, c, t) in [
        ("foreign", 1, "turns", None, None),
        (reference.as_str(), 99, "turns", None, None),
        (reference.as_str(), 1, "items", None, Some("unreceived")),
        (reference.as_str(), 1, "turns", Some("invented"), None),
        (reference.as_str(), 1, "continue", None, None),
    ] {
        assert!(p.action(r, v, a, c, Direction::Desc, t).is_err());
    }
    assert_eq!(p.wire.lock().unwrap().len(), 3);
    assert_eq!(p.context()["revision"], 1);
}

#[test]
fn context_failure_does_not_revoke_admission_and_retry_is_explicit_only() {
    let p = Peer::new(vec![
        Reply::Frame(json!({"result":turns(&["newest"],Value::Null)})),
        Reply::Frame(json!({"error":{"code":-32603,"message":"fixture item read unavailable"}})),
        Reply::Frame(json!({"result":items("newest",Value::Null)})),
    ]);
    let (_, reference) = p.admit();
    assert_eq!(p.read(), 2);
    assert_eq!(p.context()["state"], "unavailable");
    assert!(p.context()["error"]
        .as_str()
        .unwrap()
        .contains("fixture item read unavailable"));
    assert_eq!(
        p.host.snapshot()["threads"][0]["nativeResumeObserved"],
        true
    );
    assert_eq!(p.read(), 0);
    assert_eq!(
        p.action(&reference, 1, "retry", None, Direction::Desc, None)
            .unwrap()["revision"],
        2
    );
    assert_eq!(p.read(), 1);
    assert_eq!(p.context()["state"], "partial");
    assert_eq!(p.context()["error"], Value::Null);
    assert!(p
        .action(&reference, 2, "retry", None, Direction::Desc, None)
        .is_err());
    assert_eq!(
        p.wire
            .lock()
            .unwrap()
            .iter()
            .filter(|f| f["method"] == "thread/resume")
            .count(),
        1
    );
}

#[test]
fn explicit_paging_uses_received_cursor_direction_and_turn_with_new_revisions() {
    let p = Peer::new(vec![
        Reply::Frame(json!({"result":turns(&["newest"],json!("older-cursor"))})),
        Reply::Frame(json!({"result":items("newest",json!("item-next"))})),
        Reply::Frame(json!({"result":turns(&["older"],Value::Null)})),
        Reply::Frame(json!({"result":items("older",Value::Null)})),
    ]);
    let (_, reference) = p.admit();
    p.read();
    p.action(
        &reference,
        1,
        "turns",
        Some("older-cursor"),
        Direction::Desc,
        None,
    )
    .unwrap();
    assert_eq!(p.read(), 1);
    p.action(&reference, 2, "items", None, Direction::Asc, Some("older"))
        .unwrap();
    assert_eq!(p.read(), 1);
    let c = p.context();
    assert_eq!(c["revision"], 3);
    assert_eq!(c["selectedTurnId"], "older");
    assert_eq!(
        c["history"]["selected"]["itemsPage"],
        items("older", Value::Null)
    );
    assert_eq!(
        p.wire.lock().unwrap().len(),
        6,
        "one explicitly chosen page per action"
    );
}

#[test]
fn a_new_context_choice_supersedes_delayed_turns_and_prevents_automatic_phase_two() {
    let (started, seen) = channel();
    let (release, wait) = channel();
    let p = Peer::new(vec![
        Reply::Held(
            json!({"result":turns(&["obsolete"],Value::Null)}),
            started,
            wait,
        ),
        Reply::Frame(json!({"result":turns(&["chosen"],Value::Null)})),
    ]);
    let (_, reference) = p.admit();
    let h = Arc::clone(&p.host);
    let worker = std::thread::spawn(move || h.continuation_context_reads(Duration::from_secs(2)));
    seen.recv_timeout(Duration::from_secs(2)).unwrap();
    p.action(&reference, 1, "turns", None, Direction::Desc, None)
        .unwrap();
    release.send(()).unwrap();
    assert_eq!(worker.join().unwrap(), 1);
    assert!(p.context()["history"]["selected"]["turnsPage"].is_null());
    assert_eq!(p.read(), 1);
    assert_eq!(
        p.context()["history"]["selected"]["turnsPage"],
        turns(&["chosen"], Value::Null)
    );
    assert!(!p
        .wire
        .lock()
        .unwrap()
        .iter()
        .any(|f| f["method"] == "thread/items/list"));
}

#[test]
fn source_restart_during_a_delayed_read_keeps_old_pages_out_of_the_new_source() {
    let (started, seen) = channel();
    let (release, wait) = channel();
    let p = Peer::new(vec![Reply::Held(
        json!({"result":turns(&["obsolete"],Value::Null)}),
        started,
        wait,
    )]);
    let (_, reference) = p.admit();
    let h = Arc::clone(&p.host);
    let worker = std::thread::spawn(move || h.continuation_context_reads(Duration::from_secs(2)));
    seen.recv_timeout(Duration::from_secs(2)).unwrap();
    {
        let mut i = p.host.inner.0.lock().unwrap();
        Host::close_generation(&mut i);
        i.generation["spawnCounter"] = json!(2);
        i.state = "ready".into();
    }
    release.send(()).unwrap();
    assert_eq!(worker.join().unwrap(), 1);
    assert_eq!(p.context()["sourceCurrent"], false);
    assert_eq!(p.context()["state"], "observation-ended");
    assert!(p.context()["history"]["selected"]["turnsPage"].is_null());
    assert!(p
        .action(&reference, 1, "retry", None, Direction::Desc, None)
        .is_err());
    assert_eq!(p.read(), 0);
}

#[test]
fn empty_item_page_and_unfamiliar_native_status_keep_the_actual_partial_result() {
    for page in [
        json!({"data":[],"nextCursor":null}),
        json!({"data":[{"turnId":"newest","item":{"id":"image","type":"imageGeneration","status":"future-native-status","result":"retained native result"}}],"nextCursor":null}),
    ] {
        let p = Peer::new(vec![
            Reply::Frame(json!({"result":turns(&["newest"],Value::Null)})),
            Reply::Frame(json!({"result":page})),
        ]);
        p.admit();
        assert_eq!(p.read(), 2);
        let c = p.context();
        assert_eq!(c["history"]["selected"]["itemsPage"], page);
        assert_eq!(
            c["state"],
            if page["data"].as_array().unwrap().is_empty() {
                "empty"
            } else {
                "partial"
            }
        );
    }
}

#[test]
fn timeout_uncorrelated_malformed_oversized_and_wrong_turn_results_are_not_accepted() {
    let mut wrong_turn = items("foreign-turn", Value::Null);
    wrong_turn["data"][0]["item"]["text"] = json!("Never adopted as this conversation");
    let oversize = turns(&vec!["turn"; 21], Value::Null);
    let cases = vec![
        (vec![Reply::Silent], "turns"),
        (
            vec![Reply::Uncorrelated(
                json!({"id":987654,"result":turns(&["foreign"],Value::Null)}),
            )],
            "turns",
        ),
        (
            vec![Reply::Frame(json!({"result":{"data":"bad-native-page"}}))],
            "turns",
        ),
        (vec![Reply::Frame(json!({"result":oversize}))], "turns"),
        (
            vec![
                Reply::Frame(json!({"result":turns(&["newest"],Value::Null)})),
                Reply::Frame(json!({"result":wrong_turn})),
            ],
            "items",
        ),
    ];
    for (replies, stream) in cases {
        let p = Peer::new(replies);
        p.admit();
        p.read();
        let c = p.context();
        assert_eq!(c["state"], "unavailable");
        assert!(c["history"]["selected"][if stream == "turns" {
            "turnsPage"
        } else {
            "itemsPage"
        }]
        .is_null());
        assert_eq!(
            p.host.snapshot()["threads"][0]["nativeResumeObserved"],
            true,
            "read failure does not alter admission"
        );
        assert_eq!(p.read(), 0, "no timeout/error auto retry");
    }
}

#[test]
fn delayed_item_completion_after_wait_timeout_requires_a_new_explicit_read() {
    let (started, seen) = channel();
    let (release, wait) = channel();
    let p = Peer::new(vec![
        Reply::Frame(json!({"result":turns(&["newest"],Value::Null)})),
        Reply::Held(json!({"result":items("newest",Value::Null)}), started, wait),
    ]);
    let (_, reference) = p.admit();
    let h = Arc::clone(&p.host);
    let worker =
        std::thread::spawn(move || h.continuation_context_reads(Duration::from_millis(25)));
    seen.recv_timeout(Duration::from_secs(2)).unwrap();
    assert_eq!(worker.join().unwrap(), 2);
    assert_eq!(p.context()["state"], "unavailable");
    release.send(()).unwrap();
    // Waiting ended locally. The original query has no automatic accept path.
    assert_eq!(p.read(), 0);
    assert!(p.context()["history"]["selected"]["itemsPage"].is_null());
    p.replies
        .lock()
        .unwrap()
        .push_back(Reply::Frame(json!({"result":items("newest",Value::Null)})));
    p.action(&reference, 1, "retry", None, Direction::Desc, None)
        .unwrap();
    assert_eq!(p.read(), 1);
    assert_eq!(p.context()["state"], "partial");
    assert_eq!(
        p.wire
            .lock()
            .unwrap()
            .iter()
            .filter(|f| f["method"] == "thread/resume")
            .count(),
        1
    );
}
