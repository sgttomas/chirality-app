//! Unread source delivery to the Host's one in-process native projection owner.
//!
//! These events do not use observer JSON, diagnostic cursors or Serde tokens.
//! The parent Host serializes publication, pending capture and acknowledgment
//! under its Inner lock. Incorporation is acknowledged by exact Arc prefix
//! identity; dropping a batch acknowledges nothing. This lifetime ends at
//! projection incorporation, not at a global memory bound or retention limit.

use serde_json::Value;
use std::collections::VecDeque;
use std::sync::Arc;

pub(crate) enum NativeProjectionEvent {
    Ready(Value),
    Frame(Value),
    Close(Value),
}

// Only claim creates the private identity. Neither ownership nor a pending
// prefix can be reconstructed from an observation, serialized or cloned.
pub(crate) struct NativeProjectionOwner {
    key: Arc<()>,
}

pub(crate) struct NativeProjectionBatch {
    key: Arc<()>,
    prefix: Vec<Arc<NativeProjectionEvent>>,
    pub(super) observation: Value,
}

impl NativeProjectionBatch {
    pub(crate) fn observation(&self) -> &Value {
        &self.observation
    }

    pub(crate) fn events(&self) -> impl Iterator<Item = &NativeProjectionEvent> {
        self.prefix.iter().map(Arc::as_ref)
    }
}

pub(super) struct NativeDelivery {
    key: Arc<()>,
    claimed: bool,
    events: VecDeque<Arc<NativeProjectionEvent>>,
}

impl Default for NativeDelivery {
    fn default() -> Self {
        Self {
            key: Arc::new(()),
            claimed: false,
            events: VecDeque::new(),
        }
    }
}

impl NativeDelivery {
    pub(super) fn claim(&mut self) -> Result<NativeProjectionOwner, String> {
        if self.claimed {
            return Err("native projection owner already claimed for this Host".into());
        }
        self.claimed = true;
        Ok(NativeProjectionOwner {
            key: Arc::clone(&self.key),
        })
    }

    pub(super) fn publish(&mut self, event: NativeProjectionEvent) {
        self.events.push_back(Arc::new(event));
    }

    pub(super) fn pending(
        &self,
        owner: &NativeProjectionOwner,
        observation: Value,
    ) -> Result<NativeProjectionBatch, String> {
        self.check_owner(owner)?;
        Ok(NativeProjectionBatch {
            key: Arc::clone(&self.key),
            prefix: self.events.iter().cloned().collect(),
            observation,
        })
    }

    pub(super) fn ack(
        &mut self,
        owner: &NativeProjectionOwner,
        batch: NativeProjectionBatch,
    ) -> Result<(), String> {
        self.check_owner(owner)?;
        if !Arc::ptr_eq(&self.key, &batch.key) {
            return Err("native projection batch belongs to another Host".into());
        }
        // Check the entire prefix before removing anything. Equal JSON from a
        // later publication is a different event, and cannot satisfy an old ack.
        if self.events.len() < batch.prefix.len()
            || !self
                .events
                .iter()
                .zip(&batch.prefix)
                .all(|(current, original)| Arc::ptr_eq(current, original))
        {
            return Err("native projection batch prefix is no longer pending".into());
        }
        // Empty batches are owner-validated no-ops, including after appends.
        for _ in 0..batch.prefix.len() {
            let _ = self.events.pop_front();
        }
        Ok(())
    }

    fn check_owner(&self, owner: &NativeProjectionOwner) -> Result<(), String> {
        if !Arc::ptr_eq(&self.key, &owner.key) {
            return Err("native projection owner belongs to another Host".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    use std::sync::Mutex;

    fn generation(counter: u64) -> Value {
        json!({"appSession":"delivery-session","home":"delivery-home","spawnCounter":counter})
    }

    fn positioned(counter: u64, position: u64, text: &str) -> Value {
        json!({"generation":generation(counter),"position":position,"class":"notification",
            "frame":{"method":"item/agentMessage/delta","params":{"threadId":"thread","turnId":"turn","itemId":"item","delta":text},
                "emittedAtMs":17,"supplierExtra":{"typedId":"1","number":1,"nested":[null,true,{"unchanged":"é\n包括"}]}}})
    }

    fn observations(batch: &NativeProjectionBatch) -> Vec<(&'static str, Value)> {
        batch
            .events()
            .map(|event| match event {
                NativeProjectionEvent::Ready(value) => ("ready", value.clone()),
                NativeProjectionEvent::Frame(value) => ("frame", value.clone()),
                NativeProjectionEvent::Close(value) => ("close", value.clone()),
            })
            .collect()
    }

    fn pending(delivery: &NativeDelivery, owner: &NativeProjectionOwner) -> NativeProjectionBatch {
        delivery
            .pending(owner, json!({"state":"observed"}))
            .unwrap()
    }

    #[test]
    fn preserves_publication_order_full_generations_and_all_projected_values() {
        let mut delivery = NativeDelivery::default();
        let first_ready = json!({"generation":generation(1),"state":"ready","versionIdentity":{"supplier":"original"}});
        let first = positioned(1, 1, "first");
        let second = positioned(1, 2, "second");
        let second_ready =
            json!({"generation":generation(2),"state":"ready","supplierExtra":false});
        let next = positioned(2, 1, "new generation, reset position");
        delivery.publish(NativeProjectionEvent::Ready(first_ready.clone()));
        delivery.publish(NativeProjectionEvent::Frame(first.clone()));
        delivery.publish(NativeProjectionEvent::Frame(second.clone()));
        delivery.publish(NativeProjectionEvent::Close(generation(1)));
        delivery.publish(NativeProjectionEvent::Ready(second_ready.clone()));
        delivery.publish(NativeProjectionEvent::Frame(next.clone()));
        let owner = delivery.claim().unwrap();
        let final_observation = json!({"generation":generation(2),"state":"ready","ordinaryEvidence":{"value":"retained"}});
        let mut batch = delivery.pending(&owner, final_observation.clone()).unwrap();
        assert_eq!(batch.observation(), &final_observation);
        assert_eq!(
            observations(&batch),
            vec![
                ("ready", first_ready),
                ("frame", first),
                ("frame", second),
                ("close", generation(1)),
                ("ready", second_ready),
                ("frame", next),
            ]
        );
        // The parent can append normal evidence outside Inner. It cannot edit
        // the private event identities or turn observation JSON into an ack.
        batch.observation["ordinaryEvidence"]["outsideInner"] = json!(true);
        delivery.ack(&owner, batch).unwrap();
        assert_eq!(pending(&delivery, &owner).events().count(), 0);
    }

    #[test]
    fn close_without_ready_is_not_replaced_by_an_invented_ready() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        delivery.publish(NativeProjectionEvent::Close(generation(7)));
        let batch = pending(&delivery, &owner);
        assert_eq!(observations(&batch), vec![("close", generation(7))]);
        delivery.ack(&owner, batch).unwrap();
    }

    #[test]
    fn dropping_unacked_batch_preserves_exact_events_for_retry() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        let frame = positioned(1, 4, "no acknowledgment");
        delivery.publish(NativeProjectionEvent::Frame(frame.clone()));
        let first = delivery
            .pending(&owner, json!({"cursor":999,"ack":true}))
            .unwrap();
        let original = Arc::clone(&first.prefix[0]);
        drop(first);
        let retry = pending(&delivery, &owner);
        assert!(Arc::ptr_eq(&retry.prefix[0], &original));
        assert_eq!(observations(&retry), vec![("frame", frame)]);
        delivery.ack(&owner, retry).unwrap();
        assert_eq!(pending(&delivery, &owner).events().count(), 0);
    }

    #[test]
    fn independent_append_after_capture_survives_prefix_ack() {
        let delivery = Arc::new(Mutex::new(NativeDelivery::default()));
        let owner = delivery.lock().unwrap().claim().unwrap();
        let first = positioned(1, 1, "captured");
        delivery
            .lock()
            .unwrap()
            .publish(NativeProjectionEvent::Frame(first.clone()));
        let captured = pending(&delivery.lock().unwrap(), &owner);
        let publisher = Arc::clone(&delivery);
        let later = positioned(1, 2, "published after capture");
        let published = later.clone();
        std::thread::spawn(move || {
            let mut delivery = publisher.lock().unwrap();
            delivery.publish(NativeProjectionEvent::Frame(published));
            delivery.publish(NativeProjectionEvent::Close(generation(1)));
        })
        .join()
        .unwrap();
        assert_eq!(observations(&captured), vec![("frame", first)]);
        let mut delivery = delivery.lock().unwrap();
        delivery.ack(&owner, captured).unwrap();
        assert_eq!(
            observations(&pending(&delivery, &owner)),
            vec![("frame", later), ("close", generation(1))]
        );
    }

    #[test]
    fn second_claim_refuses_even_after_original_owner_is_dropped() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        assert!(delivery.claim().is_err());
        delivery.publish(NativeProjectionEvent::Close(generation(1)));
        assert_eq!(pending(&delivery, &owner).events().count(), 1);
        drop(owner);
        assert!(delivery.claim().is_err());
        assert_eq!(delivery.events.len(), 1);
    }

    #[test]
    fn wrong_host_owner_or_batch_refuses_without_removing_either_queue() {
        let mut first = NativeDelivery::default();
        let mut second = NativeDelivery::default();
        let first_owner = first.claim().unwrap();
        let second_owner = second.claim().unwrap();
        let frame = positioned(1, 1, "identical payload does not share ownership");
        first.publish(NativeProjectionEvent::Frame(frame.clone()));
        second.publish(NativeProjectionEvent::Frame(frame.clone()));
        assert!(first.pending(&second_owner, Value::Null).is_err());
        let batch = pending(&first, &first_owner);
        assert!(first.ack(&second_owner, batch).is_err());
        let wrong_host_batch = pending(&second, &second_owner);
        assert!(first.ack(&first_owner, wrong_host_batch).is_err());
        assert_eq!(
            observations(&pending(&first, &first_owner)),
            vec![("frame", frame.clone())]
        );
        assert_eq!(
            observations(&pending(&second, &second_owner)),
            vec![("frame", frame)]
        );
    }

    #[test]
    fn stale_competing_prefix_cannot_ack_a_later_equal_value_event() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        let value = positioned(1, 1, "same JSON, different publication");
        delivery.publish(NativeProjectionEvent::Frame(value.clone()));
        let first = pending(&delivery, &owner);
        let competing = pending(&delivery, &owner);
        delivery.ack(&owner, first).unwrap();
        delivery.publish(NativeProjectionEvent::Frame(value.clone()));
        assert!(delivery.ack(&owner, competing).is_err());
        assert_eq!(
            observations(&pending(&delivery, &owner)),
            vec![("frame", value)]
        );
    }

    #[test]
    fn superseded_wider_batch_does_not_remove_the_remaining_tail() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        delivery.publish(NativeProjectionEvent::Frame(positioned(1, 1, "prefix")));
        let narrow = pending(&delivery, &owner);
        let tail = positioned(1, 2, "tail");
        delivery.publish(NativeProjectionEvent::Frame(tail.clone()));
        let wider = pending(&delivery, &owner);
        delivery.ack(&owner, narrow).unwrap();
        assert!(delivery.ack(&owner, wider).is_err());
        assert_eq!(
            observations(&pending(&delivery, &owner)),
            vec![("frame", tail)]
        );
    }

    #[test]
    fn mismatched_tail_is_checked_before_any_matching_head_is_removed() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        let first = positioned(1, 1, "matching head");
        let second = positioned(1, 2, "mismatched identity");
        delivery.publish(NativeProjectionEvent::Frame(first.clone()));
        delivery.publish(NativeProjectionEvent::Frame(second.clone()));
        let mut corrupted = pending(&delivery, &owner);
        // Test-only access models a bad later prefix member. Production callers
        // cannot construct or modify these private identities from JSON.
        corrupted.prefix[1] = Arc::new(NativeProjectionEvent::Frame(second.clone()));
        assert!(delivery.ack(&owner, corrupted).is_err());
        assert_eq!(
            observations(&pending(&delivery, &owner)),
            vec![("frame", first), ("frame", second)]
        );
    }

    #[test]
    fn validated_empty_batches_do_not_drain_later_appends() {
        let mut delivery = NativeDelivery::default();
        let owner = delivery.claim().unwrap();
        let first_empty = pending(&delivery, &owner);
        let competing_empty = pending(&delivery, &owner);
        let tail = positioned(1, 1, "later append");
        delivery.publish(NativeProjectionEvent::Frame(tail.clone()));
        delivery.ack(&owner, first_empty).unwrap();
        delivery.ack(&owner, competing_empty).unwrap();
        assert_eq!(
            observations(&pending(&delivery, &owner)),
            vec![("frame", tail)]
        );
        let mut other = NativeDelivery::default();
        let other_owner = other.claim().unwrap();
        let foreign_empty = pending(&other, &other_owner);
        assert!(delivery.ack(&owner, foreign_empty).is_err());
        assert_eq!(delivery.events.len(), 1);
    }
}
