#!/usr/bin/env python3
"""DEL-02-04 design prototype: guidance store, composition, supply records,
child-role configuration, limit account, delegation observation and the
conversation role-selection state machine of ROLE-v0.2.

Prototype only (ROLE-v0.2 §10; R17-1, R12-3). Not product code. Python 3
standard library only. No Codex process is started; the supplier is a test
double (SupplierDouble) that answers in the shapes of the 0.158.0 generated
types and with the behaviour OBS-2 and OBS-3 observed at 0.158.0 (resume and
fork accept new instructions and ignore them); nothing more.
"""
import hashlib
import json
import os
import shutil

ROLES = ("HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK")
ID_METHOD = "chirality.app.exact-bytes.sha256/v1"
COMPOSITION_FORMAT = "chirality.role.compose/0.2"
GUIDANCE_FILES = ["AGENTS.md"] + ["agents/AGENT_%s.md" % r for r in ROLES]
CHILD_KEY_SUFFIXES = ("description", "config_file")


class SupplyRefused(Exception):
    def __init__(self, reason, detail=""):
        Exception.__init__(self, "%s %s" % (reason, detail))
        self.reason = reason


class IllegalTransition(Exception):
    pass


def cid(data):
    return {"method": ID_METHOD, "value": hashlib.sha256(data).hexdigest()}


# ------------------------------------------------------------------ role set (§4.1)
class RoleSet:
    """The App's bundled, read-only role set (roles.json). Exactly the four roles."""

    def __init__(self, bundled_dir):
        path = os.path.join(bundled_dir, "roles.json")
        with open(path, "rb") as fh:
            raw = fh.read()
        self.identity = cid(raw)
        data = json.loads(raw.decode("utf-8"))
        names = [r["role"] for r in data["roles"]]
        if sorted(names) != sorted(ROLES) or len(names) != 4:
            raise SupplyRefused("role-set-invalid", "roles %r" % names)
        defaults = [r["role"] for r in data["roles"] if r.get("default_for_new_chat")]
        if len(defaults) > 1:
            raise SupplyRefused("role-set-invalid", "more than one default")
        self.default = defaults[0] if defaults else None
        self.by_role = {r["role"]: r for r in data["roles"]}


# ------------------------------------------------------------------ guidance store (§4.2, T-1)
class GuidanceStore:
    """Bundled defaults seeded into an editable copy in the App's data folder (K-9)."""

    def __init__(self, bundled_dir, app_data_dir, release):
        self.bundled = bundled_dir
        self.root = os.path.join(app_data_dir, "instructions")
        self.release = release
        self.seed_path = os.path.join(self.root, ".seed-record.json")

    def _bundled_bytes(self, rel):
        with open(os.path.join(self.bundled, rel), "rb") as fh:
            return fh.read()

    def seed(self):
        """Seed absent files only (exclusive create); never overwrite. Returns paths seeded."""
        seeded = []
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        record = self._seed_record()
        for rel in GUIDANCE_FILES:
            dest = os.path.join(self.root, rel)
            data = self._bundled_bytes(rel)
            try:
                with open(dest, "xb") as fh:
                    fh.write(data)
                seeded.append(rel)
                record["files"][rel] = cid(data)["value"]
            except FileExistsError:
                record["files"].setdefault(rel, cid(data)["value"])
        record["release"] = record.get("release") or self.release
        self._write_seed_record(record)
        return seeded

    def _seed_record(self):
        try:
            with open(self.seed_path, "rb") as fh:
                return json.loads(fh.read().decode("utf-8"))
        except FileNotFoundError:
            return {"release": None, "files": {}}

    def _write_seed_record(self, record):
        tmp = self.seed_path + ".tmp"
        with open(tmp, "wb") as fh:
            fh.write(json.dumps(record, sort_keys=True).encode("utf-8"))
        os.replace(tmp, self.seed_path)

    def state(self, rel):
        p = os.path.join(self.root, rel)
        if not os.path.exists(p):
            return "missing"
        try:
            with open(p, "rb") as fh:
                data = fh.read()
        except OSError:
            return "unreadable"
        return "default" if cid(data)["value"] == cid(self._bundled_bytes(rel))["value"] else "modified"

    def read(self, rel):
        """Read once; refuse rather than fall back (§4.2 GS-5)."""
        p = os.path.join(self.root, rel)
        if os.path.islink(p):
            raise SupplyRefused("guidance-file-unreadable", rel + " is a symbolic link")
        try:
            with open(p, "rb") as fh:
                data = fh.read()
        except FileNotFoundError:
            raise SupplyRefused("guidance-file-missing", rel)
        except OSError as e:
            raise SupplyRefused("guidance-file-unreadable", "%s %s" % (rel, e))
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            raise SupplyRefused("guidance-not-utf8", rel)
        src = {"store": "seeded-copy", "path": rel, "release": self._seed_record().get("release") or self.release,
               "state": "default" if cid(data) == cid(self._bundled_bytes(rel)) else "modified",
               "defaultContent": cid(self._bundled_bytes(rel))}
        return data, src

    def restore(self, rel):
        p = os.path.join(self.root, rel)
        tmp = p + ".restore.tmp"
        with open(tmp, "wb") as fh:
            fh.write(self._bundled_bytes(rel))
        os.replace(tmp, p)
        return "guidance-restored"

    def upgrade(self, new_bundled_dir, new_release):
        """A new release with new defaults (§4.2 GS-6): an unmodified copy (equal to
        the default that was seeded) takes the new default; a modified copy is kept
        and flagged. Returns [(path, action)]."""
        record = self._seed_record()
        actions = []
        for rel in GUIDANCE_FILES:
            with open(os.path.join(new_bundled_dir, rel), "rb") as fh:
                new = fh.read()
            p = os.path.join(self.root, rel)
            current = open(p, "rb").read() if os.path.exists(p) else None
            seeded = record["files"].get(rel)
            if cid(new)["value"] == seeded:
                actions.append((rel, "unchanged-default"))
            elif current is not None and cid(current)["value"] == seeded:
                tmp = p + ".upgrade.tmp"
                with open(tmp, "wb") as fh:
                    fh.write(new)
                os.replace(tmp, p)
                record["files"][rel] = cid(new)["value"]
                actions.append((rel, "release-default-applied"))
            else:
                actions.append((rel, "kept-modified; new-default-available"))
        record["release"] = new_release
        self._write_seed_record(record)
        self.bundled, self.release = new_bundled_dir, new_release
        return actions


# ------------------------------------------------------------------ composition (§5.1)
def compose(store, roleset, role):
    """Role guidance only (R19-1, R19-7): product guidance, then the role.
    Returns (composed_bytes, parts). role is one of ROLES or 'none'.
    No workflow part: a workflow is supplied per run by DEL-02-02's run-start text."""
    pieces = []
    agents, src = store.read("AGENTS.md")
    pieces.append((b"", agents, {"kind": "product-guidance", "source": src}))
    if role != "none":
        if role not in ROLES:
            raise SupplyRefused("role-set-invalid", "unknown role " + role)
        data, src = store.read(roleset.by_role[role]["guidance"])
        pieces.append((("\n\n# Active role: %s\n\n" % role).encode("utf-8"), data,
                       {"kind": "role-guidance", "role": role, "source": src}))
    out, parts = b"", []
    for sep, data, meta in pieces:
        out += sep
        meta = dict(meta)
        meta.update({"content": cid(data), "offset": len(out), "length": len(data)})
        parts.append(meta)
        out += data
    return out, parts


def verify_composition(composed, parts, total):
    """Recompute each part from its byte range, and the whole (VC-R5)."""
    problems = []
    if cid(composed) != total:
        problems.append("whole content identity differs")
    for p in parts:
        piece = composed[p["offset"]:p["offset"] + p["length"]]
        if cid(piece) != p["content"]:
            problems.append("part %s differs" % p["kind"])
    return problems


def changed_since_start(store, roleset, record):
    """§4.4 GC-1: which parts of the guidance this conversation started with
    differ from the store now. The conversation is not changed (L-2); the
    App shows 'guidance changed since this conversation started'."""
    changed = []
    for p in record["carried"]["developerInstructions"]["parts"]:
        try:
            data, _ = store.read(p["source"]["path"])
            if cid(data) != p["content"]:
                changed.append(p["source"]["path"])
        except SupplyRefused as e:
            changed.append("%s (%s)" % (p["source"]["path"], e.reason))
    return changed


# ------------------------------------------------------------------ child roles (§5.3)
def child_roles(store, roleset, parent_role, user_agent_names, out_dir, supported_at_pin=True):
    """Additive config keys for native child roles (R17-9 as amended by R18-4).
    The role file's developer_instructions replace the parent's for the child
    (OBS-2 O-4a, through an adapter), so each file carries product guidance +
    role. Never sets features.*, agents.enabled or agents.max_depth (K-10).
    user_agent_names None means config/read failed. Returns (config, entries)."""
    config, entries = {}, []
    offered = roleset.by_role[parent_role]["offersChildRoles"] if parent_role != "none" else []
    os.makedirs(out_dir, exist_ok=True)
    agents, _ = store.read("AGENTS.md")
    for role in ROLES:
        if role not in offered:
            entries.append({"role": role, "status": "not-supplied", "reason": "not-offered-by-role"})
            continue
        if not supported_at_pin:
            entries.append({"role": role, "status": "not-supplied", "reason": "mechanism-not-supported-at-pin"})
            continue
        if user_agent_names is None:   # config/read failed: never shadow what we could not see
            entries.append({"role": role, "status": "not-supplied", "reason": "user-configuration-not-read"})
            continue
        if role in user_agent_names:
            entries.append({"role": role, "status": "not-supplied", "reason": "user-configuration-defines-role"})
            continue
        data, _ = store.read(roleset.by_role[role]["guidance"])
        text = agents + ("\n\n# Active role: %s\n\n" % role).encode("utf-8") + data
        body = ("developer_instructions = %s\n" % json.dumps(text.decode("utf-8"))).encode("utf-8")
        path = os.path.join(out_dir, "%s-%s.toml" % (role, hashlib.sha256(body).hexdigest()))
        try:
            with open(path, "xb") as fh:
                fh.write(body)
        except FileExistsError:
            with open(path, "rb") as fh:
                if fh.read() != body:
                    raise SupplyRefused("guidance-file-unreadable", "child role file altered " + path)
        keys = ["agents.%s.description" % role, "agents.%s.config_file" % role]
        config[keys[0]] = "Chirality %s (%s)" % (role, roleset.by_role[role]["meaning"])
        config[keys[1]] = path
        entries.append({"role": role, "status": "supplied", "configKeys": keys, "composed": cid(text), "file": cid(body),
                        "_text": text})
    return config, entries


# ------------------------------------------------------------------ request check (§5.2)
FORBIDDEN_PARAMS = ("baseInstructions", "personality", "approvalPolicy", "approvalsReviewer", "sandbox", "multiAgentMode")


def check_request(params, method="thread/start"):
    """The role-supply part of a request. On thread/start: only developerInstructions
    and additive agents.<ROLE>.(description|config_file) config keys. On
    thread/resume and thread/fork: no instructions at all (ignored at 0.158.0,
    OBS-2 O-5, OBS-3 W-6; the App does not send what it would have to record as
    'supplied' while knowing it is not taken up). Raises SupplyRefused."""
    for k in FORBIDDEN_PARAMS:
        if k in params:
            raise SupplyRefused("forbidden-input-in-request", k)
    if method != "thread/start" and ("developerInstructions" in params or params.get("config")):
        raise SupplyRefused("forbidden-input-in-request", "instructions on " + method)
    for key in (params.get("config") or {}):
        parts = key.split(".")
        if not (len(parts) == 3 and parts[0] == "agents" and parts[1] in ROLES and parts[2] in CHILD_KEY_SUFFIXES):
            raise SupplyRefused("forbidden-input-in-request", "config key " + key)
    return True


# ------------------------------------------------------------------ supplier double
class SupplierDouble:
    """Answers thread/start, thread/resume and thread/fork in 0.158.0 shapes and
    with the observed behaviour: resume and fork ignore new instructions (OBS-2
    O-5; OBS-3 W-6); a fork keeps the source's developer text and reports
    forkedFromId. mode: 'ok' | 'no-response' | 'error'."""

    def __init__(self, mode="ok"):
        self.mode = mode
        self.n, self.in_force = 0, {}
        self.sent = []

    def call(self, method, params):
        self.n += 1
        self.sent.append((method, params))
        if self.mode == "no-response":
            return None
        if self.mode == "error":
            return {"error": {"code": -32603, "message": "invented error"}}
        if method == "thread/start":
            tid = "thr-%d" % self.n
            self.in_force[tid] = params.get("developerInstructions")
            return {"result": {"thread": {"id": tid, "agentRole": None, "forkedFromId": None}, "instructionSources": []}}
        if method == "thread/fork":
            tid = "thr-%d" % self.n
            self.in_force[tid] = self.in_force.get(params["threadId"])   # source's text kept
            return {"result": {"thread": {"id": tid, "agentRole": None, "forkedFromId": params["threadId"]}, "instructionSources": []}}
        if method == "thread/resume":
            return {"result": {"thread": {"id": params["threadId"], "agentRole": None, "forkedFromId": None}, "instructionSources": []}}
        raise ValueError(method)


# ------------------------------------------------------------------ supply (§5, §6.1)
_seq = [0]


def _sid():
    _seq[0] += 1
    return "sup:%04d" % _seq[0]


def _base(thread, trigger, method, role, preselected, roleset):
    return {"format": "chirality.role.supply", "formatVersion": "0.2", "supplyId": _sid(),
            "thread": thread, "trigger": trigger, "request": {"method": method},
            "selection": {"role": role, "preselected": preselected, "roleSet": roleset.identity},
            "adoption": "unknown"}


def start(supplier, conv_ref, store, roleset, role, preselected=False, user_agent_names=(), child_dir=None,
          generation=1, extra_params=None, continued_from=None):
    """thread/start with the role composition (the only supply of a conversation)."""
    rec = _base(conv_ref, "thread-start", "thread/start", role, preselected, roleset)
    if continued_from:
        rec["continuedFrom"] = continued_from
    try:
        composed, parts = compose(store, roleset, role)
        config, entries = ({}, [{"role": r, "status": "not-supplied", "reason": "not-offered-by-role"} for r in ROLES])
        if role != "none" and child_dir:
            config, entries = child_roles(store, roleset, role, user_agent_names if user_agent_names is None else set(user_agent_names), child_dir)
        entries = [{k: v for k, v in e.items() if not k.startswith("_")} for e in entries]
        params = {"developerInstructions": composed.decode("utf-8")}
        if config:
            params["config"] = config
        params.update(extra_params or {})
        check_request(params, "thread/start")
    except SupplyRefused as e:
        rec.update({"outcome": "refused-before-send", "refusal": e.reason})
        return rec, None
    rec["carried"] = {"compositionFormat": COMPOSITION_FORMAT,
                      "developerInstructions": {"content": cid(composed), "byteLength": len(composed), "parts": parts},
                      "baseInstructions": "not-set", "nativeChildRoles": entries}
    rec["request"].update({"requestRef": "req:%d" % (supplier.n + 1), "generation": generation})
    resp = supplier.call("thread/start", params)
    _settle(rec, resp)
    return rec, composed


def fork(supplier, source_record, generation=1):
    """A same-role copy (R19-8): thread/fork with no instructions; the fork keeps
    the source's role and guidance. Recorded as 'inherited', never 'supplied'."""
    sel = source_record["selection"]
    rec = {"format": "chirality.role.supply", "formatVersion": "0.2", "supplyId": _sid(),
           "thread": source_record["thread"], "trigger": "fork", "request": {"method": "thread/fork"},
           "selection": dict(sel, preselected=False), "inheritedFrom": source_record["supplyId"], "adoption": "unknown"}
    params = {"threadId": source_record["thread"]}
    check_request(params, "thread/fork")
    rec["request"].update({"requestRef": "req:%d" % (supplier.n + 1), "generation": generation})
    resp = supplier.call("thread/fork", params)
    _settle(rec, resp, inherited=True)
    return rec


def resume(supplier, thread):
    """Relaunch or reattach: thread/resume with no instructions; no supply record."""
    params = {"threadId": thread}
    check_request(params, "thread/resume")
    return supplier.call("thread/resume", params)


def _settle(rec, resp, inherited=False):
    if resp is None:
        rec["outcome"] = "unknown-no-response"
        rec["supplierReported"] = {"instructionSources": "not-reported"}
    elif "error" in resp:
        rec["outcome"] = "request-failed"
        rec["supplierReported"] = {"instructionSources": "not-reported"}
    else:
        r = resp["result"]
        rec["thread"] = r["thread"]["id"]
        rec["outcome"] = "inherited" if inherited else "supplied"
        rep = {"instructionSources": r["instructionSources"], "agentRole": r["thread"]["agentRole"]}
        if inherited:
            rep["forkedFromId"] = r["thread"]["forkedFromId"]
        rec["supplierReported"] = rep


# ------------------------------------------------------------------ limit account (§6.2)
def limit_account(store, roleset, release, pin="0.158.0"):
    roles = []
    for role in ROLES:
        rel = roleset.by_role[role]["guidance"]
        data, src = store.read(rel)
        limits = []
        if role == "TASK":
            if src["state"] == "default":
                limits.append({"limitId": "L-TASK-1", "statement": "A task agent does not delegate",
                               "standing": "stated-not-enforced", "presentedAs": "Stated, not enforced",
                               "basis": "DECISION-K3 K-10; stated in the shipped TASK guidance; no supplier control at 0.158.0 (multiAgentMode '@deprecated Ignored', observed-in-generated-types); a TASK-guided parent delegated (OBS-2 O-4b, through an adapter)",
                               "notEnforcement": ["approval-policy", "sandbox", "user-configuration", "depth-limit"]})
            else:
                limits.append({"limitId": "L-TASK-1", "statement": "A task agent does not delegate",
                               "standing": "unknown", "presentedAs": "Not known whether the supplied guidance states this",
                               "basis": "TASK guidance modified from the shipped default; its text is not checked"})
        limits.append({"limitId": "L-ALL-1", "statement": "Work within the brief's write targets",
                       "standing": "stated-not-enforced" if src["state"] == "default" else "unknown",
                       "presentedAs": "Stated, not enforced" if src["state"] == "default" else "Not known whether the supplied guidance states this",
                       "basis": "A brief is text; Codex sandbox and approval are the person's own settings (D3), not role enforcement",
                       "notEnforcement": ["brief-text", "worktree", "sandbox", "approval-policy"]})
        roles.append({"role": role, "meaning": roleset.by_role[role]["meaning"],
                      "delegation": roleset.by_role[role]["delegation"], "guidanceState": src["state"],
                      "guidanceContent": cid(data), "limits": limits})
    return {"format": "chirality.role.limits", "formatVersion": "0.2", "accountId": "lim:%s" % release,
            "appRelease": release, "supplierPin": pin, "roles": roles}


# ------------------------------------------------------------------ delegation observation (§6.3)
def children(notifications):
    """Children are known from completed spawnAgent items' receiverThreadIds:
    Codex sends no thread/started for a child (OBS-2 O-4). The started item has
    an empty receiver list."""
    out = {}
    for n in notifications:
        item = n["params"]["item"]
        if n["method"] == "item/completed" and item.get("type") == "collabAgentToolCall" and item.get("tool") == "spawnAgent":
            for c in item["receiverThreadIds"]:
                out[c] = item["senderThreadId"]
    return out


def role_in_force(top_level, child_parent, thread_read, supplied_child_roles):
    """top_level: thread -> role supplied at start (or 'none').
    child_parent: child -> parent (from children()).
    thread_read: child -> Thread.agentRole as read (thread/read).
    supplied_child_roles: parent -> set of roles supplied as native child roles.
    A child's role counts only if it names a child role the App supplied to its
    parent; otherwise its guidance is unknown (R18-4)."""
    out = {t: (r, "supplied-to-thread") for t, r in top_level.items() if r != "none"}
    for c, p in child_parent.items():
        r = thread_read.get(c)
        root = p
        while root in child_parent:
            root = child_parent[root]
        if r in ROLES and r in supplied_child_roles.get(root, set()):
            out[c] = (r, "native-child-role-reported")
    return out


def observe(notifications, in_force, supply_by_thread=None):
    """in_force: thread -> (role, basis). One observation per spawnAgent item id
    whose sender has TASK in force. Records; never prevents (K-10)."""
    seen, out = set(), []
    for n in notifications:
        item = n["params"]["item"]
        if item.get("type") != "collabAgentToolCall" or item.get("tool") != "spawnAgent":
            continue
        sender = item["senderThreadId"]
        role, basis = in_force.get(sender, (None, None))
        if role != "TASK" or item["id"] in seen:
            continue
        seen.add(item["id"])
        obs = {"observationId": "obs:%s" % item["id"], "limitId": "L-TASK-1", "thread": sender,
               "roleInForce": "TASK", "roleBasis": basis,
               "item": {k: item[k] for k in ("type", "id", "tool", "senderThreadId", "receiverThreadIds", "status")},
               "finding": "delegation by a task agent (stated limit, not enforced)",
               "shownIn": ["conversation", "delegation-view", "run-record"]}
        if supply_by_thread and sender in supply_by_thread:
            obs["supplyRef"] = supply_by_thread[sender]
        out.append(obs)
    return out


# ------------------------------------------------------------------ selection state machine (§3.2, T-2)
# The role is fixed for the conversation's life (DECISION-L L-2; R19-3).
T2 = {
    "draft": {"select": "draft", "clear": "draft", "send": "starting"},
    "starting": {"ok": "supplied", "error": "not-started", "no-response": "start-unknown", "refused": "supply-refused"},
    "supply-refused": {"select": "draft", "clear": "draft", "restored": "draft"},
    "not-started": {"send": "starting", "select": "not-started", "clear": "not-started"},
    "start-unknown": {"thread-read-ok": "supplied", "thread-read-absent": "not-started"},
    "supplied": {"send": "supplied", "guidance-changed": "supplied", "relaunch": "supplied"},
}


class Conversation:
    def __init__(self, roleset, role=None, preselected=None, continued_from=None, prefill=None):
        self.state = "draft"
        if role is None:
            self.role = roleset.default or "none"   # preselection from the role set (R17-9)
            self.preselected = roleset.default is not None
        else:
            self.role, self.preselected = role, bool(preselected)
        self.continued_from, self.prefill = continued_from, prefill
        self.guidance_changed = []
        self.trace = [("init", self.state, self.role)]

    def on(self, event, **kw):
        nxt = T2.get(self.state, {}).get(event)
        if nxt is None:
            raise IllegalTransition("%s --%s-->" % (self.state, event))
        if event in ("select", "clear"):
            self.role = kw.get("role", "none") if event == "select" else "none"
            self.preselected = False
        if event == "guidance-changed":
            self.guidance_changed = kw.get("parts", [])
        self.state = nxt
        self.trace.append((event, self.state, self.role))
        return nxt

    def continue_as(self, roleset, role, summary):
        """'Continue as <role>' (R19-3, R19-8): a NEW conversation, role chosen,
        the handoff summary pre-filled for the person to edit; nothing is sent.
        This conversation is unchanged."""
        if self.state != "supplied":
            raise IllegalTransition("continue-as from " + self.state)
        return Conversation(roleset, role=role, preselected=False, continued_from=self, prefill=summary)
