"""Invented offline fixtures only. Run directly; unittest discovery is not needed."""
import copy
import json
import unittest
from swbpipe_projection import CATALOG_PATH, ROOT, Pending, declarations, expand, response, validate

CAT = json.loads(CATALOG_PATH.read_text())
HASH = {"algorithm": "sha256", "canonicalization": "rfc8785_jcs", "payload_scope": "model_payload",
        "payload_ref": "invented:model", "value": "a" * 64, "hash_status": "computed_local_preview"}
BASIS = {"workspaceHandle": "invented:workspace", "applicationGeneration": 1, "modelRevision": 2,
         "modelHash": HASH, "stateId": None, "runId": None}
BINDING = {"requestRef": "invented:request", "rpcId": 7, "threadId": "invented:thread",
           "turnId": "invented:turn", "callId": "invented:call", "tool": "swbpipe_read_nodes",
           "workspaceHandle": BASIS["workspaceHandle"], "applicationGeneration": 1, "modelRevision": 2}
ARGS = {"workspaceHandle": BASIS["workspaceHandle"], "basis": BASIS, "page": {"cursor": None, "limit": 2}}
RESULT = {"status": "ok", "basis": BASIS, "message": "Invented bounded page.",
          "data": {"nodes": [{"id": "invented:node", "position": {"x": 0, "y": 1, "z": 2}, "unit": "m"}],
                   "projectUnits": {"length": "m"}, "nextCursor": None}}


class Projection(unittest.TestCase):
    def pending(self, args=None):
        return Pending(CAT, BINDING, json.dumps(ARGS if args is None else args).encode(), BASIS)

    def test_supported_pinned_declaration_and_response_fields(self):
        pin = ROOT / "app/src-tauri/resources/supplier/0.160.0"
        schema = json.loads((pin / "codex_app_server_protocol.v2.schemas.json").read_text())
        definition = schema["definitions"]["DynamicToolSpec"]["oneOf"][0]
        projected = declarations(CAT)
        self.assertEqual(len(projected), 6)
        for tool in projected:
            self.assertEqual(set(tool), {"type", "name", "description", "inputSchema"})
            self.assertLessEqual(set(tool), set(definition["properties"]))
            self.assertNotIn("$ref", json.dumps(tool))
        schema = json.loads((pin / "codex_app_server_protocol.schemas.json").read_text())
        wire = self.pending().complete(BINDING, RESULT, BASIS)
        self.assertEqual(set(wire["result"]), set(schema["definitions"]["DynamicToolCallResponse"]["required"]))
        self.assertEqual(wire["result"]["contentItems"][0]["type"], "inputText")
        self.assertEqual(json.loads(wire["result"]["contentItems"][0]["text"]), RESULT)
        self.assertEqual(wire["id"], 7)

    def test_wrong_binding_and_duplicate(self):
        pending = self.pending()
        for key in BINDING:
            changed = dict(BINDING, **{key: "wrong"})
            with self.subTest(key=key), self.assertRaises(ValueError):
                pending.complete(changed, RESULT, BASIS)
        pending.complete(BINDING, RESULT, BASIS)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            pending.complete(BINDING, RESULT, BASIS)

    def test_wrong_generation_and_basis_never_complete(self):
        for key, value in [("applicationGeneration", 2), ("modelRevision", 3),
                           ("workspaceHandle", "other"), ("modelHash", dict(HASH, value="b" * 64))]:
            changed = dict(BASIS, **{key: value})
            for current, result in [(changed, RESULT), (BASIS, dict(RESULT, basis=changed))]:
                with self.subTest(key=key), self.assertRaises(ValueError):
                    self.pending().complete(BINDING, result, current)
        args = copy.deepcopy(ARGS)
        args["basis"]["modelRevision"] = 99
        with self.assertRaises(ValueError):
            self.pending(args)

    def test_bounds_and_schema_refusals(self):
        for limit in [0, 51, True]:
            args = copy.deepcopy(ARGS)
            args["page"]["limit"] = limit
            with self.assertRaises(ValueError):
                self.pending(args)
        with self.assertRaises(ValueError):
            self.pending(dict(ARGS, path="/invented/not-permitted"))
        with self.assertRaises(ValueError):
            Pending(CAT, BINDING, b" " * (CAT["limits"]["argumentBytes"] + 1), BASIS)
        bad = copy.deepcopy(RESULT)
        bad["data"]["nodes"][0]["position"]["x"] = float("nan")
        with self.assertRaises(ValueError):
            self.pending().complete(BINDING, bad, BASIS)

    def test_domain_rejection_and_execution_error(self):
        tool = next(t for t in CAT["tools"] if t["name"] == "swbpipe_propose_operations")
        for status, success in [("rejected", True), ("stale_basis", True), ("execution_error", False)]:
            wire = response(CAT, tool, dict(RESULT, status=status, data=None))
            self.assertEqual(wire["success"], success)
        with self.assertRaises(ValueError):
            response(CAT, tool, dict(RESULT, status="pending_review", data=None))

    def test_native_intent_discriminators_and_solve_claim(self):
        tool = next(t for t in CAT["tools"] if t["name"] == "swbpipe_propose_operations")
        schema = expand(CAT, tool["inputSchema"])
        native = expand(CAT, CAT["definitions"]["operationIntent"])
        self.assertEqual(native["properties"]["change"]["properties"]["change_kind"], {"const": "set_field"})
        self.assertEqual(native["properties"]["author_type"], {"const": "agent"})
        self.assertNotIn("maxItems", schema["properties"]["operations"])
        solve = next(t for t in CAT["tools"] if t["name"] == "swbpipe_solve")
        args = {"workspaceHandle": BASIS["workspaceHandle"], "basis": BASIS, "claimedModelHash": HASH}
        binding = dict(BINDING, tool=solve["name"])
        Pending(CAT, binding, json.dumps(args).encode(), BASIS)
        args["claimedModelHash"] = dict(HASH, value="b" * 64)
        with self.assertRaisesRegex(ValueError, "claimed hash"):
            Pending(CAT, binding, json.dumps(args).encode(), BASIS)
        del args["claimedModelHash"]
        with self.assertRaises(ValueError):
            Pending(CAT, binding, json.dumps(args).encode(), BASIS)

    def test_native_proposal_fixture_units_limits_and_attribution(self):
        intent = {
            "operation_id": "invented:operation", "operation_kind": "modify",
            "operation_status": "proposed", "author_type": "agent",
            "target": {"object_type": "Node", "ref": "invented:node"},
            "change": {"change_id": "invented:change", "change_kind": "set_field",
                       "field_label": "position.x", "field_path": "position.x",
                       "before": "0", "after": "1", "unit": "m", "dimension": "length",
                       "source_note": "Invented offline fixture"},
            "validation": {key: "not_run" for key in
                           ["schema_validation", "constraint_validation", "unit_validation",
                            "diff_preview_status", "application_status"]},
            "audit_boundary": {"mutation_route": "structured_operations_only",
                               "direct_model_mutation_allowed": False,
                               "requires_user_acceptance": True, "mutates_accepted_model_state": False},
            "professional_boundary": {key: key == "human_review_required" for key in
                                      ["human_review_required", "software_makes_compliance_claim",
                                       "software_makes_certification_claim", "software_makes_sealing_claim",
                                       "software_makes_approval_claim", "software_makes_authentication_claim"]},
            "rationale": "Invented coordinate adjustment"}
        args = {"workspaceHandle": BASIS["workspaceHandle"], "basis": BASIS,
                "claimedModelHash": HASH, "operations": [intent]}
        binding = dict(BINDING, tool="swbpipe_propose_operations")
        def admit(value, cat=CAT):
            return Pending(cat, binding, json.dumps(value).encode(), BASIS, {"length": "m"})
        pending = admit(args)
        outcome = dict(RESULT, status="pending_review",
                       data={"proposalHandle": "invented:proposal", "author_type": "agent"})
        self.assertTrue(pending.complete(binding, outcome, BASIS)["result"]["success"])
        bad = copy.deepcopy(args)
        bad["operations"][0]["change"]["unit"] = "mm"
        with self.assertRaisesRegex(ValueError, "unit mismatch"):
            admit(bad)
        bad = copy.deepcopy(args)
        bad["operations"][0]["author_type"] = "user"
        with self.assertRaises(ValueError):
            admit(bad)
        configured = copy.deepcopy(CAT)
        configured["limits"]["proposalOperations"] = 1
        with self.assertRaisesRegex(ValueError, "batch limit"):
            admit(dict(args, operations=[intent, intent]), configured)

    def test_summary_and_withheld_results(self):
        summary = next(t for t in CAT["tools"] if t["name"] == "swbpipe_read_model_summary")
        validate({}, expand(CAT, summary["inputSchema"]))
        with self.assertRaises(ValueError):
            validate({"basis": BASIS}, expand(CAT, summary["inputSchema"]))
        results = next(t for t in CAT["tools"] if t["name"] == "swbpipe_read_results")
        row = {"id": "invented:row", "kind": "displacement", "entityRef": "invented:node",
               "value": None, "exactDecimal": None, "unit": "m", "availability": "withheld", "reason": "view floor"}
        value = dict(RESULT, data={"runHandle": "invented:run", "runId": "invented:run-id",
                     "evaluatedModelHash": HASH, "values": [row], "nextCursor": None,
                     "standing": {"route": "invented", "health": "not_assessed", "checks": ["not_run"]}})
        self.assertTrue(response(CAT, results, value)["success"])
        row["value"] = 3
        with self.assertRaisesRegex(ValueError, "withheld"):
            response(CAT, results, value)


if __name__ == "__main__":
    unittest.main()
