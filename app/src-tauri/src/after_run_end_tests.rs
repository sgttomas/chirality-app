//! Invented records/captures only; no native person/supplier witness.
use super::*;
#[test]
fn after_run_end_orders_valid_rfc3339_instants_without_rewriting_text() {
    let utc = instant("2026-10-13T12:00:00.123Z").unwrap();
    assert_eq!(instant("2026-10-13T14:30:00.123+02:30"), Some(utc));
    assert!(instant("2026-10-13T12:00:00.123000001Z").unwrap() > utc);
    for bad in [
        "bad",
        "2026-02-30T12:00:00Z",
        "2026-10-13T-1:00:00Z",
        "2026-10-13T12:00:60Z",
        "2026-10-13T12:00:00-00:00",
        "2026-10-13T12:00:00.1234567890Z",
        "2026-10-13T12:00:00+-1:00",
    ] {
        assert_eq!(instant(bad), None, "{bad}");
    }
}
#[test]
fn after_run_end_subject_is_historical_and_never_follows_a_path() {
    let root = Path::new("/invented/project");
    let arrival = json!({"body":{"referents":[{"subject":"output summary: file out/summary.md"}]}});
    assert_eq!(subjects(root, &arrival), vec![root.join("out/summary.md")]);
    for bad in [
        "output summary: file ../outside",
        "output summary: file /outside",
        "output a: file ambiguous: file out/a",
    ] {
        assert!(subjects(root, &json!({"body":{"referents":[{"subject":bad}]}})).is_empty());
    }
}
