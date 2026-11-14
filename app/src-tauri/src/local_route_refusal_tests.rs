// DEL-01-05 "For 4.0.0": the App does not offer a local model server or a local
// provider, and every host command that would prepare, read, create, edit,
// select or start that route refuses at the command boundary with words a
// person can act on. These tests call each command that takes only the App's
// state, and read the source of those that also take a window or an App
// handle (a mock App cannot supply the release runtime's window), so a command
// that stops refusing fails here.
use super::*;
use tauri::{test::mock_app, Manager};

fn refuses(result: Result<Value, String>, command: &str) {
    assert_eq!(result.unwrap_err(), LOCAL_ROUTE_NOT_OFFERED, "{command} refuses with the words a person can act on");
}

#[test]
fn local_route_words_name_what_is_not_offered_and_what_to_do() {
    assert!(!LOCAL_ROUTE_OFFERED, "the local route is not offered in this version");
    assert!(LOCAL_ROUTE_NOT_OFFERED.starts_with("This version of the App does not offer a local model server or a local provider."));
    assert!(LOCAL_ROUTE_NOT_OFFERED.contains("sign in under Connection and access"), "it says what the person can do instead");
    assert_eq!(local_route_refused().unwrap_err(), LOCAL_ROUTE_NOT_OFFERED);
    let reading = local_route_not_offered_reading();
    assert_eq!(reading, json!({"state":"not-in-this-version","offered":false,"reason":LOCAL_ROUTE_NOT_OFFERED}), "a read returns a reading, not a fault");
}

#[test]
fn every_state_only_local_route_command_refuses_and_reads_return_not_in_this_version() {
    let (root, state, home, _, _, _) = super::workflow_root_context_tests::fixture();
    let generation = home.host.snapshot()["generation"].clone();
    let app = mock_app();
    app.manage(state);
    let state = || app.state::<AppState>();
    refuses(provider_create_offer(state(), generation.clone(), "invented-provider".into(), "Invented".into(), "http://127.0.0.1:8000/v1".into(), "e".into()), "provider_create_offer");
    refuses(provider_endpoint_offer(state(), generation.clone(), "invented-provider".into(), "http://127.0.0.1:8000/v1".into(), "e".into()), "provider_endpoint_offer");
    refuses(select_home(state(), "local-provider".into()), "select_home(local-provider)");
    assert_eq!(state().homes.lock().unwrap().snapshot()["activeModeHomeClass"], json!("account"), "the account home stays active");
    refuses(host_start(state(), "local-provider".into()), "host_start(local-provider)");
    assert_eq!(read_configured_providers(state(), generation.clone(), "account".into()).unwrap(), local_route_not_offered_reading());
    assert_eq!(local_model_settings_read(state()), local_route_not_offered_reading());
    // The account home is still selectable: only the local route is refused.
    assert!(select_home(state(), "account".into()).is_ok());
    std::fs::remove_dir_all(root).unwrap();
}

/// The body of `fn name(` in lib.rs, from its opening brace.
fn body(source: &str, name: &str) -> String {
    let start = source.find(&format!("fn {name}(")).unwrap_or_else(|| panic!("{name} is in lib.rs"));
    let open = start + source[start..].find('{').unwrap();
    source[open + 1..].lines().map(str::trim).filter(|line| !line.is_empty()).take(1).collect()
}

#[test]
fn every_local_route_command_that_takes_a_window_refuses_before_anything_else() {
    let source = include_str!("lib.rs");
    for name in ["prepare_local_provider", "submit_local_provider_key", "local_model_settings_save", "provider_create_save", "provider_endpoint_save",
        "provider_create_offer", "provider_endpoint_offer"] {
        assert_eq!(body(source, name), "local_route_refused()?;", "{name} refuses as its first statement");
    }
    for name in ["read_configured_providers", "local_model_settings_read"] {
        assert!(body(source, name).starts_with("if !LOCAL_ROUTE_OFFERED { return"), "{name} returns the not-in-this-version reading first");
    }
    // A conversation start refuses the local entries, and any start in the local home, before the entry check.
    let start = &source[source.find("fn start_conversation_inner(").unwrap()..];
    let guard = start.find("if entry_id==native_local_provider::ENTRY || entry_id==\"local-provider\" || home.class()==home_resources::HomeClass::LocalProvider { local_route_refused()?; }").expect("the start's guard");
    assert!(guard < start.find("let allowed = match home.class()").unwrap(), "the guard comes before the entry check");
}
