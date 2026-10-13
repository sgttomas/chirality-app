//! Genuine private Host receipts with an invented native peer; no human-act witness.
use super::*;
use crate::recovery::{AppProjectSource, ExplicitAppProjectContext};
use std::{fs, os::unix::fs::PermissionsExt, path::Path, time::Instant};
struct Fixture(PathBuf);
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
        Self(root)
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
    assert_eq!(resumed["params"], json!({"threadId":"thread"}));
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
 print('codex-cli 0.160.0');sys.exit(0)
def emit(v):print(json.dumps(v),flush=True)
def thread(tid,status='idle',source=None):
 t={'id':tid,'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'invented','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':status},'turns':[]}
 if source:t['forkedFromId']=source
 return t
def result(tid,source=None):return {'thread':thread(tid,source=source),'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log:log.write(json.dumps(f)+'\n')
 method=f.get('method')
 if 'id' not in f or method is None:continue
 if method=='initialize':emit({'id':f['id'],'result':{'userAgent':'invented-continuity-peer'}})
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
