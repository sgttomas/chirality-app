"""Constructed CI-29 schema checks; no source/provider or performed-act claim."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent
old = json.loads((ROOT / "connector.route-account.schema.json").read_text())
new = json.loads((ROOT / "connector.route-account.v0.2.schema.json").read_text())
standing = json.loads((ROOT / "connector.standing.schema.json").read_text())
registry = Registry().with_resource(standing["$id"], Resource.from_contents(standing))
for schema in (old, new, standing):
    Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(new, registry=registry)
legacy = Draft202012Validator(old, registry=registry)
account = {
    "format": "chirality.connector.route-account", "formatVersion": "0.2",
    "account_id": "ra:CI29", "question": {"id": "Q1", "text": "What remains?", "at_revision": "requested-revision"},
    "trigger": {"connector": "pec", "why": "absent"}, "sources": [], "facts": [],
    "gaps": [{"gap": "Needed graph unavailable", "effect": "Q1 unsupported", "responsible": "project owner"}],
    "conclusions": {"supported": [], "unsupported": [{"conclusion": "Q1 answer", "why": "No source read"}],
        "prohibited": ["no_work", "ready", "permitted", "correct_by_presence"]},
    "duties": [{"duty": duty, "actor_role": role, "standing": "outstanding", "reason": "Not performed"}
        for duty, role in [("locate_compare", "agent"), ("review_integrate", "manager"), ("cross_undertaking_coordination", "person")]],
    "recorder": {"kind": "tool", "identity": "constructed-schema-check"}, "written_at": "2026-10-08T00:00:00Z", "written_at_source": "build_constant"
}
checks = 0
def expect(value, valid, checker=validator):
    global checks
    errors = list(checker.iter_errors(value))
    assert (not errors) == valid, [e.message for e in errors]
    checks += 1

expect(account, True)
for field in ("gaps",):
    bad = copy.deepcopy(account); bad[field] = []; expect(bad, False)
for field in ("unsupported", "prohibited"):
    bad = copy.deepcopy(account); bad["conclusions"][field] = []; expect(bad, False)
bad = copy.deepcopy(account); bad["facts"] = [{"fact_id": "f1", "statement": "invented", "source_id": "missing", "anchor": "x"}]; expect(bad, False)
bad = copy.deepcopy(account); bad["conclusions"]["supported"] = [{"statement": "invented", "basis": "source_route"}]; expect(bad, False)
bad = copy.deepcopy(account); del bad["gaps"][0]["responsible"]; expect(bad, False)
bad = copy.deepcopy(account); bad["duties"][0]["standing"] = "performed"; expect(bad, False)
read = copy.deepcopy(account); read["sources"] = [{"source_id": "s1", "path": "graph.json", "revision": "r1", "sha256": "a" * 64, "role": "graph"}]
read["facts"] = [{"fact_id": "f1", "statement": "constructed fact", "source_id": "s1", "anchor": "node"}]
read["conclusions"]["supported"] = [{"statement": "constructed answer part", "basis": "source_route", "refs": ["f1"]}]
expect(read, True)
for field in ("revision", "sha256", "path"):
    bad = copy.deepcopy(read); del bad["sources"][0][field]; expect(bad, False)
expect(read, False, legacy)
read["formatVersion"] = "0.1"; expect(read, True, legacy); expect(read, False)
bad = copy.deepcopy(account); bad["formatVersion"] = "0.1"; expect(bad, False, legacy)
print(f"CI-29 constructed schema checks: {checks} passed")
