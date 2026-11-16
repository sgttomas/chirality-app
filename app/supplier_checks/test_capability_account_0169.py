"""The account covers the actual pinned protocol, with no duplicate or omitted identity."""
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


class CapabilityAccount(unittest.TestCase):
    def test_every_generated_identity_has_one_group_signal_and_standing(self):
        account = json.loads((HERE / "capability_account_0.169.0.json").read_bytes())
        root = HERE.parent / "src-tauri/resources/supplier/0.169.0"
        main = json.loads((root / "codex_app_server_protocol.schemas.json").read_bytes())["definitions"]
        v2 = json.loads((root / "codex_app_server_protocol.v2.schemas.json").read_bytes())["definitions"]
        expected = {(kind, row["properties"]["method"]["enum"][0])
                    for kind in ("ClientRequest", "ServerRequest", "ServerNotification", "ClientNotification")
                    for row in main[kind]["oneOf"]}
        expected |= {("ThreadItem", row["properties"]["type"]["enum"][0]) for row in v2["ThreadItem"]["oneOf"]}
        actual = [(row["kind"], row["name"]) for row in account["items"]]
        self.assertEqual(len(actual), len(set(actual)))
        self.assertEqual(set(actual), expected)
        for row in account["items"]:
            with self.subTest(kind=row["kind"], name=row["name"]):
                self.assertIn(row["standing"], ("stable", "experimental"))
                for field in ("capability_group", "standing_signal", "availability_signal", "generated_definition"):
                    self.assertTrue(isinstance(row[field], str) and row[field].strip())
                self.assertIn("/d32063f96c2dff1dc96af839b3952abb6acfeda4/", row["source"])


if __name__ == "__main__":
    unittest.main()
