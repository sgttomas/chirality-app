#[path = "../src/native_history.rs"]
mod native_history;
use native_history::{Direction, HistoryQuery, NativeHistory};
use serde_json::{json, Value};
fn g() -> Value {
    json!({"appSession":"page-session","home":"page-home","spawnCounter":1})
}
fn thread(id: &str) -> Value {
    json!({"id":id,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/invented","ephemeral":false,"modelProvider":"configured","preview":"synthetic","projectId":null,"sessionId":"session","source":"appServer","status":{"type":"notLoaded"},"turns":[]})
}
fn accept(h: &mut NativeHistory, q: &HistoryQuery, page: &Value) {
    h.receive(q, "page-home", &g(), page).unwrap();
}
fn selected() -> NativeHistory {
    let mut h = NativeHistory::new("page-home", g()).unwrap();
    let q = h.list_threads(None, Direction::Desc).unwrap();
    accept(
        &mut h,
        &q,
        &json!({"data":[thread("thread"),thread("other")],"nextCursor":null}),
    );
    h.select("thread").unwrap();
    let q = h.turns_page(None, Direction::Desc).unwrap();
    accept(
        &mut h,
        &q,
        &json!({"data":[{"id":"turn","status":"completed","items":[],"itemsView":"summary","error":null}],"nextCursor":null}),
    );
    h
}
fn page() -> Value {
    json!({"data":[{"turnId":"turn","item":{"id":"user","type":"userMessage","content":[{"type":"text","text":"synthetic exact\r\ntext","text_elements":[]}]}}],"nextCursor":"opaque-next","nativeExtra":{"preserved":true}})
}
#[test]
fn exact_latest_query_metadata_and_borrowed_existing_raw_page() {
    let mut h = selected();
    let q = h.items_page("turn", None, Direction::Asc).unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    let raw = page();
    accept(&mut h, &q, &raw);
    let w = h.accepted_items_observation(&q).unwrap();
    assert_eq!(w.query(), &q);
    assert!(w.owner_instance() > 0);
    assert_eq!(w.selection_epoch(), h.selection_epoch());
    assert_eq!(w.stream_revision(), 1);
    assert_eq!(w.stream(), "item-pages");
    assert_eq!(w.page(), &raw);
    assert!(std::ptr::eq(
        w.page(),
        h.accepted_items_observation(&q).unwrap().page()
    ));
    assert_eq!(h.snapshot()["selected"]["itemsPage"], raw);
    assert_eq!(h.snapshot()["activeBindingPerformed"], false);
}
#[test]
fn newer_cursor_pending_error_and_recovery_never_turn_prior_page_into_current_witness() {
    let mut h = selected();
    let q = h.items_page("turn", None, Direction::Asc).unwrap();
    let raw = page();
    accept(&mut h, &q, &raw);
    let next = h
        .items_page("turn", Some("opaque-next"), Direction::Asc)
        .unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    assert!(h.accepted_items_observation(&next).is_err());
    h.waiting_ended(&next).unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    h.receive_error(
        &next,
        "page-home",
        &g(),
        &json!({"code":-32600,"message":"synthetic refusal"}),
    )
    .unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    assert_eq!(h.snapshot()["selected"]["itemsPage"], raw);
    let recovered = h
        .items_page("turn", Some("opaque-next"), Direction::Asc)
        .unwrap();
    let tail = json!({"data":[],"nextCursor":null});
    accept(&mut h, &recovered, &tail);
    let w = h.accepted_items_observation(&recovered).unwrap();
    assert_eq!(w.query().params()["cursor"], "opaque-next");
    assert_eq!(w.page(), &tail);
    assert_eq!(w.stream_revision(), 3);
}
#[test]
fn foreign_owner_full_tuple_and_malformed_or_wrong_turn_cannot_supply_witness() {
    let mut h = selected();
    let q = h.items_page("turn", None, Direction::Asc).unwrap();
    let mut other = selected();
    let foreign = other.items_page("turn", None, Direction::Asc).unwrap();
    assert!(h.accepted_items_observation(&foreign).is_err());
    let raw = page();
    assert!(h.receive(&q, "foreign-home", &g(), &raw).is_err());
    let g2 = json!({"appSession":"page-session","home":"page-home","spawnCounter":2});
    assert!(h.receive(&q, "page-home", &g2, &raw).is_err());
    assert!(h
        .receive(&q, "page-home", &g(), &json!({"data":"invalid"}))
        .is_err());
    let mut wrong = raw.clone();
    wrong["data"][0]["turnId"] = json!("foreign-turn");
    assert!(h.receive(&q, "page-home", &g(), &wrong).is_err());
    assert!(h.accepted_items_observation(&q).is_err());
    accept(&mut h, &q, &raw);
    assert!(h.accepted_items_observation(&foreign).is_err());
    assert_eq!(h.accepted_items_observation(&q).unwrap().page(), &raw);
}
#[test]
fn reselect_and_generation_close_withhold_read_only_witness() {
    let mut h = selected();
    let q = h.items_page("turn", None, Direction::Asc).unwrap();
    accept(&mut h, &q, &page());
    h.select("other").unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    h.select("thread").unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
    h.close_generation(&g()).unwrap();
    assert!(h.accepted_items_observation(&q).is_err());
}
#[test]
fn superseded_pending_query_does_not_block_new_accepted_page_or_change_other_streams() {
    let mut h = selected();
    let old = h.items_page("turn", None, Direction::Asc).unwrap();
    let newest = h.items_page("turn", None, Direction::Asc).unwrap();
    accept(&mut h, &newest, &page());
    assert!(h.receive(&old, "page-home", &g(), &page()).is_err());
    let owner = h
        .accepted_items_observation(&newest)
        .unwrap()
        .owner_instance();
    let goal = h.read_goal().unwrap();
    assert_eq!(
        h.accepted_items_observation(&newest)
            .unwrap()
            .owner_instance(),
        owner
    );
    accept(&mut h, &goal, &json!({"goal":null}));
    assert_eq!(
        h.accepted_items_observation(&newest)
            .unwrap()
            .stream_revision(),
        2
    );
}
