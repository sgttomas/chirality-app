
    #[test]
    fn oauth_review_oh1_completion_unexpected_framing_id_is_not_public() {
        let host=host();let login=oauth_fixture_login(&host,false);
        host.on_line(&serde_json::to_vec(&json!({"method":"account/login/completed","id":AUTH_CANARY,"params":{"loginId":AUTH_CANARY,"success":true}})).unwrap(),&g());
        assert_eq!(host.account_oauth_observation(&login).unwrap()["phase"],"Pending");
        assert_auth_retained_safe(&host,Some(login.source()));
    }
    #[test]
    fn oauth_review_oh1_wrong_typed_reply_unexpected_echo_is_not_public() {
        let host=host();let login=oauth_fixture_login(&host,false);
        host.on_line(&serde_json::to_vec(&json!({"id":"1","result":{(AUTH_CANARY):AUTH_CANARY}})).unwrap(),&g());
        assert_eq!(host.account_oauth_observation(&login).unwrap()["phase"],"Pending");
        assert_auth_retained_safe(&host,Some(login.source()));
    }
