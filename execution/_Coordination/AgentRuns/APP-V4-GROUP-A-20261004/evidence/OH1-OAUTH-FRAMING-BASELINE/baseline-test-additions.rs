
    fn oauth_baseline_framing_source(host:&Arc<Host>)->SourceRequest {
        let mut source=None;
        exchange(host,Some(json!({"result":{"type":"chatgpt","loginId":AUTH_CANARY,"authUrl":AUTH_CANARY}})),vec![],||{
            let r=host.request_begin_scoped("account/login/start",json!({"type":"chatgpt"}),json!({"kind":"person-directed"}),false,Some(&g()))?;
            let o=host.source_request_wait(&r,Duration::from_millis(50))?;source=Some(r);Ok(o)
        }).0.unwrap();let source=source.unwrap();assert_auth_retained_safe(host,Some(&source));source
    }
    #[test]
    fn oauth_baseline_oh1_completion_unexpected_framing_id_is_not_public(){
        let host=host();let source=oauth_baseline_framing_source(&host);let before=source.evidence();
        host.on_line(&serde_json::to_vec(&json!({"method":"account/login/completed","id":AUTH_CANARY,"params":{"loginId":AUTH_CANARY,"success":true}})).unwrap(),&g());
        assert_eq!(source.evidence()["response"],before["response"]);assert_auth_retained_safe(&host,Some(&source));
    }
    #[test]
    fn oauth_baseline_oh1_wrong_typed_reply_unexpected_echo_is_not_public(){
        let host=host();let source=oauth_baseline_framing_source(&host);let before=source.evidence();
        host.on_line(&serde_json::to_vec(&json!({"id":"1","result":{(AUTH_CANARY):AUTH_CANARY}})).unwrap(),&g());
        assert_eq!(source.evidence()["response"],before["response"]);assert_auth_retained_safe(&host,Some(&source));
    }
