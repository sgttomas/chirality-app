"""CAM-v0.1 maintained schema shapes; constructed only, no producer/witness claim."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent
schema = json.loads((ROOT / "connector.route-account.v0.3.schema.json").read_text())
standing = json.loads((ROOT / "connector.standing.schema.json").read_text())
Draft202012Validator.check_schema(schema)
registry = Registry().with_resource(standing["$id"], Resource.from_contents(standing))
validator = Draft202012Validator(schema, registry=registry)
legacy = Draft202012Validator(json.loads((ROOT / "connector.route-account.v0.2.schema.json").read_text()), registry=registry)
H = "a" * 64
OID = "b" * 40
account = {
    "format": "chirality.connector.route-account", "formatVersion": "0.3",
    "standing": "source_evidence_draft", "account_id": "ra:constructed-cam",
    "question": {"id": "Q1", "text": "What does the source record?", "at_revision": OID},
    "trigger": {"connector": "pec", "why": "constructed absent", "standing": "constructed", "receiving_records": []},
    "sources": [], "facts": [],
    "gaps": [{"gap": "Source not available in constructed case", "effect": "No source-derived answer", "responsible": {"standing": "unassigned", "identity": None}, "origin": "observed_git_failure", "context": {"side": "at", "requested_commit": OID, "path": "graph.md"}}],
    "conclusions": {"supported": [], "unsupported": [{"conclusion": "Factual answer", "why": "Not established by this evidence draft"}], "prohibited": ["no_work", "ready", "permitted", "correct_by_presence"]},
    "duties": [{"duty": duty, "actor_role": role, "standing": "outstanding", "reason": "Explicit constructed caller input; no act observed", "assertion_standing": "caller_reported_unverified"} for duty, role in [("locate_compare", "agent"), ("review_integrate", "manager"), ("cross_undertaking_coordination", "person")]],
    "recorder": {"kind": "app", "identity": "constructed-app-instance"}, "written_at": "2026-10-08T00:00:00Z", "written_at_source": "observed_clock",
    "evidence": {"kind": "host_observed_git_receipt", "project_identity": {"device": "1", "inode": "9007199254740993"}, "project_display": "/synthetic/project", "association_sha256": H, "engine_sha256": H, "git_request": {"at": OID, "since": None}, "selection_mechanism": "synthetic_test_callback", "verification_limit": "same_engine_consistency_not_truth_authorship_or_authority", "custody_limit": "stored_receipt_not_hot_capability_or_independent_reverification"},
    "interpretations": []
}
checks = 0
def expect(value, valid, check=validator):
    global checks
    errors = list(check.iter_errors(value))
    assert (not errors) == valid, [e.message for e in errors]
    checks += 1

def changed(path, value):
    result = copy.deepcopy(account)
    obj = result
    for key in path[:-1]:
        obj = obj[key]
    obj[path[-1]] = value
    return result

expect(account, True)
expect(account, False, legacy)
for path, value in [
    (["formatVersion"], "0.2"),
    (["standing"], "accepted"),
    (["facts"], [{"fact_id": "f", "statement": "claim", "source_id": "s", "anchor": "L1"}]),
    (["conclusions", "supported"], [{"statement": "claim", "basis": "source_route"}]),
    (["conclusions", "unsupported"], []),
    (["conclusions", "prohibited"], []),
    (["duties", 0, "standing"], "performed"),
    (["duties", 0, "standing"], "not_required"),
    (["duties", 0, "actor_role"], "person"),
    (["gaps", 0, "responsible"], "guessed person"),
    (["gaps", 0, "responsible"], {"standing": "unassigned", "identity": "person"}),
    (["gaps", 0, "responsible"], {"standing": "caller_assigned", "identity": None}),
    (["recorder", "kind"], "person"),
    (["written_at_source"], "build_constant"),
    (["trigger", "standing"], "actual"),
    (["evidence", "custody_limit"], "verified"),
    (["evidence", "project_identity", "inode"], 9007199254740993),
    (["evidence", "git_request", "at"], "HEAD"),
    (["gaps"], []),
]:
    expect(changed(path, value), False)
expect(changed(["gaps", 0, "responsible"], {"standing": "caller_assigned", "identity": "explicit caller assignment"}), True)
source = {"source_id": "s1", "path": "graph.md", "revision": OID, "sha256": H, "role": "caller-described record", "role_standing": "caller_assertion", "provenance": {"side": "at", "object_format": "sha1", "commit": OID, "root_tree": OID, "blob": OID, "mode": "100644", "raw_commit_sha256": H, "traversal_sha256": H, "observed_at": "2026-10-08T00:00:00Z", "time_provenance": "observed_clock", "verification": "same_engine_object_id_consistency", "observation_reference": "constructed-git-side"}, "excerpts": []}
with_source = changed(["sources"], [source])
expect(with_source, True)
for field in ("provenance", "role_standing", "excerpts"):
    bad = copy.deepcopy(with_source); del bad["sources"][0][field]; expect(bad, False)
bad = copy.deepcopy(with_source); bad["sources"][0]["provenance"]["mode"] = "160000"; expect(bad, False)
bad = copy.deepcopy(with_source); bad["sources"] *= 3; expect(bad, False)
for field in ("standing", "evidence", "interpretations"):
    bad = copy.deepcopy(account); del bad[field]; expect(bad, False)
print(f"CAM constructed schema shape checks: {checks} passed; semantic producer checks remain separate")
