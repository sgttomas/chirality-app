#!/usr/bin/env python3
"""Executable model of DEL-01-05/ACCESS-v0.1 (design prototype, not product code).

Node D4 of run APP-V4-DESIGN-PASS-3-20261001. Python 3 standard library only.
No Codex process, no model, no network, no credential: every value is invented.
The strings used to test custody are canaries that are deliberately NOT shaped
like any real key, token, URL or code.

Contents
  TABLES             the §5 transition tables (ACCESS-v0.1), row for row
  Machine            a table-driven state machine that refuses unlisted moves
  parse_doc_tables   reads the same tables from ACCOUNT_AND_PROVIDER_ACCESS.md
  App / Conversation the K-3 selection walk and K2-1 routing (§2-§6)
  Recorder           the CR-1…CR-10 redaction and the custody scan (§7)
  link_case          the configuration-link dry run in a temporary folder (§5.5)
  network_view       the K-12 view merge (§9)
"""
import os
import re
import tempfile

# ---------------------------------------------------------------------------
# §5 transition tables: (id, from, event, to)
# ---------------------------------------------------------------------------
TABLES = {
    "AE": [
        ("AE-1", "unknown", "read:null", "signed-out"),
        ("AE-2", "unknown", "read:chatgpt", "signed-in"),
        ("AE-3", "unknown", "read:other-kind", "signed-out"),
        ("AE-4", "signed-out", "policy:excluded", "not-permitted"),
        ("AE-5", "not-permitted", "policy:permitted", "signed-out"),
        ("AE-6", "signed-out", "person:sign-in", "signing-in"),
        ("AE-7", "signed-out", "start:error", "signed-out"),
        ("AE-8", "signing-in", "completed:success", "signed-in"),
        ("AE-9", "signing-in", "completed:failure", "signed-out"),
        ("AE-10", "signing-in", "person:cancel", "signed-out"),
        ("AE-11", "signing-in", "generation:closed", "unknown"),
        ("AE-12", "signed-in", "person:sign-out", "signing-out"),
        ("AE-13", "signing-out", "logout:ok", "signed-out"),
        ("AE-14", "signing-out", "logout:failed", "unknown"),
        ("AE-15", "signed-in", "auth:recovery-started", "needs-reauth"),
        ("AE-16", "needs-reauth", "auth:recovery-completed", "signed-in"),
        ("AE-17", "needs-reauth", "read:null", "signed-out"),
        ("AE-18", "signed-in", "generation:closed", "unknown"),
        ("AE-19", "signed-out", "generation:closed", "unknown"),
        ("AE-20", "needs-reauth", "person:sign-in", "signing-in"),
    ],
    "KE": [
        ("KE-1", "unknown", "read:null", "absent"),
        ("KE-2", "unknown", "read:apiKey", "present"),
        ("KE-3", "absent", "policy:excluded", "not-permitted"),
        ("KE-4", "not-permitted", "policy:permitted", "absent"),
        ("KE-5", "absent", "person:enter-key", "entering"),
        ("KE-6", "entering", "login:ok", "present"),
        ("KE-7", "entering", "login:error", "absent"),
        ("KE-8", "entering", "generation:closed", "unknown"),
        ("KE-9", "present", "use:auth-failed", "failing"),
        ("KE-10", "failing", "use:ok", "present"),
        ("KE-11", "present", "person:replace-key", "entering"),
        ("KE-12", "failing", "person:replace-key", "entering"),
        ("KE-13", "present", "person:remove-key", "removing"),
        ("KE-14", "failing", "person:remove-key", "removing"),
        ("KE-15", "removing", "logout:ok", "absent"),
        ("KE-16", "removing", "logout:failed", "unknown"),
        ("KE-17", "present", "generation:closed", "unknown"),
        ("KE-18", "absent", "generation:closed", "unknown"),
    ],
    "LE": [
        ("LE-1", "not-configured", "config:local", "listed"),
        ("LE-2", "not-configured", "config:needs-credential", "not-offered"),
        ("LE-3", "listed", "start:reported", "in-use"),
        ("LE-4", "listed", "use:failed", "failing"),
        ("LE-5", "in-use", "use:failed", "failing"),
        ("LE-6", "failing", "use:ok", "in-use"),
        ("LE-7", "listed", "config:gone", "not-configured"),
        ("LE-8", "in-use", "config:gone", "not-configured"),
        ("LE-9", "failing", "config:gone", "not-configured"),
        ("LE-10", "not-offered", "config:gone", "not-configured"),
        ("LE-11", "listed", "config:needs-credential", "not-offered"),
        ("LE-12", "not-offered", "config:local", "listed"),
    ],
    "CS": [
        ("CS-1", "no-selection", "person:message", "no-selection"),
        ("CS-2", "offer-shown", "person:message", "offer-shown"),
        ("CS-3", "no-selection", "app:last-choice-exists", "offer-shown"),
        ("CS-4", "offer-shown", "person:accept-offer", "selected"),
        ("CS-5", "no-selection", "person:choose", "selected"),
        ("CS-6", "offer-shown", "person:choose", "selected"),
        ("CS-7", "selected", "person:choose", "selected"),
        ("CS-8", "selected", "person:message", "starting"),
        ("CS-9", "starting", "start:ok", "started"),
        ("CS-10", "starting", "start:error", "start-failed"),
        ("CS-11", "starting", "generation:closed", "start-failed"),
        ("CS-12", "start-failed", "person:choose", "selected"),
        ("CS-13", "start-failed", "person:message", "starting"),
        ("CS-14", "selected", "entry:unavailable", "entry-unavailable"),
        ("CS-15", "started", "entry:unavailable", "entry-unavailable"),
        ("CS-16", "entry-unavailable", "entry:available-unstarted", "selected"),
        ("CS-17", "entry-unavailable", "entry:available-started", "started"),
        ("CS-18", "started", "person:change-model", "started"),
        ("CS-19", "started", "person:change-entry", "started"),
        ("CS-20", "entry-unavailable", "person:message", "entry-unavailable"),
        ("CS-21", "started", "person:message", "started"),
    ],
    "CL": [
        ("CL-1", "not-set-up", "setup:target-exists", "linked"),
        ("CL-2", "not-set-up", "setup:target-absent", "target-missing"),
        ("CL-3", "not-set-up", "setup:mechanism-unworkable", "own-config"),
        ("CL-4", "linked", "check:replaced", "link-broken"),
        ("CL-5", "linked", "check:target-gone", "target-missing"),
        ("CL-6", "target-missing", "check:target-back", "linked"),
        ("CL-7", "link-broken", "person:relink", "linked"),
        ("CL-8", "link-broken", "person:keep-own", "own-config"),
        ("CL-9", "own-config", "person:link", "linked"),
        ("CL-10", "linked", "check:intact", "linked"),
    ],
}

INITIAL = {"AE": "unknown", "KE": "unknown", "LE": "not-configured",
           "CS": "no-selection", "CL": "not-set-up"}


class Refused(Exception):
    """A move with no row in the table (the model never invents a transition)."""


class Machine:
    def __init__(self, table):
        self.table = table
        self.state = INITIAL[table]
        self.trace = []

    def apply(self, event):
        for rid, frm, ev, to in TABLES[self.table]:
            if frm == self.state and ev == event:
                self.trace.append(rid)
                self.state = to
                return rid
        raise Refused("%s: no row from %r on %r" % (self.table, self.state, event))


ROW_RE = re.compile(r"^\| ((?:AE|KE|LE|CS|CL)-\d+) \| ([a-z-]+) \| `([A-Za-z:-]+)` \| ([a-z-]+) \|")


def parse_doc_tables(md_path):
    found = {k: [] for k in TABLES}
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            m = ROW_RE.match(line)
            if m:
                rid, frm, ev, to = m.groups()
                found[rid.split("-")[0]].append((rid, frm, ev, to))
    return found


# ---------------------------------------------------------------------------
# Custody: canaries and the recorder (§7)
# ---------------------------------------------------------------------------
KEY_CANARY = "INVENTED-KEY-CANARY-d4-0001"
URL_CANARY = "https://auth.example.invalid/start?state=INVENTED-STATE-CANARY-d4"
VURL_CANARY = "https://device.example.invalid/INVENTED-VURL-CANARY-d4"
CODE_CANARY = "INVENTED-CODE-CANARY-d4"
CANARIES = (KEY_CANARY, URL_CANARY, VURL_CANARY, CODE_CANARY)
REDACTED = "[redacted:credential]"
SECRET_PARAMS = ("apiKey", "accessToken", "secretAccessKey", "sessionToken")
SECRET_RESULTS = ("authUrl", "verificationUrl", "userCode")


def redact_text(text, secrets):
    for s in secrets:
        if s:
            text = text.replace(s, REDACTED)
    return text


class Recorder:
    """Everything durable the App writes: records, logs, snapshots, errors (CR-2, CR-4)."""

    def __init__(self):
        self.records = []
        self.logs = []
        self.errors = []
        self.wire = []        # frames written to the child: the one place a key must pass
        self.display = []     # transient display; cleared when the sign-in ends
        self._in_flight = set()

    def client_request(self, method, params):
        secrets = {params.get(k) for k in SECRET_PARAMS if params.get(k)}
        self._in_flight |= secrets
        self.wire.append({"method": method, "params": dict(params)})
        kept = {k: (REDACTED if k in SECRET_PARAMS else v) for k, v in params.items()}
        self.records.append({"kind": "client-request", "method": method, "params": kept})
        self.logs.append("sent %s type=%s" % (method, params.get("type")))

    def response(self, method, result):
        secrets = {result.get(k) for k in SECRET_RESULTS if result.get(k)}
        self._in_flight |= secrets
        kept = {k: (REDACTED if k in SECRET_RESULTS else v) for k, v in result.items()}
        self.records.append({"kind": "response", "method": method, "result": kept})

    def error(self, method, text):
        clean = redact_text(text, self._in_flight | set(CANARIES))
        self.errors.append({"method": method, "text": clean})
        self.logs.append("error %s: %s" % (method, clean))

    def release(self):
        """CR-1: after the frame is written, nothing keeps the secret."""
        self._in_flight = set()
        self.display = []

    def durable_text(self, extra=()):
        parts = [repr(self.records), repr(self.logs), repr(self.errors)]
        parts.extend(repr(x) for x in extra)
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# App, homes, entries and conversations (§2-§6; K-2, K-3, K2-1)
# ---------------------------------------------------------------------------
ENTRY_HOME = {"chatgpt-account": "account", "api-key": "api-key", "local-provider": "account"}
CLASS = {"chatgpt-account": "user-chosen cloud", "api-key": "user-chosen cloud",
         "local-provider": "local model server"}
NO_MODEL = "run not started — no model selected"


class App:
    def __init__(self):
        self.rec = Recorder()
        self.children = {"account": {"generation": 1, "state": "ready"}}  # H-key only with a key
        self.account = Machine("AE")
        self.key = Machine("KE")
        self.local = {}
        self.thread_starts = []      # (home, params) handed to DEL-01-01 S-4
        self.last_choice = {}        # project -> (entryId, providerId, model)
        self._login = None
        self._threads = 0

    # -- account (Q-2, Q-4) --
    def read_account(self, kind):
        self.account.apply({"null": "read:null", "chatgpt": "read:chatgpt"}.get(kind, "read:other-kind"))

    def sign_in_browser(self):
        self.account.apply("person:sign-in")
        self.rec.client_request("account/login/start", {"type": "chatgpt"})
        self._login = "login-1"
        self.rec.response("account/login/start", {"type": "chatgpt", "loginId": self._login, "authUrl": URL_CANARY})
        self.rec.display.append(URL_CANARY)  # opened in the system browser (CR-3)

    def sign_in_device(self):
        self.account.apply("person:sign-in")
        self.rec.client_request("account/login/start", {"type": "chatgptDeviceCode"})
        self._login = "login-2"
        self.rec.response("account/login/start", {"type": "chatgptDeviceCode", "loginId": self._login,
                                                  "verificationUrl": VURL_CANARY, "userCode": CODE_CANARY})
        self.rec.display += [VURL_CANARY, CODE_CANARY]

    def login_completed(self, login_id, success):
        if login_id != self._login:
            self.rec.logs.append("login/completed for a sign-in the App did not start (AR-1)")
            return None
        rid = self.account.apply("completed:success" if success else "completed:failure")
        self.rec.release()
        return rid

    # -- API key (Q-6, Q-7; K2-1) --
    def enter_key(self, key, outcome="ok", echo_in_error=False):
        self.key.apply("person:enter-key")
        if "api-key" not in self.children:
            self.children["api-key"] = {"generation": 1, "state": "ready"}
        self.rec.client_request("account/login/start", {"type": "apiKey", "apiKey": key})
        if outcome == "ok":
            self.rec.response("account/login/start", {"type": "apiKey"})
            self.key.apply("login:ok")
        elif outcome == "error":
            text = "invalid api key %s" % key if echo_in_error else "login failed"
            self.rec.error("account/login/start", text)
            self.key.apply("login:error")
        elif outcome == "exit":
            self.key.apply("generation:closed")   # never re-sent (CR-6)
        self.rec.release()

    # -- local providers (Q-8) --
    def configure_local(self, pid, needs_credential=False):
        m = self.local.setdefault(pid, Machine("LE"))
        m.apply("config:needs-credential" if needs_credential else "config:local")

    # -- entries --
    def entry_available(self, entry_id):
        kind = entry_id.split(":")[0]
        if kind == "chatgpt-account":
            return self.account.state == "signed-in"
        if kind == "api-key":
            return self.key.state in ("present", "failing")
        if kind == "local-provider":
            m = self.local.get(entry_id.split(":", 1)[1])
            return bool(m) and m.state in ("listed", "in-use", "failing")
        return False

    def new_conversation(self, project):
        return Conversation(self, project)

    def start_thread(self, conv):
        kind = conv.selection["entryId"].split(":")[0]
        home = ENTRY_HOME[kind]
        if home not in self.children:
            return None
        params = {"modelProvider": conv.selection["providerId"], "model": conv.selection["model"]}
        self.thread_starts.append((home, params))
        self._threads += 1
        return {"threadId": "thread-%04d" % self._threads, "home": home,
                "requested": {"provider": params["modelProvider"], "model": params["model"]},
                "reported": {"provider": params["modelProvider"], "model": params["model"]}}


class Conversation:
    def __init__(self, app, project):
        self.app = app
        self.project = project
        self.m = Machine("CS")
        self.selection = None
        self.offer = None
        self.thread = None
        self.refusal = None
        self.sent = []
        self.drafts = []
        if project in app.last_choice:
            e, p, mod = app.last_choice[project]
            self.offer = {"entryId": e, "model": mod, "label": "your last choice for this project",
                          "applied": False, "_provider": p}
            self.m.apply("app:last-choice-exists")

    def choose(self, entry_id, provider_id, model, source="person"):
        self.m.apply("person:choose")
        self.selection = {"entryId": entry_id, "providerId": provider_id, "model": model,
                          "source": source, "chosenAt": "2026-10-01T12:00:00Z"}
        self.offer = None
        self.app.last_choice[self.project] = (entry_id, provider_id, model)

    def accept_offer(self):
        self.m.apply("person:accept-offer")
        o = self.offer
        self.selection = {"entryId": o["entryId"], "providerId": o["_provider"], "model": o["model"],
                          "source": "offered-last-choice-accepted", "chosenAt": "2026-10-01T12:00:00Z"}
        self.offer = None

    def message(self, text, start_outcome="ok"):
        s = self.m.state
        if s in ("no-selection", "offer-shown"):
            self.m.apply("person:message")
            self.drafts.append(text)
            self.refusal = {"reason": "no-model-selected", "text": NO_MODEL}
            return "refused"
        if s == "entry-unavailable":
            self.m.apply("person:message")
            self.refusal = {"reason": "entry-unavailable", "text": "the chosen access is unavailable"}
            return "refused"
        if s in ("selected", "start-failed"):
            if not self.app.entry_available(self.selection["entryId"]):
                self.m.apply("entry:unavailable") if s == "selected" else None
                self.refusal = {"reason": "entry-unavailable", "text": "the chosen access is unavailable"}
                return "refused"
            self.m.apply("person:message")
            if start_outcome == "ok":
                self.thread = self.app.start_thread(self)
                self.m.apply("start:ok")
                self.refusal = None
                self.sent.append(text)
                return "started"
            self.m.apply("start:error" if start_outcome == "error" else "generation:closed")
            self.refusal = {"reason": "start-failed", "text": "the conversation did not start"}
            return "start-failed"
        if s == "started":
            self.m.apply("person:message")
            self.sent.append(text)
            return "turn"
        raise Refused(s)

    def change_entry(self, entry_id):
        self.m.apply("person:change-entry")
        self.refusal = {"reason": "entry-change-not-offered",
                        "text": "start a new conversation for another access mode"}
        return "refused"

    def entry_changed(self, available):
        if not available:
            self.m.apply("entry:unavailable")
        else:
            self.m.apply("entry:available-started" if self.thread else "entry:available-unstarted")

    def record(self):
        r = {"schema": "chirality.access-selection/v0.1", "conversation": "conv-%x" % id(self),
             "project": self.project, "state": self.m.state, "selection": self.selection}
        if self.offer:
            r["offer"] = {k: v for k, v in self.offer.items() if not k.startswith("_")}
        if self.thread:
            r["thread"] = self.thread
        if self.refusal:
            r["refusal"] = self.refusal
        return r


def state_snapshot(app):
    entries = [{"entryId": "chatgpt-account", "kind": "chatgpt-account", "state": app.account.state,
                "home": "account", "providerId": "openai", "destinationClass": CLASS["chatgpt-account"]},
               {"entryId": "api-key", "kind": "api-key", "state": app.key.state, "home": "api-key",
                "destinationClass": CLASS["api-key"]}]
    for pid, m in sorted(app.local.items()):
        if m.state == "not-offered":
            entries.append({"entryId": "other-provider:" + pid, "kind": "other-provider", "state": "not-offered",
                            "providerId": pid, "destinationClass": "not-applicable",
                            "notOfferedReason": "definition carries a credential element"})
        else:
            entries.append({"entryId": "local-provider:" + pid, "kind": "local-provider", "state": m.state,
                            "home": "account", "providerId": pid, "destinationClass": CLASS["local-provider"]})
    homes = [{"role": r, "configLink": "linked", "childState": c["state"], "generation": c["generation"]}
             for r, c in sorted(app.children.items())]
    return {"schema": "chirality.access-state/v0.1", "observedAt": "2026-10-01T12:00:00Z",
            "homes": homes, "entries": entries}


# ---------------------------------------------------------------------------
# Configuration link dry run (§5.5; decision record M-A)
# ---------------------------------------------------------------------------
def check_link(app_cfg, target):
    if os.path.islink(app_cfg):
        if os.path.realpath(app_cfg) != os.path.realpath(target):
            return "check:replaced"
        return "check:intact" if os.path.exists(target) else "check:target-gone"
    if os.path.exists(app_cfg):
        return "check:replaced"
    return "check:target-gone"


def link_case():
    """Returns (steps, touched_paths, root). Invented content only; under $TMPDIR."""
    root = tempfile.mkdtemp(prefix="chirality-d4-link-")
    person_home = os.path.join(root, "person-codex-home")
    app_home = os.path.join(root, "app-home-acct")
    probe_home = os.path.join(root, "app-home-probe")
    for d in (person_home, app_home, probe_home):
        os.makedirs(d)
    target = os.path.join(person_home, "config.toml")
    with open(target, "w") as f:
        f.write('# invented\nmodel_provider = "example_local"\n\n[model_providers.example_local]\n'
                'name = "Example"\nbase_url = "http://127.0.0.1:1/v1"\nwire_api = "responses"\n')
    app_cfg = os.path.join(app_home, "config.toml")
    m = Machine("CL")
    steps = []
    os.symlink(target, app_cfg)
    steps.append(("setup", m.apply("setup:target-exists"), m.state))
    # read through the link sees the person's settings
    steps.append(("read-through-link", "example_local" in open(app_cfg).read(), m.state))
    # write A: explicit filePath = resolved target (Q-8 step 3)
    with open(os.path.realpath(app_cfg), "a") as f:
        f.write('\n[model_providers.example_local2]\nname = "Example 2"\n'
                'base_url = "http://127.0.0.1:2/v1"\nwire_api = "responses"\n')
    ev = check_link(app_cfg, target)
    steps.append(("write-explicit-target", m.apply(ev), m.state))
    # write B: a writer that replaces the file at the link path (temp + rename)
    tmp = os.path.join(app_home, ".config.toml.tmp")
    with open(tmp, "w") as f:
        f.write(open(app_cfg).read() + '\n# written by replacement at the link path\n')
    os.replace(tmp, app_cfg)
    ev = check_link(app_cfg, target)
    steps.append(("write-by-replacement", m.apply(ev), m.state))
    diverged = open(app_cfg).read() != open(target).read()
    steps.append(("diverged-and-both-kept", diverged and os.path.exists(target), m.state))
    # person re-links: the divergent file is kept as a dated backup (CL-7)
    backup = app_cfg + ".backup-2026-10-01"
    os.replace(app_cfg, backup)
    os.symlink(target, app_cfg)
    steps.append(("person-relink", m.apply("person:relink"), m.state))
    steps.append(("backup-kept", os.path.exists(backup), m.state))
    steps.append(("probe-home-separate", len({os.path.realpath(p) for p in (person_home, app_home, probe_home)}) == 3, m.state))
    touched = []
    for dp, dns, fns in os.walk(root):
        for n in dns + fns:
            touched.append(os.path.join(dp, n))
    return steps, touched, root


# ---------------------------------------------------------------------------
# Network view (§9; K-12)
# ---------------------------------------------------------------------------
LIMITS = ("lower bound: connections shorter than the sampling interval may be missing; "
          "host names only where the expected list or a lookup supplies them")

# Expected list at 0.158.0 from OBS-1 §8 and B.5 (destinations by name; the
# settings column waits for OBS-2 O-7).
EXPECTED_0158 = [
    {"host": "chatgpt.com", "process": "codex", "purpose": "remote-control", "setting": "features.remote_control"},
    {"host": "chatgpt.com", "process": "codex", "purpose": "plugins-featured", "setting": "features.plugins"},
    {"host": "github.com", "process": "git", "purpose": "plugin-sync", "setting": "features.plugins"},
]


def network_view(observed, o7_settled=None, home="account", generation=1):
    """observed: list of dicts {address, port, process, phase, host_hint}; host_hint matches the
    expected list only when the sampling tool supplied a name (never inferred from an address)."""
    o7_settled = o7_settled or {}
    rows, matched = [], set()
    for ob in observed:
        exp = None
        for i, e in enumerate(EXPECTED_0158):
            if ob.get("host_hint") == e["host"] and ob["process"] == e["process"] and i not in matched:
                exp = (i, e)
                break
        if exp:
            i, e = exp
            matched.add(i)
            state = o7_settled.get(e["setting"], "pending-observation")
            rows.append({"destination": {"host": e["host"], "hostSource": "expected-list",
                                         "address": ob["address"], "port": ob["port"]},
                         "process": ob["process"], "phase": ob["phase"], "purpose": e["purpose"],
                         "sources": ["app-observed", "expected-at-pin"],
                         "appSetting": {"name": e["setting"], "state": state}})
        elif ob.get("model"):
            rows.append({"destination": {"host": None, "hostSource": "none", "address": ob["address"],
                                         "port": ob["port"]},
                         "process": ob["process"], "phase": "turn", "purpose": "model",
                         "sources": ["app-observed"], "appSetting": {"state": "not-applicable"}})
        else:
            rows.append({"destination": {"host": None, "hostSource": "none", "address": ob["address"],
                                         "port": ob["port"]},
                         "process": ob["process"], "phase": ob["phase"], "purpose": "unlisted",
                         "sources": ["app-observed"], "appSetting": {"state": "no-setting-known"}})
    for i, e in enumerate(EXPECTED_0158):
        if i not in matched:
            rows.append({"destination": {"host": e["host"], "hostSource": "expected-list", "address": None,
                                         "port": 443},
                         "process": e["process"], "phase": "start-up", "purpose": e["purpose"],
                         "sources": ["expected-at-pin"],
                         "appSetting": {"name": e["setting"],
                                        "state": o7_settled.get(e["setting"], "pending-observation")}})
    return {"schema": "chirality.access-network/v0.1", "pin": "0.158.0", "home": home,
            "generation": generation, "remoteControlStatus": "connecting", "limits": LIMITS, "rows": rows}
