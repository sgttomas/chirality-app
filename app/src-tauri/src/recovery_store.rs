//! The App ledger's SQLite store (DEL-01-02 §7; owner direction 2026-10-12,
//! PRD R-STORE). App-private operational state, not a record.
//!
//! - Entries are only ever inserted: triggers refuse every UPDATE and DELETE of
//!   an entry or an import record, so a rewrite fails in the database itself,
//!   not only in this code.
//! - Each entry is stored with its exact JSON (validated against the ledger
//!   schema by the caller before insert, and again on every read) and the
//!   indexed columns readers use: kind, session, home, thread, generation.
//! - Entries that must stand together are inserted in one transaction.
//! - The host holds only the *current* entries ([`currency`]): every entry of
//!   the few kinds that only accumulate slowly (session markers, quits, Codex
//!   stops, stop requests, RQ-06 endings), the latest `conversation_index`
//!   entry per conversation, generation, appending session and tag list, and
//!   the latest `register_entry_summary` per request and state while the
//!   request is still listed. They are read by one indexed query
//!   ([`Store::current_entries`]), never by loading the whole ledger.
//! - Durability: rollback journal (`journal_mode=DELETE`), `synchronous=EXTRA`,
//!   `fullfsync` and `checkpoint_fullfsync`. SQLite writes and syncs the
//!   journal and the database file with `F_FULLFSYNC` (fullfsync). A commit
//!   becomes durable when the journal is unlinked, and SQLite's own directory
//!   sync after that unlink (EXTRA) is a plain `fsync`, not `F_FULLFSYNC`, and
//!   is skipped silently when the folder cannot be opened (3.46.0
//!   `unixDelete`, `full_fsync(fd,0,0)`). So after every commit this store
//!   flushes the database's folder itself (`File::sync_all`, which is
//!   `F_FULLFSYNC` on macOS), and a commit is reported confirmed only when
//!   that flush succeeds; if it fails the append is reported not confirmed.
//! - The JSON Lines ledger of earlier builds is imported once, in order, every
//!   complete and valid line. Only a final line that is not newline-closed (a
//!   torn write) is a recorded limit, never an entry. A complete invalid line
//!   anywhere, a file changed since its import, a file that appeared after the
//!   database was created and a file not imported before the App recorded
//!   entries fail the open and import nothing (DEL-01-02 §7: no reading is
//!   derived from part of a history, or from one out of order). The file is never written. The import is recorded (source
//!   path, byte length, content identity, the file's device, inode, length and
//!   modification time) in the same transaction as its entries, so it happens
//!   at most once.
use rusqlite::{params, Connection, OpenFlags, OptionalExtension, TransactionBehavior};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

/// The exact-byte content method used for the imported file's identity.
const EXACT_BYTES: &str = "chirality.app.exact-bytes.sha256/v1";
const SCHEMA_VERSION: &str = "1";
/// How the `currency` and `subject` columns are derived from an entry
/// ([`currency`], [`subject`]), recorded in `ledger_meta` as `index_format`.
/// Migration rule: a later derivation gets a new number and never rewrites
/// rows. A database whose recorded format differs (or is absent) is read by a
/// full scan that derives the keys from each entry's JSON, ignoring the
/// stored columns; entries this build inserts carry its own derivation.
pub(crate) const INDEX_FORMAT: &str = "1";
/// One explicit historical read, independent of the live/current projection.
pub(crate) const TERMINAL_REQUEST_ROWS: usize = 64;
const TERMINAL_REQUEST_BYTES: usize = 256 * 1024;
const SCHEMA: &str = "
CREATE TABLE IF NOT EXISTS ledger_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS ledger_entry (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    session TEXT,
    home TEXT,
    thread TEXT,
    generation TEXT,
    origin TEXT NOT NULL CHECK (origin IN ('app', 'legacy-import')),
    batch INTEGER NOT NULL,
    currency TEXT,
    subject TEXT,
    entry TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ledger_entry_kind ON ledger_entry (kind, seq);
CREATE INDEX IF NOT EXISTS ledger_entry_session ON ledger_entry (session, seq);
CREATE INDEX IF NOT EXISTS ledger_entry_thread ON ledger_entry (home, thread, seq);
CREATE INDEX IF NOT EXISTS ledger_entry_generation ON ledger_entry (generation, seq);
CREATE INDEX IF NOT EXISTS ledger_entry_batch ON ledger_entry (batch);
CREATE INDEX IF NOT EXISTS ledger_entry_currency ON ledger_entry (currency, seq);
CREATE INDEX IF NOT EXISTS ledger_entry_subject ON ledger_entry (subject, seq);
CREATE TABLE IF NOT EXISTS legacy_import (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_path TEXT NOT NULL,
    byte_length INTEGER NOT NULL,
    content_method TEXT NOT NULL,
    content_value TEXT NOT NULL,
    imported_lines INTEGER NOT NULL,
    first_seq INTEGER,
    last_seq INTEGER,
    tail_limit TEXT,
    imported_at TEXT NOT NULL,
    file_identity TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS ledger_entry_never_rewritten BEFORE UPDATE ON ledger_entry
    BEGIN SELECT RAISE(ABORT, 'ledger entries are never rewritten'); END;
CREATE TRIGGER IF NOT EXISTS ledger_entry_never_deleted BEFORE DELETE ON ledger_entry
    BEGIN SELECT RAISE(ABORT, 'ledger entries are never deleted'); END;
CREATE TRIGGER IF NOT EXISTS legacy_import_never_rewritten BEFORE UPDATE ON legacy_import
    BEGIN SELECT RAISE(ABORT, 'import records are never rewritten'); END;
CREATE TRIGGER IF NOT EXISTS legacy_import_never_deleted BEFORE DELETE ON legacy_import
    BEGIN SELECT RAISE(ABORT, 'import records are never deleted'); END;
CREATE TRIGGER IF NOT EXISTS ledger_meta_never_rewritten BEFORE UPDATE ON ledger_meta
    BEGIN SELECT RAISE(ABORT, 'ledger metadata is never rewritten'); END;
CREATE TRIGGER IF NOT EXISTS ledger_meta_never_deleted BEFORE DELETE ON ledger_meta
    BEGIN SELECT RAISE(ABORT, 'ledger metadata is never deleted'); END;
";

#[cfg(test)]
thread_local! {
    /// Test hook: the next batch fails after inserting this many entries.
    pub(crate) static FAIL_BATCH_AFTER: std::cell::Cell<Option<usize>> = const { std::cell::Cell::new(None) };
    /// Test hook: the next batch commits, then its folder flush fails, so the
    /// append is reported not confirmed although it landed.
    pub(crate) static FAIL_FLUSH_AFTER_COMMIT: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
    pub(crate) static AFTER_TERMINAL_READ: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) };
}

/// The key under which a later entry supersedes an earlier one among the
/// entries the host holds; `None`: every entry of that kind is held. For a
/// `conversation_index` the key keeps apart each tag list, so the union of a
/// conversation's tags over its held entries is the union over all of them,
/// and each generation and appending session, so the custody view's ordering
/// (source session, spawn counter, position) finds the same latest entry.
pub(crate) fn currency(entry: &Value) -> Option<String> {
    match entry["kind"].as_str()? {
        "conversation_index" => Some(
            json!(["conversation_index", entry["home"], entry["threadId"], entry["lastLoadedGeneration"], entry["session"], entry["tags"]]).to_string(),
        ),
        "register_entry_summary" if entry["transition"] != "RQ-06" => {
            Some(json!(["register_entry_summary", entry["generation"], entry["requestIdentity"], entry["state"]]).to_string())
        }
        _ => None,
    }
}
/// A request's identity in the ledger (generation and request identity).
pub(crate) fn subject(entry: &Value) -> Option<String> {
    (entry["kind"] == "register_entry_summary").then(|| json!([entry["generation"], entry["requestIdentity"]]).to_string())
}

/// The database beside the configured ledger location.
pub(crate) fn database_path(ledger: &Path) -> PathBuf {
    ledger.with_extension("sqlite")
}

/// The database file and its side files: a regular, single-link leaf (or
/// absent), never a symbolic link (the equivalent of today's O_NOFOLLOW and
/// hard-link checks for a file SQLite opens itself).
pub(crate) fn preflight(database: &Path) -> Result<(), String> {
    use std::os::unix::fs::MetadataExt;
    for path in side_files(database) {
        match std::fs::symlink_metadata(&path) {
            Ok(meta) if !meta.is_file() || meta.nlink() != 1 => {
                return Err(format!("REC ledger database leaf {} is not a regular single-link file", path.display()))
            }
            Ok(_) => {}
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(e) => return Err(format!("REC ledger database leaf metadata unavailable: {e}")),
        }
    }
    Ok(())
}
fn side_files(database: &Path) -> [PathBuf; 4] {
    let name = |suffix: &str| {
        let mut s = database.as_os_str().to_owned();
        s.push(suffix);
        PathBuf::from(s)
    };
    [database.to_path_buf(), name("-journal"), name("-wal"), name("-shm")]
}
fn identity(path: &Path) -> Result<(u64, u64), String> {
    use std::os::unix::fs::MetadataExt;
    let meta = std::fs::symlink_metadata(path).map_err(|e| format!("REC ledger database metadata unavailable: {e}"))?;
    Ok((meta.dev(), meta.ino()))
}
fn db_error(context: &str) -> impl Fn(rusqlite::Error) -> String + '_ {
    move |e| format!("{context}: {e}")
}

pub(crate) struct Store {
    path: PathBuf,
    /// The database's folder, resolved; flushed after every commit.
    folder: PathBuf,
    connection: Connection,
    /// The device and inode of the file SQLite has open; the path must name
    /// it at open and before every write.
    opened: (u64, u64),
    /// Whether the stored index columns follow [`INDEX_FORMAT`].
    index_current: bool,
}

impl Store {
    /// Opens (creating when absent) the database. `create` is false when the
    /// caller expects an existing database: a missing one is then an error.
    /// `legacy_present`: whether a JSON Lines ledger exists beside it now; a
    /// database created without one never imports a file that appears later.
    pub(crate) fn open(path: &Path, create: bool, legacy_present: bool) -> Result<Self, String> {
        preflight(path)?;
        let existed = std::fs::symlink_metadata(path).is_ok();
        if !existed && !create {
            return Err("App history unavailable: the ledger database is missing".into());
        }
        // No symbolic link is followed, and the descriptor SQLite opened must be
        // the file the path names.
        let mut flags = OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_NO_MUTEX | OpenFlags::SQLITE_OPEN_NOFOLLOW;
        if create {
            flags |= OpenFlags::SQLITE_OPEN_CREATE;
        }
        // NOFOLLOW refuses a symbolic link anywhere in the name SQLite opens, so it
        // opens the name under the folder's resolved path: the leaf is never followed.
        let folder = path.parent().ok_or("ledger database has no parent directory")?.canonicalize().map_err(|e| format!("App history unavailable: ledger folder not resolvable: {e}"))?;
        let resolved = folder.join(path.file_name().ok_or("ledger database has no file name")?);
        let connection = Connection::open_with_flags(&resolved, flags).map_err(db_error("App history unavailable: ledger database not openable"))?;
        let opened = descriptor_identity(&connection)?;
        if identity(path)? != opened {
            return Err("REC ledger database leaf changed while it was opened".into());
        }
        connection.busy_timeout(busy_timeout()).map_err(db_error("ledger database busy timeout not set"))?;
        // Rollback journal; EXTRA also syncs the directory after the journal is
        // unlinked, the moment a commit becomes durable (module text).
        let mode: String = connection.query_row("PRAGMA journal_mode=DELETE", [], |r| r.get(0)).map_err(db_error("ledger journal mode not set"))?;
        if !mode.eq_ignore_ascii_case("delete") {
            return Err(format!("ledger journal mode not established ({mode})"));
        }
        connection.execute_batch("PRAGMA synchronous=EXTRA; PRAGMA fullfsync=ON; PRAGMA checkpoint_fullfsync=ON;").map_err(db_error("ledger durability not set"))?;
        let durability = durability(&connection).map_err(db_error("ledger durability not readable"))?;
        if (durability.0.as_str(), durability.1, durability.2, durability.3) != DURABILITY {
            return Err(format!("ledger durability not established ({durability:?})"));
        }
        let mut store = Self { path: path.to_path_buf(), folder: folder.clone(), opened, connection, index_current: false };
        store.ensure_schema(legacy_present)?;
        store.index_current = store.meta("index_format")?.as_deref() == Some(INDEX_FORMAT);
        if !existed {
            let parent = path.parent().ok_or("ledger database has no parent directory")?;
            crate::storage::sync_dir(parent).map_err(|e| format!("ledger database creation not durable: {e}"))?;
        }
        preflight(path)?;
        if identity(path)? != store.opened {
            return Err("REC ledger database leaf changed while it was opened".into());
        }
        Ok(store)
    }
    fn ensure_schema(&mut self, legacy_present: bool) -> Result<(), String> {
        // An established database is only read: no write lock is taken to open it.
        let established: Option<String> = self.connection
            .query_row("SELECT value FROM ledger_meta WHERE key = 'schema'", [], |r| r.get(0))
            .optional()
            .or_else(|e| if e.to_string().contains("no such table") { Ok(None) } else { Err(e) })
            .map_err(db_error("ledger schema not readable"))?;
        match established.as_deref() {
            Some(SCHEMA_VERSION) => return Ok(()),
            Some(other) => return Err(format!("App history unavailable: ledger database schema {other} is not this App's ({SCHEMA_VERSION})")),
            None => {}
        }
        let tx = self.connection.transaction_with_behavior(TransactionBehavior::Immediate).map_err(db_error("ledger schema not established"))?;
        tx.execute_batch(SCHEMA).map_err(db_error("ledger schema not established"))?;
        let version: Option<String> = tx.query_row("SELECT value FROM ledger_meta WHERE key = 'schema'", [], |r| r.get(0)).optional().map_err(db_error("ledger schema not readable"))?;
        match version.as_deref() {
            None => {
                tx.execute("INSERT INTO ledger_meta (key, value) VALUES ('schema', ?1)", [SCHEMA_VERSION]).map_err(db_error("ledger schema not recorded"))?;
                tx.execute("INSERT INTO ledger_meta (key, value) VALUES ('legacy_at_creation', ?1)", [if legacy_present { "present" } else { "absent" }]).map_err(db_error("ledger schema not recorded"))?;
                tx.execute("INSERT INTO ledger_meta (key, value) VALUES ('index_format', ?1)", [INDEX_FORMAT]).map_err(db_error("ledger schema not recorded"))?;
            }
            Some(SCHEMA_VERSION) => {}
            Some(other) => return Err(format!("App history unavailable: ledger database schema {other} is not this App's ({SCHEMA_VERSION})")),
        }
        tx.commit().map_err(db_error("ledger schema not committed"))?;
        self.flush("ledger schema not committed")
    }
    /// After a commit: the unlink of its journal, the moment it became durable,
    /// is flushed to the device with the folder (module text).
    fn flush(&self, context: &str) -> Result<(), String> {
        crate::storage::sync_dir(&self.folder).map_err(|e| format!("{context}: the commit returned but its folder was not flushed ({e})"))
    }
    fn meta(&self, key: &str) -> Result<Option<String>, String> {
        self.connection.query_row("SELECT value FROM ledger_meta WHERE key = ?1", [key], |r| r.get(0)).optional().map_err(db_error("ledger metadata not readable"))
    }
    /// The effective durability settings (journal mode, synchronous level,
    /// fullfsync, checkpoint_fullfsync), for tests.
    #[cfg(test)]
    pub(crate) fn durability(&self) -> (String, i64, i64, i64) {
        durability(&self.connection).unwrap()
    }
    /// The write guard: the path still names the opened regular single-link file.
    pub(crate) fn guard(&self) -> Result<(), String> {
        preflight(&self.path)?;
        if identity(&self.path)? != self.opened {
            return Err("REC ledger database leaf is redirected or replaced".into());
        }
        Ok(())
    }
    /// Every entry in order, each validated again with `validate`. Reads the
    /// whole ledger: for inspection and tests, never on the host's paths.
    pub(crate) fn entries(&self, validate: &dyn Fn(&Value) -> Result<(), String>) -> Result<Vec<Value>, String> {
        let mut statement = self.connection.prepare("SELECT entry FROM ledger_entry ORDER BY seq").map_err(db_error("App history unavailable"))?;
        let rows = statement.query_map([], |r| r.get::<_, String>(0)).map_err(db_error("App history unavailable"))?;
        let mut entries = Vec::new();
        for row in rows {
            let text = row.map_err(db_error("App history unavailable"))?;
            let entry: Value = serde_json::from_str(&text).map_err(|e| format!("App history unavailable: stored entry is not JSON: {e}"))?;
            validate(&entry).map_err(|e| format!("App history unavailable: {e}"))?;
            entries.push(entry);
        }
        Ok(entries)
    }
    /// How many entries the database holds.
    pub(crate) fn count(&self) -> Result<u64, String> {
        self.connection.query_row("SELECT COUNT(*) FROM ledger_entry", [], |r| r.get::<_, i64>(0)).map(|n| n as u64).map_err(db_error("App history unavailable"))
    }
    /// Latest closed summary per original (full generation, typed serialized
    /// request ID), newest first at a fixed ledger cut. Only this bounded page
    /// enters Rust memory. Legacy index formats derive keys in SQL from JSON,
    /// never trust old columns or load the whole ledger to derive a page.
    pub(crate) fn terminal_request_page(
        &self,
        cursor: Option<&Value>,
        validate: &dyn Fn(&Value) -> Result<(), String>,
    ) -> Result<Value, String> {
        crate::storage::check_path(&self.path)?;
        self.guard()?;
        let mut source = self.path.as_os_str().as_encoded_bytes().to_vec();
        source.extend_from_slice(&self.opened.0.to_be_bytes());
        source.extend_from_slice(&self.opened.1.to_be_bytes());
        let source = crate::util::sha256_hex(&source);
        let tx = self.connection.unchecked_transaction().map_err(db_error("Request history unavailable"))?;
        let maximum: i64 = tx.query_row("SELECT COALESCE(MAX(seq), 0) FROM ledger_entry", [], |r| r.get(0)).map_err(db_error("Request history unavailable"))?;
        let decimal = |value: &Value| -> Result<i64, String> {
            let text = value.as_str().ok_or("Invalid request-history cursor")?;
            let number = text.parse::<i64>().map_err(|_| "Invalid request-history cursor")?;
            if number < 0 || number.to_string() != text { return Err("Invalid request-history cursor".into()); }
            Ok(number)
        };
        let (through, before) = match cursor {
            None => (maximum, None),
            Some(value) => {
                if value.as_object().is_none_or(|o| o.len() != 3)
                    || value["source"] != source {
                    return Err("Foreign or invalid request-history cursor".into());
                }
                let through = decimal(&value["throughSequence"])?;
                let before = decimal(&value["beforeSequence"])?;
                if through > maximum || before == 0 || before > through.saturating_add(1) {
                    return Err("Request-history cursor is outside its ledger cut".into());
                }
                (through, Some(before))
            }
        };
        let (kind, subject) = if self.index_current {
            ("kind", "subject")
        } else {
            ("json_extract(entry, '$.kind')", "json_array(json_extract(entry, '$.generation'), json_extract(entry, '$.requestIdentity'))")
        };
        let sql = format!(
            "SELECT seq, length(CAST(entry AS BLOB)), kind, currency, subject, entry
             FROM ledger_entry WHERE seq <= ?1 AND (?2 IS NULL OR seq < ?2)
               AND {kind} = 'register_entry_summary' AND json_extract(entry, '$.state') = 'closed'
               AND seq IN (SELECT MAX(seq) FROM ledger_entry
                   WHERE seq <= ?1 AND {kind} = 'register_entry_summary'
                     AND json_extract(entry, '$.state') = 'closed' GROUP BY {subject})
             ORDER BY seq DESC LIMIT ?3"
        );
        let mut entries = Vec::new();
        let mut bytes = 0usize;
        let mut last_sequence = None;
        let mut more = false;
        {
            let mut statement = tx.prepare(&sql).map_err(db_error("Request history unavailable"))?;
            let mut rows = statement.query(params![through, before, (TERMINAL_REQUEST_ROWS + 1) as i64]).map_err(db_error("Request history unavailable"))?;
            while let Some(row) = rows.next().map_err(db_error("Request history unavailable"))? {
                if entries.len() == TERMINAL_REQUEST_ROWS { more = true; break; }
                let size: i64 = row.get(1).map_err(db_error("Request history unavailable"))?;
                if size < 0 || size as u64 > TERMINAL_REQUEST_BYTES as u64 {
                    return Err("Request history unavailable: one summary exceeds the bounded read budget".into());
                }
                if bytes + size as usize > TERMINAL_REQUEST_BYTES { more = true; break; }
                let sequence: i64 = row.get(0).map_err(db_error("Request history unavailable"))?;
                if sequence <= 0 { return Err("Request history unavailable: invalid source sequence".into()); }
                let text: String = row.get(5).map_err(db_error("Request history unavailable"))?;
                let entry: Value = serde_json::from_str(&text).map_err(|_| "Request history unavailable: stored summary is not JSON")?;
                validate(&entry).map_err(|e| format!("Request history unavailable: {e}"))?;
                if entry["kind"] != "register_entry_summary" || entry["state"] != "closed" {
                    return Err("Request history unavailable: selected entry is not a closed summary".into());
                }
                if self.index_current {
                    let kind: String = row.get(2).map_err(db_error("Request history unavailable"))?;
                    let held: Option<String> = row.get(3).map_err(db_error("Request history unavailable"))?;
                    let request: Option<String> = row.get(4).map_err(db_error("Request history unavailable"))?;
                    if entry["kind"] != kind || currency(&entry) != held || self::subject(&entry) != request {
                        return Err("Request history unavailable: stored index columns do not match the original summary".into());
                    }
                }
                bytes += size as usize;
                last_sequence = Some(sequence);
                entries.push(entry);
            }
        }
        tx.commit().map_err(db_error("Request history unavailable"))?;
        #[cfg(test)]
        if let Some(hook) = AFTER_TERMINAL_READ.with(|slot| slot.borrow_mut().take()) { hook(); }
        crate::storage::check_path(&self.path)?;
        self.guard()?;
        let next = if more {
            Some(json!({"source":source,"throughSequence":through.to_string(),"beforeSequence":last_sequence.ok_or("Request history unavailable: empty bounded page")?.to_string()}))
        } else { None };
        Ok(json!({"entries":entries,"nextCursor":next,"throughSequence":through.to_string(),"hasMore":more,
            "rowLimit":TERMINAL_REQUEST_ROWS,"byteLimit":TERMINAL_REQUEST_BYTES,
            "coverage":"Bounded latest closed summary per original generation and typed request identity at this ledger cut; not a complete request transition history",
            "oldRequestsAnswerable":false}))
    }
    /// The current entries in ledger order (see the module text), by one
    /// indexed query; a request whose latest entry is closed is not held.
    /// Each is validated with `validate`, and its stored columns must be the
    /// ones its JSON gives.
    pub(crate) fn current_entries(&self, validate: &dyn Fn(&Value) -> Result<(), String>) -> Result<Vec<Value>, String> {
        if !self.index_current {
            return self.current_entries_scanned(validate);
        }
        let mut statement = self
            .connection
            .prepare(
                "SELECT kind, currency, subject, entry FROM ledger_entry
                 WHERE currency IS NULL
                    OR (seq IN (SELECT MAX(seq) FROM ledger_entry WHERE currency IS NOT NULL GROUP BY currency)
                        AND (subject IS NULL OR subject NOT IN (
                            SELECT latest.subject FROM ledger_entry AS latest
                            WHERE latest.seq IN (SELECT MAX(seq) FROM ledger_entry WHERE subject IS NOT NULL GROUP BY subject)
                              AND json_extract(latest.entry, '$.state') = 'closed')))
                 ORDER BY seq",
            )
            .map_err(db_error("App history unavailable"))?;
        let rows = statement
            .query_map([], |r| Ok((r.get::<_, String>(0)?, r.get::<_, Option<String>>(1)?, r.get::<_, Option<String>>(2)?, r.get::<_, String>(3)?)))
            .map_err(db_error("App history unavailable"))?;
        let mut entries = Vec::new();
        for row in rows {
            let (kind, held, request, text) = row.map_err(db_error("App history unavailable"))?;
            let entry: Value = serde_json::from_str(&text).map_err(|e| format!("App history unavailable: stored entry is not JSON: {e}"))?;
            validate(&entry).map_err(|e| format!("App history unavailable: {e}"))?;
            if entry["kind"] != kind.as_str() || currency(&entry) != held || subject(&entry) != request {
                return Err("App history unavailable: a stored entry's index columns do not match its JSON".into());
            }
            entries.push(entry);
        }
        Ok(entries)
    }
    /// [`Self::current_entries`] for a database whose index columns follow
    /// another format: one pass over every entry, keys derived from its JSON
    /// (the stored columns are not used). Holds only the current entries and
    /// each request's latest state.
    fn current_entries_scanned(&self, validate: &dyn Fn(&Value) -> Result<(), String>) -> Result<Vec<Value>, String> {
        use std::collections::{BTreeMap, HashMap};
        let mut statement = self.connection.prepare("SELECT seq, entry FROM ledger_entry ORDER BY seq").map_err(db_error("App history unavailable"))?;
        let rows = statement.query_map([], |r| Ok((r.get::<_, i64>(0)?, r.get::<_, String>(1)?))).map_err(db_error("App history unavailable"))?;
        let mut held: BTreeMap<i64, (Value, Option<String>, Option<String>)> = BTreeMap::new();
        let mut latest: HashMap<String, i64> = HashMap::new();
        let mut settled: HashMap<String, bool> = HashMap::new();
        for row in rows {
            let (seq, text) = row.map_err(db_error("App history unavailable"))?;
            let entry: Value = serde_json::from_str(&text).map_err(|e| format!("App history unavailable: stored entry is not JSON: {e}"))?;
            let (key, request) = (currency(&entry), subject(&entry));
            if let Some(request) = &request {
                settled.insert(request.clone(), entry["state"] == "closed");
            }
            match &key {
                Some(key) => {
                    if let Some(earlier) = latest.insert(key.clone(), seq) {
                        held.remove(&earlier);
                    }
                    held.insert(seq, (entry, Some(key.clone()), request));
                }
                None => {
                    held.insert(seq, (entry, None, request));
                }
            }
        }
        let mut entries = Vec::new();
        for (_, (entry, key, request)) in held {
            if key.is_some() && request.as_ref().is_some_and(|r| settled.get(r) == Some(&true)) {
                continue;
            }
            validate(&entry).map_err(|e| format!("App history unavailable: {e}"))?;
            entries.push(entry);
        }
        Ok(entries)
    }
    /// One transaction: every entry is recorded, or none is.
    pub(crate) fn insert_batch(&mut self, entries: &[Value]) -> Result<(), String> {
        self.guard()?;
        let tx = self.connection.transaction_with_behavior(TransactionBehavior::Immediate).map_err(db_error("recovery ledger append not confirmed"))?;
        let batch = next_batch(&tx).map_err(db_error("recovery ledger append not confirmed"))?;
        for (n, entry) in entries.iter().enumerate() {
            #[cfg(test)]
            if FAIL_BATCH_AFTER.with(|f| f.get()) == Some(n) {
                FAIL_BATCH_AFTER.with(|f| f.set(None));
                return Err("recovery ledger append not confirmed: injected failure inside the batch; nothing recorded".into());
            }
            let _ = n;
            let text = serde_json::to_string(entry).map_err(|e| format!("recovery ledger append not confirmed: {e}"))?;
            insert(&tx, entry, &text, "app", batch).map_err(db_error("recovery ledger append not confirmed"))?;
        }
        tx.commit().map_err(db_error("recovery ledger append not confirmed"))?;
        #[cfg(test)]
        if FAIL_FLUSH_AFTER_COMMIT.with(|f| f.replace(false)) {
            return Err("recovery ledger append not confirmed: the commit returned but its folder was not flushed (injected)".into());
        }
        self.flush("recovery ledger append not confirmed")
    }
    /// The JSON Lines ledger at `legacy`, open as `file` (with the caller's
    /// descriptor guards), imported once (see the module text). It is read in
    /// bounded pieces: once for its length and content identity, and, only
    /// when it is imported now, once more line by line; a change between the
    /// two reads is refused. Returns the import reading shown with the ledger.
    pub(crate) fn import_legacy(
        &mut self,
        legacy: &Path,
        file: &mut std::fs::File,
        validate: &dyn Fn(&Value) -> Result<(), String>,
    ) -> Result<Value, String> {
        let source = legacy.to_string_lossy().into_owned();
        // The file as last imported, unchanged (same file, length and
        // modification time): its content identity is not read again.
        let file_identity = file_identity(file)?;
        let unchanged: Option<(String, i64, String, i64, Option<String>)> = self
            .connection
            .query_row(
                "SELECT source_path, byte_length, content_value, imported_lines, tail_limit FROM legacy_import WHERE source_path = ?1 AND file_identity = ?2 ORDER BY id LIMIT 1",
                params![source, file_identity],
                |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?, r.get(3)?, r.get(4)?)),
            )
            .optional()
            .map_err(db_error("legacy ledger import record not readable"))?;
        if let Some((path, imported_length, imported_content, lines, limit)) = unchanged {
            return Ok(json!({"state":"imported earlier","sourcePath":path,"byteLength":imported_length,
                "content":{"method":EXACT_BYTES,"value":imported_content},"importedLines":lines,"limit":limit}));
        }
        let (length, content) = read_identity(file)?;
        let length = length as i64;
        let tx = self.connection.transaction_with_behavior(TransactionBehavior::Immediate).map_err(db_error("legacy ledger import not recorded"))?;
        let earlier: Option<(String, i64, String, i64, Option<String>)> = tx
            .query_row(
                "SELECT source_path, byte_length, content_value, imported_lines, tail_limit FROM legacy_import WHERE source_path = ?1 OR content_value = ?2 ORDER BY id LIMIT 1",
                params![source, content],
                |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?, r.get(3)?, r.get(4)?)),
            )
            .optional()
            .map_err(db_error("legacy ledger import record not readable"))?;
        if let Some((path, imported_length, imported_content, lines, limit)) = earlier {
            drop(tx);
            let mut reading = json!({"state":"imported earlier","sourcePath":path,"byteLength":imported_length,
                "content":{"method":EXACT_BYTES,"value":imported_content},"importedLines":lines,"limit":limit});
            if imported_content != content || imported_length != length {
                // Fail closed (§7): entries written after the import are not in
                // the database, so no startup reading may be derived from it.
                return Err(format!("App history unavailable: the JSON Lines ledger changed after its import (it now has {length} bytes with content {content}; {imported_length} bytes were imported). Entries written to it since are not in the ledger database, so its history is incomplete and nothing is derived from it; no App recovery is recorded until this is resolved. The file is not written. Moving it aside lets the App record again and gives up the entries an earlier build appended to it: they will never be imported."));
            }
            return Ok(reading);
        }
        let at_creation: Option<String> = tx.query_row("SELECT value FROM ledger_meta WHERE key = 'legacy_at_creation'", [], |r| r.get(0)).optional().map_err(db_error("legacy ledger import record not readable"))?;
        if at_creation.as_deref() == Some("absent") {
            drop(tx);
            return Err(format!("App history unavailable: a JSON Lines ledger ({length} bytes) appeared after the ledger database was created without one. Its entries would not follow the database's order and are not imported, so the history is incomplete and nothing is derived from it; no App recovery is recorded until this is resolved. The file is not written. Moving it aside lets the App record again, but its entries will then never be imported."));
        }
        // Entries the App recorded without this file come first in the
        // database; its history cannot be placed before them, at any later start.
        let recorded: bool = tx.query_row("SELECT EXISTS(SELECT 1 FROM ledger_entry WHERE origin = 'app')", [], |r| r.get(0)).map_err(db_error("legacy ledger import record not readable"))?;
        if recorded {
            drop(tx);
            return Err(format!("App history unavailable: the ledger database recorded entries before this JSON Lines ledger ({length} bytes) was imported, so its history would follow them out of order; it is not imported, and nothing is derived from it. No App recovery is recorded until this is resolved. The file is not written. Moving it aside lets the App record again, but its entries will then never be imported."));
        }
        // Every complete, valid line in order; the first that is not ends the
        // import. Each is inserted as it is read; none is held after.
        use sha2::Digest;
        use std::io::{BufRead, Seek};
        file.seek(std::io::SeekFrom::Start(0)).map_err(|e| format!("App history unavailable: {e}"))?;
        let mut reader = std::io::BufReader::with_capacity(1 << 20, file);
        let mut hasher = sha2::Sha256::new();
        let batch = next_batch(&tx).map_err(db_error("legacy ledger import not recorded"))?;
        let (mut first, mut last, mut imported) = (None, None, 0i64);
        let mut offset = 0usize;
        let mut limit: Option<String> = None;
        let mut line = Vec::new();
        // After the first line that is not imported: its offset, reason and
        // length, and the newline-closed lines from it on.
        let mut refused: Option<(usize, String, usize, usize)> = None;
        loop {
            line.clear();
            let read = reader.read_until(b'\n', &mut line).map_err(|e| format!("App history unavailable: {e}"))?;
            if read == 0 {
                break;
            }
            hasher.update(&line);
            let closed = line.last() == Some(&b'\n');
            if let Some((_, _, _, rest)) = refused.as_mut() {
                *rest += closed as usize;
            } else if !closed {
                limit = Some(format!("final line at byte {offset} is not newline-closed ({} bytes); not imported", line.len()));
            } else {
                let parsed: Result<Value, String> = serde_json::from_slice(&line).map_err(|e| e.to_string()).and_then(|v| validate(&v).map(|()| v));
                match parsed {
                    // The line's exact bytes are kept, without its line feed.
                    Ok(entry) => {
                        let text = String::from_utf8_lossy(&line[..line.len() - 1]).into_owned();
                        let seq = insert(&tx, &entry, &text, "legacy-import", batch).map_err(db_error("legacy ledger import not recorded"))?;
                        first.get_or_insert(seq);
                        last = Some(seq);
                        imported += 1;
                    }
                    Err(reason) => refused = Some((offset, reason, line.len(), 1)),
                }
            }
            offset += line.len();
        }
        let digest: String = hasher.finalize().iter().map(|b| format!("{b:02x}")).collect();
        if offset as i64 != length || digest != content {
            return Err("App history unavailable: the JSON Lines ledger changed while it was being imported; nothing imported".into());
        }
        if let Some((at, reason, size, rest)) = refused {
            // A complete line that is not an entry is no torn write (RS R-2):
            // wherever it is, nothing is imported (§7). Only an unclosed final
            // line is a crash's trace and a limit.
            let after = offset - at - size;
            return Err(format!("App history unavailable: line {} at byte {at} of the JSON Lines ledger is a complete line that is not a valid ledger entry ({reason}){}. Nothing is imported and nothing is derived from it; no App recovery is recorded until this is resolved. The file is not written. Repair the file to import it at the next start. Moving it aside lets the App record again, but its entries will then never be imported.", imported + 1,
                if after > 0 { format!(", and {after} bytes ({} newline-closed lines) follow it", rest - 1) } else { String::new() }));
        }
        let at = crate::util::now_rfc3339();
        tx.execute(
            "INSERT INTO legacy_import (source_path, byte_length, content_method, content_value, imported_lines, first_seq, last_seq, tail_limit, imported_at, file_identity) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
            params![source, length, EXACT_BYTES, content, imported, first, last, limit, at, file_identity],
        )
        .map_err(db_error("legacy ledger import not recorded"))?;
        tx.commit().map_err(db_error("legacy ledger import not committed"))?;
        self.flush("legacy ledger import not committed")?;
        Ok(json!({"state":"imported","sourcePath":source,"byteLength":length,"content":{"method":EXACT_BYTES,"value":content},
            "importedLines":imported,"limit":limit,"importedAt":at}))
    }
    #[cfg(test)]
    pub(crate) fn connection(&self) -> &Connection {
        &self.connection
    }
}

/// The open file's device, inode, length and modification time.
fn file_identity(file: &std::fs::File) -> Result<String, String> {
    use std::os::unix::fs::MetadataExt;
    let meta = file.metadata().map_err(|e| format!("App history unavailable: {e}"))?;
    Ok(json!([meta.dev(), meta.ino(), meta.len(), meta.mtime(), meta.mtime_nsec()]).to_string())
}
/// The durability settings [`Store::open`] establishes.
const DURABILITY: (&str, i64, i64, i64) = ("delete", 3, 1, 1);
fn durability(connection: &Connection) -> rusqlite::Result<(String, i64, i64, i64)> {
    let mode: String = connection.query_row("PRAGMA journal_mode", [], |r| r.get(0))?;
    let read = |pragma: &str| connection.query_row(&format!("PRAGMA {pragma}"), [], |r| r.get::<_, i64>(0));
    Ok((mode.to_ascii_lowercase(), read("synchronous")?, read("fullfsync")?, read("checkpoint_fullfsync")?))
}
/// The device and inode of the file SQLite has open as `main`. The unix VFS's
/// file object begins {methods, vfs, inode info, descriptor} (`struct
/// unixFile` of the bundled SQLite, which must be 3.46.0). The descriptor is
/// read only when the object's VFS pointer is, by pointer equality, the
/// connection's own VFS (`SQLITE_FCNTL_VFS_POINTER`) and that VFS is a unix
/// one; otherwise the open is refused. The descriptor is examined with `fstat`.
fn descriptor_identity(connection: &Connection) -> Result<(u64, u64), String> {
    use rusqlite::ffi;
    use std::os::raw::{c_char, c_int, c_void};
    #[repr(C)]
    struct UnixFileHead {
        methods: *const c_void,
        vfs: *const ffi::sqlite3_vfs,
        inode: *const c_void,
        descriptor: c_int,
    }
    let unavailable = || "REC ledger database descriptor unavailable; not opened".to_string();
    // SAFETY: SQLITE_FCNTL_FILE_POINTER and SQLITE_FCNTL_VFS_POINTER write the
    // main database's sqlite3_file and the connection's sqlite3_vfs, both owned
    // by the open connection borrowed here. The file object is read as a
    // unixFile only for the pinned SQLite version and only when its VFS field
    // equals the connection's VFS pointer, compared without dereferencing it.
    unsafe {
        if ffi::sqlite3_libversion_number() != 3_046_000 {
            return Err(unavailable());
        }
        let main = b"main\0".as_ptr() as *const c_char;
        let mut file: *mut ffi::sqlite3_file = std::ptr::null_mut();
        let rc = ffi::sqlite3_file_control(connection.handle(), main, ffi::SQLITE_FCNTL_FILE_POINTER, &mut file as *mut _ as *mut c_void);
        if rc != ffi::SQLITE_OK || file.is_null() || (*file).pMethods.is_null() {
            return Err(unavailable());
        }
        let mut vfs: *mut ffi::sqlite3_vfs = std::ptr::null_mut();
        let rc = ffi::sqlite3_file_control(connection.handle(), main, ffi::SQLITE_FCNTL_VFS_POINTER, &mut vfs as *mut _ as *mut c_void);
        if rc != ffi::SQLITE_OK || vfs.is_null() || (*vfs).zName.is_null() || !std::ffi::CStr::from_ptr((*vfs).zName).to_bytes().starts_with(b"unix") {
            return Err(unavailable());
        }
        let head = &*(file as *const UnixFileHead);
        if !std::ptr::eq(head.vfs, vfs as *const ffi::sqlite3_vfs) || head.descriptor < 0 {
            return Err(unavailable());
        }
        let mut stat: libc::stat = std::mem::zeroed();
        if libc::fstat(head.descriptor, &mut stat) != 0 || (stat.st_mode & libc::S_IFMT) != libc::S_IFREG {
            return Err(unavailable());
        }
        Ok((stat.st_dev as u64, stat.st_ino as u64))
    }
}
/// A file's length and exact-byte content identity, read in bounded pieces.
fn read_identity(file: &mut std::fs::File) -> Result<(u64, String), String> {
    use sha2::Digest;
    use std::io::{Read, Seek};
    file.seek(std::io::SeekFrom::Start(0)).map_err(|e| format!("App history unavailable: {e}"))?;
    let mut hasher = sha2::Sha256::new();
    let mut buffer = vec![0u8; 1 << 20];
    let mut length = 0u64;
    loop {
        let n = file.read(&mut buffer).map_err(|e| format!("App history unavailable: {e}"))?;
        if n == 0 {
            break;
        }
        hasher.update(&buffer[..n]);
        length += n as u64;
    }
    Ok((length, hasher.finalize().iter().map(|b| format!("{b:02x}")).collect()))
}
fn next_batch(tx: &rusqlite::Transaction) -> rusqlite::Result<i64> {
    tx.query_row("SELECT COALESCE(MAX(batch), 0) + 1 FROM ledger_entry", [], |r| r.get(0))
}
fn insert(tx: &rusqlite::Transaction, entry: &Value, text: &str, origin: &str, batch: i64) -> rusqlite::Result<i64> {
    let column = |key: &str| entry.get(key).and_then(Value::as_str).map(str::to_owned);
    let generation = column("generation").or_else(|| column("lastLoadedGeneration"));
    tx.execute(
        "INSERT INTO ledger_entry (kind, session, home, thread, generation, origin, batch, currency, subject, entry) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
        params![column("kind").unwrap_or_default(), column("session"), column("home"), column("threadId"), generation, origin, batch, currency(entry), subject(entry), text],
    )?;
    Ok(tx.last_insert_rowid())
}

/// How long a write waits for another App instance's transaction before it
/// is reported not confirmed.
fn busy_timeout() -> std::time::Duration {
    #[cfg(test)]
    if let Some(ms) = BUSY_TIMEOUT_MS.with(|t| t.get()) {
        return std::time::Duration::from_millis(ms);
    }
    std::time::Duration::from_secs(5)
}
#[cfg(test)]
thread_local! {
    /// Test hook: a shorter busy timeout for connections opened on this thread.
    pub(crate) static BUSY_TIMEOUT_MS: std::cell::Cell<Option<u64>> = const { std::cell::Cell::new(None) };
}

#[cfg(test)]
#[path = "recovery_store_tests.rs"]
mod tests;
