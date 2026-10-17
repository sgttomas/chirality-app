#!/usr/bin/env python3
"""Map SWBPIPE's operation contract corpus into DEL-03-02 P / DEL-03-01 C terms.

Prototype only (R12-3): Python 3 standard library, no package, no network, not
product code. It reads SWBPIPE sources read-only at the commit recorded in
`../swbpipe-corpus-pins.json`, refuses any pinned file whose bytes have drifted,
maps every corpus case (fixtures/model_operations/contract_corpus/case_*.json)
to the P section 9 / C section 4.1 outcome it lands on, or to no contract outcome, and
names the findings (NR-nn: what SWBPIPE would need to add; A-nn: App-side gaps)
that stop an App record being formed. See `../SWBPIPE_CORPUS_RECEIVING.md`.

Standing rules the mapping enforces (and this script checks):
  * nothing gains stronger standing than the source gives it: a host Apply is
    never an A5, never per item, never a named person's act; a receipt is not an
    acceptance; no row carries a decision, accepted, rejected or withdrawn;
  * a host refusal is 'refused', never A10 (P REQ-004);
  * the App never computes a host identity (C section 5.3, 5.5): what the host does not
    supply stays 'not supplied'.

Usage (from this folder):
  python3 -B swbpipe_corpus_map.py               # verify pins, regenerate, compare, check
  python3 -B swbpipe_corpus_map.py --write       # rewrite ../swbpipe-corpus-mapping.json
  python3 -B swbpipe_corpus_map.py --write-pins  # re-pin SWBPIPE sources at HEAD (a new read)
Exit status 0 only if every check holds.
"""

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
ROOT = DESIGN.parents[5]                    # repository root
PIPING = "projects/chirality-piping"
CORPUS = f"{PIPING}/fixtures/model_operations/contract_corpus"
PINS = DESIGN / "swbpipe-corpus-pins.json"
MAPPING = DESIGN / "swbpipe-corpus-mapping.json"

# SWBPIPE sources read for the mapping besides the corpus (path, what it is read for).
SOURCES = [
    (f"{CORPUS}/README.md", "corpus format, comparison rules, review status of each case range"),
    (f"{PIPING}/core/model_operations/operation_applier/src/lib.rs",
     "single-operation outcome; acceptance record (no actor, act reference or time); binding status; "
     "OP-STALE-BEFORE-VALUE; agent-authored k rule O5 on asserted author_type; engine version 0.1.0"),
    (f"{PIPING}/core/model_operations/operation_applier/src/atomic_batch.rs",
     "per-batch Apply: atomic commit or rollback, one acceptance basis per batch, claimed hash required, "
     "author and source identity asserted metadata only"),
    (f"{PIPING}/core/model_operations/operation_applier/src/bend_authoring.rs", "OP-BEND-FLEXIBILITY-USER-ENTRY-REQUIRED"),
    (f"{PIPING}/core/serialization/canonical_json/src/lib.rs", "RFC 8785 canonical JSON behind the whole-model hash"),
    (f"{PIPING}/fixtures/canonical_hash/cases.json", "canonical hash vectors"),
    (f"{PIPING}/apps/desktop/src/services/operationBatchService.ts", "batch outcome type; apply/validate routes"),
    (f"{PIPING}/apps/desktop/src/types.ts", "OperationAcceptanceRecord; AppliedOperationReceipt (session receipt)"),
    (f"{PIPING}/apps/desktop/src/features/workspace/workspaceSession.ts",
     "batch Apply gated on the registered basis hash; session receipt minted in UI state; receipts reset on open/create"),
    (f"{PIPING}/apps/desktop/src/features/toolkit/BatchReviewPanel.tsx", "Clear pending changes and batches (no record)"),
    (f"{PIPING}/apps/desktop/src/features/offline-proposal-intake/OfflineProposalIntakePanel.tsx",
     "proposals arrive as files; author attribution not verified; no connected agent provider"),
    (f"{PIPING}/apps/desktop/src/features/workspace/shellLayout.ts", "Agent: not available yet"),
    (f"{PIPING}/apps/desktop/src/features/operations/OperationApplyPanel.tsx", "per-intent Apply of session-queued editor intents"),
    (f"{PIPING}/core/model_operations/audit_trail/engine.py",
     "DEL-16-03 accept/reject/held audit records with actor fields; not called by the Apply route"),
]

STALE_CODES = {"OP-STALE-BEFORE-VALUE", "OP-CLAIMED-MODEL-HASH-MISMATCH"}
BASIS_CLAIM_INVALID = {"OP-CLAIMED-MODEL-HASH-METADATA-INVALID", "OP-CLAIMED-MODEL-HASH-METADATA-UNSUPPORTED"}
AUTHORITY_CODES = {"OP-BEND-FLEXIBILITY-USER-ENTRY-REQUIRED"}

# Findings. NR-nn: what SWBPIPE would need to add for the App to form the record (sent to the piping project).
# A-nn: App-side gaps (DEL-03-02 / DEL-03-01 contract), for the App coordinator. Text is in SWBPIPE_CORPUS_RECEIVING.md.
NR = {
    "NR-01": "no attributable acceptance record per change (actor, act reference, capture time, capture evidence, bound content)",
    "NR-02": "no rejection record (A10); Clear discards without a record",
    "NR-03": "no per-change decision within a submission; agent proposals are applied as atomic batches",
    "NR-04": "no host-assigned change-item content identity",
    "NR-05": "no receipt reference on the outcome; the session receipt is UI state only and not durable",
    "NR-06": "basis on outcomes is the whole-model hash only: no model revision",
    "NR-07": "relied-on basis not carried: no claimed hash; per-field before-values are the only staleness guard",
    "NR-08": "no proposal record keyed by identity: no de-duplication before the basis check, no submission count, "
             "no observation by identity, no time",
    "NR-09": "no route for agent-originated proposals on main (offline file intake only; no live agent binding)",
    "NR-10": "no capability catalog: operation identity/version, declared errors, preconditions, class, exposure, edition",
    "NR-11": "an actor-dependent rule is a validation error on caller-asserted author_type, not a treatment on a verified actor",
}
APP = {
    "A-01": "no App representation for an application at a person-initiated host Apply without an attributable act record",
    "A-02": "resulting_object.relation has no 'removed' for a deletion",
    "A-03": "no element for an application's persistence status (session only, not saved)",
}
NEVER = ["acceptance by a named person (A5)", "a per-change act", "rejection (A10)", "withdrawal (A11)",
         "checking (A4)", "engineering approval (A6)", "professional reliance (A7)"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def corpus_files():
    return sorted((ROOT / CORPUS).glob("case_*.json"))


def write_pins():
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    files = [{"path": p, "sha256": sha(ROOT / p), "read_for": why} for p, why in SOURCES]
    files += [{"path": str(f.relative_to(ROOT)), "sha256": sha(f), "read_for": "corpus case"} for f in corpus_files()]
    doc = {"pin_kind": "swbpipe_sources_read", "repository": "sgttomas/chirality", "commit": commit,
           "read_on": subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip(),
           "standing": "read only; SWBPIPE files are data about SWBPIPE at this commit, not commitments (DECISION-3)",
           "files": files}
    PINS.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"pinned {len(files)} files at {commit}")


def verify_pins(fails):
    pins = json.loads(PINS.read_text())
    drift = [f["path"] for f in pins["files"] if not (ROOT / f["path"]).exists() or sha(ROOT / f["path"]) != f["sha256"]]
    pinned_cases = {f["path"] for f in pins["files"] if f["read_for"] == "corpus case"}
    present = {str(f.relative_to(ROOT)) for f in corpus_files()}
    check(fails, f"{len(pins['files'])} pinned SWBPIPE files match their bytes at commit {pins['commit'][:10]}", not drift,
          f"drifted: {drift[:5]}")
    check(fails, "the corpus has exactly the pinned cases (none added or removed)", pinned_cases == present,
          f"added {sorted(present - pinned_cases)[:3]} removed {sorted(pinned_cases - present)[:3]}")
    return pins


def check(fails, label, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {label}" + ("" if ok or not detail else f"  -- {detail}"))
    if not ok:
        fails.append(label)


def evaluated_basis(outcome):
    """C section 5.1 descriptor from what the host states. Nothing is computed by the App."""
    mb = outcome["model_basis"]
    return {"workspace_identity": {"not_supplied": "host_declares_none"},   # SQ-07 (a): none on main
            "generation": {"not_supplied": "host_declares_none"},
            "model_revision": {"not_supplied": "omitted"},                  # NR-06
            "canonical_content_identity": mb["backend_model_hash"],
            "identity_method": f"host: sha256 over {mb['backend_canonicalization']} canonical JSON of model_payload"}


def map_case(path):
    d = json.loads(path.read_text())
    intent, out = d["intent"], d["expected"]["outcome"]
    change = intent.get("change") or {}
    codes = sorted({x["code"] for x in out["diagnostics"]})
    blocking = sorted({x["code"] for x in out["diagnostics"] if x["severity"] == "blocking"})
    status = out["validation"]["application_status"]
    mb = out["model_basis"]
    claimed = d["claimed_model_hash"] is not None
    host = {"mode": d["mode"], "change_kind": change.get("change_kind"), "operation_kind": intent.get("operation_kind"),
            "target_ref": out.get("target_ref"), "author_type_asserted": intent.get("author_type"),
            "application_status": status, "diagnostic_codes": codes, "binding_status": mb["binding_status"],
            "claimed_model_hash": "present" if claimed else "absent",
            "acceptance": out["acceptance"], "diff_rows": len(out.get("diff_preview") or []),
            "resulting_whole_model_hash": d["expected"]["applied_model_canonical_sha256"]}
    terms = {"author_identity": "unverified (author_type is caller-asserted; SQ-14; R4-15)" if intent.get("author_type")
             else "not supplied (intent incomplete)",
             "evaluated_basis": evaluated_basis(out),
             "relied_on_basis": ("carried: the claimed whole-model hash" if claimed else
                                 "not carried: no claimed hash; per-field before-values guard staleness")}
    blocked_by, gaps = ["NR-04", "NR-06", "NR-08", "NR-09", "NR-10"], []
    if not claimed:
        blocked_by.append("NR-07")
    if d["mode"] == "validate_only":
        if blocking:
            outcome = "error"
            terms["outcome_statement"] = "C section 4.1 error of a non-mutating host check (validate-only preview)"
            terms["error_identities"] = blocking
        else:
            outcome = "success"
            terms["outcome_statement"] = ("non-mutating host check ran (validate-only preview, DEL-16-02): diff preview "
                                          "with old/new values; nothing queued, applied or accepted")
            terms["proposal_view_rows"] = host["diff_rows"]
    elif status == "applied_to_session_model":
        outcome = None
        terms["outcome_statement"] = ("no contract outcome: the host applied the change to its session model at the "
                                      "person's Apply, recording only acceptance basis "
                                      f"'{out['acceptance']['acceptance_basis']}'; P 'applied' needs branch "
                                      "after_acceptance with an A5 act record, or direct_under_grant, and neither holds")
        terms["host_stated_acceptance_basis"] = out["acceptance"]["acceptance_basis"]
        terms["resulting_revision"] = {"canonical_content_identity": host["resulting_whole_model_hash"],
                                       "model_revision": "not supplied"}
        rel = {"create": "created", "insert": "created", "connect": "created"}.get(intent.get("operation_kind"), "changed")
        if intent.get("operation_kind") == "delete":
            terms["resulting_objects"] = [{"object_identity": out["target_ref"], "relation": "removed (no App relation)"}]
            gaps.append("A-02")
        else:
            terms["resulting_objects"] = [{"object_identity": out["target_ref"], "relation": rel,
                                           "subject_content_identity": "not supplied (R8-4)"}]
        blocked_by[:0] = ["NR-01", "NR-05"]
        gaps[:0] = ["A-01"]
        gaps.append("A-03")
    elif set(blocking) & STALE_CODES:
        outcome = "refused_stale"
        if "OP-CLAIMED-MODEL-HASH-MISMATCH" in blocking:
            terms["staleness_scope"] = "whole_model"
            terms["failing_targets"] = "not supplied (host scope: whole model)"
        else:
            terms["staleness_scope"] = "host_stated_other: per-field before-value of the bound target"
            terms["failing_targets"] = sorted({r for x in out["diagnostics"] if x["code"] in STALE_CODES
                                               for r in x["affected_refs"]})
        terms["item_left_cause"] = "refused_stale"
        terms["error_identities"] = blocking
    else:
        outcome = "refused_invalid"
        terms["error_identities"] = blocking
        terms["item_left_cause"] = "refused_invalid"
        if set(blocking) & BASIS_CLAIM_INVALID:
            terms["note"] = ("the relied-on basis claim is malformed or of another method: incomparable (C section 5.2 "
                             "rule 6), never stale")
        if set(blocking) & AUTHORITY_CODES:
            terms["note"] = ("an authority difference (agent may not write k) received as the host states it; P section 2 "
                             "expects 'not permitted' naming the governing treatment, which the host does not supply")
            blocked_by.append("NR-11")
    if outcome in ("refused_stale", "refused_invalid"):
        terms["refusal_at"] = "the host's apply step (main validates again at Apply); nothing applied, no act recorded"
    return {"case_id": d["case_id"], "file": path.name, "sha256": sha(path), "host": host,
            "app": {"contract_outcome": outcome, "contract_terms": terms, "app_record_formable": False,
                    "blocked_by": sorted(set(blocked_by)), "app_gaps": gaps}}


def build(pins):
    rows = [map_case(f) for f in corpus_files()]
    counts = Counter(str(r["app"]["contract_outcome"]) for r in rows)
    return {"mapping_kind": "swbpipe_corpus_receiving", "format": "proposed-0.1", "evidence_label": "illustrative",
            "statement": ("A mapping of SWBPIPE's committed contract corpus into App contract terms. It observes no "
                          "SWBPIPE run, no App run and no person; no row establishes any human act."),
            "contracts": {"P": "DEL-03-02/P-v0.8 sections 2, 3.5, 4.1-4.3, 5, 9, 9.1, 10",
                          "C": "DEL-03-01/C-v0.8 sections 4.1, 5.1-5.4"},
            "sources": {"pins": PINS.name, "pins_sha256": sha(PINS), "commit": pins["commit"]},
            "no_row_establishes": NEVER,
            "findings": {"swbpipe_would_need": NR, "app_side": APP},
            "counts": {"cases": len(rows), **{k: counts[k] for k in sorted(counts)}},
            "cases": rows}


def invariants(doc, fails):
    rows = doc["cases"]
    check(fails, f"every corpus case mapped exactly once ({len(rows)})", len(rows) == len({r['case_id'] for r in rows}) == 84)
    text = json.dumps(rows)
    check(fails, "no row carries a decision, an A5/A10/A11, or an accepted/rejected/withdrawn outcome",
          not any(t in text for t in ('"decision"', '"A5"', '"A10"', '"A11"', '"accepted"', '"rejected"', '"withdrawn"')))
    applied = [r for r in rows if r["host"]["application_status"] == "applied_to_session_model"]
    check(fails, f"every host application ({len(applied)}) lands on no contract outcome, blocked by NR-01 and NR-05 (A-01)",
          applied and all(r["app"]["contract_outcome"] is None and {"NR-01", "NR-05"} <= set(r["app"]["blocked_by"])
                          and "A-01" in r["app"]["app_gaps"] for r in applied))
    check(fails, "no row is given an applied branch (after_acceptance or direct_under_grant)", '"branch"' not in text)
    refused = [r for r in rows if r["app"]["contract_outcome"] in ("refused_stale", "refused_invalid")]
    check(fails, f"every blocked apply ({len(refused)}) is 'refused', with an item-left cause and no act",
          all(r["host"]["application_status"] == "blocked" and r["app"]["contract_terms"]["item_left_cause"] ==
              r["app"]["contract_outcome"] for r in refused) and
          len(refused) == sum(1 for r in rows if r["host"]["application_status"] == "blocked"))
    stale = [r for r in refused if r["app"]["contract_outcome"] == "refused_stale"]
    check(fails, f"stale refusals ({len(stale)}) carry only host stale codes and a staleness scope",
          all(set(r["app"]["contract_terms"]["error_identities"]) <= STALE_CODES and "staleness_scope" in
              r["app"]["contract_terms"] for r in stale))
    check(fails, "the two validate-only previews are non-mutating outcomes (success / error), never queued or applied",
          sorted(r["app"]["contract_outcome"] for r in rows if r["host"]["mode"] == "validate_only") == ["error", "success"])
    check(fails, "no App record is formable for any case (every row names what blocks it)",
          all(not r["app"]["app_record_formable"] and r["app"]["blocked_by"] for r in rows))
    check(fails, "author identity is never verified", all(r["app"]["contract_terms"]["author_identity"].startswith(
        ("unverified", "not supplied")) for r in rows))
    check(fails, "the App computes no identity: every evaluated basis copies the host hash and marks the rest not supplied",
          all(r["app"]["contract_terms"]["evaluated_basis"]["model_revision"] == {"not_supplied": "omitted"} for r in rows))
    k = next(r for r in rows if r["file"].startswith("case_84_"))
    check(fails, "the agent-authored k refusal (case 84) is refused_invalid as the host states it, with NR-11",
          k["app"]["contract_outcome"] == "refused_invalid" and "NR-11" in k["app"]["blocked_by"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--write-pins", action="store_true")
    a = ap.parse_args()
    if a.write_pins:
        write_pins()
    fails = []
    pins = verify_pins(fails)
    doc = build(pins)
    invariants(doc, fails)
    if a.write:
        MAPPING.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    on_disk = json.loads(MAPPING.read_text()) if MAPPING.exists() else None
    check(fails, f"{MAPPING.name} equals the regenerated mapping", on_disk == doc)
    print("counts:", json.dumps(doc["counts"]))
    print(f"{'ALL CHECKS HOLD' if not fails else 'FAILED'}: {len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
