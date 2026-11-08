"""Offline derivation, containment and retained product-binding regressions."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

from tools import instruction_resources as resource

ROOT = Path(__file__).resolve().parents[1]


def snapshot(root):
    return {str(path.relative_to(root)): (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
            for path in root.rglob("*") if path.is_file()}


class DerivationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="app-instruction-resources-")
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name).resolve()
        self.source = self.project / resource.SOURCE
        shutil.copytree(ROOT / resource.SOURCE, self.source)
        (self.project / resource.OUTPUT.parent).mkdir(parents=True)
        self.output = self.project / resource.OUTPUT
        self.record = self.project / resource.DERIVATION

    def test_generation_is_deterministic_byte_and_mode_copy_without_library(self):
        old_umask = os.umask(0o077)
        try:
            first = resource.generate(self.project)
        finally:
            os.umask(old_umask)
        self.assertEqual(snapshot(self.source), snapshot(self.output))
        for directory in resource.DIRECTORIES:
            self.assertEqual(stat.S_IMODE((self.output / directory).stat().st_mode), 0o755)
        before = snapshot(self.output), self.record.read_bytes()
        resource.generate(self.project)
        self.assertEqual(before, (snapshot(self.output), self.record.read_bytes()))
        self.assertEqual(first["derivationSha256"], resource.generate(self.project, check=True)["derivationSha256"])
        # A plain source export is sufficient: no .git, Library or runtime state.
        self.assertFalse((self.project / ".git").exists())

    def test_source_changes_require_both_output_and_manifest_refresh(self):
        resource.generate(self.project)
        old_manifest = self.record.read_bytes()
        changed = self.source / "AGENTS.md"
        changed.write_bytes(changed.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "Generated instructions stale"):
            resource.generate(self.project, check=True)
        # Even independently editing the output cannot conceal stale derivation.
        (self.output / "AGENTS.md").write_bytes(changed.read_bytes())
        with self.assertRaisesRegex(ValueError, "INSTRUCTION_RESOURCE_DERIVATION"):
            resource.generate(self.project, check=True)
        resource.generate(self.project)
        self.assertNotEqual(old_manifest, self.record.read_bytes())
        self.assertEqual(snapshot(self.source), snapshot(self.output))
        self.assertEqual((self.source / "SOURCE_MAP.json").read_bytes(), (self.output / "SOURCE_MAP.json").read_bytes())

    def test_missing_declared_output_is_restored_but_extra_entries_are_never_deleted(self):
        resource.generate(self.project)
        (self.output / "AGENTS.md").unlink()
        with self.assertRaises(ValueError):
            resource.generate(self.project, check=True)
        resource.generate(self.project)
        before = snapshot(self.output)
        extra = self.output / "unlisted.md"
        extra.write_bytes(b"keep this unknown file")
        (self.source / "AGENTS.md").write_bytes(b"changed source")
        with self.assertRaisesRegex(ValueError, "Unexpected instruction entry"):
            resource.generate(self.project)
        self.assertEqual(extra.read_bytes(), b"keep this unknown file")
        self.assertEqual(before["AGENTS.md"], snapshot(self.output)["AGENTS.md"])

    def test_source_file_set_and_modes_are_explicit(self):
        for relative in ("extra.md", "agents/AGENT_INTERLOCUTOR.md"):
            with self.subTest(relative=relative):
                extra = self.source / relative
                extra.write_bytes(b"not selected")
                with self.assertRaises(ValueError):
                    resource.generate(self.project)
                self.assertFalse(self.output.exists())
                extra.unlink()
        target = self.source / "AGENTS.md"
        target.chmod(0o755)
        with self.assertRaisesRegex(ValueError, "file mode differs"):
            resource.generate(self.project)
        target.chmod(0o644)
        resource.generate(self.project)
        (self.output / "AGENTS.md").chmod(0o600)
        with self.assertRaisesRegex(ValueError, "file mode differs"):
            resource.generate(self.project, check=True)

    def test_symlink_source_destination_ancestor_and_manifest_are_refused(self):
        outside = self.project / "outside"
        outside.mkdir()
        sentinel = outside / "sentinel"
        sentinel.write_bytes(b"outside stays unchanged")
        source = self.source / "AGENTS.md"
        original = source.read_bytes()
        source.unlink()
        source.symlink_to(sentinel)
        with self.assertRaises(ValueError):
            resource.generate(self.project)
        source.unlink()
        source.write_bytes(original)
        source.chmod(0o644)
        resource.generate(self.project)
        shutil.rmtree(self.output / "agents")
        (self.output / "agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            resource.generate(self.project)
        (self.output / "agents").unlink()
        resource.generate(self.project)
        self.record.unlink()
        self.record.symlink_to(sentinel)
        with self.assertRaises(OSError):
            resource.generate(self.project)
        self.record.unlink()
        # Reject an aliased ancestor as well as individual generated files.
        shutil.rmtree(self.output)
        self.output.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            resource.generate(self.project)
        self.assertEqual(sentinel.read_bytes(), b"outside stays unchanged")

    def test_hardlinked_and_special_outputs_refuse_before_any_write(self):
        resource.generate(self.project)
        sentinel = self.project / "sentinel"
        sentinel.write_bytes(b"outside")
        sentinel.chmod(0o644)
        target = self.output / "AGENTS.md"
        target.unlink()
        os.link(sentinel, target)
        with self.assertRaisesRegex(ValueError, "unaliased regular file"):
            resource.generate(self.project)
        self.assertEqual(sentinel.read_bytes(), b"outside")
        target.unlink()
        os.mkfifo(target)
        with self.assertRaisesRegex(ValueError, "Unexpected instruction entry"):
            resource.generate(self.project)

    def test_manifest_data_never_selects_a_write_path_and_check_is_read_only(self):
        resource.generate(self.project)
        manifest = json.loads(self.record.read_text())
        manifest["files"][0]["path"] = "../../escape"
        self.record.write_text(json.dumps(manifest))
        before = snapshot(self.output), self.record.read_bytes()
        with self.assertRaises(ValueError):
            resource.generate(self.project, check=True)
        self.assertEqual(before, (snapshot(self.output), self.record.read_bytes()))
        resource.generate(self.project)
        self.assertFalse((self.project / "escape").exists())
        self.assertEqual(json.loads(self.record.read_text())["files"][0]["path"], "AGENTS.md")

    def test_cli_check_refuses_stale_output_without_mutation(self):
        resource.generate(self.project)
        target = self.output / "AGENTS.md"
        target.write_bytes(b"stale")
        result = subprocess.run([sys.executable, "-B", "-m", "tools.instruction_resources", "--project", str(self.project), "--check"], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"Generated instructions stale", result.stderr)
        self.assertEqual(target.read_bytes(), b"stale")


class RetainedProductTests(unittest.TestCase):
    def test_current_eight_file_payload_and_historical_bindings_are_preserved(self):
        resource.generate(ROOT, check=True)
        source = resource.tree(ROOT / resource.SOURCE)
        lines = b"".join(f"{hashlib.sha256(source[p]).hexdigest()}  {p}\n".encode() for p in sorted(source))
        self.assertEqual(hashlib.sha256(lines).hexdigest(), "50c82a3c663773b327d7ed84bb27a7d639514062e0d1335f7c47b6f3b0194d18")
        binding = json.loads(source["ROLE_SET_SOURCE_BINDING.json"])
        self.assertEqual(binding["basisCommit"], "89acac6a3983c605820496d0d121c73bb2297706")
        self.assertEqual(hashlib.sha256(source["ROLE_SET_SOURCE_BINDING.json"]).hexdigest(), "da57b6103c2443a7e9996ac1a7a608da05b7704f9c95812ddd35743b1743702d")
        self.assertEqual(hashlib.sha256(source["SOURCE_MAP.json"]).hexdigest(), "138aba1849de0fd39a4bcf75a69ffb82b8d59a2a0b02ff0790da9a44bfd66be6")
        roles = json.loads(source["roles.json"])["roles"]
        self.assertEqual([r["name"] for r in roles], ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"])
        self.assertTrue(all(r["default_for_new_chat"] is False for r in roles))
        for guidance in binding["guidance"]:
            self.assertEqual(hashlib.sha256(source[guidance["path"]]).hexdigest(), guidance["sha256"])

    def test_selected_documentary_passages_remain_bound_without_repin(self):
        binding = json.loads((ROOT / resource.SOURCE / "ROLE_SET_SOURCE_BINDING.json").read_text())
        for item in binding["sources"]:
            relative = item["repositoryPath"].removeprefix("projects/chirality-app-v4/").replace("/Design/", "/Work/")
            raw = (ROOT / relative).read_bytes()
            if "selectors" in item:
                lines = raw.decode("utf-8").splitlines(keepends=True)
                framed = bytearray()
                for selector in item["selectors"]:
                    if "heading" in selector:
                        heading = selector["heading"]
                        starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == heading]
                        self.assertEqual(len(starts), 1)
                        start = starts[0]
                        level = len(heading) - len(heading.lstrip("#"))
                        end = len(lines)
                        for i in range(start + 1, len(lines)):
                            count = len(lines[i]) - len(lines[i].lstrip("#"))
                            if 0 < count <= level and lines[i][count:count + 1] == " ":
                                end = i
                                break
                        selected = "".join(lines[start:end])
                    else:
                        matching = [line for line in lines if line.startswith(selector["linePrefix"])]
                        self.assertEqual(len(matching), 1)
                        selected = matching[0]
                        if "columns" in selector:
                            cells = selected.rstrip("\r\n").strip("|").split("|")
                            selected = "|".join(cells[i] for i in selector["columns"])
                    selected = selected.encode("utf-8")
                    framed.extend(len(selected).to_bytes(8, "big"))
                    framed.extend(selected)
                raw = bytes(framed)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"], relative)


if __name__ == "__main__":
    unittest.main()
