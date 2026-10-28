//! Source-owned operational facts, independent of diagnostic replay storage.
//! These are minimal observations, not native envelopes or reconstructed authority.
//! Replay retention and its numerical policy are deliberately unchanged here.
use serde_json::{json, Value};
use std::collections::BTreeMap;

#[derive(Default)]
pub(super) struct ObservationFacts {
    generation: Value,
    turn_boundaries: BTreeMap<String, Value>,
    resolutions: Vec<(Value, Value)>,
    account_change: Option<u64>,
    exit: Option<Value>,
}

impl ObservationFacts {
    fn scope(&mut self, generation: &Value) {
        if self.generation != *generation {
            *self = Self {
                generation: generation.clone(),
                ..Self::default()
            };
        }
    }

    // Called only for an actual current, open source receipt, after sensitive
    // projection. Even a malformed native boundary must not revive an older
    // active-looking memo. Preserve only the fields used by the old journal scans.
    pub(super) fn receive(&mut self, generation: &Value, position: u64, frame: &Value) {
        self.scope(generation);
        match frame["method"].as_str() {
            Some("turn/started" | "turn/completed") => {
                if let Some(thread) = frame["params"]["threadId"].as_str() {
                    self.turn_boundaries.insert(
                        thread.to_owned(),
                        json!({
                            "generation":generation,"position":position,"method":frame["method"],
                            "threadId":thread,"turnId":frame["params"]["turn"]["id"].as_str(),
                            "status":frame["params"]["turn"]["status"].as_str()
                        }),
                    );
                }
            }
            Some("serverRequest/resolved") => {
                let subject = (
                    frame["params"]["requestId"].clone(),
                    frame["params"]["threadId"].clone(),
                );
                if !self.resolutions.contains(&subject) {
                    self.resolutions.push(subject);
                }
            }
            Some("account/updated") => self.account_change = Some(position),
            _ => (),
        }
    }

    pub(super) fn turn_boundary(&self, generation: &Value, thread: &str) -> Option<&Value> {
        (self.generation == *generation)
            .then(|| self.turn_boundaries.get(thread))
            .flatten()
    }

    pub(super) fn turn_boundaries(&self, generation: &Value) -> Vec<&Value> {
        if self.generation == *generation {
            self.turn_boundaries.values().collect()
        } else {
            vec![]
        }
    }

    pub(super) fn resolved(&self, generation: &Value, id: &Value, thread: &Value) -> bool {
        self.generation == *generation
            && self.resolutions.iter().any(|(i, t)| i == id && t == thread)
    }

    pub(super) fn account_revision(&self, generation: &Value) -> Value {
        json!({"generation":generation,"lastChangeReceiptPosition":
            if self.generation == *generation { self.account_change } else { None }})
    }

    pub(super) fn observe_exit(&mut self, generation: &Value, facts: Value) {
        self.scope(generation);
        self.exit = Some(facts);
    }

    pub(super) fn exit(&self, generation: &Value) -> Option<&Value> {
        (self.generation == *generation)
            .then_some(self.exit.as_ref())
            .flatten()
    }
}
