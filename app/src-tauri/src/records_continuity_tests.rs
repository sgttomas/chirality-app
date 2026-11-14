//! Genuine private Host receipts with an invented native peer; no human-act witness.
use super::*;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use std::{fs, os::unix::fs::PermissionsExt, path::Path, time::Instant};
/// The second field: the fixture's App data (`app/`) held as the App holds it
/// before it opens a ledger, so that a later Host on it models a relaunch.
struct Fixture(PathBuf, #[allow(dead_code)] crate::AppDataCustody);
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(opaque_id("records-continuity-").unwrap());
        for dir in ["project", "account", "probe", "app"] {
            fs::create_dir_all(root.join(dir)).unwrap();
        }
        fs::write(root.join("peer.py"), PEER).unwrap();
        fs::set_permissions(root.join("peer.py"), fs::Permissions::from_mode(0o700)).unwrap();
        let project = root.join("project");
        let log = crate::storage::project_log(&project, Some("run:continuity"), "fixture-writer")
            .unwrap();
        fs::create_dir_all(log.parent().unwrap()).unwrap();
        let entry = crate::records::envelope(
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"CONTINUITY-MARKER","detail":"invented"}),
            "rec:continuity".into(),
            1,
            Some("run:continuity"),
            None,
        );
        fs::write(log, format!("{entry}\n")).unwrap();
        let custody = crate::hold_app_data_for_test(&root.join("app")).unwrap();
        Self(root, custody)
    }
    fn context(&self) -> ExplicitAppProjectContext {
        ExplicitAppProjectContext::known(
            self.0.join("project").to_str().unwrap(),
            AppProjectSource::ConfiguredDirectory,
        )
        .unwrap()
    }
    fn host(&self, offered: bool, project: Option<&str>, home: &str) -> Arc<Host> {
        let host = Arc::new(Host::new());
        host.configure_recovery(self.0.join("app/recovery.ledger.jsonl"))
            .unwrap();
        self.launch(&host, offered, project, home);
        host
    }
    fn launch(&self, host: &Arc<Host>, offered: bool, project: Option<&str>, home: &str) {
        if offered {
            let context = match project {
                Some(project) => {
                    ExplicitAppProjectContext::known(project, AppProjectSource::ConfiguredDirectory)
                        .unwrap()
                }
                None => self.context(),
            };
            let configured = project
                .filter(|reference| {
                    Path::new(reference).is_absolute() && Path::new(reference).exists()
                })
                .map(PathBuf::from)
                .unwrap_or_else(|| self.0.join("project"));
            host.configure_records_capability_with_context(
                Arc::new(
                    crate::records_access::RecordsCapability::at(
                        &configured,
                        self.0.join("app/reads.jsonl"),
                    )
                    .unwrap(),
                ),
                context,
            );
        }
        fs::create_dir_all(self.0.join(home)).unwrap();
        let mut config = HostConfig::new(
            self.0.join("peer.py"),
            self.0.join(home),
            self.0.join("probe"),
            // Native spawn uses the real directory; the explicit Root receipt
            // still retains its configured spelling (which may be an alias).
            self.0.join("project").canonicalize().unwrap(),
        );
        config.allow_unverified_dev = true;
        config.wait_limit = Duration::from_secs(2);
        host.start(&config, "invented continuity peer").unwrap();
    }
    fn start(&self, host: &Host, model: &str) -> Result<SourceRequest, String> {
        let generation = host.snapshot()["generation"].clone();
        let request = host.thread_start_with_guidance_dispatch(
            &generation,
            self.0.join("project").to_str().unwrap(),
            model,
            "fixture-provider",
            "invented guidance",
        )?;
        host.source_request_wait(&request, Duration::from_millis(200))?;
        host.thread_start_dispatch_finish(&request)?;
        let context = host
            .records_project_context()
            .unwrap_or_else(|| self.context());
        host.observe_conversation_project(&generation, "thread", Some("H-acct"), &context)?;
        Ok(request)
    }
    fn resume(&self, host: &Host, thread: &str) -> Result<Value, String> {
        let generation = host.snapshot()["generation"].clone();
        let home = generation["home"].as_str().unwrap();
        let mut history = NativeHistory::new(home, generation.clone()).unwrap();
        let list = history
            .list_threads(None, crate::native_history::Direction::Desc)
            .unwrap();
        let sent = host.history_dispatch(&list).unwrap();
        let evidence = host.history_wait(&sent, Duration::from_secs(2)).unwrap();
        history
            .receive(&list, home, &generation, &evidence["response"]["result"])
            .unwrap();
        history.select(thread).unwrap();
        let query = history.continue_query().unwrap();
        let sent = host.history_dispatch(&query).unwrap();
        let evidence = host.history_wait(&sent, Duration::from_secs(2)).unwrap();
        history
            .receive(&query, home, &generation, &evidence["response"]["result"])
            .unwrap();
        let admitted = host.history_admit_resume(&history, &sent)?;
        if host.snapshot()["generation"] == generation {
            assert!(host
                .history_admit_resume(&history, &sent)
                .unwrap_err()
                .contains("already operationally admitted"));
        }
        Ok(admitted)
    }
    fn values(&self, host: &Host) -> Vec<Value> {
        host.tags_of("H-acct", "thread", records_continuity::OWNER)
    }
    fn reads(&self) -> Vec<Value> {
        fs::read_to_string(self.0.join("app/reads.jsonl"))
            .unwrap_or_default()
            .lines()
            .map(|line| serde_json::from_str(line).unwrap())
            .collect()
    }
    fn tool(&self, host: &Host, thread: &str) -> Value {
        self.tool_at(host, thread, &self.0.join("project"))
    }
    fn tool_at(&self, host: &Host, thread: &str, wire_project: &Path) -> Value {
        let before = wire(wire_project).len();
        let generation = host.snapshot()["generation"].clone();
        host.turn_start_text(&generation, thread, "Read records")
            .unwrap();
        let id = format!("records-{thread}");
        let until = Instant::now() + Duration::from_secs(3);
        loop {
            let frames = wire(wire_project)
                .into_iter()
                .skip(before)
                .collect::<Vec<_>>();
            if let Some(reply) = frames
                .iter()
                .find(|frame| frame["id"] == id && frame.get("method").is_none())
            {
                if let Some(other) = frames.iter().find(|frame| {
                    frame["id"] == format!("other-{thread}") && frame.get("method").is_none()
                }) {
                    assert!(other["error"].is_object());
                    return reply.clone();
                }
            }
            assert!(Instant::now() < until, "tool reply absent");
            std::thread::sleep(Duration::from_millis(10));
        }
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn wire(project: &Path) -> Vec<Value> {
    fs::read_to_string(project.join("wire.jsonl"))
        .unwrap_or_default()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect()
}
fn stop(host: &Host) {
    let _ = host.stop("invented peer", "finished test step");
    // Each fixture Host is its own App process; a stopped one has ended
    // (one App at a time on this data).
    host.end_process_for_test();
}
#[test]
fn records_continuity_original_start_to_fresh_host_explicit_cold_resume_and_logged_read() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    let original = f.start(&first, "fixture-model").unwrap();
    let values = f.values(&first);
    assert_eq!(values.len(), 1);
    let receipt =
        records_continuity::Receipt::decode(values[0]["value"].as_str().unwrap()).unwrap();
    assert_eq!(receipt.admitted.request, original.request_ref());
    assert_eq!(receipt.project, f.context().reference().unwrap());
    let old_generation = first.snapshot()["generation"].clone();
    stop(&first);
    drop(first);
    let cold = f.host(true, None, "account");
    let generation = cold.snapshot()["generation"].clone();
    assert_ne!(old_generation["appSession"], generation["appSession"]);
    let row = f.resume(&cold, "thread").unwrap();
    assert_eq!(
        row["recordsCapabilityBinding"]["state"],
        "bound in current generation"
    );
    assert_eq!(row["appRole"]["standing"], "unknown");
    let reply = f.tool(&cold, "thread");
    assert_eq!(reply["result"]["success"], true);
    assert!(reply.to_string().contains("run:continuity"));
    assert_eq!(f.reads().len(), 1);
    assert_eq!(
        f.reads()[0]["generation"],
        crate::recovery::generation_ref(&generation).unwrap()
    );
    let resumed = wire(&f.0.join("project"))
        .into_iter()
        .find(|frame| frame["method"] == "thread/resume")
        .unwrap();
    assert_eq!(resumed["params"], json!({"threadId":"thread","excludeTurns":true}));
    let fork = cold.thread_fork_dispatch(&generation, "thread").unwrap();
    cold.source_request_wait(&fork, Duration::from_secs(2))
        .unwrap();
    let child = cold.thread_fork_finish(&fork).unwrap();
    assert_eq!(
        child["recordsCapabilityBinding"]["persistence"],
        "durable App metadata"
    );
    assert_eq!(f.tool(&cold, "forked")["result"]["success"], true);
    assert_eq!(f.reads().len(), 2);
    let tags = cold.tags_of("H-acct", "forked", records_continuity::OWNER);
    assert_eq!(tags.len(), 1);
    let child_receipt =
        records_continuity::Receipt::decode(tags[0]["value"].as_str().unwrap()).unwrap();
    assert_eq!(child_receipt.from.as_deref(), Some("thread"));
    assert_eq!(child_receipt.admitted.request, fork.request_ref());
    assert_eq!(
        fork.attempted_frame()["params"],
        json!({"threadId":"thread","deferGoalContinuation":true})
    );
    stop(&cold);
    drop(cold);
    let restarted = f.host(true, None, "account");
    assert_eq!(
        f.resume(&restarted, "forked").unwrap()["recordsCapabilityBinding"]["state"],
        "bound in current generation"
    );
    assert_eq!(f.tool(&restarted, "forked")["result"]["success"], true);
    assert_eq!(f.reads().len(), 3);
    stop(&restarted);
}
#[test]
fn records_continuity_missing_or_foreign_receipt_never_backfills_same_cwd() {
    for mismatch in [
        "unoffered",
        "wrong-project",
        "wrong-home",
        "malformed",
        "definition",
        "conflict",
    ] {
        let f = Fixture::new();
        let first = f.host(mismatch != "unoffered", None, "account");
        f.start(&first, "fixture-model").unwrap();
        let generation = first.snapshot()["generation"].clone();
        if matches!(mismatch, "malformed" | "definition" | "conflict") {
            let value = if mismatch == "malformed" {
                "{bad".into()
            } else {
                let mut receipt: Value =
                    serde_json::from_str(f.values(&first)[0]["value"].as_str().unwrap()).unwrap();
                if mismatch == "definition" {
                    receipt["definition"] = json!("unsupported-definition");
                } else {
                    receipt["offered"]["request"] = json!("different-source");
                    receipt["admitted"]["request"] = json!("different-source");
                }
                receipt.to_string()
            };
            assert_eq!(
                first.tag_conversation(
                    &generation,
                    "thread",
                    Some("H-acct"),
                    records_continuity::OWNER,
                    &value
                )["persistence"],
                "durable App metadata"
            );
        }
        stop(&first);
        drop(first);
        let cold = f.host(
            true,
            if mismatch == "wrong-project" {
                Some("another explicit App project")
            } else {
                None
            },
            if mismatch == "wrong-home" {
                "key"
            } else {
                "account"
            },
        );
        let row = f.resume(&cold, "thread").unwrap();
        assert_eq!(
            row["recordsCapabilityBinding"]["state"], "unknown/unsupported",
            "{mismatch}: {row}"
        );
        assert!(f.tool(&cold, "thread")["error"].is_object(), "{mismatch}");
        assert!(f.reads().is_empty());
        stop(&cold);
    }
}
#[test]
fn records_continuity_failed_or_unknown_start_cannot_supply_a_receipt() {
    for model in ["fail", "unknown", "malformed"] {
        let f = Fixture::new();
        let first = f.host(true, None, "account");
        assert!(f.start(&first, model).is_err());
        assert!(f.values(&first).is_empty());
        stop(&first);
        drop(first);
        let cold = f.host(true, None, "account");
        let row = f.resume(&cold, "thread").unwrap();
        assert_eq!(
            row["recordsCapabilityBinding"]["state"],
            "unknown/unsupported"
        );
        assert!(f.tool(&cold, "thread")["error"].is_object());
        assert!(f.reads().is_empty());
        stop(&cold);
    }
}
#[test]
fn records_continuity_generation_replacement_during_lookup_installs_no_binding() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    f.start(&first, "fixture-model").unwrap();
    stop(&first);
    drop(first);
    let cold = f.host(true, None, "account");
    let old = cold.snapshot()["generation"].clone();
    let weak = Arc::downgrade(&cold);
    *cold.before_records_receipt_bind.lock().unwrap() = Some(Box::new(move || {
        let host = weak.upgrade().unwrap();
        let mut inner = host.inner.0.lock().unwrap();
        Host::close_generation(&mut inner);
        inner.generation["spawnCounter"] =
            json!(inner.generation["spawnCounter"].as_u64().unwrap() + 1);
        inner.state = "ready".into();
    }));
    f.resume(&cold, "thread").unwrap();
    assert!(!cold
        .inner
        .0
        .lock()
        .unwrap()
        .records_offers
        .iter()
        .any(|(generation, _)| generation == &old));
    stop(&cold);
}
#[test]
fn records_continuity_tag_failure_keeps_hot_use_and_fresh_recovery_reads_only_landed_receipts() {
    for landed in [false, true] {
        let f = Fixture::new();
        let first = f.host(true, None, "account");
        let generation = first.snapshot()["generation"].clone();
        let request = first
            .thread_start_with_guidance_dispatch(
                &generation,
                f.0.join("project").to_str().unwrap(),
                "fixture-model",
                "fixture-provider",
                "invented guidance",
            )
            .unwrap();
        first
            .source_request_wait(&request, Duration::from_secs(2))
            .unwrap();
        first.thread_start_dispatch_finish(&request).unwrap();
        first
            .observe_conversation_project_inner(&generation, "thread", Some("H-acct"), &f.context())
            .unwrap();
        if landed {
            crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|fault| fault.set(true));
        } else {
            crate::recovery::store::FAIL_BATCH_AFTER.with(|fault| fault.set(Some(0)));
        }
        first.persist_records_receipt(&generation, "thread", Some("H-acct"));
        assert!(
            f.values(&first).is_empty(),
            "unconfirmed tag is not held as durable"
        );
        assert_eq!(
            first.snapshot()["threads"][0]["recordsCapabilityBinding"]["persistence"],
            "memory-only"
        );
        assert_eq!(
            f.tool(&first, "thread")["result"]["success"],
            true,
            "genuine hot offering survives receipt publication failure"
        );
        stop(&first);
        drop(first);
        if landed {
            // Continuing directory-sync failure refuses fresh REC initialization,
            // so even the readable landed receipt cannot hydrate a handler.
            let failed = Arc::new(Host::new());
            crate::storage::fail_directory_for_test(Some(f.0.join("app")));
            assert!(failed
                .configure_recovery(f.0.join("app/recovery.ledger.jsonl"))
                .is_err());
            f.launch(&failed, true, None, "account");
            let row = f.resume(&failed, "thread").unwrap();
            assert_eq!(
                row["recordsCapabilityBinding"]["state"],
                "unknown/unsupported"
            );
            crate::storage::fail_directory_for_test(None);
            assert!(f.tool(&failed, "thread")["error"].is_object());
            stop(&failed);
            drop(failed);
        }
        let cold = f.host(true, None, "account");
        let row = f.resume(&cold, "thread").unwrap();
        assert_eq!(
            row["recordsCapabilityBinding"]["state"],
            if landed {
                "bound in current generation"
            } else {
                "unknown/unsupported"
            }
        );
        let response = f.tool(&cold, "thread");
        assert_eq!(response["result"]["success"] == true, landed);
        assert_eq!(f.reads().len(), if landed { 2 } else { 1 });
        stop(&cold);
    }
}
#[test]
fn records_continuity_changed_physical_project_never_uses_textual_root_alias_or_path() {
    for change in ["alias", "replaced-before-resume", "replaced-while-hot"] {
        let f = Fixture::new();
        let project = f.0.join("project");
        let old = f.0.join("physical-a");
        let new = f.0.join("physical-b");
        let alias = f.0.join("configured-project");
        let reference = if change == "alias" {
            std::os::unix::fs::symlink(&project, &alias).unwrap();
            Some(alias.to_str().unwrap())
        } else {
            None
        };
        let first = f.host(true, reference, "account");
        f.start(&first, "fixture-model").unwrap();
        if change == "alias" {
            stop(&first);
            fs::remove_file(&alias).unwrap();
            fs::create_dir(&new).unwrap();
            std::os::unix::fs::symlink(&new, &alias).unwrap();
        } else {
            fs::rename(&project, &old).unwrap();
            fs::create_dir(&project).unwrap();
            // Keep the same explicit records-store project identity so the
            // real supplier retention admission is valid. Physical equality
            // is a separate receiver check and must still fail.
            let link = crate::records_store::PROJECT_LINK;
            fs::create_dir_all(project.join(link).parent().unwrap()).unwrap();
            fs::copy(old.join(link), project.join(link)).unwrap();
            assert_eq!(
                fs::read(old.join(link)).unwrap(),
                fs::read(project.join(link)).unwrap()
            );
        }
        if change == "replaced-while-hot" {
            assert!(f.tool_at(&first, "thread", &old)["error"].is_object());
            assert!(f.reads().is_empty());
        }
        stop(&first);
        drop(first);
        let cold = f.host(true, reference, "account");
        let row = f.resume(&cold, "thread").unwrap();
        assert_eq!(
            row["recordsCapabilityBinding"]["state"], "unknown/unsupported",
            "{change}: {row}"
        );
        assert!(f.tool(&cold, "thread")["error"].is_object());
        assert!(f.reads().is_empty());
        stop(&cold);
    }
}
#[test]
fn records_continuity_new_conflicting_tag_during_lookup_remains_unknown() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    f.start(&first, "fixture-model").unwrap();
    stop(&first);
    drop(first);
    let cold = f.host(true, None, "account");
    let generation = cold.snapshot()["generation"].clone();
    let weak = Arc::downgrade(&cold);
    *cold.before_records_receipt_bind.lock().unwrap() = Some(Box::new(move || {
        let host = weak.upgrade().unwrap();
        assert_eq!(
            host.tag_conversation(
                &generation,
                "thread",
                Some("H-acct"),
                records_continuity::OWNER,
                "{new conflicting malformed claim"
            )["persistence"],
            "durable App metadata"
        );
    }));
    let row = f.resume(&cold, "thread").unwrap();
    assert_eq!(
        row["recordsCapabilityBinding"]["state"],
        "unknown/unsupported"
    );
    assert!(f.tool(&cold, "thread")["error"].is_object());
    assert!(f.reads().is_empty());
    stop(&cold);
}
#[test]
fn records_continuity_original_project_is_frozen_and_capability_only_setup_clears_context() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    let generation = host.snapshot()["generation"].clone();
    let request = host
        .thread_start_with_guidance_dispatch(
            &generation,
            f.0.join("project").to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            "invented guidance",
        )
        .unwrap();
    host.source_request_wait(&request, Duration::from_secs(2))
        .unwrap();
    let capability = host.records_capability().unwrap();
    host.configure_records_capability_with_context(
        capability.clone(),
        ExplicitAppProjectContext::known(
            "different explicit project",
            AppProjectSource::OpenedDirectory,
        )
        .unwrap(),
    );
    host.thread_start_dispatch_finish(&request).unwrap();
    host.observe_conversation_project(&generation, "thread", Some("H-acct"), &f.context())
        .unwrap();
    let receipt =
        records_continuity::Receipt::decode(f.values(&host)[0]["value"].as_str().unwrap()).unwrap();
    assert_eq!(
        receipt.project,
        f.context().reference().unwrap(),
        "response admission cannot relabel original offering"
    );
    assert!(
        f.tool(&host, "thread")["error"].is_object(),
        "changed current context cannot borrow the old offering"
    );
    host.configure_records_capability(capability);
    assert!(host.records_project_context().is_none());
    stop(&host);
}
#[test]
fn records_continuity_unsupported_definition_and_ineligible_start_receive_no_binding() {
    for kind in [
        "unsupported-definition",
        "duplicate-definition",
        "not-loaded",
    ] {
        let f = Fixture::new();
        let host = f.host(true, None, "account");
        let generation = host.snapshot()["generation"].clone();
        let (mut params, project) = host
            .offered_start_params(
                f.0.join("project").to_str().unwrap(),
                if kind == "not-loaded" {
                    "not-loaded"
                } else {
                    "fixture-model"
                },
                "fixture-provider",
                Some("invented guidance"),
            )
            .unwrap();
        if kind == "unsupported-definition" {
            params["dynamicTools"][0]["description"] = json!("unsupported earlier definition");
        }
        if kind == "duplicate-definition" {
            params["dynamicTools"] = json!([
                crate::records_access::definition(),
                crate::records_access::definition()
            ]);
        }
        let request = host
            .request_begin_with_offer(
                "thread/start",
                params,
                json!({"kind":"person-directed"}),
                false,
                Some(&generation),
                false,
                None,
                None,
                None,
                project,
            )
            .unwrap();
        host.source_request_wait(&request, Duration::from_secs(2))
            .unwrap();
        host.thread_start_dispatch_finish(&request).unwrap();
        host.observe_conversation_project(&generation, "thread", Some("H-acct"), &f.context())
            .unwrap();
        assert!(f.values(&host).is_empty(), "{kind}");
        assert!(f.tool(&host, "thread")["error"].is_object(), "{kind}");
        assert!(f.reads().is_empty());
        stop(&host);
    }
}
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,os
if '--version' in sys.argv:
 print('codex-cli 0.167.0');sys.exit(0)
def emit(v):print(json.dumps(v),flush=True)
def thread(tid,status='idle',source=None):
 t={'id':tid,'cliVersion':'0.167.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'invented','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':status},'turns':[]}
 if source:t['forkedFromId']=source
 return t
def result(tid,source=None):return {'thread':thread(tid,source=source),'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log:log.write(json.dumps(f)+'\n')
 method=f.get('method')
 if 'id' not in f or method is None:continue
 if method=='initialize':emit({'id':f['id'],'result':{'userAgent':'invented-continuity-peer'}})
 elif method=='config/read':emit({'id':f['id'],'result':{'config':{'model_provider':'openai','model_providers':{}},'origins':{}}})
 elif method=='thread/start':
  if f['params'].get('model')=='fail':emit({'id':f['id'],'error':{'code':-32600,'message':'invented refusal'}})
  elif f['params'].get('model')=='malformed':emit({'id':f['id'],'result':{'thread':{'id':'thread'}}})
  elif f['params'].get('model')=='not-loaded':
   r=result('thread');r['thread']['status']={'type':'notLoaded'};emit({'id':f['id'],'result':r})
  elif f['params'].get('model')!='unknown':emit({'id':f['id'],'result':result('thread')})
 elif method=='thread/list':emit({'id':f['id'],'result':{'data':[thread('thread','notLoaded'),thread('forked','notLoaded','thread')],'nextCursor':None}})
 elif method=='thread/resume':emit({'id':f['id'],'result':result(f['params']['threadId'])})
 elif method=='thread/fork':emit({'id':f['id'],'result':result('forked',f['params']['threadId'])})
 elif method=='turn/start':
  tid=f['params']['threadId']
  emit({'id':f['id'],'result':{'turn':{'id':'turn-'+tid,'status':'inProgress','items':[],'error':None,'itemsView':'summary'}}})
  emit({'id':'records-'+tid,'method':'item/tool/call','params':{'threadId':tid,'turnId':'turn-'+tid,'callId':'read-'+tid,'tool':'chirality_records_read_v1','namespace':None,'arguments':{'operation':'list_runs'}}})
  emit({'id':'other-'+tid,'method':'item/tool/call','params':{'threadId':tid,'turnId':'turn-'+tid,'callId':'other-'+tid,'tool':'another_tool','namespace':None,'arguments':{}}})
 else:emit({'id':f['id'],'result':{}})
"#;

// ---- The project identity is read with no Host state held, and compared
// under it (the read touches the filesystem: canonicalize and metadata).

/// Replaces the fixture's project at the same path (same canonical path, a
/// different folder), keeping its records-store link, and returns where the
/// old folder (the running peer's working directory) now is.
fn replace_project(root: &Path) -> PathBuf {
    let project = root.join("project");
    let old = root.join("physical-a");
    fs::rename(&project, &old).unwrap();
    fs::create_dir(&project).unwrap();
    let link = crate::records_store::PROJECT_LINK;
    fs::create_dir_all(project.join(link).parent().unwrap()).unwrap();
    fs::copy(old.join(link), project.join(link)).unwrap();
    old
}

/// A reading that does not return (a stalled project filesystem) holds no
/// Host state: the Host's snapshot is had at once meanwhile, and the records
/// call is answered once the reading returns.
#[test]
fn records_identity_reading_that_stalls_does_not_hold_the_host_state() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    f.start(&first, "fixture-model").unwrap();
    let (entered_tx, entered_rx) = std::sync::mpsc::channel();
    let (release_tx, release_rx) = std::sync::mpsc::channel::<()>();
    *first.within_records_identity_read.lock().unwrap() = Some(Box::new(move || {
        entered_tx.send(()).unwrap();
        let _ = release_rx.recv();
    }));
    // While the records call's reading is stalled, another thread takes the
    // Host's snapshot, then lets the reading return.
    let host = Arc::clone(&first);
    let checker = std::thread::spawn(move || {
        entered_rx.recv_timeout(Duration::from_secs(3)).expect("the records call's reading began");
        let (snap_tx, snap_rx) = std::sync::mpsc::channel();
        std::thread::spawn(move || { let _ = snap_tx.send(host.snapshot()["state"].clone()); });
        let state = snap_rx.recv_timeout(Duration::from_millis(500));
        release_tx.send(()).unwrap();
        state
    });
    let reply = f.tool(&first, "thread");
    let state = checker.join().unwrap().expect("the Host's state is not held by the stalled reading");
    assert_eq!(state, "ready");
    assert_eq!(reply["result"]["success"], true, "answered once the reading returned: {reply}");
    stop(&first);
}

/// The project replaced (or gone) after the Host's reading and before its
/// use: the Host admits the call on the reading it took, as it did when the
/// reading was taken under its state (nothing on disk ever waited for that
/// state). The capability reads the identity again before it reads anything,
/// refuses, and returns nothing from either folder.
#[test]
fn records_project_replaced_after_the_hosts_reading_is_never_read_as_the_old_one() {
    for change in ["replaced", "gone"] {
        let f = Fixture::new();
        let first = f.host(true, None, "account");
        f.start(&first, "fixture-model").unwrap();
        let root = f.0.clone();
        let moved = root.join("physical-a");
        *first.within_records_identity_read.lock().unwrap() = Some(Box::new(move || {
            if change == "replaced" { replace_project(&root); } else { fs::rename(root.join("project"), root.join("physical-a")).unwrap(); }
        }));
        let reply = f.tool_at(&first, "thread", &moved);
        assert_ne!(reply["result"]["success"], true, "{change}: {reply}");
        assert!(f.reads().iter().all(|read| read["outcome"] == "refused"), "{change}: {:?}", f.reads());
        assert!(!reply.to_string().contains("CONTINUITY-MARKER"), "{change}: nothing from the old project is returned: {reply}");
        stop(&first);
    }
}

/// The capability configured again after the Host's reading and before its
/// comparison: the reading went through the old capability and is not
/// current for the new one, so the call is not admitted as a records read.
#[test]
fn records_capability_configured_again_after_the_reading_is_not_current() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    f.start(&first, "fixture-model").unwrap();
    let weak = Arc::downgrade(&first);
    let (project, reads, context) = (f.0.join("project"), f.0.join("app/reads.jsonl"), f.context());
    *first.within_records_identity_read.lock().unwrap() = Some(Box::new(move || {
        let host = weak.upgrade().unwrap();
        host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&project, reads).unwrap()), context);
    }));
    let reply = f.tool(&first, "thread");
    assert!(reply["error"].is_object(), "{reply}");
    assert!(f.reads().is_empty());
    stop(&first);
}

/// A receipt's binding compares a reading of its own, taken after its
/// lookup's: the project replaced between the two is caught at binding.
#[test]
fn records_receipt_binding_reads_the_project_again_after_its_lookup() {
    let f = Fixture::new();
    let first = f.host(true, None, "account");
    f.start(&first, "fixture-model").unwrap();
    stop(&first);
    drop(first);
    let cold = f.host(true, None, "account");
    let root = f.0.clone();
    *cold.before_records_receipt_bind.lock().unwrap() = Some(Box::new(move || { replace_project(&root); }));
    let row = f.resume(&cold, "thread").unwrap();
    assert_eq!(row["recordsCapabilityBinding"]["state"], "unknown/unsupported", "{row}");
    assert!(row["recordsCapabilityBinding"]["limit"].as_str().unwrap_or_default().contains("physical project changed"), "{row}");
    stop(&cold);
}

/// A call that could not be an offered records call (a stale generation, a
/// conversation never offered it) and a receipt lookup that already failed
/// take no project reading at all: they never wait on the project's filesystem.
#[test]
fn records_ineligible_calls_and_failed_lookups_take_no_project_reading() {
    use std::sync::atomic::{AtomicUsize, Ordering};
    let f = Fixture::new();
    let host = Host::new();
    host.configure_records_capability_with_context(Arc::new(crate::records_access::RecordsCapability::at(&f.0.join("project"), f.0.join("app/reads.jsonl")).unwrap()), f.context());
    let readings = Arc::new(AtomicUsize::new(0));
    let count = |host: &Host, readings: &Arc<AtomicUsize>| {
        let counter = Arc::clone(readings);
        *host.within_records_identity_read.lock().unwrap() = Some(Box::new(move || { counter.fetch_add(1, Ordering::SeqCst); }));
    };
    let stale = json!({"appSession":"stale", "home":"app-home:stale", "spawnCounter":1});
    count(&host, &readings);
    host.on_line(&serde_json::to_vec(&json!({"id":"unoffered", "method":"item/tool/call", "params":{"tool":crate::records_access::TOOL, "threadId":"unoffered", "namespace":null}})).unwrap(), &stale);
    assert_eq!(readings.load(Ordering::SeqCst), 0, "a call no offer admits reads nothing of the project");
    count(&host, &readings);
    host.restore_records_receipt(&stale, "unadmitted");
    assert_eq!(readings.load(Ordering::SeqCst), 0, "a lookup that failed takes no binding reading");
    count(&host, &readings);
    host.persist_records_receipt(&stale, "unoffered", Some("H-acct"));
    assert_eq!(readings.load(Ordering::SeqCst), 0, "a conversation never offered the capability takes no reading");
    assert!(f.reads().is_empty());
}

/// A recovery ledger replaced by a second configuration closes its database
/// after the Host's state is released, not under it.
#[test]
fn a_replaced_recovery_ledger_closes_after_the_host_state_is_released() {
    use std::sync::atomic::{AtomicBool, Ordering};
    struct Probe { host: Arc<Host>, closed: AtomicBool, held: AtomicBool }
    unsafe extern "C" fn close_trace(kind: u32, context: *mut std::ffi::c_void, _: *mut std::ffi::c_void, _: *mut std::ffi::c_void) -> i32 {
        if kind == rusqlite::ffi::SQLITE_TRACE_CLOSE as u32 {
            let probe = unsafe { &*(context as *const Probe) };
            probe.closed.store(true, Ordering::SeqCst);
            probe.held.store(probe.host.inner.0.try_lock().is_err(), Ordering::SeqCst);
        }
        0
    }
    let f = Fixture::new();
    let host = Arc::new(Host::new());
    host.configure_recovery(f.0.join("app/first-ledger.jsonl")).unwrap();
    let probe = Box::new(Probe { host: Arc::clone(&host), closed: AtomicBool::new(false), held: AtomicBool::new(false) });
    {
        let ledger = host.inner.0.lock().unwrap().recovery.clone().unwrap();
        let ledger = ledger.lock().unwrap();
        let connection = ledger.store().unwrap().connection();
        let result = unsafe { rusqlite::ffi::sqlite3_trace_v2(connection.handle(), rusqlite::ffi::SQLITE_TRACE_CLOSE as u32, Some(close_trace), (&*probe as *const Probe).cast_mut().cast()) };
        assert_eq!(result, rusqlite::ffi::SQLITE_OK);
    }
    host.configure_recovery(f.0.join("app/second-ledger.jsonl")).unwrap();
    assert!(probe.closed.load(Ordering::SeqCst), "the replaced ledger's database was closed");
    assert!(!probe.held.load(Ordering::SeqCst), "and not while the Host's state was held");
}

/// Round 2's reproduction: a records-tool notification (no request identity,
/// so never a request) and a fork whose source receipt names another records
/// project context take no project reading, as the parent read nothing there.
#[test]
fn records_notifications_and_mismatched_fork_inheritance_take_no_project_reading() {
    use std::sync::atomic::{AtomicUsize, Ordering};
    {
        let f = Fixture::new();
        let host = f.host(true, None, "account");
        f.start(&host, "fixture-model").unwrap();
        let generation = host.snapshot()["generation"].clone();
        let reads = Arc::new(AtomicUsize::new(0));
        let count = Arc::clone(&reads);
        *host.within_records_identity_read.lock().unwrap() = Some(Box::new(move || { count.fetch_add(1, Ordering::SeqCst); }));
        host.on_line(&serde_json::to_vec(&json!({"method":"item/tool/call","params":{"tool":crate::records_access::TOOL,"threadId":"thread","namespace":null}})).unwrap(), &generation);
        assert_eq!(reads.load(Ordering::SeqCst), 0, "a notification is never a records request");
        assert!(f.reads().is_empty());
        stop(&host);
    }
    {
        let f = Fixture::new();
        let host = f.host(true, None, "account");
        f.start(&host, "fixture-model").unwrap();
        let generation = host.snapshot()["generation"].clone();
        let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
        host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
        host.configure_records_capability_with_context(host.records_capability().unwrap(), ExplicitAppProjectContext::known("different explicit project", AppProjectSource::OpenedDirectory).unwrap());
        // The first reading taken, if any, is recorded with where it was taken.
        // The fork's own offer check (persist_records_receipt, which the parent
        // also read for) may read; receipt inheritance for another records
        // project context must not.
        let taken = Arc::new(std::sync::Mutex::new(None::<String>));
        let at = Arc::clone(&taken);
        *host.within_records_identity_read.lock().unwrap() = Some(Box::new(move || { *at.lock().unwrap() = Some(std::backtrace::Backtrace::force_capture().to_string()); }));
        host.thread_fork_finish(&request).unwrap();
        if let Some(trace) = taken.lock().unwrap().as_deref() {
            assert!(trace.contains("persist_records_receipt"), "the only reading is the fork's offer check, not receipt inheritance: {trace}");
        }
        assert!(!host.inner.0.lock().unwrap().records_receipts.iter().any(|(_, thread, _)| thread == "forked"));
        stop(&host);
    }
}

/// Every producer of a bound state says what the binding rests on, so the
/// view gives only the meaning that basis supports.
#[test]
fn every_bound_state_states_its_basis() {
    let binding = |host: &Host, thread: &str| host.snapshot()["threads"].as_array().unwrap().iter().rev()
        .find(|row| row["threadId"] == thread && row["generation"] == host.snapshot()["generation"]).map(|row| row["recordsCapabilityBinding"].clone()).unwrap_or(Value::Null);
    // A start with an explicit project context: a receipt.
    {
        let f = Fixture::new();
        let host = f.host(true, None, "account");
        f.start(&host, "fixture-model").unwrap();
        let bound = binding(&host, "thread");
        assert_eq!((bound["state"].as_str(), bound["basis"].as_str()), (Some("bound in current generation"), Some("receipt")), "{bound}");
        stop(&host);
        // A cold resume restored from that receipt: a receipt.
        drop(host);
        let cold = f.host(true, None, "account");
        let row = f.resume(&cold, "thread").unwrap();
        assert_eq!((row["recordsCapabilityBinding"]["state"].as_str(), row["recordsCapabilityBinding"]["basis"].as_str()), (Some("bound in current generation"), Some("receipt")), "{row}");
        stop(&cold);
    }
    // A hot start with no explicit project context: offered at its start, no receipt.
    {
        let f = Fixture::new();
        let host = f.host(true, None, "account");
        host.configure_records_capability(host.records_capability().unwrap());
        f.start(&host, "fixture-model").unwrap();
        let bound = binding(&host, "thread");
        assert_eq!((bound["state"].as_str(), bound["basis"].as_str()), (Some("bound in current generation"), Some("offer")), "{bound}");
        // A fork of it, with no receipt to inherit: admitted as a fork of an offered conversation.
        let generation = host.snapshot()["generation"].clone();
        let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
        host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
        let row = host.thread_fork_finish(&request).unwrap();
        let forked = row["threadId"].as_str().unwrap().to_owned();
        let bound = binding(&host, &forked);
        assert_eq!((bound["state"].as_str(), bound["basis"].as_str()), (Some("bound in current generation"), Some("fork of an offered conversation")), "{bound}");
        stop(&host);
    }
}

fn reads(host: &Host) -> usize {
    host.records_identity_reads.load(std::sync::atomic::Ordering::SeqCst)
}

/// thread_fork_finish: each refusal the old code gave under the state before
/// its project reading (a local provider's reported source, a fork already
/// admitted, a generation replaced or closed) takes no reading and gives the
/// old error. The checks and the look that decides the reading are one
/// function (fork_admission).
#[test]
fn fork_finish_refusals_before_its_reading_take_none_and_keep_their_errors() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    f.start(&host, "fixture-model").unwrap();
    let generation = host.snapshot()["generation"].clone();
    let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
    host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
    // The source holds a receipt for the current records project context, so
    // an admitted fork would read the project to inherit it.
    assert!(host.inner.0.lock().unwrap().records_receipts.iter().any(|(_, thread, _)| thread == "thread"));
    host.inner.0.lock().unwrap().local_provider = Some(access_provider::LocalProviderBinding::for_test("invented-local-home", "/invented/work"));
    let before = reads(&host);
    assert_eq!(host.thread_fork_finish(&request).unwrap_err(), crate::native_local_provider::LIMIT);
    assert_eq!(reads(&host), before, "a local provider's refusal takes no reading");
    host.inner.0.lock().unwrap().local_provider = None;
    let before = reads(&host);
    host.thread_fork_finish(&request).unwrap();
    assert!(reads(&host) > before, "an admitted fork that inherits a receipt reads the project");
    let before = reads(&host);
    assert_eq!(host.thread_fork_finish(&request).unwrap_err(), "forked thread already operationally admitted in generation");
    assert_eq!(reads(&host), before, "a duplicate finish takes no reading (round 3)");
    stop(&host);
    let before = reads(&host);
    assert_eq!(host.thread_fork_finish(&request).unwrap_err(), "thread/fork result belongs to a closed or replaced generation; native response retained");
    assert_eq!(reads(&host), before, "a finish after the generation closed takes no reading");
}

/// on_line: each condition under which the old receipt read nothing of the
/// project before deciding a records call (a generation replaced or closed;
/// not a server request; another tool or a namespace; a conversation not
/// offered it) takes no reading. The look that decides the reading is the
/// receipt's own projection (received_view) and the records branch's checks
/// (records_call_look). A records call that qualifies takes one.
#[test]
fn records_call_lines_the_receipt_would_not_take_as_records_calls_take_no_reading() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    f.start(&host, "fixture-model").unwrap();
    let generation = host.snapshot()["generation"].clone();
    let call = |id: &str, thread: &str| json!({"id":id,"method":"item/tool/call","params":{"tool":crate::records_access::TOOL,"threadId":thread,"turnId":"turn","callId":id,"namespace":null,"arguments":{}}});
    let stale = json!({"appSession":"stale", "home":"app-home:stale", "spawnCounter":1});
    let mut notification = call("n", "thread");
    notification.as_object_mut().unwrap().remove("id");
    let mut observation = call("o", "thread");
    observation["observation"] = json!("a frame carrying an observation is not a server request");
    let mut other_tool = call("t", "thread");
    other_tool["params"]["tool"] = json!("another_tool");
    let mut namespaced = call("s", "thread");
    namespaced["params"]["namespace"] = json!("a-namespace");
    let cases: [(&str, Value, &Value); 6] = [
        ("a generation replaced", call("g", "thread"), &stale),
        ("a notification", notification, &generation),
        ("an observation frame", observation, &generation),
        ("another tool", other_tool, &generation),
        ("a namespace", namespaced, &generation),
        ("a conversation not offered it", call("u", "unoffered"), &generation),
    ];
    for (case, frame, at) in cases {
        let before = reads(&host);
        host.on_line(&serde_json::to_vec(&frame).unwrap(), at);
        assert_eq!(reads(&host), before, "{case} takes no reading");
    }
    let before = reads(&host);
    f.tool(&host, "thread");
    assert!(reads(&host) > before, "a records call the receipt takes as one reads the project");
    stop(&host);
    let before = reads(&host);
    host.on_line(&serde_json::to_vec(&call("c", "thread")).unwrap(), &generation);
    assert_eq!(reads(&host), before, "a call on a closed generation takes no reading");
}

/// The receipt's persistence and binding: each refusal the old code gave
/// before its reading takes none. Persistence: the conversation out of scope,
/// or never offered the capability. Binding: a lookup that failed, the
/// conversation out of scope, or no capability configured.
#[test]
fn receipt_persistence_and_binding_refusals_before_their_reading_take_none() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    f.start(&host, "fixture-model").unwrap();
    let generation = host.snapshot()["generation"].clone();
    let stale = json!({"appSession":"stale", "home":"app-home:stale", "spawnCounter":1});
    for (case, generation, thread) in [("out of scope", &stale, "thread"), ("not a conversation of this generation", &generation, "unknown")] {
        let before = reads(&host);
        host.persist_records_receipt(generation, thread, Some("H-acct"));
        host.restore_records_receipt(generation, thread);
        assert_eq!(reads(&host), before, "{case}: persistence and binding take no reading");
    }
    // A conversation of this generation never offered the capability.
    host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":"unoffered"}));
    let before = reads(&host);
    host.persist_records_receipt(&generation, "unoffered", Some("H-acct"));
    assert_eq!(reads(&host), before, "never offered: persistence takes no reading");
    // No capability configured: the binding's look refuses before any reading.
    host.inner.0.lock().unwrap().records_capability = None;
    let before = reads(&host);
    host.restore_records_receipt(&generation, "thread");
    assert_eq!(reads(&host), before, "no capability configured: the binding takes no reading");
    stop(&host);
}

/// Round 4's case, inverted: the source's first receipt names another records
/// project context and a later one the current context. The old inheritance
/// took the first receipt and read nothing; the look that decides the reading
/// is now that same expression (inheritable_receipt), so the fork takes no
/// inheritance reading. The fork's own offer persistence still reads, as
/// before.
#[test]
fn a_fork_whose_first_source_receipt_is_of_another_context_takes_no_inheritance_reading() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    f.start(&host, "fixture-model").unwrap();
    let generation = host.snapshot()["generation"].clone();
    host.configure_records_capability_with_context(
        host.records_capability().unwrap(),
        ExplicitAppProjectContext::known("different explicit project", AppProjectSource::OpenedDirectory).unwrap(),
    );
    host.thread_start_selected(f.0.join("project").to_str().unwrap(), "fixture-model", "fixture-provider").unwrap();
    {
        let inner = host.inner.0.lock().unwrap();
        let context = inner.records_project_context.as_ref().and_then(|c| c.reference());
        let receipts = inner.records_receipts.iter().filter(|(g, thread, _)| g == &generation && thread == "thread").collect::<Vec<_>>();
        assert_eq!(receipts.len(), 2, "both receipts for the source are held");
        assert_ne!(context, Some(receipts[0].2.project.as_str()), "the first is of another context");
        assert_eq!(context, Some(receipts[1].2.project.as_str()), "a later one is of the current context");
    }
    let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
    host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
    let taken = Arc::new(std::sync::Mutex::new(None::<String>));
    let at = Arc::clone(&taken);
    *host.within_records_identity_read.lock().unwrap() = Some(Box::new(move || {
        *at.lock().unwrap() = Some(std::backtrace::Backtrace::force_capture().to_string());
    }));
    let before = reads(&host);
    host.thread_fork_finish(&request).unwrap();
    assert_eq!(reads(&host) - before, 1, "only the fork's offer persistence reads");
    let trace = taken.lock().unwrap().clone().expect("the offer persistence reads");
    assert!(trace.contains("persist_records_receipt"), "the one reading is the offer persistence, not inheritance: {trace}");
    assert!(!host.inner.0.lock().unwrap().records_receipts.iter().any(|(_, thread, _)| thread == "forked"), "nothing is inherited");
    stop(&host);
}

/// The fork's reading is bound to the receipt and context its look selected:
/// the records project context changed while the project was read, the
/// selection after the reading differs, and nothing is admitted.
#[test]
fn a_fork_whose_selected_receipt_or_context_changes_during_its_reading_is_refused() {
    let f = Fixture::new();
    let host = f.host(true, None, "account");
    f.start(&host, "fixture-model").unwrap();
    let generation = host.snapshot()["generation"].clone();
    let request = host.thread_fork_dispatch(&generation, "thread").unwrap();
    host.source_request_wait(&request, Duration::from_secs(2)).unwrap();
    let during = Arc::clone(&host);
    *host.within_records_identity_read.lock().unwrap() = Some(Box::new(move || {
        during.configure_records_capability_with_context(during.records_capability().unwrap(), ExplicitAppProjectContext::known("different explicit project", AppProjectSource::OpenedDirectory).unwrap());
    }));
    assert_eq!(host.thread_fork_finish(&request).unwrap_err(), "thread/fork records project reading no longer matches the admission it was taken for; native response retained");
    assert!(!host.inner.0.lock().unwrap().threads.iter().any(|row| row["generation"] == generation && row["threadId"] == "forked"), "nothing is admitted");
    stop(&host);
}
