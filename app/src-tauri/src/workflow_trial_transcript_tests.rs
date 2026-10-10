//! Tests for WR §4.2 TT-10 (transcript) and TT-11 (Compare) pure functions.
use super::*;
use serde_json::json;

const RUN_TEXT: &str = "Follow the workflow steps below.\nStep 1: read the brief.";

fn trial_source() -> TranscriptSource {
    TranscriptSource::Trial {
        sequence: 3,
        draft_name: "review-brief".into(),
        rev12: "0123456789ab".into(),
        clean: true,
        thread: "thr-clean".into(),
    }
}

fn run_source() -> TranscriptSource {
    TranscriptSource::Run {
        run: "run-7".into(),
        origin: "local".into(),
        name: "review-brief".into(),
        rev12: "ba9876543210".into(),
        thread: "thr-run".into(),
    }
}

fn trial_line() -> TrialTextLine {
    TrialTextLine { run_text: RUN_TEXT.into(), line: "[trial text 3 · sha256 abcd · as composed]".into() }
}

fn input<'a>(source: TranscriptSource, turns: &'a [TurnRead]) -> TranscriptInput<'a> {
    TranscriptInput {
        source,
        read_at: "2026-10-10T12:00:00Z".into(),
        turns,
        turns_limit: None,
        trial_text: Some(trial_line()),
        include_native: false,
        bound: TRANSCRIPT_BOUND,
    }
}

fn cmd(command: &str, exit: Value, dur: Value, out: Value, status: &str) -> Value {
    json!({"type":"commandExecution","id":"c","command":command,"commandActions":[],"cwd":"/w",
           "exitCode":exit,"durationMs":dur,"aggregatedOutput":out,"status":status})
}

fn turn(id: &str, status: &str, items: Vec<Value>) -> TurnRead {
    TurnRead { turn: json!({"id":id,"items":[],"status":status}), items: Ok(items) }
}

/// A trial history: trial text, agent message, commands, file change, plan,
/// a native reasoning item; second turn failed with an error.
fn trial_turns() -> Vec<TurnRead> {
    vec![
        turn(
            "t-1",
            "completed",
            vec![
                json!({"type":"userMessage","id":"u1","content":[
                    {"type":"text","text":format!("[Chirality] Trial header\n{RUN_TEXT}")},
                    {"type":"text","text":"Please be brief."},
                    {"type":"localImage","path":"/x.png"}]}),
                json!({"type":"reasoning","id":"r1","summary":["thinking"]}),
                json!({"type":"agentMessage","id":"a1","text":"Reading the brief."}),
                cmd("ls", json!(0), json!(12), json!("a.txt\nb.txt\n"), "completed"),
                cmd("false", json!(1), Value::Null, Value::Null, "failed"),
                json!({"type":"fileChange","id":"f1","status":"completed","changes":[
                    {"path":"out/report.md","kind":{"type":"add"},"diff":""},
                    {"path":"old.md","kind":{"type":"update","move_path":"new.md"},"diff":""}]}),
                json!({"type":"plan","id":"p1","text":"1. read 2. write"}),
                json!({"type":"agentMessage","id":"a2","text":"Done with turn one."}),
            ],
        ),
        TurnRead {
            turn: json!({"id":"t-2","items":[],"status":"failed","error":{"message":"model overloaded"}}),
            items: Ok(vec![json!({"type":"userMessage","id":"u2","content":[{"type":"text","text":"Continue."}]})]),
        },
    ]
}

const TRIAL_GOLDEN: &str = "[Chirality] Trial 3 of draft review-brief @ 0123456789ab: transcript read from Codex history at 2026-10-10T12:00:00Z (clean conversation thr-clean). A record of that conversation; it instructs nothing.
Turn 1 (t-1)
Person: [trial text 3 · sha256 abcd · as composed]
Person: Please be brief.
Person: [localImage]
Agent: Reading the brief.
Command: ls (exit 0, 12 ms)
  a.txt
  b.txt
Command: false (exit 1, duration not reported ms)
  (no output)
File change: out/report.md (add)
File change: old.md (update, moved to new.md)
Plan: 1. read 2. write
Agent: Done with turn one.
Native items not included: 1 (tick \"include native items\" to include them)
Turn ended: completed
Turn 2 (t-2)
Person: Continue.
Turn ended: failed — model overloaded";

#[test]
fn trial_transcript_golden() {
    let turns = trial_turns();
    let t = compose_transcript(&input(trial_source(), &turns));
    assert_eq!(t.text, TRIAL_GOLDEN);
    assert!(t.shortenings.is_empty());
    assert!(!t.text.ends_with('\n'));
}

#[test]
fn trial_text_is_replaced_by_its_line() {
    let turns = trial_turns();
    let t = compose_transcript(&input(trial_source(), &turns));
    assert!(!t.text.contains("Step 1: read the brief."));
    assert!(t.text.contains("Person: [trial text 3 · sha256 abcd · as composed]"));
    // Without a trial text line the message is reproduced.
    let mut i = input(trial_source(), &turns);
    i.trial_text = None;
    assert!(compose_transcript(&i).text.contains("Step 1: read the brief."));
}

#[test]
fn delegated_trial_header_names_sub_agent() {
    let turns: Vec<TurnRead> = Vec::new();
    let src = TranscriptSource::Trial {
        sequence: 1,
        draft_name: "d".into(),
        rev12: "r".into(),
        clean: false,
        thread: "thr-sub".into(),
    };
    let t = compose_transcript(&input(src, &turns));
    assert_eq!(
        t.text,
        "[Chirality] Trial 1 of draft d @ r: transcript read from Codex history at 2026-10-10T12:00:00Z (sub-agent thr-sub). A record of that conversation; it instructs nothing."
    );
}

#[test]
fn include_native_shows_items_as_compact_json() {
    let turns = trial_turns();
    let mut i = input(trial_source(), &turns);
    i.include_native = true;
    let t = compose_transcript(&i);
    assert!(t.text.contains("Native item reasoning: {\"id\":\"r1\",\"summary\":[\"thinking\"],\"type\":\"reasoning\"}"));
    assert!(!t.text.contains("Native items not included"));
    // Placed in item order: after the person's messages, before the agent.
    let pos_n = t.text.find("Native item reasoning").unwrap();
    assert!(t.text.find("Person: [localImage]").unwrap() < pos_n);
    assert!(pos_n < t.text.find("Agent: Reading the brief.").unwrap());
}

#[test]
fn run_transcript_golden_with_limits() {
    let turns = vec![
        turn(
            "r-1",
            "completed",
            vec![
                json!({"type":"userMessage","id":"u","content":[{"type":"text","text":"Start."}]}),
                cmd("cargo test", json!(101), json!(4500), json!("error: failed"), "completed"),
                json!({"type":"webSearch","id":"w","query":"q"}),
                json!({"type":"mcpToolCall","id":"m","server":"s","tool":"t","arguments":{},"status":"completed"}),
            ],
        ),
        TurnRead { turn: json!({"id":"r-2","status":"interrupted"}), items: Err("page 2 failed: timeout".into()) },
    ];
    let mut i = input(run_source(), &turns);
    i.turns_limit = Some("thread/turns/list page 3 failed".into());
    let t = compose_transcript(&i);
    assert_eq!(
        t.text,
        "[Chirality] Run run-7 of local:review-brief revision ba9876543210 (registered): transcript read from Codex history at 2026-10-10T12:00:00Z (conversation thr-run). A record of that conversation; it instructs nothing.
Turns list incomplete: thread/turns/list page 3 failed; later turns were not read.
Turn 1 (r-1)
Person: Start.
Command: cargo test (exit 101, 4500 ms)
  error: failed
Native items not included: 2 (tick \"include native items\" to include them)
Turn ended: completed
Turn 2 (r-2)
Turn items incomplete: page 2 failed: timeout; nothing is invented for this turn.
Turn ended: interrupted"
    );
}

#[test]
fn missing_fields_are_tolerated() {
    let turns = vec![TurnRead {
        turn: json!({}),
        items: Ok(vec![
            json!({"type":"commandExecution"}),
            json!({"type":"fileChange","changes":[{}]}),
            json!({"type":"agentMessage"}),
            json!({}),
        ]),
    }];
    let t = compose_transcript(&input(run_source(), &turns));
    assert!(t.text.contains("Turn 1 (id not reported)"));
    assert!(t.text.contains("Command: command not reported (exit not reported, duration not reported ms)\n  (no output)"));
    assert!(t.text.contains("File change: path not reported (kind not reported)"));
    assert!(t.text.contains("Native items not included: 1"));
    assert!(t.text.ends_with("Turn ended: not reported"));
}

#[test]
fn deterministic_for_equal_input() {
    let turns = trial_turns();
    let mut i = input(trial_source(), &turns);
    i.include_native = true;
    let a = compose_transcript(&i);
    let b = compose_transcript(&i.clone());
    assert_eq!(a, b);
    let mut small = i.clone();
    small.bound = 300;
    assert_eq!(compose_transcript(&small), compose_transcript(&small.clone()));
}

fn big_output_turns() -> Vec<TurnRead> {
    // Outputs of 5000 and 3000 bytes (multibyte chars around the cut).
    let out1 = format!("{}é{}", "x".repeat(1999), "y".repeat(2999));
    let out2 = "z".repeat(3000);
    vec![
        turn("t-1", "completed", vec![cmd("one", json!(0), json!(1), json!(out1), "completed")]),
        turn("t-2", "completed", vec![cmd("two", json!(0), json!(1), json!(out2), "completed")]),
    ]
}

#[test]
fn bound_a_cuts_long_outputs_on_char_boundary() {
    let turns = big_output_turns();
    let mut i = input(run_source(), &turns);
    i.trial_text = None;
    i.bound = 6000;
    let t = compose_transcript(&i);
    assert!(t.text.len() <= 6000);
    // 1999 x's then 'é' (2 bytes) would cross 2000: cut keeps 1999 bytes.
    let line = format!("  {}\n  … {} bytes omitted", "x".repeat(1999), 5000 - 1999);
    assert!(t.text.contains(&line), "{}", t.text);
    assert!(t.text.contains(&format!("  {}\n  … 1000 bytes omitted", "z".repeat(2000))));
    assert_eq!(t.shortenings, vec!["… 3001 bytes omitted".to_string(), "… 1000 bytes omitted".to_string()]);
    for s in &t.shortenings {
        assert!(t.text.contains(s.as_str()));
    }
    // Without a bound problem nothing is cut.
    i.bound = TRANSCRIPT_BOUND;
    assert!(compose_transcript(&i).shortenings.is_empty());
}

#[test]
fn bound_b_omits_outputs_earliest_first() {
    let turns = big_output_turns();
    let mut i = input(run_source(), &turns);
    i.trial_text = None;
    let full_header = compose_transcript(&input(run_source(), &[])).text.len();
    // Room for the second turn's cut output but not both.
    i.bound = full_header + 2300;
    let t = compose_transcript(&i);
    assert!(t.text.len() <= i.bound, "{} > {}", t.text.len(), i.bound);
    assert!(t.text.contains("Command: one (exit 0, 1 ms)\n  … 5000 bytes omitted\n"));
    assert!(t.text.contains(&format!("  {}\n  … 1000 bytes omitted", "z".repeat(2000))));
    assert_eq!(t.shortenings, vec!["… 5000 bytes omitted".to_string(), "… 1000 bytes omitted".to_string()]);
    assert!(!t.text.contains("later turns omitted"));
}

#[test]
fn bound_c_ends_at_turn_boundary() {
    let turns = big_output_turns();
    let mut i = input(run_source(), &turns);
    let header = compose_transcript(&input(run_source(), &[])).text.len();
    i.bound = header + 150;
    let t = compose_transcript(&i);
    assert!(t.text.len() <= i.bound);
    assert!(t.text.contains("Turn 1 (t-1)\nCommand: one (exit 0, 1 ms)\n  … 5000 bytes omitted\nTurn ended: completed\n"));
    assert!(t.text.ends_with("\nlater turns omitted: 1; open the conversation to read them"));
    assert!(!t.text.contains("Turn 2"));
    assert_eq!(
        t.shortenings,
        vec!["… 5000 bytes omitted".to_string(), "later turns omitted: 1; open the conversation to read them".to_string()]
    );
}

#[test]
fn bound_c_keeps_zero_turns_for_one_enormous_message() {
    let turns = vec![
        turn("t-1", "completed", vec![json!({"type":"agentMessage","id":"a","text":"w".repeat(500_000)})]),
        turn("t-2", "completed", vec![json!({"type":"agentMessage","id":"b","text":"short"})]),
    ];
    let t = compose_transcript(&input(trial_source(), &turns));
    assert!(t.text.len() <= TRANSCRIPT_BOUND);
    let lines: Vec<&str> = t.text.split('\n').collect();
    assert_eq!(lines.len(), 2);
    assert!(lines[0].starts_with("[Chirality] Trial 3"));
    assert_eq!(lines[1], "later turns omitted: 2; open the conversation to read them");
}

#[test]
fn header_alone_too_long_is_truncated() {
    let turns = trial_turns();
    let mut i = input(trial_source(), &turns);
    i.bound = 40;
    let t = compose_transcript(&i);
    assert_eq!(t.text, "[Chirality] Trial 3 of draft review-brie");
    assert_eq!(t.shortenings.len(), 1);
}

#[test]
fn never_exceeds_bound() {
    let mut turns = trial_turns();
    turns.extend(big_output_turns());
    turns.push(turn("t-9", "completed", vec![json!({"type":"agentMessage","id":"a","text":"é".repeat(3000)})]));
    let full = compose_transcript(&input(trial_source(), &turns)).text.len();
    for bound in [0, 1, 10, 100, 250, 300, 500, 1000, 2500, 4000, 6000, 9000, 12000, full - 1, full, full + 1] {
        for native in [false, true] {
            let mut i = input(trial_source(), &turns);
            i.bound = bound;
            i.include_native = native;
            let t = compose_transcript(&i);
            assert!(t.text.len() <= bound, "bound {bound}: {}", t.text.len());
        }
    }
    let mut i = input(trial_source(), &turns);
    i.bound = full;
    assert!(compose_transcript(&i).shortenings.is_empty());
}

// ---- version_difference ----

fn files(entries: &[(&str, &[u8])]) -> BTreeMap<String, Vec<u8>> {
    entries.iter().map(|(p, b)| (p.to_string(), b.to_vec())).collect()
}

#[test]
fn version_difference_text_files() {
    let before = files(&[
        ("same.md", b"keep\n"),
        ("WORKFLOW.md", b"a\nb\nc\nd\n"),
        ("gone.txt", b"x\ny\n"),
    ]);
    let after = files(&[
        ("same.md", b"keep\n"),
        ("WORKFLOW.md", b"a\nB\nc\nd\ne\n"),
        ("new.txt", b"n1\nn2"),
    ]);
    let d = version_difference(&before, &after);
    assert_eq!(d["unchanged"], 1);
    assert_eq!(d["standing"], "difference between the two versions' files; scores and judges nothing");
    let fs = d["files"].as_array().unwrap();
    let paths: Vec<&str> = fs.iter().map(|f| f["path"].as_str().unwrap()).collect();
    assert_eq!(paths, vec!["WORKFLOW.md", "gone.txt", "new.txt"]);
    assert_eq!(fs[0]["change"], "changed");
    assert_eq!(fs[0]["lines"], json!(["- b", "+ B", "+ e"]));
    assert_eq!(fs[0]["text"], true);
    assert_eq!(fs[0]["limit"], Value::Null);
    assert_eq!(fs[0]["before"], json!({"bytes":8,"sha256":crate::util::sha256_hex(b"a\nb\nc\nd\n")}));
    assert_eq!(fs[1]["change"], "removed");
    assert_eq!(fs[1]["after"], Value::Null);
    assert_eq!(fs[1]["lines"], json!(["- x", "- y"]));
    assert_eq!(fs[2]["change"], "added");
    assert_eq!(fs[2]["before"], Value::Null);
    assert_eq!(fs[2]["lines"], json!(["+ n1", "+ n2"]));
}

#[test]
fn version_difference_lcs_is_minimal() {
    let before = files(&[("f", b"1\n2\n3\n4\n5\n")]);
    let after = files(&[("f", b"0\n1\n3\n5\n6\n")]);
    let d = version_difference(&before, &after);
    assert_eq!(d["files"][0]["lines"], json!(["+ 0", "- 2", "- 4", "+ 6"]));
}

#[test]
fn version_difference_non_text_and_order() {
    let before = files(&[("b.bin", &[0u8, 1, 2]), ("z", b"ok")]);
    let after = files(&[("b.bin", &[0u8, 1, 3]), ("z", &[0xff, 0xfe]), ("Z", b"upper")]);
    let d = version_difference(&before, &after);
    let fs = d["files"].as_array().unwrap();
    let paths: Vec<&str> = fs.iter().map(|f| f["path"].as_str().unwrap()).collect();
    assert_eq!(paths, vec!["Z", "b.bin", "z"]);
    assert_eq!(fs[1]["text"], false);
    assert_eq!(fs[1]["lines"], Value::Null);
    assert_eq!(fs[1]["after"]["bytes"], 3);
    assert_eq!(fs[2]["text"], false, "invalid UTF-8 on one side");
    assert_eq!(fs[2]["lines"], Value::Null);
    assert_eq!(d["unchanged"], 0);
}

#[test]
fn version_difference_line_limit() {
    let big: String = (0..4001).map(|i| format!("{i}\n")).collect();
    let ok: String = (0..4000).map(|i| format!("{i}\n")).collect();
    let before = files(&[("big", b"x\n"), ("ok", b"x\n")]);
    let after = files(&[("big", big.as_bytes()), ("ok", ok.as_bytes())]);
    let d = version_difference(&before, &after);
    let fs = d["files"].as_array().unwrap();
    assert_eq!(fs[0]["lines"], Value::Null);
    assert_eq!(fs[0]["limit"], "too large for a line difference (more than 4000 lines)");
    assert_eq!(fs[0]["text"], true);
    assert_eq!(fs[1]["limit"], Value::Null);
    assert_eq!(fs[1]["lines"].as_array().unwrap().len(), 4001);
}

// ---- activity_summary ----

#[test]
fn activity_summary_counts_and_failures() {
    let turns = vec![
        turn(
            "t-1",
            "completed",
            vec![
                cmd("ok", json!(0), json!(1), json!(""), "completed"),
                cmd("nonzero", json!(2), json!(1), json!(""), "completed"),
                cmd("failed", Value::Null, Value::Null, Value::Null, "failed"),
                cmd("declined", Value::Null, Value::Null, Value::Null, "declined"),
                cmd("running", Value::Null, Value::Null, Value::Null, "inProgress"),
                json!({"type":"agentMessage","id":"a","text":"first"}),
                json!({"type":"fileChange","id":"f","status":"completed","changes":[{"path":"p","kind":{"type":"delete"},"diff":""}]}),
            ],
        ),
        TurnRead { turn: json!({"id":"t-2","status":"failed"}), items: Err("timeout".into()) },
        turn("t-3", "interrupted", vec![json!({"type":"agentMessage","id":"b","text":"last"})]),
    ];
    let s = activity_summary(&turns, Some("page 2 failed"));
    assert_eq!(s["turns"], 3);
    assert_eq!(
        s["endings"],
        json!([{"turn":"t-1","status":"completed"},{"turn":"t-2","status":"failed"},{"turn":"t-3","status":"interrupted"}])
    );
    assert_eq!(s["commands"]["run"], 5);
    assert_eq!(s["commands"]["failed"], 3);
    assert_eq!(s["commands"]["list"][1], json!({"command":"nonzero","exitCode":2,"status":"completed"}));
    assert_eq!(s["fileChanges"], json!([{"path":"p","kind":"delete"}]));
    assert_eq!(s["finalAgentMessage"], "last");
    assert_eq!(s["limits"], json!(["turns list incomplete: page 2 failed", "turn t-2: items not read (timeout)"]));
}

#[test]
fn activity_summary_empty() {
    let s = activity_summary(&[], None);
    assert_eq!(
        s,
        json!({"turns":0,"endings":[],"commands":{"run":0,"failed":0,"list":[]},"fileChanges":[],
               "finalAgentMessage":null,"limits":[]})
    );
}
