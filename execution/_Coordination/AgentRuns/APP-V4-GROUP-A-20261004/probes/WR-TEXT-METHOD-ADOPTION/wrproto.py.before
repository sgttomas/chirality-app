#!/usr/bin/env python3
"""wrproto.py - design prototype for DEL-02-02 WR-v0.1 (workspace and registration).

NOT PRODUCT CODE. A design aid under R12-3 / R17-1: it models the library, draft,
review, registration and selection rules of WORKSPACE_AND_REGISTRATION.md over
invented packages in a temporary folder, with a double for DEL-01-04's act
control, and checks that every record it produces conforms to
../workspace-registration.schema.json. It chooses no placement, storage
library, process or service (OI-008, OI-014 stay open) and passing it
establishes no candidate, consumer, host or qualification.

Python 3 standard library only. No network. Writes only under a temporary
directory it removes. It imports, read-only, two sibling design prototypes:
  DEL-02-01 prototype/wdproto.py  - revision file set (WD 6.1 RV-1..RV-5, the
                                    illustrative digest proto-sha256-list-0),
                                    declared-part reader, WD name rule
  DEL-04-03 prototype/minischema.py - JSON Schema subset validator with a
                                    registry that resolves WD's and RS's $id

Usage:  python3 wrproto.py            run every check; exit 1 on a mismatch
"""
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
E = os.path.abspath(os.path.join(DESIGN, "..", "..", "..", ".."))
WD_DIR = os.path.join(E, "PKG-02_Workflow and role portability", "1_Working",
                      "DEL-02-01_Portable workflow contract and shared allocation", "Design")
RS_DIR = os.path.join(E, "PKG-04_Human acts, autonomy and run evidence", "1_Working",
                      "DEL-04-03_Content-bound decisions and compact run records", "Design")
SCHEMA = os.path.join(DESIGN, "workspace-registration.schema.json")
VALID = os.path.join(DESIGN, "workspace-registration.valid.examples.jsonl")
INVALID = os.path.join(DESIGN, "workspace-registration.invalid.examples.json")

sys.path.insert(0, os.path.join(WD_DIR, "prototype"))
sys.path.insert(0, os.path.join(RS_DIR, "prototype"))
import wdproto  # noqa: E402
import minischema  # noqa: E402

METHOD = "proto-sha256-list-0"
NAME_RE = re.compile(r"^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
OS_FILES = {".DS_Store", "Thumbs.db", "desktop.ini", "Icon\r", ".localized"}
OS_DIRS = {".Spotlight-V100", ".Trashes", ".fseventsd", "__MACOSX"}
SIZE_LIMIT = 16 * 1024 * 1024
FILE_LIMIT = 1000
WR_ID = "urn:chirality:app-v4:del-02-02:workspace-registration:WR-v0.2"
RS_ID = "urn:chirality:app-v4:del-04-03:rs-record:0.1"
RS_PROJ_ID = "urn:local:wrproto:rs-record-projected-C-01"
CODEX_ID = "urn:local:wrproto:codex-0.158.0-v2"
GEN = os.path.join(E, "PKG-01_Native App and third-party harness integration", "1_Working",
                   "DEL-01-01_Stock Codex hosting and supplier contract", "Design", "generated", "0.158.0",
                   "json-schema", "experimental", "codex_app_server_protocol.v2.schemas.json")
FRAME = "WR-FRAME-1"
ORIGINS = ("project", "user", "bundled", "host")


def proposal_line(t):
    """WR 16.2 line 3 (R20-1; RX with R20-9; RX2 with R20-11 (2)): both agent lines name origin and name; the finished line is the run's own and comes last or just before the proposal line."""
    return ('[Chirality] When you judge this workflow finished, end the message with a line of its own "Workflow finished: %s:%s". '
            'To propose that another registered workflow runs next, end the message with a line of its own '
            '"Next workflow: <origin>:<name>", where <origin> is project, user, bundled or host; '
            'when you write both, the finished line comes just before it. '
            'The person decides; nothing ends or starts until they confirm.' % (t["origin"], t["name"]))


# R20-9: the App reads only these exact forms, each alone on its own line (trailing white space tolerated, as before)
PROPOSAL_RE = re.compile(r"^Next workflow: (project|user|bundled|host):([a-z0-9]+(?:-[a-z0-9]+)*)\s*$")
FINISHED_RE = re.compile(r"^Workflow finished: (project|user|bundled|host):([a-z0-9]+(?:-[a-z0-9]+)*)\s*$")


def rs_tuple(t):
    """WD tuple (snake_case) -> RS workflowTuple (camelCase), the one-to-one mapping of WD 3.6."""
    if t is None:
        return None
    m = {"kind": "kind", "origin": "origin", "source_root": "sourceRoot", "name": "name", "revision": "revision",
         "revision_method": "revisionMethod"}
    out = {m[k]: v for k, v in t.items() if k in m}
    if t.get("derived_from"):
        out["derivedFrom"] = rs_tuple(t["derived_from"])
    return out


def id3(kind, location, name, value):
    """WR ID-3: draft:<location>:<name>@<content identity>; L-4 adds entry:… for a library entry."""
    return "%s:%s:%s@%s" % (kind, location, name, value)


class Crash(Exception):
    """A simulated process loss between two publication steps."""


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def short(v):
    return v[:12]


# ------------------------------------------------------------------ content and hygiene
def content_identity(d):
    r = wdproto.revision(d)
    if r["status"] != "computed":
        return None, r["reason"]
    return {"method": METHOD, "value": r["value"]}, None


def hygiene(d, name):
    """WR 4.5 HY-1..HY-7 (and HY-6: declared-part findings are reported, never refusing)."""
    f, total, count = [], 0, 0
    if not NAME_RE.match(name or ""):
        f.append({"code": "HY-2 name", "detail": "folder name %r breaks WD's name rule" % name})
    for dp, dns, fns in os.walk(d, followlinks=False):
        for dn in list(dns):
            p = os.path.join(dp, dn)
            if os.path.islink(p):
                f.append({"code": "HY-3 non-regular entry", "detail": os.path.relpath(p, d)})
                dns.remove(dn)
            elif dn in OS_DIRS:
                f.append({"code": "HY-4 operating-system file", "detail": os.path.relpath(p, d)})
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, d)
            if os.path.islink(p) or not os.path.isfile(p):
                f.append({"code": "HY-3 non-regular entry", "detail": rel})
                continue
            if fn in OS_FILES or fn.startswith("._"):
                f.append({"code": "HY-4 operating-system file", "detail": rel})
            total += os.path.getsize(p)
            count += 1
    if total > SIZE_LIMIT or count > FILE_LIMIT:
        f.append({"code": "HY-5 size bound", "detail": "%d files, %d bytes" % (count, total)})
    wf = os.path.join(d, "WORKFLOW.md")
    if not os.path.isfile(wf) or os.path.islink(wf):
        f.append({"code": "HY-1 no WORKFLOW.md", "detail": "no regular WORKFLOW.md at the package root"})
        return f
    raw = open(wf, "rb").read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        f.append({"code": "HY-7 not UTF-8", "detail": "WORKFLOW.md is not UTF-8"})
        return f
    fm, _, _ = wdproto.split_front_matter(text)
    if not fm or fm.get("name") != name:
        f.append({"code": "HY-2 name", "detail": "front-matter name %r differs from folder %r" % ((fm or {}).get("name"), name)})
    return f


REFUSING = {"HY-1 no WORKFLOW.md", "HY-2 name", "HY-3 non-regular entry", "HY-4 operating-system file",
            "HY-5 size bound", "HY-7 not UTF-8"}


def declared_part_note(d, wd_schema):
    try:
        R = wdproto.read_package(d, wd_schema)
        return "declared part: %s; %d finding(s)" % (R.get("declared_part"), len(R.get("findings") or []))
    except Exception as e:  # reading never refuses registration (HY-6)
        return "declared part: not read (%s)" % type(e).__name__


def copy_regular(src, dst):
    """Copy every regular file of a package (no links followed); the caller has refused non-regular entries."""
    os.makedirs(dst, exist_ok=False)
    for dp, dns, fns in os.walk(src, followlinks=False):
        rel = os.path.relpath(dp, src)
        for dn in dns:
            os.makedirs(os.path.join(dst, rel, dn), exist_ok=True)
        for fn in fns:
            shutil.copyfile(os.path.join(dp, fn), os.path.join(dst, rel, fn))


# ------------------------------------------------------------------ libraries
class Library:
    """A project or user library under a '.chirality' folder (WR section 3, PROPOSED layout)."""

    def __init__(self, base, origin, source_root):
        self.base, self.origin, self.source_root = base, origin, source_root
        self.drafts = os.path.join(base, "workflow-drafts")
        self.slots = os.path.join(base, "workflows")
        self.store = os.path.join(base, "workflow-revisions")
        self.unrecorded = os.path.join(base, "workflow-unrecorded")
        self.ledger = os.path.join(base, "workflow-registry.jsonl")
        self.lock = os.path.join(base, "workflow-registry.lock")
        self.staging = os.path.join(base, ".workflow-staging")
        self.acts = os.path.join(base, "records", "acts.jsonl")  # RS act log; location is RS U-05's
        for p in (self.drafts, self.slots, self.store, self.staging, os.path.dirname(self.acts)):
            os.makedirs(p, exist_ok=True)

    def entries(self):
        if not os.path.exists(self.ledger):
            return []
        return [json.loads(l) for l in open(self.ledger, encoding="utf-8") if l.strip()]

    def registered(self, name):
        return sorted([e for e in self.entries() if e["outcome"] == "registered" and e["identity"]["name"] == name],
                      key=lambda e: e["sequence"])

    def latest(self, name):
        r = self.registered(name)
        return r[-1] if r else None

    def act_records(self):
        if not os.path.exists(self.acts):
            return []
        return [json.loads(l) for l in open(self.acts, encoding="utf-8") if l.strip()]

    def purpose(self):
        return "make it available in the %s library" % ("project" if self.origin == "project" else "user")


def tuple_(lib_origin, source_root, name, value=None, derived_from=None):
    t = {"kind": "workflow", "origin": lib_origin, "source_root": source_root, "name": name}
    if value:
        t["revision"], t["revision_method"] = value, METHOD
    if derived_from:
        t["derived_from"] = derived_from
    return t


def same_slot(t, lib, name):
    return t and t["origin"] == lib.origin and t["source_root"] == lib.source_root and t["name"] == name


def chain(t):
    out = []
    while t:
        out.append({k: v for k, v in t.items() if k != "derived_from"})
        t = t.get("derived_from")
    return out


# ------------------------------------------------------------------ act control double (DEL-01-04)
class ActControlDouble:
    """Stands in for DEL-01-04's App act control (K-8; EXEC CAP-1..CAP-9). The only way to capture A15 is
    person_operates(), which models a native interface event; no agent-callable path exists (CAP-4)."""

    def __init__(self, ws):
        self.ws, self.shown, self.n = ws, {}, 0

    def present(self, descriptor):
        self.shown[descriptor["descriptor_id"]] = descriptor

    def withdraw(self, descriptor_id):
        self.shown.pop(descriptor_id, None)

    def person_operates(self, descriptor_id):
        d = self.shown.get(descriptor_id)
        if d is None:
            return {"captured": False, "shown": "nothing to register: review not current"}
        if not self.ws.fresh(d["review_ref"]):
            self.withdraw(descriptor_id)
            return {"captured": False, "shown": "changed since review - review again"}
        lib = self.ws.lib_of(d["subject"])
        self.n += 1
        rd = d["relations"]["reviewed_draft"]
        cap = "cap:%s" % descriptor_id
        t = self.ws.tick()
        body = {"actKind": "A15", "actClass": {"value": "person's act (V4-WF-02)"},
                "decisionActor": {"displayName": "Engineer A", "osAccount": "enga", "identityVerified": False},
                "recordingMode": "direct capture",
                "boundSubject": ["workflow revision %s:%s@%s" % (d["subject"]["origin"], d["subject"]["name"],
                                                                  short(d["subject"]["revision"]))],
                "boundContent": [{"method": METHOD, "value": d["bound_content"]["value"]}],
                "scope": d["scope"], "purpose": d["purpose"],
                "captureEvidence": [{"kind": "capture evidence", "ref": cap, "resolutionAtWrite": "resolved"}],
                "captureTime": t, "evidenceLimits": ["identity not verified"],
                # C-01 (R18-1): the persisted A15 form RS defines (FR-06), written through the RS writer.
                "relations": {"reviewedDraft": {"draft": id3("draft", rd["draft"]["draft_location"], rd["draft"]["name"],
                                                             rd["content"]["value"]),
                                                "content": {"method": METHOD, "value": rd["content"]["value"]}},
                              "priorRevision": rs_tuple(d["relations"]["prior_revision"])}}
        return self._write(lib, body, t, cap, descriptor_id, d["bound_content"])

    def _write(self, lib, body, t, cap, descriptor_id, bound):
        rid = "rec:app:acts:%04d" % (len(lib.act_records()) + 1)
        rec = {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": rid, "kind": "human_act",
               "recorder": {"role": "App interface (capturing surface)", "identity": "app-interface:local"},
               "context": {"surface": "App"}, "seq": len(lib.act_records()) + 1, "writtenAt": "w-" + t, "body": body}
        with open(lib.acts, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        self.ws.rs_records.append(rec)
        self.withdraw(descriptor_id)
        return {"captured": True, "record_id": rid, "capture_evidence": cap, "descriptor_id": descriptor_id,
                "bound_content": bound, "time": t}

    def person_operates_multi(self, descriptor_id):
        """L-4: one A15 binding several library entries in place; refused if any entry changed since review."""
        d = self.shown.get(descriptor_id)
        if d is None:
            return {"captured": False, "shown": "nothing to register: review not current"}
        if not self.ws.fresh_multi(d["review_ref"]):
            self.withdraw(descriptor_id)
            return {"captured": False, "shown": "an entry changed since review - review again"}
        lib = self.ws.reviews[d["review_ref"]]["lib"]
        t = self.ws.tick()
        cap = "cap:%s" % descriptor_id
        body = {"actKind": "A15", "actClass": {"value": "person's act (V4-WF-02)"},
                "decisionActor": {"displayName": "Engineer A", "osAccount": "enga", "identityVerified": False},
                "recordingMode": "direct capture",
                "boundSubject": ["workflow revision %s:%s@%s" % (e["subject"]["origin"], e["subject"]["name"],
                                                                   short(e["subject"]["revision"])) for e in d["entries"]],
                "boundContent": [{"method": METHOD, "value": e["bound_content"]["value"]} for e in d["entries"]],
                "scope": d["scope"], "purpose": d["purpose"],
                "captureEvidence": [{"kind": "capture evidence", "ref": cap, "resolutionAtWrite": "resolved"}],
                "captureTime": t, "evidenceLimits": ["identity not verified"],
                # RS-v0.9's shape for several entries (F-C, in progress): relations.registeredEntries
                "relations": {"registeredEntries": [
                    {"subject": "workflow revision %s:%s@%s" % (e["subject"]["origin"], e["subject"]["name"],
                                                                 short(e["subject"]["revision"])),
                     "reviewedDraft": {"draft": e["reviewed_entry"],
                                       "content": {"method": METHOD, "value": e["bound_content"]["value"]}},
                     "priorRevision": None} for e in d["entries"]]}}
        return self._write(lib, body, t, cap, descriptor_id, [e["bound_content"] for e in d["entries"]])


# ------------------------------------------------------------------ the workspace
class Workspace:
    def __init__(self, root, wd_schema):
        self.root, self.wd_schema, self.clock = root, wd_schema, 0
        self.libs = {}
        self.bundled = {}      # name -> (dir, tuple)
        self.shipped = {}      # name -> [tuple, ...]  every revision a release shipped (L-4 manifest, PROPOSED)
        self.host = {}         # name -> (dir, tuple, holding library)
        self.bases = {}        # (draft_root, name) -> tuple   App-kept (R17-4)
        self.reviews = {}
        self.records = []      # every WR record produced
        self.rs_records = []
        self.selections = []
        self.acts = ActControlDouble(self)
        self.attempts = {}     # App-kept attempt journal (review id -> state)

    def tick(self):
        self.clock += 1
        return "t%03d" % self.clock

    def emit(self, rec):
        self.records.append(rec)
        return rec

    def add_lib(self, key, origin, source_root):
        self.libs[key] = Library(os.path.join(self.root, key, ".chirality"), origin, source_root)
        return self.libs[key]

    def lib_of(self, t):
        for lib in self.libs.values():
            if lib.origin == t["origin"] and lib.source_root == t["source_root"]:
                return lib
        raise KeyError(t["source_root"])

    def key(self, lib, name):
        return {"draft_location": lib.origin, "draft_root": lib.source_root, "name": name}

    # -------------------------------------------------------------- drafts
    def transition(self, lib, name, event, frm, to, cause, attribution, content=None, disposition=None, extra=None):
        r = {"record_kind": "draft_transition", "event": event, "draft": self.key(lib, name), "from": frm, "to": to,
             "cause": cause, "time": self.tick(), "attribution": attribution}
        r.update(extra or {})
        if content:
            r["content"] = content
        if disposition:
            r["disposition"] = disposition
        return self.emit(r)

    def agent_writes_draft(self, lib, name, files, thread="thr-1"):
        d = os.path.join(lib.drafts, name)
        existed = os.path.isdir(d)
        os.makedirs(d, exist_ok=True)
        for rel, text in files.items():
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(text)
        ci, _ = content_identity(d)
        self.transition(lib, name, "changed" if existed else "written", "draft" if existed else "absent", "draft",
                        "files written in the drafts folder", {"kind": "file change item", "thread": thread,
                                                               "item": "item-%d" % self.clock}, ci)
        return d

    def draft_from(self, src_dir, base, lib, name):
        """App action: copy a registered (or host-listed, or bundled) revision into a new draft and record its
        base (SP-3). Refused if a draft of that name exists."""
        d = os.path.join(lib.drafts, name)
        if os.path.exists(d):
            return None, "a draft named %s already exists" % name
        copy_regular(src_dir, d)
        self.bases[(lib.source_root, name)] = base
        ci, _ = content_identity(d)
        self.transition(lib, name, "written", "absent", "draft", "draft made from %s:%s" % (base["origin"], base["name"]),
                        {"kind": "app action"}, ci)
        return d, None

    def review_to_register(self, lib, name):
        """App action on library content without a registration record (LS-2) or a changed published copy
        (LS-3): copy it into a draft. Base: none for LS-2; the latest registered revision for LS-3."""
        d = os.path.join(lib.drafts, name)
        if os.path.exists(d):
            return None, "a draft named %s already exists" % name
        copy_regular(os.path.join(lib.slots, name), d)
        latest = lib.latest(name)
        if latest:
            self.bases[(lib.source_root, name)] = latest["identity"]
        ci, _ = content_identity(d)
        self.transition(lib, name, "written", "absent", "draft", "library content copied for review",
                        {"kind": "app action"}, ci)
        return d, None

    def draft_reference(self, lib, name, state=None):
        d = os.path.join(lib.drafts, name)
        ci, why = content_identity(d)
        fnd = hygiene(d, name)
        base = self.bases.get((lib.source_root, name))
        if state is None:
            state = "not valid" if any(x["code"] in REFUSING for x in fnd) else "draft"
        nfiles = sum(len(f) for _, _, f in os.walk(d))
        r = {"record_kind": "draft_reference", "draft": self.key(lib, name), "state": state,
             "content": ci if ci else {"not_established": why}, "file_count": nfiles,
             "base": base, "base_recorded_by": "app" if base else "none", "findings": fnd, "observed_at": self.tick()}
        return self.emit(r)

    # -------------------------------------------------------------- dispositions (WR 4.1)
    def slot_content(self, lib, name):
        p = os.path.join(lib.slots, name)
        if not os.path.isdir(p):
            return None
        ci, _ = content_identity(p)
        return ci

    def disposition(self, lib, name, content, base):
        regs = lib.registered(name)
        slot = self.slot_content(lib, name)
        latest = regs[-1] if regs else None
        if latest and any(e["identity"]["revision"] == content["value"] for e in regs):
            seq = [e["sequence"] for e in regs if e["identity"]["revision"] == content["value"]][0]
            return "refused: identical content", latest, "identical to revision %d of this slot; select it instead" % seq
        if not regs and slot is not None:
            if slot["value"] == content["value"]:
                return "in place", None, "registers the library content already in this slot (no registration record yet)"
            return "refused: name taken", None, ("A workflow named %s is in this library without a registration record. "
                                                 "Choose a new name for the draft." % name)
        if not regs:
            return "new workflow", None, "registers a new workflow %s:%s" % (lib.origin, name)
        made_from = base is not None and any(same_slot(t, lib, name) and any(
            e["identity"]["revision"] == t.get("revision") for e in regs) for t in chain(base))
        if made_from:
            return "new revision", latest, "registers revision %d of %s:%s; earlier revisions are kept" % (
                latest["sequence"] + 1, lib.origin, name)
        return "refused: name taken", latest, ("A workflow named %s already exists in this library and this draft was "
                                               "not made from it. Choose a new name for the draft." % name)

    def same_name_elsewhere(self, lib, name):
        out = []
        for other in self.libs.values():
            if other is lib:
                continue
            for e in other.registered(name):
                out.append({"identity": e["identity"], "holding_library": other.source_root, "standing": "registered"})
        if name in self.bundled:
            out.append({"identity": self.bundled[name][1], "holding_library": "App bundle", "standing": "bundled"})
        if name in self.host:
            out.append({"identity": self.host[name][1], "holding_library": self.host[name][2], "standing": "host-listed"})
        return out

    # -------------------------------------------------------------- review (WR 4.3 RB-1..RB-7)
    def review(self, lib, name):
        rid = "rv-%d" % (len(self.reviews) + 1)
        live = os.path.join(lib.drafts, name)
        ref = self.draft_reference(lib, name)
        snap = os.path.join(lib.staging, rid, name)
        refusing = [x for x in ref["findings"] if x["code"] in REFUSING]
        base = self.bases.get((lib.source_root, name))
        target = {"origin": lib.origin, "source_root": lib.source_root, "name": name}
        if refusing or "not_established" in ref["content"]:
            disp, prior, msg = "refused: draft not valid", None, "the draft cannot be registered: " + "; ".join(
                x["code"] for x in refusing)
            content = ref["content"] if "value" in ref["content"] else {"method": METHOD, "value": "not established"}
        else:
            copy_regular(live, snap)
            content, _ = content_identity(snap)
            again, _ = content_identity(live)
            if again != content or content != ref["content"]:
                disp, prior, msg = "refused: changed since review", None, "the draft changed while it was read; review again"
            else:
                disp, prior, msg = self.disposition(lib, name, content, base)
        prior_t = prior["identity"] if prior else None
        stale = bool(prior and base and same_slot(base, lib, name) and base.get("revision") != prior["identity"]["revision"])
        if stale:
            msg += "; made from an earlier revision (not the latest): the latest revision's changes are not in it"
        rep = {"record_kind": "registration_disposition", "occasion": "registration review", "review_ref": rid,
               "target_slot": target, "reviewed": {"draft": self.key(lib, name), "content": content},
               "disposition": disp, "prior_revision": prior_t, "base": base, "lineage": chain(base) if base else [],
               "stale_base": stale, "same_name_elsewhere": self.same_name_elsewhere(lib, name),
               "findings": ref["findings"] + [{"code": "declared-part finding",
                                               "detail": declared_part_note(live, self.wd_schema)}],
               "message": msg}
        self.emit(rep)
        desc = None
        if disp in ("new workflow", "new revision", "in place"):
            subj = tuple_(lib.origin, lib.source_root, name, content["value"], base)
            desc = {"record_kind": "a15_descriptor", "descriptor_id": "a15d-%s" % rid, "act_kind": "A15",
                    "wording": "register workflow revision", "subject": subj, "bound_content": content,
                    "relations": {"reviewed_draft": {"draft": self.key(lib, name), "content": content},
                                  "prior_revision": prior_t, "derived_from": base},
                    "disposition": disp, "scope": "%s library %s" % (lib.origin, lib.source_root),
                    "purpose": lib.purpose(), "review_ref": rid,
                    "freshness": {"draft_content": content,
                                  "slot_latest": {"method": METHOD, "value": prior_t["revision"]} if prior_t else None}}
            self.emit(desc)
            self.acts.present(desc)
        self.reviews[rid] = {"lib": lib, "name": name, "snap": snap, "content": content, "disposition": disp,
                             "prior": prior_t, "descriptor": desc, "slot_at_review": self.slot_content(lib, name)}
        self.transition(lib, name, "review shown" if desc else "registration refused", "draft",
                        "under review" if desc else ref["state"], msg, {"kind": "app action"}, content, disp)
        return rid, rep, desc

    def fresh(self, rid):
        r = self.reviews[rid]
        live, _ = content_identity(os.path.join(r["lib"].drafts, r["name"]))
        latest = r["lib"].latest(r["name"])
        latest_v = latest["identity"]["revision"] if latest else None
        prior_v = r["prior"]["revision"] if r["prior"] else None
        return live == r["content"] and latest_v == prior_v

    # -------------------------------------------------------------- registration (WR 6 SQ-G)
    def _ledger_append(self, lib, entry):
        fd = os.open(lib.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)  # G-4 exclusive section
        try:
            entry["ledger_seq"] = len(lib.entries()) + 1
            with open(lib.ledger, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry) + "\n")
        finally:
            os.close(fd)
            os.remove(lib.lock)
        return self.emit(entry)

    def _not_completed(self, r, cap, reason):
        lib = r["lib"]
        e = {"record_kind": "library_entry", "ledger_seq": 0, "outcome": "not completed",
             "identity": r["descriptor"]["subject"], "prior_revision": r["prior"],
             "reviewed_draft": {"draft": self.key(lib, r["name"]), "content": r["content"]},
             "act": {"record_id": cap["record_id"], "capture_evidence": cap["capture_evidence"]},
             "reason": reason, "written_at": self.tick(), "evidence_limits": ["identity not verified"]}
        self._ledger_append(lib, e)
        self.transition(lib, r["name"], "registration not completed", "under review", "draft", reason,
                        {"kind": "app action"}, r["content"], extra={"a15_record": cap["record_id"]})   # C-02
        return {"registered": False, "reason": reason}

    def register(self, rid, cap, crash_after=None):
        r = self.reviews[rid]
        lib, name, desc = r["lib"], r["name"], r["descriptor"]
        # G-0 the capture must be this review's A15, bound to these bytes (FX-56 (c): no carried-forward act)
        if not cap or not cap.get("captured") or desc is None or cap["descriptor_id"] != desc["descriptor_id"] \
                or cap["bound_content"] != r["content"]:
            return {"registered": False, "reason": "no A15 captured for this reviewed content; the draft stays a draft"}
        self.attempts[rid] = {"state": "captured", "cap": cap}
        # G-1 the slot has not moved on since review (the act bound the prior revision)
        latest = lib.latest(name)
        if (latest["identity"]["revision"] if latest else None) != (r["prior"]["revision"] if r["prior"] else None):
            self.attempts.pop(rid)
            return self._not_completed(r, cap, "slot moved on: another revision was registered after this review")
        # G-2 exclusive reservation in the store
        key = os.path.join(lib.store, name, short(r["content"]["value"]))
        os.makedirs(os.path.dirname(key), exist_ok=True)
        try:
            os.mkdir(key)
        except FileExistsError:
            ci, _ = content_identity(os.path.join(key, name))
            if ci != r["content"]:
                self.attempts.pop(rid)
                return self._not_completed(r, cap, "store conflict at %s" % os.path.relpath(key, lib.base))
        pkg = os.path.join(key, name)
        if not os.path.isdir(pkg):
            # G-3 copy the reviewed snapshot (never the live draft) and verify
            copy_regular(r["snap"], pkg)
        ci, _ = content_identity(pkg)
        if ci != r["content"]:
            shutil.rmtree(key)
            self.attempts.pop(rid)
            return self._not_completed(r, cap, "copy verification failed")
        self.attempts[rid]["state"] = "stored"
        if crash_after == "store":
            raise Crash("after G-3, before G-4")
        return self._commit(rid)

    def _commit(self, rid):
        r = self.reviews[rid]
        lib, name, desc, cap = r["lib"], r["name"], r["descriptor"], self.attempts[rid]["cap"]
        latest = lib.latest(name)
        seq = latest["sequence"] + 1 if latest else 1
        key = os.path.join(lib.store, name, short(r["content"]["value"]), name)
        e = {"record_kind": "library_entry", "ledger_seq": 0, "outcome": "registered", "identity": desc["subject"],
             "sequence": seq, "disposition": desc["disposition"], "prior_revision": r["prior"],
             "reviewed_draft": {"draft": self.key(lib, name), "content": r["content"]},
             "act": {"record_id": cap["record_id"], "capture_evidence": cap["capture_evidence"]},
             "store_path": os.path.relpath(key, lib.base), "written_at": self.tick(),
             "evidence_limits": ["identity not verified"]}
        self._ledger_append(lib, e)                       # G-4 commit point
        self._publish_slot(lib, name, key, r)              # G-5 published copy
        self.attempts.pop(rid)
        self.bases[(lib.source_root, name)] = desc["subject"]   # the unchanged draft is now this revision's
        self.transition(lib, name, "registered", "under review", "registered, unchanged since",
                        "registered as revision %d" % seq, {"kind": "app action"}, r["content"], desc["disposition"],
                        extra={"a15_record": cap["record_id"], "revision": r["content"]["value"]})   # C-02
        return {"registered": True, "sequence": seq, "entry": e}

    def _publish_slot(self, lib, name, pkg, r):
        slot = os.path.join(lib.slots, name)
        cur = self.slot_content(lib, name)
        if cur == r["content"]:
            return None
        if cur is not None and (r["prior"] is None or cur["value"] != r["prior"]["revision"]):
            # the slot copy holds content no registration recorded: keep it, never overwrite (REQ-003)
            keep = os.path.join(lib.unrecorded, name, short(cur["value"]))
            os.makedirs(os.path.dirname(keep), exist_ok=True)
            os.rename(slot, keep)
        new = os.path.join(lib.staging, "slot-new-" + name)
        copy_regular(pkg, new)
        if os.path.isdir(slot):
            old = os.path.join(lib.staging, "slot-old-" + name)
            os.rename(slot, old)
            os.rename(new, slot)
            shutil.rmtree(old)   # a published copy of a revision that stays in the store
        else:
            os.rename(new, slot)
        return slot

    def reconcile(self):
        """SQ-X: after relaunch, finish or close attempts the journal shows as stored but not committed."""
        out = []
        for rid in list(self.attempts):
            a, r = self.attempts[rid], self.reviews[rid]
            latest = r["lib"].latest(r["name"])
            moved = (latest["identity"]["revision"] if latest else None) != (r["prior"]["revision"] if r["prior"] else None)
            if a["state"] == "stored" and not moved:
                out.append(("completed", self._commit(rid)))
            else:
                self.attempts.pop(rid)
                out.append(("not completed", self._not_completed(r, a["cap"], "interrupted, and the slot moved on")))
        return out

    # -------------------------------------------------------------- standing, listing, selection (WR 4.4, 4.6)
    def standing(self, lib, name):
        """Standing of each registered revision, plus the published copy (LS-1..LS-4)."""
        acts = {a["recordId"]: a for a in lib.act_records()}
        res = []
        for e in [x for x in lib.entries() if x["outcome"] == "registered" and x["identity"]["name"] == name]:
            a = acts.get(e["act"]["record_id"])
            pkg = os.path.join(lib.base, e["store_path"])
            ci, _ = content_identity(pkg) if os.path.isdir(pkg) else (None, None)
            ok = a is not None and any(b["value"] == e["identity"]["revision"] for b in a["body"]["boundContent"]) \
                and ci is not None and ci["value"] == e["identity"]["revision"]
            res.append((e["identity"]["revision"], "registered" if ok else "registration record incomplete"))
        slot = self.slot_content(lib, name)
        regs = {v for v, s in res}
        if slot is not None and slot["value"] not in regs:
            if not regs and any(s.get("revision") == slot["value"] for s in self.shipped.get(name, [])):
                res.append((slot["value"], "shipped revision held in this library"))     # L-4 (LS-8)
            else:
                res.append((slot["value"], "library copy changed outside registration" if regs
                            else "present without registration record"))
        return res

    def runnable(self, t):
        if t["origin"] == "bundled":
            return any(s.get("revision") == t.get("revision") and s["source_root"] == t["source_root"]
                       for s in self.shipped.get(t["name"], []))
        if t["origin"] == "host":
            return t["name"] in self.host
        lib = self.lib_of(t)
        return (t.get("revision"), "registered") in self.standing(lib, t["name"])

    def select(self, t, holding, conversation, how="explicit", candidates=None, replaces=None, prior_run=None,
               proposal=None):
        if "revision" not in t:
            return None, "a slot is not selected content: choose a revision"
        if not self.runnable(t):
            return None, "not a registered revision: review to register"
        if t["origin"] == "bundled" and holding != "App bundle":
            lib = [x for x in self.libs.values() if x.source_root == holding][0]
            if (t["revision"], "shipped revision held in this library") not in self.standing(lib, t["name"]):
                return None, "this library's copy is not the shipped revision: review to register"
        standing = {"bundled": "bundled", "host": "host-listed"}.get(t["origin"], "registered")
        if t["origin"] == "bundled" and holding != "App bundle":
            standing = "shipped revision held in this library"
        rec = {"record_kind": "selection_record", "selection_id": "sel-%d" % (len(self.selections) + 1), "identity": t,
               "holding_library": holding, "standing": standing,
               "selected_by": "the person (App interface)", "how": how, "conversation": conversation,
               "selected_at": self.tick()}
        if candidates:
            rec["candidates"] = candidates
        if replaces:
            rec["replaces"] = replaces
        if prior_run:
            rec["prior_run"] = prior_run
        if proposal:
            rec["proposal"] = proposal
        self.selections.append(rec)
        return self.emit(rec), None

    def select_draft(self, lib, name):
        return None, "draft only - not a workflow identity (register it first)"   # EXEC T-1; K-7

    def resolve(self, sel):
        """The resolver double (EXEC 6.1 resolved): bytes of the selected revision from the store, verified."""
        t = sel["identity"]
        if t["origin"] == "bundled":
            if sel["holding_library"] == "App bundle":
                pkg = self.bundled[t["name"]][0]
            else:   # L-4: the copy held in a library, recognized as the shipped revision
                lib = [x for x in self.libs.values() if x.source_root == sel["holding_library"]][0]
                pkg = os.path.join(lib.slots, t["name"])
            ci, _ = content_identity(pkg)
            return (pkg, "verified") if ci and ci["value"] == t["revision"] else (None, "revision not verified")
        lib = self.lib_of(t)
        e = [x for x in lib.registered(t["name"]) if x["identity"]["revision"] == t["revision"]]
        if not e:
            return None, "selected revision not resolvable"
        pkg = os.path.join(lib.base, e[0]["store_path"])
        ci, _ = content_identity(pkg)
        return (pkg, "verified") if ci and ci["value"] == t["revision"] else (None, "revision not verified")

    def newer_available(self, sel):
        t = sel["identity"]
        if t["origin"] not in ("project", "user"):
            return None
        latest = self.lib_of(t).latest(t["name"])
        return latest["sequence"] if latest and latest["identity"]["revision"] != t["revision"] else None

    def unqualified(self, name):
        """SL-3: candidates in order project, user, bundled, host (host last, PROPOSED)."""
        order = []
        for origin in ("project", "user"):
            for lib in self.libs.values():
                if lib.origin == origin and lib.registered(name):
                    order.append(tuple_(lib.origin, lib.source_root, name))
        if name in self.bundled:
            order.append({k: v for k, v in self.bundled[name][1].items() if k in ("kind", "origin", "source_root", "name")})
        if name in self.host:
            order.append({k: v for k, v in self.host[name][1].items() if k in ("kind", "origin", "source_root", "name")})
        return order

    def discovery(self, name):
        entries = []
        for lib in self.libs.values():
            for e in lib.registered(name):
                entries.append({"identity": e["identity"], "holding_library": lib.source_root, "standing": "registered"})
            s = self.slot_content(lib, name)
            if s and not lib.registered(name):
                entries.append({"identity": tuple_(lib.origin, lib.source_root, name, s["value"]),
                                "holding_library": lib.source_root, "standing": "present without registration record"})
        if name in self.bundled:
            entries.append({"identity": self.bundled[name][1], "holding_library": "App bundle", "standing": "bundled"})
        if name in self.host:
            entries.append({"identity": self.host[name][1], "holding_library": self.host[name][2], "standing": "host-listed"})
        origins = sorted({e["identity"]["origin"] for e in entries})
        first = entries[0]["identity"]
        rep = {"record_kind": "registration_disposition", "occasion": "discovery",
               "target_slot": {"origin": first["origin"], "source_root": first["source_root"], "name": name},
               "same_name_elsewhere": entries[1:],
               "message": "%s exists in %d origin(s): %s. Each is listed with its holding library; no selection changes."
                          % (name, len(origins), ", ".join(origins))}
        return self.emit(rep), entries

    def trial(self, lib, name, conversation):
        ci, _ = content_identity(os.path.join(lib.drafts, name))
        return self.emit({"record_kind": "trial_pointer", "draft": self.key(lib, name), "content": ci,
                          "conversation": conversation, "time": self.tick(),
                          "standing": "draft tried in conversation; not a run of any workflow identity"})

    # -------------------------------------------------------------- L-4: several entries in place, one act (WR 4.7)
    def review_entries(self, lib, names):
        rid = "rv-%d" % (len(self.reviews) + 1)
        entries, snaps = [], {}
        for n in names:
            st = self.standing(lib, n)
            if st != [(self.slot_content(lib, n)["value"], "present without registration record")]:
                return None, "%s is not library content without a registration record" % n
            if [x for x in hygiene(os.path.join(lib.slots, n), n) if x["code"] in REFUSING]:
                return None, "%s is not valid (hygiene)" % n
            snap = os.path.join(lib.staging, rid, n)
            copy_regular(os.path.join(lib.slots, n), snap)
            ci, _ = content_identity(snap)
            snaps[n] = (snap, ci)
            entries.append({"subject": tuple_(lib.origin, lib.source_root, n, ci["value"]), "bound_content": ci,
                            "reviewed_entry": id3("entry", lib.origin, n, ci["value"])})
        desc = {"record_kind": "a15_multi_descriptor", "descriptor_id": "a15m-%s" % rid, "act_kind": "A15",
                "wording": "register workflow revisions", "disposition": "in place",
                "library": {"origin": lib.origin, "source_root": lib.source_root}, "entries": entries,
                "scope": "%s library %s" % (lib.origin, lib.source_root),
                "purpose": "make them available in the %s library" % ("project" if lib.origin == "project" else "user"),
                "review_ref": rid}
        self.emit(desc)
        self.acts.present(desc)
        self.reviews[rid] = {"lib": lib, "multi": snaps, "descriptor": desc}
        return rid, desc

    def fresh_multi(self, rid):
        r = self.reviews[rid]
        return all(self.slot_content(r["lib"], n) == ci and not r["lib"].registered(n) for n, (_, ci) in r["multi"].items())

    def register_multi(self, rid, cap):
        """Per entry: G-1 (slot still the bound bytes, still unregistered), G-2/G-3 store, G-4 ledger citing the one A15."""
        r = self.reviews[rid]
        lib, desc = r["lib"], r["descriptor"]
        if not cap.get("captured") or cap["descriptor_id"] != desc["descriptor_id"]:
            return {"registered": [], "not_completed": list(r["multi"])}
        done, failed = [], []
        for e in desc["entries"]:
            n = e["subject"]["name"]
            snap, ci = r["multi"][n]
            base = {"record_kind": "library_entry", "ledger_seq": 0, "identity": e["subject"], "prior_revision": None,
                    "reviewed_entry": {"entry": e["reviewed_entry"], "content": ci},
                    "act": {"record_id": cap["record_id"], "capture_evidence": cap["capture_evidence"]},
                    "evidence_limits": ["identity not verified"]}
            if self.slot_content(lib, n) != ci or lib.registered(n):
                self._ledger_append(lib, dict(base, outcome="not completed", written_at=self.tick(),
                                              reason="entry changed after the act; review it again"))
                failed.append(n)
                continue
            key = os.path.join(lib.store, n, short(ci["value"]))
            os.makedirs(key)
            copy_regular(snap, os.path.join(key, n))
            self._ledger_append(lib, dict(base, outcome="registered", sequence=1, disposition="in place",
                                          store_path=os.path.relpath(os.path.join(key, n), lib.base),
                                          written_at=self.tick()))
            done.append(n)
        return {"registered": done, "not_completed": failed}


# ------------------------------------------------------------------ run text (R19-2, R19-7; WR section 16)
def tsha(text):
    return {"method": "sha256 over UTF-8 text", "value": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def rev12(t):
    return t["revision"][:12]


def markers(t):
    return ("<<<chirality-workflow %s@%s begin>>>" % (t["name"], rev12(t)),
            "<<<chirality-workflow %s@%s end>>>" % (t["name"], rev12(t)))


def extract_body(text, t):
    """TX-3: the bytes between the begin-marker line and the last end-marker line."""
    b, e = markers(t)
    i = text.find(b + "\n")
    j = text.rfind("\n" + e)
    if i < 0 or j < 0 or j < i:
        return None
    return text[i + len(b) + 1:j]


class RunDesk:
    """Per conversation: one run at a time (R19-2), run text composition (TX-1..TX-6), supply check (SC-1..SC-6),
    agent proposals (PR-1..PR-5). DEL-02-03 starts and ends runs; this double stands in for it where needed."""

    def __init__(self, ws):
        self.ws, self.conv, self.n = ws, {}, 0

    def state(self, c):
        return self.conv.setdefault(c, {"current": None, "history": [], "notice_pending": None})

    def compose_start(self, sel, pkg, run, c, chain, origin, folder_label):
        t = sel["identity"]
        raw = open(os.path.join(pkg, "WORKFLOW.md"), "rb").read()
        body = raw.decode("utf-8")     # HY-7: UTF-8 is a registration condition
        b, e = markers(t)
        lines = {}
        if chain:
            lines["chain_line"] = ("[Chirality] Previous workflow run ended: %s revision %s (run %s, %s). "
                                   "Its instructions no longer apply." % (chain["prior_workflow"]["name"],
                                                                         rev12(chain["prior_workflow"]),
                                                                         chain["prior_run"], chain["ended"]))
        lines["start_line"] = ('[Chirality] Workflow run start: %s from the %s library "%s", revision %s, run %s. '
                               'Follow the workflow between the two markers below for this run, until the person '
                               'ends the run.' % (t["name"], t["origin"],
                                                                  t["source_root"].replace('"', "'"), rev12(t), run))
        lines["proposal_line"] = proposal_line(t)
        others = []
        for dp, _, fns in os.walk(pkg):
            for fn in fns:
                rel = os.path.relpath(os.path.join(dp, fn), pkg).replace(os.sep, "/")
                if rel != "WORKFLOW.md":
                    others.append({"path": rel, "sha256": sha(os.path.join(dp, fn))})
        others.sort(key=lambda x: x["path"].encode("utf-8"))
        if others:
            lines["files_line"] = ('[Chirality] Other files of this revision, in the folder "%s": ' % folder_label
                                   + "; ".join("%s (sha256 %s)" % (o["path"], o["sha256"][:12]) for o in others))
        lines["begin_marker"], lines["end_marker"] = b, e
        head = [lines[k] for k in ("chain_line", "start_line", "proposal_line", "files_line", "begin_marker") if k in lines]
        text = "\n".join(head) + "\n" + body + "\n" + e
        rec = {"record_kind": "run_text", "purpose": "run start", "framing": FRAME, "run": run, "conversation": c,
               "workflow": t, "holding_library": sel["holding_library"],
               "workflow_file": {"path": "WORKFLOW.md", "content": {"method": "sha256 over UTF-8 text",
                                                                    "value": hashlib.sha256(raw).hexdigest()},
                                 "bytes": len(raw)},
               "chain": chain, "origin_of_start": origin, "selection": sel["selection_id"], "lines": lines,
               "text_identity": tsha(text), "text_bytes": len(text.encode("utf-8"))}
        if others:
            rec["other_files"] = others
        return text, rec

    def compose_end(self, prior, c):
        line = ("[Chirality] Workflow run ended: %s revision %s (run %s, %s). No workflow is in force."
                % (prior["workflow"]["name"], rev12(prior["workflow"]), prior["run"], prior["ended"]))
        rec = {"record_kind": "run_text", "purpose": "run end notice", "framing": FRAME, "run": prior["run"],
               "conversation": c, "lines": {"end_line": line}, "text_identity": tsha(line),
               "text_bytes": len(line.encode("utf-8"))}
        return line, rec

    def start(self, c, sel, pkg, person_text, origin="selected by the person", folder_label=""):
        """Returns (turn/start params, run_text record) or (None, refusal)."""
        s = self.state(c)
        if s["current"]:
            return None, "one run at a time: run %s (%s) is in force; end it first" % (
                s["current"]["run"], s["current"]["workflow"]["name"])
        self.n += 1
        run = "run:%s/%d" % (c, self.n)
        prior = s["history"][-1] if s["history"] else None
        chain = {"prior_run": prior["run"], "prior_workflow": prior["workflow"], "ended": prior["ended"]} if prior else None
        text, rec = self.compose_start(sel, pkg, run, c, chain, origin, folder_label)
        s["current"] = {"run": run, "workflow": sel["identity"], "text": text, "rec": rec}
        s["notice_pending"] = None    # TX-5: a chain line supersedes a pending end notice
        cuid = "cum:" + run
        params = {"threadId": c, "clientUserMessageId": cuid,
                  "input": [{"type": "text", "text": text, "text_elements": []}]
                  + ([{"type": "text", "text": person_text, "text_elements": []}] if person_text else [])}
        self.ws.emit(rec)
        return params, rec

    def end(self, c, how):
        s = self.state(c)
        cur = s["current"]
        s["history"].append({"run": cur["run"], "workflow": cur["workflow"], "ended": how})
        s["current"] = None
        s["notice_pending"] = s["history"][-1]

    def next_plain_turn(self, c, person_text):
        """A turn with no run start: carries the end notice first if one is pending (R19-2)."""
        s = self.state(c)
        inputs = []
        rec = None
        if s["notice_pending"]:
            line, rec = self.compose_end(s["notice_pending"], c)
            self.ws.emit(rec)
            inputs.append({"type": "text", "text": line, "text_elements": []})
            s["notice_pending"] = None
        inputs.append({"type": "text", "text": person_text, "text_elements": []})
        return {"threadId": c, "input": inputs}, rec

    # ---- supply check (SC-1..SC-6), read with thread/items/list (R21-4; HOSTING §4.4 "Recovery reads")
    def check(self, read, rec, expected_text, turn_id, cuid, now):
        """`read` answers `thread/items/list` params with one page ({data: [ThreadItemEntry], nextCursor}) or None when
        the request fails; None for `read` means no read could be made. Pages are followed to the end."""
        out = {"record_kind": "supply_check", "check": "chk-%s-%s" % (rec["run"], now), "run": rec["run"],
               "conversation": rec["conversation"], "purpose": rec["purpose"], "expected_text": rec["text_identity"],
               "read_at": now, "evidence_limits": ["supplied is not adopted: whether the model followed it is not shown"]}
        if rec["purpose"] == "run start":
            out["expected_workflow"] = rec["workflow_file"]["content"]
        if cuid:
            out["client_user_message_id"] = cuid
        if read is None:
            out["state"] = "unreadable"
            return self.ws.emit(out)
        items, cursor = [], None
        while True:
            params = {"threadId": rec["conversation"], "turnId": turn_id}
            if cursor:
                params["cursor"] = cursor
            page = read(params)
            if page is None:                  # a page could not be read: the check is incomplete
                out["state"] = "unreadable"
                return self.ws.emit(out)
            items += [e["item"] for e in page["data"] if e["turnId"] == turn_id]
            cursor = page.get("nextCursor")
            if not cursor:
                break
        if not items:
            out["state"] = "not found"
            return self.ws.emit(out)
        ums = [i for i in items if i["type"] == "userMessage"]
        um = [i for i in ums if cuid and i.get("clientId") == cuid]
        located = "client id" if um else "first user message of the turn"
        um = um or ums[:1]
        texts = [x for x in (um[0]["content"] if um else []) if x.get("type") == "text"]
        if not texts:
            out["state"] = "not found"
            return self.ws.emit(out)
        got = texts[0]["text"]
        out.update({"turn": turn_id, "item": um[0]["id"], "located_by": located, "observed_text": tsha(got)})
        if tsha(got) == rec["text_identity"]:
            out["state"] = "verified"
        else:
            body = extract_body(got, rec["workflow"]) if rec["purpose"] == "run start" else None
            same = body is not None and hashlib.sha256(body.encode("utf-8")).hexdigest() == rec["workflow_file"]["content"]["value"]
            out["state"] = "text differs, workflow bytes equal" if same else "text differs, workflow bytes differ"
        return self.ws.emit(out)

    # ---- agent proposals (PR-1..PR-5)
    def proposal_in(self, agent_text):
        """PR-1 (R20-5, R20-9, R20-11 (2)): the last non-empty line, exactly 'Next workflow: <origin>:<name>',
        appearing at most once in the message. Returns (origin, name)."""
        lines = [l for l in agent_text.split("\n") if l.strip()]
        if sum(1 for l in lines if PROPOSAL_RE.match(l)) != 1:
            return None
        m = PROPOSAL_RE.match(lines[-1]) if lines else None
        return (m.group(1), m.group(2)) if m else None

    def finished_in(self, c, agent_text):
        """FN-1 (R20-1, R20-9, R20-11 (2)): 'Workflow finished: <origin>:<name>', at most once, as the last non-empty
        line or the line immediately before the proposal line, naming the run in force by its tuple's origin and name."""
        cur = self.state(c)["current"]
        lines = [l for l in agent_text.split("\n") if l.strip()]
        if not lines or sum(1 for l in lines if FINISHED_RE.match(l)) != 1:
            return None
        cand = lines[-1]
        if self.proposal_in(agent_text) and len(lines) >= 2:
            cand = lines[-2]
        m = FINISHED_RE.match(cand)
        if m and cur and (m.group(1), m.group(2)) == (cur["workflow"]["origin"], cur["workflow"]["name"]):
            return m.group(1), m.group(2)
        return None

    def end_and_start(self, c, sel, pkg, person_text, finished=False, origin="selected by the person", folder_label=""):
        """CH-1 (R20-11 (1), (4)): the one step 'End <A> and start <B>'. A is ended by the person (DEF-4) with cause
        'ended to start <B>', or 'completed' when the person chose it on a finished report (FN-2, R20-1); then B starts."""
        cur = self.state(c)["current"]
        if not cur:
            return None, "no run in force: the offer is a plain 'Start %s'" % sel["identity"]["name"]
        self.end(c, "completed" if finished else "ended to start %s" % sel["identity"]["name"])
        return self.start(c, sel, pkg, person_text, origin=origin, folder_label=folder_label)

    def resolve_pair(self, origin, name):
        """PR-2 (RX): SL-3's candidates restricted to the named origin."""
        return [t for t in self.ws.unqualified(name) if t["origin"] == origin]

    def offers(self, c, agent_text):
        """FN-2: what the App offers after an agent message; nothing is ended or started by the words alone."""
        out = []
        cur = self.state(c)["current"]
        fin = self.finished_in(c, agent_text)
        nxt = self.proposal_in(agent_text)
        if cur and fin:
            out.append("End run")
        if nxt and len(self.resolve_pair(*nxt)) == 1:
            out.append(("End %s and start %s" % (cur["workflow"]["name"], nxt[1])) if cur else ("Start %s" % nxt[1]))
        return out

    def offer(self, pair):
        origin, name = pair
        cands = self.resolve_pair(origin, name)
        if len(cands) == 1:
            return {"offer": "Start %s" % name, "candidates": cands}
        if len(cands) > 1:
            return {"offer": None, "notice": "proposed workflow %s:%s names more than one registered workflow" % pair}
        for lib in self.ws.libs.values():
            if lib.origin == origin and os.path.isdir(os.path.join(lib.drafts, name)):
                return {"offer": None, "notice": "proposed workflow %s:%s is a draft only - not a workflow identity" % pair}
        return {"offer": None, "notice": "proposed workflow %s:%s is not registered" % pair}


# ------------------------------------------------------------------ fixtures
def e1_package_text():
    prose = open(os.path.join(WD_DIR, "prototype", "fixtures", "E1.prose.md"), encoding="utf-8").read()
    decl = json.load(open(os.path.join(WD_DIR, "workflow-declaration.valid.example.json"), encoding="utf-8"))
    return wdproto.render(decl, prose)


def simple_pkg(name, body):
    return {"WORKFLOW.md": "---\nname: %s\ndescription: %s\n---\n\n# %s\n\n%s\n" % (name, body, name, body)}


# ------------------------------------------------------------------ self-test
def main():
    results = []

    def check(cid, label, cond, got=""):
        results.append(bool(cond))
        print("%s %s %s%s" % ("PASS" if cond else "FAIL", cid, label, "" if cond else "  -> got: %r" % (got,)))

    print("wrproto.py (DEL-02-02 WR-v0.1 design prototype; not product code)")
    print("python %s" % sys.version.split()[0])
    for p in (os.path.join(WD_DIR, "prototype", "wdproto.py"), os.path.join(RS_DIR, "prototype", "minischema.py"),
              os.path.join(WD_DIR, "workflow-declaration.schema.json"), os.path.join(RS_DIR, "RS_RECORD.schema.json"),
              SCHEMA, VALID, INVALID, os.path.abspath(__file__)):
        print("  input %s sha256 %s" % (os.path.relpath(p, E), sha(p)))

    wd_schema = wdproto.load(wdproto.SCHEMA_PATH)
    reg = minischema.Registry()
    reg.add(wd_schema)                       # WD uses keywords outside minischema's subset; tuples are
    reg.load(SCHEMA)                         # cross-checked with wdproto's own validator below
    reg.load(os.path.join(RS_DIR, "RS_RECORD.schema.json"))
    wr = reg.by_id[WR_ID]
    rs = reg.by_id[RS_ID]
    wd_ident = wd_schema["$defs"]["workflow_identity"]
    # C-01 (R18-1; FR-06): RS's schema projected with the persisted A15 form, built in memory from the on-disk
    # RS schema (F-C edits RS in parallel; the on-disk outcome is printed, not judged).
    rsp = copy.deepcopy(rs)
    rsp["$id"] = RS_PROJ_ID
    ha = rsp["$defs"]["humanAct"]
    rel = ha["properties"]["relations"]["properties"]
    rel.pop("derivedFrom", None)
    one = {"type": "object", "required": ["draft", "content"], "additionalProperties": False,
           "properties": {"draft": {"type": "string", "pattern": "^(draft|entry):(project|user):[^@]+@.+$"},
                          "content": {"$ref": "#/$defs/contentIdentity"}}}
    prior = {"anyOf": [{"$ref": "#/$defs/workflowTuple"}, {"type": "null"}]}
    rel["reviewedDraft"] = one
    rel["priorRevision"] = prior
    rel["registeredEntries"] = {"type": "array", "minItems": 2, "items": {
        "type": "object", "required": ["subject", "reviewedDraft", "priorRevision"], "additionalProperties": False,
        "properties": {"subject": {"type": "string", "minLength": 1}, "reviewedDraft": one, "priorRevision": prior}}}
    a15_rule = [i for i, x in enumerate(ha.get("allOf", [])) if "A15 (" in json.dumps(x) or "R12-5" in json.dumps(x)][:1]
    new_rule = {"anyOf": [{"properties": {"actKind": {"not": {"const": "A15"}}}},
                          {"required": ["relations"], "properties": {"relations": {"anyOf": [
                              {"required": ["reviewedDraft", "priorRevision"], "not": {"required": ["registeredEntries"]}},
                              {"required": ["registeredEntries"],
                               "not": {"anyOf": [{"required": ["reviewedDraft"]}, {"required": ["priorRevision"]}]}}]}}}]}
    if a15_rule:
        ha["allOf"][a15_rule[0]] = new_rule
    else:
        ha.setdefault("allOf", []).append(new_rule)
    reg.add(rsp)
    reg.dir_of[id(rsp)] = RS_DIR
    gen = json.load(open(GEN, encoding="utf-8"))
    gen["$id"] = CODEX_ID
    reg.add(gen)

    def tuples_in(x):
        if isinstance(x, dict):
            if x.get("kind") == "workflow" and "origin" in x:
                yield x
            for v in x.values():
                yield from tuples_in(v)
        elif isinstance(x, list):
            for v in x:
                yield from tuples_in(v)

    def conforms(rec):
        errs = minischema.validate(rec, wr, reg)
        werrs = [e for t in tuples_in(rec) for e in wdproto.validate(wd_ident, t, wd_schema)]
        return errs + [str(e) for e in werrs]

    # ---- S: schema instances
    print("\n== schema conformance instances ==")
    valid = [json.loads(l) for l in open(VALID, encoding="utf-8") if l.strip()]
    kinds = set()
    for i, inst in enumerate(valid, 1):
        kinds.add(inst["record_kind"])
        check("S-1.%d" % i, "valid example %s conforms" % inst["record_kind"], not conforms(inst), conforms(inst))
    check("S-2", "valid examples cover all 10 record kinds", len(kinds) == 10, sorted(kinds))
    for c in json.load(open(INVALID, encoding="utf-8")):
        top = minischema.validate(c["instance"], wr, reg)
        sub = minischema.validate(c["instance"], {"$ref": WR_ID + "#/$defs/" + c["kind"]}, reg)
        check(c["case"].split(" ")[0], "%s: rejected (%s)" % (c["case"].split(" ", 1)[1][:64], c["expect"]),
              top and any(c["expect"] in e for e in sub), sub[:2])

    root = tempfile.mkdtemp(prefix="wrproto-")
    try:
        ws = Workspace(root, wd_schema)
        P = ws.add_lib("fx-proj", "project", "fx-proj (LIB-A1)")
        U = ws.add_lib("fx-user", "user", "user library (fx-user)")
        e1 = e1_package_text()

        print("\n== drafts and hygiene (WR 4.5; 5.1) ==")
        ws.agent_writes_draft(P, "supports-adjust", {"WORKFLOW.md": e1})
        ref = ws.draft_reference(P, "supports-adjust")
        ci_wd = wdproto.revision(os.path.join(P.drafts, "supports-adjust"))
        check("P-01", "draft content identity equals WD RV-1..RV-5 over the draft folder; base none",
              ref["content"]["value"] == ci_wd["value"] and ref["base"] is None and ref["state"] == "draft", ref["state"])
        bad = ws.agent_writes_draft(P, "bad-pkg", simple_pkg("bad-pkg", "x"))
        open(os.path.join(bad, ".DS_Store"), "wb").write(b"\0")
        os.symlink("/etc/hosts", os.path.join(bad, "link.txt"))
        r = ws.draft_reference(P, "bad-pkg")
        codes = {x["code"] for x in r["findings"]}
        check("P-02", "OS file and symbolic link make the draft not valid (HY-3, HY-4; RV-2)",
              r["state"] == "not valid" and "HY-3 non-regular entry" in codes and "HY-4 operating-system file" in codes, codes)
        ws.agent_writes_draft(P, "Bad_Name", simple_pkg("Bad_Name", "x"))
        ws.agent_writes_draft(P, "mismatch", simple_pkg("other-name", "x"))
        a, b = ws.draft_reference(P, "Bad_Name"), ws.draft_reference(P, "mismatch")
        check("P-03", "name rule and front-matter name mismatch are HY-2 findings",
              a["state"] == "not valid" and b["state"] == "not valid", (a["findings"], b["findings"]))
        rid, rep, desc = ws.review(P, "bad-pkg")
        check("P-04", "review of a not-valid draft: refused, no A15 descriptor presented",
              rep["disposition"] == "refused: draft not valid" and desc is None, rep["disposition"])

        print("\n== trial in conversation (K-7; WR 4.2) ==")
        tp = ws.trial(P, "supports-adjust", "thr-2")
        check("P-05", "a trial leaves a pointer to draft content, no workflow identity, no run",
              "identity" not in tp and tp["content"] == ref["content"], tp)
        s, why = ws.select_draft(P, "supports-adjust")
        check("P-06", "a draft cannot be selected for a run (EXEC T-1)", s is None and "draft only" in why, why)

        print("\n== review, act and registration (K-8; WR 4.1, 4.3, 6 SQ-G) ==")
        rid1, rep1, d1 = ws.review(P, "supports-adjust")
        check("P-07", "first registration: DS-1 new workflow; descriptor binds the reviewed bytes; purpose per library",
              rep1["disposition"] == "new workflow" and d1["bound_content"] == rep1["reviewed"]["content"]
              and d1["subject"]["revision"] == d1["bound_content"]["value"]
              and d1["purpose"] == "make it available in the project library", rep1["disposition"])
        out = ws.register(rid1, None)
        check("P-08", "no act captured (an agent saying 'registered'): nothing registered (FX-56 (b))",
              not out["registered"] and not P.registered("supports-adjust"), out)
        open(os.path.join(P.drafts, "supports-adjust", "WORKFLOW.md"), "a", encoding="utf-8").write("\nedited\n")
        cap = ws.acts.person_operates(d1["descriptor_id"])
        check("P-09", "draft changed after review: the act control refuses capture, asks for a new review (K-8)",
              not cap["captured"] and "review again" in cap["shown"], cap)
        rid1, rep1, d1 = ws.review(P, "supports-adjust")
        cap1 = ws.acts.person_operates(d1["descriptor_id"])
        out1 = ws.register(rid1, cap1)
        rev1 = d1["subject"]
        check("P-10", "person operates the control: A15 captured, revision 1 registered, slot copy published",
              out1["registered"] and out1["sequence"] == 1 and ws.slot_content(P, "supports-adjust")["value"] == rev1["revision"],
              out1)
        a15 = ws.rs_records[-1]
        errs = minischema.validate(a15, rsp, reg)
        print("     on-disk RS_RECORD.schema.json $defs/humanAct, for the C-01 form (information; F-C edits RS in parallel): %s"
              % (minischema.validate(a15["body"], {"$ref": RS_ID + "#/$defs/humanAct"}, reg)[:3] or "conforms"))
        check("P-11", "the A15 record, in C-01's persisted form, conforms to RS's schema projected with FR-06 (direct capture, identity not verified)",
              not errs, errs[:2])
        st = ws.standing(P, "supports-adjust")
        check("P-12", "standing LS-1 registered: ledger, A15 record and store bytes agree", st == [(rev1["revision"], "registered")], st)

        print("\n== refinements and the slot policy (K-6; WR 4.1) ==")
        store1 = os.path.join(P.base, out1["entry"]["store_path"])
        shutil.rmtree(os.path.join(P.drafts, "supports-adjust"))
        ws.bases.pop((P.source_root, "supports-adjust"), None)
        d, err = ws.draft_from(store1, rev1, P, "supports-adjust")
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write("\nRefinement 1: re-examine twice.\n")
        rid2, rep2, d2 = ws.review(P, "supports-adjust")
        cap2 = ws.acts.person_operates(d2["descriptor_id"])
        out2 = ws.register(rid2, cap2)
        rev2 = d2["subject"]
        check("P-13", "refinement 1: DS-2 new revision; prior revision = rev 1; derived_from = draft base",
              rep2["disposition"] == "new revision" and rep2["prior_revision"]["revision"] == rev1["revision"]
              and rev2["derived_from"]["revision"] == rev1["revision"] and out2["sequence"] == 2, rep2["disposition"])
        check("P-14", "earlier revision kept and still registered (nothing overwritten)",
              [s for _, s in ws.standing(P, "supports-adjust")] == ["registered", "registered"], ws.standing(P, "supports-adjust"))
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write("\nRefinement 2: name the spacing limit.\n")
        rid3, rep3, d3 = ws.review(P, "supports-adjust")
        out_old = ws.register(rid3, cap2)
        check("P-15", "rev-2's act cannot register the changed content (FX-56 (c); VER-002)",
              not out_old["registered"], out_old)
        cap3 = ws.acts.person_operates(d3["descriptor_id"])
        out3 = ws.register(rid3, cap3)
        rev3 = d3["subject"]
        check("P-16", "refinement 2 registered as revision 3 (V4-EXM-10's two refinements)",
              out3["registered"] and out3["sequence"] == 3, out3)
        rid4, rep4, d4 = ws.review(P, "supports-adjust")
        check("P-17", "re-review of unchanged content: DS-4 refused, identical to revision 3",
              rep4["disposition"] == "refused: identical content" and d4 is None, rep4["message"])
        before = {p: sha(os.path.join(dp, p)) for dp, _, fs in os.walk(P.slots) for p in fs}
        shutil.rmtree(os.path.join(P.drafts, "supports-adjust"))
        ws.bases.pop((P.source_root, "supports-adjust"), None)
        ws.agent_writes_draft(P, "supports-adjust", {"WORKFLOW.md": e1.replace("Adjust supports", "Adjust supports (fresh)")})
        rid5, rep5, d5 = ws.review(P, "supports-adjust")
        after = {p: sha(os.path.join(dp, p)) for dp, _, fs in os.walk(P.slots) for p in fs}
        check("P-18", "same-name draft with no recorded origin: DS-3 refused, asks for a new name; library bytes unchanged",
              rep5["disposition"] == "refused: name taken" and "Choose a new name" in rep5["message"] and before == after,
              rep5["message"])

        print("\n== stale base, concurrency and interruption (WR 4.1 SP-7; 6 SQ-G, SQ-X) ==")
        shutil.rmtree(os.path.join(P.drafts, "supports-adjust"))
        d, _ = ws.draft_from(store1, rev1, P, "supports-adjust")
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write("\nBranch from revision 1.\n")
        rid6, rep6, d6 = ws.review(P, "supports-adjust")
        check("P-19", "draft made from revision 1 after revision 3: DS-2 with the stale-base notice; prior = rev 3",
              rep6["disposition"] == "new revision" and rep6["stale_base"] and rep6["prior_revision"]["revision"] == rev3["revision"],
              (rep6["disposition"], rep6["stale_base"]))
        cap6 = ws.acts.person_operates(d6["descriptor_id"])
        # Before rid6 is published, a second refinement of the same slot (made from revision 3, in the same
        # drafts folder) is reviewed, acted on and registered first: the slot moves on.
        live = os.path.join(P.drafts, "supports-adjust")
        aside = os.path.join(root, "aside-branch")
        os.rename(live, aside)
        ws.bases.pop((P.source_root, "supports-adjust"), None)
        d, _ = ws.draft_from(os.path.join(P.base, out3["entry"]["store_path"]), rev3, P, "supports-adjust")
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write("\nConcurrent refinement.\n")
        ridc, repc, dc = ws.review(P, "supports-adjust")
        outc = ws.register(ridc, ws.acts.person_operates(dc["descriptor_id"]))
        out6 = ws.register(rid6, cap6)
        last = P.entries()[-1]
        check("P-20", "slot moved on between capture and publication: not completed, recorded with the act; no new revision",
              outc["registered"] and not out6["registered"] and last["outcome"] == "not completed"
              and last["act"]["record_id"] == cap6["record_id"] and len(P.registered("supports-adjust")) == 4,
              (out6, last["outcome"]))
        shutil.rmtree(aside)
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write("\nAfter the concurrent one.\n")
        rid8, rep8, d8 = ws.review(P, "supports-adjust")
        cap8 = ws.acts.person_operates(d8["descriptor_id"])
        try:
            ws.register(rid8, cap8, crash_after="store")
            crashed = False
        except Crash:
            crashed = True
        mid = [s for _, s in ws.standing(P, "supports-adjust")]
        rec = ws.reconcile()
        check("P-21", "loss after the store copy, before the ledger: not registered until relaunch reconciliation completes it with the same act",
              crashed and len(mid) == 4 and rec and rec[0][0] == "completed" and rec[0][1]["registered"]
              and P.latest("supports-adjust")["act"]["record_id"] == cap8["record_id"], (mid, rec))

        print("\n== selection, discovery and the four origins (WR 4.4; WD C-1..C-6) ==")
        rev_latest = P.latest("supports-adjust")["identity"]
        sel, why = ws.select(rev3, P.source_root, "thr-10")
        check("P-22", "selection pins revision 3 and resolves its verified store bytes",
              sel and ws.resolve(sel)[1] == "verified", why)
        check("P-23", "a later revision is offered, never followed silently (C-4 visible; PROPOSED pin)",
              ws.newer_available(sel) == P.latest("supports-adjust")["sequence"] and sel["identity"]["revision"] == rev3["revision"],
              ws.newer_available(sel))
        bdir = os.path.join(root, "bundle", "supports-adjust")
        os.makedirs(bdir)
        open(os.path.join(bdir, "WORKFLOW.md"), "w").write(e1.replace("Adjust supports", "Bundled"))
        bci, _ = content_identity(bdir)
        ws.bundled["supports-adjust"] = (bdir, tuple_("bundled", "App bundle fx-release", "supports-adjust", bci["value"]))
        hdir = os.path.join(P.base, "workflow-imports", "fx-root", "supports-adjust")
        os.makedirs(hdir)
        open(os.path.join(hdir, "WORKFLOW.md"), "w").write(e1.replace("Adjust supports", "Adjust supports (host)"))
        hci, _ = content_identity(hdir)
        host_t = tuple_("host", "fx-root", "supports-adjust", hci["value"], rev1)
        ws.host["supports-adjust"] = (hdir, host_t, "LIB-A2 (fx-app-import)")
        ws.agent_writes_draft(U, "supports-adjust", {"WORKFLOW.md": e1.replace("Adjust supports", "Adjust my supports")})
        ridu, repu, du = ws.review(U, "supports-adjust")
        ws.register(ridu, ws.acts.person_operates(du["descriptor_id"]))
        rep_d, entries = ws.discovery("supports-adjust")
        origins = sorted({e["identity"]["origin"] for e in entries})
        check("P-24", "discovery lists all four origins, each with its holding library (C-1)",
              origins == ["bundled", "host", "project", "user"] and all(e["holding_library"] for e in entries), origins)
        check("P-25", "the earlier selection is unchanged after same-name additions (C-2; AC-004)",
              ws.selections[0]["identity"] == rev3 and ws.resolve(ws.selections[0])[1] == "verified", ws.selections[0]["identity"])
        cands = ws.unqualified("supports-adjust")
        check("P-26", "an unqualified name gives candidates project, user, bundled, host and selects nothing by itself",
              [c["origin"] for c in cands] == ["project", "user", "bundled", "host"], [c["origin"] for c in cands])
        sel2, _ = ws.select(rev_latest, P.source_root, "thr-10", how="from unqualified name", candidates=cands,
                            replaces=sel["selection_id"])
        check("P-27", "following the newer revision is a new selection event citing the one it replaces (C-3)",
              sel2 and sel2["replaces"] == sel["selection_id"], sel2)
        slot = os.path.join(P.slots, "supports-adjust", "WORKFLOW.md")
        open(slot, "a").write("\nagent edit in the library copy\n")
        st = ws.standing(P, "supports-adjust")
        check("P-28", "an agent edit of the published copy: 'library copy changed outside registration'; registered revisions still verified",
              st[-1][1] == "library copy changed outside registration" and ws.resolve(sel2)[1] == "verified", st[-1])
        changed_t = tuple_("project", P.source_root, "supports-adjust", st[-1][0])
        s3, why3 = ws.select(changed_t, P.source_root, "thr-10")
        check("P-29", "the changed copy is not selectable (K-7: only registered revisions run)", s3 is None, why3)

        print("\n== library content without a record; in-place registration (WR 4.6 LS-2, DS-7) ==")
        os.makedirs(os.path.join(P.slots, "legacy-flow"))
        open(os.path.join(P.slots, "legacy-flow", "WORKFLOW.md"), "w").write(simple_pkg("legacy-flow", "v3 era")["WORKFLOW.md"])
        st = ws.standing(P, "legacy-flow")
        check("P-30", "a v3-era or agent-written library package: 'present without registration record'",
              st and st[0][1] == "present without registration record", st)
        ws.review_to_register(P, "legacy-flow")
        ridl, repl, dl = ws.review(P, "legacy-flow")
        ws.register(ridl, ws.acts.person_operates(dl["descriptor_id"]))
        check("P-31", "review to register: DS-7 in place; the slot bytes are unchanged and now registered",
              repl["disposition"] == "in place" and ws.standing(P, "legacy-flow") == [(st[0][0], "registered")],
              (repl["disposition"], ws.standing(P, "legacy-flow")))

        print("\n== host-origin refinement and bundled refinement (EXEC HR-1..HR-7, RT-6; CA section 4) ==")
        shutil.rmtree(os.path.join(P.drafts, "supports-adjust"))
        ws.bases.pop((P.source_root, "supports-adjust"), None)
        d, _ = ws.draft_from(hdir, host_t, P, "supports-adjust")
        open(os.path.join(d, "WORKFLOW.md"), "a").write("\nRefined after the host adaptation.\n")
        ridh, reph, dh = ws.review(P, "supports-adjust")
        outh = ws.register(ridh, ws.acts.person_operates(dh["descriptor_id"]))
        check("P-32", "draft based on the host tuple whose lineage reaches LIB-A1: DS-2 new revision, derived_from = host tuple, origin project",
              reph["disposition"] == "new revision" and dh["subject"]["origin"] == "project"
              and dh["subject"]["derived_from"]["origin"] == "host" and outh["registered"]
              and [t["origin"] for t in reph["lineage"]] == ["host", "project"], (reph["disposition"], reph["lineage"]))
        check("P-32b", "the agent-edited published copy (P-28) was kept aside, not overwritten, when the new revision was published",
              os.path.isdir(os.path.join(P.unrecorded, "supports-adjust")), os.listdir(P.base))
        other_host = tuple_("host", "fx-root", "supports-adjust", hci["value"])     # no derived-from recorded
        shutil.rmtree(os.path.join(P.drafts, "supports-adjust"))
        ws.bases.pop((P.source_root, "supports-adjust"), None)
        d, _ = ws.draft_from(hdir, other_host, P, "supports-adjust")
        open(os.path.join(d, "WORKFLOW.md"), "a").write("\nunrelated\n")
        ridn, repn, dn = ws.review(P, "supports-adjust")
        check("P-33", "host base whose lineage does not reach the slot: DS-3 refused, name taken",
              repn["disposition"] == "refused: name taken", repn["disposition"])
        ws.bundled["create-workflow"] = (bdir, tuple_("bundled", "App bundle fx-release", "create-workflow", bci["value"]))
        d, _ = ws.draft_from(bdir, ws.bundled["create-workflow"][1], U, "create-workflow")
        open(os.path.join(d, "WORKFLOW.md"), "w").write(simple_pkg("create-workflow", "my variant")["WORKFLOW.md"])
        ridb, repb, db = ws.review(U, "create-workflow")
        ws.register(ridb, ws.acts.person_operates(db["descriptor_id"]))
        check("P-34", "bundled workflow refined into the user library: DS-1 new workflow, derived_from bundled; shadowing listed",
              repb["disposition"] == "new workflow" and db["subject"]["derived_from"]["origin"] == "bundled"
              and any(e["standing"] == "bundled" for e in repb["same_name_elsewhere"])
              and db["purpose"] == "make it available in the user library", repb["disposition"])

        print("\n== forged ledger line; C-01 persisted form ==")
        forged = dict(P.registered("legacy-flow")[0])
        forged.update({"ledger_seq": len(P.entries()) + 1, "sequence": 2,
                       "act": {"record_id": "rec:app:acts:9999", "capture_evidence": "cap:none"}})
        with open(P.ledger, "a") as fh:
            fh.write(json.dumps(forged) + "\n")
        st = ws.standing(P, "legacy-flow")
        check("P-35", "a ledger line without a matching A15 record: 'registration record incomplete', not runnable (LS-4)",
              st[-1][1] == "registration record incomplete", st)
        old = copy.deepcopy(a15)
        old["body"]["relations"] = {"derivedFrom": old["body"]["relations"]["reviewedDraft"]["draft"]}
        free = copy.deepcopy(a15)
        free["body"]["relations"]["priorRevision"] = "workflow revision project:supports-adjust@" + short(rev1["revision"])
        e_old = minischema.validate(old["body"], {"$ref": RS_PROJ_ID + "#/$defs/humanAct"}, reg)
        e_free = minischema.validate(free["body"], {"$ref": RS_PROJ_ID + "#/$defs/humanAct"}, reg)
        check("P-36", "the FR-06 projection refuses RS-v0.8's 'derivedFrom' form and a prior revision written as a free string (C-01)",
              bool(e_old) and bool(e_free), (e_old[:1], e_free[:1]))

        print("\n== C-02 (R18-1): draft transitions carry the A15 record and the revision ==")
        regd = [r for r in ws.records if r["record_kind"] == "draft_transition" and r["event"] == "registered"]
        ncs = [r for r in ws.records if r["record_kind"] == "draft_transition" and r["event"] == "registration not completed"]
        check("P-40", "every 'registered' transition carries a15_record and revision; every 'not completed' one a15_record only",
              regd and ncs and all(r.get("a15_record", "").startswith("rec:") and r.get("revision") == r["content"]["value"]
                                   for r in regd) and all("a15_record" in r and "revision" not in r for r in ncs),
              (len(regd), len(ncs)))
        bad_t = dict(regd[0], event="written", **{"from": "absent", "to": "draft"})
        e = minischema.validate(bad_t, {"$ref": WR_ID + "#/$defs/draft_transition"}, reg)
        check("P-41", "the schema refuses a15_record and revision on a 'written' transition", bool(e), e[:1])

        print("\n== L-4 as clarified: shipped revisions recognized; several entries in one act (WR 4.6 LS-8, 4.7) ==")
        sdir = os.path.join(root, "bundle", "review-notes")
        os.makedirs(sdir)
        open(os.path.join(sdir, "WORKFLOW.md"), "w").write(simple_pkg("review-notes", "shipped in fx-release")["WORKFLOW.md"])
        sci, _ = content_identity(sdir)
        ship_t = tuple_("bundled", "App bundle fx-release", "review-notes", sci["value"])
        old_text = simple_pkg("review-notes", "shipped in fx-release-0")["WORKFLOW.md"]
        odir = os.path.join(root, "bundle-0", "review-notes")
        os.makedirs(odir)
        open(os.path.join(odir, "WORKFLOW.md"), "w").write(old_text)
        oci, _ = content_identity(odir)
        old_t = tuple_("bundled", "App bundle fx-release-0", "review-notes", oci["value"])
        ws.bundled["review-notes"] = (sdir, ship_t)
        ws.shipped["review-notes"] = [ship_t, old_t]          # the release's manifest lists earlier shipped revisions
        copy_regular(sdir, os.path.join(P.slots, "review-notes"))
        st = ws.standing(P, "review-notes")
        sel_s, why = ws.select(ship_t, P.source_root, "thr-30")
        check("P-42", "a library entry byte-equal to a shipped revision: 'shipped revision held in this library'; runs as the bundled tuple, held here",
              st == [(sci["value"], "shipped revision held in this library")] and sel_s
              and sel_s["standing"] == "shipped revision held in this library" and ws.resolve(sel_s)[1] == "verified", (st, why))
        copy_regular(odir, os.path.join(U.slots, "review-notes"))
        st_u = ws.standing(U, "review-notes")
        check("P-43", "a copy equal to an earlier release's shipped revision is recognized as that revision (manifest)",
              st_u == [(oci["value"], "shipped revision held in this library")] and ws.select(old_t, U.source_root, "thr-31")[0],
              st_u)
        open(os.path.join(P.slots, "review-notes", "WORKFLOW.md"), "a").write("\nlocal edit\n")
        st = ws.standing(P, "review-notes")
        check("P-44", "an edited copy is no longer recognized: present without registration record; not selectable",
              st[0][1] == "present without registration record" and ws.select(ship_t, P.source_root, "thr-30")[0] is None
              or (st[0][1] == "present without registration record" and ws.resolve(sel_s)[1] == "revision not verified"), st)
        for n in ("notes-a", "notes-b", "notes-c"):
            os.makedirs(os.path.join(P.slots, n))
            open(os.path.join(P.slots, n, "WORKFLOW.md"), "w").write(simple_pkg(n, "pre-v4 library content")["WORKFLOW.md"])
        ridm, dm = ws.review_entries(P, ["notes-a", "notes-b", "notes-c"])
        open(os.path.join(P.slots, "notes-c", "WORKFLOW.md"), "a").write("\nchanged before the act\n")
        capm = ws.acts.person_operates_multi(dm["descriptor_id"])
        check("P-45", "an entry changed after review: the control refuses the whole capture; review again", not capm["captured"], capm)
        ridm, dm = ws.review_entries(P, ["notes-a", "notes-b", "notes-c"])
        capm = ws.acts.person_operates_multi(dm["descriptor_id"])
        open(os.path.join(P.slots, "notes-b", "WORKFLOW.md"), "a").write("\nchanged after the act\n")
        outm = ws.register_multi(ridm, capm)
        act = ws.rs_records[-1]
        lines = [x for x in P.entries() if x["act"]["record_id"] == capm["record_id"]]
        check("P-46", "one A15 binds three entries; per entry: two registered in place, the one changed after the act not completed; all lines cite the act",
              outm == {"registered": ["notes-a", "notes-c"], "not_completed": ["notes-b"]} and len(act["body"]["boundContent"]) == 3
              and len(lines) == 3 and [s for _, s in ws.standing(P, "notes-a")] == ["registered"]
              and [s for _, s in ws.standing(P, "notes-c")] == ["registered"], (outm, len(lines)))
        print("     on-disk RS_RECORD.schema.json $defs/humanAct, for the multi-entry form (information): %s"
              % (minischema.validate(act["body"], {"$ref": RS_ID + "#/$defs/humanAct"}, reg)[:3] or "conforms"))
        check("P-47", "the multi-entry A15 (relations.registeredEntries, as RS-v0.9 in progress names it; entry: ID-3 strings) conforms to the projection",
              not minischema.validate(act, rsp, reg), minischema.validate(act, rsp, reg)[:2])

        print("\n== run text, supply check and chaining (R19-2, R19-7; WR section 16) ==")
        desk = RunDesk(ws)
        proj_root = os.path.dirname(P.base)

        def label(pkg):
            return os.path.relpath(pkg, proj_root).replace(os.sep, "/")

        def turn_of(turn_id, params, agent_text="ok", view=None):
            items = [{"type": "userMessage", "id": "item-u-" + turn_id, "clientId": params.get("clientUserMessageId"),
                      "content": params["input"]},
                     {"type": "agentMessage", "id": "item-a-" + turn_id, "text": agent_text, "phase": None,
                      "memoryCitation": None, "delivery": None, "questions": None}]
            tr = {"id": turn_id, "items": items, "status": "completed"}
            if view:
                tr["itemsView"] = view
            return tr

        def read_of(c, turns, page_size=1, fail_after_first=False):
            """A stand-in for Codex answering thread/items/list {threadId, turnId, cursor} with pages (R21-4)."""
            entries = [{"turnId": t["id"], "item": i} for t in turns for i in t["items"]]
            seen.clear()

            def fetch(params):
                seen.append(params)
                sel = [e for e in entries if params.get("turnId") in (None, e["turnId"])]
                start = int(params.get("cursor") or 0)
                if fail_after_first and start > 0:
                    return None
                nxt = str(start + page_size) if start + page_size < len(sel) else None
                return {"data": sel[start:start + page_size], "nextCursor": nxt, "backwardsCursor": None}
            return fetch
        seen = []

        # a registered multi-file workflow B
        ws.agent_writes_draft(P, "review-pack", {"WORKFLOW.md": simple_pkg("review-pack", "check the pack")["WORKFLOW.md"],
                                                 "resources/checklist.md": "- item one\n- item two\n"})
        ridB, repB, dB = ws.review(P, "review-pack")
        ws.register(ridB, ws.acts.person_operates(dB["descriptor_id"]))
        revB = dB["subject"]
        c = "thr-40"
        selA, _ = ws.select(rev3, P.source_root, c)
        pkgA, _ = ws.resolve(selA)
        pA, recA = desk.start(c, selA, pkgA, "Inputs: run R-12, supports S-1…S-4.", folder_label=label(pkgA))
        textA = pA["input"][0]["text"]
        rawA = open(os.path.join(pkgA, "WORKFLOW.md"), "rb").read()
        _, again = desk.compose_start(selA, pkgA, recA["run"], c, None, "selected by the person", label(pkgA))
        check("P-48", "run start for A: the text carries WORKFLOW.md's exact bytes between the markers; identity recorded; composition deterministic",
              extract_body(textA, rev3).encode("utf-8") == rawA and recA["text_identity"] == tsha(textA)
              and again["text_identity"] == recA["text_identity"] and recA["chain"] is None
              and textA.split("\n")[0].startswith("[Chirality] Workflow run start: supports-adjust"), recA["lines"]["start_line"])
        other_names = ("notes-a", "review-pack", "legacy-flow", "review-notes")
        check("P-49", "A's run text names no other registered workflow (R19-7: the model is not shown other workflows)",
              not any(n in textA for n in other_names), [n for n in other_names if n in textA])
        tA = turn_of("turn-A1", pA)
        e1_ = minischema.validate(pA, {"$ref": CODEX_ID + "#/definitions/TurnStartParams"}, reg)
        e2_ = minischema.validate(tA, {"$ref": CODEX_ID + "#/definitions/Turn"}, reg)
        check("P-50", "the constructed turn/start params and the turn conform to Codex 0.158.0's generated types (TurnStartParams, Turn)",
              not e1_ and not e2_, (e1_[:2], e2_[:2]))
        ck = desk.check(read_of(c, [tA]), recA, textA, "turn-A1", pA["clientUserMessageId"], ws.tick())
        sent = [dict(x) for x in seen]
        fetch = read_of(c, [tA])
        pages = [fetch(dict(sent[0])), fetch(dict(sent[1]))]
        e3_ = [x for pg in pages for x in minischema.validate(pg, {"$ref": CODEX_ID + "#/definitions/ThreadItemsListResponse"}, reg)]
        e4_ = [x for pr in sent for x in minischema.validate(pr, {"$ref": CODEX_ID + "#/definitions/ThreadItemsListParams"}, reg)]
        check("P-50a", "R21-4: the supply check reads with thread/items/list {threadId, turnId, cursor} (HOSTING §4.4), never "
              "thread/read {includeTurns: true}; it follows the pages to the end; params and pages conform to Codex 0.158.0's "
              "generated types", not e3_ and not e4_ and len(sent) == 2 and sent[0] == {"threadId": c, "turnId": "turn-A1"}
              and sent[1].get("cursor") == "1" and "includeTurns" not in str(sent), (sent, e3_[:2], e4_[:2]))
        tA2 = dict(tA, items=[dict(tA["items"][0], clientId=None), tA["items"][1]])
        ck2 = desk.check(read_of(c, [tA2]), recA, textA, "turn-A1", pA["clientUserMessageId"], ws.tick())
        check("P-51", "supply check against thread/items/list: verified, located by client id, or by the first user message when no client id is echoed",
              ck["state"] == "verified" and ck["located_by"] == "client id" and ck2["state"] == "verified"
              and ck2["located_by"] == "first user message of the turn", (ck["state"], ck2.get("located_by")))
        crlf = copy.deepcopy(pA)
        crlf["input"][0]["text"] = textA.replace("\n", "\r\n")
        fr = copy.deepcopy(pA)
        fr["input"][0]["text"] = textA.replace("[Chirality] Workflow run start:", "[Chirality] Workflow run begins:")
        s1 = desk.check(read_of(c, [turn_of("turn-A1", crlf)]), recA, textA, "turn-A1", None, ws.tick())["state"]
        s2 = desk.check(read_of(c, [turn_of("turn-A1", fr)]), recA, textA, "turn-A1", None, ws.tick())["state"]
        s3 = desk.check(read_of(c, [tA]), recA, textA, "turn-XX", None, ws.tick())["state"]
        s4 = desk.check(read_of(c, [tA], fail_after_first=True), recA, textA, "turn-A1", None, ws.tick())["state"]
        s5 = desk.check(None, recA, textA, "turn-A1", None, ws.tick())["state"]
        check("P-52", "mismatch states: line endings changed; framing changed with bytes intact; turn absent; a later page failed; read failed",
              (s1, s2, s3, s4, s5) == ("text differs, workflow bytes differ", "text differs, workflow bytes equal",
                                       "not found", "unreadable", "unreadable"), (s1, s2, s3, s4, s5))
        selB, _ = ws.select(revB, P.source_root, c)
        pkgB, _ = ws.resolve(selB)
        refused, why = desk.start(c, selB, pkgB, "", folder_label=label(pkgB))
        check("P-53", "one run at a time: starting B while A is in force is refused", refused is None and "one run at a time" in why, why)
        desk.end(c, "ended by the person")
        selB2, _ = ws.select(revB, P.source_root, c, prior_run={"run": recA["run"], "workflow": rev3, "ended": "ended by the person"},
                             replaces=selB["selection_id"])
        pB, recB = desk.start(c, selB2, pkgB, "Now the pack.", folder_label=label(pkgB))
        textB = pB["input"][0]["text"]
        ckB = desk.check(read_of(c, [tA, turn_of("turn-B1", pB)]), recB, textB, "turn-B1", pB["clientUserMessageId"], ws.tick())
        check("P-54", "(a) sequential: B's run text opens with the line saying run A ended; B's record and selection cite run A; other files listed; verified",
              textB.startswith("[Chirality] Previous workflow run ended: supports-adjust revision %s (run %s, ended by the person)."
                               % (rev12(rev3), recA["run"]))
              and recB["chain"]["prior_run"] == recA["run"] and selB2["prior_run"]["run"] == recA["run"]
              and "resources/checklist.md (sha256 " in recB["lines"]["files_line"] and ckB["state"] == "verified",
              textB.split("\n")[0])
        desk.end(c, "completed")
        p1, n1 = desk.next_plain_turn(c, "Thanks. Anything else?")
        p2, n2 = desk.next_plain_turn(c, "And now?")
        ckN = desk.check(read_of(c, [turn_of("turn-N1", p1)]), n1, p1["input"][0]["text"], "turn-N1", None, ws.tick())
        check("P-55", "after B completes with no successor: the next turn carries the end notice first, once; it is verified",
              n1 and p1["input"][0]["text"].startswith("[Chirality] Workflow run ended: review-pack") and len(p1["input"]) == 2
              and n2 is None and len(p2["input"]) == 1 and ckN["state"] == "verified", (p1["input"][0]["text"][:60], n2))
        agent = "The pack is checked.\n\nNext workflow: project:supports-adjust\n"
        pair = desk.proposal_in(agent)
        name = "%s:%s" % pair
        before = len(ws.selections)
        off = desk.offer(pair)
        check("P-56", "(b) an agent proposal line 'Next workflow: <origin>:<name>' yields an offer naming one workflow and no selection",
              pair == ("project", "supports-adjust") and off["offer"] == "Start supports-adjust"
              and len(off["candidates"]) == 1 and len(ws.selections) == before, off)
        latest = P.latest("supports-adjust")["identity"]
        selC, _ = ws.select(latest, P.source_root, c, how="agent proposal confirmed by the person",
                            candidates=off["candidates"],
                            proposal={"conversation": c, "item": "item-a-turn-N1", "proposed_name": name},
                            prior_run={"run": recB["run"], "workflow": revB, "ended": "completed"})
        pkgC, _ = ws.resolve(selC)
        pC, recC = desk.start(c, selC, pkgC, "", origin="agent proposal confirmed by the person", folder_label=label(pkgC))
        check("P-57", "the person confirms: selection 'agent proposal confirmed by the person'; run start chained after B",
              selC["how"] == "agent proposal confirmed by the person" and recC["origin_of_start"] == "agent proposal confirmed by the person"
              and recC["chain"]["prior_run"] == recB["run"] and "(run %s, completed)" % recB["run"] in recC["lines"]["chain_line"],
              recC["lines"].get("chain_line"))
        q = desk.proposal_in("You could try:\nNext workflow: project:review-pack\nbut I am not sure.")
        q2 = desk.proposal_in("The pack is checked.\nNext workflow: review-pack\n")
        q3 = desk.proposal_in("The pack is checked.\nNext workflow: shared:review-pack\n")
        dr = desk.offer(("project", "bad-pkg"))
        un = desk.offer(("project", "no-such-flow"))
        wo = desk.offer(("host", "review-pack"))
        wu = desk.offer(("user", "supports-adjust"))
        check("P-58", "a proposal not on the last line, or naming no origin or an unknown origin, is not one; a draft, an unknown pair or a name registered only in another origin gives a notice and no Start offer; the origin selects among same-name workflows",
              q is None and q2 is None and q3 is None and dr["offer"] is None and "draft only" in dr["notice"]
              and un["offer"] is None and "not registered" in un["notice"] and wo["offer"] is None
              and "not registered" in wo["notice"] and wu["offer"] == "Start supports-adjust"
              and [t["origin"] for t in wu["candidates"]] == ["user"], (q, q2, q3, dr, un, wo, wu))
        desk.end(c, "ended by the person")
        c2 = "thr-41"
        ship_ok = os.path.join(P.slots, "review-notes")
        shutil.rmtree(ship_ok)
        copy_regular(sdir, ship_ok)
        selS, _ = ws.select(ship_t, P.source_root, c2)
        pkgS, _ = ws.resolve(selS)
        pS, recS = desk.start(c2, selS, pkgS, "", folder_label=label(pkgS))
        check("P-59", "a run of a shipped revision held in the project names the bundled tuple and the holding library",
              recS["workflow"]["origin"] == "bundled" and recS["holding_library"] == P.source_root
              and 'from the bundled library "App bundle fx-release"' in recS["lines"]["start_line"], recS["lines"]["start_line"])

        print("\n== R20-1 run end only by the person; R20-3 the run-end line ==")
        c3 = "thr-42"
        selF, _ = ws.select(rev3, P.source_root, c3)
        pkgF, _ = ws.resolve(selF)
        pF, recF = desk.start(c3, selF, pkgF, "", folder_label=label(pkgF))
        msg = "All supports are checked.\nWorkflow finished: project:supports-adjust\nNext workflow: project:review-pack\n"
        offs = desk.offers(c3, msg)
        still = desk.state(c3)["current"] is not None
        check("P-60", "the agent reports the workflow finished and proposes B (both lines by origin and name): the App offers 'End run' and 'End supports-adjust and start review-pack'; the run is still in force",
              offs == ["End run", "End supports-adjust and start review-pack"] and still
              and desk.offers(c3, "Workflow finished: project:other-flow") == []
              and desk.offers(c3, "Workflow finished: supports-adjust") == []
              and desk.offers(c3, "Workflow finished: user:supports-adjust") == [], offs)
        desk.end(c3, "completed")          # the person chose 'End run' after the report (R20-1: cause completed)
        pn, nn = desk.next_plain_turn(c3, "Summarize, please.")
        check("P-61", "no run starts with the next turn: it is prefixed by one App-written line naming the workflow and revision (R20-3)",
              len(pn["input"]) == 2 and pn["input"][0]["text"] == nn["lines"]["end_line"]
              and "\n" not in nn["lines"]["end_line"]
              and nn["lines"]["end_line"] == "[Chirality] Workflow run ended: supports-adjust revision %s (run %s, completed). No workflow is in force." % (rev12(rev3), recF["run"]),
              pn["input"][0]["text"])

        print("\n== R20-9 the two agent lines in the run text (RX) ==")
        pl = recF["lines"]["proposal_line"]
        plS = recS["lines"]["proposal_line"]
        check("P-62", "the run text's proposal line names the run's own origin and name in its finished line and the 'Next workflow: <origin>:<name>' form; a shipped revision held in a library reads 'bundled'",
              '"Workflow finished: project:supports-adjust"' in pl and '"Next workflow: <origin>:<name>"' in pl
              and '"Workflow finished: bundled:review-notes"' in plS and pl == proposal_line(recF["workflow"]),
              (pl, plS))

        print("\n== RX2: the run_text example's identities; R20-11 (1), (2), (4) ==")
        fxd = os.path.join(HERE, "fixtures")
        bad63 = []
        texts = {}
        for r in valid:
            if r["record_kind"] != "run_text":
                continue
            L = r["lines"]
            if r["purpose"] == "run end notice":
                txt = L["end_line"]
            else:
                pk = os.path.join(fxd, r["workflow"]["name"])
                raw = open(os.path.join(pk, "WORKFLOW.md"), "rb").read()
                if (hashlib.sha256(raw).hexdigest(), len(raw)) != (r["workflow_file"]["content"]["value"], r["workflow_file"]["bytes"]):
                    bad63.append(("WORKFLOW.md identity", r["run"]))
                for o in r.get("other_files", []):
                    h = sha(os.path.join(pk, o["path"]))
                    if h != o["sha256"] or "%s (sha256 %s)" % (o["path"], h[:12]) not in L.get("files_line", ""):
                        bad63.append(("other file", o["path"]))
                b_, e_ = markers(r["workflow"])
                if (L["begin_marker"], L["end_marker"]) != (b_, e_) or L["proposal_line"] != proposal_line(r["workflow"]):
                    bad63.append(("markers or proposal line", r["run"]))
                head = [L[k] for k in ("chain_line", "start_line", "proposal_line", "files_line", "begin_marker") if k in L]
                txt = "\n".join(head) + "\n" + raw.decode("utf-8") + "\n" + L["end_marker"]
            if tsha(txt) != r["text_identity"] or len(txt.encode("utf-8")) != r["text_bytes"]:
                bad63.append(("text identity or bytes", r["run"], r["purpose"]))
            texts[(r["run"], r["purpose"])] = r["text_identity"]
        for r in valid:
            if r["record_kind"] == "supply_check" and texts.get((r["run"], r["purpose"])) != r["expected_text"]:
                bad63.append(("supply check expected text", r["check"]))
        check("P-63", "the valid run_text examples' identities and sizes recompute from their lines and the fixture bytes (prototype/fixtures/review-pack); the supply check example expects that identity",
              not bad63 and len(texts) == 2, bad63)
        c4 = "thr-43"
        selG, _ = ws.select(rev3, P.source_root, c4)
        pkgG, _ = ws.resolve(selG)
        desk.start(c4, selG, pkgG, "", folder_label=label(pkgG))
        offs_run = desk.offers(c4, "Checked.\nNext workflow: project:review-pack\n")
        selH, _ = ws.select(revB, P.source_root, c4)
        pkgH, _ = ws.resolve(selH)
        pH, recH = desk.end_and_start(c4, selH, pkgH, "", folder_label=label(pkgH))
        offs_none = desk.offers("thr-44", "Next workflow: project:review-pack\n")
        check("P-64", "R20-11 (1), (4): during a run a proposal is offered only as 'End A and start B'; confirming it ends A 'ended to start B' and B's chain line says so; with no run, a plain 'Start B'",
              offs_run == ["End supports-adjust and start review-pack"] and offs_none == ["Start review-pack"]
              and recH["chain"]["ended"] == "ended to start review-pack"
              and "(run %s, ended to start review-pack)" % recH["chain"]["prior_run"] in recH["lines"]["chain_line"]
              and desk.state(c4)["history"][-1]["ended"] == "ended to start review-pack", (offs_run, offs_none, recH["lines"].get("chain_line")))
        fin_ok = desk.finished_in(c4, "Done.\nWorkflow finished: project:review-pack\nNext workflow: project:supports-adjust")
        fin_last = desk.finished_in(c4, "Done.\nWorkflow finished: project:review-pack")
        fin_bad = desk.finished_in(c4, "Workflow finished: project:review-pack\nThanks for waiting.")
        fin_two = desk.finished_in(c4, "Workflow finished: project:review-pack\nok\nWorkflow finished: project:review-pack")
        prop_two = desk.proposal_in("Next workflow: project:supports-adjust\nor\nNext workflow: project:review-pack")
        check("P-65", "R20-11 (2): the finished line counts as the last line or the one just before the proposal line, each at most once; two proposal lines are no proposal",
              fin_ok == ("project", "review-pack") and fin_last == ("project", "review-pack") and fin_bad is None
              and fin_two is None and prop_two is None, (fin_ok, fin_last, fin_bad, fin_two, prop_two))

        print("\n== every record the prototype produced ==")
        bad = [(r["record_kind"], conforms(r)[:2]) for r in ws.records if conforms(r)]
        counts = {}
        for r in ws.records:
            counts[r["record_kind"]] = counts.get(r["record_kind"], 0) + 1
        check("P-37", "all %d WR records conform to workspace-registration.schema.json %s" % (len(ws.records), counts),
              not bad and len(counts) == 10, bad[:3])
        rbad = [minischema.validate(r, rsp, reg)[:1] for r in ws.rs_records if minischema.validate(r, rsp, reg)]
        check("P-38", "all %d A15 records conform to RS_RECORD.schema.json as projected with FR-06" % len(ws.rs_records), not rbad, rbad[:2])
        wrong = [d for d in ws.records if d["record_kind"] == "a15_descriptor" and d["subject"]["revision"] != d["bound_content"]["value"]]
        check("P-39", "reader check: every A15 descriptor's subject revision equals its bound content", not wrong, wrong[:1])
    finally:
        shutil.rmtree(root)

    n, ok = len(results), sum(results)
    print("\n%d checks, %d passed, %d failed" % (n, ok, n - ok))
    return 0 if ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
