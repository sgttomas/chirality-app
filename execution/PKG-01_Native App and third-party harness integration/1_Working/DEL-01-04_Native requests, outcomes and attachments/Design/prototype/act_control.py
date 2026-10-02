"""Executable model of DEL-01-04/AAC-v0.2 (APP_ACT_CONTROL.md), the App act control.

Design prototype only (R17-1; R12-3). PROPOSED until SCA-V4-003 carries
SC2-01-04-1 (R17-6). Not product code and not the OI-008 placement: "host"
below names the side that R17-5's PROPOSED division gives the act control's
capture to; nothing here runs in a Tauri process.

What it models (AAC §3-§6):
  * offer composition bound to the content identity shown (AC-1), one act kind
    at a time, with the decline where ACT §2.3 defines one;
  * operation only from the host-owned native confirmation (CAP-4; AC-R);
  * the stale-binding refusal (K-8: a draft or file changed after it was shown
    needs a new review) (AC-6);
  * capture evidence (AAC §5.2) and the RS `human_act` / `act_declined` entry,
    written through DEL-04-03's prototype writer (record_store.Writer), so the
    entries are checked by RS's own PROPOSED schema;
  * A15: the act is recorded at capture like every kind; the registration is
    then performed by DEL-02-02 (a stub here) and its outcome is reported
    beside the act, as ACT keeps "accepted — not applied" apart from A5
    (AAC §4.2; AK-f);
  * record write failure and late write (RS FC-1), and relaunch recovery of a
    capture whose record was not written (AC-R1).
"""

import hashlib
import json

from nir_model import canonical

KIND_TABLE = {
    "A4": {"wording": "mark checked", "served": True, "decline": True, "actorRequirement": "the person",
           "subjectClass": "App file"},
    "A6": {"wording": "approve (engineering approval)", "served": True, "decline": True,
           "actorRequirement": "the accountable person", "subjectClass": "App file"},
    "A7": {"wording": "rely (professional reliance)", "served": True, "decline": True,
           "actorRequirement": "the accountable professional; recorded as your own statement", "subjectClass": "App file"},
    "A15": {"wording": "register workflow revision", "served": True, "decline": False,
            "actorRequirement": "the person", "subjectClass": "workflow revision (reviewed draft content)"},
    "A12": {"served": False, "why": "no setting that the App itself establishes exists in this increment (EXEC CAP-1; ACT §2.6)"},
    "A5": {"served": False, "why": "no App-content proposal exists in this increment; host proposals use the host's act facility (ACT §2.6)"},
    "A10": {"served": False, "why": "as A5"},
    "A11": {"served": False, "why": "the proposer's act on a host proposal; not App content"},
    "A13": {"served": False, "why": "captured by the host's enablement facility (ACT §2.6); no App-owned external interface exists"},
}
ACT_CLASS = {"A4": "reserved to the person", "A6": "reserved to the person", "A7": "reserved to the person",
             "A15": "person's act (V4-WF-02)"}
NATIVE_SOURCE = "host-native-confirmation"
SURFACE = "App interface"


class ActControl:
    def __init__(self, identity, read_content, registrar, writers, clock, descriptor_current=lambda d: True,
                 rs_a15_form="relations"):
        self.identity = identity            # () -> person dict (K1-4 sources)
        self.read_content = read_content    # (subject ref) -> bytes or None
        self.registrar = registrar          # (capture) -> (ok, revision or reason)
        self.writers = writers              # (run_id or None) -> RS Writer
        self.clock = clock
        self.descriptor_current = descriptor_current   # DEL-02-02 RB-3: is the A15 descriptor still current?
        self.offers, self.captures, self.states = {}, {}, {}
        self.rs_a15_form = rs_a15_form                 # "relations" (RS after FR-06) or "derivedFrom" (RS-v0.8)
        self.locations = {}                            # prototype only: where each A15 entry's live bytes are read
        self.n = 0

    def _id(self, prefix):
        self.n += 1
        return f"{prefix}:{self.n:04d}"

    def _identity(self, data):
        return {"method": "illustration: sha-256 over content bytes (method unselected; RS U-04, WD U-03)",
                "value": hashlib.sha256(data).hexdigest()}

    # AC-1 compose ----------------------------------------------------------
    def compose(self, kind, subject_ref, scope, purpose, arrival=None, run_id=None, request_ref=None,
                descriptors=None):
        """For A15, subject_ref is ignored: the offer is composed from one or more of DEL-02-02's
        a15_descriptors (WR RB-4), one entry each (L-4: several entries in one act)."""
        k = KIND_TABLE.get(kind)
        if k is None or not k["served"]:
            return None, f"not offered: {kind} — " + (k["why"] if k else "unknown act kind")
        offer = {"format": "chirality.aac.offer", "formatVersion": "0.2", "offerId": self._id("offer"),
                 "actKind": kind, "wording": k["wording"],
                 "scope": scope, "purpose": purpose, "actorRequirement": k["actorRequirement"],
                 "declineAvailable": k["decline"], "composedAt": self.clock()}
        if kind == "A15":
            if not descriptors:
                return None, "not offered: no A15 descriptor from the workspace (WR RB-4)"
            entries, locations = [], []
            for d in descriptors:
                data = self.read_content(d["location"])
                if data is None or self._identity(data)["value"] != d["reviewedDraft"]["content"]["value"] \
                        or not self.descriptor_current(d["descriptorId"]):
                    return None, f"not offered: entry {d['subject']} is not current (changed since review, WR RB-3)"
                entries.append({"descriptorId": d["descriptorId"],
                                "subject": {"ref": d["subject"], "contentIdentity": d["reviewedDraft"]["content"]},
                                "reviewedDraft": d["reviewedDraft"], "priorRevision": d["priorRevision"]})
                locations.append(d["location"])
            offer["entries"] = entries
        else:
            data = self.read_content(subject_ref)
            if data is None:
                return None, "not offered: the subject's content identity is not obtainable"
            offer["subject"] = {"class": k["subjectClass"], "ref": subject_ref, "contentIdentity": self._identity(data)}
        if arrival:
            offer["answers"] = {"arrival": arrival, "runId": run_id}
        else:
            offer["answers"] = {"standing": "no arrival: a standing act (RC-6)"}
        if request_ref:
            offer["requestRef"] = request_ref
        offer["offerDigest"] = {"method": "illustration: sha-256 over the canonical offer",
                                "value": hashlib.sha256(canonical(offer)).hexdigest()}
        if kind == "A15":
            self.locations[offer["offerId"]] = locations
        self.offers[offer["offerId"]] = offer
        self.states[offer["offerId"]] = "AC-1 composed"
        return offer, None

    # AC-2 present ----------------------------------------------------------
    def present(self, offer_id):
        self.states[offer_id] = "AC-2 presented"
        return self.offers[offer_id]

    # AC-3...AC-9 operate -----------------------------------------------------
    def operate(self, offer_id, source, choice):
        offer = self.offers.get(offer_id)
        if offer is None:
            return "AC-R refused", "no such offer"
        if source != NATIVE_SOURCE:
            # CAP-4: no agent tool, MCP operation, App rule, supplier request or webview script operates it
            return "AC-R refused", f"not operable from {source!r}: only the person's native confirmation"
        if self.states[offer_id] != "AC-2 presented":
            return "AC-R refused", f"offer is {self.states[offer_id]!r}, not presented"
        if choice == "dismiss":
            self.states[offer_id] = "AC-5 dismissed"
            return "AC-5 dismissed", "nothing recorded"
        if choice == "decline" and not offer["declineAvailable"]:
            return "AC-R refused", f"no decline for {offer['actKind']} (ACT §2.3); close the control instead"
        if offer["actKind"] == "A15":
            # every entry's bytes are bound: one changed or withdrawn entry makes the whole offer stale
            for e, loc in zip(offer["entries"], self.locations[offer_id]):
                if not self.descriptor_current(e["descriptorId"]):
                    self.states[offer_id] = "AC-6 stale"
                    return "AC-6 stale", (f"the workspace withdrew the descriptor of {e['subject']['ref']} "
                                          "(WR RB-3): nothing captured; review it again")
                data = self.read_content(loc)
                if data is None or self._identity(data)["value"] != e["subject"]["contentIdentity"]["value"]:
                    self.states[offer_id] = "AC-6 stale"
                    return "AC-6 stale", (f"{e['subject']['ref']} changed since it was shown: nothing captured; "
                                          "review it again")
            subjects = [e["subject"]["ref"] for e in offer["entries"]]
            contents = [e["subject"]["contentIdentity"] for e in offer["entries"]]
        else:
            data = self.read_content(offer["subject"]["ref"])
            now_id = self._identity(data) if data is not None else None
            if now_id is None or now_id["value"] != offer["subject"]["contentIdentity"]["value"]:
                self.states[offer_id] = "AC-6 stale"
                return "AC-6 stale", "content changed since it was shown: nothing captured; review it again"
            subjects, contents = [offer["subject"]["ref"]], [offer["subject"]["contentIdentity"]]
        person = self.identity()
        cap = {"format": "chirality.aac.capture-evidence", "formatVersion": "0.2", "captureId": self._id("cap"),
               "offerId": offer_id, "offerDigest": offer["offerDigest"], "choice": choice,
               "actKind": offer["actKind"], "actor": person, "boundSubject": subjects,
               "boundContent": contents, "scope": offer["scope"],
               "purpose": offer["purpose"], "capturedAt": self.clock(), "surface": SURFACE,
               "inputSource": NATIVE_SOURCE, "answers": offer["answers"],
               "evidenceLimits": ["identity not verified"]}
        if "requestRef" in offer:
            cap["requestRef"] = offer["requestRef"]
        if offer["actKind"] == "A15":
            cap["entries"] = [{"descriptorId": e["descriptorId"], "revision": e["subject"]["ref"],
                               "reviewedDraft": e["reviewedDraft"], "priorRevision": e["priorRevision"]}
                              for e in offer["entries"]]
        self.captures[cap["captureId"]] = cap
        self.states[offer_id] = "AC-3 captured" if choice == "act" else "AC-4 declined"
        result = self._record(cap)
        if offer["actKind"] == "A15":
            # the capture is reported to the workspace, which registers exactly the reviewed bytes, per entry
            failed = []
            for e in cap["entries"]:
                ok, res = self.registrar(cap, e)
                e["outcome"] = ({"registration": "completed", "revisionIdentity": res} if ok
                                else {"registration": "not completed", "reason": res})
                if not ok:
                    failed.append((e["revision"], res))
            if failed:
                self.states[offer_id] = "AC-9 recorded; registration not completed"
                return "AC-9 recorded; registration not completed", "; ".join(f"{r}: {why}" for r, why in failed)
        return result

    def _entry(self, cap):
        run_id = cap["answers"].get("runId")
        ev = [{"kind": "capture evidence", "ref": cap["captureId"], "resolutionAtWrite": "resolved"}]
        if cap["choice"] == "decline":
            body = {"actor": cap["actor"], "declinedKind": cap["actKind"], "subject": cap["boundSubject"],
                    "time": cap["capturedAt"], "captureEvidence": ev}
            if "arrival" in cap["answers"]:
                body["arrival"] = cap["answers"]["arrival"]
            if "requestRef" in cap:
                body["requestRef"] = cap["requestRef"]
            return run_id, "act_declined", body
        body = {"actKind": cap["actKind"], "actClass": {"value": ACT_CLASS[cap["actKind"]]},
                "decisionActor": cap["actor"], "recordingMode": "direct capture",
                "boundSubject": cap["boundSubject"], "boundContent": cap["boundContent"],
                "scope": cap["scope"], "purpose": cap["purpose"], "captureEvidence": ev,
                "captureTime": cap["capturedAt"], "evidenceLimits": list(cap["evidenceLimits"])}
        rel = {}
        if "arrival" in cap["answers"]:
            rel["arrivalAnswered"] = cap["answers"]["arrival"]
        if "requestRef" in cap:
            rel["requestRef"] = cap["requestRef"]
        if cap["actKind"] == "A15":
            if self.rs_a15_form == "relations":
                # RS after node F (FR-06; C-01; L-4): reviewedDraft and priorRevision for one entry,
                # registeredEntries {subject, reviewedDraft, priorRevision} for several
                if len(cap["entries"]) == 1:
                    e = cap["entries"][0]
                    rel["reviewedDraft"], rel["priorRevision"] = e["reviewedDraft"], e["priorRevision"]
                else:
                    rel["registeredEntries"] = [{"subject": e["revision"], "reviewedDraft": e["reviewedDraft"],
                                                 "priorRevision": e["priorRevision"]} for e in cap["entries"]]
            else:
                # RS-v0.8 (before node F) requires one string named derivedFrom for A15; it carries
                # each entry's reviewed draft (WR ID-3 string) and prior revision (join J-R2, J-R2b).
                rel["derivedFrom"] = " | ".join(
                    f"{e['revision']}: reviewed draft {e['reviewedDraft']['draft']}; prior revision "
                    + (f"{e['priorRevision']['origin']}:{e['priorRevision']['name']}@{e['priorRevision'].get('revision')}"
                       if e["priorRevision"] else "none")
                    for e in cap["entries"])
        if rel:
            body["relations"] = rel
        return run_id, "human_act", body

    def _record(self, cap):
        from record_store import WriteFailed     # DEL-04-03's prototype writer (read-only import)
        run_id, kind, body = self._entry(cap)
        writer = self.writers(run_id)
        rec_id = "rec:app-interface:" + cap["captureId"].split(":")[1]
        cap["recordId"] = rec_id
        try:
            written = writer.append(kind, body, rec_id)
        except WriteFailed as exc:
            self.states[cap["offerId"]] = "AC-8 record pending"
            return "AC-8 record pending", f"capture kept; the record is written late: {exc}"
        ids = {w["recordId"] for w in written}
        for other in self.captures.values():      # a pending record written late, in order (RS W-2)
            if other.get("recordId") in ids:
                self.states[other["offerId"]] = "AC-7 recorded"
        return "AC-7 recorded", rec_id

    def retry_pending(self, run_id=None):
        """W-2: the writer writes pending entries in order, then 'record write failed'."""
        written = self.writers(run_id).flush()
        for cap in self.captures.values():
            if self.states.get(cap["offerId"]) == "AC-8 record pending" and \
                    any(w["recordId"] == cap.get("recordId") for w in written):
                self.states[cap["offerId"]] = "AC-7 recorded"
        return written

    def recover(self, records_present):
        """AC-R1 after relaunch: a capture whose record is in no log gets its record, late, in order."""
        done = []
        for cap in self.captures.values():
            if cap.get("recordId") in records_present:
                continue
            done.append(self._record(cap))
        return done


def dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)
