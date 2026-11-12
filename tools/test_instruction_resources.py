"""The packaged App instruction tree keeps its reviewed payload and bindings."""
import hashlib
import json
from pathlib import Path
import stat
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / "app/src-tauri/resources/instructions"
FILES = (
    "AGENTS.md", "ROLE_SET_SOURCE_BINDING.json",
    "agents/AGENT_HELPS_HUMANS.md", "agents/AGENT_HELP_HUMAN.md",
    "agents/AGENT_TASK.md", "agents/AGENT_WORKING_ITEMS.md", "roles.json",
)
# The App's own instruction documents, packaged beside the bound role-set
# payload but outside it: the role set and its source binding do not name them.
APP_OWN = {"DELEGATION_RECORDS.md": "80c52d8c9fb5765fb6c3ac8b66b6b601476f5f613262f9f0fdc43042b4173d4c"}


class PackagedInstructionTests(unittest.TestCase):
    def test_current_payload_and_role_binding_are_preserved(self):
        entries = sorted(INSTRUCTIONS.rglob("*"))
        files = [path for path in entries if not path.is_dir() or path.is_symlink()]
        self.assertEqual(sorted(path.relative_to(INSTRUCTIONS).as_posix() for path in files), sorted(FILES + tuple(APP_OWN)))
        self.assertEqual([path.name for path in entries if path.is_dir() and not path.is_symlink()], ["agents"])
        for path in files:
            meta = path.lstat()
            self.assertTrue(stat.S_ISREG(meta.st_mode) and meta.st_nlink == 1, path)
        source = {name: (INSTRUCTIONS / name).read_bytes() for name in FILES}
        lines = b"".join(f"{hashlib.sha256(source[p]).hexdigest()}  {p}\n".encode() for p in sorted(source))
        self.assertEqual(hashlib.sha256(lines).hexdigest(), "2b12b8435270f508ea3909994e39852f08879d4dde8ea400b85256cc54cdbcdf")
        binding = json.loads(source["ROLE_SET_SOURCE_BINDING.json"])
        self.assertEqual(binding["basisCommit"], "89acac6a3983c605820496d0d121c73bb2297706")
        self.assertEqual(hashlib.sha256(source["ROLE_SET_SOURCE_BINDING.json"]).hexdigest(), "1cd505a5079e8210a1bfd387e97a7b578e893527c4365a2bb8c890c962966b4b")
        roles = json.loads(source["roles.json"])["roles"]
        self.assertEqual([r["name"] for r in roles], ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"])
        self.assertTrue(all(r["default_for_new_chat"] is False for r in roles))
        for guidance in binding["guidance"]:
            self.assertEqual(hashlib.sha256(source[guidance["path"]]).hexdigest(), guidance["sha256"])

    def test_app_own_documents_are_named_and_kept_apart_from_the_role_set(self):
        binding = json.loads((INSTRUCTIONS / "ROLE_SET_SOURCE_BINDING.json").read_bytes())
        roles = json.loads((INSTRUCTIONS / "roles.json").read_bytes())["roles"]
        bound = {g["path"] for g in binding["guidance"]} | {binding["roleSet"]["path"]}
        for path, digest in APP_OWN.items():
            self.assertNotIn(path, bound)
            self.assertNotIn(path, {r["guidance_file"] for r in roles})
            self.assertEqual(hashlib.sha256((INSTRUCTIONS / path).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
