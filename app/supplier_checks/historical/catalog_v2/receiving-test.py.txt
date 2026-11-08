"""Opt-in offline checks against exact receiving bytes, never a sibling-dependent default test.

Usage: python3 swbpipe_receiving_test.py --catalog <exported committed JSON>
No processes or network; reads only supplied catalog and existing local fixtures.
"""
import argparse
import copy
import hashlib
import json
import unittest
from pathlib import Path
from swbpipe_projection import Pending, expand, validate, validate_assumptions
from swbpipe_projection_test import BASIS, BINDING, HASH, ARGS, RESULT, CAT

RECEIVING_SHA256 = "fe1439998d709e5f3e9641a4d39567000ced56c498fab5b6b8f2028df7c9f669"
V2 = None
LATER = dict(BASIS, modelRevision=3, modelHash=dict(HASH, value="b" * 64))


class Receiving(unittest.TestCase):
    def call(self, tool, args, current=BASIS, record=None):
        binding = dict(BINDING, tool=tool)
        return Pending(V2, binding, json.dumps(args).encode(), current, retained_record=record), binding

    def finish(self, pending, binding, result, current=LATER):
        record = {"binding": copy.deepcopy(binding), "basis": copy.deepcopy(BASIS), "result": copy.deepcopy(result)}
        return pending.complete(binding, result, current, retained_record=record)

    def test_applied_observation_survives_live_edit_and_refuses_forgery(self):
        args = {"workspaceHandle": BASIS["workspaceHandle"], "basis": BASIS, "proposalHandle": "invented:proposal"}
        retained = {"basis": BASIS, "handle": args["proposalHandle"]}
        pending, binding = self.call("swbpipe_observe_proposal", args, LATER, retained)
        result = dict(RESULT, status="applied", data={"proposalHandle": args["proposalHandle"],
                      "proposalBasis": BASIS, "outcomeModelHash": LATER["modelHash"],
                      "author_type": "agent", "assumptions": []})
        record = {"binding": binding, "basis": BASIS, "result": copy.deepcopy(result)}
        forged = copy.deepcopy(result)
        forged["data"]["outcomeModelHash"] = HASH
        with self.assertRaisesRegex(ValueError, "forged"):
            pending.complete(binding, forged, LATER, retained_record=record)
        with self.assertRaisesRegex(ValueError, "detached"):
            pending.complete(binding, result, LATER, retained_record=record, session_attached=False)
        self.assertTrue(self.finish(pending, binding, result)["result"]["success"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.finish(pending, binding, result)
        for wrong in [dict(LATER, workspaceHandle="wrong"), dict(LATER, applicationGeneration=2)]:
            with self.assertRaises(ValueError):
                self.call("swbpipe_observe_proposal", args, wrong, retained)

    def test_solve_completes_against_admitted_basis_after_edit(self):
        args = {"workspaceHandle": BASIS["workspaceHandle"], "basis": BASIS, "claimedModelHash": HASH}
        pending, binding = self.call("swbpipe_solve", args)
        result = dict(RESULT, status="completed", data={"runHandle": "invented:run",
                      "runId": "invented:run-id", "evaluatedModelHash": HASH,
                      "health": "not_assessed", "solverMode": "invented-mode"})
        self.assertTrue(self.finish(pending, binding, result)["result"]["success"])
        with self.assertRaises(ValueError):
            self.call("swbpipe_solve", args, LATER)

    def test_historical_result_pages_bind_retained_run(self):
        args = dict(ARGS, runHandle="invented:run")
        retained = {"basis": BASIS, "handle": args["runHandle"]}
        pending, binding = self.call("swbpipe_read_results", args, LATER, retained)
        result = dict(RESULT, data={"runHandle": args["runHandle"], "runId": "invented:run-id",
                      "evaluatedModelHash": HASH, "values": [], "nextCursor": None,
                      "standing": {"route": "invented", "health": "not_assessed", "checks": ["not_run"]}})
        self.assertTrue(self.finish(pending, binding, result)["result"]["success"])
        with self.assertRaisesRegex(ValueError, "handle"):
            self.call("swbpipe_read_results", dict(args, runHandle="wrong"), LATER, retained)
        pending, binding = self.call("swbpipe_read_results", args, LATER, retained)
        with self.assertRaisesRegex(ValueError, "rebased"):
            self.finish(pending, binding, dict(result, basis=LATER))

    def test_live_reads_still_refuse_revision_drift(self):
        pending, binding = self.call("swbpipe_read_nodes", ARGS)
        with self.assertRaisesRegex(ValueError, "basis changed"):
            pending.complete(binding, RESULT, LATER)
        with self.assertRaises(ValueError):
            self.call("swbpipe_read_nodes", ARGS, LATER)

    def test_assumptions_are_required_bounded_and_referential(self):
        schema = expand(V2, V2["definitions"]["assumptions"])
        assumptions = [{"assumptionId": "invented:a", "statement": "Invented context",
                        "affectedOperationIds": ["invented:op"]}]
        validate(assumptions, schema)
        validate([], schema)
        validate_assumptions([{"operation_id": "invented:op"}], assumptions)
        for value in [assumptions * 17, [dict(assumptions[0], affectedOperationIds=["invented:op"] * 2)]]:
            with self.assertRaises(ValueError):
                validate(value, schema)
        for value in [assumptions * 2, [dict(assumptions[0], affectedOperationIds=["wrong"])]]:
            with self.assertRaises(ValueError):
                validate_assumptions([{"operation_id": "invented:op"}], value)
        self.assertIn("assumptions", V2["definitions"]["proposeInput"]["required"])
        self.assertEqual(V2["definitions"]["operationIntent"], CAT["definitions"]["operationIntent"])

    def test_submission_terminal_statuses_match_settled_interface(self):
        statuses = V2["definitions"]["proposeOutput"]["properties"]["status"]
        for status in ("pending_review", "rejected", "withdrawn", "applied", "unknown"):
            validate(status, statuses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    options = parser.parse_args()
    raw = Path(options.catalog).read_bytes()
    if hashlib.sha256(raw).hexdigest() != RECEIVING_SHA256:
        parser.error("catalog does not match the reviewed receiving revision")
    V2 = json.loads(raw)
    unittest.main(argv=[__file__])
