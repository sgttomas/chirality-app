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
use std::sync::atomic::{AtomicBool, Ordering};
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

/// Adds the page-load hook to the App's builder. The App has no other page-load hook.
pub fn install<R: Runtime>(builder: Builder<R>) -> Builder<R> {
    stage("process started", json!({ "pid": std::process::id() }));
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
            stage("script evaluated", json!({ "attempt": attempt, "returned": read, "windows": windows }));
            std::process::exit(if heading.is_some() { 0 } else { 5 });
        }
        std::thread::sleep(WAIT);
    }
}
