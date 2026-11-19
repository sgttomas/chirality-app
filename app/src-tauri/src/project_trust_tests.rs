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
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
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
    let off = trust.switch_off_launched().unwrap();
    assert_eq!(off["state"], "switched-off");
    assert_eq!(lines(&project).len(), 1);
    let line = &lines(&project)[0];
    assert_eq!(line.as_object().unwrap().len(), 5, "format, at, trust, and the store and project identities it was written under");
    let attached = records_store::attach(&project, false).unwrap();
    assert_eq!(line["projectId"].as_str(), attached.project.as_deref());
    assert_eq!(line["storeId"].as_str(), Some(records_store::opened_existing().unwrap().1.as_str()));
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
    let off = trust.switch_off_launched().unwrap();
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
    trust.switch_off_launched().unwrap();
    std::fs::OpenOptions::new().append(true).open(switches(&project)).unwrap().write_all(b"{\"damaged\n").unwrap();
    assert!(matches!(choice(&trust), AppTrust::NotRead { detail: Some(_) }));
    let before = std::fs::read(switches(&project)).unwrap();
    assert!(trust.switch_off_launched().unwrap_err().starts_with(CANNOT_SWITCH));
    assert_eq!(std::fs::read(switches(&project)).unwrap(), before, "a file not read whole is left as it is");
    assert_eq!(trust.view()["choice"], "not-read");
    assert_eq!(trust.view()["sentence"], CHOICE_NOT_READ);
    // A complete line the App does not write hides the choice too.
    let (other, other_trust) = set_up("trust-foreign-");
    other_trust.switch_off_launched().unwrap();
    std::fs::OpenOptions::new().append(true).open(switches(&other)).unwrap().write_all(b"{\"format\":\"chirality.project-trust-switch\",\"at\":\"x\",\"trust\":\"maybe\"}\n").unwrap();
    assert!(matches!(choice(&other_trust), AppTrust::NotRead { .. }));
    for p in [project, other] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_choice_follows_the_identity_when_the_folder_moves_and_is_adopted_and_a_new_identity_starts_without_it() {
    let (project, trust) = set_up("trust-moved-");
    trust.switch_off_launched().unwrap();
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
    for refused in [trust.switch_off_launched().unwrap_err(), trust.preview_on_launched().unwrap_err()] {
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
    assert!(trust.switch_off_launched().unwrap_err().starts_with(CANNOT_SWITCH));
    assert!(trust.preview_on_launched().unwrap_err().starts_with(CANNOT_SWITCH));
    assert_eq!(trust.view()["canSwitch"], false);
    assert!(!switches(&project).exists());
    for p in [bare, project] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_store_carries_the_switches_in_its_census_and_export() {
    let (project, trust) = set_up("trust-census-");
    trust.switch_off_launched().unwrap();
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
    trust.switch_off_launched().unwrap();
    let count = || lines(&project).len();
    // Declined at the native confirmation: nothing written, and the token is spent.
    let preview = trust.preview_on_launched().unwrap();
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
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    let above = project.parent().unwrap().join(".git");
    assert!(!above.exists(), "the fixture's parent is no repository");
    let inner = project.join("inner");
    std::fs::create_dir_all(&inner).unwrap();
    let moved_trust = ProjectTrust::for_launch(Some(&inner), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    records_store::attach(&inner, true).unwrap();
    let token_inner = moved_trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    *moved_trust.after_confirmation.lock().unwrap() = Some(Box::new({
        let repo = project.join(".git");
        move || { std::fs::create_dir_all(&repo).unwrap(); std::fs::write(repo.join("HEAD"), b"ref: refs/heads/main\n").unwrap(); }
    }));
    let refused = moved_trust.confirm_on(&token_inner, |_, _, _| Ok(true)).unwrap_err();
    assert_eq!(refused, CHANGED_WHILE_OPEN);
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
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    // The project's folder is now inside a repository: what trust turns on changed.
    std::fs::create_dir_all(base.join(".git")).unwrap();
    std::fs::write(base.join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap();
    let refused = trust.confirm_on(&token, |_, _, _| panic!("no confirmation for a changed preview")).unwrap_err();
    assert!(refused.contains("changed since the preview"), "{refused}");
    assert!(!switches(&project).exists());
    // A fresh preview shows the repository sentence; confirmed, it is written.
    let preview = trust.preview_on_launched().unwrap();
    assert_eq!(preview["content"]["effects"]["insideRepository"]["root"], json!(base.to_string_lossy()));
    let mut shown = String::new();
    // Whole where it fits the native confirmation; otherwise named natively and shown in full, as plain text, in
    // the App.
    trust.confirm_on(preview["token"].as_str().unwrap(), |s, _, _| {
        shown = s.in_app.as_ref().map_or_else(|| s.text.clone(), |c| { assert!(s.text.starts_with(SWITCH_ON_POINTER)); c.content.as_str().unwrap().to_owned() });
        Ok(true)
    }).unwrap();
    assert!(shown.contains(&format!("{INSIDE_REPOSITORY_BEFORE}{}{INSIDE_REPOSITORY_AFTER}", base.to_string_lossy())));
    assert!(shown.contains(EFFECTS_TEXT) && shown.contains(TAKES_EFFECT));
    assert_eq!(lines(&project).len(), 1);
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn switching_off_is_immediate_with_no_confirmation() {
    let (project, trust) = set_up("trust-off-");
    let off = trust.switch_off_launched().unwrap();
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
    let on_write = product.find("self.write(&project, true, Some(&preview))").expect("the one on write, bound to the reviewed preview");
    let confirm = product.find("pub(crate) fn confirm_on(").unwrap();
    let after_confirm = product[confirm..].find("let answer = confirm(statement, DECLINE, PERFORM);").map(|i| i + confirm).unwrap();
    let next_fn = product[confirm + 1..].find("pub(crate) fn ").map(|i| i + confirm + 1).unwrap();
    assert!(after_confirm < on_write && on_write < next_fn, "the on write follows the confirmation, inside confirm_on");
    assert!(!product.contains("self.write(&project, on") && !product.contains("\"trust\": \"on\"") && !product.contains("switch_line(true"));
    assert_eq!(product.matches("switch_line(").count(), 3, "its definition, the write, and the new identity's off line");
    assert!(product.contains("switch_line(false, store, project, Some(NEW_IDENTITY_REASON))"));
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
    assert_eq!(view["takesEffect"], "A change applies to conversations you start, continue or fork after it.");
    assert_eq!(view["offers"], json!(["switch-off"]));
    let preview = trust.preview_on_launched().unwrap();
    assert_eq!(preview["content"]["effects"]["text"], EFFECTS_TEXT);
    // Off: the view says when, offers switching on, and shows no effects as in force.
    let off = trust.switch_off_launched().unwrap();
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
        "This project's folder is inside the Git repository at <root>. A trusted mark is made for that repository's top folder, so Codex then also loads the AGENTS.md files in the folders from there down to this one, and can load .codex settings in those folders.");
    std::fs::remove_dir_all(own).unwrap();
}

#[test]
fn the_words_are_the_agreed_sentences() {
    assert_eq!(WILL_TRUST, "Chirality's trust is on for a project you set up here, unless you have switched it off.");
    assert_eq!(CHOICE_ON_BY_SETUP, "Chirality's choice for this project is on: you set it up in Chirality and have not switched its trust off.");
    assert_eq!(format!("{CHOICE_ON_BY_SWITCH_PREFIX}T."), "Chirality's choice for this project is on: it was switched on at T.");
    assert_eq!(format!("{CHOICE_OFF_BY_SWITCH_PREFIX}T."), "Chirality's choice for this project is off: it was switched off at T.");
    assert_eq!(CHOICE_OFF_BY_NEW_IDENTITY, "Chirality's choice for this project is off: its records say the project was given a new identity, and trust is not carried to a new identity. Switch it on to have Chirality trust the project again.");
    assert_eq!(CHOICE_NOT_READ, "The App could not read its record of this project's trust choice, so Chirality marks a conversation started in this project's folder as untrusted until the record can be read.");
    assert_eq!(CHOICE_FOLDER_CHANGED, "The project's folder is no longer the folder Chirality opened, so Chirality marks a conversation started in it as untrusted.");
    assert_eq!(CHOICE_SETTINGS_CAN_OVERRIDE, "The Codex settings Chirality uses make a conversation untrusted where they mark this project untrusted or cannot be read. What each start sent is shown with the conversation's access level.");
    assert_eq!(NEW_IDENTITY_TRUST_LINE, "Giving this folder a new identity also sets the project's trust off under it, until you switch it on. If Chirality cannot record that, it says so.");
    assert_eq!(format!("{NEW_IDENTITY_NOT_SET_OFF}<reason>"), "The new identity was made, but Chirality could not record its trust as off, so Chirality's trust is on for this project now. You can switch it off in Settings. <reason>");
    assert_eq!(CANNOT_SWITCH, "Trust can be switched only for a project that is open in Chirality with its identity in the App's records store. A closed or disposed project, or one with no identity, cannot be switched, and the records store can refuse a switch; its reason is shown.");
    assert_eq!(setup_trust_pointer("D"), "Chirality's trust is on for a project you set up here, unless you have switched it off. What trust turns on is shown in full in the App now, under \"Content named by an open native confirmation\". Its sha-256 digest: D");
    assert_eq!(SETUP_TRUST_AMONG_EFFECTS, "Chirality's trust is on for a project you set up here, unless you have switched it off; what trust turns on is among the complete effects shown in the App.");
    // The status sentences and the settings-file message.
    assert_eq!(format!("{}T{}", cl::TRUST_ON_BY_SWITCH_PREFIX, cl::TRUST_ON_BY_SWITCH_SUFFIX), "Chirality's choice for this project is on (switched on at T), so the App sent a trusted entry for the project root shown below.");
    assert_eq!(format!("{}T{}", cl::TRUST_OFF_BY_SWITCH_PREFIX, cl::TRUST_OFF_BY_SWITCH_SUFFIX), "Chirality's choice for this project is off (switched off at T), so the App sent an untrusted entry for the project root shown below.");
    assert_eq!(cl::TRUST_OFF_BY_NEW_IDENTITY, "Chirality's choice for this project is off (its records say the project was given a new identity), so the App sent an untrusted entry for the project root shown below.");
    assert_eq!(cl::TRUST_MARK_UNREADABLE, "The App's reading of the Codex settings it uses held a project mark it could not read.");
    assert_eq!(format!("{}T{}", cl::PROJECT_SETTINGS_AT_BEFORE, cl::PROJECT_SETTINGS_AT_AFTER), "At T, Codex could not load its settings, so it did not start the conversation. This project was marked trusted in that request, so one of its own settings files may be the cause.");
    assert_eq!(cl::PROJECT_SETTINGS_FILES, "The project's own settings files Codex may have read:");
    assert_eq!(cl::PROJECT_SETTINGS_REASON, "Codex's reason:");
    assert_eq!(cl::PROJECT_SETTINGS_REMEDY, "You can fix the file, or switch this project's trust off in Chirality, and start the conversation again.");
    assert_eq!(cl::PROJECT_SETTINGS_COMMAND_ERROR, "Codex could not load its settings, so it did not start the conversation. This project was marked trusted in that request, so one of its own settings files may be the cause. See the project's trust in Chirality for the files and Codex's reason.");
}

#[test]
fn the_effects_text_is_the_owners_words() {
    assert_eq!(EFFECTS_TEXT, "While Chirality's trust is on for this project, Chirality marks the project as trusted when it starts, continues or forks a conversation in the project's folder, except in the cases named with the project's trust in Settings. With a trusted mark, Codex loads the project's own instructions (its AGENTS.md files) and its own Codex settings and rules (in the project's .codex folder). With them, the project's own files can:\n- start MCP server programs on this Mac when a conversation starts, outside the sandbox, and have Codex connect to MCP servers at addresses they name;\n- set the shell environment of the commands the agent runs, and through it have a start-up file of the project's own run inside each of those commands, under the same access level as that command;\n- let commands run outside the sandbox without asking you, through the project's rules. Chirality cannot switch that off while the project is trusted;\n- stop new conversations from starting in this project, where Codex cannot load the project's settings file, until the file is fixed or trust is switched off.\nYou can switch trust off for this project in Chirality while the project is open and its records can be written.");
    // With these words the switch-on statement fits the native confirmation whole for a project that is its own
    // root; with the repository sentence it does not, and the confirmation shows the whole text in the App
    // (`a_preview_whose_effects_changed_is_refused_before_any_confirmation` reads either form).
    assert!(ns::bounded("project trust", format!("{EFFECTS_TEXT}\n{TAKES_EFFECT} {RUNNING_UNCHANGED}")).is_ok(), "whole, its own root");
    assert!(ns::bounded("project trust", format!("{EFFECTS_TEXT}\n{INSIDE_REPOSITORY_BEFORE}/a/b{INSIDE_REPOSITORY_AFTER}\n{TAKES_EFFECT} {RUNNING_UNCHANGED}")).is_err(), "in the App, inside a repository");
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
    let off = trust.switch_off_launched().unwrap();
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
    trust.switch_off_launched().unwrap();
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
    assert!(trust.switch_off_launched().unwrap_err().starts_with(CANNOT_SWITCH));
}

#[test]
fn a_legal_hold_does_not_prevent_a_switch() {
    let (r, trust) = Retained::new();
    r.act("set-hold", None).unwrap();
    assert_eq!(trust.view()["canSwitch"], true);
    trust.switch_off_launched().unwrap();
    confirmed_on(&trust);
    assert_eq!(lines(&r.project).len(), 2, "both switches are written under the hold");
    assert!(matches!(choice(&trust), AppTrust::OnBySwitch { .. }));
}

// ---- Repair after the independent review: the persisted choice (B) ----

fn append(project: &Path, line: &str) {
    std::fs::OpenOptions::new().append(true).open(switches(project)).unwrap().write_all(line.as_bytes()).unwrap();
}
fn ids(project: &Path) -> (String, String) {
    (records_store::opened_existing().unwrap().1, records_store::attach(project, false).unwrap().project.unwrap())
}

#[test]
fn every_complete_line_is_validated_so_an_earlier_bad_line_is_not_hidden_by_a_later_valid_one() {
    let (project, trust) = set_up("trust-every-line-");
    trust.switch_off_launched().unwrap();
    // A complete line the App does not write, then a valid one after it, written by hand.
    append(&project, "{\"format\":\"chirality.project-trust-switch\",\"trust\":\"on\"}\n");
    let (store, id) = ids(&project);
    append(&project, &format!("{}\n", json!({"format": SWITCH_FORMAT, "at": "2026-11-19T03:00:00.000Z", "trust": "on", "storeId": store, "projectId": id})));
    assert!(matches!(choice(&trust), AppTrust::NotRead { detail: Some(ref d) } if d.contains("line 2")), "{:?}", choice(&trust));
    // And the appender refuses to add a later line behind it.
    let before = std::fs::read(switches(&project)).unwrap();
    assert!(trust.switch_off_launched().unwrap_err().starts_with(CANNOT_SWITCH));
    assert_eq!(std::fs::read(switches(&project)).unwrap(), before);
    // A line whose time is not an RFC 3339 instant is not one the App writes.
    let (other, other_trust) = set_up("trust-bad-time-");
    other_trust.switch_off_launched().unwrap();
    let (store, id) = ids(&other);
    append(&other, &format!("{}\n", json!({"format": SWITCH_FORMAT, "at": "yesterday", "trust": "off", "storeId": store, "projectId": id})));
    assert!(matches!(choice(&other_trust), AppTrust::NotRead { .. }));
    for p in [project, other] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn an_on_line_made_for_another_store_or_identity_is_passed_over_and_an_off_line_is_honoured_whatever_its_origin() {
    let (project, trust) = set_up("trust-origin-");
    let (store, id) = ids(&project);
    let line = |trust: &str, store: &str, id: &str| format!("{}\n", json!({"format": SWITCH_FORMAT, "at": "2026-11-19T04:00:00.000Z", "trust": trust, "storeId": store, "projectId": id}));
    let dir = switches(&project);
    std::fs::create_dir_all(dir.parent().unwrap()).unwrap();
    // Off here, then an on made in another store, then one made under another identity: both passed over.
    std::fs::write(&dir, format!("{}{}{}", line("off", &store, &id), line("on", "another-store", &id), line("on", &store, "chirality-project:another"))).unwrap();
    assert_eq!(choice(&trust), AppTrust::OffBySwitch { at: "2026-11-19T04:00:00.000Z".into() });
    let view = trust.view();
    assert_eq!((view["choice"].as_str(), view["passedOver"].as_str()), (Some("off"), Some(CHOICE_PASSED_OVER)));
    // With nothing before them, the default stands.
    std::fs::write(&dir, line("on", "another-store", &id)).unwrap();
    assert_eq!(choice(&trust), AppTrust::OnBySetup);
    // An off line from elsewhere is honoured.
    std::fs::write(&dir, line("off", "another-store", "chirality-project:another")).unwrap();
    assert!(matches!(choice(&trust), AppTrust::OffBySwitch { .. }));
    // Made here: honoured.
    std::fs::write(&dir, line("on", &store, &id)).unwrap();
    assert!(matches!(choice(&trust), AppTrust::OnBySwitch { .. }));
    assert!(trust.view()["passedOver"].is_null());
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_revision_changes_with_every_switch_and_with_the_identity() {
    let (project, trust) = set_up("trust-revision-");
    let known = trust.launched().unwrap();
    let first = ProjectTrust::read_choice(&known, None).revision;
    assert_eq!(ProjectTrust::read_choice(&known, None).revision, first, "reading changes nothing");
    trust.switch_off_launched().unwrap();
    let second = ProjectTrust::read_choice(&known, None).revision;
    assert_ne!(first, second);
    confirmed_on(&trust);
    assert_ne!(ProjectTrust::read_choice(&known, None).revision, second);
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn an_absent_trust_folder_is_no_switches_and_an_invalid_one_is_not_read() {
    let (project, trust) = set_up("trust-parent-");
    let dir = records_store::attach(&project, false).unwrap().dir.unwrap();
    assert!(!dir.join("trust").exists());
    assert_eq!(choice(&trust), AppTrust::OnBySetup, "absent: no switches");
    // A link in its place, to a folder with no switch file: not read, never the default.
    let elsewhere = folder("trust-parent-elsewhere-");
    std::os::unix::fs::symlink(&elsewhere, dir.join("trust")).unwrap();
    assert!(matches!(choice(&trust), AppTrust::NotRead { .. }), "{:?}", choice(&trust));
    assert!(trust.switch_off_launched().is_err());
    assert!(!elsewhere.join("switches.jsonl").exists(), "nothing written through the link");
    // A file in its place: not read.
    std::fs::remove_file(dir.join("trust")).unwrap();
    std::fs::write(dir.join("trust"), b"").unwrap();
    assert!(matches!(choice(&trust), AppTrust::NotRead { .. }));
    std::fs::remove_file(dir.join("trust")).unwrap();
    assert_eq!(choice(&trust), AppTrust::OnBySetup);
    for p in [project, elsewhere] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn a_package_imported_into_another_store_carries_an_off_but_not_an_on() {
    for on in [false, true] {
        let (r, trust) = Retained::new();
        trust.switch_off_launched().unwrap();
        if on { confirmed_on(&trust); }
        let before = choice(&trust);
        let bag = r.export("with-switches");
        records_store::use_store_for_test(Some(Ok(records_store::Store { root: r.output.join("destination-store"), placement: records_store::Placement::Test, limits: vec![] })));
        let plan = records_store::package::prepare(&r.project, &bag, &r.actor, &r.observed).unwrap();
        records_store::package::apply(plan, &r.actor, &r.observed).unwrap();
        let after = choice(&trust);
        if on {
            // The on was confirmed in another store: not used here; the line before it (off) stands.
            assert!(matches!(after, AppTrust::OffBySwitch { .. }), "{after:?}");
            assert_eq!(trust.view()["passedOver"], CHOICE_PASSED_OVER);
        } else {
            assert_eq!(after, before, "an off is honoured after import");
        }
    }
}

// ---- Repair after the independent review: the acts (C) ----

#[test]
fn a_switch_off_while_the_confirmation_is_open_invalidates_it_and_a_second_preview_is_refused() {
    let (project, trust) = set_up("trust-open-");
    trust.switch_off_launched().unwrap();
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    let lines_before = lines(&project).len();
    let refused = trust.confirm_on(&token, |_, _, _| {
        // While the native dialog is open: a second preview is refused, and the person switches off.
        assert!(trust.preview_on_launched().unwrap_err().contains("already open"));
        trust.switch_off_launched().unwrap();
        Ok(true)
    }).unwrap_err();
    assert_eq!(refused, CHANGED_WHILE_OPEN);
    assert_eq!(lines(&project).len(), lines_before + 1, "only the off was written");
    assert!(matches!(choice(&trust), AppTrust::OffBySwitch { .. }), "trust stays off");
    // Once the dialog has closed, a preview can be opened again.
    assert!(trust.preview_on_launched().is_ok());
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn a_new_identity_while_the_confirmation_is_open_writes_nothing_under_either_identity() {
    let (project, trust) = set_up("trust-open-identity-");
    trust.switch_off_launched().unwrap();
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    let old = switches(&project);
    let refused = trust.confirm_on(&token, |_, _, _| { records_store::new_identity(&project).unwrap(); Ok(true) }).unwrap_err();
    assert_eq!(refused, CHANGED_WHILE_OPEN);
    assert_eq!(std::fs::read_to_string(&old).unwrap().lines().count(), 1, "nothing under the old identity");
    assert!(!switches(&project).exists(), "nothing under the new");
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_commands_name_their_project_and_the_labels_are_the_fixed_strings() {
    assert_eq!((PERFORM, DECLINE), ("Trust this project", "Keep untrusted"));
    let (project, trust) = set_up("trust-named-");
    let other = folder("trust-named-other-");
    for refused in [trust.switch_off(&other.to_string_lossy()).unwrap_err(), trust.preview_on(&other.to_string_lossy()).unwrap_err()] {
        assert_eq!(refused, "This project is not one the App holds; nothing written");
    }
    assert!(!switches(&project).exists());
    let name = trust.view()["project"].as_str().unwrap().to_owned();
    assert_eq!(trust.switch_off(&name).unwrap()["state"], "switched-off");
    assert_eq!(trust.preview_on(&name).unwrap()["perform"], "Trust this project");
    for p in [project, other] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn the_new_identity_act_writes_off_under_the_new_identity_for_a_project_on_by_setup() {
    let (project, trust) = set_up("trust-new-identity-");
    confirmed_on(&trust);
    let (line, not_set_off) = trust.new_identity_off_line(&project).expect("on by its setup: the act writes off");
    assert_eq!(not_set_off, NEW_IDENTITY_NOT_SET_OFF);
    let done = records_store::new_identity_with_trust_off(&project, Some((&line, not_set_off))).unwrap();
    assert_eq!(done["trustOff"], true);
    let written = lines(&project);
    assert_eq!(written.len(), 1);
    assert_eq!((written[0]["trust"].as_str(), written[0]["reason"].as_str()), (Some("off"), Some(NEW_IDENTITY_REASON)));
    assert_eq!(written[0]["projectId"].as_str(), done["projectId"].as_str(), "under the new identity");
    assert!(matches!(choice(&trust), AppTrust::OffByNewIdentity { .. }));
    let view = trust.view();
    assert_eq!((view["why"].as_str(), view["sentence"].as_str(), view["offers"].clone()), (Some("new-identity"), Some(CHOICE_OFF_BY_NEW_IDENTITY), json!(["switch-on"])));
    // Switched on again by the confirmed act.
    confirmed_on(&trust);
    assert!(matches!(choice(&trust), AppTrust::OnBySwitch { .. }));
    // An environment-route project the App holds gets the line too (point 5 of the second repair); a folder the
    // App does not hold gets none.
    let opened = ProjectTrust::for_launch(Some(&project), "explicit Root native environment path inputs");
    assert_eq!(opened.new_identity_off_line(&project).map(|(_, text)| text), Some(NEW_IDENTITY_NOT_SET_OFF_ENVIRONMENT));
    assert_eq!(opened.view()["newIdentity"], NEW_IDENTITY_TRUST_LINE);
    assert_eq!(trust.view()["newIdentity"], NEW_IDENTITY_TRUST_LINE);
    let other = folder("trust-new-identity-other-");
    assert!(trust.new_identity_off_line(&other).is_none());
    for p in [project, other] { std::fs::remove_dir_all(p).unwrap(); }
}

// ---- Second repair: the revision, the new identity on every route, its failure (B) ----

#[test]
fn the_revision_covers_every_line_so_an_earlier_decisive_line_replaced_under_the_same_last_line_and_count_changes_it() {
    let (project, trust) = set_up("trust-revision-all-");
    let known = trust.launched().unwrap();
    let (store, id) = ids(&project);
    let line = |trust: &str, store: &str, id: &str| format!("{}\n", json!({"format": SWITCH_FORMAT, "at": "2026-11-19T05:00:00.000Z", "trust": trust, "storeId": store, "projectId": id}));
    let file = switches(&project);
    std::fs::create_dir_all(file.parent().unwrap()).unwrap();
    // The last line, an on made in another store, is passed over: the line before it decides.
    let passed_over = line("on", "another-store", &id);
    std::fs::write(&file, format!("{}{passed_over}", line("off", &store, &id))).unwrap();
    let off = ProjectTrust::read_choice(&known, None);
    assert!(matches!(off.choice, AppTrust::OffBySwitch { .. }) && off.passed_over);
    // The earlier, decisive line replaced by another valid line; the count and the last line are the same.
    std::fs::write(&file, format!("{}{passed_over}", line("on", &store, &id))).unwrap();
    let on = ProjectTrust::read_choice(&known, None);
    assert!(matches!(on.choice, AppTrust::OnBySwitch { .. }));
    assert_ne!(on.revision, off.revision, "the revision covers every line");
    // A confirmation open across the same replacement writes nothing.
    std::fs::write(&file, format!("{}{passed_over}", line("off", &store, &id))).unwrap();
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    let refused = trust.confirm_on(&token, |_, _, _| {
        std::fs::write(&file, format!("{}{passed_over}", line("on", &store, &id))).unwrap();
        Ok(true)
    }).unwrap_err();
    assert_eq!(refused, CHANGED_WHILE_OPEN);
    assert_eq!(lines(&project).len(), 2, "nothing written");
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn a_new_identity_whose_off_line_cannot_be_written_says_the_identity_was_made_and_its_trust_is_on() {
    let (project, trust) = set_up("trust-new-identity-fails-");
    let old = ids(&project).1;
    let (line, not_set_off) = trust.new_identity_off_line(&project).unwrap();
    // The act's store line writes complete (the old identity's release, the new one's roots line); the off line,
    // the next, is stopped before it is put in place.
    records_store::interrupt_append_after_for_test(2, Some(records_store::AppendStop::BeforeWrite));
    let refused = records_store::new_identity_with_trust_off(&project, Some((&line, not_set_off))).unwrap_err();
    records_store::interrupt_append_for_test(None);
    assert!(refused.starts_with(NEW_IDENTITY_NOT_SET_OFF) && refused.len() > NEW_IDENTITY_NOT_SET_OFF.len(), "the agreed text, then the reason: {refused}");
    // The identity was made: the folder is attached to a new identity, with no switch line under it.
    let now = ids(&project).1;
    assert_ne!(now, old, "the new identity was made");
    assert!(!switches(&project).exists(), "its off line was not written");
    assert_eq!(choice(&trust), AppTrust::OnBySetup, "so the App's trust is on by its setup");
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn a_new_identity_whose_off_line_cannot_be_written_for_a_project_opened_from_the_environment_says_there_is_no_choice() {
    let project = folder("trust-new-identity-fails-environment-");
    records_store::attach(&project, true).unwrap();
    let trust = ProjectTrust::for_launch(Some(&project), "explicit Root native environment path inputs");
    let old = ids(&project).1;
    let (line, not_set_off) = trust.new_identity_off_line(&project).unwrap();
    assert_eq!(format!("{not_set_off}<reason>"), "The new identity was made, but Chirality could not record its trust as off. Chirality makes no trust choice for this project now, so the Codex settings Chirality uses decide. You can switch trust off in Settings. <reason>");
    records_store::interrupt_append_after_for_test(2, Some(records_store::AppendStop::BeforeWrite));
    let refused = records_store::new_identity_with_trust_off(&project, Some((&line, not_set_off))).unwrap_err();
    records_store::interrupt_append_for_test(None);
    assert!(refused.starts_with(NEW_IDENTITY_NOT_SET_OFF_ENVIRONMENT) && refused.len() > NEW_IDENTITY_NOT_SET_OFF_ENVIRONMENT.len(), "the agreed text, then the reason: {refused}");
    assert_ne!(ids(&project).1, old, "the new identity was made");
    assert!(!switches(&project).exists(), "its off line was not written");
    assert_eq!(choice(&trust), AppTrust::NoChoice, "so the App makes no choice");
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_settings_sentence_is_given_where_the_choice_is_on_or_none_and_not_where_the_entry_is_already_untrusted() {
    let (project, trust) = set_up("trust-settings-sentence-");
    let said = |trust: &ProjectTrust| (trust.view()["choice"].as_str().map(str::to_owned), trust.view()["settingsCanOverride"].as_str().map(str::to_owned));
    let sentence = Some(CHOICE_SETTINGS_CAN_OVERRIDE.to_owned());
    assert_eq!(said(&trust), (Some("on".into()), sentence.clone()));
    let environment = folder("trust-settings-sentence-environment-");
    assert_eq!(said(&ProjectTrust::for_launch(Some(&environment), "explicit Root native environment path inputs")), (Some("none".into()), sentence));
    trust.switch_off_launched().unwrap();
    assert_eq!(said(&trust), (Some("off".into()), None));
    append(&project, "{\"damaged\n");
    assert_eq!(said(&trust), (Some("not-read".into()), None));
    for p in [project, environment] { std::fs::remove_dir_all(p).unwrap(); }
}

#[test]
fn a_folder_that_no_longer_resolves_to_the_folder_admitted_gets_no_choice_applied() {
    let base = folder("trust-repointed-");
    let (first, second) = (base.join("first"), base.join("second"));
    for p in [&first, &second] { std::fs::create_dir_all(p).unwrap(); }
    records_store::attach(&first, true).unwrap();
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&first, &alias).unwrap();
    let trust = ProjectTrust::default();
    trust.add(&alias, Known::SetUpInApp);
    assert_eq!(trust.choice_for(&alias), Some(AppTrust::OnBySetup));
    // The given path now names another folder.
    std::fs::remove_file(&alias).unwrap();
    std::os::unix::fs::symlink(&second, &alias).unwrap();
    assert_eq!(trust.choice_for(&alias), Some(AppTrust::FolderChanged));
    let view = trust.view();
    assert_eq!((view["choice"].as_str(), view["sentence"].as_str(), view["canSwitch"].clone()), (Some("folder-changed"), Some(CHOICE_FOLDER_CHANGED), json!(false)));
    assert!(view["settingsCanOverride"].is_null(), "its own sentence says the entry is untrusted");
    assert!(trust.preview_on(&alias.to_string_lossy()).is_err());
    let mut reading = cl::TrustReading::not_read(alias.clone(), cl::TRUST_READ_FAILED, None);
    reading.case = cl::TrustCase::Trusted { key: alias.to_string_lossy().into_owned() };
    reading.choice = trust.choice_for(&alias);
    assert_eq!((reading.trust_level(), reading.status()["lines"].clone()), ("untrusted", json!([cl::TRUST_FOLDER_CHANGED])));
    std::fs::remove_dir_all(base).unwrap();
}

// ---- Second repair: the folder's own identity (A) ----

#[test]
fn another_folder_put_at_the_projects_path_is_not_the_project() {
    let base = folder("trust-same-path-");
    let project = base.join("project");
    std::fs::create_dir_all(&project).unwrap();
    let trust = ProjectTrust::for_launch(Some(&project), crate::desktop_startup::SAVED_REQUEST_SOURCE);
    assert_eq!(trust.choice_for(&project), Some(AppTrust::OnBySetup));
    std::fs::rename(&project, base.join("project-old")).unwrap();
    std::fs::create_dir_all(&project).unwrap();
    assert_eq!(trust.choice_for(&project), Some(AppTrust::FolderChanged), "same path, another folder");
    std::fs::remove_dir_all(base).unwrap();
}

// ---- Second repair: the acts and the view (C) ----

#[test]
fn a_preview_cannot_be_installed_while_a_confirmation_is_in_its_dialog_two_threads() {
    use std::sync::mpsc::channel;
    use std::time::Duration;
    let (project, trust) = set_up("trust-preview-race-");
    trust.switch_off_launched().unwrap();
    let first = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    // A second preview is held after its check, before its install.
    let (checked_tx, checked_rx) = channel::<()>();
    let (go_tx, go_rx) = channel::<()>();
    *trust.before_preview_install.lock().unwrap() = Some(Box::new(move || { checked_tx.send(()).unwrap(); go_rx.recv().unwrap(); }));
    let (in_dialog_tx, in_dialog_rx) = channel::<()>();
    let (close_tx, close_rx) = channel::<()>();
    std::thread::scope(|scope| {
        let second = scope.spawn(|| trust.preview_on_launched());
        checked_rx.recv_timeout(Duration::from_secs(5)).unwrap();
        // The first preview's confirmation reaches its dialog only after the second preview's step has ended.
        let (trust, first) = (&trust, &first);
        let confirming = scope.spawn(move || trust.confirm_on(first, |_, _, _| { in_dialog_tx.send(()).unwrap(); close_rx.recv().unwrap(); Ok(false) }));
        assert!(in_dialog_rx.recv_timeout(Duration::from_millis(300)).is_err(), "the dialog waits for the preview's one step");
        go_tx.send(()).unwrap();
        let second = second.join().unwrap().unwrap()["token"].as_str().unwrap().to_owned();
        in_dialog_rx.recv_timeout(Duration::from_secs(5)).unwrap();
        // While the dialog is open: no preview is installed, and none can be.
        assert!(trust.preview.lock().unwrap().is_none(), "the preview installed before the dialog is withdrawn with it");
        assert!(trust.preview_on_launched().unwrap_err().contains("already open"));
        close_tx.send(()).unwrap();
        assert_eq!(confirming.join().unwrap().unwrap()["state"], "cancelled; trust not switched on");
        assert_eq!(trust.confirm_on(&second, |_, _, _| Ok(true)).unwrap_err(), "This trust preview is not the open one; review it again");
    });
    assert!(matches!(choice(&trust), AppTrust::OffBySwitch { .. }));
    std::fs::remove_dir_all(project).unwrap();
}

#[test]
fn the_view_offers_no_switch_where_the_choice_cannot_be_read_and_gives_its_detail() {
    let (project, trust) = set_up("trust-view-not-read-");
    trust.switch_off_launched().unwrap();
    let view = trust.view();
    assert_eq!((view["canSwitch"].as_bool(), view["offers"].clone()), (Some(true), json!(["switch-on"])), "the control");
    std::fs::OpenOptions::new().append(true).open(switches(&project)).unwrap().write_all(b"{\"format\":\"chirality.project-trust-switch\",\"trust\":\"on\"}\n").unwrap();
    let AppTrust::NotRead { detail: Some(detail) } = choice(&trust) else { panic!("not read") };
    let view = trust.view();
    assert_eq!((view["canSwitch"].as_bool(), view["offers"].clone(), view["cannotSwitch"].as_str()), (Some(false), json!([]), Some(CANNOT_SWITCH)));
    assert_eq!(view["cannotSwitchDetail"], json!({"text": detail, "standing": cl::NOT_THE_APPS_TEXT}));
    // And the acts refuse as the view says.
    assert_eq!(trust.preview_on_launched().unwrap_err(), format!("{CANNOT_SWITCH} {detail}"));
    assert!(trust.switch_off_launched().unwrap_err().starts_with(CANNOT_SWITCH));
    std::fs::remove_dir_all(project).unwrap();
}
