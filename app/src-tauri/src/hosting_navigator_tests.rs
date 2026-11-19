// The navigator's projection of a Host settles nothing: a reply write that
// completed and has not been observed stays unsettled across it, where
// `snapshot` settles it. Invented material only; no process is started.
use super::*;

fn g() -> Value { json!({"appSession":"navigator-session","home":"navigator-home","spawnCounter":1}) }

#[test]
fn the_navigator_projection_leaves_a_completed_reply_write_unsettled() {
    let host = Host::new();
    {
        let mut i = host.inner.0.lock().unwrap();
        i.state = "ready".into();
        i.generation = g();
        i.threads.push(json!({"generation":g(),"threadId":"thread","name":"Invented","preview":"invented","status":{"type":"idle"},"cwd":"/invented","model":"not projected"}));
        i.threads.push(json!({"generation":{"appSession":"navigator-session","home":"navigator-home","spawnCounter":0},"threadId":"earlier"}));
        i.server_requests.receive(&g(), 1, &json!({"id":"answered","method":"item/tool/requestUserInput","params":{"threadId":"thread","questions":[]}}), &json!({"experimentalApi":false})).unwrap();
        i.server_requests.receive(&g(), 2, &json!({"id":"waiting","method":"item/tool/requestUserInput","params":{"threadId":"child","questions":[]}}), &json!({"experimentalApi":false})).unwrap();
        i.server_requests.prepare_error(&g(), &json!("answered"), &json!({"code":-32000,"message":"invented"}), "app-rule:invented").unwrap();
        let write = i.server_requests.begin_reply_write(&g(), &json!("answered")).unwrap();
        write.complete(true);
    }
    let state = |host: &Host| host.inner.0.lock().unwrap().server_requests.entries()[0]["state"].clone();
    assert_eq!(state(&host), "settling");
    let projection = host.navigator_projection();
    assert_eq!(state(&host), "settling", "the projection settled a reply write");
    assert_eq!((projection.state.as_str(), &projection.generation, projection.generation_closed), ("ready", &g(), false));
    assert_eq!(projection.threads, vec![json!({"generation":g(),"threadId":"thread","name":"Invented","preview":"invented","status":{"type":"idle"},"cwd":"/invented"})]);
    let groups = crate::waiting_requests::groups_in(crate::home_resources::HomeClass::Account, &json!(projection.state), &projection.generation, &projection.server_requests);
    assert_eq!(groups.len(), 1);
    assert_eq!((groups[0]["threadId"].clone(), groups[0]["count"].clone()), (json!("child"), json!(1)));
    // The control: `snapshot` settles it.
    host.snapshot();
    assert_eq!(state(&host), "errored");
}
