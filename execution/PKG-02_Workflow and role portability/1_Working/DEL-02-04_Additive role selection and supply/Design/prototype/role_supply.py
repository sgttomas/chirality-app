#!/usr/bin/env python3
"""DEL-02-04 design prototype: guidance store, composition, supply records,
child-role configuration, limit account, delegation observation and the
conversation role-selection state machine of ROLE-v0.1.

Prototype only (ROLE-v0.1 §10; R17-1, R12-3). Not product code. Python 3
standard library only. No Codex process is started; the supplier is a test
double (SupplierDouble) that answers in the shapes of the 0.158.0 generated
types (observed-in-generated-types), nothing more.
"""
import hashlib
import json
import os
import shutil

ROLES = ("HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK")
ID_METHOD = "proto-sha256-0 (illustration; HOSTING U-08 open)"
REV_METHOD = "proto-sha256-list-0 (illustration; WD U-03 open)"
COMPOSITION_FORMAT = "chirality.role.compose/0.1"
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


def package_revision(pkg_dir):
    """WD-v0.8 §6.1 RV-1..RV-5 with the illustration method of WD's prototype
    (re-implemented here, not imported). Returns a contentIdentity or raises."""
    entries = []
    for dp, dns, fns in os.walk(pkg_dir, followlinks=False):
        for name in dns + fns:
            p = os.path.join(dp, name)
            if os.path.islink(p) or not (os.path.isdir(p) or os.path.isfile(p)):
                raise SupplyRefused("revision-not-verified", "non-regular entry " + name)
        for f in fns:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, pkg_dir).replace(os.sep, "/")
            with open(p, "rb") as fh:
                entries.append((rel.encode("utf-8"), hashlib.sha256(fh.read()).hexdigest()))
    entries.sort()
    listing = "".join("%s  %s\n" % (h, r.decode("utf-8")) for r, h in entries).encode("utf-8")
    return {"method": REV_METHOD, "value": hashlib.sha256(listing).hexdigest()}


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
def compose(store, roleset, role, workflow=None):
    """Return (composed_bytes, parts). role is one of ROLES or 'none'.
    workflow: dict(tuple=..., package_dir=..., registered=bool) or None."""
    pieces = []  # (separator_bytes, data, part_meta)
    agents, src = store.read("AGENTS.md")
    pieces.append((b"", agents, {"kind": "product-guidance", "source": src}))
    if role != "none":
        if role not in ROLES:
            raise SupplyRefused("role-set-invalid", "unknown role " + role)
        rel = roleset.by_role[role]["guidance"]
        data, src = store.read(rel)
        pieces.append((("\n\n# Active role: %s\n\n" % role).encode("utf-8"), data,
                       {"kind": "role-guidance", "role": role, "source": src}))
    if workflow is not None:
        if not workflow.get("registered"):
            raise SupplyRefused("workflow-not-registered", workflow["tuple"]["name"])
        rev = package_revision(workflow["package_dir"])
        if rev != workflow["tuple"]["revision"]:
            raise SupplyRefused("revision-not-verified", workflow["tuple"]["name"])
        with open(os.path.join(workflow["package_dir"], "WORKFLOW.md"), "rb") as fh:
            data = fh.read()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            raise SupplyRefused("guidance-not-utf8", "WORKFLOW.md")
        t = workflow["tuple"]
        sep = ("\n\n# Selected workflow: %s (%s, revision %s)\n\n" % (t["name"], t["origin"], t["revision"]["value"][:12])).encode("utf-8")
        wsrc = {"workflow": t, "file": "WORKFLOW.md", "revisionVerified": True}
        if workflow.get("runRef"):
            wsrc["runRef"] = workflow["runRef"]
        pieces.append((sep, data, {"kind": "workflow", "source": wsrc}))
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


# ------------------------------------------------------------------ child roles (§5.3)
def child_roles(store, roleset, parent_role, user_agent_names, out_dir, supported_at_pin=True):
    """Additive per-thread config keys for native child roles (R17-9). Never sets
    features.*, agents.enabled or agents.max_depth (K-10). Returns (config, entries)."""
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
        entries.append({"role": role, "status": "supplied", "configKeys": keys, "composed": cid(text), "file": cid(body)})
    return config, entries


# ------------------------------------------------------------------ request check (§5.2)
FORBIDDEN_PARAMS = ("baseInstructions", "personality", "approvalPolicy", "approvalsReviewer", "sandbox", "multiAgentMode")


def check_request(params):
    """The role-supply part of a request: only developerInstructions and additive
    agents.<ROLE>.(description|config_file) config keys. Raises SupplyRefused."""
    for k in FORBIDDEN_PARAMS:
        if k in params:
            raise SupplyRefused("forbidden-input-in-request", k)
    for key in (params.get("config") or {}):
        parts = key.split(".")
        if not (len(parts) == 3 and parts[0] == "agents" and parts[1] in ROLES and parts[2] in CHILD_KEY_SUFFIXES):
            raise SupplyRefused("forbidden-input-in-request", "config key " + key)
    return True


# ------------------------------------------------------------------ supplier double
class SupplierDouble:
    """Answers thread/start, thread/resume and thread/fork in 0.158.0 shapes.
    mode: 'ok' | 'no-response' | 'error'. adopts_resume_overrides models the
    unobserved P-15 behaviour (OBS-2 O-5 pending): it only changes what the
    double later reports as in force, which the App cannot see in reality."""

    def __init__(self, mode="ok", adopts_resume_overrides=None):
        self.mode, self.adopts = mode, adopts_resume_overrides
        self.n, self.in_force = 0, {}
        self.sent = []

    def call(self, method, params):
        self.n += 1
        self.sent.append((method, params))
        if self.mode == "no-response":
            return None
        if self.mode == "error":
            return {"error": {"code": -32603, "message": "invented error"}}
        tid = params.get("threadId") or "thr-%d" % self.n
        if method == "thread/start" or method == "thread/fork":
            self.in_force[tid] = params.get("developerInstructions")
        elif method == "thread/resume" and self.adopts:
            self.in_force[tid] = params.get("developerInstructions")
        return {"result": {"thread": {"id": tid, "agentRole": None}, "instructionSources": []}}


# ------------------------------------------------------------------ supply (§5, §6.1)
_seq = [0]


def _sid():
    _seq[0] += 1
    return "sup:%04d" % _seq[0]


def supply(supplier, method, thread, store, roleset, role, preselected=False, workflow=None,
           trigger="thread-start", change_cause=None, previous=None, user_agent_names=(),
           child_dir=None, generation=1, extra_params=None):
    rec = {"format": "chirality.role.supply", "formatVersion": "0.1", "supplyId": _sid(),
           "thread": thread, "trigger": trigger, "request": {"method": method},
           "selection": {"role": role, "preselected": preselected, "roleSet": roleset.identity},
           "adoption": "unknown"}
    if previous:
        rec["previousSupply"] = previous
    if change_cause:
        rec["changeCause"] = change_cause
    try:
        composed, parts = compose(store, roleset, role, workflow)
        config, entries = ({}, [{"role": r, "status": "not-supplied", "reason": "not-offered-by-role"} for r in ROLES])
        if role != "none" and child_dir:
            config, entries = child_roles(store, roleset, role, set(user_agent_names), child_dir)
        params = {"developerInstructions": composed.decode("utf-8")}
        if config:
            params["config"] = config
        if method != "thread/start":
            params["threadId"] = thread
        params.update(extra_params or {})
        check_request(params)
    except SupplyRefused as e:
        rec.update({"outcome": "refused-before-send", "refusal": e.reason})
        return rec, None
    rec["carried"] = {"compositionFormat": COMPOSITION_FORMAT,
                      "developerInstructions": {"content": cid(composed), "byteLength": len(composed), "parts": parts},
                      "baseInstructions": "not-set", "nativeChildRoles": entries}
    rec["request"].update({"requestRef": "req:%d" % (supplier.n + 1), "generation": generation})
    resp = supplier.call(method, params)
    if resp is None:
        rec["outcome"] = "unknown-no-response"
        rec["supplierReported"] = {"instructionSources": "not-reported"}
    elif "error" in resp:
        rec["outcome"] = "request-failed"
        rec["supplierReported"] = {"instructionSources": "not-reported"}
    else:
        r = resp["result"]
        rec["thread"] = r["thread"]["id"]
        rec["outcome"] = "supplied"
        rec["supplierReported"] = {"instructionSources": r["instructionSources"], "agentRole": r["thread"]["agentRole"]}
    return rec, composed


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
                               "basis": "DECISION-K3 K-10; stated in the shipped TASK guidance; no supplier control at 0.158.0 (multiAgentMode '@deprecated Ignored', observed-in-generated-types)",
                               "notEnforcement": ["approval-policy", "sandbox", "user-configuration"]})
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
    return {"format": "chirality.role.limits", "formatVersion": "0.1", "accountId": "lim:%s" % release,
            "appRelease": release, "supplierPin": pin, "roles": roles}


# ------------------------------------------------------------------ delegation observation (§6.3)
def observe(notifications, role_in_force, supply_by_thread=None):
    """role_in_force: thread -> (role, basis). One observation per spawnAgent item
    id whose sender thread is a TASK thread. Records; never prevents (K-10)."""
    seen, out = set(), []
    for n in notifications:
        item = n["params"]["item"]
        if item.get("type") != "collabAgentToolCall" or item.get("tool") != "spawnAgent":
            continue
        sender = item["senderThreadId"]
        role, basis = role_in_force.get(sender, (None, None))
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
# state -> event -> next state. Guards are applied by Conversation.
T2 = {
    "draft": {"select": "draft", "clear": "draft", "send": "starting"},
    "starting": {"ok": "supplied", "error": "not-started", "no-response": "start-unknown", "refused": "supply-refused"},
    "supply-refused": {"select": "draft", "clear": "draft", "restored": "draft"},
    "not-started": {"send": "starting", "select": "not-started", "clear": "not-started"},
    "start-unknown": {"thread-read-ok": "supplied", "thread-read-absent": "not-started"},
    "supplied": {"select": "change-pending", "clear": "change-pending", "guidance-changed": "change-pending",
                 "run-start": "change-pending", "run-end": "change-pending", "relaunch": "relaunched", "send": "supplied"},
    "change-pending": {"select": "change-pending", "clear": "change-pending", "guidance-changed": "change-pending",
                       "revert": "supplied", "send": "re-supplying", "relaunch": "relaunched"},
    "re-supplying": {"ok": "supplied", "ok-not-adopted-route": "change-not-applied", "error": "change-not-applied",
                     "no-response": "re-supply-unknown", "refused": "change-not-applied"},
    "re-supply-unknown": {"thread-read-ok": "supplied-unknown-guidance", "relaunch": "relaunched"},
    "supplied-unknown-guidance": {"send": "re-supplying", "relaunch": "relaunched"},
    "change-not-applied": {"send-anyway": "supplied", "new-conversation": "closed-here", "select": "change-pending",
                           "revert": "supplied"},
    "relaunched": {"send": "re-supplying"},
}


class Conversation:
    def __init__(self, roleset):
        self.state = "draft"
        self.role = roleset.default or "none"   # preselection from the role set (R17-9)
        self.preselected = roleset.default is not None
        self.pending = None
        self.trace = [("init", self.state, self.role)]

    def on(self, event, **kw):
        nxt = T2.get(self.state, {}).get(event)
        if nxt is None:
            raise IllegalTransition("%s --%s-->" % (self.state, event))
        if event in ("select", "clear"):
            new_role = kw.get("role", "none") if event == "select" else "none"
            if self.state in ("draft", "not-started", "supply-refused"):
                self.role, self.preselected = new_role, False
            else:
                self.pending = new_role
        if event == "revert":
            self.pending = None
        if event in ("ok",) and self.state == "re-supplying" and self.pending is not None:
            self.role, self.pending = self.pending, None
        self.state = nxt
        self.trace.append((event, self.state, self.role))
        return nxt
