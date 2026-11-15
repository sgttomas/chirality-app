//! App-owned explanation of command/file/question answers. Supplier leaves are
//! marked by native_text::supplied on the sheet; the complete
//! frozen, annotated envelope is always available at the request card.
use crate::{act_control::native_statement as ns, request_answer_presentation as p};
use serde_json::{json, Value};

pub(crate) const STALE: &str = "Codex's request, or what this sheet said about it, changed while the sheet was open, so nothing was sent. Review the card and answer again.";
const OPENING: &str = "Send your answer to Codex? This answers Codex's request; it is not an act.";
const FOOTER: &str = "Send answer sends this answer once. Don't send (the default) and this sheet's Cancel button send nothing; this confirmation does not answer the request.";
const NO_DECLINE: &str = "Codex offers no way to refuse and let the agent continue: refusing interrupts the turn, and you can then tell the agent what to do instead.";
const LINKS: &str = "Locations are read from the paths Codex gave; the App has not followed links.";
const UNKNOWN_PROJECT: &str = "The App has not established where your project folder is, so it cannot mark which of these are inside it.";
const CHANGED: &str =
    "The request or its details changed since you last saw them; review them again.";

fn key(v: &Value) -> &str {
    v.as_str()
        .or_else(|| {
            v.as_object()
                .and_then(|o| o.keys().next().map(String::as_str))
        })
        .unwrap_or("")
}
fn text(v: &Value) -> String {
    v.as_str()
        .map(str::to_owned)
        .unwrap_or_else(|| v.to_string())
}
fn nonempty(v: &Value) -> Option<&str> {
    v.as_str().filter(|s| !s.is_empty())
}
fn words(section: &str, key: &str) -> Result<String, String> {
    let table: Value = serde_json::from_str(include_str!("../../src/requestAnswerWords.json"))
        .expect("maintained App word table");
    table[section][key]
        .as_str()
        .map(str::to_owned)
        .ok_or_else(|| "The App has no answer wording for this choice; nothing sent".into())
}

/// Same lexical path arithmetic as RequestCards: no filesystem read or link
/// following, including the deliberately case-sensitive Windows comparison.
fn absolute(s: &str) -> bool {
    s.starts_with('/') || windows(s)
}
fn windows(s: &str) -> bool {
    let b = s.as_bytes();
    b.len() > 2 && b[0].is_ascii_alphabetic() && b[1] == b':' && matches!(b[2], b'/' | b'\\')
}
fn resolve(path: &str, base: Option<&str>) -> Option<(String, bool)> {
    let relative = !absolute(path);
    let full = if relative {
        format!("{}/{}", base.filter(|b| absolute(b))?, path)
    } else {
        path.into()
    };
    let win = windows(&full);
    let mut parts = full.split(|c| c == '/' || win && c == '\\');
    let root = parts.next().unwrap_or("");
    let mut kept = Vec::new();
    for part in parts {
        match part {
            "" | "." => {}
            ".." => {
                kept.pop();
            }
            _ => kept.push(part),
        }
    }
    Some((
        if win {
            format!("{}\\{}", root, kept.join("\\"))
        } else {
            format!("/{}", kept.join("/"))
        },
        relative,
    ))
}
fn location(value: &Value, cwd: Option<&str>, context: &Value) -> Value {
    let given = text(value);
    let Some((path, relative)) = resolve(&given, cwd) else {
        return p::detail("Path","codex",value.clone(),vec!["relative to a working folder the App has not received; where it goes cannot be shown".into()]);
    };
    let project = &context["project"];
    let (base, folder) = if project["kind"] == "folder" {
        (nonempty(&project["folder"]), "your project folder")
    } else if project["kind"] == "none" {
        (
            nonempty(&context["thread"]["cwd"]),
            "this conversation's working folder",
        )
    } else {
        (None, "your project folder")
    };
    let mark=match base.and_then(|b|resolve(b,None).map(|p|p.0)) {
        None if project["kind"]=="none"=>"The App has not received this conversation's working folder, so it cannot compare this location with it.".into(),
        None=>"The App could not compare it with your project folder, because it has not established where your project folder is.".into(),
        Some(base)=>{let sep=if windows(&base){"\\"}else{"/"};let prefix=if base.ends_with(sep){base.clone()}else{format!("{base}{sep}")};format!("{} {folder}",if path==base || path.starts_with(&prefix){"inside"}else{"OUTSIDE"})}
    };
    // The full resolved path and supplied resolution base travel together; the
    // source strings remain boxed on the page, with the App mark beside them.
    p::detail(
        "Path",
        "codex",
        json!({"path":path,"relativeTo":if relative {cwd} else {None}}),
        vec![mark],
    )
}

pub(crate) struct Prepared {
    pub(crate) context: Value,
    pub(crate) content: Value,
    pub(crate) digest: String,
    pub(crate) statement: ns::NativeStatement,
}

pub(crate) fn prepare(
    snapshot: &Value,
    generation: &Value,
    id: &Value,
    preview: &Value,
    choice: Option<&str>,
) -> Result<Prepared, String> {
    let context = p::context(snapshot, generation, id)?;
    let request = &context["request"];
    let method = request["method"].as_str().unwrap_or("");
    let parameters = &request["nativeParameters"];
    let answer = &preview["answer"];
    let command = matches!(method, p::COMMAND | p::LEGACY_COMMAND);
    let files = matches!(method, p::FILE | p::LEGACY_FILE);
    let question = method == p::QUESTION;
    let input = command && parameters["kind"] == "writeStdin";
    let decision = &answer["decision"];
    let decision_key = key(decision);
    let mut head = vec![OPENING.to_owned()];
    let mut details = Vec::new();
    let built_in =
        nonempty(&context["thread"]["permissionProfile"]).is_some_and(|p| p.starts_with(':'));
    let selected = if question {
        match choice {
            Some("question-decline")
                if answer["answers"].as_object().is_some_and(|o| o.is_empty()) =>
            {
                words("questionChoices", "question-decline")?
            }
            Some("question-answers") => words("questionChoices", "question-answers")?,
            // Old callers carry no presentation choice. Say only the semantic
            // answer, without inventing which of two equal-payload buttons ran.
            None => "Send question answers".into(),
            _ => return Err("The question button and answer do not agree; nothing sent".into()),
        }
    } else {
        if choice.is_some() {
            return Err("A question choice does not belong to this request; nothing sent".into());
        }
        words("decisions", decision_key)?
    };
    head.push(format!("Your answer: {selected}"));
    let modern_changes = context["item"]["native"]["changes"].as_array();
    let file_count = if method == p::FILE {
        modern_changes.filter(|a| !a.is_empty()).map(Vec::len)
    } else {
        parameters["fileChanges"].as_object().map(|o| o.len())
    };
    if question {
        let count = parameters["questions"].as_array().map_or(0, Vec::len);
        let answers = answer["answers"].as_object().map_or(0, |o| o.len());
        head.push(format!("Codex asks {count} question(s). This sends answers for {answers}; omitted questions stay unanswered. Entered empty answers are sent as empty answers."));
        if parameters["isBlocking"] == false {
            head.push("Not blocking the turn: the agent continues while this waits.".into());
        }
        for (i, q) in parameters["questions"]
            .as_array()
            .into_iter()
            .flatten()
            .enumerate()
        {
            let a = q["id"].as_str().and_then(|id| answer["answers"].get(id));
            let mut notes = vec![format!("Question {}", i + 1)];
            notes.push(
                if a.is_none() {
                    "No answer is sent for this question."
                } else if q["isSecret"] == true {
                    "The secret answer is masked here and sent unchanged."
                } else {
                    "The answer below is sent for this question."
                }
                .into(),
            );
            details.push(p::detail("Question", "codex", q["question"].clone(), notes));
            if !q["header"].is_null() {
                details.push(p::detail(
                    "Question heading",
                    "codex",
                    q["header"].clone(),
                    vec![],
                ));
            }
            for (option_index, option) in q["options"].as_array().into_iter().flatten().enumerate()
            {
                details.push(p::detail(
                    "Offered option",
                    "codex",
                    option["label"].clone(),
                    vec![format!("Option {}", option_index + 1)],
                ));
                if !option["description"].is_null() {
                    details.push(p::detail(
                        "Option description",
                        "codex",
                        option["description"].clone(),
                        vec![],
                    ));
                }
            }
            if let Some(a) = a {
                details.push(p::detail(
                    "Your answer",
                    "person",
                    a["answers"].clone(),
                    vec![],
                ));
            }
        }
    } else {
        let refusal = matches!(decision_key, "decline" | "cancel" | "denied" | "abort");
        if refusal {
            head.push(if input {"This input is not allowed. The command is already running and keeps running; refusing withholds this input only."}
                else if files {"These file changes are not allowed; Codex does not write them."} else {"This command is not allowed; it does not run."}.into());
            head.push(
                match decision_key {
                    "decline" => "The agent continues the turn without it.",
                    "cancel" => {
                        "The turn is interrupted; you can then tell the agent what to do instead."
                    }
                    "denied" => "The agent tries something else.",
                    _ => "The agent waits for your next message.",
                }
                .into(),
            );
        } else if command {
            if input {
                head.push("This request sends input to a command that is already running.".into());
            }
            head.push(if built_in {"If you allow this command, it runs once outside Codex's sandbox, with your account's access to all your files and to the network, in the working folder shown."}
                else {"If you allow this command, it runs once with more access than Codex's sandbox gives, which may be all of your account's access to your files and the network, in the working folder shown."}.into());
        } else if files {
            head.push(if file_count.is_some() {format!("If you allow this, Codex writes these files where they are shown, including any outside {}.",if context["project"]["kind"]=="none"{"this conversation's working folder"}else{"your project folder"})}
                else {"The App has not received the list of files, so it cannot show where these changes go. If you allow this, Codex writes changes you have not seen.".into()});
        }
        if matches!(decision_key, "acceptForSession" | "approved_for_session") {
            head.push(if files {"This answer also covers later changes to only these same files, until Codex stops. Nothing is saved."}else{"This answer also covers this same command, in this folder, until Codex stops. Nothing is saved."}.into());
        }
        if matches!(
            decision_key,
            "acceptWithExecpolicyAmendment" | "approved_execpolicy_amendment"
        ) {
            let rule = if decision_key == "acceptWithExecpolicyAmendment" {
                &decision[decision_key]["execpolicy_amendment"]
            } else {
                &decision[decision_key]["proposed_execpolicy_amendment"]
            };
            let prefix = if rule.as_array().is_some_and(|a| !a.is_empty()) {
                "the words shown"
            } else {
                "words Codex has not reported"
            };
            let access = if built_in {
                "runs outside Codex's sandbox"
            } else {
                "runs with more access than Codex's sandbox gives"
            };
            head.push(format!("This adds a lasting rule to the rules file in this App's sign-in folder: from then on, in every conversation of this home, any command beginning with {prefix} {access}, with no request to you. It stays until it is removed from that file."));
            details.push(p::detail("The rule's words", "codex", rule.clone(), vec![]));
        }
        if matches!(
            decision_key,
            "applyNetworkPolicyAmendment" | "network_policy_amendment"
        ) {
            let amendment = &decision[decision_key]["network_policy_amendment"];
            let action = match amendment["action"].as_str() {
                Some("allow") => "allows",
                Some("deny") => "denies",
                _ => return Err("Invalid network rule action; nothing sent".into()),
            };
            head.push(format!("This also applies the network rule Codex proposed for the host shown: it {action} network access to that host, and the rule is kept by Codex after this answer."));
            details.push(p::detail(
                "The host",
                "codex",
                amendment["host"].clone(),
                vec![],
            ));
        }
        if decision_key == "denied" {
            let reason = &decision["denied"]["rejection"];
            if nonempty(reason).is_some() {
                details.push(p::detail(
                    "Your reason, as it will be sent",
                    "person",
                    reason.clone(),
                    vec![],
                ));
            } else {
                head.push("No reason is sent.".into());
            }
        }
        let no_decline = parameters["availableDecisions"]
            .as_array()
            .is_some_and(|a| {
                a.iter().any(|v| key(v) == "cancel")
                    && !a
                        .iter()
                        .any(|v| matches!(key(v), "decline" | "denied" | "abort"))
            });
        if no_decline {
            head.push(NO_DECLINE.into());
        }
        if files && !parameters["grantRoot"].is_null() {
            if !refusal {
                head.push(if method==p::FILE {"It also asks to write under the folder shown for the rest of the session (Codex marks this UNSTABLE)."}else{"It also asks to write under the folder shown for the session."}.into());
            }
            details.push(p::detail(
                "The requested write folder",
                "codex",
                parameters["grantRoot"].clone(),
                vec![],
            ));
        }
        if files {
            head.push(LINKS.into());
            if context["project"]["kind"] == "unknown" {
                head.push(UNKNOWN_PROJECT.into());
            }
            head.push(
                file_count
                    .map(|n| format!("Codex asks to change {n} file(s)."))
                    .unwrap_or_else(|| {
                        "Codex asks to change files; the App has not received the list.".into()
                    }),
            );
            let cwd = nonempty(&parameters["cwd"]).or_else(|| nonempty(&context["thread"]["cwd"]));
            if method == p::FILE {
                for change in modern_changes.into_iter().flatten() {
                    let mut location = location(&change["path"], cwd, &context);
                    location["notes"].as_array_mut().unwrap().insert(
                        0,
                        json!(match change["kind"]["type"].as_str() {
                            Some("add") => "add",
                            Some("delete") => "delete",
                            Some("update") => "update",
                            _ => "change",
                        }),
                    );
                    details.push(location);
                    if nonempty(&change["kind"]["move_path"]).is_some() {
                        let mut dest =
                            location_for_move(&change["kind"]["move_path"], cwd, &context);
                        dest["notes"]
                            .as_array_mut()
                            .unwrap()
                            .insert(0, json!("moved to"));
                        details.push(dest);
                    }
                    details.push(p::detail(
                        "The change (diff)",
                        "codex",
                        change["diff"].clone(),
                        vec![],
                    ));
                }
            } else {
                for (path, change) in parameters["fileChanges"].as_object().into_iter().flatten() {
                    details.push(location(&json!(path), cwd, &context));
                    details.push(p::detail(
                        "The proposed change",
                        "codex",
                        change.clone(),
                        vec![],
                    ));
                }
            }
        } else {
            head.push(
                if input {
                    "Codex asks to send input to a command that is already running."
                } else {
                    "Codex asks to run a command."
                }
                .into(),
            );
            if parameters["command"].is_null() {
                head.push("Codex did not give a command.".into());
            } else {
                let command = if method == p::LEGACY_COMMAND {
                    parameters["command"]
                        .as_array()
                        .map(|a| json!(a.iter().map(text).collect::<Vec<_>>().join(" ")))
                        .unwrap_or_else(|| parameters["command"].clone())
                } else {
                    parameters["command"].clone()
                };
                details.push(p::detail("Command", "codex", command, vec![]));
            }
            if parameters["cwd"].is_null() {
                head.push("Codex did not give a working folder.".into());
                if !context["thread"]["cwd"].is_null() {
                    details.push(p::detail(
                        "The conversation's working folder",
                        "codex",
                        context["thread"]["cwd"].clone(),
                        vec![],
                    ));
                }
            } else {
                details.push(location(
                    &parameters["cwd"],
                    nonempty(&context["thread"]["cwd"]),
                    &context,
                ));
            }
            if context["project"]["kind"] == "unknown" {
                head.push("The App has not established where your project folder is.".into());
            }
            if !parameters["additionalPermissions"].is_null() {
                details.push(p::detail(
                    "Additional permissions requested",
                    "codex",
                    parameters["additionalPermissions"].clone(),
                    vec![],
                ));
            }
        }
        if !parameters["reason"].is_null() {
            details.push(p::detail(
                "Reason given",
                "codex",
                parameters["reason"].clone(),
                vec![],
            ));
        }
    }
    if nonempty(&context["thread"]["name"]).is_some() {
        head.push("Asked in: the conversation whose title is in the request details.".into());
        details.push(p::detail(
            "Conversation title",
            "codex",
            context["thread"]["name"].clone(),
            vec![],
        ));
    } else {
        head.push("Asked in: a conversation whose title Codex has not reported.".into());
    }
    let asker = &context["asker"];
    details.push(p::detail("Requester","codex",json!({"role":asker["role"],"nickname":asker["nickname"]}),vec![match asker["kind"].as_str(){Some("conversation")=>"Asked by the conversation's own agent",Some("delegated")=>"Asked by a delegated agent; any name and role below are as Codex reports them",Some("no-conversation")=>"Who asked is not established: no conversation is named",_=>"Who asked is not established: no delegation record from the Codex process that asked"}.into()]));
    let presentation = json!({"head":head,"details":details,"itemCount":details.len()});
    let (content, digest) = p::envelope(&context, answer, &presentation)?;
    let mut sheet = head;
    if p::changed(generation, id, &content) {
        sheet.insert(0, CHANGED.into());
    }
    let mut whole = sheet.clone();
    for row in &details {
        whole.extend(supplied_detail(row)?);
    }
    whole.push(format!(
        "These request and answer details are kept in full at the card: {digest}."
    ));
    whole.push(FOOTER.into());
    let text = match ns::bounded("Request answer", whole.join("\n")) {
        Ok(text) => text,
        Err(_) => {
            // Move every annotated detail as one unit. The complete selected
            // consequence, uncertainty warnings and Asked in stay on the sheet.
            sheet.push(format!("Request and answer details ({} items) are at the card, not here: {digest}. If unreadable now, cancel this sheet, read, then answer again.", details.len()));
            sheet.push(FOOTER.into());
            ns::bounded("Request answer", sheet.join("\n"))?
        }
    };
    let statement = ns::NativeStatement {
        text,
        in_app: Some(ns::InApp {
            kind: "request answer",
            digest: digest.clone(),
            content: content.clone(),
        }),
    };
    Ok(Prepared {
        context,
        content,
        digest,
        statement,
    })
}
/// Labels and provenance are closed caller-owned words. JSON is only the
/// companion transport; it never supplies the helper's static label.
fn supplied_detail(row: &Value) -> Result<Vec<String>, String> {
    use crate::native_text::{supplied, Source};
    let label = match row["label"].as_str() {
        Some("Question") => "Question",
        Some("Question heading") => "Question heading",
        Some("Offered option") => "Offered option",
        Some("Option description") => "Option description",
        Some("Your answer") => "Your answer",
        Some("Path") => "Path",
        Some("The rule's words") => "The rule's words",
        Some("The host") => "The host",
        Some("Your reason, as it will be sent") => "Your reason, as it will be sent",
        Some("The requested write folder") => "The requested write folder",
        Some("The change (diff)") => "The change (diff)",
        Some("The proposed change") => "The proposed change",
        Some("Command") => "Command",
        Some("The conversation's working folder") => "The conversation's working folder",
        Some("Additional permissions requested") => "Additional permissions requested",
        Some("Reason given") => "Reason given",
        Some("Conversation title") => "Asked in",
        Some("Requester") => "Requester",
        _ => return Err("An answer detail has no App-owned label; nothing sent".into()),
    };
    let source = match row["source"].as_str() {
        Some("codex") => Source::Codex,
        Some("person") => Source::Person,
        _ => return Err("An answer detail has no established source; nothing sent".into()),
    };
    let mut lines = Vec::new();
    if label == "Path" && row["value"].get("path").is_some() {
        lines.extend_from_slice(supplied("Full path", source, &row["value"]["path"]).lines());
        if !row["value"]["relativeTo"].is_null() {
            lines.extend_from_slice(
                supplied(
                    "Resolved against working folder",
                    source,
                    &row["value"]["relativeTo"],
                )
                .lines(),
            );
        }
    } else {
        lines.extend_from_slice(supplied(label, source, &row["value"]).lines());
    }
    // These notes are constructed solely from closed branches above. No
    // supplier value is interpolated into them.
    lines.extend(
        row["notes"]
            .as_array()
            .into_iter()
            .flatten()
            .filter_map(Value::as_str)
            .map(str::to_owned),
    );
    Ok(lines)
}

// Separate name because a local row also bears the name `location`.
fn location_for_move(value: &Value, cwd: Option<&str>, context: &Value) -> Value {
    location(value, cwd, context)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::native_request_answer::answer_with_choice;
    use crate::native_requests::RequestRegister;
    use std::cell::{Cell, RefCell};
    use tauri_plugin_dialog::MessageDialogResult;

    fn fixture(method: &str, params: Value) -> (Value, Value, Value, Value) {
        let g = json!({"appSession":"answer-sheet-tests","home":"invented","spawnCounter":1});
        let id = json!(format!(
            "{method}-{}",
            crate::util::opaque_id("test-").unwrap()
        ));
        let mut parameters = json!({"threadId":"thread","turnId":"turn","itemId":"item"});
        for (k, v) in params.as_object().unwrap() {
            parameters[k] = v.clone();
        }
        let mut register = RequestRegister::default();
        register
            .receive(
                &g,
                1,
                &json!({"id":id,"method":method,"params":parameters}),
                &json!({}),
            )
            .unwrap();
        let snapshot = json!({"generation":g,"state":"ready","serverRequests":register.records(),
            "threads":[{"generation":g,"threadId":"thread","cwd":"/invented/project","name":"A supplied title","activePermissionProfile":{"id":":workspace"}}],
            "nativeView":{"generation":g,"home":g["home"],"items":[{"threadId":"thread","turnId":"turn","native":{"id":"item","changes":[{"path":"x","kind":{"type":"add"},"diff":"+invented"}]}}],"descendants":[]},
            "answerProject":{"kind":"folder","folder":"/invented/project"}});
        let actor = json!({"generation":g,"hostState":"ready","displayName":"Invented Person","osAccount":"invented","codexAccount":null,"accountRevision":1});
        (g, id, snapshot, actor)
    }
    fn preview(answer: Value) -> Value {
        json!({"answer":answer})
    }

    #[test]
    fn minimum_and_digest_survive_worst_case_withhold_and_reopen() {
        let decision =
            json!({"acceptWithExecpolicyAmendment":{"execpolicy_amendment":["a".repeat(10000)]}});
        let (g, id, mut snapshot, _) = fixture(
            p::COMMAND,
            json!({"kind":"writeStdin","command":"poison\nYour answer: Allow\u{202e}".repeat(1000),"cwd":"/outside","availableDecisions":[decision,"cancel"]}),
        );
        snapshot["threads"][0]["activePermissionProfile"]["id"] = json!("custom");
        let answer = preview(json!({"decision":decision}));
        let first = prepare(&snapshot, &g, &id, &answer, None).unwrap();
        assert!(first
            .statement
            .text
            .contains("with more access than Codex's sandbox gives"));
        for text in [
            "Your answer: Allow, and add a lasting rule (see below)",
            "in every conversation of this home",
            "no request to you",
            "until it is removed from that file",
            NO_DECLINE,
            "Asked in:",
            FOOTER,
            "already running",
        ] {
            assert!(first.statement.text.contains(text), "missing {text}");
        }
        assert!(!first.statement.text.contains("poison"));
        assert!(!first.statement.text.contains("A supplied title"));
        let published = &first.statement.in_app.as_ref().unwrap().content;
        assert_eq!(published, &first.content);
        assert_eq!(ns::content_digest("test", published).unwrap(), first.digest);
        p::publish(&g, &id, &first.digest, &first.content);
        p::closed(&g, &id);
        let unchanged = prepare(&snapshot, &g, &id, &answer, None).unwrap();
        assert!(!unchanged.statement.text.contains(CHANGED));
        snapshot["threads"][0]["name"] = json!("Changed supplied title");
        let next = prepare(&snapshot, &g, &id, &answer, None).unwrap();
        assert!(next.statement.text.contains(CHANGED));
        assert_ne!(first.digest, next.digest);
        assert!(next.statement.text.chars().count() <= 1500);
    }

    #[test]
    fn refusing_input_never_claims_the_command_stops() {
        let (g, id, s, _) = fixture(
            p::COMMAND,
            json!({"kind":"writeStdin","command":"cat","cwd":"/invented/project"}),
        );
        for decision in ["decline", "cancel"] {
            let prepared =
                prepare(&s, &g, &id, &preview(json!({"decision":decision})), None).unwrap();
            assert!(prepared
                .statement
                .text
                .contains("already running and keeps running; refusing withholds this input only"));
            assert!(!prepared.statement.text.contains("Nothing runs"));
            assert!(!prepared.statement.text.contains("If you allow"));
        }
    }

    #[test]
    fn context_changes_refuse_send_even_when_actor_and_generation_do_not_change() {
        for change in [
            "profile",
            "cwd",
            "project",
            "files",
            "title",
            "parameters",
            "requester",
            "number-string",
            "number-object",
        ] {
            let (g, id, mut snapshot, actor) =
                fixture(p::FILE, json!({"additionalPermissions":{"fixture":0.5}}));
            // The exact same open parameter tree is bound, not a handpicked
            // digest input that could erase a value's original JSON type.
            snapshot["nativeView"]["descendants"] = json!([{"threadId":"thread","nativeThread":{"agentRole":"helper","agentNickname":"one"}}]);
            let source = RefCell::new(snapshot);
            let wrote = Cell::new(false);
            let result = answer_with_choice(
                &g,
                &id,
                &json!({"decision":"accept"}),
                None,
                || (source.borrow().clone(), actor.clone()),
                |_| {
                    let mut s = source.borrow_mut();
                    match change {
                        "profile" => {
                            s["threads"][0]["activePermissionProfile"]["id"] = json!("custom")
                        }
                        "cwd" => s["threads"][0]["cwd"] = json!("/other"),
                        "project" => s["answerProject"] = json!({"kind":"unknown"}),
                        "files" => {
                            s["nativeView"]["items"][0]["native"]["changes"][0]["path"] =
                                json!("/other")
                        }
                        "title" => s["threads"][0]["name"] = json!("other"),
                        "requester" => {
                            s["nativeView"]["descendants"][0]["nativeThread"]["agentRole"] =
                                json!("other")
                        }
                        "number-string" => {
                            s["serverRequests"][0]["nativeParameters"]["additionalPermissions"]
                                ["fixture"] = json!("0.5")
                        }
                        "number-object" => {
                            s["serverRequests"][0]["nativeParameters"]["additionalPermissions"]
                                ["fixture"] = json!({"number":"0.5"})
                        }
                        _ => {
                            s["serverRequests"][0]["nativeParameters"]["reason"] = json!("changed")
                        }
                    }
                    Ok(MessageDialogResult::Custom(ns::SEND_ANSWER.into()))
                },
                |_| {
                    wrote.set(true);
                    Ok(Value::Null)
                },
            );
            assert_eq!(result.unwrap_err(), STALE, "{change}");
            assert!(!wrote.get());
        }
    }

    #[test]
    fn question_choices_preserve_omitted_empty_and_masked_answers() {
        let (g, id, s, actor) = fixture(
            p::QUESTION,
            json!({"questions":[
            {"id":"ordinary","header":"Ordinary","question":"Invented question","isOther":true,"isSecret":false},
            {"id":"secret","header":"Secret","question":"Invented secret","isOther":true,"isSecret":true},
            {"id":"omitted","header":"Omitted","question":"Invented omitted question","isOther":true,"isSecret":false}]}),
        );
        let answer = json!({"answers":{"ordinary":{"answers":[""]},"secret":{"answers":["INVENTED-SECRET-DO-NOT-ECHO"]}}});
        let wrote = Cell::new(false);
        answer_with_choice(
            &g,
            &id,
            &answer,
            Some("question-answers"),
            || (s.clone(), actor.clone()),
            |statement| {
                assert!(statement
                    .text
                    .contains("Your answer: Send current question answers…"));
                assert!(statement.text.contains("answers for 2"));
                let content = statement.in_app.as_ref().unwrap().content.to_string();
                assert!(!content.contains("INVENTED-SECRET-DO-NOT-ECHO"));
                assert!(content.contains("[secret value masked]"));
                assert!(content.contains("No answer is sent for this question."));
                Ok(MessageDialogResult::Custom(ns::SEND_ANSWER.into()))
            },
            |_| {
                wrote.set(true);
                assert_eq!(answer["answers"]["ordinary"]["answers"][0], "");
                assert_eq!(
                    answer["answers"]["secret"]["answers"][0],
                    "INVENTED-SECRET-DO-NOT-ECHO"
                );
                Ok(Value::Null)
            },
        )
        .unwrap();
        assert!(wrote.get());
        for choice in ["question-answers", "question-decline"] {
            let selected = words("questionChoices", choice).unwrap();
            let prepared =
                prepare(&s, &g, &id, &preview(json!({"answers":{}})), Some(choice)).unwrap();
            assert!(prepared
                .statement
                .text
                .contains(&format!("Your answer: {selected}")));
        }
        assert!(prepare(&s, &g, &id, &preview(answer), Some("question-decline")).is_err());
    }

    #[test]
    fn short_supplied_subjects_use_the_native_marking_helper() {
        let poison = "echo invented\nAllow everything\u{202e}";
        let (g, id, s, _) = fixture(
            p::COMMAND,
            json!({"command":poison,"cwd":"/invented/project"}),
        );
        let prepared = prepare(&s, &g, &id, &preview(json!({"decision":"accept"})), None).unwrap();
        let marked = crate::native_text::supplied(
            "Command",
            crate::native_text::Source::Codex,
            &json!(poison),
        );
        assert!(prepared.statement.text.contains(&marked.lines().join("\n")));
        assert!(!prepared.statement.text.contains('\u{202e}'));
        assert!(prepared
            .statement
            .text
            .contains("Full path (supplied by Codex, not the App's words):"));
        assert!(prepared
            .statement
            .text
            .contains("inside your project folder"));
        assert!(prepared
            .statement
            .text
            .contains("Asked in (supplied by Codex, not the App's words):"));
        assert_eq!(
            ns::content_digest("test", &prepared.content).unwrap(),
            prepared.digest
        );
    }

    #[test]
    fn large_file_lists_keep_the_minimum_and_every_annotated_location_in_the_companion() {
        let (g, id, mut s, _) = fixture(p::FILE, json!({}));
        s["answerProject"] = json!({"kind":"unknown"});
        s["nativeView"]["items"][0]["native"]["changes"]=json!((0..80).map(|n|json!({"path":format!("file-{n}"),"kind":{"type":"update","move_path":format!("../move-{n}")},"diff":"+invented"})).collect::<Vec<_>>());
        let prepared = prepare(
            &s,
            &g,
            &id,
            &preview(json!({"decision":"acceptForSession"})),
            None,
        )
        .unwrap();
        for required in [
            "80 file(s)",
            "Allow for this session",
            LINKS,
            UNKNOWN_PROJECT,
            "Asked in:",
            FOOTER,
        ] {
            assert!(
                prepared.statement.text.contains(required),
                "missing {required}"
            );
        }
        let frozen = prepared.content.to_string();
        for n in 0..80 {
            assert!(frozen.contains(&format!("file-{n}")));
            assert!(frozen.contains(&format!("move-{n}")));
        }
        assert!(frozen.contains("could not compare"));
        assert!(prepared.statement.text.contains("at the card, not here"));
    }

    #[test]
    fn forms_and_permission_requests_keep_the_existing_sheet() {
        for (method, params, answer) in [
            (
                "mcpServer/elicitation/request",
                json!({"mode":"form","requestedSchema":{"type":"object"}}),
                json!({"action":"decline","content":null,"_meta":null}),
            ),
            (
                "item/permissions/requestApproval",
                json!({"permissions":{}}),
                json!({"permissions":{},"scope":"turn"}),
            ),
        ] {
            let (g, id, s, actor) = fixture(method, params);
            let a = crate::runtime_session::actor_reference(
                actor["displayName"].as_str(),
                actor["osAccount"].as_str(),
                actor["codexAccount"].as_str(),
            );
            let preview = crate::runtime_session::answer_preview(&s, &g, &id, &answer, &a).unwrap();
            let expected = ns::request_answer_statement(&preview).unwrap();
            answer_with_choice(
                &g,
                &id,
                &answer,
                None,
                || (s.clone(), actor.clone()),
                |actual| {
                    assert_eq!(actual.text, expected.text);
                    assert_eq!(
                        actual.in_app.as_ref().map(|a| &a.content),
                        expected.in_app.as_ref().map(|a| &a.content)
                    );
                    Ok(MessageDialogResult::Cancel)
                },
                |_| panic!("Cancel must not send"),
            )
            .unwrap();
        }
    }

    #[test]
    fn every_offered_command_and_file_answer_keeps_its_wire_value() {
        for method in [p::COMMAND, p::FILE, p::LEGACY_COMMAND, p::LEGACY_FILE] {
            let decisions = if matches!(method, p::LEGACY_COMMAND | p::LEGACY_FILE) {
                vec![
                    json!("approved"),
                    json!("approved_for_session"),
                    json!("abort"),
                    json!({"denied":{"rejection":"A".repeat(2000)}}),
                ]
            } else {
                vec![
                    json!("accept"),
                    json!("acceptForSession"),
                    json!("decline"),
                    json!("cancel"),
                ]
            };
            for decision in decisions {
                let (g, id, s, actor) = fixture(
                    method,
                    json!({"conversationId":"thread","command":["invented"],"cwd":"/invented/project","fileChanges":{"x":{"type":"add","content":"invented"}}}),
                );
                let answer = json!({"decision":decision});
                for send in [false, true] {
                    let writes = Cell::new(0);
                    let result=answer_with_choice(&g,&id,&answer,None,|| (s.clone(),actor.clone()),|statement| {
                        assert!(statement.text.contains(&words("decisions",key(&decision)).unwrap()));
                        assert!(!statement.text.contains(&"A".repeat(2000)));
                        Ok(if send {MessageDialogResult::Custom(ns::SEND_ANSWER.into())}else{MessageDialogResult::Cancel})
                    },|actor|{
                        let mut register=RequestRegister::default();
                        register.receive(&g,1,&json!({"id":id,"method":method,"params":s["serverRequests"][0]["nativeParameters"]}),&json!({})).unwrap();
                        let wire=register.prepare(&g,&id,&answer,"person-via-interaction",Some(actor))?;
                        assert_eq!(wire["result"],answer);
                        writes.set(writes.get()+1);Ok(json!({"replyWriteResult":"written","acknowledgment":"not-observed"}))
                    }).unwrap();
                    assert_eq!(writes.get(), usize::from(send));
                    if !send {
                        assert_eq!(result["state"], "dismissed");
                    }
                    assert!(p::companions(&g, &id)
                        .as_array()
                        .unwrap()
                        .iter()
                        .all(|row| row["pending"] == false));
                }
            }
        }
    }

    #[test]
    fn locations_preserve_comparison_unknown_and_resolution_base() {
        let (g, id, mut s, _) = fixture(p::FILE, json!({}));
        for project in [
            json!({"kind":"folder","folder":"/invented/project"}),
            json!({"kind":"none"}),
            json!({"kind":"unknown"}),
        ] {
            s["answerProject"] = project.clone();
            let context = p::context(&s, &g, &id).unwrap();
            let row = location(&json!("../outside"), Some("/invented/project"), &context);
            assert_eq!(row["value"]["path"], "/invented/outside");
            assert_eq!(row["value"]["relativeTo"], "/invented/project");
            let mark = row["notes"][0].as_str().unwrap();
            assert!(if project["kind"] == "unknown" {
                mark.contains("could not compare")
            } else {
                mark.starts_with("OUTSIDE")
            });
        }
        assert!(resolve("relative", None).is_none());
        assert_eq!(
            resolve("../other", Some("C:\\project\\folder")),
            Some(("C:\\project\\other".into(), true))
        );
    }
}

#[cfg(test)]
mod bounds_tests {
    use super::*;
    #[test]
    fn every_sheet_head_fits_including_missing_subject_and_changed_warning() {
        let decisions = vec![
            json!("accept"),
            json!("acceptForSession"),
            json!("decline"),
            json!("cancel"),
            json!({"acceptWithExecpolicyAmendment":{"execpolicy_amendment":[]}}),
            json!({"applyNetworkPolicyAmendment":{"network_policy_amendment":{"action":"deny","host":"invented"}}}),
        ];
        for input in [false, true] {
            for known in [false, true] {
                for supplied in [false, true] {
                    for decision in &decisions {
                        let g = json!({"appSession":"bound-fixture","home":"invented","spawnCounter":1});
                        let id = json!(format!("{input}-{known}-{supplied}-{decision}"));
                        let s = json!({"serverRequests":[{"generation":g,"requestIdentity":id,"method":p::COMMAND,"nativeParameters":{"command":if supplied{json!("command")}else{Value::Null},"cwd":if supplied{json!("/invented")}else{Value::Null},"kind":if input{"writeStdin"}else{"command"},"availableDecisions":[decision,"cancel"]}}],"answerProject":if known{json!({"kind":"none"})}else{json!({"kind":"unknown"})}});
                        let prepared =
                            prepare(&s, &g, &id, &json!({"answer":{"decision":decision}}), None)
                                .unwrap_or_else(|e| {
                                    panic!("{input}/{known}/{supplied}/{decision}: {e}")
                                });
                        // Reopen against a preceding different snapshot: the real
                        // formatter can move supplied details out, never the minimum.
                        p::publish(&g, &id, "previous", &json!({"different":true}));
                        p::closed(&g, &id);
                        let changed =
                            prepare(&s, &g, &id, &json!({"answer":{"decision":decision}}), None)
                                .unwrap_or_else(|e| {
                                    panic!("changed {input}/{known}/{supplied}/{decision}: {e}")
                                });
                        assert!(changed.statement.text.contains(CHANGED));
                        assert!(prepared.statement.text.contains(FOOTER));
                        assert!(changed.statement.text.contains(FOOTER));
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod shared_cases {
    use super::*;
    #[test]
    fn card_and_sheet_share_independent_consequence_examples() {
        let cases: Vec<Value> = serde_json::from_str(include_str!(
            "../../tests/fixtures/request_answer_cases.json"
        ))
        .unwrap();
        for case in cases {
            let g = json!({"appSession":"shared-example","home":"invented","spawnCounter":1});
            let id = case["name"].clone();
            let mut params = case["params"].clone();
            params["threadId"] = json!("thread");
            params["turnId"] = json!("turn");
            params["itemId"] = json!("item");
            let s = json!({"serverRequests":[{"generation":g,"requestIdentity":id,"method":case["method"],"nativeParameters":params}],
                "threads":[{"generation":g,"threadId":"thread","cwd":"/invented/project","activePermissionProfile":{"id":case["profile"]}}],
                "nativeView":{"generation":g,"home":g["home"],"items":[{"threadId":"thread","turnId":"turn","native":{"id":"item","changes":case["changes"]}}]},"answerProject":case["project"]});
            let prepared = prepare(
                &s,
                &g,
                &id,
                &json!({"answer":{"decision":case["decision"]}}),
                None,
            )
            .unwrap();
            for expected in case["expected"].as_array().unwrap() {
                assert!(
                    prepared
                        .statement
                        .text
                        .replace('’', "'")
                        .contains(&expected.as_str().unwrap().replace('’', "'")),
                    "{} missing {expected}",
                    case["name"]
                );
            }
        }
    }
}
