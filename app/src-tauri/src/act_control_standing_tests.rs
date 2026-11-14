use super::*;

struct Fixture {
    root: PathBuf,
    request: Value,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().join(crate::util::opaque_id("a16-standing-").unwrap());
        std::fs::create_dir_all(root.join("project/decisions")).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        std::fs::copy(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
            root.join("project/decisions/PKG-1.json"),
        )
        .unwrap();
        let request = crate::recorder::identify_packages(&root).unwrap().remove(0);
        Self { root, request }
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.root).unwrap();
    }
}

#[test]
fn decision_view_small_invented_set_reread_cost() {
    let f = Fixture::new();
    let start = std::time::Instant::now();
    let view = crate::decision_view::derive(&f.root, &[]);
    let elapsed = start.elapsed();
    eprintln!(
        "A16 standing re-read: {} request, {} entries; derive took {elapsed:?}",
        view["rows"].as_array().unwrap().len(),
        storage::read_all(&f.root).0.len()
    );
    assert_eq!(view["rows"][0]["package"], f.request["recordId"]);
    assert!(view["limits"].as_array().unwrap().is_empty(), "{view}");
    assert!(
        elapsed < std::time::Duration::from_secs(1),
        "derive takes seconds: {elapsed:?}"
    );
    f.native();
    f.request_again(false);
    let start = std::time::Instant::now();
    let with_capture = crate::decision_view::derive(&f.root, &[]);
    let elapsed = start.elapsed();
    eprintln!("A16 standing re-read with an unsealed A16 capture: 2 requests, {} entries; derive took {elapsed:?}", storage::read_all(&f.root).0.len());
    assert_eq!(with_capture["rows"].as_array().unwrap().len(), 2);
    assert_eq!(with_capture["rows"][0]["decision"]["shownStatementBinding"]["state"], "bound");
    assert!(elapsed < std::time::Duration::from_secs(1), "derive takes seconds: {elapsed:?}");
}

impl Fixture {
    fn path(&self) -> PathBuf {
        self.root.join("project/decisions/PKG-1.json")
    }
    fn compose(&self) -> (ActControl, String) {
        let mut control = ActControl::new(&self.root);
        let offer = control
            .compose_a16(self.request["recordId"].as_str().unwrap())
            .unwrap();
        let id = offer["offerId"].as_str().unwrap().to_owned();
        (control, id)
    }
    fn request_again(&self, different: bool) -> Value {
        let mut body = self.request["body"].clone();
        if different {
            body["evidence"]["claimedIdentity"] = json!("1".repeat(64));
        }
        records::append(
            &storage::project_file(&self.root, LOG).unwrap(),
            "act_request",
            &records::APP_WRITER,
            body,
        )
        .unwrap()
    }
    fn claim(&self, request: &Value, alternative: &str, serial: usize) -> Value {
        let body = json!({
            "actKind":"A16", "decisionActor":person(Some("Invented person"),Some("invented")),
            "recordingMode":"direct capture", "boundSubject":[format!("decision package {}",request["recordId"].as_str().unwrap())],
            "boundContent":[{"method":request["body"]["evidence"]["method"],"value":request["body"]["evidence"]["claimedIdentity"]}],
            "scope":request["body"]["scope"],"purpose":request["body"]["purpose"],
            "captureEvidence":[{"kind":"capture evidence","ref":format!("cap:invented-{serial}"),"resolutionAtWrite":"resolved"}],
            "captureTime":"2026-11-14T12:00:00Z","evidenceLimits":["synthetic fixture; no person's act"],
            "relations":{"requestRef":request["recordId"],"alternativeChosen":alternative}
        });
        records::append(
            &storage::project_file(&self.root, LOG).unwrap(),
            "human_act",
            &records::APP_WRITER,
            body,
        )
        .unwrap()
    }
    fn native(&self) -> (Value, String) {
        let (mut control, id) = self.compose();
        let actor = person(Some("Invented person"), Some("invented"));
        let statement = control
            .confirmation_statement(&id, "ALT-1", &actor)
            .unwrap();
        control.present(&id).unwrap();
        let result = control
            .confirm_shown(&id, "ALT-1", actor, &statement.text)
            .unwrap();
        assert_eq!(result["state"], "AC-7 recorded", "{result}");
        (result, statement.text)
    }
    fn corrupt_record(&self, id: &str) {
        let log = storage::project_file(&self.root, LOG).unwrap();
        let text = std::fs::read_to_string(&log).unwrap();
        let mut found = false;
        let changed = text
            .lines()
            .map(|line| {
                let parsed: Value = serde_json::from_str(line).unwrap();
                if parsed["recordId"] == id {
                    found = true;
                    "corrupt invented decision line".to_owned()
                } else {
                    line.to_owned()
                }
            })
            .collect::<Vec<_>>()
            .join("\n")
            + "\n";
        assert!(found);
        std::fs::write(log, changed).unwrap();
    }
}

#[test]
fn decided_request_is_shown_and_corrupting_its_record_removes_the_claim() {
    let f = Fixture::new();
    let record = f.claim(&f.request, "ALT-1", 1);
    let (mut c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "decided");
    let text = c
        .confirmation_text(&id, "ALT-2", &person(None, None))
        .unwrap();
    assert!(
        text.contains(
            "A decision on this request is already recorded: alternative ALT-1, recorded at "
        ),
        "{text}"
    );
    f.corrupt_record(record["recordId"].as_str().unwrap());
    let (mut c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "unknown");
    let text = c
        .confirmation_text(&id, "ALT-2", &person(None, None))
        .unwrap();
    assert!(
        text.contains("not known: The decision records could not all be read"),
        "{text}"
    );
    assert!(!text
        .lines()
        .any(|l| l.starts_with("A decision on this request is already recorded:")));
}

#[test]
fn several_unordered_decisions_have_their_own_form() {
    let f = Fixture::new();
    f.claim(&f.request, "ALT-1", 1);
    f.claim(&f.request, "ALT-2", 2);
    let (mut c, id) = f.compose();
    assert_eq!(
        c.offers[&id].offer["packageStanding"]["form"],
        "several-unordered"
    );
    assert_eq!(c.offers[&id].offer["otherRequestsForPath"], json!({"state":"read-whole","rows":[]}));
    let text = c.confirmation_text(&id, "ALT-1", &person(None, None)).unwrap();
    assert!(text.contains("Several decisions on this request are recorded"));
    assert!(!text.contains("Other requests for the file at this path could not all be read."));
}

#[test]
fn own_unordered_standing_does_not_hide_an_unreadable_other_request() {
    let f = Fixture::new();
    f.claim(&f.request, "ALT-1", 1);
    f.claim(&f.request, "ALT-2", 2);
    let other = f.request_again(false);
    let decision = f.claim(&other, "ALT-1", 3);
    let (c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "several-unordered");
    assert_eq!(c.offers[&id].offer["otherRequestsForPath"]["state"], "read-whole");
    f.corrupt_record(decision["recordId"].as_str().unwrap());
    let (mut c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["otherRequestsForPath"]["state"], "not-read-whole");
    let text = c.confirmation_text(&id, "ALT-1", &person(None, None)).unwrap();
    assert!(text.contains("Other requests for the file at this path could not all be read."));
}

#[test]
fn a_decision_between_compose_and_confirm_refuses_before_capture_and_restatement() {
    for restate in [false, true] {
        let f = Fixture::new();
        let (mut c, id) = f.compose();
        let actor = person(None, None);
        c.confirmation_text(&id, "ALT-1", &actor).unwrap();
        c.present(&id).unwrap();
        f.claim(&f.request, "ALT-2", 1);
        let error = if restate {
            c.confirmation_text(&id, "ALT-1", &actor).unwrap_err()
        } else {
            c.confirm(&id, "ALT-1", InputSource::HostNativeConfirmation, actor)
                .unwrap_err()
        };
        assert_eq!(error, package_standing::CHANGED);
        assert_eq!(c.offers[&id].state, OfferState::Stale);
        assert!(c.native_captures.is_empty());
    }
}

#[test]
fn either_missing_standing_property_is_refused_at_native_confirmation() {
    for missing in ["packageStanding", "otherRequestsForPath"] {
        let f = Fixture::new();
        let (mut c, id) = f.compose();
        let actor = person(None, None);
        c.confirmation_text(&id, "ALT-1", &actor).unwrap();
        c.present(&id).unwrap();
        c.offers
            .get_mut(&id)
            .unwrap()
            .offer
            .as_object_mut()
            .unwrap()
            .remove(missing);
        let error = c
            .confirm(&id, "ALT-1", InputSource::HostNativeConfirmation, actor)
            .unwrap_err();
        assert!(error.contains("no complete request standing"), "{error}");
        assert!(c.native_captures.is_empty());
    }
}

#[test]
fn shown_statement_is_native_capture_evidence_and_the_reader_requires_it() {
    let f = Fixture::new();
    let (result, text) = f.native();
    let capture = &result["capture"];
    assert_eq!(
        capture["shownStatement"],
        json!({"method":"sha-256","value":crate::util::sha256_hex(text.as_bytes())})
    );
    assert!(capture.get("seal").is_none());
    assert_eq!(capture["evidenceLimits"], json!(["identity not verified"]));
    let view = crate::decision_view::derive(&f.root, &[]);
    assert_eq!(
        view["rows"][0]["decision"]["shownStatementBinding"]["state"], "bound",
        "{view}"
    );
    let path = storage::capture_path(&f.root, capture["captureId"].as_str().unwrap()).unwrap();
    let mut missing = capture.clone();
    missing.as_object_mut().unwrap().remove("shownStatement");
    std::fs::write(&path, serde_json::to_vec(&missing).unwrap()).unwrap();
    let view = crate::decision_view::derive(&f.root, &[]);
    assert_eq!(
        view["rows"][0]["decision"]["shownStatementBinding"]["state"], "not-bound",
        "{view}"
    );
    let mut changed = capture.clone();
    changed["shownStatement"]["value"] = json!("0".repeat(64));
    let log = storage::project_file(&f.root, LOG).unwrap();
    let record_bytes = std::fs::read(&log).unwrap();
    std::fs::write(&path, serde_json::to_vec(&changed).unwrap()).unwrap();
    let binding = crate::decision_view::derive(&f.root, &[])["rows"][0]["decision"]["shownStatementBinding"].clone();
    assert_eq!(binding["state"], "bound");
    assert_eq!(binding["digest"], changed["shownStatement"]);
    assert_eq!(std::fs::read(&log).unwrap(), record_bytes);
    let words = binding["statement"].as_str().unwrap();
    assert!(words.contains("The records chain does not protect any capture field"));
    assert!(words.contains("an edited unsealed digest still reads bound"));
    // An unsealed digest does not authenticate its writer or detect an edited digest.
    // If a capture does carry a seal, its evidence must still check before reporting bound.
    crate::capture_seal::seal(&f.root, &mut changed).unwrap();
    std::fs::write(&path, serde_json::to_vec(&changed).unwrap()).unwrap();
    assert_eq!(crate::decision_view::derive(&f.root, &[])["rows"][0]["decision"]["shownStatementBinding"]["state"], "bound");
    changed["shownStatement"]["value"] = json!("1".repeat(64));
    std::fs::write(&path, serde_json::to_vec(&changed).unwrap()).unwrap();
    assert_eq!(crate::decision_view::derive(&f.root, &[])["rows"][0]["decision"]["shownStatementBinding"]["state"], "not-bound");    std::fs::remove_file(&path).unwrap();
    let binding = crate::decision_view::derive(&f.root, &[])["rows"][0]["decision"]["shownStatementBinding"].clone();
    assert_eq!(binding["state"], "not-bound");
    assert!(!binding["statement"].as_str().unwrap().contains("verified"));
}


#[test]
fn native_a16_does_not_create_capture_seal_keys() {
    let f = Fixture::new();
    let keys = f.root.with_file_name(crate::util::opaque_id("a16-unused-keys-").unwrap());
    crate::capture_seal::set_folder_for_test(Some(Some(keys.clone())));
    let (result, _) = f.native();
    let view = crate::decision_view::derive(&f.root, &[]);
    crate::capture_seal::set_folder_for_test(None);
    assert!(result["capture"].get("seal").is_none());
    assert!(!keys.exists());
    assert_eq!(view["rows"][0]["decision"]["shownStatementBinding"]["state"], "bound");
}

#[test]
fn the_exact_presented_statement_is_required_not_only_its_offer() {
    let f = Fixture::new();
    let (mut c, id) = f.compose();
    let actor = person(None, None);
    let text = c.confirmation_text(&id, "ALT-1", &actor).unwrap();
    c.present(&id).unwrap();
    assert!(c
        .confirm_shown(&id, "ALT-1", actor, &(text + "changed"))
        .unwrap_err()
        .contains("differs from what was presented"));
    assert!(c.native_captures.is_empty());
}

#[test]
fn another_decided_request_at_the_exact_path_is_shown_and_unreadable_is_not_whole() {
    let f = Fixture::new();
    let other = f.request_again(false);
    let act = f.claim(&other, "ALT-2", 2);
    let (mut c, id) = f.compose();
    let offer = &c.offers[&id].offer;
    assert_eq!(offer["packageStanding"]["form"], "none-recorded");
    assert_eq!(offer["otherRequestsForPath"]["state"], "read-whole");
    assert_eq!(offer["otherRequestsForPath"]["rows"][0]["form"], "decided");
    assert_eq!(
        offer["otherRequestsForPath"]["rows"][0]["relation"],
        "later"
    );
    let text = c
        .confirmation_text(&id, "ALT-1", &person(None, None))
        .unwrap();
    assert!(
        text.contains(
            "A later request for the file at this path has a recorded decision: alternative ALT-2"
        ),
        "{text}"
    );
    f.corrupt_record(act["recordId"].as_str().unwrap());
    let (mut c, id) = f.compose();
    assert_eq!(
        c.offers[&id].offer["otherRequestsForPath"]["state"],
        "not-read-whole"
    );
    let text = c
        .confirmation_text(&id, "ALT-1", &person(None, None))
        .unwrap();
    assert!(text.contains("Other requests for the file at this path could not all be read."));
    assert!(!text.contains("has a recorded decision"));
}

#[test]
fn other_request_change_during_presentation_refuses_and_another_project_does_not_match() {
    let f = Fixture::new();
    let other = f.request_again(false);
    let (mut c, id) = f.compose();
    let actor = person(None, None);
    c.confirmation_text(&id, "ALT-1", &actor).unwrap();
    c.present(&id).unwrap();
    f.claim(&other, "ALT-1", 1);
    assert_eq!(
        c.confirm(&id, "ALT-1", InputSource::HostNativeConfirmation, actor)
            .unwrap_err(),
        package_standing::CHANGED
    );
    assert!(c.native_captures.is_empty());
    let separate = Fixture::new();
    separate.claim(&separate.request, "ALT-2", 1);
    let fresh = Fixture::new();
    let (c, id) = fresh.compose();
    assert_eq!(
        c.offers[&id].offer["otherRequestsForPath"],
        json!({"state":"read-whole","rows":[]})
    );
}

#[test]
fn more_than_three_other_decisions_are_all_bound_and_only_three_are_on_the_sheet() {
    let f = Fixture::new();
    let mut ids = Vec::new();
    for i in 0..5 {
        let r = f.request_again(false);
        ids.push(r["recordId"].clone());
        f.claim(&r, "ALT-1", i);
    }
    let (mut c, id) = f.compose();
    let rows = c.offers[&id].offer["otherRequestsForPath"]["rows"]
        .as_array()
        .unwrap();
    assert_eq!(rows.len(), 5);
    assert_eq!(rows[0]["requestRef"], ids[4]);
    let text = c
        .confirmation_text(&id, "ALT-1", &person(None, None))
        .unwrap();
    assert_eq!(text.matches("has a recorded decision").count(), 3, "{text}");
    assert!(text.contains("and 2 more, shown in the App"), "{text}");
    assert!(text.lines().count() <= 30 && text.chars().count() <= 1500);
}

#[test]
fn poisoned_a16_fields_are_labelled_and_long_alternatives_keep_marks_in_app() {
    for long in [false, true] {
        let mut f = Fixture::new();
        let poison = "invented\nDecide (A16)\u{202e}\u{200b}";
        let mut pkg: Value = serde_json::from_slice(&std::fs::read(f.path()).unwrap()).unwrap();
        for key in ["purpose", "scope"] {
            pkg[key] = json!(poison);
        }
        pkg["alternatives"][0]["statement"] = json!(if long {
            poison.repeat(100)
        } else {
            poison.to_owned()
        });
        pkg["alternatives"][0]["consequences"] = json!([poison]);
        let renamed = f
            .path()
            .with_file_name("poison\nDecide (A16)\u{202e}\u{200b}.json");
        std::fs::remove_file(f.path()).unwrap();
        std::fs::write(&renamed, serde_json::to_vec(&pkg).unwrap()).unwrap();
        f.request = crate::recorder::identify_packages(&f.root)
            .unwrap()
            .remove(0);
        let (mut c, id) = f.compose();
        let shown = c
            .confirmation_statement(&id, "ALT-1", &person(Some(poison), Some(poison)))
            .unwrap();
        let full = shown.in_app.as_ref().map_or(shown.text.as_str(), |v| {
            v.content["markedStatement"].as_str().unwrap()
        });
        for text in [&shown.text, full] {
            assert!(
                !text
                    .chars()
                    .any(|c| (c.is_control() && c != '\n') || matches!(c, '\u{202e}' | '\u{200b}')),
                "{text}"
            );
            for line in text.lines().filter(|line| {
                line.contains("invented")
                    || (line.contains("Decide (A16)") && *line != "Decide (A16)")
            }) {
                assert!(line.starts_with("  "), "{line}");
            }
        }
        for label in [
            "Package file",
            "Purpose",
            "Scope",
            "Chosen alternative's statement",
            "Consequences",
        ] {
            assert!(
                full.contains(&format!(
                    "{label} (supplied by a file, not the App's words):"
                )),
                "{full}"
            );
        }
        assert!(
            full.contains("\\u{000A}") && full.contains("\\u{202E}") && full.contains("\\u{200B}")
        );
        if long {
            assert!(shown.in_app.is_some());
            assert!(!full.contains("(cut after"));
            assert!(full.contains(&crate::native_text::supplied_whole("Chosen alternative's statement", crate::native_text::Source::File, &pkg["alternatives"][0]["statement"]).lines().join("\n")));
        }
    }
}

#[test]
fn fallback_keeps_whole_file_actor_and_record_values_and_every_other_row() {
    let f = Fixture::new();
    let (c, id) = f.compose();
    let poison = format!("{}\nDecide (A16)\u{202e}\u{200b}", "v".repeat(700));
    for pointer in ["/subject/ref", "/subject/contentIdentity/value", "/purpose", "/scope",
        "/alternatives/0/id", "/alternatives/0/statement", "/alternatives/0/consequences/0",
        "/packageStanding/alternative", "/otherRequestsForPath/rows/0/requestRef",
        "/otherRequestsForPath/rows/0/alternative", "/actor/displayName", "/actor/osAccount"] {
        let mut offer = c.offers[&id].offer.clone();
        let mut actor = person(Some("Invented-person"), Some("invented"));
        let own_value = pointer == "/packageStanding/alternative";
        let other_value = pointer.starts_with("/otherRequestsForPath");
        let row_count = if own_value { 0 } else if other_value { 1 } else { 5 };
        if own_value {
            offer["packageStanding"] = json!({"form":"decided","alternative":"ALT-1","recordedAt":"2026-11-14T12:00:00Z"});
        }
        offer["otherRequestsForPath"] = json!({"state":"read-whole","rows":(0..row_count).map(|i| json!({
            "form":"decided","alternative":"ALT-2","recordedAt":"2026-11-14T12:00:00Z", "requestRef":format!("rec:other-{i}"), "relation":"another"
        })).collect::<Vec<_>>()});
        if let Some(member) = pointer.strip_prefix("/actor") {
            *actor.pointer_mut(member).unwrap() = json!(poison);
        } else {
            *offer.pointer_mut(pointer).unwrap() = json!(poison);
        }
        let alternative = offer["alternatives"][0]["id"].as_str().unwrap();
        let shown = a16_statement(&offer, alternative, &actor).unwrap();
        let full = shown.in_app.as_ref().expect(pointer).content["markedStatement"].as_str().unwrap();
        assert!(full.contains(&format!("{}\\u{{000A}}\n  Decide (A16)\\u{{202E}}\\u{{200B}}", "v".repeat(700))), "{pointer}: {full}");
        assert!(!full.contains("(cut after"), "{pointer}");
        assert_eq!(full.matches("has a recorded decision").count(), row_count, "{pointer}");
        assert!(shown.text.contains("any values cut here are whole there"), "{pointer}");
        assert!(native_statement::bounded("A16", shown.text).is_ok());
    }
}

#[test]
fn even_a_shortened_alert_gets_whole_app_content_when_one_value_would_be_cut() {
    let f = Fixture::new();
    let (c, id) = f.compose();
    let mut offer = c.offers[&id].offer.clone();
    offer["subject"]["ref"] = json!("x");
    offer["purpose"] = json!("p".repeat(700));
    offer["scope"] = json!("x");
    offer["alternatives"][0]["statement"] = json!("x");
    offer["alternatives"][0]["consequences"] = json!([]);
    let actor = person(None, None);
    let uncut = a16_lines(&offer, "ALT-1", &actor, true, false).unwrap();
    assert!(native_statement::bounded("A16", uncut).is_ok());
    let shown = a16_statement(&offer, "ALT-1", &actor).unwrap();
    let full = shown.in_app.as_ref().unwrap().content["markedStatement"].as_str().unwrap();
    assert!(full.contains(&"p".repeat(700)) && !full.contains("(cut after"));
    assert!(shown.text.contains("The complete marked statement has moved to the App"));
}

#[test]
fn a16_schema_properties_accept_evidence_and_reject_invalid_maintained_fixtures() {
    let fixtures = Path::new(env!("CARGO_MANIFEST_DIR")).join("schemas/fixtures");
    for (name, validate) in [
        (
            "aac.offer.example.valid.json",
            crate::schema_validation::validate_offer as fn(&Value) -> Result<(), String>,
        ),
        (
            "aac.capture-evidence.example.valid.json",
            crate::schema_validation::validate_capture,
        ),
    ] {
        let values: Value =
            serde_json::from_slice(&std::fs::read(fixtures.join(name)).unwrap()).unwrap();
        for value in values["instances"].as_array().unwrap() {
            validate(value).unwrap();
        }
    }
    for name in [
        "aac.offer.standing-form.invalid.json",
        "aac.offer.decided-missing-alternative.invalid.json",
        "aac.offer.other-requests.invalid.json",
    ] {
        let value = serde_json::from_slice(&std::fs::read(fixtures.join(name)).unwrap()).unwrap();
        assert!(
            crate::schema_validation::validate_offer(&value).is_err(),
            "{name}"
        );
    }
    let other = serde_json::from_slice(
        &std::fs::read(fixtures.join("aac.offer.other-requests.example.valid.json")).unwrap(),
    )
    .unwrap();
    crate::schema_validation::validate_offer(&other).unwrap();
    let value = serde_json::from_slice(
        &std::fs::read(fixtures.join("aac.capture-evidence.shown-statement.invalid.json")).unwrap(),
    )
    .unwrap();
    assert!(crate::schema_validation::validate_capture(&value).is_err());
}

#[test]
fn equivalent_records_keep_the_decided_alternative_without_inventing_one_record_time() {
    let f = Fixture::new();
    f.claim(&f.request, "ALT-1", 1);
    f.claim(&f.request, "ALT-1", 1);
    let view = crate::decision_view::derive(&f.root, &[]);
    assert!(view["rows"][0]["decision"]["act"].is_null(), "{view}");
    let (mut c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "decided");
    assert_eq!(
        c.offers[&id].offer["packageStanding"]["alternative"],
        "ALT-1"
    );
    assert!(c
        .confirmation_text(&id, "ALT-2", &person(None, None))
        .unwrap()
        .contains("recording time not uniquely established"));
}

#[test]
fn other_requests_only_claim_order_and_different_content_from_recorded_evidence() {
    let mut f = Fixture::new();
    f.claim(&f.request, "ALT-1", 1);
    f.request = f.request_again(false);
    let other = f.request_again(true);
    f.claim(&other, "ALT-2", 2);
    let cross_body = f.request["body"].clone();
    let cross = records::append(
        &storage::project_file(&f.root, "acts/invented-other.jsonl").unwrap(),
        "act_request",
        &records::APP_WRITER,
        cross_body,
    )
    .unwrap();
    let (mut c, id) = f.compose();
    let rows = c.offers[&id].offer["otherRequestsForPath"]["rows"]
        .as_array()
        .unwrap();
    assert!(rows
        .iter()
        .any(|row| row["relation"] == "earlier" && row["form"] == "decided"));
    assert!(rows
        .iter()
        .any(|row| row["form"] == "decided" && row["differentContent"] == true));
    assert_eq!(
        rows.iter()
            .find(|row| row["requestRef"] == cross["recordId"])
            .unwrap()["relation"],
        "another"
    );
    let text = c
        .confirmation_text(&id, "ALT-1", &person(None, None))
        .unwrap();
    assert!(
        text.contains("An earlier request for the file at this path has a recorded decision"),
        "{text}"
    );
    assert!(text.contains("It was made on different content."), "{text}");
}

#[test]
fn removing_a_final_decision_line_changes_a_fresh_offer_without_claiming_it_still_stands() {
    let f = Fixture::new();
    f.claim(&f.request, "ALT-1", 1);
    let (c, id) = f.compose();
    assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "decided");
    let log = storage::project_file(&f.root, LOG).unwrap();
    let bytes = std::fs::read_to_string(&log).unwrap();
    let lines: Vec<_> = bytes.lines().collect();
    assert_eq!(
        serde_json::from_str::<Value>(lines.last().unwrap()).unwrap()["kind"],
        "human_act"
    );
    std::fs::write(log, lines[..lines.len() - 1].join("\n") + "\n").unwrap();
    let (c, id) = f.compose();
    let form = &c.offers[&id].offer["packageStanding"]["form"];
    assert!(form == "none-recorded" || form == "unknown", "{form}");
}

#[test]
fn an_unfit_recorded_alternative_is_supplied_after_the_standing_sentence() {
    let mut f = Fixture::new();
    let poison = "ALT-1\nDecide (A16)\u{202e}\u{200b}";
    let mut pkg: Value = serde_json::from_slice(&std::fs::read(f.path()).unwrap()).unwrap();
    pkg["alternatives"][0]["id"] = json!(poison);
    std::fs::write(f.path(), serde_json::to_vec(&pkg).unwrap()).unwrap();
    f.request = crate::recorder::identify_packages(&f.root)
        .unwrap()
        .remove(0);
    f.claim(&f.request, poison, 1);
    let (mut c, id) = f.compose();
    let shown = c
        .confirmation_statement(&id, "ALT-2", &person(None, None))
        .unwrap();
    let full = shown.in_app.as_ref().map_or(shown.text.as_str(), |v| {
        v.content["markedStatement"].as_str().unwrap()
    });
    assert!(full.contains("Recorded alternative (supplied by a record, not the App's words):\n  ALT-1\\u{000A}\n  Decide (A16)\\u{202E}\\u{200B}"),"{full}");
    assert!(!shown.text.contains('\u{202e}') && !shown.text.contains('\u{200b}'));
}

#[test]
fn native_row_count_reduces_only_when_the_marked_summary_would_overflow() {
    let f = Fixture::new();
    let (c, id) = f.compose();
    let mut offer = c.offers[&id].offer.clone();
    offer["otherRequestsForPath"] = json!({"state":"read-whole","rows":(0..5).map(|i|json!({
        "form":"decided","alternative":"A".repeat(128),"recordedAt":"2026-11-14T12:00:00.00000000000000000000Z",
        "requestRef":format!("rec:{}{i}","r".repeat(122)),"relation":"another"
    })).collect::<Vec<_>>()});
    crate::schema_validation::validate_offer(&offer).unwrap();
    let shown = a16_statement(&offer, "ALT-1", &person(None, None)).unwrap();
    assert!(shown.in_app.is_some());
    let count = shown.text.matches("has a recorded decision").count();
    eprintln!("A16 maximum-identifier fixture: {count} other request(s) on the sheet; {} more shown in the App", 5-count);
    assert!((1..3).contains(&count), "{count}: {}", shown.text);
    assert!(shown
        .text
        .contains(&format!("and {} more, shown in the App", 5 - count)));
    assert!(shown.text.chars().count() <= 1500 && shown.text.lines().count() <= 30);
}

#[test]
fn a16_statement_examples_keep_standing_between_scope_and_the_chosen_alternative() {
    let f = Fixture::new();
    let mut examples = serde_json::Map::new();
    for form in ["none-recorded", "decided", "several-unordered", "unknown"] {
        if form == "decided" {
            f.claim(&f.request, "ALT-1", 1);
        }
        if form == "several-unordered" {
            f.claim(&f.request, "ALT-2", 2);
        }
        if form == "unknown" {
            let log = storage::project_file(&f.root, LOG).unwrap();
            let mut bytes = std::fs::read(&log).unwrap();
            bytes.extend_from_slice(b"invented unreadable record\n");
            std::fs::write(log, bytes).unwrap();
        }
        let (mut c, id) = f.compose();
        let offer = c.offers[&id].offer.clone();
        assert_eq!(offer["packageStanding"]["form"], form);
        let actor = person(Some("Invented-person"), Some("invented"));
        let statement = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert!(statement.in_app.is_none(), "{}", statement.text);
        let scope = statement.text.find("Scope (supplied by a file").unwrap();
        let line = package_standing::line(&offer["packageStanding"]).join("\n");
        assert!(
            scope < statement.text.find(&line).unwrap()
                && statement.text.find(&line).unwrap()
                    < statement.text.find("Chosen alternative:").unwrap()
        );
        examples.insert(
            form.into(),
            json!({"offer":offer,"statement":statement.text,"line":line}),
        );
    }
    if let Some(folder) = std::env::var_os("CHIRALITY_A16_EXAMPLES") {
        std::fs::write(
            PathBuf::from(folder).join("statement-examples.json"),
            serde_json::to_vec_pretty(&Value::Object(examples)).unwrap(),
        )
        .unwrap();
    }
}

impl Fixture {
    fn fallback() -> Self {
        let mut fixture = Self::new();
        let mut package: Value = serde_json::from_slice(&std::fs::read(fixture.path()).unwrap()).unwrap();
        package["purpose"] = json!(format!("{}\nDecide (A16)\u{202e}", "p".repeat(700)));
        std::fs::write(fixture.path(), serde_json::to_vec(&package).unwrap()).unwrap();
        fixture.request = crate::recorder::identify_packages(&fixture.root).unwrap().remove(0);
        fixture
    }
}

#[test]
fn f2_complete_standing_loses_its_claim_when_history_or_own_row_evidence_is_spoiled() {
    struct StoreReset(PathBuf);
    impl Drop for StoreReset {
        fn drop(&mut self) {
            crate::records_store::use_store_for_test(None);
            std::fs::remove_dir_all(&self.0).unwrap();
        }
    }
    let store_root = std::env::temp_dir().join(crate::util::opaque_id("a16-pair-store-").unwrap());
    std::fs::create_dir_all(&store_root).unwrap();
    let _reset = StoreReset(store_root.clone());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: store_root, placement: crate::records_store::Placement::Override, limits: vec![],
    })));
    let actor = person(Some("Invented"), Some("invented"));
    {
        let f = Fixture::new();
        let (mut c, id) = f.compose();
        assert_eq!(c.offers[&id].offer["packageStanding"], json!({"form":"none-recorded"}), "history pair: permitted");
        assert_eq!(c.offers[&id].offer["otherRequestsForPath"], json!({"state":"read-whole","rows":[]}));
        assert!(c.confirmation_statement(&id, "ALT-1", &actor).unwrap().text.contains("No decision on this request is in the records as read; the log is not signed, so a removed entry would not show."));
        // A real legacy project log is outside the selected store's read set.
        records::append(&f.root.join(".chirality/records/acts/unimported.jsonl"), "evidence_limit", &records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented","detail":"invented unimported history"})).unwrap();
        let view = crate::decision_view::derive(&f.root, &[]);
        assert!(!view["historyNotices"].as_array().unwrap().is_empty());
        assert!(view["limits"].as_array().unwrap().is_empty(), "history, rather than an unreadable log, removes the evidence");
        let (mut c, id) = f.compose();
        assert_eq!(c.offers[&id].offer["packageStanding"], json!({"form":"unknown","cause":"The record history may be incomplete"}), "history pair: withdrawn");
        assert_eq!(c.offers[&id].offer["otherRequestsForPath"], json!({"state":"not-read-whole","rows":[]}));
        let statement = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert!(statement.text.contains("The record history may be incomplete"));
        assert!(!statement.text.contains("No decision on this request is in the records as read; the log is not signed, so a removed entry would not show."));
    }
    {
        let mut f = Fixture::new();
        let (mut c, id) = f.compose();
        assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "none-recorded", "own-row pair: permitted");
        assert_eq!(c.offers[&id].offer["otherRequestsForPath"], json!({"state":"read-whole","rows":[]}));
        assert!(c.confirmation_statement(&id, "ALT-1", &actor).unwrap().text.contains("No decision on this request is in the records as read; the log is not signed, so a removed entry would not show."));
        // Still schema-valid, but one alternative has no recorded consequence.
        let mut body = f.request["body"].clone();
        body["consequences"].as_array_mut().unwrap().retain(|value| value["alternative"] == "ALT-1");
        f.request = records::append(&storage::project_file(&f.root, LOG).unwrap(), "act_request", &records::APP_WRITER, body).unwrap();
        let (mut c, id) = f.compose();
        assert_eq!(c.offers[&id].offer["packageStanding"], json!({"form":"unknown","cause":"The request's recorded standing could not be resolved"}), "own-row pair: withdrawn");
        let statement = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert!(statement.text.contains("The request's recorded standing could not be resolved"));
        assert!(!statement.text.contains("No decision on this request is in the records as read; the log is not signed, so a removed entry would not show."));
    }
}

#[test]
fn f2_different_content_wording_requires_two_comparable_recorded_identities() {
    for missing_identity in [false, true] {
        let f = Fixture::new();
        let log = storage::project_file(&f.root, LOG).unwrap();
        let before_other_request = std::fs::read(&log).unwrap();
        let comparable = f.request_again(true);
        let (mut c, id) = f.compose();
        let rows = c.offers[&id].offer["otherRequestsForPath"]["rows"].as_array().unwrap();
        assert_eq!(rows.len(), 1);
        assert_eq!(rows[0]["requestRef"], comparable["recordId"]);
        assert_eq!(rows[0]["differentContent"], true, "content pair: permitted");
        let actor = person(Some("Invented"), Some("invented"));
        assert!(c.confirmation_statement(&id, "ALT-1", &actor).unwrap().text.contains("It was made on different content."));
        // Replace the actual request suffix, not an offer/view value, then append a
        // schema-valid request without the comparison evidence used above.
        std::fs::write(&log, &before_other_request).unwrap();
        let mut body = comparable["body"].clone();
        if missing_identity {
            body["evidence"].as_object_mut().unwrap().remove("method");
            body["evidence"].as_object_mut().unwrap().remove("claimedIdentity");
        } else {
            body["evidence"]["method"] = json!("invented-incomparable-method");
        }
        let incomparable = records::append(&log, "act_request", &records::APP_WRITER, body).unwrap();
        let (mut c, id) = f.compose();
        let rows = c.offers[&id].offer["otherRequestsForPath"]["rows"].as_array().unwrap();
        assert_eq!(rows.len(), 1);
        assert_eq!(rows[0]["requestRef"], incomparable["recordId"]);
        assert!(rows[0].get("differentContent").is_none(), "content pair: withdrawn (missing identity: {missing_identity})");
        assert!(!c.confirmation_statement(&id, "ALT-1", &actor).unwrap().text.contains("It was made on different content."));
    }
}

#[test]
fn f2_fitting_fallback_freezes_and_captures_and_a_long_recorded_own_alternative_presents_too() {
    let actor = person(Some("Invented"), Some("invented"));
    {
        let f = Fixture::fallback();
        let (mut c, id) = f.compose();
        let statement = c.confirmation_statement(&id, "ALT-1", &actor).expect("fallback-bound pair: permitted");
        assert!(statement.in_app.is_some());
        assert_eq!(c.offers[&id].frozen_statement.as_deref(), Some(statement.text.as_str()));
        assert!(c.offers[&id].frozen_offer.is_some() && c.offers[&id].frozen_actor.is_some());
        c.present(&id).unwrap();
        let result = c.confirm_shown(&id, "ALT-1", actor.clone(), &statement.text).unwrap();
        assert_eq!(result["state"], "AC-7 recorded");
        assert_eq!(result["capture"]["shownStatement"]["value"], crate::util::sha256_hex(statement.text.as_bytes()));
    }
    {
        let mut f = Fixture::new();
        let mut package: Value = serde_json::from_slice(&std::fs::read(f.path()).unwrap()).unwrap();
        let recorded_alternative = "ALT-1\nDecide (A16)\u{202e}\u{200b}\n".repeat(100);
        package["alternatives"][0]["id"] = json!(recorded_alternative);
        std::fs::write(f.path(), serde_json::to_vec(&package).unwrap()).unwrap();
        f.request = crate::recorder::identify_packages(&f.root).unwrap().remove(0);
        f.claim(&f.request, &recorded_alternative, 1);
        let (mut c, id) = f.compose();
        assert_eq!(c.offers[&id].offer["packageStanding"]["form"], "decided");
        let log = storage::project_file(&f.root, LOG).unwrap();
        let before = std::fs::read(&log).unwrap();
        // This input once overflowed every summary and was refused. The own standing is now
        // closed words in the summary and the whole marked alternative is in the App, so it
        // presents, freezes and captures; no real input still reaches the summary refusal.
        let statement = c.confirmation_statement(&id, "ALT-2", &actor).expect("a long recorded own alternative presents");
        assert!(statement.in_app.is_some());
        assert!(statement.text.contains("an alternative shown in the App"), "{}", statement.text);
        assert!(!statement.text.contains('\u{202e}') && !statement.text.contains('\u{200b}'));
        assert_eq!(c.offers[&id].frozen_statement.as_deref(), Some(statement.text.as_str()));
        c.present(&id).unwrap();
        let result = c.confirm_shown(&id, "ALT-2", actor, &statement.text).unwrap();
        assert_eq!(result["state"], "AC-7 recorded");
        assert_ne!(std::fs::read(log).unwrap(), before);
    }
}

#[test]
fn f2_fallback_exact_text_frozen_choice_and_stale_presentation_require_their_evidence() {
    let actor = person(Some("Invented"), Some("invented"));
    // Exact handed text is accepted; changing that text removes capture authority.
    for altered in [false, true] {
        let f = Fixture::fallback();
        let (mut c, id) = f.compose();
        let statement = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        let in_app = statement.in_app.as_ref().expect("fallback-specific pair");
        assert_eq!(in_app.digest, native_statement::content_digest("A16 pair", &in_app.content).unwrap());
        native_statement::showing_in_app(Some(in_app), || {
            let shown = native_statement::shown_in_app();
            assert_eq!(shown.as_array().unwrap().len(), 1);
            assert_eq!(shown[0]["content"], in_app.content);
            assert_eq!(shown[0]["digest"], in_app.digest);
        });
        assert_eq!(native_statement::shown_in_app(), json!([]));
        c.present(&id).unwrap();
        let log = storage::project_file(&f.root, LOG).unwrap();
        let before = std::fs::read(&log).unwrap();
        let text = if altered { statement.text.clone() + "x" } else { statement.text.clone() };
        let result = c.confirm_shown(&id, "ALT-1", actor.clone(), &text);
        if altered {
            assert!(result.unwrap_err().contains("differs from what was presented"), "handed-text pair: withdrawn");
            assert!(c.native_captures.is_empty());
            assert_eq!(std::fs::read(log).unwrap(), before);
        } else {
            let result = result.expect("handed-text pair: permitted");
            assert_eq!(result["state"], "AC-7 recorded");
            assert_eq!(result["capture"]["shownStatement"]["value"], crate::util::sha256_hex(statement.text.as_bytes()));
        }
    }
    // Repeating the same frozen facts is accepted; changing the choice is refused.
    {
        let f = Fixture::fallback();
        let (mut c, id) = f.compose();
        let first = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        c.present(&id).unwrap();
        let repeated = c.confirmation_statement(&id, "ALT-1", &actor).expect("frozen-choice pair: permitted");
        assert_eq!(repeated.text, first.text);
        assert_eq!(repeated.in_app.unwrap().content, first.in_app.as_ref().unwrap().content);
        assert!(c.confirmation_statement(&id, "ALT-2", &actor).err().expect("frozen-choice pair: withdrawn").contains("frozen for another alternative"));
        assert!(c.confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor.clone()).unwrap_err().contains("differs from the frozen native confirmation"));
        assert!(c.native_captures.is_empty());
        assert_eq!(c.offers[&id].frozen_statement.as_deref(), Some(first.text.as_str()));
        assert_eq!(c.confirm_shown(&id, "ALT-1", actor.clone(), &first.text).unwrap()["state"], "AC-7 recorded");
    }
    // Fresh presentation is accepted; changed evidence makes that same slot Stale.
    // Restoring the bytes cannot revive it, while a fresh offer can proceed.
    {
        let f = Fixture::fallback();
        let (mut c, id) = f.compose();
        let first = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert!(first.in_app.is_some());
        c.present(&id).expect("stale-presentation pair: permitted");
        let log = storage::project_file(&f.root, LOG).unwrap();
        let before = std::fs::read(&log).unwrap();
        f.claim(&f.request, "ALT-2", 1);
        assert_eq!(c.confirm_shown(&id, "ALT-1", actor.clone(), &first.text).unwrap_err(), package_standing::CHANGED);
        assert_eq!(c.offers[&id].state, OfferState::Stale);
        std::fs::write(&log, &before).unwrap();
        let restored = c.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert_eq!(restored.text, first.text);
        assert_eq!(restored.in_app.unwrap().content, first.in_app.unwrap().content);
        assert!(c.present(&id).unwrap_err().contains("Stale"), "stale-presentation pair: withdrawn");
        assert!(c.confirm_shown(&id, "ALT-1", actor.clone(), &first.text).unwrap_err().contains("Stale"));
        assert!(c.native_captures.is_empty());
        assert_eq!(std::fs::read(log).unwrap(), before);
        let fresh = c.compose_a16(f.request["recordId"].as_str().unwrap()).unwrap();
        let fresh_id = fresh["offerId"].as_str().unwrap();
        let statement = c.confirmation_statement(fresh_id, "ALT-1", &actor).unwrap();
        assert!(statement.in_app.is_some());
        c.present(fresh_id).unwrap();
        assert_eq!(c.confirm_shown(fresh_id, "ALT-1", actor, &statement.text).unwrap()["state"], "AC-7 recorded");
    }
}

#[test]
fn a_long_marked_own_recorded_alternative_moves_to_the_app_instead_of_refusing() {
    let f = Fixture::new();
    let (c, id) = f.compose();
    let actor = person(Some("Invented-person"), Some("invented"));
    let mut offer = c.offers[&id].offer.clone();
    let alternative = offer["alternatives"][0]["id"].as_str().unwrap().to_owned();
    // Permitted: a plain recorded alternative stays on the native summary itself.
    offer["packageStanding"] = json!({"form":"decided","alternative":"ALT-2","recordedAt":"2026-11-14T12:00:00Z"});
    offer["purpose"] = json!("p".repeat(1400));
    let plain = a16_statement(&offer, &alternative, &actor).unwrap();
    assert!(plain.in_app.is_some());
    assert!(plain.text.contains("A decision on this request is already recorded: alternative ALT-2, recorded at 2026-11-14T12:00:00Z."), "{}", plain.text);
    // Spoiled: 700 direction overrides mark to far more than the alert bound. Before, every
    // fallback summary kept that marked value and the act was refused; now it moves wholly
    // into the App content and the summary names it there in closed words.
    let poison = "\u{202E}".repeat(700);
    offer["packageStanding"] = json!({"form":"decided","alternative":poison,"recordedAt":"2026-11-14T12:00:00Z"});
    let moved = a16_statement(&offer, &alternative, &actor).expect("a long recorded alternative must not refuse the act");
    assert!(moved.text.contains("A decision on this request is already recorded: an alternative shown in the App, recorded at 2026-11-14T12:00:00Z."), "{}", moved.text);
    assert!(!moved.text.contains("\\u{202E}") && !moved.text.contains('\u{202E}'));
    let full = moved.in_app.as_ref().unwrap().content["markedStatement"].as_str().unwrap();
    assert_eq!(full.matches("\\u{202E}").count(), 700, "the whole marked value is in the App");
    assert!(native_statement::bounded("A16", moved.text).is_ok());
}


#[test]
fn f2_a_summary_that_cannot_fit_neither_presents_nor_freezes_nor_captures() {
    // The decided property, kept by a test-only seam now that no real input overflows the
    // closed fallback summary: whatever the cause, a statement that cannot fit does nothing.
    struct Reset;
    impl Drop for Reset {
        fn drop(&mut self) { native_statement::TEST_LIMIT.with(|limit| limit.set(None)); }
    }
    let actor = person(Some("Invented"), Some("invented"));
    let f = Fixture::fallback();
    let (mut c, id) = f.compose();
    let log = storage::project_file(&f.root, LOG).unwrap();
    let before = std::fs::read(&log).unwrap();
    {
        let _reset = Reset;
        native_statement::TEST_LIMIT.with(|limit| limit.set(Some((3, 120))));
        let error = c.confirmation_statement(&id, "ALT-1", &actor).err().expect("a summary that cannot fit is refused");
        assert!(error.contains("exceeds the readable native confirmation (3 lines, 120 characters)"), "{error}");
    }
    let slot = &c.offers[&id];
    assert!(slot.selected.is_none() && slot.frozen_offer.is_none() && slot.frozen_actor.is_none() && slot.frozen_statement.is_none());
    assert!(c.confirm(&id, "ALT-1", InputSource::HostNativeConfirmation, actor.clone()).unwrap_err().contains("not presented"));
    c.present(&id).unwrap();
    assert!(c.confirm(&id, "ALT-1", InputSource::HostNativeConfirmation, actor.clone()).unwrap_err().contains("differs from the frozen native confirmation"));
    assert!(c.native_captures.is_empty());
    assert_eq!(std::fs::read(&log).unwrap(), before);
    // Permitted half: with the real limit the same offer presents and captures.
    let (mut c, id) = f.compose();
    let statement = c.confirmation_statement(&id, "ALT-1", &actor).expect("the real limit presents");
    c.present(&id).unwrap();
    assert_eq!(c.confirm_shown(&id, "ALT-1", actor, &statement.text).unwrap()["state"], "AC-7 recorded");
}
