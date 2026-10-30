use super::*;

struct Fixture {
    root: PathBuf,
    project: ProjectRecords,
    run: String,
    start: String,
    selection: String,
    check: String,
    folder: PathBuf,
}
impl Fixture {
    fn new() -> Self {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("historical-learning-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let folder = crate::storage::project_file(&root, "workflow").unwrap();
        std::fs::create_dir_all(&folder).unwrap();
        let project = ProjectRecords::open(&root).unwrap();
        let mut f = Self {
            root,
            project,
            run: "run:historical-read".into(),
            start: String::new(),
            selection: String::new(),
            check: String::new(),
            folder,
        };
        let mut start = Self::example("run_text", Some("run start"));
        start["run"] = json!(f.run);
        start["conversation"] = json!("thread:historical");
        start["selection"] = json!("selection:historical");
        start["chain"] = Value::Null;
        start["lines"].as_object_mut().unwrap().remove("chain_line");
        let selection = json!({"record_kind":"selection_record","selection_id":"selection:historical","identity":start["workflow"],"holding_library":start["holding_library"],"standing":"registered","selected_by":"the person (App interface)","how":"explicit","conversation":start["conversation"],"selected_at":"fixture"});
        f.selection = f.wr(selection, &[]);
        f.start = f.wr(start.clone(), &[f.selection.clone()]);
        let mut check = Self::example("supply_check", None);
        check["run"] = json!(f.run);
        check["conversation"] = start["conversation"].clone();
        f.check = f.wr(check, &[f.start.clone()]);
        f.rs("run_opened",json!({"runId":f.run,"startedBy":{"kind":"person"},"surface":"App run","workflow":{"kind":start["workflow"]["kind"],"origin":start["workflow"]["origin"],"sourceRoot":start["workflow"]["source_root"],"name":start["workflow"]["name"],"revision":start["workflow"]["revision"],"revisionVerification":"verified"},"conversationRef":start["conversation"]}));
        f
    }
    fn example(kind: &str, purpose: Option<&str>) -> Value {
        include_str!("../../../execution/PKG-02/DEL-02-02/Work/workspace-registration.valid.examples.jsonl").lines().map(|l|serde_json::from_str::<Value>(l).unwrap()).find(|v|v["record_kind"]==kind && purpose.is_none_or(|p|v["purpose"]==p)).unwrap()
    }
    fn wr(&self, body: Value, basis: &[String]) -> String {
        let reference = crate::util::opaque_id("wr-record:v1:").unwrap();
        let envelope = json!({"version":1,"record_id":reference,"writer":"fixture:historical-reader","observed_at":"fixture","body":body,"basis_records":basis,"source_references":[]});
        let path = self.folder.join(format!(
            "{}.json",
            reference.strip_prefix("wr-record:v1:").unwrap()
        ));
        std::fs::write(path, serde_json::to_vec(&envelope).unwrap()).unwrap();
        self.project.resolve(&reference).unwrap();
        reference
    }
    fn rs(&self, kind: &'static str, body: Value) {
        let mut entry =
            crate::records::supply::PendingRunEntry::new(kind, body, crate::util::now_rfc3339())
                .unwrap();
        crate::records::supply::append_run_entry(&self.root, &self.run, &mut entry).unwrap();
    }
    fn read(&self) -> Result<HistoricalRun, String> {
        HistoricalRun::read(&self.project, &self.run)
    }
    fn change(&self, reference: &str, edit: impl FnOnce(&mut Value)) {
        let path = self.folder.join(format!(
            "{}.json",
            reference.strip_prefix("wr-record:v1:").unwrap()
        ));
        let mut v: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        edit(&mut v);
        std::fs::write(path, serde_json::to_vec(&v).unwrap()).unwrap();
    }
    fn ended(&self) {
        self.rs(
            "run_ended",
            json!({"stoppedBy":"the person","cause":"ended by the person","waitingArrivals":[]}),
        );
    }
    fn notice(&self) -> String {
        let mut notice = Self::example("run_text", Some("run end notice"));
        notice["run"] = json!(self.run);
        notice["conversation"] = json!("thread:historical");
        let reference = self.wr(notice.clone(), &[self.start.clone()]);
        let mut check = Self::example("supply_check", None);
        check["check"] = json!("check:end");
        check["run"] = json!(self.run);
        check["conversation"] = notice["conversation"].clone();
        check["purpose"] = json!("run end notice");
        check["turn"] = json!("turn:end");
        check["client_user_message_id"] = json!("client:end");
        check["expected_text"] = notice["text_identity"].clone();
        check["observed_text"] = notice["text_identity"].clone();
        check.as_object_mut().unwrap().remove("expected_workflow");
        self.wr(check, &[reference.clone()]);
        reference
    }
    fn following(&self) -> PathBuf {
        let original = self.project.resolve(&self.start).unwrap();
        let mut start = original.body().clone();
        let run = "run:following";
        start["run"] = json!(run);
        // Reusing the selected workflow retains the choice ID across runs.
        start["chain"] = json!({"prior_run":self.run,"prior_workflow":original.body()["workflow"],"ended":"ended by the person"});
        start["lines"]["chain_line"]=json!(format!("[Chirality] Previous workflow run ended: review-pack revision rev-P1 (run {}, ended by the person). Its instructions no longer apply.",self.run));
        let mut selection = self
            .project
            .resolve(&self.selection)
            .unwrap()
            .body()
            .clone();
        selection["selection_id"] = start["selection"].clone();
        selection["prior_run"] = json!({"run":self.run,"workflow":original.body()["workflow"],"ended":"ended by the person"});
        let selected = self.wr(selection, &[]);
        let started = self.wr(start.clone(), &[selected]);
        let mut check = self.project.resolve(&self.check).unwrap().body().clone();
        check["run"] = json!(run);
        check["turn"] = json!("following-turn");
        check["client_user_message_id"] = json!("following-client");
        check["check"] = json!("following-check");
        self.wr(check, &[started]);
        let (entries, _) = crate::storage::read_all(&self.root);
        let mut body = entries
            .iter()
            .find(|e| e["kind"] == "run_opened" && e["runId"] == self.run)
            .unwrap()["body"]
            .clone();
        body["runId"] = json!(run);
        body["follows"] = json!(self.run);
        let mut entry = crate::records::supply::PendingRunEntry::new(
            "run_opened",
            body,
            crate::util::now_rfc3339(),
        )
        .unwrap();
        crate::records::supply::append_run_entry(&self.root, run, &mut entry).unwrap();
        crate::records::supply::run_log(&self.root, run).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

fn rec(home: &str, run: &str, thread: &str) -> Value {
    json!({"kind":"conversation_index","session":"original-session","home":home,"threadId":thread,"project":"historical-project","tags":[{"owner":crate::run_restart::RUN_TAG_OWNER,"value":run,"seq":1}],"lastLoadedGeneration":crate::recovery::generation_ref(&json!({"home":"original-home","appSession":"original-session","spawnCounter":1})).unwrap()})
}

fn pointer_row(f: &Fixture, turn: &str, client: &str) -> Value {
    let mut row = rec("H-acct", &f.run, "thread:historical");
    let generation =
        crate::recovery::generation_from_ref(row["lastLoadedGeneration"].as_str().unwrap())
            .unwrap();
    let value = json!({"version":1,"run":f.run,"conversation":"thread:historical","run_text_ref":f.start,"purpose":"run start","generation":generation,"turn":turn,"client_user_message_id":client});
    row["tags"].as_array_mut().unwrap().push(
        json!({"owner":crate::workflow_learning_pointers::OWNER,"value":value.to_string(),"seq":2}),
    );
    row
}

#[test]
fn historical_learning_original_ack_pointer_supplies_coordinates_without_a_saved_check() {
    let f = Fixture::new();
    let path = f.folder.join(format!(
        "{}.json",
        f.check.strip_prefix("wr-record:v1:").unwrap()
    ));
    std::fs::remove_file(path).unwrap();
    let rows = vec![pointer_row(
        &f,
        "native-original-turn",
        "native-original-client",
    )];
    let run = HistoricalRun::read_with_recovery(&f.project, &f.run, &rows).unwrap();
    assert_eq!(run.start.turn, "native-original-turn");
    assert!(run.start.checks.is_empty());
    assert_eq!(run.start.recovery_pointers.len(), 1);
    run.recheck_with_recovery(&f.project, &rows).unwrap();
    assert!(run
        .recheck_with_recovery(&f.project, &[rec("H-acct", &f.run, "thread:historical")])
        .is_err());
}

#[test]
fn historical_learning_ack_pointer_conflicting_with_check_or_original_rec_generation_is_refused() {
    let f = Fixture::new();
    let rows = vec![pointer_row(&f, "different-turn", "different-client")];
    assert!(HistoricalRun::read_with_recovery(&f.project, &f.run, &rows)
        .err()
        .unwrap()
        .contains("conflicting original turn/client"));
    let mut row = pointer_row(&f, "turn-B1", "cum:run:thr-40/2");
    row["session"] = json!("different-session");
    assert!(
        HistoricalRun::read_with_recovery(&f.project, &f.run, &[row])
            .err()
            .unwrap()
            .contains("original native pointer app-session occurrence")
    );
}

#[test]
fn historical_learning_new_ack_keeps_old_execution_index_and_later_inherited_tag_copies() {
    let f = Fixture::new();
    let path = f.folder.join(format!(
        "{}.json",
        f.check.strip_prefix("wr-record:v1:").unwrap()
    ));
    std::fs::remove_file(path).unwrap();
    let mut row = pointer_row(&f, "restarted-native-turn", "restarted-native-client");
    let mut pointer: Value =
        serde_json::from_str(row["tags"][1]["value"].as_str().unwrap()).unwrap();
    pointer["generation"]["appSession"] = json!("restarted-session");
    pointer["generation"]["spawnCounter"] = json!(2);
    row["tags"][1]["value"] = json!(pointer.to_string());
    row["session"] = json!("restarted-session");
    // The producer intentionally does not reclassify historical execution.
    assert_ne!(
        row["lastLoadedGeneration"],
        crate::recovery::generation_ref(&pointer["generation"]).unwrap()
    );
    let mut later = row.clone();
    later["session"] = json!("still-later-session");
    let run = HistoricalRun::read_with_recovery(&f.project, &f.run, &[row.clone(), later.clone()])
        .unwrap();
    assert_eq!(run.start.turn, "restarted-native-turn");
    run.recheck_with_recovery(&f.project, &[row, later])
        .unwrap();
}

#[test]
fn historical_learning_reads_unique_original_records_without_creating_live_authority_or_rewriting()
{
    let f = Fixture::new();
    let before = Snapshot::read(&f.project).unwrap().files;
    let run = f.read().unwrap();
    assert_eq!(run.run, f.run);
    assert_eq!(run.conversation, "thread:historical");
    assert_eq!(run.start.turn, "turn-B1");
    assert_eq!(run.start.client_message, "cum:run:thr-40/2");
    assert!(!run.recorded_ended);
    assert!(run.end.is_none());
    assert_eq!(
        run.workflow,
        f.project.resolve(&f.start).unwrap().body()["workflow"]
    );
    assert!(run.limits.iter().any(|l| l.contains("no live run")));
    run.recheck(&f.project).unwrap();
    assert_eq!(Snapshot::read(&f.project).unwrap().files, before);
    let home = run
        .source_home(&[rec("H-acct", &f.run, &run.conversation)], &[])
        .unwrap();
    assert_eq!(home.home_class, "H-acct");
    assert_eq!(
        home.recorded_generations[0]["appSession"],
        "original-session"
    );
}

#[test]
fn historical_learning_rejects_duplicate_starts_and_full_selection_tuple_conflicts() {
    let f = Fixture::new();
    let start = f.project.resolve(&f.start).unwrap();
    f.wr(start.body().clone(), &[f.selection.clone()]);
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("duplicate or conflicting WR run starts"));
    let f = Fixture::new();
    f.change(&f.selection, |e| {
        e["body"]["identity"]["source_root"] = json!("different full slot")
    });
    assert!(f.read().is_err());
    let f = Fixture::new();
    let mut conflict = f.project.resolve(&f.selection).unwrap().body().clone();
    conflict["identity"]["source_root"] = json!("another full slot with the same selection ID");
    f.wr(conflict, &[]);
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("conflicting original selection identity"));
}

#[test]
fn historical_learning_rejects_conflicting_original_check_coordinates_and_duplicate_ids() {
    let f = Fixture::new();
    let mut check = f.project.resolve(&f.check).unwrap().body().clone();
    check["check"] = json!("check:other");
    check["turn"] = json!("other-turn");
    f.wr(check, &[f.start.clone()]);
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("conflicting original turn/client"));
    let f = Fixture::new();
    f.wr(
        f.project.resolve(&f.check).unwrap().body().clone(),
        &[f.start.clone()],
    );
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("duplicate supply-check identity"));
}

#[test]
fn historical_learning_refuses_rs_supply_that_disagrees_with_original_wr_correspondence() {
    let f = Fixture::new();
    let start = f.project.resolve(&f.start).unwrap();
    let check = f.project.resolve(&f.check).unwrap();
    let joined = crate::records::supply::correspond(&f.project, &start, &check).unwrap();
    f.rs("supplied_guidance", joined.recorded_claim().clone());
    f.read().unwrap();
    let mut wrong = joined.recorded_claim().clone();
    wrong["sourceIdentity"] = json!("different full workflow tuple");
    f.rs("supplied_guidance", wrong);
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("RS workflow supply disagrees"));
    // Version comparison keeps its separate, strictly recorded metadata path.
    HistoricalVersion::read(&f.project, &f.run).unwrap();
}

#[test]
fn historical_learning_requires_exact_closed_run_boundary_and_its_original_correspondence() {
    let f = Fixture::new();
    f.ended();
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("no exact acknowledged native end boundary"));
    f.notice();
    let run = f.read().unwrap();
    assert!(run.recorded_ended);
    assert_eq!(run.end.as_ref().unwrap().turn, "turn:end");
    let mut check = f.project.resolve(&f.check).unwrap().body().clone();
    check["check"] = json!("check:refusal");
    check["state"] = json!("not found");
    f.wr(check, &[f.start.clone()]);
    let read = f.read().unwrap();
    assert!(read.limits.iter().any(|l| l.contains("recorded not found")));
}

#[test]
fn historical_learning_keeps_original_notice_and_later_following_start_for_native_order_selection()
{
    let f = Fixture::new();
    f.ended();
    f.notice();
    f.following();
    let run = f.read().unwrap();
    assert!(run.recorded_ended);
    assert!(run.end.is_none());
    assert_eq!(run.end_candidates.len(), 2);
    assert!(run
        .end_candidates
        .iter()
        .any(|end| end.kind == "run end notice"));
    assert!(run
        .end_candidates
        .iter()
        .any(|end| end.kind == "following run start"));
}

#[test]
fn historical_learning_following_start_must_belong_to_its_original_run_writer_log() {
    let f = Fixture::new();
    f.ended();
    let log = f.following();
    let moved = log.with_file_name("different-writer.jsonl");
    std::fs::rename(log, moved).unwrap();
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("following opening is outside its original App workflow log"));
}

#[test]
fn historical_learning_missing_original_check_is_unavailable_evidence_not_a_new_human_act_rule() {
    let f = Fixture::new();
    let path = f.folder.join(format!(
        "{}.json",
        f.check.strip_prefix("wr-record:v1:").unwrap()
    ));
    std::fs::remove_file(path).unwrap();
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("original acknowledged turn/check boundary is unavailable"));
    let version = HistoricalVersion::read(&f.project, &f.run).unwrap();
    assert_eq!(
        version.workflow,
        f.project.resolve(&f.start).unwrap().body()["workflow"]
    );
    version.recheck(&f.project).unwrap();
}

#[test]
fn historical_learning_early_not_found_does_not_poison_later_agreeing_native_check() {
    let f = Fixture::new();
    let mut later = f.project.resolve(&f.check).unwrap().body().clone();
    f.change(&f.check, |e| e["body"]["state"] = json!("not found"));
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("only not-found checks survived"));
    later["check"] = json!("later-check");
    later["read_at"] = json!("later");
    f.wr(later, &[f.start.clone()]);
    let run = f.read().unwrap();
    assert_eq!(run.start.turn, "turn-B1");
    assert_eq!(run.start.checks.len(), 2);
    assert!(run.limits.iter().any(|l| l.contains("recorded not found")));
}

#[test]
fn historical_learning_keeps_nonverified_original_findings_distinct_from_positive_boundary_correlation(
) {
    let f = Fixture::new();
    let original = f.project.resolve(&f.check).unwrap().body().clone();
    let states = [
        "text differs, workflow bytes equal",
        "text differs, workflow bytes differ",
        "incomparable",
        "unreadable",
    ];
    for (index, state) in states.iter().enumerate() {
        let mut prior = original.clone();
        prior["check"] = json!(format!("prior-check-{index}"));
        prior["state"] = json!(state);
        prior["read_at"] = json!(format!("prior-read-{index}"));
        prior["evidence_limits"] = json!([format!("original cause-{index}")]);
        if *state == "incomparable" {
            prior["observed_text"]["method"] = json!("another historical text method");
        } else if state.starts_with("text differs") {
            prior["observed_text"]["value"] = json!("a".repeat(64));
        } else {
            for field in ["observed_text", "item", "located_by"] {
                prior.as_object_mut().unwrap().remove(field);
            }
        }
        f.wr(prior, &[f.start.clone()]);
    }
    let row = pointer_row(&f, "turn-B1", "cum:run:thr-40/2");
    let run = HistoricalRun::read_with_recovery(&f.project, &f.run, &[row]).unwrap();
    assert_eq!(run.start.turn, "turn-B1");
    assert_eq!(run.start.checks.len(), 5);
    for (index, state) in states.iter().enumerate() {
        assert!(
            run.limits.iter().any(|limit| limit.contains(state)
                && limit.contains(&format!("prior-check-{index}"))
                && limit.contains(&format!("prior-read-{index}"))
                && limit.contains(&format!("original cause-{index}"))
                && limit.contains("separate from fresh native content correlation")),
            "{}",
            run.limits.join("\n")
        );
    }
    assert!(!run
        .limits
        .iter()
        .any(|limit| limit.contains("later agreeing check")));
}

#[test]
fn historical_learning_refuses_duplicate_openings_and_incomplete_rs_instead_of_inferring_end() {
    let f = Fixture::new();
    let (entries, limits) = crate::storage::read_all(&f.root);
    assert!(limits.is_empty());
    f.rs(
        "run_opened",
        entries.iter().find(|e| e["kind"] == "run_opened").unwrap()["body"].clone(),
    );
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("duplicate or conflicting RS run_opened"));
    let f = Fixture::new();
    f.ended();
    f.notice();
    let path = crate::records::supply::run_log(&f.root, &f.run).unwrap();
    use std::io::Write;
    std::fs::OpenOptions::new()
        .append(true)
        .open(path)
        .unwrap()
        .write_all(b"{")
        .unwrap();
    assert!(f
        .read()
        .err()
        .unwrap()
        .contains("RS record set is incomplete"));
}

#[test]
fn historical_learning_rechecks_raw_same_byte_file_replacement_and_distinct_project() {
    let f = Fixture::new();
    let run = f.read().unwrap();
    let path = f.folder.join(format!(
        "{}.json",
        f.start.strip_prefix("wr-record:v1:").unwrap()
    ));
    let bytes = std::fs::read(&path).unwrap();
    std::fs::remove_file(&path).unwrap();
    std::fs::write(&path, bytes).unwrap();
    assert!(run.recheck(&f.project).is_err());
    let other = Fixture::new();
    assert!(run.recheck(&other.project).is_err());
}

#[test]
fn historical_learning_ignores_unrelated_ancestor_directory_activity_but_not_source_links() {
    let f = Fixture::new();
    let run = f.read().unwrap();
    let sibling = f
        .root
        .parent()
        .unwrap()
        .join(crate::util::opaque_id("unrelated-sibling-").unwrap());
    std::fs::create_dir(&sibling).unwrap();
    run.recheck(&f.project).unwrap();
    std::fs::remove_dir(sibling).unwrap();
    let path = f.folder.join(format!(
        "{}.json",
        f.start.strip_prefix("wr-record:v1:").unwrap()
    ));
    let moved = path.with_extension("saved");
    std::fs::rename(&path, &moved).unwrap();
    std::os::unix::fs::symlink(&moved, &path).unwrap();
    assert!(run.recheck(&f.project).is_err());
}

#[test]
fn historical_learning_native_home_requires_tag_generation_and_rejects_conflicting_or_absent_evidence(
) {
    let row = rec("H-acct", "run:A", "thread:A");
    assert_eq!(
        source_home_for_run("run:A", "thread:A", &[row.clone()], &[])
            .unwrap()
            .home_class,
        "H-acct"
    );
    let mut untagged = row.clone();
    untagged["tags"] = json!([]);
    assert!(source_home_for_run("run:A", "thread:A", &[untagged], &[]).is_err());
    let mut missing = row.clone();
    missing
        .as_object_mut()
        .unwrap()
        .remove("lastLoadedGeneration");
    assert!(source_home_for_run("run:A", "thread:A", &[missing], &[]).is_err());
    assert!(source_home_for_run("run:A", "thread:A", &[], &[]).is_err());
    assert!(source_home_for_run(
        "run:A",
        "thread:A",
        &[row.clone(), rec("H-key", "run:A", "thread:A")],
        &[]
    )
    .is_err());
    assert!(source_home_for_run(
        "run:A",
        "thread:A",
        &[row.clone(), rec("H-acct", "run:A", "other-thread")],
        &[]
    )
    .is_err());
    assert!(source_home_for_run(
        "run:A",
        "thread:A",
        &[row],
        &[json!({"kind":"app_restart_interruption","threadId":"thread:A","home":"H-key"})]
    )
    .is_err());
}
