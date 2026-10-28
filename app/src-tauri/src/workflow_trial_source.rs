//! Future clean-trial native history correspondence. Unsigned App metadata,
//! never a native receipt, hot authoring default, run, selection or act.
use super::*;
use std::path::Path;

pub(crate) const OWNER: &str = "DEL-02-02/clean-trial-source/v1";
pub(crate) fn owner(reference: &str) -> String {
    format!("{OWNER}/{reference}")
}
const STANDING: &str = "historical clean-trial source correspondence only; no native receipt, authoring default, run, selection, registration or act restored";
#[cfg(test)]
thread_local! { pub(crate) static FAIL_METADATA: std::cell::Cell<Option<&'static str>> = const { std::cell::Cell::new(None) }; }

/// Identity facts only; no lease crosses a native wait.
pub(crate) fn physical(path: &Path) -> Result<Value, String> {
    physical_kind(path, false)
}
fn physical_kind(path: &Path, directory: bool) -> Result<Value, String> {
    crate::workflow_workspace::registration::drafts::trials::source_physical(path, directory)
}

fn native_home(home: &HomeSession) -> Result<Value, String> {
    let config = home
        .host_config
        .as_ref()
        .map_err(|cause| format!("clean trial native home configuration unavailable: {cause}"))?;
    let expected = format!(
        "app-home:{}",
        crate::util::sha256_hex(config.codex_home.as_os_str().as_encoded_bytes())
    );
    if home.host.snapshot()["generation"]["home"] != expected {
        return Err("clean trial configured native home differs from original current Host".into());
    }
    physical_kind(&config.codex_home, true)
}

fn original_occurrence(
    rows: &[Value],
    link: &Value,
    generation: &Value,
    class: &str,
) -> Result<(), String> {
    crate::recovery::generation_ref(generation)?;
    let thread = link["trial"]["clean_conversation"]
        .as_str()
        .ok_or("clean trial conversation absent")?;
    if !rows
        .iter()
        .any(|row| row["kind"] == "session_started" && row["session"] == generation["appSession"])
    {
        return Err("clean trial original REC app session unavailable".into());
    }
    let original = crate::recovery::generation_ref(generation)?;
    if !rows.iter().any(|row| {
        row["kind"] == "conversation_index"
            && row["threadId"] == thread
            && row["home"] == class
            && row["session"] == generation["appSession"]
            && row["lastLoadedGeneration"] == original
    }) {
        return Err("clean trial original full REC generation occurrence unavailable".into());
    }
    Ok(())
}

/// Only a genuine Host positive observation can create a held pointer. Decoded
/// metadata has a separate read-only Proof and cannot be persisted by this API.
pub(crate) struct Pointer {
    value: Value,
    host: std::sync::Arc<crate::hosting::Host>,
    pub status: Value,
    saved: Option<Value>,
    native_home_path: std::path::PathBuf,
}
impl Pointer {
    pub(crate) fn observed(
        home: &HomeSession,
        positive: &crate::hosting::PositiveTextStart,
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        reference: &str,
        text: &TrialText,
    ) -> Result<Self, String> {
        home.host.check_positive_text_start(positive)?;
        let (link, link_source) = links.source_link(reference)?;
        let frame = positive.source().attempted_frame();
        let trial = &link["trial"];
        if trial["kind"] != "clean"
            || trial["reference"] != text.reference()
            || trial["text_identity"] != text.identity()
            || trial["text_bytes"] != text.bytes()
            || trial["snapshot_folder"] != text.snapshot_folder()
            || trial["turn"] != positive.turn()
            || trial["client_message"] != frame["params"]["clientUserMessageId"]
            || trial["clean_conversation"] != frame["params"]["threadId"]
            || frame["params"]["input"][0]["text"] != text.text()
        {
            return Err("clean trial acknowledged text/link correspondence differs".into());
        }
        let class = crate::stop_records::home_class(home.class().as_str())
            .ok_or("clean trial native home class unavailable")?;
        let (path, rows) = home.host.trial_recovery_rows()?;
        original_occurrence(&rows, &link, positive.source().generation(), class)?;
        let value = json!({"version":1,"link":link,"linkSource":link_source,"generation":positive.source().generation(),"homeClass":class,"recSource":physical(&path)?,"nativeHome":native_home(home)?,"standing":STANDING});
        Ok(Self {
            value,
            host: home.host.clone(),
            status: Value::Null,
            saved: None,
            native_home_path: home
                .host_config
                .as_ref()
                .map_err(Clone::clone)?
                .codex_home
                .clone(),
        })
    }
    pub(crate) fn persist(
        &mut self,
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
    ) -> Value {
        let result = (|| {
            let (link, proof) = links.source_link(
                self.value["link"]["trial"]["reference"]
                    .as_str()
                    .ok_or("held trial reference absent")?,
            )?;
            if link != self.value["link"] || proof != self.value["linkSource"] {
                return Err("held original trial link changed; metadata not rebound".to_string());
            }
            let (path, rows) = self.host.trial_recovery_rows()?;
            if physical(&path)? != self.value["recSource"] {
                return Err("held original REC physical source changed".into());
            }
            original_occurrence(
                &rows,
                &link,
                &self.value["generation"],
                self.value["homeClass"].as_str().unwrap_or_default(),
            )?;
            let now = self.host.snapshot()["generation"].clone();
            let original = &self.value["generation"];
            if now["home"] != original["home"] || now["appSession"] != original["appSession"] {
                return Err("original source owner closed; metadata cannot be rebound".into());
            }
            if physical_kind(&self.native_home_path, true)? != self.value["nativeHome"] {
                return Err("held native home replaced; metadata not rebound".into());
            }
            #[cfg(test)]
            FAIL_METADATA.with(|mode| match mode.take() {
                Some("before") => {
                    crate::recovery::store::FAIL_BATCH_AFTER.with(|hook| hook.set(Some(0)))
                }
                Some("after") => {
                    crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|hook| hook.set(true))
                }
                _ => {}
            });
            Ok(self.host.tag_conversation(
                &now,
                link["trial"]["clean_conversation"].as_str().unwrap(),
                self.value["homeClass"].as_str(),
                &owner(link["trial"]["reference"].as_str().unwrap()),
                &self.value.to_string(),
            ))
        })();
        let mut attempt = result.unwrap_or_else(
            |cause| json!({"persistence":"memory-only","limit":cause,"standing":STANDING}),
        );
        if attempt["persistence"] == "durable App metadata" {
            attempt["state"] = json!("saved");
            self.saved = Some(attempt.clone());
        } else if let Some(saved) = &self.saved {
            attempt["state"] = json!("saved; current revalidation unavailable");
            attempt["persistence"] = json!("durable App metadata previously confirmed");
            attempt["originalSave"] = saved.clone();
        } else {
            // An error after commit may have landed the exact tag. Neither a
            // transport error nor a failed flush proves durable absence.
            attempt["state"] = json!("save not confirmed");
            attempt["persistence"] = json!("not confirmed");
        }
        attempt["heldMetadata"] = json!(true);
        attempt["pointerIdentity"] =
            json!(crate::util::sha256_hex(self.value.to_string().as_bytes()));
        attempt["retry"] =
            json!("explicit Read again retries only this held metadata; never resends the trial");
        self.status = attempt;
        self.status.clone()
    }
}

#[derive(Clone)]
pub(crate) struct Proof {
    pub link: Value,
    pub generation: Value,
    pub class: String,
    link_source: Value,
    rec_source: Value,
    pointer: Value,
    occurrences: Vec<Value>,
}
impl Proof {
    fn from_homes(
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        reference: &str,
        homes: &[&HomeSession],
    ) -> Result<(Self, usize), String> {
        let (link, link_source) = links.source_link(reference)?;
        if link["trial"]["kind"] != "clean" {
            return Err("delegated cold child source not established".into());
        }
        let mut claims = BTreeMap::<String, (Value, Value, Vec<Value>)>::new();
        for home in homes {
            let Ok((path, rows)) = home.host.trial_recovery_rows() else {
                continue;
            };
            let rec_source = physical(&path)?;
            for row in rows.iter().filter(|r| r["kind"] == "conversation_index") {
                for tag in row["tags"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .filter(|t| t["owner"] == owner(reference))
                {
                    let raw = tag["value"]
                        .as_str()
                        .ok_or("clean trial source pointer is not text")?;
                    let value: Value = serde_json::from_str(raw)
                        .map_err(|_| "clean trial source pointer malformed")?;
                    if value["link"]["trial"]["reference"] != reference {
                        return Err("clean trial relevant pointer names a different trial".into());
                    }
                    let fields = [
                        "version",
                        "link",
                        "linkSource",
                        "generation",
                        "homeClass",
                        "recSource",
                        "nativeHome",
                        "standing",
                    ];
                    if value.as_object().is_none_or(|o| {
                        o.len() != fields.len() || fields.iter().any(|k| !o.contains_key(*k))
                    }) || value["version"] != 1
                        || value["standing"] != STANDING
                        || value["link"] != link
                        || value["linkSource"] != link_source
                        || value["recSource"] != rec_source
                        || value["homeClass"] != row["home"]
                        || row["threadId"] != link["trial"]["clean_conversation"]
                        || !matches!(value["homeClass"].as_str(), Some("H-acct" | "H-key"))
                    {
                        return Err(
                            "clean trial source pointer/link/physical correspondence differs"
                                .into(),
                        );
                    }
                    original_occurrence(
                        &rows,
                        &link,
                        &value["generation"],
                        value["homeClass"].as_str().unwrap(),
                    )?;
                    let original = crate::recovery::generation_ref(&value["generation"])?;
                    if !rows.iter().any(|original_row| {
                        original_row["kind"] == "conversation_index"
                            && original_row["home"] == value["homeClass"]
                            && original_row["threadId"] == link["trial"]["clean_conversation"]
                            && original_row["session"] == value["generation"]["appSession"]
                            && original_row["tags"]
                                .as_array()
                                .into_iter()
                                .flatten()
                                .any(|t| t["owner"] == owner(reference) && t["value"] == raw)
                    }) {
                        return Err("clean trial exact source pointer has no original-session REC occurrence".into());
                    }
                    let occurrence: Vec<_> = rows
                        .iter()
                        .filter(|r| {
                            (r["kind"] == "session_started"
                                && r["session"] == value["generation"]["appSession"])
                                || (r["kind"] == "conversation_index"
                                    && r["threadId"] == link["trial"]["clean_conversation"]
                                    && r["lastLoadedGeneration"] == original
                                    && r["session"] == value["generation"]["appSession"])
                        })
                        .cloned()
                        .collect();
                    claims.insert(raw.into(), (value, rec_source.clone(), occurrence));
                }
            }
        }
        if claims.len() != 1 {
            return Err("clean trial original source pointer unavailable or conflicting; no native source inferred".into());
        }
        let (_, (pointer, rec_source, occurrences)) = claims.into_iter().next().unwrap();
        let class = pointer["homeClass"].as_str().unwrap().to_owned();
        let candidates: Vec<_> = homes
            .iter()
            .enumerate()
            .filter(|(_, home)| {
                crate::stop_records::home_class(home.class().as_str()) == Some(class.as_str())
            })
            .collect();
        let [(index, home)] = candidates.as_slice() else {
            return Err("clean trial current source home missing or ambiguous; no fallback".into());
        };
        current_history_source(home, &home.host.snapshot()["generation"])?;
        if home.host.snapshot()["generation"]["home"] != pointer["generation"]["home"]
            || native_home(home)? != pointer["nativeHome"]
        {
            return Err("clean trial original native home changed; no same-class fallback".into());
        }
        // The selected owning current home must itself hold this original REC source.
        let (path, _) = home.host.trial_recovery_rows()?;
        if physical(&path)? != rec_source {
            return Err("current clean trial home does not hold the original REC source".into());
        }
        Ok((
            Self {
                link,
                generation: pointer["generation"].clone(),
                class,
                link_source,
                rec_source,
                pointer,
                occurrences,
            },
            *index,
        ))
    }
    pub(crate) fn read(
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        reference: &str,
        homes: &[std::sync::Arc<HomeSession>],
    ) -> Result<(Self, std::sync::Arc<HomeSession>), String> {
        let borrowed: Vec<_> = homes.iter().map(|home| home.as_ref()).collect();
        let (proof, index) = Self::from_homes(links, reference, &borrowed)?;
        Ok((proof, homes[index].clone()))
    }
    pub(crate) fn for_home(
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        reference: &str,
        home: &HomeSession,
    ) -> Result<Self, String> {
        Self::from_homes(links, reference, &[home]).map(|(proof, _)| proof)
    }
    pub(crate) fn recheck_home(
        &self,
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        home: &HomeSession,
    ) -> Result<(), String> {
        let now = Self::for_home(
            links,
            self.link["trial"]["reference"].as_str().unwrap(),
            home,
        )?;
        if now.link_source != self.link_source
            || now.rec_source != self.rec_source
            || now.pointer != self.pointer
            || now.occurrences != self.occurrences
        {
            return Err("clean trial durable source changed during history reading".into());
        }
        Ok(())
    }
    pub(crate) fn recheck(
        &self,
        links: &crate::workflow_workspace::registration::drafts::TrialLinks,
        homes: &[std::sync::Arc<HomeSession>],
    ) -> Result<std::sync::Arc<HomeSession>, String> {
        let (now, home) = Self::read(
            links,
            self.link["trial"]["reference"].as_str().unwrap(),
            homes,
        )?;
        if now.link_source != self.link_source
            || now.rec_source != self.rec_source
            || now.pointer != self.pointer
            || now.occurrences != self.occurrences
        {
            return Err("clean trial durable source changed during history reading".into());
        }
        Ok(home)
    }
    pub(crate) fn view(&self) -> Value {
        json!({"homeClass":self.class,"originalGeneration":self.generation,"standing":STANDING})
    }
}
