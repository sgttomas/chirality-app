#!/usr/bin/env python3
"""VC version-advance wrapper: rerun the OBS-2 and OBS-3 harnesses, unchanged, against Codex 0.160.0.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-4-20261003, node VC). Not product code; not an App
candidate; nothing here is qualified. Python 3 standard library only.

It imports ../obs2/obs2_harness.py and ../obs3/obs3_harness.py without editing them and changes four
things at run time, all to stay inside the VC brief (no network other than the one approved download):

1. No warm plugin-cache template. OBS-2 seeded each home with a plugin cache copied from an OBS-1b scratch
   home; that cache made Codex run `git ls-remote` against github.com at start (OBS-2 O-7 v0). Here every
   home is created cold (warm=False), as OBS-3 did.
2. Start-up network off in every home. A session whose home's config.toml does not already say
   `plugins = false` is started with the launch override `-c features.plugins=false` (OBS-2 O-7 found this
   feature stops both start-up connections at 0.158.0). OBS-3 homes and the O-7 variants used here carry it
   in config.toml already, so they get no override. Consequence: O-6 cases whose home has no such line show
   an extra `sessionFlags` layer holding `features.plugins = false` in config/read.
3. Guards. Every session ends its process group at once if a `git` process appears in it (OBS-2's cold-home
   guard, applied to all), and any non-loopback socket of a Codex process group, at any time, stops the
   scenario (stop id "S-5-any"), not only during a turn.
4. O-7 runs only the variants that set `plugins = false` (v1, v6, v7, v8); the baseline and the variants that
   leave plugins on (v0, v2, v3, v4, v5) would contact chatgpt.com and github.com and are not run.

The begin event's pin label is rewritten to 0.160.0. Everything else (scenarios, prompts, invented
material, S-1...S-11 checks, S-9 memory-pressure stop, answers with origin observation-harness) is the
OBS-2/OBS-3 code as committed.

Usage:
  va_harness.py obs2 --obs DIR --binary PATH [obs2 options] SCENARIO
  va_harness.py obs3 --obs DIR --binary PATH [obs3 options] SCENARIO
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "obs2"))
sys.path.insert(0, os.path.join(HERE, "..", "obs3"))
import obs2_harness as H  # noqa: E402  (unchanged)

PIN = "0.160.0"
OVERRIDE = ["-c", "features.plugins=false"]

# 1. cold homes only
_orig_make_home = H.Run.make_home


def make_home(self, name, config_text=None, warm=True):
    return _orig_make_home(self, name, config_text, warm=False)


H.Run.make_home = make_home

# 2. plugins off for every session; 3a. git guard for every session
_orig_init = H.Session.__init__


def session_init(self, run, label, home, cwd, argv_extra=(), env_extra=None, policy=None, snap_interval=0.25):
    cfg = os.path.join(home, "config.toml")
    text = ""
    if os.path.exists(cfg):
        with open(cfg, "r", encoding="utf-8") as f:
            text = f.read()
    extra = list(argv_extra)
    if "plugins = false" not in text and "features.plugins=false" not in " ".join(extra):
        extra = OVERRIDE + extra
    _orig_init(self, run, label, home, cwd, argv_extra=extra, env_extra=env_extra, policy=policy,
               snap_interval=snap_interval)
    self.kill_on_git = True


H.Session.__init__ = session_init

# 3b. any non-loopback socket stops the scenario; pin label
_orig_event = H.Run.event


def run_event(self, kind, **kw):
    if kind == "begin":
        kw["pin"] = PIN
        kw["wrapper"] = "version_advance/va_harness.py"
    _orig_event(self, kind, **kw)
    if kind.endswith(":non-loopback-socket"):
        self.trigger_stop("S-5-any", "non-loopback socket from a Codex process group: %s %s:%s"
                          % (kw.get("process", "?")[:80], kw.get("remote"), kw.get("port")))


H.Run.event = run_event

# 4. O-7: plugins-off variants only
H.O7_VARIANTS = [v for v in H.O7_VARIANTS if "plugins = false" in v[1]]


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("obs2", "obs3"):
        raise SystemExit(__doc__)
    suite = sys.argv.pop(1)
    if suite == "obs2":
        H.main()
    else:
        import obs3_harness as H3  # noqa: E402  (unchanged; imports the same, patched, obs2_harness module)
        assert H3.H is H
        H3.main()


if __name__ == "__main__":
    main()
