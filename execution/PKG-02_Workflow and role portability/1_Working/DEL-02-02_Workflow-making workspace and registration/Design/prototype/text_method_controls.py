#!/usr/bin/env python3
"""Offline WR source-method controls only; no supplier, model, act or product proof."""
import copy
import json
from pathlib import Path
import unittest
import wrproto as wr

HERE = Path(__file__).resolve().parent


class TextMethodControls(unittest.TestCase):
    def setUp(self):
        self.registry = wr.minischema.Registry()
        self.registry.add(wr.wdproto.load(wr.wdproto.SCHEMA_PATH))
        self.registry.load(wr.SCHEMA)
        self.schema = self.registry.by_id[wr.WR_ID]
        self.fixture = json.loads((HERE / "fixtures/text-method-controls.json").read_text())
        self.valid_bytes = Path(wr.VALID).read_bytes()
        self.records = [json.loads(line) for line in self.valid_bytes.splitlines()]

    def validate(self, value, kind):
        return wr.minischema.validate(value, {"$ref": wr.WR_ID + "#/$defs/" + kind}, self.registry)

    def test_known_vector_and_no_normalization(self):
        self.assertEqual(wr.tsha("abc"), {"method": wr.TEXT_METHOD, "value": self.fixture["value"]})
        self.assertNotEqual(wr.tsha("a\n"), wr.tsha("a\r\n"))
        self.assertNotEqual(wr.tsha("é"), wr.tsha("e\u0301"))
        self.assertNotEqual(wr.tsha("abc"), wr.tsha("abc "))

    def test_opaque_carriage_and_value_gate(self):
        for method in self.fixture["methods"]:
            identity = {"method": method, "value": self.fixture["value"]}
            before = copy.deepcopy(identity)
            self.assertEqual(self.validate(identity, "text_identity"), [])
            self.assertEqual(identity, before)
        for bad in [{"method": "", "value": self.fixture["value"]},
                    {"method": wr.TEXT_METHOD, "value": "ABC"},
                    {"value": self.fixture["value"]}]:
            self.assertTrue(self.validate(bad, "text_identity"))

    def test_new_composition_and_source_scopes(self):
        original = next(r for r in self.records if r.get("purpose") == "run start")
        desk = wr.RunDesk(None)
        text, rec = desk.compose_start({"identity": original["workflow"], "holding_library": original["holding_library"], "selection_id": "synthetic-selection"},
            str(HERE / "fixtures/review-pack"), "new-method-run", "synthetic-thread", None,
            original["origin_of_start"], "synthetic-folder")
        self.assertEqual(rec["text_identity"], wr.tsha(text))
        self.assertEqual(rec["workflow_file"]["content"]["method"], wr.TEXT_METHOD)
        raw = (HERE / "fixtures/review-pack/WORKFLOW.md").read_bytes()
        self.assertEqual(wr.extract_body(text, rec["workflow"]).encode("utf-8"), raw)
        self.assertEqual(rec["workflow_file"]["content"], wr.tsha(raw.decode("utf-8")))
        self.assertNotEqual(rec["text_identity"], rec["workflow_file"]["content"])
        self.assertEqual(self.validate(rec, "run_text"), [])

    def test_actual_check_path_same_value_different_methods(self):
        class Sink:
            def emit(self, value):
                return value
        desk = wr.RunDesk(Sink())
        for method in self.fixture["methods"]:
            rec = {"run": "synthetic", "conversation": "thread", "purpose": "run end notice",
                   "text_identity": {"method": method, "value": self.fixture["value"]}}
            before = copy.deepcopy(rec)
            def read(params):
                self.assertEqual(params, {"threadId": "thread", "turnId": "turn"})
                return {"data": [{"turnId": "turn", "item": {"id": "item", "type": "userMessage",
                    "content": [{"type": "text", "text": "abc"}]}}], "nextCursor": None}
            result = desk.check(read, rec, "abc", "turn", None, "synthetic-time")
            self.assertEqual(result["state"], "verified" if method == wr.TEXT_METHOD else "incomparable")
            self.assertEqual(result["expected_text"], rec["text_identity"])
            self.assertEqual(result["observed_text"], wr.tsha("abc"))
            self.assertEqual(rec, before)
            self.assertEqual(self.validate(result, "supply_check"), [])
            if method != wr.TEXT_METHOD:
                self.assertTrue(any("incomparable" in x for x in result["evidence_limits"]))

    def test_body_fallback_requires_same_method(self):
        original = next(r for r in self.records if r.get("purpose") == "run start")
        text, rec = wr.RunDesk(None).compose_start({"identity": original["workflow"], "holding_library": original["holding_library"], "selection_id": "synthetic-selection"},
            str(HERE / "fixtures/review-pack"), "new-method-run", "synthetic-thread", None,
            original["origin_of_start"], "synthetic-folder")
        changed = "framing changed\n" + text
        self.assertEqual(wr.text_standing(changed, rec), "text differs, workflow bytes equal")
        rec["workflow_file"]["content"]["method"] = wr.LEGACY_TEXT_METHOD
        self.assertEqual(wr.text_standing(changed, rec), "incomparable")
        # Equal full text under its designated method requires no body fallback.
        self.assertEqual(wr.text_standing(text, rec), "verified")

    def test_historical_examples_unchanged_and_valid(self):
        for rec in self.records:
            if rec["record_kind"] in ("run_text", "supply_check"):
                self.assertEqual(self.validate(rec, rec["record_kind"]), [])
        self.assertEqual(Path(wr.VALID).read_bytes(), self.valid_bytes)


if __name__ == "__main__":
    unittest.main()
