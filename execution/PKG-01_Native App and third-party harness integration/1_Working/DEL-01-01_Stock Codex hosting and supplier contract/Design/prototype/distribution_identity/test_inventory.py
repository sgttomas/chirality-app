import copy
import hashlib
import json
from pathlib import Path
import unittest
from inventory_model import VALIDATOR, validate, manifest, compare, prepend_path

FIXTURE = json.loads(Path(__file__).with_name("synthetic-inventory.json").read_text())


class InventoryContract(unittest.TestCase):
    def change(self, path, field, value):
        item = copy.deepcopy(FIXTURE)
        next(e for e in item["entries"] if e["path"] == path)[field] = value
        item["manifest_sha256"] = manifest(item["entries"])
        return item

    def test_schema_and_positive(self):
        VALIDATOR.check_schema(VALIDATOR.schema)
        self.assertEqual(validate(FIXTURE), [])
        self.assertTrue(compare(FIXTURE, copy.deepcopy(FIXTURE))["equal"])

    def test_fixed_multibyte_vector_and_order(self):
        # Independent exact expected bytes: digest of b"abc" and a non-ASCII path.
        entries = [{"kind":"file", "path":"é.txt", "sha256":
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}]
        raw = b"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  \xc3\xa9.txt\n"
        self.assertEqual(manifest(entries), hashlib.sha256(raw).hexdigest())
        self.assertEqual(manifest(FIXTURE["entries"]), manifest(list(reversed(FIXTURE["entries"]))))
        self.assertNotEqual(hashlib.sha256(raw[:-1]).hexdigest(), manifest(entries))

    def test_resource_change_unchanged_main(self):
        changed = self.change("codex-resources/é.txt", "sha256", "0" * 64)
        self.assertFalse(compare(FIXTURE, changed)["equal"])
        self.assertEqual(compare(FIXTURE, changed)["changed"], ["codex-resources/é.txt"])

    def test_modes_sizes_empty_directories(self):
        for path in (".", "bin", "bin/codex"):
            with self.subTest(path=path):
                changed = self.change(path, "mode", 448)
                self.assertEqual(changed["manifest_sha256"], FIXTURE["manifest_sha256"])
                self.assertFalse(compare(FIXTURE, changed)["equal"])
        self.assertFalse(compare(FIXTURE, self.change("bin/codex", "size", 999))["equal"])
        changed=copy.deepcopy(FIXTURE)
        changed["entries"]=[e for e in changed["entries"] if e["path"] != "codex-resources/empty"]
        self.assertEqual(validate(changed), [])
        self.assertFalse(compare(FIXTURE, changed)["equal"])

    def test_duplicate_and_missing_parent(self):
        changed=copy.deepcopy(FIXTURE); changed["entries"].append(changed["entries"][0])
        self.assertTrue(validate(changed))
        self.assertTrue(validate(self.change("codex-resources/é.txt", "path", "missing/x")))

    def test_invalid_paths_and_types(self):
        for path in ("/escape", "../escape", "bin/../escape", "bin//x", "bin/x\n", "bin/x\r", "bin/x\0", "bin/x\\y", "bin/."):
            with self.subTest(path=path):
                changed=copy.deepcopy(FIXTURE)
                changed["entries"][-1]["path"]=path
                self.assertTrue(validate(changed))
        for kind in ("symlink", "fifo", "socket"):
            changed=copy.deepcopy(FIXTURE); changed["entries"][-1]["kind"]=kind
            self.assertTrue(validate(changed))
        changed=copy.deepcopy(FIXTURE); changed["entries"][-1]["path"]="\ud800"
        self.assertTrue(validate(changed))

    def test_missing_invalid_method_and_manifest(self):
        for key,value in (("method","unknown"),("algorithm","md5"),("manifest_sha256","0"*64)):
            changed=copy.deepcopy(FIXTURE); changed[key]=value
            self.assertTrue(validate(changed))
            self.assertFalse(compare(FIXTURE,changed)["equal"])
        changed=copy.deepcopy(FIXTURE); del changed["entries"]
        self.assertTrue(validate(changed))

    def test_path_relocation_and_inheritance(self):
        self.assertEqual(prepend_path("/App With Spaces/codex-path", ":/usr/bin:"),
                         "/App With Spaces/codex-path::/usr/bin:")
        self.assertEqual(prepend_path("/a", None), "/a")
        self.assertEqual(prepend_path("/a", ""), "/a:")
        for prefix in ("/a:b/codex-path", "", "/a\0"):
            with self.assertRaises(ValueError): prepend_path(prefix, "/usr/bin")


if __name__ == "__main__":
    unittest.main()
