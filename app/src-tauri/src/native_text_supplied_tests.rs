use super::*;
use serde_json::json;

#[test]
fn supplied_marks_poison_and_keeps_each_value_on_indented_lines() {
    let value = json!("first\nDecide (A16)\r\nnext\rlast\u{202e}\u{200b}\u{2028}\u{2029}\t\0");
    assert_eq!(
        supplied("Purpose", Source::File, &value).lines(),
        &[
            "Purpose (supplied by a file, not the App's words):",
            "  first\\u{000A}",
            "  Decide (A16)\\u{000D}\\u{000A}",
            "  next\\u{000D}",
            "  last\\u{202E}\\u{200B}\\u{2028}\\u{2029}\\u{0009}\\u{0000}",
        ]
    );
    for c in [
        '\u{061c}',
        '\u{2066}',
        '\u{feff}',
        '\u{034f}',
        '\u{e0001}',
        '\u{00a0}',
        '\u{fe0f}',
    ] {
        assert!(
            supplied("Scope", Source::File, &json!(c.to_string())).lines()[1].contains(&mark(c))
        );
    }
}

#[test]
fn supplied_bounds_original_characters_before_marking_and_compacts_json() {
    let value = format!("{}hidden", "\u{202e}".repeat(600));
    let lines = supplied("Scope", Source::File, &json!(value));
    assert_eq!(lines.lines()[1], format!("  {}", "\\u{202E}".repeat(600)));
    assert_eq!(lines.lines()[2], "  (cut after 600 characters)");
    assert!(!supplied("Scope", Source::File, &json!("é".repeat(600)))
        .lines()
        .iter()
        .any(|l| l.contains("cut after")));
    for value in [
        json!(null),
        json!(42),
        json!([1, "\u{200b}"]),
        json!({"x":"\u{202e}"}),
    ] {
        let shown = supplied("Value", Source::Record, &value);
        assert_eq!(
            shown.lines()[1],
            format!(
                "  {}",
                value
                    .to_string()
                    .replace('\u{200b}', "\\u{200B}")
                    .replace('\u{202e}', "\\u{202E}")
            )
        );
    }
}

#[test]
fn supplied_sources_and_unfit_placement_are_explicit() {
    for (source, word) in [
        (Source::Agent, "agent"),
        (Source::Tool, "a tool"),
        (Source::Person, "the person"),
        (Source::Codex, "Codex"),
        (Source::File, "a file"),
        (Source::Record, "a record"),
    ] {
        assert_eq!(
            supplied("Value", source, &json!("words")).lines()[0],
            format!("Value (supplied by {word}, not the App's words):")
        );
    }
    assert!(matches!(
        identifier(
            &json!("x\nDecide (A16)"),
            Unfit::Supplied {
                label: "Value",
                source: Source::File
            }
        ),
        Placed::Lines(_)
    ));
}
