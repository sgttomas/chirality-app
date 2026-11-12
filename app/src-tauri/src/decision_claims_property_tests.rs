//! The class property of the decision reader's door (review rounds 1 and 2 of
//! #247): adding any set of claim records leaves every row's state, decision
//! and lapse, the decision need's state and the work item's category exactly
//! as the derivation without them; only claims lists differ. A claim request
//! for a package no authorized request names may add a row of its own, which
//! never reads decided. Invented records only; no person performed any act.
use super::*;

#[derive(Clone, Copy, Debug, PartialEq)]
enum ClaimOrigin {
    /// Brought in by the explicit legacy import (copy and account line).
    Legacy,
    /// Written to the store, naming its recorder as the decision actor.
    RecorderAsActor,
    /// Written to the project folder, which the store-held project no longer reads.
    ProjectFile,
}
#[derive(Clone, Copy, Debug, PartialEq)]
enum ClaimKind {
    ActAlt1,
    ActAlt2,
    ActUnnamedAlternative,
    ActOtherKind,
    SameIdIdentical,
    SameIdConflicting,
    CorrectAct,
    Supersede,
    SupersedeSameId,
    Native,
    CorrectRequest,
    LapseLapsed,
    LapseUnknown,
    RequestSameIdIdentical,
    RequestSameIdConflicting,
    RequestSamePackage,
    RequestOtherPackage,
}
const KINDS: [ClaimKind; 17] = [
    ClaimKind::ActAlt1,
    ClaimKind::ActAlt2,
    ClaimKind::ActUnnamedAlternative,
    ClaimKind::ActOtherKind,
    ClaimKind::SameIdIdentical,
    ClaimKind::SameIdConflicting,
    ClaimKind::CorrectAct,
    ClaimKind::Supersede,
    ClaimKind::SupersedeSameId,
    ClaimKind::Native,
    ClaimKind::CorrectRequest,
    ClaimKind::LapseLapsed,
    ClaimKind::LapseUnknown,
    ClaimKind::RequestSameIdIdentical,
    ClaimKind::RequestSameIdConflicting,
    ClaimKind::RequestSamePackage,
    ClaimKind::RequestOtherPackage,
];
fn is_act(kind: ClaimKind) -> bool {
    !matches!(
        kind,
        ClaimKind::CorrectRequest
            | ClaimKind::LapseLapsed
            | ClaimKind::LapseUnknown
            | ClaimKind::RequestSameIdIdentical
            | ClaimKind::RequestSameIdConflicting
            | ClaimKind::RequestSamePackage
            | ClaimKind::RequestOtherPackage
    )
}

fn base_request(d: &Decision) -> Value {
    serde_json::from_slice(&std::fs::read(d.dir.join("acts/00-request.jsonl")).unwrap()).unwrap()
}
fn lapse(a: &Value, id: &str, state: &str) -> Value {
    json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":id,"kind":"act_lapsed",
        "recorder":{"role":"App writer","identity":"writer:lapse"},"context":{"surface":"App"},"seq":1,"writtenAt":"invented",
        "body":{"act":{"recordId":a["recordId"],"actKind":"A16","capturedAt":a["body"]["captureTime"],"capturingSurface":"app_act_control"},
            "state":state,"referents":a["body"]["boundSubject"],"c0":a["body"]["boundContent"][0],
            "c1":{"method":util::FILE_IDENTITY_METHOD,"value":"changed-invented"},"time":"invented"}})
}
fn corrects(mut record: Value, id: &str, target: &str) -> Value {
    record["recordId"] = json!(id);
    record["corrects"] = json!(target);
    record["correctionReason"] = json!("invented correction");
    record
}
fn native(mut a: Value) -> Value {
    a["recorder"] = json!({"role":crate::records::APP_INTERFACE.role,"identity":crate::records::APP_INTERFACE.identity});
    a["body"]["recordingMode"] = json!("direct capture");
    a["observedAt"] = a["body"]["captureTime"].clone();
    a
}
/// Writes several entries as one log, numbering them.
fn log(dir: &Path, name: &str, entries: &[Value]) {
    std::fs::create_dir_all(dir).unwrap();
    let mut text = String::new();
    for (n, e) in entries.iter().enumerate() {
        let mut e = e.clone();
        e["seq"] = json!(n + 1);
        crate::schema_validation::bundled().unwrap().validate(&e).unwrap();
        text += &(e.to_string() + "\n");
    }
    std::fs::write(dir.join(format!("{name}.jsonl")), text).unwrap();
}

/// The authorized record sets, rebuilt from both reviewers' probe families.
const BASES: [&str; 19] = [
    "control", "pending", "unordered-disagree", "unordered-agree", "corrected", "lapsed-witness",
    "lapse-corrected", "unknown-observation", "supersession", "native-ordered", "two-requests",
    "binding-mismatch", "wrong-alternative", "other-kind", "package-edited", "package-absent",
    "incomplete", "request-corrected", "recorder-as-actor-in-store",
];
fn base(f: &Fixture, d: &Decision, name: &str) {
    let acts = d.dir.join("acts");
    let a = act(d, "act", "ALT-2");
    match name {
        "control" => act_log(&d.dir, "10-act", &a),
        "pending" => {}
        "unordered-disagree" | "unordered-agree" => {
            act_log(&d.dir, "10-act", &a);
            act_log(&d.dir, "11-other", &act(d, "other", if name == "unordered-agree" { "ALT-2" } else { "ALT-1" }));
        }
        "corrected" => {
            let first = act(d, "act", "ALT-1");
            let mut fix = corrects(act(d, "act", "ALT-2"), "rec:act-fix", "rec:act");
            fix["body"]["captureEvidence"][0]["ref"] = json!("cap:act-fix");
            log(&acts, "10-act", &[first, fix]);
        }
        "lapsed-witness" => {
            act_log(&d.dir, "10-act", &a);
            act_log(&d.dir, "20-lapse", &lapse(&a, "rec:lapse", "lapsed"));
        }
        "lapse-corrected" => {
            act_log(&d.dir, "10-act", &a);
            let l = lapse(&a, "rec:lapse", "lapsed");
            let mut fix = corrects(l.clone(), "rec:lapse-fix", "rec:lapse");
            fix["body"]["state"] = json!("unknown (unavailable)");
            log(&acts, "20-lapse", &[l, fix]);
        }
        "unknown-observation" => {
            act_log(&d.dir, "10-act", &a);
            act_log(&d.dir, "20-lapse", &lapse(&a, "rec:lapse", "unknown (unavailable)"));
        }
        "supersession" => {
            let mut first = act(d, "act", "ALT-1");
            first["body"]["relations"]["supersededBy"] = json!("rec:other");
            act_log(&d.dir, "10-act", &first);
            act_log(&d.dir, "11-other", &act(d, "other", "ALT-2"));
        }
        "native-ordered" => log(&acts, "10-native", &[native(act(d, "act", "ALT-1")), native(act(d, "other", "ALT-2"))]),
        "two-requests" => {
            let mut r = base_request(d);
            r["recordId"] = json!("rec:request-2");
            act_log(&d.dir, "01-request-2", &r);
            let mut b = act(d, "other", "ALT-1");
            b["body"]["relations"]["requestRef"] = json!("rec:request-2");
            b["body"]["boundSubject"] = json!(["decision package rec:request-2"]);
            act_log(&d.dir, "10-act", &a);
            act_log(&d.dir, "11-other", &b);
        }
        "binding-mismatch" => {
            let mut r = base_request(d);
            r["body"]["evidence"]["claimedIdentity"] = json!("invented-other-content");
            act_log(&d.dir, "00-request", &r);
            act_log(&d.dir, "10-act", &a);
        }
        "wrong-alternative" => act_log(&d.dir, "10-act", &act(d, "act", "ALT-9")),
        "other-kind" => {
            let mut k = a.clone();
            k["body"]["actKind"] = json!("A13");
            k["body"]["relations"].as_object_mut().unwrap().remove("alternativeChosen");
            act_log(&d.dir, "10-act", &k);
        }
        "package-edited" => {
            act_log(&d.dir, "10-act", &a);
            std::fs::write(&d.package, b"{\"edited\":\"after the decision\"}").unwrap();
        }
        "package-absent" => {
            act_log(&d.dir, "10-act", &a);
            std::fs::remove_file(&d.package).unwrap();
        }
        "incomplete" => {
            act_log(&d.dir, "10-act", &a);
            std::fs::write(acts.join("99-unreadable.jsonl"), b"garbage\n").unwrap();
        }
        "request-corrected" => {
            let mut fix = corrects(base_request(d), "rec:request-2", "rec:request");
            fix["body"]["purpose"] = json!("an authorized corrected purpose");
            act_log(&d.dir, "01-request-fix", &fix);
            let mut b = act(d, "act", "ALT-2");
            b["body"]["relations"]["requestRef"] = json!("rec:request-2");
            b["body"]["boundSubject"] = json!(["decision package rec:request-2"]);
            act_log(&d.dir, "10-act", &b);
        }
        "recorder-as-actor-in-store" => {
            let mut s = a.clone();
            s["recorder"]["identity"] = json!("agent:invented");
            s["body"]["decisionActor"] = json!({"displayName":"agent:invented","identityVerified":false});
            act_log(&d.dir, "10-act", &s);
        }
        other => panic!("unknown base {other}"),
    }
    let _ = f;
}

fn claim_record(d: &Decision, request: &Value, kind: ClaimKind, n: usize) -> Value {
    let id = format!("claim-{n}");
    let rid = format!("rec:{id}");
    let mut a = act(d, &id, "ALT-1");
    match kind {
        ClaimKind::ActAlt1 => a,
        ClaimKind::ActAlt2 => act(d, &id, "ALT-2"),
        ClaimKind::ActUnnamedAlternative => act(d, &id, "ALT-9"),
        ClaimKind::ActOtherKind => {
            a["body"]["actKind"] = json!("A13");
            a["body"]["relations"].as_object_mut().unwrap().remove("alternativeChosen");
            a
        }
        ClaimKind::SameIdIdentical => act(d, "act", "ALT-2"),
        ClaimKind::SameIdConflicting => act(d, "act", "ALT-1"),
        ClaimKind::CorrectAct => corrects(a, &rid, "rec:act"),
        ClaimKind::Supersede => {
            let mut s = act(d, "act", "ALT-2");
            s["recordId"] = json!(rid);
            s["body"]["relations"]["supersededBy"] = json!("rec:act");
            s
        }
        ClaimKind::SupersedeSameId => {
            let mut s = act(d, "act", "ALT-2");
            s["body"]["relations"]["supersededBy"] = json!("rec:other");
            s
        }
        ClaimKind::Native => native(a),
        ClaimKind::CorrectRequest => {
            let mut r = corrects(request.clone(), &rid, "rec:request");
            r["body"]["purpose"] = json!("an imported purpose");
            r
        }
        ClaimKind::LapseLapsed => lapse(&act(d, "act", "ALT-2"), &rid, "lapsed"),
        ClaimKind::LapseUnknown => lapse(&act(d, "act", "ALT-2"), &rid, "unknown (unavailable)"),
        ClaimKind::RequestSameIdIdentical => request.clone(),
        ClaimKind::RequestSameIdConflicting => {
            let mut r = request.clone();
            r["body"]["purpose"] = json!("an imported purpose");
            r
        }
        ClaimKind::RequestSamePackage => {
            let mut r = request.clone();
            r["recordId"] = json!(rid);
            r["body"]["purpose"] = json!("an imported purpose");
            r
        }
        ClaimKind::RequestOtherPackage => {
            let mut r = request.clone();
            r["recordId"] = json!(rid);
            r["body"]["evidence"]["ref"] = json!(format!("decisions/claimed-{n}.json"));
            r
        }
    }
}
/// Adds one claim of `kind` with `origin`, as its own log.
fn add_claim(f: &Fixture, d: &Decision, kind: ClaimKind, origin: ClaimOrigin, n: usize) {
    let request = base_request(d);
    let mut record = claim_record(d, &request, kind, n);
    let name = format!("9{n:02}-claim");
    match origin {
        ClaimOrigin::RecorderAsActor => {
            record["recorder"]["identity"] = json!("agent:invented-claimant");
            record["body"]["decisionActor"] = json!({"displayName":"agent:invented-claimant","identityVerified":false});
            log(&d.dir.join("acts"), &name, &[record]);
        }
        ClaimOrigin::ProjectFile => log(&f.project.join(".chirality/records/acts"), &name, &[record]),
        ClaimOrigin::Legacy => {
            // The copy and its account line, as the explicit import writes them.
            let place = f.project.join(".chirality/records/acts");
            log(&place, &name, &[record]);
            let bytes = std::fs::read(place.join(format!("{name}.jsonl"))).unwrap();
            std::fs::write(d.dir.join(format!("acts/{name}.jsonl")), &bytes).unwrap();
            let line = json!({"format":"chirality.records-store.import","formatVersion":"0.1","event":"completed",
                "importId":format!("import:invented-{n}"),"at":"invented",
                "files":[{"original":format!(".chirality/records/acts/{name}.jsonl"),"copy":format!("acts/{name}.jsonl"),
                    "outcome":"copied","sha256":util::sha256_hex(&bytes),"bytes":bytes.len()}],"conflicts":[],"censusChanged":[]});
            let account = d.dir.join("imports.jsonl");
            let mut text = std::fs::read_to_string(&account).unwrap_or_default();
            text += &(line.to_string() + "\n");
            std::fs::write(account, text).unwrap();
        }
    }
}

/// What a person relies on: each row's state, decision and lapse; the need's
/// state; the item's category; whether the act records were fully read.
fn observe(f: &Fixture) -> (Value, Value) {
    observe_with_claims(f).0
}
/// As `observe`, with the number of claims the reader lists anywhere.
fn observe_with_claims(f: &Fixture) -> ((Value, Value), usize) {
    let dv = decision_command(&f.project);
    let listed = array(&dv["claims"]).len() + array(&dv["rows"]).iter().map(|r| array(&r["claims"]).len()).sum::<usize>();
    let (category, need) = decision_need(&f.read());
    let rows: serde_json::Map<String, Value> = array(&dv["rows"])
        .iter()
        .map(|r| {
            (
                format!("{}|{}", text(&r["packageFile"]), text(&r["packageIdentity"]["value"])),
                json!({"state":r["state"],"act":r["decision"]["act"],"alternative":r["decision"]["alternativeChosen"],
                    "lapse":r["decision"]["lapse"],"lapseShown":r["decision"]["lapseShown"],"restsOnClaim":r["restsOnClaimRequest"]}),
            )
        })
        .collect();
    ((Value::Object(rows), json!({"need":need["state"],"category":category,"complete":dv["recordSetComplete"]})), listed)
}
fn same(base: &(Value, Value), with: &(Value, Value), what: &str) {
    assert_eq!(base.1, with.1, "{what}: the need, item or completeness changed");
    for (key, row) in base.0.as_object().unwrap() {
        assert_eq!(Some(row), with.0.get(key), "{what}: row {key} changed");
    }
    for (key, row) in with.0.as_object().unwrap() {
        if !base.0.as_object().unwrap().contains_key(key) {
            assert_eq!(row["restsOnClaim"], true, "{what}: an added row {key} rests on an authorized request");
            assert_ne!(row["state"], "decided", "{what}: an added row {key} reads decided");
        }
    }
}
/// Deterministic choices for the generated combinations.
struct Lcg(u64);
impl Lcg {
    fn next(&mut self, n: usize) -> usize {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 33) as usize) % n
    }
}

#[test]
fn decision_claims_change_nothing_but_the_claims_lists() {
    let mut singles: Vec<(ClaimKind, ClaimOrigin)> = Vec::new();
    for kind in KINDS {
        for origin in [ClaimOrigin::Legacy, ClaimOrigin::RecorderAsActor, ClaimOrigin::ProjectFile] {
            if origin == ClaimOrigin::RecorderAsActor && !is_act(kind) {
                continue; // only an act record names a decision actor
            }
            singles.push((kind, origin));
        }
    }
    let mut rng = Lcg(0x247);
    let mut combinations = 0;
    for name in BASES {
        let without = {
            let f = Fixture::new();
            let d = decision_fixture(&f);
            base(&f, &d, name);
            observe(&f)
        };
        let mut sets: Vec<Vec<(ClaimKind, ClaimOrigin)>> = singles.iter().map(|s| vec![*s]).collect();
        for _ in 0..8 {
            let size = 2 + rng.next(4);
            sets.push((0..size).map(|_| singles[rng.next(singles.len())]).collect());
        }
        for set in sets {
            let f = Fixture::new();
            let d = decision_fixture(&f);
            base(&f, &d, name);
            for (n, (kind, origin)) in set.iter().enumerate() {
                add_claim(&f, &d, *kind, *origin, n);
            }
            let (with, listed) = observe_with_claims(&f);
            same(&without, &with, &format!("{name} + {set:?}"));
            if set.iter().any(|(_, origin)| *origin != ClaimOrigin::ProjectFile) {
                assert!(listed > 0, "{name} + {set:?}: the claims were read and listed");
            }
            combinations += 1;
        }
    }
    println!("DECISION_CLAIMS_PROPERTY: {} base record sets, {} claim combinations", BASES.len(), combinations);
}

#[test]
fn decision_claims_from_a_package_import_change_nothing_but_the_claims_lists() {
    // Claims brought in by a package import: written, exported, removed and
    // restored before the authorized records are written.
    for name in BASES {
        let without = {
            let f = Fixture::new();
            let d = decision_fixture(&f);
            base(&f, &d, name);
            observe(&f)
        };
        let f = Fixture::new();
        let d = decision_fixture(&f);
        let request = base_request(&d);
        std::fs::remove_file(d.dir.join("acts/00-request.jsonl")).unwrap();
        let kinds = [ClaimKind::SameIdConflicting, ClaimKind::CorrectAct, ClaimKind::LapseLapsed, ClaimKind::RequestSameIdConflicting, ClaimKind::Native];
        let records: Vec<Value> = kinds.iter().enumerate().map(|(n, k)| claim_record(&d, &request, *k, n)).collect();
        for (n, record) in records.iter().enumerate() {
            log(&d.dir.join("acts"), &format!("9{n:02}-claim"), &[record.clone()]);
        }
        let bag = f.root.join("invented-package");
        crate::records_export::export(&f.project, &bag).unwrap();
        for n in 0..records.len() {
            std::fs::remove_file(d.dir.join(format!("acts/9{n:02}-claim.jsonl"))).unwrap();
        }
        let actor = crate::act_control::person(Some("Invented package fixture"), Some("fixture-os"));
        let observed = json!({"fixture":"source-only package import stand-in; no live person's act"});
        let plan = records_store::package::prepare(&f.project, &bag, &actor, &observed).unwrap();
        records_store::package::apply(plan, &actor, &observed).unwrap();
        act_log(&d.dir, "00-request", &request);
        base(&f, &d, name);
        same(&without, &observe(&f), &format!("{name} + package-imported claims"));
    }
}
