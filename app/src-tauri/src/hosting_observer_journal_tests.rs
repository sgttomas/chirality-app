//! Actual parser and H4 release with disposable observer replay budgets.
//! Authored source/stdio fixtures only; no stock supplier, model or account.
use super::*;

fn g(counter: u64) -> Value {
    json!({"appSession":"journal-session","home":"journal-home","spawnCounter":counter})
}

fn host_with_limits(entries: usize, bytes: usize, state: &str) -> Arc<Host> {
    let host = Arc::new(Host::new());
    {
        let mut i = host.inner.0.lock().unwrap();
        i.app_session = "journal-session".into();
        i.home = "journal-home".into();
        i.spawn_counter = 1;
        i.generation = g(1);
        i.state = state.into();
        i.start_attempt = 1;
        i.start_admission = Some(StartAdmission::Installed {
            attempt: 1,
            generation: g(1),
        });
        i.version_identity = Some(json!({"declaredPin":"0.160.0"}));
        i.supplier_standing = Some("synthetic source fixture".into());
        i.journal = observer_journal::ObserverJournal::with_limits(entries, bytes);
        i.journal.begin_generation(g(1));
        i.observer_rebuild.reset(&g(1));
    }
    host
}

fn notice(number: u64) -> Value {
    json!({"method":"fixture/notification","params":{"number":number,"text":"é\n包括\"\\"},
           "emittedAtMs":77,"supplierExtra":{"typed":"1","numeric":1,"nested":[null,true]}})
}

fn envelope(frame: &Value, position: u64) -> Value {
    json!({"generation":g(1),"position":position,"class":"notification","frame":frame,"sourceProjection":null})
}

fn emit(host: &Host, frame: &Value, generation: &Value) {
    host.on_line(&serde_json::to_vec(frame).unwrap(), generation);
}

fn private_frames(batch: &NativeProjectionBatch) -> Vec<Value> {
    batch
        .events()
        .filter_map(|event| match event {
            NativeProjectionEvent::Frame(frame) => Some(frame.clone()),
            _ => None,
        })
        .collect()
}

fn ready(host: &Host) -> Value {
    host.finish_start_handshake(
        &g(1),
        1,
        json!({"experimentalApi":true}),
        Ok(json!({"id":1,"result":{"userAgent":"codex/0.160.0"}})),
        false,
    )
    .unwrap()
}

fn auth_request() -> Value {
    json!({"id":"invented-refresh-request","method":"account/chatgptAuthTokens/refresh","params":{}})
}

#[test]
fn default_count_limit_retains_parser_suffix_without_draining_private_delivery_or_writing() {
    let host = host_with_limits(4096, 16 * 1024 * 1024, "ready");
    let owner = host.claim_native_projection().unwrap();
    for number in 1..=4097 {
        emit(&host, &notice(number), &g(1));
    }
    let public = host.journal();
    assert_eq!(public.len(), 4096);
    assert_eq!(public.first().unwrap()["position"], 2);
    assert_eq!(public.last().unwrap()["position"], 4097);
    assert_eq!(
        public
            .iter()
            .map(|value| value["position"].as_u64().unwrap())
            .collect::<Vec<_>>(),
        (2..=4097).collect::<Vec<_>>()
    );
    let before = host.pending_native_projection(&owner).unwrap();
    assert_eq!(private_frames(&before).len(), 4097);
    let status = host.snapshot();
    let coverage = &status["observerRetention"];
    assert_eq!(coverage["maxFrames"], 4096);
    assert_eq!(coverage["maxSerializedBytes"], 16 * 1024 * 1024);
    assert_eq!(coverage["omittedThrough"], 1);
    assert_eq!(coverage["deliveredThrough"], 4097);
    assert_eq!(
        coverage["retainedSerializedBytes"],
        public
            .iter()
            .map(|value| serde_json::to_vec(value).unwrap().len())
            .sum::<usize>()
    );
    assert_eq!(host.observe(&g(1), 1)["gap"], false);
    assert_eq!(host.observe(&g(1), 0)["gap"], true);
    let after = host.pending_native_projection(&owner).unwrap();
    assert_eq!(private_frames(&after), private_frames(&before));
    assert_eq!(host.inner.0.lock().unwrap().send_position, 0);
    assert!(host.client_requests().is_empty());
}

#[test]
fn exact_compact_utf8_budget_includes_metadata_unknown_fields_and_no_newline() {
    let first = notice(1);
    let second = notice(2);
    let expected = vec![envelope(&first, 1), envelope(&second, 2)];
    let budget = expected
        .iter()
        .map(|value| serde_json::to_vec(value).unwrap().len())
        .sum::<usize>();
    for (bytes, retained, floor) in [
        (budget, expected.clone(), 0),
        (budget - 1, vec![expected[1].clone()], 1),
    ] {
        let host = host_with_limits(10, bytes, "ready");
        let owner = host.claim_native_projection().unwrap();
        emit(&host, &first, &g(1));
        emit(&host, &second, &g(1));
        assert_eq!(host.journal(), retained);
        let observed = host.observe(&g(1), floor);
        assert_eq!(observed["gap"], false);
        assert_eq!(observed["position"], 2);
        assert_eq!(
            observed["observerRetention"],
            observed["snapshot"]["observerRetention"]
        );
        assert_eq!(
            observed["observerRetention"]["retainedSerializedBytes"],
            retained
                .iter()
                .map(|value| serde_json::to_vec(value).unwrap().len())
                .sum::<usize>()
        );
        assert_eq!(
            private_frames(&host.pending_native_projection(&owner).unwrap()),
            expected
        );
    }
}

#[test]
fn floor_future_foreign_missing_and_closed_cursors_have_honest_coverage() {
    let host = host_with_limits(2, usize::MAX, "ready");
    for number in 1..=3 {
        emit(&host, &notice(number), &g(1));
    }
    for (after, gap, positions) in [
        (0, true, vec![2, 3]),
        (1, false, vec![2, 3]),
        (2, false, vec![3]),
        (3, false, vec![]),
        (4, true, vec![2, 3]),
    ] {
        let observed = host.observe(&g(1), after);
        assert_eq!(observed["gap"], gap);
        assert_eq!(observed["position"], 3);
        assert_eq!(
            observed["frames"]
                .as_array()
                .unwrap()
                .iter()
                .map(|value| value["position"].as_u64().unwrap())
                .collect::<Vec<_>>(),
            positions
        );
    }
    let mut foreign = vec![Value::Null, json!(1)];
    for field in ["home", "appSession", "spawnCounter"] {
        let mut generation = g(1);
        generation[field] = if field == "spawnCounter" {
            json!(2)
        } else {
            json!("foreign")
        };
        foreign.push(generation);
    }
    for generation in foreign {
        let observed = host.observe(&generation, 3);
        assert_eq!(observed["generation"], g(1));
        assert_eq!(observed["position"], 3);
        assert_eq!(observed["gap"], true);
        assert_eq!(observed["frames"].as_array().unwrap().len(), 2);
    }
    // A ready-looking lifecycle string cannot reopen the actual closed source.
    Host::close_generation(&mut host.inner.0.lock().unwrap());
    let closed = host.observe(&g(1), 1);
    assert_eq!(closed["snapshot"]["state"], "ready");
    assert_eq!(closed["snapshot"]["generationClosed"], true);
    assert_eq!(closed["gap"], true);
    assert_eq!(closed["frames"], json!([]));
    assert_eq!(closed["position"], 3);
    assert_eq!(
        closed["snapshot"]["observerRebuild"]["sourceAvailable"],
        false
    );
    assert!(closed["snapshot"]["observerRebuild"]["unavailableReason"].is_string());
    assert_eq!(
        host.journal().len(),
        2,
        "debug copies do not become closed-source replay"
    );
}

#[test]
fn scoped_stale_source_refuses_before_capture_or_queue_but_missing_cursor_uses_selected_source() {
    let host = host_with_limits(2, usize::MAX, "ready");
    {
        let mut i = host.inner.0.lock().unwrap();
        i.threads
            .push(json!({"generation":g(1),"threadId":"actual-thread"}));
        i.threads
            .push(json!({"generation":g(2),"threadId":"foreign-thread"}));
    }
    for number in 1..=3 {
        emit(&host, &notice(number), &g(1));
    }
    let before = host.inner.0.lock().unwrap().observer_rebuild.snapshot();
    for field in ["home", "appSession", "spawnCounter"] {
        let mut stale = g(1);
        stale[field] = if field == "spawnCounter" {
            json!(2)
        } else {
            json!("foreign")
        };
        let refused = host.observe_scoped(&stale, &Value::Null, 0);
        assert_eq!(refused["sourceUnavailable"], true);
        assert_eq!(refused["requestedSourceGeneration"], stale);
        assert_eq!(refused["generation"], g(1));
        assert!(refused["snapshot"].is_null());
        assert!(refused["position"].is_null());
        assert_eq!(refused["frames"], json!([]));
        assert_eq!(
            host.inner.0.lock().unwrap().observer_rebuild.snapshot(),
            before
        );
    }
    let selected = host.observe_scoped(&g(1), &Value::Null, 0);
    assert_ne!(selected["sourceUnavailable"], true);
    assert_eq!(selected["generation"], g(1));
    assert_eq!(selected["position"], 3);
    assert_eq!(selected["gap"], true);
    assert_eq!(selected["frames"].as_array().unwrap().len(), 2);
    assert_eq!(
        selected["snapshot"]["observerRebuild"]["sourceAvailable"],
        true
    );
    let queued = host.inner.0.lock().unwrap().observer_rebuild.snapshot();
    assert_ne!(queued, before);
    assert_eq!(queued["generation"], g(1));
    assert_eq!(
        queued["requestedCut"], 1,
        "the omission floor, not H or the requested cursor"
    );
    assert_eq!(queued["targets"].as_array().unwrap().len(), 1);
    assert_eq!(queued["targets"][0]["threadId"], "actual-thread");
    host.observe_scoped(&g(1), &g(1), u64::MAX);
    assert_eq!(
        host.inner.0.lock().unwrap().observer_rebuild.snapshot(),
        queued,
        "a future cursor cannot invent a new read cut"
    );
    assert!(
        host.client_requests().is_empty(),
        "observe only queues metadata; it sends no history RPC"
    );
    assert_eq!(host.inner.0.lock().unwrap().send_position, 0);
}

#[test]
fn foreign_and_unpositioned_diagnostics_use_budgets_without_advancing_source_cursor() {
    let host = host_with_limits(2, usize::MAX, "ready");
    emit(&host, &notice(1), &g(1));
    emit(&host, &notice(2), &g(2));
    emit(&host, &notice(3), &g(3));
    let observed = host.observe(&g(1), 1);
    assert_eq!(observed["position"], 1);
    assert_eq!(observed["gap"], false);
    assert_eq!(observed["frames"], json!([]));
    let retained = host.journal();
    assert_eq!(retained.len(), 2);
    assert!(retained.iter().all(
        |value| value["class"] == "closed-generation-frame" && value.get("position").is_none()
    ));
    assert_eq!(observed["observerRetention"]["omittedThrough"], 1);
    assert_eq!(observed["observerRetention"]["generation"], g(1));
    assert_eq!(host.inner.0.lock().unwrap().receipt_position, 1);

    let small = host_with_limits(10, 512, "ready");
    emit(&small, &notice(1), &g(1));
    let prefix = small.journal();
    let mut oversized = notice(2);
    oversized["supplierExtra"] = json!("x".repeat(4096));
    emit(&small, &oversized, &g(2));
    assert_eq!(small.journal(), prefix);
    assert_eq!(small.observe(&g(1), 0)["gap"], false);
    assert_eq!(
        small.snapshot()["observerRetention"]["oversizedDiagnosticFrames"],
        1
    );
    assert_eq!(small.snapshot()["observerRetention"]["deliveredThrough"], 1);
}

#[test]
fn positioned_auth_diagnostic_uses_replay_budget_without_source_highwater_or_oversize_hole() {
    let probe = host_with_limits(10, usize::MAX, "ready");
    emit(&probe, &auth_request(), &g(1));
    let mut diagnostic = probe
        .journal()
        .into_iter()
        .find(|value| value["class"] == "private-auth-request-reply")
        .unwrap();
    assert!(diagnostic.get("frame").is_none());
    diagnostic["position"] = json!(u64::MAX);

    let host = host_with_limits(2, usize::MAX, "ready");
    emit(&host, &notice(1), &g(1));
    host.inner
        .0
        .lock()
        .unwrap()
        .journal
        .push(diagnostic.clone());
    let retained = host.journal();
    let retention = host.snapshot()["observerRetention"].clone();
    assert_eq!(retained.len(), 2);
    assert_eq!(
        retention["retainedSerializedBytes"],
        retained
            .iter()
            .map(|value| serde_json::to_vec(value).unwrap().len())
            .sum::<usize>()
    );
    assert_eq!(retention["deliveredThrough"], 1);
    assert_eq!(retention["omittedThrough"], 0);
    host.inner
        .0
        .lock()
        .unwrap()
        .journal
        .push(diagnostic.clone());
    assert_eq!(
        host.snapshot()["observerRetention"]["omittedThrough"],
        1,
        "only eviction of native receipt 1 changes D"
    );
    assert_eq!(host.snapshot()["observerRetention"]["deliveredThrough"], 1);

    let small = host_with_limits(10, 512, "ready");
    emit(&small, &notice(1), &g(1));
    let prefix = small.journal();
    diagnostic["unknown"] = json!("x".repeat(4096));
    small.inner.0.lock().unwrap().journal.push(diagnostic);
    assert_eq!(small.journal(), prefix);
    let observed = small.observe(&g(1), 0);
    assert_eq!(observed["gap"], false);
    assert_eq!(observed["position"], 1);
    assert_eq!(observed["frames"], json!(prefix));
    assert_eq!(
        observed["observerRetention"]["oversizedDiagnosticFrames"],
        1
    );
    assert_eq!(observed["observerRetention"]["oversizedPrimaryFrames"], 0);
    assert_eq!(observed["observerRetention"]["omittedThrough"], 0);
}

#[test]
fn oversized_primary_is_processed_privately_whole_but_exposes_a_public_gap() {
    let host = host_with_limits(10, 512, "ready");
    let owner = host.claim_native_projection().unwrap();
    emit(&host, &notice(1), &g(1));
    let large_turn = json!({"id":"large-turn","status":"inProgress","items":[],"itemsView":"full","nativeExtra":"x".repeat(4096)});
    let large = json!({"method":"turn/started","params":{"threadId":"thread","turn":large_turn},"nativeUnknown":"unchanged"});
    emit(&host, &large, &g(1));
    assert!(host.journal().is_empty());
    let snapshot = host.snapshot();
    assert_eq!(snapshot["conversationTurns"][0]["nativeTurn"], large_turn);
    assert_eq!(snapshot["turnEventBoundaries"][0]["position"], 2);
    assert_eq!(snapshot["observerRetention"]["oversizedPrimaryFrames"], 1);
    assert_eq!(snapshot["observerRetention"]["omittedThrough"], 2);
    assert_eq!(snapshot["observerRetention"]["deliveredThrough"], 2);
    let private = private_frames(&host.pending_native_projection(&owner).unwrap());
    assert_eq!(private.len(), 2);
    assert_eq!(private[1]["frame"], large);
    assert_eq!(
        private[1]["frame"]["params"]["turn"]["nativeExtra"]
            .as_str()
            .unwrap()
            .len(),
        4096
    );
    emit(&host, &notice(3), &g(1));
    assert_eq!(host.journal()[0]["position"], 3);
    assert_eq!(host.observe(&g(1), 1)["gap"], true);
    assert_eq!(host.observe(&g(1), 2)["gap"], false);
    assert_eq!(
        host.observe(&g(1), 2)["frames"].as_array().unwrap().len(),
        1
    );
}

#[test]
fn h4_held_auth_diagnostics_do_not_advance_public_cursor_before_ready() {
    let host = host_with_limits(1, usize::MAX, "handshaking");
    let owner = host.claim_native_projection().unwrap();
    emit(&host, &auth_request(), &g(1));
    emit(&host, &notice(2), &g(1));
    let held = {
        let i = host.inner.0.lock().unwrap();
        assert_eq!(i.receipt_position, 2);
        assert_eq!(i.held_observer_diagnostics.len(), 1);
        i.held.clone()
    };
    assert_eq!(held.len(), 2);
    assert!(host.journal().is_empty());
    let before = host.observe(&g(1), 0);
    assert_eq!(before["gap"], false);
    assert_eq!(before["position"], 0);
    assert_eq!(
        before["snapshot"]["observerRebuild"]["sourceAvailable"],
        false
    );
    assert!(before["snapshot"]["observerRebuild"]["requestedCut"].is_null());
    assert_eq!(host.observe(&g(1), 1)["gap"], true);
    assert_eq!(host.observe(&g(1), 1)["position"], 0);
    assert!(host
        .pending_native_projection(&owner)
        .unwrap()
        .events()
        .next()
        .is_none());
    let snapshot = ready(&host);
    assert_eq!(snapshot["state"], "ready");
    assert_eq!(snapshot["observerRetention"]["deliveredThrough"], 2);
    assert_eq!(snapshot["observerRetention"]["omittedThrough"], 1);
    assert_eq!(snapshot["observerRetention"]["omittedFrames"], 2);
    assert_eq!(host.journal().len(), 1);
    assert_eq!(host.journal()[0]["position"], 2);
    let batch = host.pending_native_projection(&owner).unwrap();
    assert!(matches!(
        batch.events().next(),
        Some(NativeProjectionEvent::Ready(_))
    ));
    assert_eq!(private_frames(&batch), held, "both native originals precede public suffix eviction; no public-only diagnostic is injected");
}

#[test]
fn failed_held_release_marks_diagnostics_without_inventing_ready_and_new_scope_resets_replay() {
    let host = host_with_limits(10, usize::MAX, "handshaking");
    let owner = host.claim_native_projection().unwrap();
    emit(&host, &auth_request(), &g(1));
    emit(&host, &notice(2), &g(1));
    {
        let mut i = host.inner.0.lock().unwrap();
        Host::deliver_never_ready(&mut i);
        Host::close_generation(&mut i);
        i.state = "failed".into();
    }
    let all = host.journal();
    assert_eq!(all.len(), 3);
    assert_eq!(
        all.iter()
            .map(|value| value["position"].as_u64().unwrap())
            .collect::<Vec<_>>(),
        vec![1, 1, 2]
    );
    assert!(all
        .iter()
        .all(|value| value["generationNeverReady"] == true));
    let batch = host.pending_native_projection(&owner).unwrap();
    assert!(!batch
        .events()
        .any(|event| matches!(event, NativeProjectionEvent::Ready(_))));
    assert_eq!(private_frames(&batch).len(), 2);
    assert!(private_frames(&batch)
        .iter()
        .all(|value| value["generationNeverReady"] == true));
    assert_eq!(host.observe(&g(1), 0)["frames"], json!([]));
    {
        let mut i = host.inner.0.lock().unwrap();
        i.generation = g(2);
        i.spawn_counter = 2;
        i.journal.begin_generation(g(2));
        i.observer_rebuild.reset(&g(2));
        i.receipt_position = 0;
        i.state = "ready".into();
    }
    assert!(host.journal().is_empty());
    assert_eq!(host.snapshot()["observerRetention"]["deliveredThrough"], 0);
    emit(&host, &notice(99), &g(1));
    assert_eq!(host.snapshot()["observerRetention"]["generation"], g(2));
    assert_eq!(host.snapshot()["observerRetention"]["deliveredThrough"], 0);
    assert_eq!(host.observe(&g(1), 0)["gap"], true);
    assert_eq!(host.observe(&g(1), 0)["frames"], json!([]));
    emit(&host, &notice(1), &g(2));
    assert_eq!(host.observe(&g(2), 0)["position"], 1);
    assert_eq!(host.observe(&g(2), 0)["gap"], false);
    assert_eq!(
        host.observe(&g(2), 0)["frames"].as_array().unwrap().len(),
        1
    );
}

#[test]
fn late_auth_reply_observation_cannot_reenter_held_or_advance_a_closed_or_replaced_source() {
    for replace in [false, true] {
        let host = host_with_limits(10, usize::MAX, "handshaking");
        // Echo-only pipe creates an actual bound writer. Holding its serial
        // lock makes source closure win before the original write can start.
        let mut peer = Command::new("/bin/cat")
            .env_clear()
            .stdin(Stdio::piped())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        *host.stdin.lock().unwrap() = peer.stdin.take();
        let serial = host.frame_write.lock().unwrap();
        let reader = Arc::clone(&host);
        let worker = std::thread::spawn(move || emit(&reader, &auth_request(), &g(1)));
        let deadline = std::time::Instant::now() + Duration::from_secs(2);
        while host.inner.0.lock().unwrap().held.is_empty() && std::time::Instant::now() < deadline {
            std::thread::yield_now();
        }
        {
            let mut i = host.inner.0.lock().unwrap();
            assert_eq!(i.held.len(), 1);
            Host::deliver_never_ready(&mut i);
            Host::close_generation(&mut i);
            if replace {
                i.generation = g(2);
                i.spawn_counter = 2;
                i.receipt_position = 0;
                i.journal.begin_generation(g(2));
                i.observer_rebuild.reset(&g(2));
                i.state = "handshaking".into();
            } else {
                i.state = "stopped".into();
            }
        }
        drop(serial);
        worker.join().unwrap();
        *host.stdin.lock().unwrap() = None;
        assert!(peer.wait().unwrap().success());
        let diagnostics = host.journal();
        let late = diagnostics
            .iter()
            .find(|value| value["class"] == "private-auth-request-reply")
            .unwrap();
        assert!(late.get("position").is_none());
        assert_eq!(late["receiptPosition"], 1);
        assert_eq!(late["sourceClosedOrReplaced"], true);
        assert_eq!(late["generation"], g(1));
        let i = host.inner.0.lock().unwrap();
        assert!(i.held_observer_diagnostics.is_empty());
        assert_eq!(i.journal.delivered_through(), if replace { 0 } else { 1 });
    }
}
