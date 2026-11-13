//! The scripted driver's first step: a hosted proof that a test build's window loads its page and runs a script.
//!
//! Compiled only when build.rs sets cfg `chirality_scripted_driver` (CHIRALITY_SCRIPTED_DRIVER_BUILD=1), which it
//! refuses together with the release feature; a test build only, never in the shipped App. See
//! app/examination/scripted_driver/README.md for what it is approved for, and what it does not establish.
//!
//! It writes one line per stage to `$HOME/scripted-driver/stages.jsonl` as each happens, so a run that stops says
//! where: the process started; the web view started loading its page; the load finished; the script was evaluated
//! and what it returned. It then ends the process itself. It operates no control and changes nothing in the page.

#[cfg(feature = "distribution-successor")]
compile_error!("the scripted driver is a test build only; it is refused with the release feature distribution-successor");

use serde_json::{json, Value};
use std::io::Write;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tauri::webview::PageLoadEvent;
use tauri::{Builder, Manager, Runtime};

/// Present in a test build's binary and in every stage line; a release build must not contain it.
pub const MARKER: &str = "chirality-scripted-driver-test-build-v1";

/// What the script reads: nothing is clicked, typed or changed. It is evaluated again until the page's first heading
/// is present (the page renders after load), at most `TRIES` times, `WAIT` apart.
const PROOF: &str = r#"(() => {
  const heading = document.querySelector('h1, h2, [role="heading"]');
  return { title: document.title, href: String(location.href), ready: document.readyState,
           heading: heading ? heading.textContent.trim() : null,
           buttons: document.querySelectorAll('button').length,
           open_dialogs: document.querySelectorAll('dialog[open], [role="dialog"], [role="alertdialog"]').length };
})()"#;
const TRIES: u32 = 60;
const WAIT: Duration = Duration::from_millis(500);

fn folder() -> Option<PathBuf> {
    std::env::var_os("HOME").filter(|home| !home.is_empty()).map(|home| PathBuf::from(home).join("scripted-driver"))
}

/// One stage, appended as one line. A stage that cannot be written is said on stderr; the run then shows no report.
pub fn stage(name: &str, detail: Value) {
    let at_ms = SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_millis() as u64).unwrap_or(0);
    let line = json!({ "marker": MARKER, "stage": name, "at_ms": at_ms, "detail": detail }).to_string();
    let written = folder().ok_or("HOME is not set").and_then(|dir| {
        std::fs::create_dir_all(&dir).map_err(|_| "the report folder could not be made")?;
        let mut file = std::fs::OpenOptions::new().create(true).append(true).open(dir.join("stages.jsonl"))
            .map_err(|_| "the stages file could not be opened")?;
        writeln!(file, "{line}").map_err(|_| "the stage could not be written")?;
        file.sync_all().map_err(|_| "the stage could not be flushed")
    });
    if let Err(reason) = written {
        eprintln!("{MARKER}: {reason}");
    }
}

/// Every window and web view Tauri notifies as created in this process, counted in its creation notification (not
/// sampled). A second one of either ends the run at once, in that notification, before anything else is written.
static WINDOWS_CREATED: AtomicUsize = AtomicUsize::new(0);
static WEBVIEWS_CREATED: AtomicUsize = AtomicUsize::new(0);

fn created() -> Value {
    json!({ "windows_ever_created": WINDOWS_CREATED.load(Ordering::SeqCst),
            "webviews_ever_created": WEBVIEWS_CREATED.load(Ordering::SeqCst) })
}

fn exactly_one_each() -> bool {
    WINDOWS_CREATED.load(Ordering::SeqCst) == 1 && WEBVIEWS_CREATED.load(Ordering::SeqCst) == 1
}

/// The run's last act, on the main thread, where Tauri also runs its creation notifications: so the counts are read,
/// the final stage written and the process ended in one step, after any notification already queued.
fn finish_on_main<R: Runtime>(app: &tauri::AppHandle<R>, finish: impl FnOnce() -> i32 + Send + 'static) -> ! {
    if app.run_on_main_thread(move || std::process::exit(finish())).is_err() {
        stage("finish not run", json!({ "reason": "the main thread could not be reached" }));
        std::process::exit(11);
    }
    loop {
        std::thread::park();
    }
}

/// Adds the page-load hook to the App's builder (the App has no other), and a plugin with no commands whose only
/// work is to count the windows and web views created.
pub fn install<R: Runtime>(builder: Builder<R>) -> Builder<R> {
    stage("process started", json!({ "pid": std::process::id() }));
    let counter = tauri::plugin::Builder::<R>::new("scripted-driver-count")
        .on_window_ready(|window| {
            let n = WINDOWS_CREATED.fetch_add(1, Ordering::SeqCst) + 1;
            stage("window created", json!({ "label": window.label(), "windows_ever_created": n }));
            if n > 1 {
                stage("run ended: a second window", json!({ "windows_ever_created": n }));
                std::process::exit(10);
            }
        })
        .on_webview_ready(|webview| {
            let n = WEBVIEWS_CREATED.fetch_add(1, Ordering::SeqCst) + 1;
            stage("web view created", json!({ "label": webview.label(), "webviews_ever_created": n }));
            if n > 1 {
                stage("run ended: a second web view", json!({ "webviews_ever_created": n }));
                std::process::exit(10);
            }
        })
        .build();
    let builder = builder.plugin(counter);
    let started = Arc::new(AtomicBool::new(false));
    let finished = Arc::new(AtomicBool::new(false));
    builder.on_page_load(move |webview, payload| {
        let windows = webview.app_handle().webview_windows().len();
        match payload.event() {
            PageLoadEvent::Started => {
                if !started.swap(true, Ordering::SeqCst) {
                    stage("page load started", json!({ "url": payload.url().as_str(), "windows": windows }));
                }
            }
            PageLoadEvent::Finished => {
                if finished.swap(true, Ordering::SeqCst) {
                    return;
                }
                stage("page load finished", json!({ "url": payload.url().as_str(), "windows": windows }));
                let webview = webview.clone();
                std::thread::spawn(move || evaluate(webview));
            }
        }
    })
}

fn evaluate<R: Runtime>(webview: tauri::Webview<R>) {
    for attempt in 1..=TRIES {
        let (sender, receiver) = std::sync::mpsc::channel();
        if let Err(error) = webview.eval_with_callback(PROOF, move |result| { let _ = sender.send(result); }) {
            stage("script not sent", json!({ "attempt": attempt, "error": error.to_string() }));
            std::process::exit(3);
        }
        let returned = match receiver.recv_timeout(Duration::from_secs(10)) {
            Ok(text) => text,
            Err(_) => {
                stage("script sent, no result", json!({ "attempt": attempt }));
                std::process::exit(4);
            }
        };
        let read: Value = serde_json::from_str(&returned).unwrap_or(Value::String(returned));
        let heading = read.get("heading").and_then(Value::as_str).map(str::to_owned);
        if heading.is_some() || attempt == TRIES {
            let windows = webview.app_handle().webview_windows().len();
            stage("script evaluated", json!({ "attempt": attempt, "returned": read, "windows": windows, "created": created() }));
            if heading.is_none() {
                std::process::exit(5);
            }
            match scenario_input() {
                None => finish_on_main(webview.app_handle(), || {
                    let ever = created();
                    let one = exactly_one_each();
                    stage("proof finished", json!({ "created": ever, "exactly_one_each": one }));
                    if one { 0 } else { 10 }
                }),
                Some(Ok(input)) => walk(&webview, input),
                Some(Err(reason)) => {
                    stage("scenario not started", json!({ "reason": reason }));
                    std::process::exit(9);
                }
            }
        }
        std::thread::sleep(WAIT);
    }
}

/// The scenario walk (app/examination/scripted_driver/page.js, judged by judge.js), when the runner has put
/// `scenario.json` ({scenario, values}) beside the stages. Absent, the run is the proof alone.
const JUDGE: &str = include_str!("../../examination/scripted_driver/judge.js");
const PAGE: &str = include_str!("../../examination/scripted_driver/page.js");
const WALK_LIMIT: Duration = Duration::from_secs(120);

fn scenario_input() -> Option<Result<Value, String>> {
    let path = folder()?.join("scenario.json");
    if !path.exists() {
        return None;
    }
    Some(std::fs::read_to_string(&path).map_err(|_| "scenario.json could not be read".to_owned())
        .and_then(|text| serde_json::from_str::<Value>(&text).map_err(|_| "scenario.json is not JSON".to_owned())))
}

fn walk<R: Runtime>(webview: &tauri::Webview<R>, input: Value) -> ! {
    let start = format!("{JUDGE}\n{PAGE}\nwindow.__chiralityDriverRun({input}); 'started'");
    if let Err(error) = webview.eval(start) {
        stage("scenario not started", json!({ "error": error.to_string() }));
        std::process::exit(9);
    }
    stage("scenario started", json!({}));
    let began = std::time::Instant::now();
    let mut most_windows = 0;
    while began.elapsed() < WALK_LIMIT {
        std::thread::sleep(WAIT);
        most_windows = most_windows.max(webview.app_handle().webview_windows().len());
        let (sender, receiver) = std::sync::mpsc::channel();
        let asked = webview.eval_with_callback("window.__chiralityDriver && window.__chiralityDriver.done ? window.__chiralityDriver : null",
            move |result| { let _ = sender.send(result); });
        let Ok(text) = (if asked.is_ok() { receiver.recv_timeout(Duration::from_secs(10)).map_err(|_| ()) } else { Err(()) }) else { continue };
        let read: Value = serde_json::from_str(&text).unwrap_or(Value::Null);
        if read.is_null() {
            continue;
        }
        let verdict = read.get("verdict").and_then(Value::as_str).unwrap_or("").to_owned();
        finish_on_main(webview.app_handle(), move || {
            let ever = created();
            let one = exactly_one_each() && most_windows == 1;
            stage("scenario finished", json!({ "result": read, "most_windows": most_windows, "created": ever,
                                               "exactly_one_each": one }));
            match verdict.as_str() { "pass" if one => 0, "pass" | "fail" => 6, _ => 7 }
        });
    }
    stage("scenario did not finish", json!({ "seconds": WALK_LIMIT.as_secs(), "most_windows": most_windows, "created": created() }));
    std::process::exit(8);
}
