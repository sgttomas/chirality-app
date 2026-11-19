//! Synthetic original request/register checks; no App, supplier or native UI runs.
use super::*;
use crate::native_requests::RequestRegister;
use std::cell::{Cell, RefCell};

fn fixture() -> (Value, Value, Value, Value, RequestRegister) {
    let generation = json!({"appSession":"fixture-session","home":"fixture-home","spawnCounter":3});
    let id = json!(7);
    let answer = json!({"decision":"accept"});
    let mut register = RequestRegister::default();
    register.receive(&generation, 1, &json!({
        "id":id,"method":"item/fileChange/requestApproval",
        "params":{"threadId":"fixture-thread","turnId":"fixture-turn","itemId":"fixture-item"}
    }), &json!({})).unwrap();
    let snapshot =
        json!({"generation":generation,"state":"ready","serverRequests":register.records()});
    let context = json!({"generation":generation,"hostState":"ready","displayName":"Fixture Person","osAccount":"fixture-user","codexAccount":null,"accountRevision":1});
    (generation, id, answer, json!([snapshot, context]), register)
}
fn affirmative() -> MessageDialogResult {
    MessageDialogResult::Custom(ns::SEND_ANSWER.into())
}

struct HandleFixture {
    window_reads: Cell<usize>,
    display_reads: Cell<usize>,
    display_available: bool,
}
impl HasWindowHandle for HandleFixture {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        self.window_reads.set(self.window_reads.get() + 1);
        if self.window_reads.get() > 1 {
            return Err(HandleError::Unavailable);
        }
        // SAFETY: A Web ID contains no pointers. raw-window-handle's borrowed
        // handle guarantees explicitly exclude the validity of window IDs.
        // This value is inspected only; no platform consumer receives it.
        Ok(unsafe { WindowHandle::borrow_raw(raw_window_handle::WebWindowHandle::new(17).into()) })
    }
}
impl HasDisplayHandle for HandleFixture {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        self.display_reads.set(self.display_reads.get() + 1);
        if self.display_available && self.display_reads.get() == 1 {
            Ok(DisplayHandle::web())
        } else {
            Err(HandleError::Unavailable)
        }
    }
}

#[test]
fn checked_parent_caches_both_original_handles_without_another_fallible_lookup() {
    let original = HandleFixture {
        window_reads: Cell::new(0),
        display_reads: Cell::new(0),
        display_available: true,
    };
    let parent = checked_parent(&original).unwrap();
    for _ in 0..2 {
        assert_eq!(
            parent.window_handle().unwrap().as_raw(),
            raw_window_handle::WebWindowHandle::new(17).into()
        );
        assert_eq!(parent.display_handle().unwrap(), DisplayHandle::web());
    }
    assert_eq!(original.window_reads.get(), 1);
    assert_eq!(original.display_reads.get(), 1);
}

// Models the error supplied by a destroyed/unavailable native window. No fake
// native pointer is constructed or passed to the platform dialog implementation.
struct UnavailableParent;
impl HasWindowHandle for UnavailableParent {
    fn window_handle(&self) -> Result<WindowHandle<'_>, HandleError> {
        Err(HandleError::Unavailable)
    }
}
impl HasDisplayHandle for UnavailableParent {
    fn display_handle(&self) -> Result<DisplayHandle<'_>, HandleError> {
        Err(HandleError::Unavailable)
    }
}

#[test]
fn unavailable_parent_refuses_before_dialog_or_reply() {
    let (g, id, a, basis, _) = fixture();
    let shown = Cell::new(false);
    let written = Cell::new(false);
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| {
            let _parent = checked_parent(&UnavailableParent)?;
            shown.set(true);
            Ok(affirmative())
        },
        |_| {
            written.set(true);
            Ok(Value::Null)
        },
    );
    assert_eq!(
        result.unwrap_err(),
        "Invoking App window unavailable; native answer confirmation refused"
    );
    assert!(!shown.get());
    assert!(!written.get());
}

#[test]
fn affirmative_parent_revalidation_error_refuses_before_reply() {
    let (g, id, a, basis, _) = fixture();
    let written = Cell::new(false);
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| result_in_parent(&UnavailableParent, affirmative()),
        |_| {
            written.set(true);
            Ok(Value::Null)
        },
    );
    assert!(result.unwrap_err().contains("window unavailable"));
    assert!(!written.get());
}

#[test]
fn unavailable_display_refuses_before_presentation_or_reply() {
    let (g, id, a, basis, _) = fixture();
    let original = HandleFixture {
        window_reads: Cell::new(0),
        display_reads: Cell::new(0),
        display_available: false,
    };
    let result = answer(
        &g,
        &id,
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| {
            let _parent = checked_parent(&original)?;
            panic!("unavailable display presented a dialog");
        },
        |_| panic!("unavailable display wrote a reply"),
    );
    assert_eq!(
        result.unwrap_err(),
        "Invoking App display unavailable; native answer confirmation refused"
    );
}

#[test]
fn default_cancel_abort_and_nonexact_affirmatives_never_reply() {
    for result in [
        MessageDialogResult::Custom(ns::DONT_SEND.into()),
        MessageDialogResult::Cancel,
        MessageDialogResult::Ok,
        MessageDialogResult::Yes,
        MessageDialogResult::No,
        MessageDialogResult::Custom("Cancel".into()),
        MessageDialogResult::Custom("send answer".into()),
        MessageDialogResult::Custom("Send answer ".into()),
    ] {
        let (g, id, a, basis, _) = fixture();
        let reads = Cell::new(0);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                reads.set(reads.get() + 1);
                (basis[0].clone(), basis[1].clone())
            },
            |_| result_in_parent(&UnavailableParent, result),
            |_| panic!("nonaffirmative wrote a reply"),
        );
        assert_eq!(
            result.unwrap(),
            json!({"state":"dismissed","replyWriteResult":"not-attempted"})
        );
        assert_eq!(reads.get(), 1);
    }
}

#[test]
fn exact_affirmative_revalidates_original_request_and_preserves_native_reply_outcome() {
    let (g, id, a, basis, mut register) = fixture();
    let reads = Cell::new(0);
    let writes = Cell::new(0);
    let observed_outcome = json!({"replyWriteResult":"written","acknowledgment":"not-observed"});
    let result = answer(
        &g,
        &id,
        &a,
        || {
            reads.set(reads.get() + 1);
            (basis[0].clone(), basis[1].clone())
        },
        |statement| {
            assert!(statement.text.contains("Codex asks to change files"));
            assert!(!statement.text.contains("item/fileChange/requestApproval"));
            assert!(statement
                .text
                .contains("Don't send (the default) and this sheet's Cancel button send nothing"));
            Ok(affirmative())
        },
        |actor| {
            assert_eq!(
                reads.get(),
                2,
                "original source must be rechecked before write"
            );
            let frame = register.prepare(&g, &id, &a, "person-via-interaction", Some(actor))?;
            assert_eq!(frame, json!({"id":7,"result":{"decision":"accept"}}));
            assert!(actor.contains("Fixture Person / fixture-user"));
            writes.set(writes.get() + 1);
            Ok(observed_outcome.clone())
        },
    )
    .unwrap();
    assert_eq!(result, observed_outcome);
    assert_eq!(writes.get(), 1);
}

#[test]
fn changed_original_generation_or_request_refuses_after_confirmation() {
    for mutation in [
        "appSession",
        "home",
        "spawnCounter",
        "missing",
        "typed-id",
        "settled",
        "not-ready",
    ] {
        let (g, id, a, basis, _) = fixture();
        let original = RefCell::new(basis);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                let original = original.borrow();
                (original[0].clone(), original[1].clone())
            },
            |_| {
                let mut original = original.borrow_mut();
                match mutation {
                    "appSession" | "home" => {
                        original[0]["generation"][mutation] = json!("replacement")
                    }
                    "spawnCounter" => original[0]["generation"][mutation] = json!(4),
                    "missing" => original[0]["serverRequests"] = json!([]),
                    "typed-id" => original[0]["serverRequests"][0]["requestIdentity"] = json!("7"),
                    "settled" => original[0]["serverRequests"][0]["state"] = json!("answered"),
                    "not-ready" => original[0]["state"] = json!("stopped"),
                    _ => unreachable!(),
                }
                Ok(affirmative())
            },
            |_| panic!("changed original source wrote a reply"),
        );
        assert!(result.is_err(), "{mutation}");
    }
}

#[test]
fn changed_actor_or_owning_context_refuses_after_confirmation() {
    for field in [
        "displayName",
        "osAccount",
        "codexAccount",
        "accountRevision",
        "generation",
        "hostState",
    ] {
        let (g, id, a, basis, _) = fixture();
        let original = RefCell::new(basis);
        let result = answer(
            &g,
            &id,
            &a,
            || {
                let original = original.borrow();
                (original[0].clone(), original[1].clone())
            },
            |_| {
                original.borrow_mut()[1][field] = json!("changed");
                Ok(affirmative())
            },
            |_| panic!("changed actor/context wrote a reply"),
        );
        assert_eq!(result.unwrap_err(), "Attribution or owning host context changed during confirmation; review and confirm again");
    }
}

#[test]
fn invalid_initial_request_never_presents_or_writes_and_write_errors_stay_errors() {
    let (g, id, a, basis, _) = fixture();
    assert!(answer(
        &g,
        &json!("foreign"),
        &a,
        || (basis[0].clone(), basis[1].clone()),
        |_| panic!("invalid request presented"),
        |_| panic!("invalid request wrote")
    )
    .is_err());
    let error = "synthetic reply write failed; receipt unknown";
    assert_eq!(
        answer(
            &g,
            &id,
            &a,
            || (basis[0].clone(), basis[1].clone()),
            |_| Ok(affirmative()),
            |_| Err(error.into())
        )
        .unwrap_err(),
        error
    );
}

fn question_fixture() -> (Value, Value, Value, RequestRegister) {
    let generation = json!({"appSession":"fixture-session","home":"fixture-home","spawnCounter":3});
    let mut register = RequestRegister::default();
    register.receive(&generation, 1, &json!({
        "id":"asked","method":"item/tool/requestUserInput",
        "params":{"threadId":"fixture-thread","turnId":"fixture-turn","itemId":"fixture-item","isBlocking":false,"questions":[
            {"id":"free","header":"Invented","question":"Invented question?","isOther":true,"isSecret":false,"options":[{"label":"Yes","description":"Invented"}]},
            {"id":"fixed","header":"Invented","question":"Invented fixed choice?","isOther":false,"isSecret":false,"options":[{"label":"A","description":"Invented"}]}]}
    }), &json!({})).unwrap();
    let snapshot = json!({"generation":generation,"state":"ready","serverRequests":register.records()});
    let context = json!({"generation":generation,"hostState":"ready","displayName":"Fixture Person","osAccount":"fixture-user","codexAccount":null,"accountRevision":1});
    (generation, json!([snapshot, context]), json!("asked"), register)
}

/// DEL-01-04 REQ-001: an answer to the agent's question, and its decline, are sent from the card with
/// no native confirmation: the answer is checked against the question, attributed to the person and
/// handed to the register's writer exactly as given.
#[test]
fn a_questions_answers_and_its_decline_are_written_without_a_native_confirmation() {
    let (g, basis, id, _) = question_fixture();
    let given = json!({"answers":{"free":{"answers":["An answer in the person's own words"]},"fixed":{"answers":["A"]}}});
    // One answer of two is sent as given; the unanswered question is simply absent from it.
    let partial = json!({"answers":{"free":{"answers":[""]}}});
    for (answer, choice) in [(given.clone(), "question-answers"), (partial, "question-answers"), (json!({"answers":{}}), "question-decline")] {
        let wrote = RefCell::new(None);
        let result = answer_with_choice(&g, &id, &answer, Some(choice),
            || (basis[0].clone(), basis[1].clone()),
            |_| panic!("a question's answer opened a native confirmation"),
            |actor| { *wrote.borrow_mut() = Some(actor.to_owned()); Ok(json!({"replyWriteResult":"written"})) }).unwrap();
        assert_eq!(result, json!({"replyWriteResult":"written"}), "the writer's own result is returned");
        let actor = wrote.borrow().clone().expect("written");
        assert!(actor.starts_with("person:") && actor.contains("Fixture Person"), "attributed to the person: {actor}");
    }
}

/// What is refused before anything is written: a button that does not agree with the answer, no button
/// named, an answer the question does not offer, a question that was not asked, and a request that is
/// not waiting. Nothing opens a confirmation.
#[test]
fn a_questions_answer_that_does_not_agree_with_the_question_or_its_button_writes_nothing() {
    let (g, basis, id, mut register) = question_fixture();
    let given = json!({"answers":{"free":{"answers":["text"]}}});
    let attempt = |snapshot: &Value, id: &Value, answer: &Value, choice: Option<&str>| answer_with_choice(&g, id, answer, choice,
        || (snapshot.clone(), basis[1].clone()),
        |_| panic!("a question's answer opened a native confirmation"),
        |_| panic!("a refused answer was written"));
    assert_eq!(attempt(&basis[0], &id, &given, Some("question-decline")).unwrap_err(), "The question button and answer do not agree; nothing sent");
    assert_eq!(attempt(&basis[0], &id, &given, None).unwrap_err(), "The question button and answer do not agree; nothing sent");
    // "Send answers" with nothing entered would be a decline; only the decline button sends one.
    assert_eq!(attempt(&basis[0], &id, &json!({"answers":{}}), Some("question-answers")).unwrap_err(), "The question button and answer do not agree; nothing sent");
    assert_eq!(attempt(&basis[0], &id, &given, Some("invented-choice")).unwrap_err(), "The question button and answer do not agree; nothing sent");
    assert!(attempt(&basis[0], &id, &json!({"answers":{"fixed":{"answers":["Not offered"]}}}), Some("question-answers")).is_err());
    assert!(attempt(&basis[0], &id, &json!({"answers":{"unasked":{"answers":["A"]}}}), Some("question-answers")).is_err());
    assert!(attempt(&basis[0], &json!("foreign"), &given, Some("question-answers")).is_err());
    assert_eq!(register.close_for(&g, "supplier-exit"), 1);
    let ended = json!({"generation":g,"state":"ready","serverRequests":register.records()});
    assert!(attempt(&ended, &id, &given, Some("question-answers")).unwrap_err().contains("ended-unanswered"), "a question whose Codex has ended takes no answer");
}

/// The kinds that keep the confirmation keep it: a tool permission is never written unless the person
/// chose the confirmation's own send button, and a question's button does not belong to it.
#[test]
fn a_tool_permission_still_needs_the_native_confirmation() {
    let (g, id, a, basis, _) = fixture();
    let shown = Cell::new(0);
    let dismissed = answer(&g, &id, &a, || (basis[0].clone(), basis[1].clone()),
        |_| { shown.set(shown.get() + 1); Ok(MessageDialogResult::Cancel) },
        |_| panic!("a dismissed confirmation wrote")).unwrap();
    assert_eq!((shown.get(), dismissed["state"].as_str(), dismissed["replyWriteResult"].as_str()), (1, Some("dismissed"), Some("not-attempted")));
    for choice in ["question-answers", "question-decline"] {
        assert!(answer_with_choice(&g, &id, &a, Some(choice), || (basis[0].clone(), basis[1].clone()),
            |_| panic!("a question's button reached a tool permission's confirmation"),
            |_| panic!("a question's button wrote a tool permission")).is_err());
    }
}

/// A permission grant and an MCP server's input request keep the confirmation too. Neither is written
/// when the confirmation is dismissed, and a question's button, which skips the confirmation for a
/// question, sends neither: it is refused before anything is shown or written.
#[test]
fn a_permission_grant_and_an_mcp_input_request_still_need_the_native_confirmation() {
    let generation = json!({"appSession":"fixture-session","home":"fixture-home","spawnCounter":3});
    let context = json!({"generation":generation,"hostState":"ready","displayName":"Fixture Person","osAccount":"fixture-user","codexAccount":null,"accountRevision":1});
    let cases = [
        ("item/permissions/requestApproval",
         json!({"threadId":"fixture-thread","turnId":"fixture-turn","itemId":"fixture-item","permissions":{"network":{"enabled":true}},"reason":"Invented"}),
         json!({"permissions":{"network":{"enabled":true}},"scope":"turn"})),
        ("mcpServer/elicitation/request",
         json!({"mode":"form","serverName":"synthetic-server","threadId":"fixture-thread","message":"synthetic form","requestedSchema":{"type":"object","properties":{"answer":{"type":"string","minLength":2}},"required":["answer"],"additionalProperties":false}}),
         json!({"action":"accept","content":{"answer":"invented"},"_meta":null})),
    ];
    for (method, params, reply) in cases {
        let mut register = RequestRegister::default();
        let id = json!("kept");
        register.receive(&generation, 1, &json!({"id":id,"method":method,"params":params}), &json!({})).unwrap();
        let snapshot = json!({"generation":generation,"state":"ready","serverRequests":register.records()});
        let shown = Cell::new(0);
        let dismissed = answer(&generation, &id, &reply, || (snapshot.clone(), context.clone()),
            |_| { shown.set(shown.get() + 1); Ok(MessageDialogResult::Cancel) },
            |_| panic!("a dismissed confirmation wrote")).unwrap_or_else(|e| panic!("{method}: {e}"));
        assert_eq!((shown.get(), dismissed["state"].as_str(), dismissed["replyWriteResult"].as_str()), (1, Some("dismissed"), Some("not-attempted")), "{method}");
        let wrote = Cell::new(0);
        answer(&generation, &id, &reply, || (snapshot.clone(), context.clone()), |_| Ok(affirmative()),
            |_| { wrote.set(wrote.get() + 1); Ok(json!({"replyWriteResult":"written"})) }).unwrap_or_else(|e| panic!("{method}: {e}"));
        assert_eq!(wrote.get(), 1, "{method}: written only after the confirmation's own send button");
        for choice in ["question-answers", "question-decline"] {
            for sent in [reply.clone(), json!({"answers":{}}), json!({"answers":{"answer":{"answers":["invented"]}}})] {
                assert!(answer_with_choice(&generation, &id, &sent, Some(choice), || (snapshot.clone(), context.clone()),
                    |_| panic!("a question's button reached another request's confirmation"),
                    |_| panic!("a question's button wrote another kind of request")).is_err(), "{method} {choice} {sent}");
            }
        }
    }
}
