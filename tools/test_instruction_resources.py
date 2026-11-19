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


class PackagedInstructionTests(unittest.TestCase):
    def test_current_payload_and_role_binding_are_preserved(self):
        entries = sorted(INSTRUCTIONS.rglob("*"))
        files = [path for path in entries if not path.is_dir() or path.is_symlink()]
        self.assertEqual(sorted(path.relative_to(INSTRUCTIONS).as_posix() for path in files), sorted(FILES))
        self.assertEqual([path.name for path in entries if path.is_dir() and not path.is_symlink()], ["agents"])
        for path in files:
            meta = path.lstat()
            self.assertTrue(stat.S_ISREG(meta.st_mode) and meta.st_nlink == 1, path)
        source = {name: (INSTRUCTIONS / name).read_bytes() for name in FILES}
        lines = b"".join(f"{hashlib.sha256(source[p]).hexdigest()}  {p}\n".encode() for p in sorted(source))
        self.assertEqual(hashlib.sha256(lines).hexdigest(), "327f3b94e765e7d31346b1405539699eaa9087b36da74ddf348a1ea63f0b8eb4")
        binding = json.loads(source["ROLE_SET_SOURCE_BINDING.json"])
        self.assertEqual(binding["basisCommit"], "89acac6a3983c605820496d0d121c73bb2297706")
        self.assertEqual(hashlib.sha256(source["ROLE_SET_SOURCE_BINDING.json"]).hexdigest(), "62311e84459b42868439a186acd176f904a568cb944067086a0437fbca974e76")
        roles = json.loads(source["roles.json"])["roles"]
        self.assertEqual([r["name"] for r in roles], ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"])
        # DEL-02-04 TBD-004: for 4.0.0 a new conversation preselects HELP_HUMAN, and only it.
        self.assertEqual([r["name"] for r in roles if r["default_for_new_chat"] is True], ["HELP_HUMAN"])
        self.assertTrue(all(r["default_for_new_chat"] in (True, False) for r in roles))
        for guidance in binding["guidance"]:
            self.assertEqual(hashlib.sha256(source[guidance["path"]]).hexdigest(), guidance["sha256"])


if __name__ == "__main__":
    unittest.main()
