use super::*;
use crate::conversation_roles::handoff_send::send_handoff_wait;
use crate::runtime_session::{HomeRouter, WorkflowRootSession};
use std::sync::Mutex;

struct Journey {
    f: Fixture,
    handoffs: Arc<Mutex<Handoffs>>,
    homes: Arc<Mutex<HomeRouter>>,
    workflows: Arc<Mutex<WorkflowRootSession>>,
    id: String,
    target: String,
    snapshot: Value,
}
impl Journey {
    fn new() -> Self {
        let f = Fixture::new();
        let source = f.start(Some(Role::HELP_HUMAN), None);
        let handoffs = Arc::new(Mutex::new(Handoffs::default()));
        let homes = Arc::new(Mutex::new(HomeRouter::new(f.home.clone()).unwrap()));
        let workflows = Arc::new(Mutex::new(WorkflowRootSession::default()));
        let begun = continue_as_begin(
            &handoffs,
            &workflows,
            &f.home,
            &f.generation,
            &source,
            Some(Role::WORKING_ITEMS),
        )
        .unwrap();
        let id = begun["id"].as_str().unwrap().to_owned();
        f.until("actual source summary", |status| {
            handoffs.lock().unwrap().view(status)[0]["draft"]["state"] == "drafted"
        });
        let relation =
            continuation_for_start(&handoffs, &f.home, Some(&id), Some(Role::WORKING_ITEMS))
                .unwrap();
        let target = f.start(Some(Role::WORKING_ITEMS), relation);
        handoffs
            .lock()
            .unwrap()
            .started(&id, &target, &f.generation);
        assert_eq!(f.role(&source)["role"], "HELP_HUMAN");
        assert_eq!(f.role(&target)["role"], "WORKING_ITEMS");
        let mut snapshot = f.status();
        snapshot["continueAs"] = handoffs.lock().unwrap().view(&snapshot);
        snapshot["homeRouting"] = homes.lock().unwrap().snapshot();
        snapshot["roleLimits"] = json!({"account":{"roles":[]}});
        Self {
            f,
            handoffs,
            homes,
            workflows,
            id,
            target,
            snapshot,
        }
    }
    fn send(&self, text: &str) -> Value {
        send_handoff_wait(
            &self.handoffs,
            &self.homes,
            &self.workflows,
            &self.id,
            text,
            Duration::from_millis(30),
        )
        .unwrap()
    }
    fn read(&self) -> Value {
        read_handoff_send(&self.handoffs, &self.id).unwrap()
    }
    fn export(&self, name: &str, outcome: &Value) {
        if let Some(directory) = std::env::var_os("CHIRALITY_HANDOFF_FIXTURE_DIR") {
            let mut snapshot = self.f.status();
            snapshot["continueAs"] = self.handoffs.lock().unwrap().view(&snapshot);
            snapshot["homeRouting"] = json!({"activeModeHomeClass":"account"});
            snapshot["roleLimits"] = json!({"account":{"roles":[]}});
            let observation = crate::runtime_session::observe_home(
                &self.homes,
                &self.f.generation,
                &Value::Null,
                0,
            );
            let packet = json!({"snapshot":self.snapshot,"observedSnapshot":snapshot,"windowObservation":observation,"outcome":outcome,"handoffId":self.id,"target":self.target,"generation":self.f.generation,"editedText":EDITED});
            std::fs::write(
                PathBuf::from(directory).join(format!("{name}.json")),
                serde_json::to_vec_pretty(&packet).unwrap(),
            )
            .unwrap();
        }
    }
}
const EDITED: &str = "Handoff edited by the person.\nExact bytes é / 家\n";

#[test]
fn producer_receipts_preserve_native_ack_refusal_error_unknown_and_late_response() {
    let j = Journey::new();
    assert!(j.f.home.host.close_to_new_turns(&j.f.generation).unwrap());
    let refused = j.send(EDITED);
    assert_eq!(refused["state"], "not-attempted");
    j.export("not-attempted", &refused);
    let starts =
        j.f.wire()
            .iter()
            .filter(|frame| frame["method"] == "turn/start")
            .count();
    j.f.home.host.reopen_to_new_turns(&j.f.generation);
    let sent = j.send(EDITED);
    assert_eq!(sent["state"], "sent", "{sent}");
    assert_ne!(
        sent["attemptRef"], refused["attemptRef"],
        "a proved no-attempt permits a new explicit attempt"
    );
    assert_eq!(
        sent["target"],
        json!({"generation":j.f.generation,"threadId":j.target})
    );
    assert_eq!(
        sent["nativeResponse"]["result"]["turn"]["status"],
        "inProgress"
    );
    j.export("sent", &sent);
    let repeated = j.send("must not replace original edited text");
    assert_eq!(repeated["attemptRef"], sent["attemptRef"]);
    assert_eq!(
        j.f.wire()
            .iter()
            .filter(|frame| frame["method"] == "turn/start")
            .count(),
        starts + 1
    );
    let frame =
        j.f.wire()
            .into_iter()
            .filter(|frame| frame["method"] == "turn/start")
            .last()
            .unwrap();
    assert_eq!(
        frame["params"],
        json!({"threadId":j.target,"input":[{"type":"text","text":EDITED,"text_elements":[]}]})
    );
    j.f.home
        .host
        .stop("synthetic source closed", "test")
        .unwrap();
    assert_eq!(
        j.read()["state"],
        "sent",
        "an observed original response survives source closure"
    );

    let j = Journey::new();
    std::fs::write(j.f.root.join("handoff-mode"), "native-error").unwrap();
    let failed = j.send(EDITED);
    assert_eq!(failed["state"], "native-failed");
    assert_eq!(failed["nativeResponse"]["error"]["code"], -32600);
    j.export("native-failed", &failed);
    assert_eq!(
        j.send("no implicit retry")["attemptRef"],
        failed["attemptRef"]
    );

    let j = Journey::new();
    std::fs::write(j.f.root.join("handoff-mode"), "hold").unwrap();
    let unknown = j.send(EDITED);
    assert_eq!(unknown["state"], "unknown", "{unknown}");
    assert_eq!(
        j.handoffs.lock().unwrap().view(&j.f.status())[0]["draftText"],
        EDITED,
        "an observer remount retains the exact original edited draft"
    );
    j.export("unknown", &unknown);
    assert_eq!(
        j.send("do not resend pending text")["attemptRef"],
        unknown["attemptRef"]
    );
    std::fs::write(j.f.root.join("release-handoff"), "").unwrap();
    let deadline = Instant::now() + Duration::from_secs(5);
    let late = loop {
        let value = j.read();
        if value["state"] == "sent" {
            break value;
        }
        assert!(Instant::now() < deadline, "{value}");
        std::thread::sleep(Duration::from_millis(5));
    };
    assert_eq!(late["attemptRef"], unknown["attemptRef"]);
    assert_eq!(late["target"], unknown["target"]);
    j.export("late-sent", &late);
}

#[test]
fn preparing_latch_blocks_duplicates_before_the_original_writer_returns_a_source() {
    let j = Journey::new();
    let before = j.f.home.host.snapshot()["reservedNativeRequests"]
        .as_array()
        .unwrap()
        .len();
    let worker = j.f.home.host.handoff_test_block_writer(|| {
        let (h, homes, w, id) = (
            j.handoffs.clone(),
            j.homes.clone(),
            j.workflows.clone(),
            j.id.clone(),
        );
        let worker = std::thread::spawn(move || {
            send_handoff_wait(&h, &homes, &w, &id, EDITED, Duration::from_secs(2)).unwrap()
        });
        let deadline = Instant::now() + Duration::from_secs(3);
        while j.f.home.host.snapshot()["reservedNativeRequests"]
            .as_array()
            .unwrap()
            .len()
            == before
        {
            assert!(Instant::now() < deadline);
            std::thread::sleep(Duration::from_millis(5));
        }
        let pending = j.read();
        assert_eq!(pending["state"], "sending");
        assert_eq!(
            j.send("a queued second press")["attemptRef"],
            pending["attemptRef"]
        );
        worker
    });
    assert_eq!(worker.join().unwrap()["state"], "sent");
}

#[test]
fn original_generation_and_host_are_never_replaced_by_the_active_source() {
    let j = Journey::new();
    std::fs::write(j.f.root.join("handoff-mode"), "hold").unwrap();
    let unknown = j.send(EDITED);
    assert_eq!(unknown["state"], "unknown");
    j.f.home.host.stop("synthetic replacement", "test").unwrap();
    j.f.home
        .host
        .start(
            j.f.home.host_config.as_ref().unwrap(),
            "synthetic replacement",
        )
        .unwrap();
    let successor = j.f.home.host.snapshot()["generation"].clone();
    assert_ne!(successor, j.f.generation);
    for _ in 0..2 {
        j.f.home
            .host
            .thread_start_selected(
                &j.f.root.to_string_lossy(),
                "fixture-model",
                "fixture-provider",
            )
            .unwrap();
    }
    assert!(j.f.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .iter()
        .any(|thread| thread["threadId"] == j.target));
    let retained = j.send("a successor lookalike must not replace the original");
    assert_eq!(retained["target"], unknown["target"]);
    assert_eq!(retained["attemptRef"], unknown["attemptRef"]);
    assert_eq!(retained["sourceCurrent"], false);
    // A foreign Host can be active in another router; it cannot own this handoff.
    let other = Journey::new();
    let foreign = Mutex::new(HomeRouter::new(other.f.home.clone()).unwrap());
    let retained = send_handoff_wait(
        &j.handoffs,
        &foreign,
        &j.workflows,
        &j.id,
        "no retarget",
        Duration::from_millis(10),
    )
    .unwrap();
    assert_eq!(retained["attemptRef"], unknown["attemptRef"]);
    assert_eq!(retained["target"], unknown["target"]);
    assert_eq!(retained["sourceCurrent"], false);
}
