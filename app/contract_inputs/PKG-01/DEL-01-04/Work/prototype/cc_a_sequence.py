"""CC-A candidate state checks; invented inputs, no native/filesystem claim.

Atomic publication/replacement and exclusive writer serialization are modeled
as indivisible steps. Their actual product implementation needs native tests.
Run from this folder: PYTHONDONTWRITEBYTECODE=1 python3 cc_a_sequence.py
"""
from copy import deepcopy

class Conflict(Exception):
    pass

class Model:
    def __init__(self):
        self.capture = None
        self.records = []
        self.complete = True
        self.snapshot = None

    @staticmethod
    def package_scope(package):
        scope = package.get("scope", "")
        if not isinstance(scope, str):
            raise Conflict("non-string scope")
        return scope if scope else "not named by the package"

    def present(self, offer, alternative):
        if self.snapshot is not None or self.capture is not None:
            raise Conflict("active or captured offer")
        if offer["digest"] != "digest-of-fixed-offer":
            raise Conflict("invalid digest")
        matches = [a for a in offer["alternatives"] if a["id"] == alternative]
        if len(matches) != 1:
            raise Conflict("unknown or ambiguous alternative")
        self.snapshot = (deepcopy(offer), deepcopy(matches[0]))
        return deepcopy(matches[0])

    def confirm(self, live_identity, source="native", durable=True):
        if source != "native":
            raise Conflict("non-native confirmation")
        if self.snapshot is None or self.capture is not None:
            raise Conflict("no presented snapshot")
        offer, alt = self.snapshot
        if live_identity != offer["identity"]:
            self.snapshot = None
            raise Conflict("changed package")
        cap = {"captureId": "cap:one", "offerDigest": offer["digest"],
               "actor": "observed-person; identity not verified", "kind": "A16",
               "content": offer["identity"], "scope": offer["scope"],
               "purpose": offer["purpose"], "capturedAt": "original-time",
               "requestRef": "rec:request", "alternativeChosen": alt["id"]}
        if not durable:
            return "capture publication failed"
        self.capture = cap
        self.snapshot = None
        return "capture durable"

    def reconcile(self, backlink_ok=True, append_ok=True):
        # One indivisible writer/capture critical section, including scan/append.
        if self.capture is None:
            raise Conflict("no capture; no record")
        core = {k: v for k, v in self.capture.items() if k != "recordId"}
        matches = [r for r in self.records if r["captureRef"] == core["captureId"]]
        if not self.complete or len(matches) > 1:
            raise Conflict("incomplete logs or ambiguous capture reference")
        if matches:
            rec = matches[0]
            if rec["facts"] != core:
                raise Conflict("capture facts differ")
        else:
            if "recordId" in self.capture:
                raise Conflict("orphan backlink")
            if not append_ok:
                return "AC-8 record pending"
            rec = {"recordId": "rec:written-by-writer", "captureRef": core["captureId"],
                   "facts": deepcopy(core)}
            self.records.append(rec)
        if "recordId" in self.capture and self.capture["recordId"] != rec["recordId"]:
            raise Conflict("backlink conflict")
        if not backlink_ok:
            return "AC-7 recorded; record link pending"
        replacement = deepcopy(self.capture)
        replacement["recordId"] = rec["recordId"]
        self.capture = replacement
        return "AC-7 recorded"

    def restart(self):
        restored = Model()
        restored.capture = deepcopy(self.capture)
        restored.records = deepcopy(self.records)
        restored.complete = self.complete
        return restored


def rejected(fn):
    try:
        fn()
    except Conflict:
        return True
    return False


def main():
    offer = {"identity": "package-bytes-1", "digest": "digest-of-fixed-offer",
             "scope": "package-scope", "purpose": "choose one",
             "alternatives": [{"id": str(i), "statement": "own statement " + str(i),
                                "consequences": ["own consequence " + str(i)]}
                               for i in range(5)]}
    count = 0
    def check(ok, label):
        nonlocal count
        count += 1
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            raise AssertionError(label)

    m = Model(); shown = m.present(offer, "4")
    offer["alternatives"][4]["statement"] = "webview changed text"
    check(shown["statement"] == "own statement 4" and shown["consequences"] == ["own consequence 4"],
          "CA-1 five alternatives: native snapshot keeps original text/consequences")
    check(rejected(lambda: m.present(offer, "0")), "CA-2 selection cannot replace an open native snapshot")
    check(rejected(lambda: m.confirm("package-bytes-1", "webview")) and m.capture is None,
          "CA-3 a webview confirmation captures nothing")
    m.confirm("package-bytes-1")
    check(m.capture["alternativeChosen"] == "4" and "recordId" not in m.capture,
          "CA-4 frozen choice persists before any record; backlink initially absent")
    check(rejected(lambda: m.confirm("package-bytes-1")), "CA-5 second result for same offer refused")
    original = deepcopy(m.capture)
    check(m.reconcile(append_ok=False) == "AC-8 record pending" and m.capture == original and not m.records,
          "CA-6 append failure keeps unchanged durable capture without backlink")
    m = m.restart(); m.reconcile()
    check(len(m.records) == 1 and m.records[0]["facts"]["capturedAt"] == "original-time",
          "CA-7 crash before append: late record keeps original capture time")
    m = Model(); m.present(offer, "2"); m.confirm("package-bytes-1")
    original = deepcopy(m.capture)
    check(m.reconcile(backlink_ok=False) == "AC-7 recorded; record link pending" and m.capture == original,
          "CA-8 backlink failure preserves complete original capture and recorded standing")
    m = m.restart(); m.reconcile(); m.reconcile()
    check(len(m.records) == 1 and m.capture["recordId"] == m.records[0]["recordId"],
          "CA-9 crash after append: find capture-ref, add backlink once, retry idempotent")
    m.capture["recordId"] = "rec:conflict"
    check(rejected(lambda: m.reconcile()) and m.capture["recordId"] == "rec:conflict" and len(m.records) == 1,
          "CA-10 different backlink never replaced")
    m = Model(); m.present(offer, "1"); m.confirm("package-bytes-1"); m.reconcile()
    m.records[0]["facts"]["alternativeChosen"] = "0"
    check(rejected(lambda: m.reconcile()), "CA-11 reference match with different act facts refuses recovery")
    m = Model(); m.present(offer, "1"); m.confirm("package-bytes-1"); m.reconcile()
    m.records.append(deepcopy(m.records[0]))
    check(rejected(lambda: m.reconcile()), "CA-12 duplicate entries hold recovery without a new append")
    m = Model(); m.present(offer, "1"); m.confirm("package-bytes-1"); m.complete = False
    check(rejected(lambda: m.reconcile()) and not m.records, "CA-13 unreadable/torn log set never justifies replay")
    m = Model(); m.present(offer, "1")
    check(rejected(lambda: m.confirm("changed-bytes")) and m.capture is None,
          "CA-14 changed package at confirmation captures nothing")
    m = Model(); m.present(offer, "1"); m.confirm("package-bytes-1", durable=False)
    check(rejected(lambda: m.reconcile()) and not m.records,
          "CA-15 failed capture publication forbids append")
    m = Model(); m.present(offer, "1"); m.snapshot = None
    check(rejected(lambda: m.confirm("package-bytes-1")), "CA-16 cancelled dialog leaves no capture")
    m = Model(); m.present(offer, "1"); m.confirm("package-bytes-1"); m.capture["recordId"] = "rec:orphan"
    check(rejected(lambda: m.reconcile()) and not m.records, "CA-17 orphan backlink never replaced or replayed")
    bad = deepcopy(offer); bad["alternatives"].append(deepcopy(bad["alternatives"][1]))
    check(rejected(lambda: Model().present(bad, "1")), "CA-18 ambiguous alternative identity refused")
    check(Model.package_scope({}) == "not named by the package" and
          Model.package_scope({"scope": ""}) == "not named by the package",
          "CA-19 absent/empty package scope uses exact owner-selected label")
    check(Model.package_scope({"scope": "verbatim scope"}) == "verbatim scope" and
          rejected(lambda: Model.package_scope({"scope": None})),
          "CA-20 nonempty scope unchanged; non-string is invalid not absence")
    print(f"{count} checks, 0 failed; model only, no native/durable filesystem witness")

if __name__ == "__main__":
    main()
