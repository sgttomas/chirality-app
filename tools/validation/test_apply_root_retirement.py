#!/usr/bin/env python3
"""Isolated transaction/failure fixtures; mocked authority is never a CLI option."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scaffolding/apply_root_retirement.py"
SPEC = importlib.util.spec_from_file_location("retirement_under_test", SOURCE)
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)


class RetirementTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="retirement-unit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.evidence = self.root / tool.EVIDENCE_ROOTS[0] / "evidence"
        self.rows = []
        self.statuses = []
        for index in range(53):
            package = f"PKG-{index % 6 + 1:02d}_fixture"
            source = f"DEL-{index % 6 + 1:02d}-{index + 1:02d}_fixture"
            path = f"execution/{package}/1_Working/{source}/_STATUS.md"
            pre = f"# {source}\nCurrent: INITIALIZED\nHistory: INITIALIZED\n".encode()
            post = pre + b"Current: RETIRED\nHistory: RETIRED\n"
            row = {"path": path, "source_package": package, "source_id": source,
                   "preimage_sha256": tool.sha(pre), "postimage_sha256": tool.sha(post),
                   "postimage_path": f"approved/{index}.md"}
            self.put(path, pre)
            self.put(row["postimage_path"], post)
            self.rows.append(row)
            self.statuses.append((row, pre, post))
        self.state = {"source_statuses": self.rows, "gate4": {"path": tool.EVIDENCE_ROOTS[0] + "owner.md"},
                      "propagation_plan": {"path": tool.EVIDENCE_ROOTS[0] + "plan.sha", "sha256": "approved-plan"},
                      "transaction": {"path": self.evidence.relative_to(self.root).as_posix() + "/journal.json", "sha256": None}}
        self.put("state.json", json.dumps(self.state).encode())
        required = {*tool.REQUIRED_SUITES, tool.SELF, tool.TEST, "tools/validation/root_governance_state.py",
                    *tool.CONFIGS, *(f"tools/validation/{g}.py" for g in tool.GUARDS)}
        for path in required:
            self.put(path, b"# isolated fixture\n")
        pins = [{"path": p, "sha256": tool.sha((self.root / p).read_bytes())}
                for p in sorted(required | {"state.json"})]
        self.subject = {"schema": "root-retirement-application/v1",
                        "governance_state": next(p for p in pins if p["path"] == "state.json"),
                        "tested_files": pins,
                        "fixture_suites": [p for p in pins if p["path"] in tool.REQUIRED_SUITES]}
        self.effect = {"schema": "root-retirement-execution/v1", "owner_act": self.state["gate4"]}
        self.save_subject()
        fake = types.ModuleType("root_governance_state")
        fake.GovernanceError = tool.Refusal
        fake.safe_path = self.safe_path
        fake.verify_owner_act = lambda root, ref, digest: None
        fake.load_governance_state = lambda *args, **kwargs: self.state
        self.boundary = patch.dict(sys.modules, {"root_governance_state": fake})
        self.boundary.start()
        self.addCleanup(self.boundary.stop)
        self.fake = fake

    def put(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def safe_path(self, root, relative, allow_missing=False):
        raw = Path(relative)
        path = root / raw
        if raw.is_absolute() or ".." in raw.parts or not path.resolve().is_relative_to(root.resolve()):
            raise tool.Refusal("unsafe fixture path")
        if any((root / Path(*raw.parts[:index])).is_symlink() for index in range(1, len(raw.parts) + 1)):
            raise tool.Refusal("symlink fixture path")
        if not allow_missing and not path.exists():
            raise tool.Refusal("missing fixture path")
        return path

    def save_subject(self):
        self.put("subject.json", json.dumps(self.subject).encode())
        self.effect["subject_sha256"] = tool.sha((self.root / "subject.json").read_bytes())
        self.put("effect.json", json.dumps(self.effect).encode())

    def load(self):
        return tool.load_subject(self.root, self.root / "subject.json", self.root / "effect.json")

    def originals(self):
        return {row["path"]: (self.root / row["path"]).read_bytes() for row in self.rows}

    def test_exact_subject(self):
        self.assertFalse(self.load()[-1])

    def test_target_mutations_refuse_without_writes(self):
        for mutation in ("missing", "extra", "duplicate", "sibling", "traversal", "preimage", "postimage", "parents"):
            with self.subTest(mutation=mutation):
                original_rows = list(self.rows)
                old = dict(self.rows[0])
                before = self.originals()
                if mutation == "missing": self.rows.pop()
                elif mutation == "extra": self.rows.append(dict(self.rows[0]))
                elif mutation == "duplicate": self.rows[0]["path"] = self.rows[1]["path"]
                elif mutation == "sibling": self.rows[0]["path"] = "projects/other/_STATUS.md"
                elif mutation == "traversal": self.rows[0]["path"] = "../other/_STATUS.md"
                elif mutation == "preimage": self.rows[0]["preimage_sha256"] = "wrong"
                elif mutation == "postimage": self.rows[0]["postimage_sha256"] = "wrong"
                elif mutation == "parents": self.rows[0]["source_package"] = "PKG-99_unapproved"
                with self.assertRaises((tool.Refusal, OSError)):
                    self.load()
                self.rows[:] = original_rows
                self.rows[0].clear(); self.rows[0].update(old)
                self.assertEqual(before, self.originals())

    def test_symlink_refused(self):
        path = self.root / self.rows[0]["path"]
        path.unlink()
        path.symlink_to(self.root / self.rows[1]["path"])
        with self.assertRaises(tool.Refusal): self.load()

    def test_wrong_subject_and_branch_only_owner_refused(self):
        before = self.originals()
        self.effect["subject_sha256"] = "wrong"
        self.put("effect.json", json.dumps(self.effect).encode())
        with self.assertRaises(tool.Refusal): self.load()
        self.save_subject()
        self.fake.verify_owner_act = lambda *args: (_ for _ in ()).throw(tool.Refusal("branch-only"))
        with self.assertRaises(tool.Refusal): self.load()
        self.assertEqual(before, self.originals())

    def test_stale_implementation_refused(self):
        self.put(tool.SELF, b"changed")
        with self.assertRaises(tool.Refusal): self.load()

    def test_mixed_state_refused(self):
        row, _, post = self.statuses[0]
        self.put(row["path"], post)
        with self.assertRaises(tool.Refusal): self.load()

    def test_apply_all_53_and_exact_idempotence_detection(self):
        self.evidence.mkdir(parents=True)
        tool.transact(self.root, self.statuses, self.evidence, "subject", guard_runner=lambda *a: None)
        self.assertTrue(self.load()[-1])
        self.assertEqual(tool.read_json(self.evidence / "journal.json")["state"], "APPLIED")

    def test_mid_write_failure_restores_own_postimages(self):
        before = self.originals()
        self.evidence.mkdir(parents=True)
        def fail(index, path):
            if index == 17: raise OSError("injected failure")
        with self.assertRaises(OSError):
            tool.transact(self.root, self.statuses, self.evidence, "subject", after_write=fail)
        self.assertEqual(before, self.originals())
        self.assertEqual(tool.read_json(self.evidence / "journal.json")["state"], "ROLLED_BACK")

    def test_concurrent_edit_survives_guarded_rollback(self):
        self.evidence.mkdir(parents=True)
        changed = self.root / self.rows[0]["path"]
        def fail(index, path):
            if index == 17:
                changed.write_bytes(b"concurrent unrelated edit")
                raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            tool.transact(self.root, self.statuses, self.evidence, "subject", after_write=fail)
        self.assertEqual(changed.read_bytes(), b"concurrent unrelated edit")
        journal = tool.read_json(self.evidence / "journal.json")
        self.assertEqual(journal["state"], "BLOCKED_PARTIAL")
        self.assertEqual(journal["blocked"], [self.rows[0]["path"]])
        for row, pre, _ in self.statuses[1:]: self.assertEqual((self.root / row["path"]).read_bytes(), pre)

    def test_live_guard_failure_rolls_back(self):
        before = self.originals()
        self.evidence.mkdir(parents=True)
        def fail(*args): raise tool.Refusal("G2 rejected live state")
        with self.assertRaises(tool.Refusal):
            tool.transact(self.root, self.statuses, self.evidence, "subject", guard_runner=fail)
        self.assertEqual(before, self.originals())

    def test_failed_prospective_or_fixture_never_writes(self):
        for name in ("prospective",):
            with self.subTest(stage=name), tempfile.TemporaryDirectory(dir=self.root) as temp:
                before = self.originals()
                with patch.object(tool, "run_fixtures"), patch.object(tool, "prospective"):
                    with patch.object(tool, name, side_effect=tool.Refusal("injected preflight failure")):
                        with self.assertRaises(tool.Refusal):
                            tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", self.evidence.parent / name, False)
                self.assertEqual(before, self.originals())

    def test_no_force_option(self):
        with patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit) as result:
            tool.main(["--subject-manifest", "subject", "--effect-record", "effect",
                       "--evidence-dir", "evidence", "--apply", "--force"])
        self.assertEqual(result.exception.code, 2)

    def test_gate4_apply_and_idempotent_rerun_need_no_future_gate5(self):
        guards = {name: types.SimpleNamespace(check=lambda root: (0, ["isolated fixture"]))
                  for name in tool.GUARDS}
        with patch.dict(sys.modules, guards), patch.object(tool, "run_fixtures"), patch.object(tool, "prospective"):
            tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", self.evidence, True)
            self.assertEqual(tool.read_json(self.evidence / "journal.json")["state"], "APPLIED")
            before = self.originals()
            rerun = self.evidence.parent / "idempotent-evidence"
            tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", rerun, True)
            self.assertEqual(tool.read_json(rerun / "result.json")["state"], "ALREADY_APPLIED")
            self.assertEqual(before, self.originals())

    def test_exact_postimages_without_prior_subject_journal_refused(self):
        for row, _, post in self.statuses: self.put(row["path"], post)
        with self.assertRaises(OSError):
            tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", self.evidence, True)
        self.assertFalse(self.evidence.exists())

    def test_all_five_guard_invocations_and_negative_refusal(self):
        self.evidence.mkdir(parents=True)
        calls = []
        def check(name):
            def run(root):
                calls.append(name)
                return (1 if name == tool.GUARDS[-1] else 0, [name])
            return run
        guards = {name: types.SimpleNamespace(check=check(name)) for name in tool.GUARDS}
        with patch.dict(sys.modules, guards), self.assertRaises(tool.Refusal):
            tool.run_guards(self.root, self.evidence, "prospective")
        self.assertEqual(calls, list(tool.GUARDS))
        result = tool.read_json(self.evidence / "prospective-guards.json")
        self.assertEqual(result[-1]["exit_code"], 1)

    def test_failed_fixture_execution_records_actual_exit(self):
        self.evidence.mkdir(parents=True)
        failure = types.SimpleNamespace(returncode=7, stdout="fixture output", stderr="failure")
        with patch.object(tool.subprocess, "run", return_value=failure) as invoked, self.assertRaises(tool.Refusal):
            tool.run_fixtures(self.root, self.subject, self.evidence)
        self.assertEqual(tool.read_json(self.evidence / "fixture-0.json")["exit_code"], 7)
        self.assertEqual(invoked.call_args.args[0][1:4], ["-m", "pytest", "-q"])

    def test_prospective_copies_only_tracked_and_declared_files(self):
        self.evidence.mkdir(parents=True)
        self.fake.PLAN = "plan"
        self.put("plan/WRITE_TARGETS.csv", b"Target\npending/approved.md\n")
        self.put("plan/GUARDS/WRITE_PATH_INVENTORY.csv", b"Path\n")
        self.put("pending/approved.md", b"approved pending file")
        self.put("runtime/local-account-secret", b"must never copy")
        self.put("unrelated-untracked", b"must never copy")
        self.put("tracked/[id]/route.ts", b"literal tracked bracket path")
        before = self.originals()
        tracked = "\0".join([row["path"] for row in self.rows] + [p["path"] for p in self.subject["tested_files"]] + ["tracked/[id]/route.ts"]).encode() + b"\0"
        def git(command, **kwargs):
            if command[1:4] == ["-m", "pytest", "-q"]:
                scratch = kwargs["cwd"]
                self.assertNotEqual(scratch, self.root)
                for row, _, post in self.statuses:
                    self.assertEqual((scratch / row["path"]).read_bytes(), post)
                return types.SimpleNamespace(stdout="fixture executed", stderr="", returncode=0)
            return types.SimpleNamespace(stdout=tracked if command[1] == "ls-files" else str(self.root / "git-read-only") + "\n")
        observed = []
        def guards(scratch, evidence, phase):
            self.assertEqual(phase, "prospective")
            self.assertFalse((scratch / "runtime/local-account-secret").exists())
            self.assertFalse((scratch / "unrelated-untracked").exists())
            self.assertTrue((scratch / "pending/approved.md").exists())
            self.assertEqual((scratch / "tracked/[id]/route.ts").read_bytes(), b"literal tracked bracket path")
            for row, _, post in self.statuses:
                self.assertEqual((scratch / row["path"]).read_bytes(), post)
            observed.append(True)
        with patch.object(tool.subprocess, "run", side_effect=git), patch.object(tool, "run_guards", side_effect=guards):
            tool.prospective(self.root, self.statuses, self.evidence, self.subject)
        self.assertEqual(observed, [True])
        self.assertEqual(before, self.originals())

    def test_external_evidence_refused_without_directory_creation(self):
        with tempfile.TemporaryDirectory() as external:
            target = Path(external) / "must-not-exist"
            with self.assertRaises(tool.Refusal):
                tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", target, False)
            self.assertFalse(target.exists())

    def test_evidence_symlink_refused_without_following(self):
        with tempfile.TemporaryDirectory() as external:
            self.evidence.parent.mkdir(parents=True)
            link = self.evidence.parent / "escape"
            link.symlink_to(external, target_is_directory=True)
            with self.assertRaises(tool.Refusal):
                tool.execute(self.root, self.root / "subject.json", self.root / "effect.json", link / "run", False)
            self.assertFalse((Path(external) / "run").exists())

    def test_unknown_reference_and_operational_pin_refused(self):
        before = self.originals()
        self.subject["extra"] = {"path": ".env"}
        self.save_subject()
        with self.assertRaises(tool.Refusal): self.load()
        del self.subject["extra"]
        self.put(".env", b"never copy this operational state")
        self.subject["tested_files"].append({"path": ".env", "sha256": tool.sha((self.root / ".env").read_bytes())})
        self.save_subject()
        with self.assertRaises(tool.Refusal): self.load()
        self.assertEqual(before, self.originals())

    def test_final_journal_publication_failure_rolls_back(self):
        self.evidence.mkdir(parents=True)
        before = self.originals()
        real_replace = tool.os.replace
        def fail_completed_journal(source, destination):
            if Path(destination).name == "journal.json" and tool.read_json(Path(source))["state"] == "APPLIED":
                raise OSError("injected final journal replacement failure")
            return real_replace(source, destination)
        with patch.object(tool.os, "replace", side_effect=fail_completed_journal), self.assertRaises(OSError):
            tool.transact(self.root, self.statuses, self.evidence, "subject", guard_runner=lambda *args: None)
        self.assertEqual(before, self.originals())
        self.assertEqual(tool.read_json(self.evidence / "journal.json")["state"], "ROLLED_BACK")
        self.assertEqual(list(self.evidence.glob("*.tmp")), [])

    def test_final_journal_failure_preserves_concurrent_edit(self):
        self.evidence.mkdir(parents=True)
        changed = self.root / self.rows[0]["path"]
        real_write = tool.write_json
        def fail_completed_journal(path, value):
            if value.get("state") == "APPLIED":
                changed.write_bytes(b"concurrent edit during final journal publication")
                raise OSError("injected final journal failure")
            return real_write(path, value)
        with patch.object(tool, "write_json", side_effect=fail_completed_journal), self.assertRaises(OSError):
            tool.transact(self.root, self.statuses, self.evidence, "subject", guard_runner=lambda *args: None)
        journal = tool.read_json(self.evidence / "journal.json")
        self.assertEqual(journal["state"], "BLOCKED_PARTIAL")
        self.assertEqual(journal["blocked"], [self.rows[0]["path"]])
        self.assertEqual(changed.read_bytes(), b"concurrent edit during final journal publication")
        for row, pre, _ in self.statuses[1:]: self.assertEqual((self.root / row["path"]).read_bytes(), pre)

    def test_rollback_announcement_failure_does_not_prevent_restore(self):
        self.evidence.mkdir(parents=True)
        before = self.originals()
        real_write = tool.write_json
        def fail_journal(path, value):
            if value.get("state") in {"APPLIED", "ROLLING_BACK"}:
                raise OSError("injected evidence failure")
            return real_write(path, value)
        with patch.object(tool, "write_json", side_effect=fail_journal), self.assertRaises(OSError):
            tool.transact(self.root, self.statuses, self.evidence, "subject", guard_runner=lambda *args: None)
        self.assertEqual(before, self.originals())
        journal = tool.read_json(self.evidence / "journal.json")
        self.assertEqual(journal["state"], "ROLLED_BACK")
        self.assertIn("injected evidence failure", journal["journal_error"])


if __name__ == "__main__":
    unittest.main()
