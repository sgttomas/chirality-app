//! Read-only Root consumer of Host-owned recovery metadata. This is no admission
//! route, ledger writer or native History client.
use crate::runtime_session::HomeSession;
use serde_json::{json, Value};

pub(crate) fn read(
    home: &HomeSession,
    expected_class: &str,
    expected_generation: &Value,
) -> Result<Value, String> {
    if home.class().as_str() != expected_class {
        return Err("Recovery source home selection changed; refresh the selected source".into());
    }
    let before = home.host.snapshot()["generation"].clone();
    if before != *expected_generation {
        return Err("Recovery source generation changed; refresh the selected source".into());
    }
    // Null means no supplier generation was observed. It is retained as null,
    // so recovery metadata remains readable before starting any supplier.
    if !before.is_null() {
        crate::recovery::generation_ref(&before)?;
    }
    let session = home.host.shared_recovery_observation()["appSession"].clone();
    let custody = home.host.recovery_custody().snapshot();
    if home.host.snapshot()["generation"] != before
        || home.host.shared_recovery_observation()["appSession"] != session
    {
        return Err("Recovery source changed while reading; no mixed-source view returned".into());
    }
    Ok(json!({
        "source": {"modeHomeClass": home.class().as_str(), "generation": before, "appSession": session},
        "readAt": crate::util::now_rfc3339(),
        "custody": custody,
        "readStanding": "Explicit read of this Host's cached App metadata; not a durable flush, native history fetch, current execution proof or automatic resume",
        "historicalScope": "Persisted App ledger rows retain their own original home and executionGeneration; they are not reassigned to the selected home",
        "nativeHistory": "Read separately through the existing native History controls; no pointer row becomes an operational conversation",
        "compatibility": "Ledger 0.3 preserves known item-to-turn pointers; legacy absent turnId remains unknown. Older 0.2 readers reject new correlated rows; preserve the ledger on rollback, do not strip pointers."
    }))
}
