// Display metadata: each `workflowRoot.runs[]` row's `preparationOrder` is the
// run's position in this Root's maintained per-(home, conversation)
// preparation order, never the map's iteration order. Uses the maintained
// local protocol peer; no supplier, credential or model.

fn orders(root: &WorkflowRootSession) -> std::collections::BTreeMap<String, Value> {
    root.snapshot()["runs"].as_array().unwrap().iter()
        .map(|row| (row["reference"].as_str().unwrap().to_owned(), row["preparationOrder"].clone())).collect()
}

#[test]
fn preparation_order_follows_actual_preparation_per_conversation_and_is_null_when_not_established() {
    let peer = Peer::new();
    let mut root = peer.registered();
    // Three preparations in one conversation: two ended runs, then one prepared.
    let a = open_run(&peer, &mut root, "thread");
    root.runs[&a].lock().unwrap().end_run(None, None).unwrap();
    let b = open_run(&peer, &mut root, "thread");
    root.runs[&b].lock().unwrap().end_run(None, None).unwrap();
    let c = root.prepare_run(peer.home.clone(), &peer.generation, "thread", "third".into(), peer.project()).unwrap();
    // Another conversation of the same home has its own order.
    let other = peer.second_thread();
    let d = open_run(&peer, &mut root, &other);
    let (wire, wr, rs) = (peer.turn_starts(), peer.fixture.wr_files(), peer.fixture.rs_entries());
    let read = orders(&root);
    assert_eq!((&read[&a], &read[&b], &read[&c], &read[&d]), (&json!(0), &json!(1), &json!(2), &json!(0)), "{read:?}");
    assert_eq!(orders(&root), read, "a read is repeatable");
    // A busy run's row still carries its order from the maintained vector.
    {
        let busy = root.runs[&c].clone();
        let _held = busy.lock().unwrap();
        let rows = root.snapshot()["runs"].clone();
        let row = rows.as_array().unwrap().iter().find(|r| r["reference"] == c.as_str()).unwrap().clone();
        assert_eq!((row["state"].as_str(), &row["preparationOrder"]), (Some("original run operation pending"), &json!(2)));
    }
    // Not established: a run reference with no association, and one held by
    // two conversations' vectors, read null (no fallback).
    root.runs.insert("run:workflow:unassociated".into(), root.runs[&d].clone());
    root.conversations.get_mut(&(peer.generation["home"].as_str().unwrap().to_owned(), other.clone())).unwrap().push(a.clone());
    let read = orders(&root);
    assert_eq!(read["run:workflow:unassociated"], Value::Null);
    assert_eq!(read[&a], Value::Null, "a reference in two vectors is not established");
    assert_eq!((&read[&b], &read[&c], &read[&d]), (&json!(1), &json!(2), &json!(0)), "other rows keep their order");
    // Reading the snapshot sends, records and changes nothing.
    assert_eq!((peer.turn_starts(), peer.fixture.wr_files(), peer.fixture.rs_entries()), (wire, wr, rs));
    assert_eq!(root.runs[&c].lock().unwrap().lifecycle, RunLifecycle::Prepared);
}

#[test]
fn preparation_order_is_per_home_and_a_run_scope_mismatch_reads_null() {
    let peer = Peer::new();
    let mut root = peer.registered();
    let a = open_run(&peer, &mut root, "thread");
    let home = peer.generation["home"].as_str().unwrap().to_owned();
    // The same thread id under another home key is another vector: a run moved
    // there no longer matches its own readable scope.
    let vector = root.conversations.remove(&(home.clone(), "thread".into())).unwrap();
    root.conversations.insert(("another-home".into(), "thread".into()), vector.clone());
    assert_eq!(orders(&root)[&a], Value::Null, "the vector is not the run's own (home, conversation)");
    root.conversations.remove(&("another-home".to_owned(), "thread".to_owned()));
    root.conversations.insert((home, "thread".into()), vector);
    assert_eq!(orders(&root)[&a], json!(0));
}
