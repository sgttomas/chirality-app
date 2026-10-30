//! In-process ownership of one actually spawned process group. No cold PID input.
use serde_json::{json, Value};
use std::os::unix::process::{CommandExt, ExitStatusExt};
use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, Command, ExitStatus};
use std::sync::{Arc, Mutex};
use std::time::Duration;

const POLL: Duration = Duration::from_millis(50); // existing Host process polling cadence
#[cfg(test)]
thread_local! { static NEXT_MINT_ERROR: std::cell::Cell<Option<i32>> = const { std::cell::Cell::new(None) }; }
#[cfg(test)]
pub(crate) fn model_next_mint_error(errno: i32) {
    NEXT_MINT_ERROR.with(|e| e.set(Some(errno)));
}
const MEMBER_BYTES: usize = 64 * 1024;
const MEMBER_BUDGET: usize = MEMBER_BYTES / std::mem::size_of::<libc::pid_t>();

#[derive(Clone, Debug)]
pub(crate) enum Census {
    Complete(usize),
    Unknown(String),
}
impl Census {
    pub(crate) fn empty(&self) -> bool {
        matches!(self, Self::Complete(0))
    }
    pub(crate) fn report(&self) -> Value {
        match self {
            Self::Complete(n) => {
                json!({"checked":true,"surviving":n,"handling":if *n==0 {"no live members observed in the original reserved process group; detached/escaped descendants unobserved"}else{"live members observed in the original reserved process group; recorded, not ended; detached/escaped descendants unobserved"}})
            }
            Self::Unknown(e) => {
                json!({"checked":false,"surviving":null,"handling":format!("unavailable: {e}; original reserved process group only; detached/escaped descendants unobserved")})
            }
        }
    }
}
struct State {
    child: Option<Child>,
    exit: Option<ExitStatus>,
    released: bool,
    known_empty: bool,
    generation: Option<Value>,
    monitor: bool,
    observation_limit: Option<String>,
}
pub(crate) struct OwnedProcess {
    pid: i32,
    state: Mutex<State>,
    #[cfg(test)]
    pub(crate) before_group_operation: Mutex<Option<Box<dyn FnMut(i32, &'static str) + Send>>>,
    #[cfg(test)]
    pub(crate) census_override: Mutex<Option<Census>>,
    #[cfg(test)]
    pub(crate) waitid_errors: Mutex<std::collections::VecDeque<i32>>,
}
impl OwnedProcess {
    /// The creation fact is supplied here, not inferred from Child.id after exit.
    pub(crate) fn spawn(command: &mut Command) -> Result<Arc<Self>, String> {
        let child = command
            .process_group(0)
            .spawn()
            .map_err(|e| format!("spawn failed: {e}"))?;
        Self::mint(child)
    }
    fn mint(child: Child) -> Result<Arc<Self>, String> {
        let pid = child.id() as i32;
        let process = Arc::new(Self {
            pid,
            state: Mutex::new(State {
                child: Some(child),
                exit: None,
                released: false,
                known_empty: false,
                generation: None,
                monitor: false,
                observation_limit: None,
            }),
            #[cfg(test)]
            before_group_operation: Mutex::new(None),
            #[cfg(test)]
            census_override: Mutex::new(None),
            #[cfg(test)]
            waitid_errors: Mutex::new(NEXT_MINT_ERROR.with(|e| e.take()).into_iter().collect()),
        });
        // A definitive lost reservation refuses custody. Other unavailable
        // observations retain the actually spawned Child; numeric operations
        // still require a successful original-child observation.
        if let Err(error) = process.observe_exit() {
            if process.released() {
                return Err(error);
            }
            // Creation/group fact is actual. A failed observation is not a
            // reap and cannot discard this still-owned spawned Child.
        }
        Ok(process)
    }
    pub(crate) fn id(&self) -> u32 {
        self.pid as u32
    }
    pub(crate) fn bind(&self, generation: &Value) -> Result<(), String> {
        let mut s = self.state.lock().unwrap();
        if s.released || s.generation.is_some() {
            return Err("process custody already released or bound".into());
        }
        s.generation = Some(generation.clone());
        Ok(())
    }
    pub(crate) fn belongs_to(&self, generation: &Value) -> bool {
        self.state.lock().unwrap().generation.as_ref() == Some(generation)
    }
    pub(crate) fn bound_generation(&self) -> Option<Value> {
        self.state.lock().unwrap().generation.clone()
    }
    /// Released authority can also mean a lost reservation; only known-empty
    /// retirement with observed exit is a settlement fact.
    pub(crate) fn settled(&self) -> bool {
        let s = self.state.lock().unwrap();
        s.known_empty && s.exit.is_some()
    }
    pub(crate) fn take_stdin(&self) -> Option<ChildStdin> {
        self.state
            .lock()
            .unwrap()
            .child
            .as_mut()
            .and_then(|c| c.stdin.take())
    }
    pub(crate) fn take_stdout(&self) -> Option<ChildStdout> {
        self.state
            .lock()
            .unwrap()
            .child
            .as_mut()
            .and_then(|c| c.stdout.take())
    }
    pub(crate) fn take_stderr(&self) -> Option<ChildStderr> {
        self.state
            .lock()
            .unwrap()
            .child
            .as_mut()
            .and_then(|c| c.stderr.take())
    }
    fn observe_locked(&self, s: &mut State) -> Result<Option<ExitStatus>, String> {
        if s.released {
            return s
                .exit
                .map(Some)
                .ok_or_else(|| "original child reservation unavailable".into());
        }
        let mut info = unsafe { std::mem::zeroed::<libc::siginfo_t>() };
        // Nonblocking/nonreaping, with one bounded immediate EINTR retry.
        // Persistent interruption/error is retained as unknown, so polling
        // callers can release their locks before waiting again.
        let mut observation = Err(std::io::Error::from_raw_os_error(libc::EINTR));
        for _ in 0..2 {
            #[cfg(test)]
            let modeled = self.waitid_errors.lock().unwrap().pop_front();
            #[cfg(not(test))]
            let modeled: Option<i32> = None;
            observation = if let Some(errno) = modeled {
                Err(std::io::Error::from_raw_os_error(errno))
            } else {
                let rc = unsafe {
                    libc::waitid(
                        libc::P_PID,
                        self.pid as libc::id_t,
                        &mut info,
                        libc::WEXITED | libc::WNOHANG | libc::WNOWAIT,
                    )
                };
                if rc < 0 {
                    Err(std::io::Error::last_os_error())
                } else {
                    Ok(())
                }
            };
            if !observation
                .as_ref()
                .is_err_and(|e| e.raw_os_error() == Some(libc::EINTR))
            {
                break;
            }
        }
        if let Err(e) = observation {
            if e.raw_os_error() == Some(libc::ECHILD) {
                s.released = true;
                s.child = None;
            }
            let limit = format!("original child exit observation unavailable: {e}");
            s.observation_limit = Some(limit.clone());
            return Err(limit);
        }
        s.observation_limit = None;
        if info.si_pid != 0 {
            let raw = match info.si_code {
                libc::CLD_EXITED => info.si_status << 8,
                libc::CLD_KILLED => info.si_status,
                libc::CLD_DUMPED => info.si_status | 0x80,
                _ => {
                    let limit = "unknown original child exit observation".to_string();
                    s.observation_limit = Some(limit.clone());
                    return Err(limit);
                }
            };
            s.exit = Some(ExitStatus::from_raw(raw));
        }
        Ok(s.exit)
    }
    pub(crate) fn observe_exit(&self) -> Result<Option<ExitStatus>, String> {
        self.observe_locked(&mut self.state.lock().unwrap())
    }
    pub(crate) fn observation_limit(&self) -> Option<String> {
        self.state.lock().unwrap().observation_limit.clone()
    }
    /// Waits only for this original leader; a Stop can acquire custody between polls.
    pub(crate) fn wait_exit(&self) -> Result<ExitStatus, String> {
        self.wait_exit_observed(|_| {})
    }
    pub(crate) fn wait_exit_observed(
        &self,
        mut unavailable: impl FnMut(&str),
    ) -> Result<ExitStatus, String> {
        loop {
            match self.observe_exit() {
                Ok(Some(status)) => return Ok(status),
                Ok(None) => {}
                Err(error) => {
                    unavailable(&error);
                    if self.released() {
                        return Err(error);
                    }
                }
            }
            // No custody/source gate is held during wait or limit publication.
            std::thread::sleep(POLL);
        }
    }
    fn point(&self, operation: &'static str) {
        #[cfg(test)]
        if let Some(hook) = self.before_group_operation.lock().unwrap().as_mut() {
            hook(self.pid, operation);
        }
        #[cfg(not(test))]
        let _ = operation;
    }
    fn census_locked(&self, s: &mut State) -> Census {
        if s.released {
            return if s.known_empty {
                Census::Complete(0)
            } else {
                Census::Unknown("group authority unavailable; no numeric query".into())
            };
        }
        if let Err(e) = self.observe_locked(s) {
            return Census::Unknown(e);
        }
        if s.released {
            return Census::Unknown("original child reservation lost".into());
        }
        self.point("census");
        #[cfg(test)]
        if let Some(value) = self.census_override.lock().unwrap().clone() {
            return value;
        }
        #[cfg(target_os = "macos")]
        {
            // SDK sys/proc_info.h: PROC_PGRP_ONLY=2; never PROC_ALL_PIDS.
            let mut members = vec![0 as libc::pid_t; MEMBER_BUDGET];
            unsafe {
                *libc::__error() = 0;
            }
            let bytes = unsafe {
                libc::proc_listpids(
                    2,
                    self.pid as u32,
                    members.as_mut_ptr().cast(),
                    MEMBER_BYTES as i32,
                )
            };
            let error = std::io::Error::last_os_error().raw_os_error().unwrap_or(0);
            if bytes < 0 || (bytes == 0 && error != 0) {
                return Census::Unknown(format!("owned-group enumeration failed (errno {error})"));
            }
            if bytes as usize >= MEMBER_BYTES
                || bytes as usize % std::mem::size_of::<libc::pid_t>() != 0
            {
                return Census::Unknown(
                    "owned-group enumeration incomplete or exceeds member budget".into(),
                );
            }
            members.truncate(bytes as usize / std::mem::size_of::<libc::pid_t>());
            let mut live = 0;
            let mut seen = std::collections::HashSet::new();
            let original = members.clone();
            for pid in members {
                if pid <= 0 || !seen.insert(pid) {
                    return Census::Unknown("invalid or duplicate owned-group member".into());
                }
                // Darwin lists the reserved zombie leader but proc_pidinfo returns
                // ESRCH for it; only our exact WNOWAIT exit proof excludes it.
                if pid == self.pid && s.exit.is_some() {
                    continue;
                }
                let mut info = unsafe { std::mem::zeroed::<libc::proc_bsdinfo>() };
                let required = std::mem::size_of::<libc::proc_bsdinfo>();
                let n = unsafe {
                    libc::proc_pidinfo(
                        pid,
                        libc::PROC_PIDTBSDINFO,
                        0,
                        (&mut info as *mut libc::proc_bsdinfo).cast(),
                        required as i32,
                    )
                };
                if n as usize != required
                    || info.pbi_pid != pid as u32
                    || info.pbi_pgid != self.pid as u32
                {
                    return Census::Unknown(
                        "owned-group member unavailable, partial or changed association".into(),
                    );
                }
                if !(1..=libc::SZOMB).contains(&info.pbi_status) {
                    return Census::Unknown("unknown owned-group member status".into());
                }
                if info.pbi_status != libc::SZOMB {
                    live += 1;
                }
            }
            if s.exit.is_none() && !seen.contains(&self.pid) {
                return Census::Unknown("live leader association changed or unavailable".into());
            }
            // An observed member can fork and then exit while its status is read.
            // Recheck membership before treating an all-zombie snapshot as empty.
            let mut final_members = vec![0 as libc::pid_t; MEMBER_BUDGET];
            unsafe {
                *libc::__error() = 0;
            }
            let final_bytes = unsafe {
                libc::proc_listpids(
                    2,
                    self.pid as u32,
                    final_members.as_mut_ptr().cast(),
                    MEMBER_BYTES as i32,
                )
            };
            let final_error = std::io::Error::last_os_error().raw_os_error().unwrap_or(0);
            if final_bytes < 0
                || (final_bytes == 0 && final_error != 0)
                || final_bytes as usize >= MEMBER_BYTES
                || final_bytes as usize % std::mem::size_of::<libc::pid_t>() != 0
            {
                return Census::Unknown(
                    "owned-group final inventory unavailable or incomplete".into(),
                );
            }
            final_members.truncate(final_bytes as usize / std::mem::size_of::<libc::pid_t>());
            let mut before = original;
            before.sort_unstable();
            final_members.sort_unstable();
            if before != final_members {
                return Census::Unknown("owned-group membership changed during census".into());
            }
            Census::Complete(live)
        }
        #[cfg(not(target_os = "macos"))]
        {
            Census::Unknown("owned-group census unavailable on this platform".into())
        }
    }
    pub(crate) fn census(&self) -> Census {
        self.census_locked(&mut self.state.lock().unwrap())
    }
    fn signal_locked(&self, s: &mut State, signal: i32) -> Result<(), String> {
        if s.released {
            return Err("group authority released; no signal".into());
        }
        self.observe_locked(s)?;
        if s.released {
            return Err("original child reservation lost; no signal".into());
        }
        self.point("signal");
        let rc = unsafe { libc::killpg(self.pid, signal) };
        if rc < 0 {
            return Err(format!(
                "owned-group signal failed: {}",
                std::io::Error::last_os_error()
            ));
        }
        Ok(())
    }
    pub(crate) fn signal(&self, signal: i32) -> Result<(), String> {
        self.signal_locked(&mut self.state.lock().unwrap(), signal)
    }
    /// Recheck and optional force share custody with retirement. The boolean is
    /// an actual syscall attempt, including an attempted-but-failed signal.
    pub(crate) fn force_if_needed(&self) -> (bool, Option<String>) {
        let mut s = self.state.lock().unwrap();
        if self.census_locked(&mut s).empty() {
            return (false, None);
        }
        if s.released {
            return (false, Some("group authority unavailable; no signal".into()));
        }
        if let Err(e) = self.observe_locked(&mut s) {
            return (false, Some(e));
        }
        self.point("signal");
        let rc = unsafe { libc::killpg(self.pid, libc::SIGKILL) };
        (
            true,
            if rc < 0 {
                Some(format!(
                    "owned-group signal failed: {}",
                    std::io::Error::last_os_error()
                ))
            } else {
                None
            },
        )
    }
    /// A complete empty observation is made under the same reservation as reap.
    pub(crate) fn release_if_empty(&self) -> Census {
        let mut s = self.state.lock().unwrap();
        if s.released {
            return if s.known_empty {
                Census::Complete(0)
            } else {
                Census::Unknown("original child reservation unavailable".into())
            };
        }
        let census = self.census_locked(&mut s);
        if census.empty() && s.exit.is_some() {
            s.released = true;
            s.known_empty = true; // no later call can operate on this number
            if let Some(mut child) = s.child.take() {
                match child.wait() {
                    Ok(status) => s.exit = Some(status),
                    Err(e) => return Census::Unknown(format!("original child reap failed: {e}")),
                }
            }
        }
        census
    }
    pub(crate) fn maintain(self: &Arc<Self>) {
        {
            let mut s = self.state.lock().unwrap();
            if s.monitor || s.released {
                return;
            }
            s.monitor = true;
        }
        let process = Arc::clone(self);
        let result = std::thread::Builder::new()
            .name("owned-group-retirement".into())
            .spawn(move || loop {
                process.release_if_empty();
                if process.released() {
                    break;
                }
                std::thread::sleep(POLL);
            });
        if result.is_err() {
            self.state.lock().unwrap().monitor = false;
        }
    }
    pub(crate) fn released(&self) -> bool {
        self.state.lock().unwrap().released
    }
    pub(crate) fn abort_spawn(self: &Arc<Self>) -> Census {
        let _ = self.signal(libc::SIGKILL);
        let census = self.release_if_empty();
        self.maintain(); // no polling sleep in the caller's publication/source gate
        census
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn released_reservation_is_not_a_settlement_fact() {
        let process = OwnedProcess::spawn(&mut Command::new("/usr/bin/true")).unwrap();
        process.wait_exit().unwrap();
        // Model a competing reaper using this actual original Child, not a
        // sampled PID. Its lost reservation must never become a clean result.
        process.state.lock().unwrap().child.as_mut().unwrap().wait().unwrap();
        assert!(process.observe_exit().is_err());
        assert!(process.released());
        assert!(!process.settled());
        assert!(!process.release_if_empty().empty());
    }
    #[test]
    fn process_group_custody_reaped_cached_child_cannot_mint_authority() {
        // Raw Child exists only to exercise the rejected ingress; no group
        // query/signal is possible from this already-reaped test value.
        let mut child = Command::new("/usr/bin/true")
            .process_group(0)
            .spawn()
            .unwrap();
        child.wait().unwrap();
        assert!(OwnedProcess::mint(child)
            .err()
            .unwrap()
            .contains("exit observation unavailable"));
    }
    #[test]
    fn process_group_custody_bind_is_once_and_reservation_survives_unknown() {
        let p = OwnedProcess::spawn(
            Command::new("/bin/sleep")
                .arg("0.1")
                .stdin(std::process::Stdio::null())
                .stdout(std::process::Stdio::null()),
        )
        .unwrap();
        let g = json!({"appSession":"synthetic","home":"home","spawnCounter":1});
        p.bind(&g).unwrap();
        assert!(p.bind(&g).is_err());
        assert!(p.belongs_to(&g));
        p.wait_exit().unwrap();
        *p.census_override.lock().unwrap() =
            Some(Census::Unknown("partial member response".into()));
        assert!(!p.release_if_empty().empty());
        assert!(!p.released());
        assert!(p.census().report()["surviving"].is_null());
        *p.census_override.lock().unwrap() = None;
        assert!(p.release_if_empty().empty());
        assert!(p.released());
        assert_eq!(p.force_if_needed(), (false, None));
    }
}

#[cfg(test)]
mod observation_error_tests {
    use super::*;
    #[test]
    fn process_group_custody_modeled_mint_interrupt_and_nonterminal_error_keep_actual_child() {
        for errno in [libc::EINTR, libc::EINVAL] {
            // A scoped modeled SDK error; actual WNOWAIT independently proves
            // the invented owned leader remains alive/unreaped.
            model_next_mint_error(errno);
            let p = OwnedProcess::spawn(
                Command::new("/bin/sleep")
                    .arg("30")
                    .stdin(std::process::Stdio::null())
                    .stdout(std::process::Stdio::null()),
            )
            .unwrap();
            let limit = p.observation_limit();
            let mut info = unsafe { std::mem::zeroed::<libc::siginfo_t>() };
            let reserved = unsafe {
                libc::waitid(
                    libc::P_PID,
                    p.id() as libc::id_t,
                    &mut info,
                    libc::WEXITED | libc::WNOHANG | libc::WNOWAIT,
                )
            } == 0
                && info.si_pid == 0;
            p.abort_spawn();
            p.wait_exit().unwrap();
            p.release_if_empty();
            assert!(reserved);
            assert_eq!(
                limit.is_some(),
                errno != libc::EINTR,
                "nonterminal unknown is retained; single interrupt retries"
            );
            assert!(p.released());
        }
    }
}
