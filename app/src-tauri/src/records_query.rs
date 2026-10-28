//! Disposable, process-owned disk query cache. No record bodies live here.
use super::{Line, Stamp};
use rusqlite::{params, Connection, OpenFlags};
use std::path::{Path, PathBuf};
use std::cell::Cell;

pub(super) struct QueryDb {
    conn: Connection,
    pub(super) path: PathBuf,
    stamp: Option<Stamp>,
    identity: (u64, u64),
    data_version: i64,
    writing: Cell<bool>,
}
impl QueryDb {
    pub(super) fn open(root: &Path) -> Result<Self, String> {
        // Never reuse another process's mutable cache for absence/duplicate
        // decisions. Each process rebuilds from the authoritative logs.
        let stem = format!("query-{}-{}.sqlite", crate::util::sha256_hex(root.as_os_str().as_encoded_bytes()), crate::util::opaque_id("")?);
        let store = crate::records_store::current().ok().map(|s| s.root.join("indexes"));
        let mut places = store.into_iter().collect::<Vec<_>>();
        places.push(std::fs::canonicalize(std::env::temp_dir()).map_err(|e| e.to_string())?);
        let mut last = String::new();
        for dir in places {
            match Self::at(&dir.join(&stem)) { Ok(db) => return Ok(db), Err(e) => last = e }
        }
        Err(last)
    }
    fn at(path: &Path) -> Result<Self, String> {
        use std::os::unix::fs::OpenOptionsExt;
        crate::storage::ensure_directory(path.parent().ok_or("cache has no parent")?)?;
        crate::storage::check_path(path)?;
        let created = std::fs::OpenOptions::new().write(true).create_new(true).mode(0o600).custom_flags(libc::O_NOFOLLOW).open(path).map_err(|e| e.to_string())?;
        let original = Stamp::of(&created.metadata().map_err(|e| e.to_string())?);
        let identity = (original.dev, original.ino);
        let opened = || -> rusqlite::Result<Connection> {
            let conn = Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_NOFOLLOW)?;
            if !same_identity(path, identity) { return Err(rusqlite::Error::InvalidQuery); }
            // The cache is rebuildable: no durable WAL or large SQLite page
            // cache. Disk backs query sorting and membership sets too.
            conn.execute_batch("PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=FILE; PRAGMA cache_size=-2048; PRAGMA trusted_schema=OFF;
                CREATE TABLE entries(log INTEGER NOT NULL, offset INTEGER NOT NULL, len INTEGER NOT NULL, seq TEXT NOT NULL, id TEXT, act INTEGER NOT NULL, corrects TEXT, late_subject TEXT, member INTEGER, digest TEXT NOT NULL);
                CREATE INDEX entry_identities ON entries(id);
                CREATE TABLE identities(id TEXT PRIMARY KEY, holders INTEGER NOT NULL);
                CREATE INDEX duplicates ON identities(holders) WHERE holders>1;
                CREATE TRIGGER entry_added AFTER INSERT ON entries WHEN NEW.id IS NOT NULL BEGIN
                    INSERT INTO identities VALUES(NEW.id,1) ON CONFLICT(id) DO UPDATE SET holders=holders+1;
                END;
                CREATE TRIGGER entry_removed AFTER DELETE ON entries WHEN OLD.id IS NOT NULL BEGIN
                    UPDATE identities SET holders=holders-1 WHERE id=OLD.id;
                    DELETE FROM identities WHERE id=OLD.id AND holders=0;
                END;
                CREATE INDEX positions ON entries(log, offset, member);
                CREATE INDEX acts ON entries(act, id, corrects);
                CREATE INDEX late ON entries(late_subject);
                CREATE INDEX correction_targets ON entries(corrects, act);")?;
            Ok(conn)
        };
        match opened() {
            Ok(conn) => {
                let data_version = conn.query_row("PRAGMA data_version", [], |r| r.get(0)).map_err(|e| e.to_string())?;
                let mut db = Self { conn, path: path.to_path_buf(), stamp: None, identity, data_version, writing:Cell::new(false) };
                db.mark().map_err(|e| e.to_string())?; Ok(db)
            }
            Err(e) => { if same_identity(path, identity) { let _ = std::fs::remove_file(path); } Err(e.to_string()) }
        }
    }
    pub(super) fn unchanged(&self) -> bool {
        crate::storage::check_path(&self.path).is_ok() && self.stamp.is_some_and(|s| super::stamp_of(&self.path) == Some(s)) && same_identity(&self.path, self.identity) && self.version().is_ok_and(|v| v == self.data_version)
    }
    fn version(&self) -> rusqlite::Result<i64> { self.conn.query_row("PRAGMA data_version", [], |r| r.get(0)) }
    fn mark(&mut self) -> rusqlite::Result<()> {
        // A successful write through the old SQLite descriptor does not make
        // a replacement at its former pathname our cache or our cleanup leaf.
        self.stamp = super::stamp_of(&self.path).filter(|s| (s.dev, s.ino) == self.identity);
        // data_version changes on other connections' commits, never ours.
        // Keep the original basis: even an edit between our COMMIT and this
        // restamp cannot be adopted as though we made it.
        if self.stamp.is_none() || self.version()? != self.data_version { self.stamp = None; return Err(rusqlite::Error::InvalidQuery); }
        Ok(())
    }
    pub(super) fn begin_log(&self, log: u32, from: u64) -> rusqlite::Result<()> {
        self.conn.execute_batch("BEGIN IMMEDIATE")?;
        // Take SQLite's writer lock first, then check the cache basis before
        // our first mutation. External SQL commits cannot slip between them.
        if !self.unchanged() { self.conn.execute_batch("ROLLBACK")?; return Err(rusqlite::Error::InvalidQuery); }
        self.writing.set(true);
        self.conn.execute("DELETE FROM entries WHERE log=?1 AND offset>=?2", params![log, from])?;
        Ok(())
    }
    pub(super) fn clear_log(&self, log: u32) -> rusqlite::Result<()> {
        if !self.writing.get() { return Err(rusqlite::Error::InvalidQuery); }
        self.conn.execute("DELETE FROM entries WHERE log=?", [log])?; Ok(())
    }
    pub(super) fn finish_log(&mut self, success: bool) -> rusqlite::Result<()> {
        if !self.writing.replace(false) { return Err(rusqlite::Error::InvalidQuery); }
        self.conn.execute_batch(if success { "COMMIT" } else { "ROLLBACK" })?;
        self.mark()?; Ok(())
    }
    pub(super) fn insert(&self, log: u32, l: &Line) -> rusqlite::Result<()> {
        if !self.writing.get() { return Err(rusqlite::Error::InvalidQuery); }
        self.conn.prepare_cached("INSERT INTO entries VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10)")?.execute(params![log, l.offset, l.len as u64, l.seq.to_string(), l.id, l.act, l.corrects, l.late_subject, l.member.map(|m| m as u64), l.digest])?;
        Ok(())
    }
    pub(super) fn remove(&mut self, log: u32) -> rusqlite::Result<()> {
        self.begin_log(log, 0)?;
        self.finish_log(true)
    }
    /// Install only source-verified positions, retaining a byte-proved prefix.
    /// The staging file is newly built by this process, checked before/after
    /// the copy, and writer-locked by the attached SQLite transaction.
    pub(super) fn copy_log(&mut self, source: &Self, log: u32, from: u64, source_still_current: impl FnOnce() -> bool) -> rusqlite::Result<()> {
        if !source.unchanged() || !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        self.conn.execute("ATTACH DATABASE ? AS verified", [source.path.to_str().ok_or(rusqlite::Error::InvalidQuery)?])?;
        let result = (|| {
            self.begin_log(log, from)?;
            if !source.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
            self.conn.execute("INSERT INTO entries SELECT * FROM verified.entries WHERE log=?1 AND offset>=?2", params![log, from])?;
            if !source.unchanged() || !source_still_current() { return Err(rusqlite::Error::InvalidQuery); }
            self.finish_log(true)?;
            if !source.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
            Ok(())
        })();
        if result.is_err() && !self.conn.is_autocommit() { let _ = self.conn.execute_batch("ROLLBACK"); }
        self.writing.set(false);
        let detached = self.conn.execute_batch("DETACH DATABASE verified");
        if result.is_err() || detached.is_err() {
            // journal_mode=OFF is deliberate for a disposable cache; a failed
            // copy/rollback cannot establish an authoritative absence.
            self.stamp = None;
            return Err(rusqlite::Error::InvalidQuery);
        }
        result
    }
    pub(super) fn holds(&self, id: &str) -> rusqlite::Result<bool> {
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        let found = self.conn.query_row("SELECT EXISTS(SELECT 1 FROM identities WHERE id=?)", [id], |r| r.get(0))?;
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        Ok(found)
    }
    pub(super) fn touches_acts(&self, log: u32, from: u64) -> rusqlite::Result<bool> {
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        let any: bool = self.conn.query_row("SELECT EXISTS(SELECT 1 FROM entries WHERE act=1)", [], |r| r.get(0))?;
        let touches = any && self.conn.query_row("SELECT EXISTS(SELECT 1 FROM entries e WHERE e.log=?1 AND e.offset>=?2 AND (e.act=1
            OR EXISTS(SELECT 1 FROM entries a WHERE a.id=e.id AND a.act=1)
            OR EXISTS(SELECT 1 FROM entries a WHERE a.corrects=e.id AND a.act=1)))", params![log, from], |r| r.get(0))?;
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        Ok(touches)
    }
    pub(super) fn duplicates(&self) -> rusqlite::Result<Vec<String>> {
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        let mut s = self.conn.prepare("SELECT id, holders FROM identities WHERE holders>1 ORDER BY id")?;
        let mut rows = s.query([])?; let mut out = Vec::new();
        while let Some(r) = rows.next()? { let id: String = r.get(0)?; let n: usize = r.get(1)?; for _ in 1..n { out.push(format!("duplicate record identity: {id}")); } }
        if !self.unchanged() { return Err(rusqlite::Error::InvalidQuery); }
        Ok(out)
    }
    pub(super) fn lines(&self, predicate: &str, value: Option<&str>, mut each: impl FnMut(u32, Line) -> Result<(), String>) -> Result<(), String> {
        if !self.unchanged() { return Err("query cache changed".into()); }
        let mut s = self.conn.prepare(&format!("SELECT log,offset,len,seq,id,act,corrects,late_subject,member,digest FROM entries {predicate} ORDER BY log,offset,member")).map_err(|e| e.to_string())?;
        let mut rows = if let Some(v) = value { s.query([v]) } else { s.query([]) }.map_err(|e| e.to_string())?;
        while let Some(r) = rows.next().map_err(|e| e.to_string())? {
            let read = || -> rusqlite::Result<(u32, Line)> { Ok((r.get(0)?, Line { offset:r.get(1)?,len:r.get::<_,u64>(2)? as usize,seq:r.get::<_,String>(3)?.parse().map_err(|_| rusqlite::Error::InvalidQuery)?,id:r.get(4)?,act:r.get(5)?,corrects:r.get(6)?,late_subject:r.get(7)?,member:r.get::<_,Option<u64>>(8)?.map(|m| m as usize),digest:r.get(9)? })) };
            let (log, line) = read().map_err(|e| e.to_string())?; each(log, line)?;
        }
        if !self.unchanged() { return Err("query cache changed while it was read".into()); }
        Ok(())
    }
}
fn same_identity(path: &Path, identity: (u64, u64)) -> bool {
    crate::storage::check_path(path).is_ok() && super::stamp_of(path).is_some_and(|s| (s.dev, s.ino) == identity)
}
impl Drop for QueryDb {
    fn drop(&mut self) {
        // Remove only our own file, never a substituted path or symlink.
        if self.unchanged() { let _ = std::fs::remove_file(&self.path); }
    }
}
