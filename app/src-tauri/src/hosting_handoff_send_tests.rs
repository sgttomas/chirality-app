use super::*;
use crate::hosting::HandoffSendObservation;

#[test]
fn handoff_receipt_uses_its_actual_source_and_keeps_native_error_distinct() {
    for failed in [false, true] {
        let host = host();
        let mut retained = None;
        let response = if failed {
            json!({"error":{"code":-32600,"message":"refused-not-sent is only quoted native text"}})
        } else {
            json!({"result":{"turn":turn("inProgress")}})
        };
        let (result, _) = exchange(&host, Some(response), vec![], || {
            let source = host.handoff_text_begin(&g(), "thread", "exact text")?;
            retained = Some(source.clone());
            host.handoff_text_wait(&source, Duration::from_millis(100));
            assert!(host.handoff_source_current(&source));
            Ok(Value::Null)
        });
        result.unwrap();
        let source = retained.unwrap();
        assert!(
            !host.handoff_source_current(&source),
            "closing the original pipe does not attach this receipt to another source"
        );
        let observation = host.handoff_send_observation(&source, &g(), "thread", "exact text");
        assert!(if failed {
            matches!(observation, HandoffSendObservation::NativeFailed(_))
        } else {
            matches!(observation, HandoffSendObservation::Sent(_))
        });
        assert!(matches!(
            host.handoff_send_observation(&source, &g(), "thread", "different edited text"),
            HandoffSendObservation::Unknown(_)
        ));
        let foreign = super::host();
        assert!(matches!(
            foreign.handoff_send_observation(&source, &g(), "thread", "exact text"),
            HandoffSendObservation::Unknown(_)
        ));
    }
}

#[test]
fn handoff_actual_partial_pipe_write_is_unknown_and_keeps_its_original_source() {
    let host = host();
    let mut child = Command::new("/usr/bin/python3")
        .args([
            "-c",
            "import sys; data=sys.stdin.buffer.read(512); print(len(data),flush=True)",
        ])
        .env_clear()
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    *host.stdin.lock().unwrap() = child.stdin.take();
    let text = "x".repeat(2 * 1024 * 1024);
    let source = host.handoff_text_begin(&g(), "thread", &text).unwrap();
    *host.stdin.lock().unwrap() = None;
    let output = child.wait_with_output().unwrap();
    assert!(output.status.success());
    assert_eq!(String::from_utf8(output.stdout).unwrap().trim(), "512");
    assert_eq!(source.evidence()["actualWriteAttemptObserved"], true);
    assert_eq!(source.evidence()["writeResult"], "write-failed");
    host.handoff_text_wait(&source, Duration::from_millis(1));
    assert!(matches!(
        host.handoff_send_observation(&source, &g(), "thread", &text),
        HandoffSendObservation::Unknown(_)
    ));
}
