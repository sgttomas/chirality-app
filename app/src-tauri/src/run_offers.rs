//! Run offers read from completed agent messages (DEL-02-02 WR §16.5 PR-1…PR-5,
//! FN-1…FN-3; DEL-01-04 NIR §5.7 RN-3…RN-7; DEL-02-03 EXEC RE-7).
//!
//! Only the two exact line forms are read: `Next workflow: ‹origin›:‹name›` and
//! `Workflow finished: ‹origin›:‹name›`. Prose is never classified. A line is the
//! agent's statement: reading it ends, selects, starts or records nothing. Offers
//! come only from agent messages this App observed complete live, in the current
//! native generation; history pages read later never raise an offer (PR-5).
//!
//! A `FinishedReport` can only be made here, from a message the host observed. It
//! is the only way a run end can carry cause *completed* (FN-2).
use serde_json::{json, Value};

pub(crate) const ORIGINS: [&str; 4] = ["project", "user", "bundled", "host"];
const PROPOSAL_FORM: &str = "Next workflow:";
const FINISHED_FORM: &str = "Workflow finished:";

/// An `‹origin›:‹name›` pair exactly as an agent line names it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Named {
    pub origin: String,
    pub name: String,
}
impl Named {
    fn parse(text: &str) -> Option<Self> {
        let (origin, name) = text.split_once(':')?;
        (ORIGINS.contains(&origin) && crate::workflow_workspace::valid_name(name))
            .then(|| Self { origin: origin.into(), name: name.into() })
    }
    pub fn text(&self) -> String {
        format!("{}:{}", self.origin, self.name)
    }
}

/// What the two ruled line forms say in one message, read per PR-1 and FN-1.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub(crate) struct LineForms {
    pub finished: Option<Named>,
    pub proposal: Option<Named>,
}

/// PR-1: a proposal is the last non-empty line, exactly `Next workflow: ‹origin›:‹name›`,
/// and the message has no other line of that form. FN-1: a finished report is a line
/// exactly `Workflow finished: ‹origin›:‹name›`, the only line of its form, that is the
/// last non-empty line or the line immediately before a PR-1 proposal line. A line is
/// read from its first character (as the prototype's anchored forms): an indented or
/// quoted line is not the form. Only trailing whitespace is ignored.
pub(crate) fn read_lines(text: &str) -> LineForms {
    let lines: Vec<&str> = text.lines().map(str::trim_end).filter(|l| !l.is_empty()).collect();
    let proposal_lines = lines.iter().filter(|l| l.starts_with(PROPOSAL_FORM)).count();
    let finished_lines = lines.iter().filter(|l| l.starts_with(FINISHED_FORM)).count();
    let mut forms = LineForms::default();
    let Some(last) = lines.last() else { return forms };
    if proposal_lines == 1 {
        forms.proposal = last.strip_prefix("Next workflow: ").and_then(Named::parse);
    }
    if finished_lines == 1 {
        let candidate = if forms.proposal.is_some() { lines.len().checked_sub(2).map(|i| lines[i]) } else { Some(*last) };
        forms.finished = candidate.and_then(|l| l.strip_prefix("Workflow finished: ")).and_then(Named::parse);
    }
    forms
}

/// The native identity of one item, as the activity view and the commands name it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct ItemRef {
    pub thread: String,
    pub turn: String,
    pub item: String,
}
impl ItemRef {
    pub fn from_value(value: &Value) -> Result<Self, String> {
        let field = |key: &str| {
            value[key].as_str().filter(|s| !s.is_empty()).map(str::to_owned).ok_or_else(|| format!("message reference lacks {key}"))
        };
        Ok(Self { thread: field("threadId")?, turn: field("turnId")?, item: field("itemId")? })
    }
    pub fn view(&self) -> Value {
        json!({"threadId":self.thread,"turnId":self.turn,"itemId":self.item})
    }
}

/// A completed agent message this App observed live, with what its lines say.
#[derive(Clone, Debug)]
pub(crate) struct Message {
    pub item: ItemRef,
    /// The App's receipt order of the message's own row.
    pub order: u64,
    /// The receipt order of the first row of its turn (the turn's position here).
    pub turn_order: u64,
    pub forms: LineForms,
}

fn live_completed_message(row: &Value) -> Option<(&str, &str, &str, &str, u64)> {
    let native = &row["native"];
    if native["type"] != "agentMessage" || row["displayState"] != "completed" || row["standing"] != "live-observed" {
        return None;
    }
    Some((row["threadId"].as_str()?, row["turnId"].as_str()?, native["id"].as_str()?, native["text"].as_str()?, row["observedOrder"].as_u64()?))
}

/// The receipt order of the first row this App holds for a turn of a thread.
pub(crate) fn turn_order(view: &Value, thread: &str, turn: &str) -> Option<u64> {
    view["items"].as_array()?.iter().filter(|r| r["threadId"] == thread && r["turnId"] == turn).filter_map(|r| r["observedOrder"].as_u64()).min()
}

/// The turn of the thread's most recently received live row (RN-1 end-marker
/// position). History pages read later never move it.
pub(crate) fn latest_turn(view: &Value, thread: &str) -> Option<String> {
    view["items"]
        .as_array()?
        .iter()
        .filter(|r| r["threadId"] == thread && r["standing"] == "live-observed")
        .filter_map(|r| Some((r["observedOrder"].as_u64()?, r["turnId"].as_str()?)))
        .max_by_key(|(order, _)| *order)
        .map(|(_, turn)| turn.to_owned())
}

/// Completed agent messages of `thread` observed live in this view, in receipt order.
pub(crate) fn live_messages(view: &Value, thread: &str) -> Vec<Message> {
    let mut found: Vec<Message> = view["items"]
        .as_array()
        .into_iter()
        .flatten()
        .filter_map(live_completed_message)
        .filter(|(t, ..)| *t == thread)
        .map(|(t, turn, item, text, order)| Message {
            item: ItemRef { thread: t.into(), turn: turn.into(), item: item.into() },
            order,
            turn_order: turn_order(view, t, turn).unwrap_or(order),
            forms: read_lines(text),
        })
        .collect();
    found.sort_by_key(|m| m.order);
    found
}

/// Threads with a completed agent message observed live in this view.
pub(crate) fn threads_with_messages(view: &Value) -> Vec<String> {
    let mut threads: Vec<String> = view["items"].as_array().into_iter().flatten().filter_map(live_completed_message).map(|(t, ..)| t.to_owned()).collect();
    threads.sort();
    threads.dedup();
    threads
}

/// Where a run's start lies relative to the rows of this view.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum RunStart {
    /// The start turn's first row has this receipt order in this view.
    At(u64),
    /// The run started in an earlier native generation of this App session and
    /// home, so every row of this view came after it.
    BeforeView,
    /// The start cannot be placed in this view; nothing is offered for the run.
    Unknown,
}
pub(crate) fn run_start(view: &Value, thread: &str, run_generation: &Value, start_turn: Option<&str>) -> RunStart {
    let current = &view["generation"];
    if current == run_generation {
        return start_turn.and_then(|turn| turn_order(view, thread, turn)).map_or(RunStart::Unknown, RunStart::At);
    }
    let later = current["appSession"] == run_generation["appSession"]
        && current["home"] == run_generation["home"]
        && matches!((current["spawnCounter"].as_u64(), run_generation["spawnCounter"].as_u64()), (Some(now), Some(then)) if now > then);
    if later { RunStart::BeforeView } else { RunStart::Unknown }
}
impl RunStart {
    /// Whether a message whose turn has this position belongs to the run.
    fn includes(self, turn_order: u64) -> bool {
        match self {
            Self::At(start) => turn_order >= start,
            Self::BeforeView => true,
            Self::Unknown => false,
        }
    }
    /// Whether the run started after a message (that message's offer is superseded).
    pub fn after(self, message_order: u64) -> bool {
        matches!(self, Self::At(start) if start > message_order)
    }
}

/// PR-5: where the person's latest workflow selection falls in a home's view. A
/// proposal received at or before it is superseded by that selection.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct SelectionMark {
    pub home: Value,
    pub generation: Value,
    /// The last receipt order in that view when the person selected (None: nothing received yet).
    pub order: Option<u64>,
}
impl SelectionMark {
    pub fn in_view(view: &Value) -> Self {
        let order = view["items"].as_array().into_iter().flatten().filter_map(|r| r["observedOrder"].as_u64()).max();
        Self { home: view["home"].clone(), generation: view["generation"].clone(), order }
    }
    /// The mark as a supersession point in `view`: it supersedes messages received
    /// at or before it in the same generation; a later generation is newer than it.
    pub fn supersession(&self, view: &Value) -> RunStart {
        match self.order {
            Some(order) if view["home"] == self.home && view["generation"] == self.generation => RunStart::At(order + 1),
            _ => RunStart::Unknown,
        }
    }
}

/// The run in force in a conversation, as its owner holds it.
pub(crate) struct RunInForce<'a> {
    pub run: &'a str,
    pub thread: &'a str,
    pub start: RunStart,
    pub workflow: Named,
}

/// FN-1 proof that the agent stated the run in force finished, in a message this
/// App observed live during that run. Only `finished_report` makes one.
#[derive(Clone, Debug)]
pub(crate) struct FinishedReport {
    item: ItemRef,
    run: String,
    workflow: Named,
}
impl FinishedReport {
    pub fn item(&self) -> &ItemRef {
        &self.item
    }
    pub fn run(&self) -> &str {
        &self.run
    }
    pub fn view(&self) -> Value {
        json!({"message":self.item.view(),"run":self.run,"statement":format!("Workflow finished: {}",self.workflow.text()),"standing":"the agent's statement in its message; the person ended the run"})
    }
}

/// FN-1/FN-2: the newest live message of the run in force whose finished report
/// names the run's own workflow. A report naming another workflow is ignored.
pub(crate) fn finished_report(view: &Value, run: &RunInForce) -> Option<FinishedReport> {
    live_messages(view, run.thread)
        .into_iter()
        .rev()
        .filter(|m| run.start.includes(m.turn_order))
        .find(|m| m.forms.finished.as_ref() == Some(&run.workflow))
        .map(|m| FinishedReport { item: m.item, run: run.run.into(), workflow: run.workflow.clone() })
}

/// The pressed message must be the run's current finished report.
pub(crate) fn verify_finished(view: &Value, run: &RunInForce, item: &ItemRef) -> Result<FinishedReport, String> {
    let report = finished_report(view, run).ok_or_else(|| {
        format!("No finished report naming {} was observed in this conversation during run {}; the run is not ended as completed (FN-1, FN-2). Nothing recorded", run.workflow.text(), run.run)
    })?;
    if report.item != *item {
        return Err("That message is not the current finished report of the run in force; nothing recorded".into());
    }
    Ok(report)
}

/// PR-1/PR-5: the conversation's current proposal: the newest live message whose
/// last line proposes a workflow, unless a run in this conversation started after it.
pub(crate) fn current_proposal(view: &Value, thread: &str, run_starts: &[RunStart]) -> Option<(Message, Named)> {
    let newest = live_messages(view, thread).into_iter().rev().find(|m| m.forms.proposal.is_some())?;
    if run_starts.iter().any(|start| start.after(newest.order)) {
        return None;
    }
    let named = newest.forms.proposal.clone()?;
    Some((newest, named))
}

/// The pressed message must carry the conversation's current proposal.
pub(crate) fn verify_proposal(view: &Value, thread: &str, run_starts: &[RunStart], item: &ItemRef) -> Result<(Message, Named), String> {
    match current_proposal(view, thread, run_starts) {
        Some((message, named)) if message.item == *item => Ok((message, named)),
        Some(_) => Err("That message is not the conversation's current workflow proposal (a newer proposal supersedes it); nothing selected or started".into()),
        None => Err("No current workflow proposal from a message this App observed in this conversation; nothing selected or started (PR-1, PR-5)".into()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn named(o: &str, n: &str) -> Option<Named> {
        Some(Named { origin: o.into(), name: n.into() })
    }
    #[test]
    fn line_forms_follow_pr_1_and_fn_1_exactly() {
        // Prototype cases of06 and fo1…fo5 (NIR prototype run_cases.py), plus negatives.
        assert_eq!(read_lines("Done.\nNext workflow: project:load-check").proposal, named("project", "load-check"));
        assert_eq!(read_lines("Next workflow: project:load-check\nThat is my suggestion.").proposal, None, "not the last line");
        assert_eq!(read_lines("Next workflow: project:a\nNext workflow: project:load-check").proposal, None, "two proposal lines");
        assert_eq!(read_lines("You might want to run load-check next.").proposal, None, "prose is never read");
        assert_eq!(read_lines("Next workflow: load-check").proposal, None, "no origin");
        assert_eq!(read_lines("Next workflow: elsewhere:load-check").proposal, None, "unknown origin");
        assert_eq!(read_lines("Next workflow: project:Load Check").proposal, None, "not a workflow name");
        assert_eq!(read_lines("**Next workflow: project:load-check**").proposal, None, "decorated line is not the form");
        assert_eq!(read_lines("All checked.\nWorkflow finished: project:supports-adjust").finished, named("project", "supports-adjust"));
        let both = read_lines("Workflow finished: project:supports-adjust\nNext workflow: project:load-check\n\n");
        assert_eq!(both, LineForms { finished: named("project", "supports-adjust"), proposal: named("project", "load-check") });
        assert_eq!(read_lines("Workflow finished: project:supports-adjust\nLet me know.").finished, None, "not last");
        assert_eq!(read_lines("Workflow finished: project:a\nWorkflow finished: project:a").finished, None, "twice");
        assert_eq!(read_lines("Workflow finished: project:a\nDone.\nNext workflow: project:b").finished, None, "not immediately before the proposal");
        assert_eq!(read_lines("").finished, None);
        // Review M2: leading whitespace is not the form; a finished line counts as "before
        // the proposal line" only when that last line is a valid PR-1 proposal.
        assert_eq!(read_lines("Quoted:\n    Workflow finished: project:a").finished, None, "indented line");
        assert_eq!(read_lines("> Workflow finished: project:a").finished, None, "quoted line");
        assert_eq!(read_lines("Done.\n  Next workflow: project:b").proposal, None, "indented proposal");
        assert_eq!(read_lines("Workflow finished: project:a\nNext workflow: elsewhere:x"), LineForms::default(), "an invalid last line is no proposal line, so the finished line is not last");
        assert_eq!(read_lines("Done.\r\nWorkflow finished: project:a  \r\n").finished, named("project", "a"), "trailing whitespace and CRLF are ignored");
    }
    #[test]
    fn message_references_and_marks() {
        // The lib.rs commands parse the person's message reference with this function.
        let ok = ItemRef::from_value(&json!({"threadId":"T","turnId":"u","itemId":"i"})).unwrap();
        assert_eq!(ok.view(), json!({"threadId":"T","turnId":"u","itemId":"i"}));
        for bad in [json!(null), json!({"threadId":"T","turnId":"u"}), json!({"threadId":"T","turnId":"u","itemId":""}), json!({"threadId":1,"turnId":"u","itemId":"i"})] {
            assert!(ItemRef::from_value(&bad).is_err(), "{bad}");
        }
        let v = json!({"home":"h","generation":g(1),"items":[row("t1","a",3,"x","live-observed","completed"),row("t1","b",7,"x","recovered-from-supplier","completed")]});
        let mark = SelectionMark::in_view(&v);
        assert_eq!(mark.order, Some(7));
        assert_eq!(mark.supersession(&v), RunStart::At(8));
        let later = json!({"home":"h","generation":g(2),"items":[]});
        assert_eq!(mark.supersession(&later), RunStart::Unknown, "a later generation is newer than the mark");
        assert_eq!(SelectionMark::in_view(&later).supersession(&later), RunStart::Unknown, "nothing received yet supersedes nothing");
        let live = json!({"items":[row("t1","a",3,"x","live-observed","completed"),row("t2","b",9,"x","recovered-from-supplier","completed")]});
        assert_eq!(latest_turn(&live, "T").as_deref(), Some("t1"), "a history row read later does not move the end marker");
    }
    fn row(turn: &str, item: &str, order: u64, text: &str, standing: &str, state: &str) -> Value {
        json!({"threadId":"T","turnId":turn,"native":{"id":item,"type":"agentMessage","text":text},"displayState":state,"standing":standing,"observedOrder":order})
    }
    fn g(n: u64) -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":n})
    }
    fn view(items: Vec<Value>) -> Value {
        json!({"generation":g(1),"items":items})
    }
    fn in_force(start: RunStart) -> RunInForce<'static> {
        RunInForce { run: "run:a", thread: "T", start, workflow: Named { origin: "project".into(), name: "a".into() } }
    }
    #[test]
    fn finished_report_needs_a_live_completed_message_of_the_run_in_force() {
        let user = json!({"threadId":"T","turnId":"t1","native":{"id":"u","type":"userMessage"},"displayState":"completed","standing":"live-observed","observedOrder":0});
        let before = row("t0", "old", 0, "Workflow finished: project:a", "live-observed", "completed");
        let v = view(vec![before.clone(), json!({"threadId":"T","turnId":"t1","native":{"id":"u","type":"userMessage"},"displayState":"completed","standing":"live-observed","observedOrder":1})]);
        let start = run_start(&v, "T", &g(1), Some("t1"));
        assert_eq!(start, RunStart::At(1));
        assert!(finished_report(&v, &in_force(start)).is_none(), "a report before the run started is not this run's");
        let report = row("t1", "m", 2, "Done.\nWorkflow finished: project:a", "live-observed", "completed");
        let v = view(vec![before.clone(), user.clone(), report.clone()]);
        let start = run_start(&v, "T", &g(1), Some("t1"));
        let ok = verify_finished(&v, &in_force(start), &ItemRef { thread: "T".into(), turn: "t1".into(), item: "m".into() }).unwrap();
        assert_eq!(ok.run(), "run:a");
        for (rejected, why) in [
            (row("t1", "m", 2, "Done.\nWorkflow finished: project:other", "live-observed", "completed"), "another workflow"),
            (row("t1", "m", 2, "Done.\nWorkflow finished: project:a", "recovered-from-supplier", "completed"), "read from history"),
            (row("t1", "m", 2, "Done.\nWorkflow finished: project:a", "live-observed", "in-progress"), "not completed"),
            (row("t1", "m", 2, "Workflow finished: project:a\nMore text", "live-observed", "completed"), "not the last line"),
        ] {
            let v = view(vec![user.clone(), rejected]);
            let start = run_start(&v, "T", &g(1), Some("t1"));
            assert!(finished_report(&v, &in_force(start)).is_none(), "{why}");
        }
        assert!(finished_report(&view(vec![user.clone(), report.clone()]), &in_force(RunStart::Unknown)).is_none(), "an unplaced run gets no offer");
        let later = json!({"generation":g(2),"items":[report.clone()]});
        assert_eq!(run_start(&later, "T", &g(1), Some("t1")), RunStart::BeforeView, "a run started in an earlier generation precedes this view");
        let other_session = json!({"generation":{"appSession":"x","home":"h","spawnCounter":9},"items":[report]});
        assert_eq!(run_start(&other_session, "T", &g(1), Some("t1")), RunStart::Unknown);
        let wrong = ItemRef { thread: "T".into(), turn: "t1".into(), item: "other".into() };
        let v = view(vec![user, row("t1", "m", 2, "Workflow finished: project:a", "live-observed", "completed")]);
        assert!(verify_finished(&v, &in_force(RunStart::At(1)), &wrong).is_err());
    }
    #[test]
    fn the_newest_proposal_is_current_until_a_run_starts_after_it() {
        let first = row("t1", "p1", 1, "Next workflow: project:a", "live-observed", "completed");
        let second = row("t2", "p2", 4, "Next workflow: project:b", "live-observed", "completed");
        let plain = row("t3", "x", 6, "No proposal here.", "live-observed", "completed");
        let v = view(vec![first.clone(), second.clone(), plain]);
        let (message, named) = current_proposal(&v, "T", &[]).unwrap();
        assert_eq!((message.item.item.as_str(), named.name.as_str()), ("p2", "b"), "a newer proposal supersedes");
        let stale = ItemRef { thread: "T".into(), turn: "t1".into(), item: "p1".into() };
        assert!(verify_proposal(&v, "T", &[], &stale).is_err());
        assert!(current_proposal(&v, "T", &[RunStart::At(5)]).is_none(), "a run started after the proposal supersedes it");
        assert!(current_proposal(&v, "T", &[RunStart::At(3), RunStart::BeforeView]).is_some());
        let recovered = view(vec![row("t1", "p1", 1, "Next workflow: project:a", "recovered-from-supplier", "completed")]);
        assert!(current_proposal(&recovered, "T", &[]).is_none(), "history read later never raises an offer (PR-5)");
    }
}
