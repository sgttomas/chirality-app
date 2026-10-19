//! WI-1/WI-3: metadata-only menu projection and process-owned, single-use navigation.
//! Wake events carry no target. A selection waits here until the App claims it.
use crate::{runtime_session::HomeRouter, waiting_requests};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub(crate) const MENU_ID: &str = "chirality-waiting-requests";
pub(crate) const ITEM_PREFIX: &str = "chirality-waiting-item-";
pub(crate) const WAKE_EVENT: &str = "chirality-native-waiting";

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct Target {
    mode_home_class: String,
    generation: Value,
    thread_id: Option<String>,
    count: u64,
}
impl Target {
    fn validate(&self, homes: &HomeRouter) -> Result<(), String> {
        waiting_requests::validate(homes, &self.mode_home_class, &self.generation,
            &self.thread_id.as_ref().map_or(Value::Null, |s| Value::String(s.clone()))).map(|_| ())
    }
    fn label(&self) -> String {
        let conversation = self.thread_id.as_ref().map_or("no conversation named".into(), |s|format!("conversation {s}"));
        format!("{} · {}: {}", self.mode_home_class, conversation, self.count)
    }
}
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct MenuEntry { pub id: String, pub label: String, pub target: Target }
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
struct UiCheckpoint { consumer: String, revision: u64 }
#[derive(Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct Intent { pub intent_id: String, pub target: Target, checkpoint: Option<UiCheckpoint> }
struct Delivery { intent: Intent, consumer: Option<String> }
#[derive(Default)]
pub(crate) struct Registry {
    next: u64,
    entries: Vec<MenuEntry>,
    pending: Option<Delivery>,
    current_ui: Option<UiCheckpoint>,
}
impl Registry {
    fn id(&mut self) -> String {
        // One registry for the App process lifetime; never reuse retired menu IDs.
        self.next = self.next.checked_add(1).expect("native waiting ID space exhausted");
        format!("{ITEM_PREFIX}{}", self.next)
    }
    pub fn project(&mut self, overview: &Value) -> Vec<MenuEntry> {
        let targets: Vec<Target> = overview["groups"].as_array().into_iter().flatten()
            .filter_map(|g|serde_json::from_value(g.clone()).ok()).collect();
        let mut entries = Vec::new();
        for target in targets {
            let entry = self.entries.iter().find(|e|e.target == target).cloned()
                .unwrap_or_else(||MenuEntry { id:self.id(), label:target.label(), target });
            entries.push(entry);
        }
        self.entries = entries.clone();
        entries
    }
    /// Acknowledged renderer intent counters, not a permission or a clock.
    pub fn checkpoint(&mut self, consumer: &str, revision: u64) -> Result<(), String> {
        if consumer.is_empty() { return Err("Waiting UI consumer is missing".into()); }
        if self.current_ui.as_ref().is_some_and(|ui|ui.consumer == consumer && ui.revision > revision) {
            return Err("Waiting UI checkpoint cannot move backwards".into());
        }
        let ui = UiCheckpoint { consumer: consumer.to_owned(), revision };
        // Only the first attachment may bind a startup selection that predates
        // any UI checkpoint, at the untouched-UI revision zero. Later
        // attachments or a UI edited before readiness never relabel it.
        if self.current_ui.is_none() && revision == 0 {
            if let Some(pending) = self.pending.as_mut().filter(|p|p.consumer.is_none() && p.intent.checkpoint.is_none()) {
                pending.intent.checkpoint = Some(ui.clone());
            }
        }
        self.current_ui = Some(ui);
        Ok(())
    }
    pub fn select(&mut self, id: &str, homes: &HomeRouter) -> Result<(), String> {
        let target = self.entries.iter().find(|entry|entry.id == id)
            .ok_or("This waiting menu item is unknown or retired; choose from the current menu.")?.target.clone();
        target.validate(homes)?;
        if self.pending.is_some() { return Err("Waiting navigation is already pending; choose again after it finishes.".into()); }
        let intent = Intent { intent_id:self.id(), target, checkpoint:self.current_ui.clone() };
        self.pending = Some(Delivery { intent, consumer:None });
        Ok(())
    }
    pub fn claim(&mut self, consumer: &str, homes: &HomeRouter) -> Value {
        let Some(pending) = self.pending.as_mut() else { return Value::Null };
        if let Some(owner) = &pending.consumer {
            if owner == consumer { return Value::Null; }
            self.pending = None;
            return serde_json::json!({"refused":"Waiting navigation was interrupted by a window reload; choose the original item again from the current menu."});
        }
        if let Err(reason) = pending.intent.target.validate(homes) {
            self.pending = None;
            return serde_json::json!({"refused":reason});
        }
        if pending.intent.checkpoint != self.current_ui || !self.current_ui.as_ref().is_some_and(|ui|ui.consumer == consumer) {
            self.pending = None;
            return serde_json::json!({"refused":"Waiting-request navigation refused: its native selection has an older or uncertain UI checkpoint; choose again after the current UI checkpoint is acknowledged."});
        }
        pending.consumer = Some(consumer.to_owned());
        serde_json::to_value(&pending.intent).expect("typed waiting intent")
    }
    pub fn abandon(&mut self, consumer: &str) {
        if self.pending.as_ref().is_some_and(|p|p.consumer.as_deref() == Some(consumer)) { self.pending = None; }
    }
    pub fn finish(&mut self, consumer: &str, intent: &str) -> Result<(), String> {
        if !self.pending.as_ref().is_some_and(|p|p.consumer.as_deref() == Some(consumer) && p.intent.intent_id == intent) {
            return Err("Waiting navigation claim is no longer current; no retry.".into());
        }
        self.pending = None;
        Ok(())
    }
}

/// Tauri/muda interprets ampersands as mnemonics. Escape only presentation bytes.
pub(crate) fn literal_label(label: &str) -> String { label.replace('&', "&&") }

#[cfg(target_os = "macos")]
pub(crate) fn append_menu(app: &tauri::AppHandle, menu: &tauri::menu::Menu<tauri::Wry>) -> tauri::Result<()> {
    menu.append(&tauri::menu::Submenu::with_id(app, MENU_ID, "Waiting requests (0)", true)?)
}
#[derive(Default)]
pub(crate) struct MenuObserver { last: Option<Vec<MenuEntry>> }
impl MenuObserver {
    pub(crate) fn publish<E>(&mut self, entries: Vec<MenuEntry>, apply: impl FnOnce(&[MenuEntry]) -> Result<(), E>) -> Result<(), E> {
        if self.last.as_ref() == Some(&entries) { return Ok(()) }
        // Invalidate before any fallible native mutation, even when a later
        // desired projection returns to the previous successful entries.
        self.last = None;
        apply(&entries)?;
        self.last = Some(entries);
        Ok(())
    }
    #[cfg(target_os = "macos")]
    pub fn update(&mut self, app: &tauri::AppHandle, registry: &std::sync::Mutex<Registry>, overview: &Value) -> tauri::Result<()> {
        // No home, Host or registry guard may cross a synchronous native API.
        let entries = registry.lock().unwrap().project(overview);
        self.publish(entries, |entries| {
            let menu = app.menu().ok_or_else(||tauri::Error::AssetNotFound("App menu unavailable".into()))?;
            let Some(tauri::menu::MenuItemKind::Submenu(submenu)) = menu.get(&MENU_ID.to_owned()) else {
                return Err(tauri::Error::AssetNotFound("Waiting requests menu unavailable".into()));
            };
            // A failed partial update is retried; retired entries always refuse dispatch.
            for item in submenu.items()? { submenu.remove(&item)?; }
            for entry in entries {
                submenu.append(&tauri::menu::MenuItem::with_id(app, &entry.id, literal_label(&entry.label), true, None::<&str>)?)?;
            }
            submenu.set_text(format!("Waiting requests ({})", entries.iter().map(|e|e.target.count).sum::<u64>()))?;
            Ok(())
        })
    }
    #[cfg(not(target_os = "macos"))]
    pub fn update(&mut self, _app: &tauri::AppHandle, _registry: &std::sync::Mutex<Registry>, _overview: &Value) -> tauri::Result<()> { Ok(()) }
}
