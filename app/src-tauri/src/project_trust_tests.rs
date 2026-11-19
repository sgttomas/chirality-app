//! DEL-01-01: the App's trust choice for a project, its file in the records store, the person's acts, and the words.
//! Invented folders in fresh temporary places; the test build's own records store.
use super::*;
use crate::records_store;
use std::io::Write;

fn folder(prefix: &str) -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
    std::fs::create_dir_all(&p).unwrap();
    p.canonicalize().unwrap()
}
/// A project the person set up through the App, with its identity in the store (as the App gives it at launch).
fn set_up(prefix: &str) -> (PathBuf, ProjectTrust) {
    let project = folder(prefix);
    records_store::attach(&project, true).unwrap();
    let trust = ProjectTrust::for_launch(Some(&project), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    (project, trust)
}
fn switches(project: &Path) -> PathBuf {
    records_store::attach(project, false).unwrap().dir.unwrap().join(records_store::TRUST_SWITCHES)
}
fn lines(project: &Path) -> Vec<Value> {
    std::fs::read_to_string(switches(project)).unwrap().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
}
fn choice(trust: &ProjectTrust) -> AppTrust {
    ProjectTrust::choice(&trust.launched().unwrap())
}
/// The person's confirmed switch on, through the native confirmation's stand-in answering "perform".
fn confirmed_on(trust: &ProjectTrust) -> Value {
    let token = trust.preview_on().unwrap()["token"].as_str().unwrap().to_owned();
    trust.confirm_on(&token, |_, _, _| Ok(true)).unwrap()
}

// ---- How a project came to be known, and where the choice applies ----

#[test]
fn a_project_set_up_through_the_app_is_on_and_an_environment_project_has_no_choice() {
    assert_eq!(how_known(crate::desktop_startup::SAVED_REQUEST_SOURCE), Known::SetUpInApp);
    assert_eq!(how_known("explicit environment (exclusive)"), Known::EnvironmentRoute);
    assert_eq!(how_known("explicit Root native environment path inputs"), Known::EnvironmentRoute);
    let (project, trust) = set_up("trust-known-");
    assert_eq!(trust.choice_for(&project), Some(AppTrust::OnBySetup));
    let environment = ProjectTrust::for_launch(Some(&project), "explicit Root native environment path inputs");
    assert_eq!(environment.choice_for(&project), Some(AppTrust::NoChoice));
    // No project, no choice.
    assert!(ProjectTrust::for_launch(None, crate::desktop_startup::SAVED_REQUEST_SOURCE).launched().is_none());
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_choice_applies_only_to_the_projects_own_folder_as_given_or_physical() {
    let base = folder("trust-lookup-");
    let project = base.join("project");
    std::fs::create_dir_all(project.join("sub")).unwrap();
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&project, &alias).unwrap();
    // Known by the link's spelling: the physical spelling is the same project.
    let trust = ProjectTrust::default();
    trust.add(&alias, Known::SetUpInApp);
    assert!(trust.project_for(&alias).is_some() && trust.project_for(&project).is_some());
    // A folder below or above it, or the folder kept for conversations without a project, is not the project.
    for other in [project.join("sub"), base.clone(), folder("trust-no-project-")] {
        assert_eq!(trust.project_for(&other), None, "{}", other.display());
        assert_eq!(trust.choice_for(&other), None);
    }
    std::fs::remove_dir_all(base).unwrap();
}

// ---- The choice file ----

#[test]
fn nothing_is_written_by_default_and_each_switch_writes_one_line() {
    let (project, trust) = set_up("trust-file-");
    let dir = records_store::attach(&project, false).unwrap().dir.unwrap();
    assert_eq!(choice(&trust), AppTrust::OnBySetup);
    let _ = trust.view();
    assert!(!dir.join("trust").exists(), "the default writes nothing; reading and the view write nothing");
    let off = trust.switch_off().unwrap();
    assert_eq!(off["state"], "switched-off");
    assert_eq!(lines(&project).len(), 1);
    let line = &lines(&project)[0];
    assert_eq!(line.as_object().unwrap().len(), 3);
    assert_eq!((line["format"].as_str(), line["trust"].as_str(), line["at"].as_str()), (Some(SWITCH_FORMAT), Some("off"), off["at"].as_str()));
    assert_eq!(choice(&trust), AppTrust::OffBySwitch { at: off["at"].as_str().unwrap().into() });
    let on = confirmed_on(&trust);
    assert_eq!(lines(&project).len(), 2);
    assert_eq!(lines(&project)[1]["trust"], "on");
    assert_eq!(choice(&trust), AppTrust::OnBySwitch { at: on["at"].as_str().unwrap().into() });
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_choice_is_read_to_the_last_complete_line_and_a_torn_tail_is_closed_before_the_next_switch() {
    let (project, trust) = set_up("trust-torn-");
    let off = trust.switch_off().unwrap();
    // An append cut short: an "on" line without its newline is not a switch the person was told of.
    std::fs::OpenOptions::new().append(true).open(switches(&project)).unwrap().write_all(br#"{"format":"chirality.project-trust-switch","at":"x","trust":"on"}"#).unwrap();
    assert_eq!(choice(&trust), AppTrust::OffBySwitch { at: off["at"].as_str().unwrap().into() });
    // The next switch closes and names the fragment first; the file is read whole after it.
    let on = confirmed_on(&trust);
    assert_eq!(choice(&trust), AppTrust::OnBySwitch { at: on["at"].as_str().unwrap().into() });
    let bytes = std::fs::read(switches(&project)).unwrap();
    assert!(bytes.contains(&records_store::lines::MARK), "the fragment was closed with the store's mark");
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn a_damaged_complete_line_hides_the_latest_choice_so_the_choice_is_not_read_and_nothing_is_appended() {
    let (project, trust) = set_up("trust-damaged-");
    trust.switch_off().unwrap();
    std::fs::OpenOptions::new().append(true).open(switches(&project)).unwrap().write_all(b"{\"damaged\n").unwrap();
    assert!(matches!(choice(&trust), AppTrust::NotRead { detail: Some(_) }));
    let before = std::fs::read(switches(&project)).unwrap();
    assert!(trust.switch_off().unwrap_err().starts_with(CANNOT_SWITCH));
    assert_eq!(std::fs::read(switches(&project)).unwrap(), before, "a file not read whole is left as it is");
    assert_eq!(trust.view()["choice"], "not-read");
    assert_eq!(trust.view()["sentence"], CHOICE_NOT_READ);
    // A complete line the App does not write hides the choice too.
    let (other, other_trust) = set_up("trust-foreign-");
    other_trust.switch_off().unwrap();
    std::fs::OpenOptions::new().append(true).open(switches(&other)).unwrap().write_all(b"{\"format\":\"chirality.project-trust-switch\",\"at\":\"x\",\"trust\":\"maybe\"}\n").unwrap();
    assert!(matches!(choice(&other_trust), AppTrust::NotRead { .. }));
    for p in [project, other] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_choice_follows_the_identity_when_the_folder_moves_and_is_adopted_and_a_new_identity_starts_without_it() {
    let (project, trust) = set_up("trust-moved-");
    trust.switch_off().unwrap();
    let moved = project.with_file_name(format!("{}-moved", project.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&project, &moved).unwrap();
    let at_moved = ProjectTrust::for_launch(Some(&moved), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    // Before the person resolves the move, the choice cannot be read: untrusted, never the default.
    assert!(matches!(choice(&at_moved), AppTrust::NotRead { .. }));
    records_store::adopt(&moved).unwrap();
    assert!(matches!(choice(&at_moved), AppTrust::OffBySwitch { .. }), "adopted, the folder has its switches");
    // A new identity has no switches: the project is on by its setup again.
    records_store::new_identity(&moved).unwrap();
    assert_eq!(choice(&at_moved), AppTrust::OnBySetup);
    std::fs::remove_dir_all(moved).unwrap();
}

#[test]
fn a_closed_project_or_one_without_identity_cannot_be_switched_and_says_why() {
    // No identity: nothing can have been switched, so the default stands, and no switch can be written.
    let bare = folder("trust-bare-");
    let trust = ProjectTrust::for_launch(Some(&bare), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    assert_eq!(choice(&trust), AppTrust::OnBySetup);
    for refused in [trust.switch_off().unwrap_err(), trust.preview_on().unwrap_err()] {
        assert!(refused.starts_with(CANNOT_SWITCH), "{refused}");
    }
    let view = trust.view();
    assert_eq!((view["canSwitch"].clone(), view["cannotSwitch"].clone(), view["offers"].clone()), (json!(false), json!(CANNOT_SWITCH), json!([])));
    assert!(!bare.join(".chirality").exists(), "no identity is minted by a switch");
    // Closed: the store refuses the write.
    let (project, trust) = set_up("trust-closed-");
    crate::records::append_project(&project, None, "app-writer:fixture", "evidence_limit", &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"invented trust fixture"})).unwrap();
    let actor = crate::act_control::person(Some("Invented fixture person"), Some("invented-fixture-os"));
    let observed = json!({"fixture":"invented; no live person's act"});
    let plan = crate::records_retention::prepare(&project, "close", None, &actor, &observed).unwrap();
    crate::records_retention::apply(plan, &actor, &observed).unwrap();
    assert!(trust.switch_off().unwrap_err().starts_with(CANNOT_SWITCH));
    assert!(trust.preview_on().unwrap_err().starts_with(CANNOT_SWITCH));
    assert_eq!(trust.view()["canSwitch"], false);
    assert!(!switches(&project).exists());
    for p in [bare, project] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_store_carries_the_switches_in_its_census_and_export() {
    let (project, trust) = set_up("trust-census-");
    trust.switch_off().unwrap();
    let dir = records_store::attach(&project, false).unwrap().dir.unwrap();
    let census = records_store::payload::census(&dir).unwrap();
    assert!(census.members.contains_key(records_store::TRUST_SWITCHES), "{:?}", census.members.keys().collect::<Vec<_>>());
    // Routing knows the folder: a store holding only it is not "unknown".
    assert!(records_store::payload::holds_records(&dir).is_ok());
    std::fs::remove_dir_all(project).unwrap();
}

// ---- The acts ----

#[test]
fn switching_on_takes_the_open_previews_token_once_and_the_native_confirmation() {
    let (project, trust) = set_up("trust-acts-");
    trust.switch_off().unwrap();
    let count = || lines(&project).len();
    // Declined at the native confirmation: nothing written, and the token is spent.
    let preview = trust.preview_on().unwrap();
    assert_eq!((preview["perform"].as_str(), preview["decline"].as_str()), (Some(PERFORM), Some(DECLINE)));
    let token = preview["token"].as_str().unwrap().to_owned();
    let mut shown = None;
    let declined = trust.confirm_on(&token, |statement, decline, perform| { shown = Some((statement.text.clone(), decline.to_owned(), perform.to_owned())); Ok(false) }).unwrap();
    assert_eq!(declined["state"], "cancelled; trust not switched on");
    assert_eq!(count(), 1);
    let (text, decline, perform) = shown.unwrap();
    assert!(text.contains(EFFECTS_TEXT), "the confirmation shows the whole effects text: {text}");
    assert!(text.contains(TAKES_EFFECT));
    assert_eq!((decline.as_str(), perform.as_str()), (DECLINE, PERFORM));
    // Replay of a spent token, and a token never issued: refused without asking.
    for token in [token.as_str(), "project-trust-on-invented"] {
        assert!(trust.confirm_on(token, |_, _, _| panic!("no confirmation is shown for a token that is not the open one")).is_err());
    }
    assert_eq!(count(), 1);
    // The content changes while the confirmation is open (the project's folder becomes a repository's top and so
    // stays its own root, but a folder above it becomes one): nothing written.
    let token = trust.preview_on().unwrap()["token"].as_str().unwrap().to_owned();
    let above = project.parent().unwrap().join(".git");
    assert!(!above.exists(), "the fixture's parent is no repository");
    let inner = project.join("inner");
    std::fs::create_dir_all(&inner).unwrap();
    let moved_trust = ProjectTrust::for_launch(Some(&inner), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    records_store::attach(&inner, true).unwrap();
    let token_inner = moved_trust.preview_on().unwrap()["token"].as_str().unwrap().to_owned();
    *moved_trust.after_confirmation.lock().unwrap() = Some(Box::new({
        let repo = project.join(".git");
        move || { std::fs::create_dir_all(&repo).unwrap(); std::fs::write(repo.join("HEAD"), b"ref: refs/heads/main\n").unwrap(); }
    }));
    let refused = moved_trust.confirm_on(&token_inner, |_, _, _| Ok(true)).unwrap_err();
    assert!(refused.contains("changed during the confirmation"), "{refused}");
    assert!(!switches(&inner).exists(), "nothing written");
    std::fs::remove_dir_all(project.join(".git")).unwrap();
    // The open preview of the project itself, confirmed: one "on" line.
    let confirmed = trust.confirm_on(&token, |_, _, _| Ok(true)).unwrap();
    assert_eq!(confirmed["state"], "switched-on");
    assert_eq!(count(), 2);
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn a_preview_whose_effects_changed_is_refused_before_any_confirmation() {
    let base = folder("trust-changed-");
    let project = base.join("project");
    std::fs::create_dir_all(&project).unwrap();
    records_store::attach(&project, true).unwrap();
    let trust = ProjectTrust::for_launch(Some(&project), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    let token = trust.preview_on().unwrap()["token"].as_str().unwrap().to_owned();
    // The project's folder is now inside a repository: what trust turns on changed.
    std::fs::create_dir_all(base.join(".git")).unwrap();
    std::fs::write(base.join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap();
    let refused = trust.confirm_on(&token, |_, _, _| panic!("no confirmation for a changed preview")).unwrap_err();
    assert!(refused.contains("changed since the preview"), "{refused}");
    assert!(!switches(&project).exists());
    // A fresh preview shows the repository sentence; confirmed, it is written.
    let preview = trust.preview_on().unwrap();
    assert_eq!(preview["content"]["effects"]["insideRepository"]["root"], json!(base.to_string_lossy()));
    let mut shown = String::new();
    trust.confirm_on(preview["token"].as_str().unwrap(), |s, _, _| { shown = s.text.clone(); Ok(true) }).unwrap();
    assert!(shown.contains(&format!("{INSIDE_REPOSITORY_BEFORE}{}{INSIDE_REPOSITORY_AFTER}", base.to_string_lossy())));
    assert_eq!(lines(&project).len(), 1);
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn switching_off_is_immediate_with_no_confirmation() {
    let (project, trust) = set_up("trust-off-");
    let off = trust.switch_off().unwrap();
    assert_eq!((off["state"].as_str(), off["takesEffect"].as_str(), off["running"].as_str()), (Some("switched-off"), Some(TAKES_EFFECT), Some(RUNNING_UNCHANGED)));
    assert_eq!(off["view"]["choice"], "off");
    std::fs::remove_dir_all(project).unwrap();
}

/// No route from the web view or from an agent switches trust on without the native confirmation: the one
/// writer of an "on" line is `confirm_on`, reached only after its `confirm` answered "perform", and the App's one
/// caller of `confirm_on` is the command that passes the native confirmation.
#[test]
fn no_route_switches_trust_on_without_the_native_confirmation() {
    let own = include_str!("project_trust.rs");
    let product = own.split("#[cfg(test)]\n#[path").next().unwrap();
    assert_eq!(product.matches("self.write(").count(), 2, "one write for on, one for off");
    let on_write = product.find("self.write(&project, true)").expect("the one on write");
    let confirm = product.find("pub(crate) fn confirm_on(").unwrap();
    let after_confirm = product[confirm..].find("if !confirm(statement, DECLINE, PERFORM)?").map(|i| i + confirm).unwrap();
    let next_fn = product[confirm + 1..].find("pub(crate) fn ").map(|i| i + confirm + 1).unwrap();
    assert!(after_confirm < on_write && on_write < next_fn, "the on write follows the confirmation, inside confirm_on");
    assert!(!product.contains("self.write(&project, on)") && !product.contains("\"trust\": \"on\""));
    // Outside the module: the store's appender is called only here, and confirm_on only by the native command.
    let base = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    for entry in std::fs::read_dir(&base).unwrap() {
        let path = entry.unwrap().path();
        let name = path.file_name().unwrap().to_string_lossy().into_owned();
        if !name.ends_with(".rs") || name.ends_with("_tests.rs") { continue; }
        let text = std::fs::read_to_string(&path).unwrap();
        let text = text.split("#[cfg(test)]\nmod tests").next().unwrap();
        let appends = text.matches("append_trust_switch(").count();
        match name.as_str() {
            "records_store.rs" => assert_eq!(appends, 1, "its definition"),
            "project_trust.rs" => assert_eq!(appends, 1, "the one writer"),
            _ => assert_eq!(appends, 0, "{name} appends a trust switch"),
        }
        let confirms = text.matches(".confirm_on(").count();
        if name == "lib.rs" {
            assert_eq!(confirms, 1);
            let at = text.find(".confirm_on(").unwrap();
            let command = &text[text[..at].rfind("fn project_trust_confirm_on(").expect("the command")..at + 400];
            assert!(command.contains("confirm_choice(&app,project_trust::TITLE,Ok(statement),decline,perform,&mut refused)"), "{command}");
        } else {
            assert_eq!(confirms, 0, "{name} calls confirm_on");
        }
    }
}

// ---- The words ----

#[test]
fn the_effects_text_is_whole_in_the_confirmation_content_and_the_view() {
    let (project, trust) = set_up("trust-words-");
    let view = trust.view();
    assert_eq!(view["choice"], "on");
    assert_eq!(view["why"], "set-up");
    assert_eq!(view["sentence"], CHOICE_ON_BY_SETUP);
    assert_eq!(view["effects"]["text"], EFFECTS_TEXT);
    assert_eq!(view["effects"]["insideRepository"], Value::Null, "the project is its own root");
    assert_eq!(view["takesEffect"], "A change applies from the next conversation you start, continue or fork.");
    assert_eq!(view["offers"], json!(["switch-off"]));
    let preview = trust.preview_on().unwrap();
    assert_eq!(preview["content"]["effects"]["text"], EFFECTS_TEXT);
    // Off: the view says when, offers switching on, and shows no effects as in force.
    let off = trust.switch_off().unwrap();
    let view = trust.view();
    assert_eq!(view["sentence"], format!("{CHOICE_OFF_BY_SWITCH_PREFIX}{}.", off["at"].as_str().unwrap()));
    assert_eq!((view["effects"].clone(), view["offers"].clone()), (Value::Null, json!(["switch-on"])));
    // Environment route, never switched: no choice, said so. (A switch, once made, applies on either route.)
    let opened = folder("trust-words-environment-");
    let environment = ProjectTrust::for_launch(Some(&opened), "explicit Root native environment path inputs");
    assert_eq!(environment.view()["sentence"], CHOICE_NONE);
    let switched = ProjectTrust::for_launch(Some(&project), "explicit Root native environment path inputs");
    assert_eq!(switched.view()["choice"], "off");
    for p in [project, opened] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_repository_sentence_appears_only_where_the_root_codex_computes_is_not_the_projects_folder() {
    let own = folder("trust-own-root-");
    assert_eq!(inside_repository(&own), None);
    assert_eq!(effects_for(&own)["insideRepository"], Value::Null);
    std::fs::create_dir_all(own.join(".git")).unwrap();
    std::fs::write(own.join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap();
    assert_eq!(inside_repository(&own), None, "a project at its repository's top is its own root");
    let below = own.join("a").join("b");
    std::fs::create_dir_all(&below).unwrap();
    let sentence = inside_repository(&below).unwrap();
    assert_eq!(sentence, json!({"before": INSIDE_REPOSITORY_BEFORE, "root": own.to_string_lossy(), "after": INSIDE_REPOSITORY_AFTER, "standing": "The folder is supplied text."}));
    assert_eq!(cl::project_root(&below), own, "the same function the trust entry uses");
    assert_eq!(format!("{INSIDE_REPOSITORY_BEFORE}<root>{INSIDE_REPOSITORY_AFTER}"),
        "This project's folder is inside the Git repository at <root>. Trust is sent for that repository's top folder, so Codex also loads the AGENTS.md files and .codex settings in the folders between it and this one.");
    std::fs::remove_dir_all(own).unwrap();
}

#[test]
fn the_effects_text_is_the_owners_words() {
    assert_eq!(EFFECTS_TEXT, "Chirality sends this project to Codex as trusted. Codex then loads the project's own instructions (AGENTS.md) and its own Codex settings (the .codex folder in the project). With them:\n- MCP servers that the project's settings name are started on this Mac when a conversation starts, outside the sandbox.\n- The project's shell environment applies to every command the agent runs, and a start-up file of the project's own runs inside each command, under the same access level as that command.\n- The project's rules can let commands run outside the sandbox without asking you.\n- If Codex cannot load the project's settings file, no new conversation starts in this project until the file is fixed or trust is switched off.\nYou can switch trust off for this project in Chirality at any time.");
    assert!(ns::bounded("project trust", format!("{EFFECTS_TEXT}\n{INSIDE_REPOSITORY_BEFORE}/a/b{INSIDE_REPOSITORY_AFTER}\n{TAKES_EFFECT} {RUNNING_UNCHANGED}")).is_ok(), "the whole text fits the native confirmation");
}

// ---- A run with no records store ----

#[test]
fn with_no_records_store_the_environment_route_has_no_choice_and_the_setup_route_is_not_readable() {
    let project = folder("trust-no-store-");
    records_store::use_store_for_test(Some(Err("no records store configured (invented)".into())));
    let environment = ProjectTrust::for_launch(Some(&project), "explicit Root native environment path inputs");
    assert_eq!(choice(&environment), AppTrust::NoChoice, "the environment route behaves as before");
    assert_eq!(environment.view()["sentence"], CHOICE_NONE);
    let set_up = ProjectTrust::for_launch(Some(&project), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    assert!(matches!(choice(&set_up), AppTrust::NotRead { detail: Some(_) }), "the setup route stays fail closed");
    assert_eq!(set_up.view()["sentence"], CHOICE_NOT_READ);
    let mut reading = cl::TrustReading::not_read(project.clone(), cl::TRUST_READ_FAILED, None);
    reading.case = cl::TrustCase::Unmarked;
    reading.choice = Some(choice(&set_up));
    assert_eq!(reading.status()["lines"], json!([cl::TRUST_CHOICE_NOT_READ]));
    records_store::use_store_for_test(None);
    std::fs::remove_dir_all(project).unwrap();
}

// ---- The store's acts on a project with switches: package, disposal, legal hold ----

/// A project with a record and its switches in a store of its own, and the person's native-act stand-ins.
struct Retained {
    project: PathBuf,
    store: PathBuf,
    output: PathBuf,
    actor: Value,
    observed: Value,
}
impl Retained {
    fn new() -> (Self, ProjectTrust) {
        let r = Retained { project: folder("trust-retained-project-"), store: folder("trust-retained-store-"), output: folder("trust-retained-output-"),
            actor: crate::act_control::person(Some("Invented fixture person"), Some("invented-fixture-os")),
            observed: json!({"fixture":"invented; no live person's act"}) };
        records_store::use_store_for_test(Some(Ok(records_store::Store { root: r.store.clone(), placement: records_store::Placement::Test, limits: vec![] })));
        crate::records::append_project(&r.project, None, "app-writer:fixture", "evidence_limit", &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented trust fixture"})).unwrap();
        let trust = ProjectTrust::for_launch(Some(&r.project), crate::desktop_startup::SAVED_REQUEST_SOURCE);
        (r, trust)
    }
    fn act(&self, action: &str, bag: Option<&Path>) -> Result<Value, String> {
        let plan = crate::records_retention::prepare(&self.project, action, bag, &self.actor, &self.observed)?;
        crate::records_retention::apply(plan, &self.actor, &self.observed)
    }
    fn export(&self, name: &str) -> PathBuf {
        let bag = self.output.join(name);
        crate::records_export::export(&self.project, &bag).unwrap();
        bag
    }
}
impl Drop for Retained {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        for p in [&self.project, &self.store, &self.output] { let _ = std::fs::remove_dir_all(p); }
    }
}

#[test]
fn a_package_export_then_import_carries_the_switches_and_the_choice_reads_the_same() {
    let (r, trust) = Retained::new();
    let off = trust.switch_off().unwrap();
    let before = choice(&trust);
    assert_eq!(before, AppTrust::OffBySwitch { at: off["at"].as_str().unwrap().into() });
    let bag = r.export("with-switches");
    assert!(bag.join("payload").join(records_store::TRUST_SWITCHES).is_file() || walk_has(&bag, "switches.jsonl"), "the export carries the switch file");
    let bytes = std::fs::read(switches(&r.project)).unwrap();
    // Into another store.
    records_store::use_store_for_test(Some(Ok(records_store::Store { root: r.output.join("destination-store"), placement: records_store::Placement::Test, limits: vec![] })));
    let plan = records_store::package::prepare(&r.project, &bag, &r.actor, &r.observed).unwrap();
    records_store::package::apply(plan, &r.actor, &r.observed).unwrap();
    assert_eq!(std::fs::read(switches(&r.project)).unwrap(), bytes, "the switch file is imported byte for byte");
    assert_eq!(choice(&trust), before, "the choice reads the same after import");
}
fn walk_has(dir: &Path, name: &str) -> bool {
    std::fs::read_dir(dir).unwrap().flatten().any(|e| {
        let p = e.path();
        if p.is_dir() { walk_has(&p, name) } else { p.file_name().is_some_and(|n| n == name) }
    })
}

#[test]
fn disposal_removes_the_switches_and_the_entry_is_untrusted_with_the_not_readable_sentence() {
    let (r, trust) = Retained::new();
    trust.switch_off().unwrap();
    let file = switches(&r.project);
    r.act("close", None).unwrap();
    let bag = r.export("before-disposal");
    assert_eq!(r.act("dispose", Some(&bag)).unwrap()["state"], "disposed");
    assert!(!file.exists(), "disposal removes the switch file with the payload");
    // The identity stands and its records are disposed: the choice is not readable, never the setup default.
    let after = choice(&trust);
    assert!(matches!(after, AppTrust::NotRead { .. }), "{after:?}");
    let mut reading = cl::TrustReading::not_read(r.project.clone(), cl::TRUST_READ_FAILED, None);
    reading.case = cl::TrustCase::Trusted { key: r.project.to_string_lossy().into_owned() };
    reading.choice = Some(after);
    assert_eq!((reading.trust_level(), reading.status()["lines"].clone()), ("untrusted", json!([cl::TRUST_CHOICE_NOT_READ])));
    assert_eq!(trust.view()["sentence"], CHOICE_NOT_READ);
    assert!(trust.switch_off().unwrap_err().starts_with(CANNOT_SWITCH));
}

#[test]
fn a_legal_hold_does_not_prevent_a_switch() {
    let (r, trust) = Retained::new();
    r.act("set-hold", None).unwrap();
    assert_eq!(trust.view()["canSwitch"], true);
    trust.switch_off().unwrap();
    confirmed_on(&trust);
    assert_eq!(lines(&r.project).len(), 2, "both switches are written under the hold");
    assert!(matches!(choice(&trust), AppTrust::OnBySwitch { .. }));
}
