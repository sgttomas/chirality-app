"""Build fixture FX-RP1-2 for EU-F1 (RP-v0.2): one replacement decision package, assembled and left pending.

Prototype, not product code (DEL-11-03 REPLACEMENT_PACKET.md §8). Deterministic: rerunning it writes
the same bytes. It reads the supplier files and basis documents, runs read-only `git` for the thesis
identity at a FIXED commit, and writes only under F/fixtures/FX-RP1-2/. No network. FX-RP1 (v1) is kept
unchanged as the input set RR-EUF1 read; after the RP-R1/RP-R2 repair it is history and is not regenerated.

Usage: python3 -B build_fx_rp1.py
"""

import json
import os
import re
import subprocess
import sys

import rplib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fixtures", "FX-RP1-2")
FIXTURE = "FX-RP1-2"
REPO = os.path.normpath(os.path.join(L.EXEC_ROOT, "..", "..", ".."))

THESIS_COMMIT = "d2929fd62b3dfea6a56090b81d0c8248be97a4c0"  # HEAD when S2-F observed the thesis (S2-F C-5)
THESIS_PATH = "projects/chirality-app-v4/foundation/thesis"
THESIS_EXPECTED = "47fc49e96c2931ba18090f1a82d56a49f230b3ee"  # docs/PRD.md §11
DATE = "2026-10-04"
SOW_11_03 = L.P11 + "/DEL-11-03_Owner replacement evidence packet/ScopeOfWork.md"


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), check=True, capture_output=True, text=True).stdout.strip()


def norm(text):
    return re.sub(r"\s+", " ", text)


def quote(rel, ref, text):
    src = open(L.abspath(rel), encoding="utf-8").read()
    if norm(text) not in norm(src):
        sys.exit("quote not found in %s: %s" % (rel, text[:60]))
    return {"ref": ref, "quote": text, "source_sha256": L.sha256_file(L.abspath(rel))}


def record(examples_key, record_id, id_field):
    for r in L.load(examples_key):
        if r.get(id_field) == record_id:
            return r
    sys.exit("record %s not found" % record_id)


def write(rel, obj):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = L.dumps(obj)
    with open(path, "wb") as fh:
        fh.write(data)
    return L.sha256_file(path)


def main():
    # --- Basis quotes (checked against the current bytes) -------------------------
    basis = [
        quote("../docs/PRD.md", "docs/PRD.md §8 V4-REP-01",
              "v4 may replace v3.0.1 when both hold: the Chirality App supports the core loop at least at "
              "v3.0.1's level — plan, execute, save a workflow, reuse it, approvals, interruption, restart — "
              "and one live embedded journey in SWBPIPE runs from a request to the person's acceptance."),
        quote("../docs/PRD.md", "docs/PRD.md §8",
              "The owner decides the replacement; the old projects and archives are kept until then (OD-09)."),
        quote("../docs/PRD.md", "docs/PRD.md §8",
              "Replacement is distinct from all-project retirement or professional reliance (B-HTML 07)."),
        quote("../docs/EXAMINATION.md", "docs/EXAMINATION.md §7",
              "The owner decides the replacement (V4-REP-01). The evidence presented for that decision is: "
              "V4-EXM-10 and V4-EXM-11 passed on the candidate App (the core loop at least at v3.0.1's level), "
              "and V4-EXM-20 passed on the candidate App and SWBPIPE with a local model (one live embedded "
              "journey from request to acceptance)."),
        quote(SOW_11_03, "DEL-11-03 ScopeOfWork.md CLM-003",
              "The owner retains public-release decisions; the accountable professional retains professional "
              "approval/reliance. None follows from replacement, a merge or a successful operation."),
        quote(SOW_11_03, "DEL-11-03 ScopeOfWork.md REQ-005",
              "Carry limits of any practitioner observations without inventing a third fixed-duration replacement gate."),
    ]

    # --- Baseline: REFERENCES.md §2 (values checked present in its bytes) ----------
    refs_text = open(L.abspath("references"), encoding="utf-8").read()
    baseline = {
        "name": "Chirality v3.0.1",
        "source": "projects/chirality-app-v4/reference/REFERENCES.md §2",
        "source_sha256": L.sha256_file(L.abspath("references")),
        "release": "sgttomas/chirality-app release v3.0.1, published 2026-09-20T03:29:16Z",
        "desktop_source": "sgttomas/chirality@485051eac923c759238948a54cd7bb094eee4899",
        "installer": {"name": "Chirality-3.0.1-arm64.dmg", "bytes": 339832416,
                      "sha256": "eea43a0d973d1cd401da58cfd7a7156d9e932503fbb0c469a799e3cec73fd2e3"},
        "remote_rechecked": False,
        "reference_limit": ("The v3 references attached to each core-loop element come from App v3's "
                            "JOURNEY_RESULTS.md, whose later journeys ran on development candidate 266c121bb "
                            "(v3.0.0 era), which is not an ancestor of the v3.0.1 source. They describe v3 "
                            "behaviour as context; v3 evidence qualifies nothing in v4 (R23-32 F-R2)."),
    }
    for needle in ["2026-09-20T03:29:16Z", "485051eac923c759238948a54cd7bb094eee4899", "Chirality-3.0.1-arm64.dmg",
                   "339,832,416", baseline["installer"]["sha256"]]:
        if needle not in refs_text:
            sys.exit("baseline value not in REFERENCES.md: " + needle)

    # --- Supplied supplier records (copies of schema examples: illustrative) -------
    sq = record("sq_examples", "SQ-EX-05", "record_id")
    dos = record("lhq_manifest_examples", "DOS-EXAMPLE-INVENTED", "dossier_id")
    cir = record("lhq_cir_examples", "LHQ-CIR-EXAMPLE-STATE-2026-10-03", "record_id")

    # --- First-cut inputs from DEL-11-01 and DEL-09-12 -------------------------------
    observed_tree = git("rev-parse", THESIS_COMMIT + ":" + THESIS_PATH)
    files = len(git("ls-tree", "-r", "--name-only", THESIS_COMMIT, "--", THESIS_PATH).splitlines())
    continuity = {
        "record_kind": "continuity_handoff",
        "format": "RP-v0.1-first-cut",
        "account_version": 1,
        "thesis_check": {
            "result": "matches" if observed_tree == THESIS_EXPECTED else "differs",
            "method": "git rev-parse <commit>:" + THESIS_PATH + " compared with the tree docs/PRD.md §11 names",
            "expected_tree": THESIS_EXPECTED,
            "observed_tree": observed_tree,
            "at_commit": THESIS_COMMIT,
            "files": files,
            "limits": ["committed-tree identity at the named commit; working bytes are not compared by this record",
                       "attribution and nonbinding standing not yet inspected (DEL-11-01 VER-003)"],
        },
        "fallback_identity": {"source": "projects/chirality-app-v4/reference/REFERENCES.md §2",
                              "source_sha256": baseline["source_sha256"], "retained": True, "remote_rechecked": False},
        "archives": {"verify": "not_run", "source": "projects/chirality-app-v4/reference/archives/ARCHIVES.md"},
        "continuing_obligations": {"status": "not_supplied", "owner": "Owner with affected consumers (OI-024)",
                                   "point_of_need": "Before each adoption/retirement decision"},
        "adoption_status": "not_supplied",
        "replacement_standing": "replacement pending; v3.0.1 retained",
    }
    practitioner = {
        "record_kind": "practitioner_standing",
        "format": "RP-v0.1-first-cut",
        "open_issue": "OI-016 (App v4)",
        "standing": "not_agreed",
        "agreement_ref": None,
        "observations": [],
        "limits": ["no validation period or activities agreed; no practitioner use has occurred",
                   "practitioner validation is not a replacement condition (R23-32 F-R3)"],
    }

    schema_sha = L.sha256_file(L.abspath("rp_manifest_schema"))
    supplied_specs = [
        ("S-1", "sq_dossier", "supplied/sq-dossier.SQ-EX-05.json", sq, "illustrative", "sq_examples", "SQ-EX-05",
         "DEL-09-02 standalone qualification (schema example SQ-EX-05; illustrative, no real candidate)", "copied_record"),
        ("S-2", "lhq_dossier_manifest", "supplied/lhq-dossier-manifest.DOS-EXAMPLE-INVENTED.json", dos, "illustrative",
         "lhq_manifest_examples", "DOS-EXAMPLE-INVENTED",
         "DEL-09-07 local host qualification (schema example; invented, no case has run)", "copied_record"),
        ("S-3", "lhq_cir", "supplied/lhq-cir.LHQ-CIR-EXAMPLE-STATE-2026-10-03.json", cir, "illustrative",
         "lhq_cir_examples", "LHQ-CIR-EXAMPLE-STATE-2026-10-03",
         "DEL-09-07 candidate identification record (schema example; no candidate identified)", "copied_record"),
        ("S-4", "continuity_input", "supplied/continuity-handoff.json", continuity, "first_cut_interface", None,
         "$defs/continuity_input",
         "DEL-11-03's prototype builder, standing in for DEL-11-01 until its continuity account exists; the thesis "
         "result was observed by read-only git at the commit named; everything else is stated as not supplied or not run",
         "shape_only"),
        ("S-5", "practitioner_standing", "supplied/practitioner-standing.json", practitioner, "first_cut_interface",
         None, "$defs/practitioner_standing",
         "DEL-11-03's prototype builder, standing in for DEL-09-12 until its practitioner record exists; states that "
         "no validation is agreed (R23-32 P-2)", "shape_only"),
    ]
    supplied = []
    for item_id, role, rel, obj, standing, src_key, rec, produced_by, kind in supplied_specs:
        sha = write(rel, obj)
        if src_key:
            source = {"path": L.PATHS[src_key], "sha256": L.sha256_file(L.abspath(src_key)), "record_id": rec}
        else:
            source = {"path": L.PATHS["rp_manifest_schema"], "sha256": schema_sha, "record_id": rec}
        supplied.append({"item_id": item_id, "role": role, "path": rel, "sha256": sha, "standing": standing,
                         "source": source, "produced_by": produced_by, "source_kind": kind})

    # --- Rules RP-R1...RP-R5 ---------------------------------------------------------
    cl = L.core_loop(sq)
    jr = L.journey(dos)
    sq_subject = L.map_sq_candidate(sq["candidate"])
    cir_subject, cir_reason = L.map_cir_candidate(cir)
    rec = L.reconcile(sq_subject, cir_subject, cir_reason)
    complete = L.replacement_evidence_complete(cl, jr, rec)

    # Points of need (RP-v0.2): gaps never gate presentation; AX-001 lets a packet report partial or adverse evidence.
    TO_COMPLETE = "before the replacement evidence can be complete (presentation is not gated: DEL-11-03 AX-001)"
    CARRIED = "carried for the owner; not a replacement condition"
    words = {
        "p20a_not_counted_as_completed_witness": "the journey case LHQ-20's main part (P20-A) is not counted as a completed V4-EXM-20 witness; in this example it was not run",
        "no_acceptance_act_cited": "no record of the person's acceptance is cited",
        "acceptance_act_actor_equals_recorder": "an acceptance act names its recorder as its actor",
        "no_independent_review_record": "no independent examiner's review record exists for the journey",
        "p20a_result_not_resolved_to_candidate_pass": "P20-A's result is not a pass recorded on an identified candidate",
        "receipts_in_dossier_missing_from_handoff": "the dossier names a host receipt (%s) that its hand-over to DEL-11-03 does not list" % ", ".join(r["ref"] for r in jr["receipts"]["elsewhere_in_dossier"]),
    }
    gaps = []
    for e in cl["elements"]:
        if e["recorded"] != "recorded_pass":
            detail = "; ".join("%s %s%s" % (s["step"], s["state"], (" " + s["outcome"]) if "outcome" in s else "")
                               for s in e["steps"] if not (s["state"] == "recorded" and s.get("outcome") == "pass"))
            gaps.append({"gap_id": "G-CL-" + e["element"].upper().replace(" ", "-"),
                         "what": "core-loop element '%s': the dossier records %s" % (e["element"], detail),
                         "supplier": "DEL-09-02 (standalone qualification dossier)", "point_of_need": TO_COMPLETE})
    if "result_records_not_resolved_to_candidate_records" in cl["not_established_because"]:
        gaps.append({"gap_id": "G-CL-EVIDENCE",
                     "what": "none of the %d counted core-loop step results is a record of an identified candidate (the dossier is an illustrative example), so no element can be shown met or not met" % len(cl["unresolved_steps"]),
                     "supplier": "DEL-09-02 (standalone qualification dossier)", "point_of_need": TO_COMPLETE})
    if not jr["established"]:
        gaps.append({"gap_id": "G-J-WITNESS",
                     "what": "no completed V4-EXM-20 journey witness: " + "; ".join(words[r] for r in jr["not_established_because"]),
                     "supplier": "DEL-09-07 (local host qualification dossier), with the SWBPIPE owner (external dependency DEP-001); joint host work is deferred by the owner's DECISION-3",
                     "point_of_need": TO_COMPLETE})
    if rec != "reconciled":
        gaps.append({"gap_id": "G-CAND-JOINED",
                     "what": "the journey's candidate identification record (CIR) does not supply the App candidate, so one candidate across both obligations is not established",
                     "supplier": "DEL-09-07 (local host qualification: candidate identification record)", "point_of_need": TO_COMPLETE})
    if continuity["continuing_obligations"]["status"] != "supplied" or continuity["archives"]["verify"] != "passed":
        gaps.append({"gap_id": "G-CONT",
                     "what": "continuity account incomplete: continuing-obligation dispositions not supplied; the archive check was not run",
                     "supplier": "DEL-11-01 (continuity account), with affected project owners", "point_of_need": CARRIED})
    gaps.append({"gap_id": "G-ADOPT", "what": "consumer adoption status not supplied",
                 "supplier": "DEL-11-02 (adoption account)", "point_of_need": CARRIED})

    excerpts_sha = write_excerpts()

    manifest = {
        "record_kind": "rp_packet_manifest",
        "format": "RP-v0.2",
        "packet_id": "RP-FX-RP1",
        "version": 2,
        "date": DATE,
        "evidence_standing": "illustrative",
        "basis": basis,
        "basis_excerpts": {"path": "packet/basis-excerpts.md", "sha256": excerpts_sha},
        "baseline": dict(baseline, comparison_rule=(
            "EXAMINATION §7: the candidate supports the core loop at least at v3.0.1's level when V4-EXM-10 and "
            "V4-EXM-11 pass on it. v3.0.1 is not rerun (R23-32 F-R2); each element's v3 reference is context only.")),
        "candidate": {
            "subject": sq_subject,
            "mappings": [
                {"from": "DEL-09-02 SQ dossier `candidate` (S-1)", "record_id": sq["record_id"], "result": "mapped",
                 "note": "revision and build_identity copied; packaged is false because no package_record; codex_pin is configuration, not identity"},
                {"from": "DEL-09-07 candidate identification record (CIR) `app_candidate` (S-3)", "record_id": cir["record_id"],
                 "result": cir_reason, "note": cir["elements"]["app_candidate"]["source"]},
            ],
            "reconciliation": rec,
            "change_impact_refs": [],
        },
        "supplied": supplied,
        "core_loop": dict(cl, source_item="S-1"),
        "journey": dict(jr, source_item="S-2", cir_item="S-3"),
        "practitioner": {"source_item": "S-5", "standing": practitioner["standing"], "is_replacement_condition": False},
        "continuity": {"source_item": "S-4", "thesis_identity": continuity["thesis_check"]["result"],
                       "fallback_retained": True, "archives_verify": continuity["archives"]["verify"],
                       "continuing_obligations": continuity["continuing_obligations"]["status"]},
        "adoption": {"status": "not_supplied", "supplier": "DEL-11-02"},
        "replacement_evidence": complete,
        "gaps": gaps,
        "not_established": ["replacement_decision", "public_release", "retirement", "professional_reliance",
                            "consumer_adoption", "practitioner_validation"],
        "open_matters": [
            {"id": "P-1 replacing v3.0.1", "owner": "the owner", "point_of_need": "when both witnesses exist; an act, not a question now"},
            {"id": "P-5 public release (PRD OQ-08)", "owner": "the owner", "point_of_need": "Before public release"},
            {"id": "OI-024 staged adoption and retirement", "owner": "Owner with affected consumers", "point_of_need": "Before each adoption/retirement decision"},
            {"id": "OI-021 first connected activity", "owner": "Owner via outside SWB session and App/shared owner", "point_of_need": "Before connected-activity SoW and execution"},
            {"id": "DEP-001 SWBPIPE contributions", "owner": "SWBPIPE outside implementation session", "point_of_need": "Before corresponding connected-journey integration/examination and fallback-replacement decision"},
            {"id": "OI-016 (App v4) validation period and activities", "owner": "Owner", "point_of_need": "Before practitioner validation in use"},
            {"id": "OI-013/OI-014 residue: what the App candidate contributes to an embedded journey", "owner": "Shared contract owner with SWB owner", "point_of_need": "Before the CIR's App-candidate element is fixed for CA/E"},
        ],
        "terms": TERMS,
    }
    manifest_sha = write("packet/RP-FX-RP1.v2.packet-manifest.json", manifest)

    a = sq_subject["app_candidate"]
    package = {
        "format": "chirality.decision-package",
        "formatVersion": "0.1",
        "packageId": "pkg:app-v4:replacement:FX-RP1-2",
        "actKind": "A16",
        "subject": [
            "whether, and at what scope (see the alternatives), App v4 candidate (revision: %s; build: %s) replaces Chirality v3.0.1, the published fallback" % (a["revision"], a["build_identity"]),
            "packet manifest sha256:" + manifest_sha,
        ],
        "purpose": ("The owner decides (act kind A16, 'decide': choose exactly one of the four alternatives below) whether "
                    "the identified v4 candidate replaces the v3.0.1 fallback, on the evidence in the packet manifest the "
                    "subject names. FIXTURE FX-RP1-2 for EU-F1: illustrative evidence; not for presentation to the owner."),
        "scope": "the v3.0.1 fallback only; old projects, archives, active work and continuing obligations are outside this decision (OI-024)",
        "reservedBy": [
            {"ref": "docs/PRD.md §8 V4-REP-01", "statement": "The owner decides the replacement; the old projects and archives are kept until then (OD-09)."},
            {"ref": "docs/EXAMINATION.md §7", "statement": "The owner decides the replacement (V4-REP-01)."},
        ],
        "alternatives": [
            {"id": "ALT-OWN-USE",
             "statement": "Replace v3.0.1 in the owner's own work only: the owner uses this candidate instead of v3.0.1 for their own design work. For everyone else, v3.0.1 stays published and remains the fallback",
             "consequences": ["v3.0.1 remains the published fallback; nothing is published or withdrawn",
                              "No public release: publishing v4 would be a separate owner act (PRD OQ-08)",
                              "No retirement: old projects, archives and active work are kept (OI-024)",
                              "The packet's open gaps still apply to the owner's own use of this candidate"]},
            {"id": "ALT-PUBLISHED",
             "statement": "Replace as the published product: this candidate replaces v3.0.1 as the product published in sgttomas/chirality-app",
             "consequences": ["v3.0.1 is no longer the fallback for the published product",
                              "This is also a public-release act, which the owner decides separately (PRD OQ-08; DEL-11-03 CLM-003)",
                              "Inference from App v3's records (BUILD_AND_RELEASE.md §12, excerpted in the packet): v3.0.x installs check the latest published stable release, so they would be offered v4",
                              "No retirement: old projects, archives and active work are kept until their own decisions (OI-024)"]},
            {"id": "ALT-DEFER",
             "statement": "Defer: decide again when the packet's named gaps are closed",
             "consequences": ["v3.0.1 remains the fallback", "No public release",
                              "No retirement: nothing is retired",
                              "The packet is rebuilt as a new version when a supplier closes a gap"]},
            {"id": "ALT-DECLINE",
             "statement": "Decline this candidate",
             "consequences": ["v3.0.1 remains the fallback",
                              "This candidate does not replace it; a later candidate needs its own package",
                              "No public release", "No retirement: nothing is retired"]},
        ],
    }
    package_sha = write("package/PKG-REPLACEMENT-FX-RP1-2.json", package)

    disposition = {
        "record_kind": "rp_disposition",
        "format": "RP-v0.1",
        "disposition_id": "RPD-FX-RP1-2",
        "package_id": package["packageId"],
        "package_file": {"path": "package/PKG-REPLACEMENT-FX-RP1-2.json", "sha256": package_sha},
        "state": "not_presented",
        "not_presented_because": "EU-F1 fixture: prepared for the consumption check only; no owner act is requested (DEL-11-03 VER-004)",
        "fallback_status": "v3.0.1 remains the fallback; old projects and archives are kept",
        "recorder": "DEL-11-03 coordinator (prototype builder)",
        "recorded_at": DATE,
        "limits": ["fixture; illustrative supplier evidence", "no owner act exists or is implied"],
    }
    write("records/RPD-FX-RP1-2.disposition.json", disposition)

    missing = sorted(undefined_codes([package, manifest, disposition]))
    if missing:
        sys.exit("codes without a term: " + ", ".join(missing))

    lines = []
    for root, _, names in os.walk(OUT):
        for n in names:
            if n == "MANIFEST.sha256":
                continue
            p = os.path.join(root, n)
            lines.append("%s  %s" % (L.sha256_file(p), os.path.relpath(p, OUT)))
    with open(os.path.join(OUT, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    print("%s written: %d files; manifest sha256 %s; package sha256 %s" % (FIXTURE, len(lines), manifest_sha, package_sha))


# --- Legibility (RP-v0.2): terms and basis excerpts --------------------------------

CODE_RE = re.compile(r"\b(A1[0-6]|P20-A|LHQ-20|V4-[A-Z]+-\d+|OI-\d{3}|DEP-\d{3}|DECISION-\d|R23-\d+|OQ-\d{2}|OD-\d{2}|"
                     r"B-HTML|F-R\d+|P-\d|CLM-\d{3}|REQ-\d{3}|VER-\d{3}|AX-\d{3}|EXP-R\d|SQ-R\d|DH-1|CA/E|CIR|SWBPIPE|SWB|"
                     r"DEL-\d{2}-\d{2}|SoW|EXP)\b")

TERMS = [
    {"term": "A16", "meaning": "The act kind 'decide': the person chooses exactly one alternative of a decision package (App v4 act ontology, ACT-POLICY-v0.10 §2.1)."},
    {"term": "P-1, P-2, P-5", "meaning": "The person's own acts at their own points of need, as ruled for this cluster: P-1 replacing v3.0.1; P-2 agreeing the validation period and activities; P-5 public release."},
    {"term": "V4-REP-01", "meaning": "The PRD's replacement rule: v4 may replace v3.0.1 when the core loop works at least at v3.0.1's level and one live embedded SWBPIPE journey runs to the person's acceptance (excerpted)."},
    {"term": "V4-EXM-10, V4-EXM-11, V4-EXM-12, V4-EXM-20", "meaning": "Examination scenarios: 10 create and reuse a workflow; 11 interruption, approvals and restart; 12 three kinds of model access (not part of the core loop); 20 the live local-model journey in SWBPIPE (the replacement journey)."},
    {"term": "LHQ-20, P20-A", "meaning": "LHQ-20 is the local-host case that runs V4-EXM-20; P20-A is its main part, the completed journey from request to the person's acceptance and application."},
    {"term": "CIR", "meaning": "Candidate identification record: the local-host qualification's record of exactly which App, host, model server and machine a journey ran on."},
    {"term": "EXP, EXP-R3", "meaning": "EXP is the examination protocol (DEL-09-01) every result record follows; EXP-R3: only a record made on an identified candidate can stand for a scenario."},
    {"term": "DH-1, SQ-R8", "meaning": "Supplier rules: DH-1 (DEL-09-07) says when P20-A counts as a completed witness; SQ-R8 (DEL-09-02) says when a dossier is handed over as independently examined."},
    {"term": "SWBPIPE, SWB", "meaning": "The owner's piping design application, the first host; built in a separate outside session (SWB)."},
    {"term": "CA/E", "meaning": "The embedded-agent variant of the connected activity: the host's own agent works inside SWBPIPE."},
    {"term": "OI-013, OI-014, OI-016, OI-021, OI-024", "meaning": "Open issues in App v4's register, each with an owner and a point of need: 013/014 shared loop and component placement; 016 (App v4) validation period and activities; 021 the first connected activity; 024 staged adoption and retirement."},
    {"term": "OQ-08", "meaning": "PRD open question: written sign-in terms for third-party distribution, owned by the owner, needed before public release."},
    {"term": "OD-09", "meaning": "Original owner direction: the old projects and archives are kept until the replacement decision."},
    {"term": "DEP-001", "meaning": "External dependency: SWBPIPE's contributions (host operations, receipts, human-act recording), owned by the outside SWBPIPE session."},
    {"term": "DECISION-3", "meaning": "The owner's decision of 2026-09-28 deferring joint work with SWBPIPE ('defer the host joins')."},
    {"term": "R23-32, F-R2, F-R3", "meaning": "Coordinator rulings in this run's R23_RESOLUTIONS.md: F-R2 v3.0.1 is not rerun; F-R3 practitioner validation is not a replacement condition."},
    {"term": "DEL-nn-nn", "meaning": "A deliverable of the App v4 project: DEL-09-02 standalone qualification; DEL-09-07 local host qualification; DEL-09-12 practitioner validation; DEL-11-01 continuity account; DEL-11-02 adoption account; DEL-11-03 this replacement packet."},
    {"term": "CLM-001, CLM-003, REQ-004, REQ-005, AX-001, VER-003, VER-004", "meaning": "Clauses of a deliverable's ScopeOfWork (its production contract); those of DEL-11-03 are excerpted."},
    {"term": "SoW", "meaning": "ScopeOfWork, a deliverable's production contract."},
    {"term": "B-HTML", "meaning": "The accepted decision brief of the App v4 basis (2026-09-26)."},
]


def undefined_codes(objs):
    defined = set()
    for t in TERMS:
        defined.update(CODE_RE.findall(t["term"]))
    found = set(CODE_RE.findall(json.dumps(objs, ensure_ascii=False)))
    return {c for c in found if c not in defined and not c.startswith("DEL-")}


EXCERPTS = [  # (path relative to EXEC_ROOT, first line, last line, expected start)
    ("../docs/PRD.md", 444, 460, "## 8. Replacing the v3.0.1 fallback"),
    ("../docs/EXAMINATION.md", 241, 255, "## 7. Replacing v3.0.1"),
    (SOW_11_03, 33, 33, "- **CLM-001**"),
    (SOW_11_03, 35, 35, "- **CLM-003**"),
    (SOW_11_03, 45, 46, "- **REQ-004**"),
    (SOW_11_03, 69, 69, "- **AX-001**"),
    ("../reference/REFERENCES.md", 23, 53, "## 2. Fallback release (v3.0.1)"),
    ("../../chirality-app-dev/docs/BUILD_AND_RELEASE.md", 216, 226, "## 12. Product guidance and public update source"),
]


def write_excerpts():
    out = ["# Basis excerpts for package FX-RP1-2", "",
           "Exact lines from each source, with its sha256. App v3's BUILD_AND_RELEASE.md is historical evidence, not a v4 commitment.", ""]
    for rel, a, b, start in EXCERPTS:
        path = L.abspath(rel)
        lines = open(path, encoding="utf-8").read().split("\n")
        if not lines[a - 1].startswith(start):
            sys.exit("excerpt boundary moved: %s line %d" % (rel, a))
        shown = os.path.normpath(os.path.join("projects/chirality-app-v4/execution", rel))
        out += ["## %s, lines %d-%d (sha256 %s)" % (shown, a, b, L.sha256_file(path)), "", "```text"] + lines[a - 1:b] + ["```", ""]
    path = os.path.join(OUT, "packet", "basis-excerpts.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))
    return L.sha256_file(path)


if __name__ == "__main__":
    main()
