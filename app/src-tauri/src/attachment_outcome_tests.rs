// Ordinary ordered attachment submission through genuine private selection,
// preparation, pipe write and correlation. Local /bin/cat is not a supplier.
use super::*;
use crate::runtime_session::{AttachmentSelectionSession, WorkflowRootSession};

struct OutcomeDisk(std::path::PathBuf);
impl Drop for OutcomeDisk {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

// The attachment-related host_status receiving composition, without AppState's
// platform/setup projections. The result below is never used as send authority.
fn status(
    host: &Host,
    selections: &Mutex<Result<AttachmentSelectionSession, String>>,
    custody: &Arc<AttachmentCustody>,
) -> Value {
    let mut value = host.snapshot();
    let generation = value["generation"].clone();
    value["steeringTargets"] = json!(value["threads"]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|row| row["generation"] == generation)
        .filter_map(|row| row["threadId"].as_str())
        .map(|thread| {
            match crate::runtime_session::observed_steering_target(&value, &generation, thread) {
                Ok(target) => json!({"generation":generation,"threadId":thread,"target":target}),
                Err(reason) => {
                    json!({"generation":generation,"threadId":thread,"target":null,"reason":reason})
                }
            }
        })
        .collect::<Vec<_>>());
    let mut selections = selections.lock().unwrap();
    let selections = selections.as_mut().unwrap();
    selections.refresh_submissions(host, custody);
    value["attachmentSelections"] = selections.snapshot();
    value["attachmentCustody"] =
        json!({"state":"opened","root":custody.root().display().to_string()});
    value
}

fn source(host: &Host, generation: &Value) -> Option<SourceRequest> {
    host.client_requests().last().map(|row| {
        host.source_request(generation, &row["requestIdentity"])
            .unwrap()
    })
}
fn source_view(host: &Host, source: Option<&SourceRequest>) -> Value {
    source.map(|source| json!({"requestRef":source.request_ref(),"generation":source.generation(),
        "preparedFrame":source.attempted_frame(),"observation":host.source_request_status(source).unwrap()})).unwrap_or(Value::Null)
}

fn submit(
    selections: &Mutex<Result<AttachmentSelectionSession, String>>,
    workflows: &Mutex<WorkflowRootSession>,
    host: &Host,
    custody: &Arc<AttachmentCustody>,
    args: &Value,
) -> Result<Value, String> {
    let order: Vec<String> = serde_json::from_value(args["selectionRefs"].clone()).unwrap();
    crate::runtime_session::submit_attachments_with_pending_notice(
        selections,
        workflows,
        host,
        Ok(custody.clone()),
        args["ownerRef"].as_str().unwrap(),
        args["listRevision"].as_u64().unwrap(),
        &order,
        &args["generation"],
        args["threadId"].as_str().unwrap(),
        args["expectedTurnId"].as_str(),
        args["text"].as_str().unwrap(),
        crate::recovery::ExplicitAppProjectContext::unknown(),
        None,
    )
}

fn packet(
    case: &str,
    args: &Value,
    before: Value,
    after: Value,
    result: &Result<Value, String>,
    host: &Host,
    generation: &Value,
) -> Value {
    let source = source(host, generation);
    json!({"case":case,"command":"submit_attachments","args":args,
        "beforeHostStatus":before,"afterHostStatus":after,
        "resultKind":if result.is_ok(){"Ok"}else{"Err"},
        "nativeValue":result.as_ref().ok(),"nativeError":result.as_ref().err(),
        "originalSource":source_view(host,source.as_ref())})
}

// Only the pending/late case needs a controllable peer. The frame is read from
// the actual pipe immediately; its matching response is released after the
// production 20-second wait returns. Drop closes/drains on every path.
struct LatePipe {
    host: Arc<Host>,
    child: std::process::Child,
    release: Option<std::sync::mpsc::Sender<bool>>,
    worker: Option<std::thread::JoinHandle<Option<Value>>>,
}
impl LatePipe {
    fn open(host: &Arc<Host>, generation: &Value) -> Self {
        let mut child = Command::new("/bin/cat")
            .env_clear()
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let source = host.clone();
        let generation = generation.clone();
        let (tx, rx) = channel();
        let worker = std::thread::spawn(move || {
            let mut line = String::new();
            if BufReader::new(stdout).read_line(&mut line).ok()? == 0 {
                return None;
            }
            let outbound: Value = serde_json::from_str(&line).ok()?;
            if rx.recv_timeout(Duration::from_secs(45)).ok()? {
                source.on_line(
                    &serde_json::to_vec(
                        &json!({"id":outbound["id"],"result":{"turn":complete_turn()}}),
                    )
                    .unwrap(),
                    &generation,
                );
            }
            Some(outbound)
        });
        Self {
            host: host.clone(),
            child,
            release: Some(tx),
            worker: Some(worker),
        }
    }
    fn acknowledge(&mut self) -> Value {
        self.release.take().unwrap().send(true).unwrap();
        self.worker.take().unwrap().join().unwrap().unwrap()
    }
}
impl Drop for LatePipe {
    fn drop(&mut self) {
        *self
            .host
            .stdin
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner) = None;
        if let Some(release) = self.release.take() {
            let _ = release.send(false);
        }
        if let Some(worker) = self.worker.take() {
            let _ = worker.join();
        }
        let _ = self.child.wait();
    }
}

#[test]
fn attachment_outcome_actual_send_steer_refusal_and_pending_late_dto() {
    let mut cases = vec![];
    for case in [
        "send",
        "steer",
        "changed-file",
        "native-error",
        "malformed-reply",
        "pending-then-late-ack",
    ] {
        let (host, generation, root, custody, _) = context_fixture();
        let _disk = OutcomeDisk(root.clone());
        let (selections, owner, revision, order) = shared_attachment_selected(&root);
        let selection_snapshot = selections.lock().unwrap().as_ref().unwrap().snapshot();
        let workflows = Mutex::new(WorkflowRootSession::default());
        if case == "steer" {
            host.on_line(&serde_json::to_vec(&json!({"method":"turn/started","params":{"threadId":"thread","turn":complete_turn()}})).unwrap(), &generation);
            assert_eq!(
                crate::runtime_session::observed_steering_target(
                    &host.snapshot(),
                    &generation,
                    "thread"
                )
                .unwrap()["turnId"],
                "turn"
            );
        }
        crate::runtime_session::current_conversation(&host.snapshot(), &generation, "thread")
            .unwrap();
        assert_eq!(host.snapshot()["state"], "ready");
        let args = json!({"generation":generation,"threadId":"thread","expectedTurnId":if case=="steer"{json!("turn")}else{Value::Null},
            "text":"Exact person attachment text\r\n家","ownerRef":owner,"listRevision":revision,"selectionRefs":order});
        let initial_bytes = std::fs::read(root.join("first.txt")).unwrap();
        if case == "changed-file" {
            std::fs::write(root.join("first.txt"), b"changed since selection").unwrap();
        }
        let mut dto = None;
        let mut late = Value::Null;
        let result = if case == "changed-file" {
            let mut result = None;
            no_attachment_write(&host, || {
                let before = status(&host, &selections, &custody);
                let returned = submit(&selections, &workflows, &host, &custody, &args);
                let after = status(&host, &selections, &custody);
                dto = Some(packet(
                    case,
                    &args,
                    before,
                    after,
                    &returned,
                    &host,
                    &generation,
                ));
                result = Some(returned);
            });
            assert_eq!(host.inner.0.lock().unwrap().send_position, 0);
            assert!(host.client_requests().is_empty());
            result.unwrap()
        } else if case == "pending-then-late-ack" {
            let mut pipe = LatePipe::open(&host, &generation);
            let before = status(&host, &selections, &custody);
            let returned = submit(&selections, &workflows, &host, &custody, &args);
            let after = status(&host, &selections, &custody);
            dto = Some(packet(
                case,
                &args,
                before,
                after.clone(),
                &returned,
                &host,
                &generation,
            ));
            assert!(returned.is_err());
            let original = source(&host, &generation).unwrap();
            let unknown = host.source_request_status(&original).unwrap();
            assert_eq!(unknown["writeResult"], "written");
            assert_eq!(unknown["waitingEnded"], true);
            assert!(unknown["response"].is_null());
            assert!(
                after["attachmentSelections"]["submissions"][0]["outcome"]["resolution"]
                    ["nativeTurnRef"]
                    .is_null()
            );
            let request_count = host.client_requests().len();
            let send_position = host.inner.0.lock().unwrap().send_position;
            let outbound = pipe.acknowledge();
            let later = status(&host, &selections, &custody);
            let resolution =
                &later["attachmentSelections"]["submissions"][0]["outcome"]["resolution"];
            assert_eq!(resolution["nativeTurnRef"]["turnId"], "turn");
            assert_eq!(
                resolution["nativeTurnRef"]["requestIdentity"],
                *original.request_id()
            );
            assert_eq!(host.client_requests().len(), request_count);
            assert_eq!(host.inner.0.lock().unwrap().send_position, send_position);
            assert_eq!(
                source(&host, &generation).unwrap().request_ref(),
                original.request_ref()
            );
            late = json!({"afterHostStatus":later,"originalSource":source_view(&host,Some(&original)),"actualOutboundFrame":outbound,
                "standing":"late source observation only; original command remains Err; no second dispatch"});
            returned
        } else {
            let response = match case {
                "steer" => json!({"result":{"turnId":"turn"}}),
                "native-error" => {
                    json!({"error":{"code":-32600,"message":"synthetic native refusal"}})
                }
                "malformed-reply" => json!({"result":null}),
                _ => json!({"result":{"turn":complete_turn()}}),
            };
            shared_attachment_exchange(&host, &generation, response, || {
                let before = status(&host, &selections, &custody);
                let returned = submit(&selections, &workflows, &host, &custody, &args);
                let after = status(&host, &selections, &custody);
                dto = Some(packet(
                    case,
                    &args,
                    before,
                    after,
                    &returned,
                    &host,
                    &generation,
                ));
                returned
            })
        };
        if matches!(case, "send" | "steer") {
            let value = result.as_ref().unwrap();
            assert_eq!(value["sourceWriteConfirmed"], true);
            assert_eq!(value["nativeTurnRef"]["generation"], generation);
            assert_eq!(value["nativeTurnRef"]["threadId"], "thread");
            assert_eq!(value["nativeTurnRef"]["turnId"], "turn");
            assert_eq!(
                value["clientMetadata"]["submissionAssociation"]["supplyRefs"]
                    .as_array()
                    .unwrap()
                    .len(),
                order.len()
            );
            assert!(value.get("endNotice").is_none());
        } else {
            assert!(result.is_err());
        }
        let mut dto = dto.unwrap();
        let after = &dto["afterHostStatus"]["attachmentSelections"];
        assert_eq!(after["ownerRef"], owner);
        assert_eq!(after["listRevision"], revision);
        assert_eq!(
            after["selections"], selection_snapshot["selections"],
            "submission never clears or substitutes the owned list"
        );
        if case != "changed-file" {
            assert_eq!(after["submissions"].as_array().unwrap().len(), 1);
            let original = &dto["originalSource"]["observation"];
            assert_eq!(original["actualWriteAttemptObserved"], true);
            assert_eq!(original["writeResult"], "written");
            assert_eq!(
                dto["originalSource"]["preparedFrame"]["method"],
                if case == "steer" {
                    "turn/steer"
                } else {
                    "turn/start"
                }
            );
            if matches!(case, "native-error" | "malformed-reply") {
                assert!(
                    after["submissions"][0]["outcome"]["resolution"]["nativeTurnRef"].is_null()
                );
                assert!(
                    original["response"].is_object(),
                    "actual non-ACK native reply is retained"
                );
            }
            assert_eq!(
                std::fs::read(root.join("first.txt")).unwrap(),
                initial_bytes
            );
        }
        assert!(workflows.lock().unwrap().snapshot()["runs"]
            .as_array()
            .unwrap()
            .is_empty());
        dto["selectionOperationSnapshot"] = selection_snapshot;
        if !late.is_null() {
            dto["lateObservation"] = late;
        }
        cases.push(dto);
    }
    println!(
        "ATTACHMENT_OUTCOME_DTO:{}",
        json!({"cases":cases,"standing":{
            "producer":"actual submit_attachments_with_pending_notice → owned selection → private prepared packet → scoped pipe write/correlation; no pending workflow notice in this unit",
            "status":"actual Host snapshot plus the host_status steering-target, refresh_submissions, selection snapshot and opened-custody projection",
            "fixtureInputs":"existing context_fixture ready generation/thread, native selection of a fresh file, synthetic typed turn/started for Steer, local /bin/cat pipe and matching source callbacks",
            "platformLimit":"AppState/platform/home-routing/setup projections are omitted; any mounted-App wrapper is separate fixture metadata and must not change nativeValue/source observations",
            "authorityLimit":"DTOs and errors are observations, not source capabilities or resend permission; unknown is not no-attempt; provider adoption/completion not established",
            "noticeLimit":"existing TC-2 and private finish/persistence controls reused; no carrier or finish guard changed"
        }})
    );
}
