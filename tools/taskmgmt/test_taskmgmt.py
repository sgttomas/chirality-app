"""Tests for taskmgmt v0 (scan/validate)."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import taskmgmt  # noqa: E402


def write_register(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=taskmgmt.CANONICAL_COLUMNS, quoting=csv.QUOTE_ALL,
            lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def good_row(**overrides) -> dict:
    row = {c: "" for c in taskmgmt.CANONICAL_COLUMNS}
    row.update(
        RegisterSchemaVersion="1.0", ActionItemID="TM-TEST-001", Title="t",
        Concern="c", SourceRef="a/b.md", SourceSha="0" * 40,
        CandidateRef="DIRECT", DomainLenses="Decisions", AssociatedWith="x",
        NoticeRef="NONE", ScaRef="NONE", Assignment="TBD", Priority="TBD",
        PriorityBasis="TBD", Status="OPEN", Opened="2026-07-31",
    )
    row.update(overrides)
    return row


def run_validate(root: Path, register: Path):
    return taskmgmt.validate_register(root, register)


class TestValidate:
    def test_pass_on_conforming_register(self, tmp_path):
        reg = tmp_path / "REGISTER.csv"
        write_register(reg, [
            good_row(),
            good_row(ActionItemID="TM-TEST-002", Status="DEFERRED",
                     Trigger="an event"),
            good_row(ActionItemID="TM-TEST-003", Status="CLOSED",
                     Disposition="OBE", EvidenceRef="e.md",
                     EvidenceSha="1" * 40, Closed="2026-07-31"),
            good_row(ActionItemID="TM-TEST-004", Status="ELEVATED",
                     ElevatedTo="TM-OTHER-001"),
        ])
        code, lines = run_validate(tmp_path, reg)
        assert code == 0, lines

    @pytest.mark.parametrize("overrides,needle", [
        (dict(Status="CLOSED", EvidenceRef="e", EvidenceSha="1" * 40,
              Closed="2026-07-31"), "valid Disposition"),
        (dict(Status="CLOSED", Disposition="OBE", EvidenceSha="1" * 40,
              Closed="2026-07-31"), "without EvidenceRef"),
        (dict(Status="CLOSED", Disposition="OBE", EvidenceRef="e",
              Closed="2026-07-31"), "without EvidenceSha"),
        (dict(Status="DEFERRED"), "DEFERRED without Trigger"),
        (dict(Status="ELEVATED"), "ELEVATED without ElevatedTo"),
        (dict(Status="IN_PROGRESS"), "Status"),
        (dict(Disposition="OBE"), "non-CLOSED"),
        (dict(ActionItemID="BADID"), "not TM-<LOOP>-<seq>"),
        (dict(SourceSha=""), "SourceSha empty"),
        (dict(Opened="July 31"), "not YYYY-MM-DD"),
    ])
    def test_block_on_rule_violation(self, tmp_path, overrides, needle):
        reg = tmp_path / "REGISTER.csv"
        write_register(reg, [good_row(**overrides)])
        code, lines = run_validate(tmp_path, reg)
        assert code == 1
        assert any(needle in line for line in lines), lines

    def test_block_on_duplicate_id(self, tmp_path):
        reg = tmp_path / "REGISTER.csv"
        write_register(reg, [good_row(), good_row()])
        code, lines = run_validate(tmp_path, reg)
        assert code == 1
        assert any("duplicate" in line for line in lines)

    def test_block_on_wrong_header(self, tmp_path):
        reg = tmp_path / "REGISTER.csv"
        reg.write_text("A,B,C\n1,2,3\n", encoding="utf-8")
        code, lines = run_validate(tmp_path, reg)
        assert code == 1
        assert any("header" in line for line in lines)

    def test_operational_on_missing_file(self, tmp_path):
        code, lines = run_validate(tmp_path, tmp_path / "nope.csv")
        assert code == 2


class TestScan:
    def build_tree(self, root: Path) -> None:
        co = root / "execution" / "_Coordination"
        (co / "_DECISIONS").mkdir(parents=True)
        (co / "_DECISIONS" / "_REGISTER.md").write_text(
            "| D-9 | thing | basis | AWAITING_RULING | link | note |\n"
            "| D-8 | done | basis | RULED | link | note |\n",
            encoding="utf-8")
        (co / "NOTICE_STATUS_X.csv").write_text(
            "NoticePath,SHA256,DeliveryState,AcknowledgementState,ClosureEffect\n"
            "a/NOTICE_ONE.md,ff,DELIVERED,TRACKED_OPEN,NON_GATING\n"
            "a/NOTICE_TWO.md,ee,DELIVERED,ACKNOWLEDGED,NON_GATING\n",
            encoding="utf-8")
        (co / "NOTICE_LOOSE.md").write_text("# loose notice\n", encoding="utf-8")
        ev = root / "execution" / "_Evaluation" / "SNAP"
        ev.mkdir(parents=True)
        (ev / "FINDINGS.csv").write_text(
            "FindingID,Concern,Status\nF-1,open thing,OPEN_ROUTED\n"
            "F-2,closed thing,CLOSED\n", encoding="utf-8")
        # canonical-vs-copy: same ledger copied into _Evaluation
        (ev / "NOTICE_STATUS_X.csv").write_text(
            (co / "NOTICE_STATUS_X.csv").read_text(), encoding="utf-8")
        pk = root / "domains" / "d" / "_Research" / "R1"
        pk.mkdir(parents=True)
        (pk / "Open_Questions.csv").write_text(
            "OpenQuestionID,Question,Status\nOQ-1,why,OPEN\nOQ-2,ok,RESOLVED\n",
            encoding="utf-8")
        (pk / "Amendment_Candidates.csv").write_text(
            "AmendmentID,Description,HumanRuling\nAC-1,change,TBD\n",
            encoding="utf-8")
        au = root / "projects" / "p" / "_audit"
        au.mkdir(parents=True)
        (au / "X_TBD_Register.csv").write_text(
            "TBDID,Question\nTBD-1,how\n", encoding="utf-8")
        (root / "projects" / "p" / "HANDOFF_STATE.md").write_text(
            "Remaining blockers: none.\n", encoding="utf-8")
        (root / "projects" / "p2").mkdir(parents=True)
        (root / "projects" / "p2" / "HANDOFF_STATE.md").write_text(
            "Remaining blockers: waiting on X.\n", encoding="utf-8")
        # excluded tree must not be scanned
        ex = root / "domains" / "d" / "_Decomposition" / "dispatch_briefs"
        ex.mkdir(parents=True)
        (ex / "FINDINGS.csv").write_text(
            "FindingID,Concern,Status\nF-X,noise,OPEN\n", encoding="utf-8")

    def test_scan_classes_dedup_and_exclusions(self, tmp_path):
        self.build_tree(tmp_path)
        out = tmp_path / "out.json"
        code, lines = taskmgmt.scan(
            tmp_path, tmp_path / "missing_register.csv", out)
        assert code == 0
        data = json.loads(out.read_text())
        counts = data["counts"]
        assert counts["decision-non-ruled"] == 1
        assert counts["notice-tracked-open"] == 2  # original + copy, pre-dedup
        assert data["dedup_dropped_copies"] == 1
        kept = [c for c in data["candidates"]
                if c["class"] == "notice-tracked-open"]
        assert len(kept) == 1
        assert "_Coordination" in kept[0]["source"]  # canonical wins
        assert counts["notice-not-in-ledger"] == 1
        assert counts["evaluation-finding-open"] == 1  # excluded tree unseen
        assert counts["packet-field-open"] == 2  # OQ-1 open + AC-1 TBD
        assert counts["tbd-register-row"] == 1
        assert counts["handoff-blocker"] == 1
        assert all(c["authority"] == "observed" for c in data["candidates"])

    def test_scan_marks_register_known_refs(self, tmp_path):
        self.build_tree(tmp_path)
        reg = tmp_path / "REGISTER.csv"
        write_register(reg, [good_row(
            SourceRef="projects/p/_audit/X_TBD_Register.csv row TBD-1")])
        out = tmp_path / "out.json"
        code, _ = taskmgmt.scan(tmp_path, reg, out)
        assert code == 0
        data = json.loads(out.read_text())
        tbd = [c for c in data["candidates"]
               if c["class"] == "tbd-register-row"]
        assert tbd and tbd[0]["known_to_register"] is True


ROOT_REGISTER = "execution/_Coordination/_TaskManagement/REGISTER.csv"
APP_REGISTER = (
    "projects/app/execution/_Coordination/_TaskManagement/REGISTER.csv"
)
DOMAIN_REGISTER = (
    "domains/handbook/execution/_Coordination/_TaskManagement/REGISTER.csv"
)
ENGINE_REGISTER = "_DomainEngines/fixture-engine/_TaskManagement/REGISTER.csv"


def closed_row(item_id: str, **overrides) -> dict:
    values = dict(
        ActionItemID=item_id, Status="CLOSED", Disposition="OBE",
        EvidenceRef="evidence.md", EvidenceSha="1" * 40,
        Closed="2026-08-01",
    )
    values.update(overrides)
    return good_row(**values)


def install_discovery(monkeypatch, tracked: list[str],
                      untracked: list[str] | None = None) -> None:
    classified = taskmgmt.classify_register_paths(tracked, untracked or [])
    monkeypatch.setattr(taskmgmt, "discover_registers", lambda root: classified)
    archives = taskmgmt.classify_archive_paths(tracked, untracked or [])
    monkeypatch.setattr(taskmgmt, "discover_archives", lambda root: archives)


def run_federation(root: Path, invoking: str, out: Path | None = None):
    target = out or root / "survey.json"
    code, lines = taskmgmt.federation(root, Path(invoking), target)
    data = json.loads(target.read_text(encoding="utf-8")) if target.exists() else None
    return code, lines, data


class TestFederationDiscovery:
    def test_all_sanctioned_forms_and_lookalike_exclusions(self):
        tracked = [
            ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER, ENGINE_REGISTER,
            "archive/_TaskManagement/REGISTER.csv",
            "projects/app/_TaskManagement/REGISTER.csv",
            "projects/nested/name/execution/_Coordination/_TaskManagement/REGISTER.csv",
            "tools/fixture/_TaskManagement/REGISTER.csv",
        ]
        untracked = [
            "projects/untracked/execution/_Coordination/_TaskManagement/REGISTER.csv",
            "scratch/_TaskManagement/REGISTER.csv",
            "unrelated.csv",
        ]
        canonical, exclusions = taskmgmt.classify_register_paths(
            tracked, untracked)
        assert canonical == sorted(
            [ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER, ENGINE_REGISTER])
        assert {item["path"] for item in exclusions} == {
            "archive/_TaskManagement/REGISTER.csv",
            "projects/app/_TaskManagement/REGISTER.csv",
            "projects/nested/name/execution/_Coordination/_TaskManagement/REGISTER.csv",
            "tools/fixture/_TaskManagement/REGISTER.csv",
            "projects/untracked/execution/_Coordination/_TaskManagement/REGISTER.csv",
            "scratch/_TaskManagement/REGISTER.csv",
        }
        assert any("untracked" in item["reason"] for item in exclusions)

    def test_complete_inventory_header_only_fallback_and_default_output(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])

        code, lines = taskmgmt.federation(
            tmp_path, Path(APP_REGISTER), None)
        default_out = (
            tmp_path / Path(APP_REGISTER).parent / ".candidates" /
            "federation.json"
        )
        data = json.loads(default_out.read_text(encoding="utf-8"))
        assert code == 0, lines
        assert data["coverage"] == "COMPLETE"
        app = next(item for item in data["registers"]
                   if item["path"] == APP_REGISTER)
        assert app["namespace"] == "APP"
        assert app["namespace_basis"] == "PATH_FALLBACK_HEADER_ONLY"
        assert app["schema_version"] == "HEADER_ONLY"
        assert data["authority"] == taskmgmt.FEDERATION_AUTHORITY
        assert data["zero_write_proof"]["register_writes"] == 0
        assert "zero register writes occurred" in data["zero_write_proof"]["statement"]

    def test_tracked_invalid_and_mixed_namespace_are_partial(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [
            good_row(ActionItemID="TM-APP-001"),
            good_row(ActionItemID="TM-OTHER-002"),
        ])
        invalid = tmp_path / DOMAIN_REGISTER
        invalid.parent.mkdir(parents=True)
        invalid.write_text("wrong,header\na,b\n", encoding="utf-8")
        install_discovery(
            monkeypatch, [ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER])

        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 1, lines
        assert data["coverage"] == "PARTIAL"
        classes = [item["class"] for item in data["findings"]]
        assert "INVALID_REGISTER" in classes
        assert "AMBIGUOUS_REFERENCE" in classes
        assert any("do not infer global absence" in line for line in lines)

    def test_discovery_failure_is_operational_and_writes_evidence(
            self, tmp_path, monkeypatch):
        out = tmp_path / "failure.json"

        def fail(root):
            raise subprocess.CalledProcessError(1, ["git", "ls-files"])

        monkeypatch.setattr(taskmgmt, "discover_registers", fail)
        code, lines = taskmgmt.federation(
            tmp_path, Path(ROOT_REGISTER), out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert code == 2, lines
        assert data["coverage"] == "PARTIAL"
        assert any(item["stage"] == "discovery"
                   for item in data["operational_errors"])

    def test_unreadable_register_is_operational(self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])
        real_read = taskmgmt._read_register

        def unreadable(path):
            if path.as_posix().endswith(APP_REGISTER):
                raise PermissionError("fixture denied")
            return real_read(path)

        monkeypatch.setattr(taskmgmt, "_read_register", unreadable)
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 2, lines
        assert data["coverage"] == "PARTIAL"
        assert any(item["class"] == "UNREADABLE_REGISTER"
                   for item in data["findings"])

    def test_output_failure_is_operational(self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER])
        blocker = tmp_path / "not-a-directory"
        blocker.write_text("x", encoding="utf-8")
        code, lines = taskmgmt.federation(
            tmp_path, Path(ROOT_REGISTER), blocker / "federation.json")
        assert code == 2
        assert "output failed" in "\n".join(lines)

    def test_output_may_not_alias_a_register(self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])
        before = (tmp_path / APP_REGISTER).read_bytes()

        code, lines = taskmgmt.federation(
            tmp_path, Path(ROOT_REGISTER), tmp_path / APP_REGISTER)

        assert code == 2
        assert "resolves to a register surface" in "\n".join(lines)
        assert (tmp_path / APP_REGISTER).read_bytes() == before

    def test_output_symlink_may_not_alias_a_register(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER])
        output_link = tmp_path / "projection.json"
        output_link.symlink_to(tmp_path / ROOT_REGISTER)
        before = (tmp_path / ROOT_REGISTER).read_bytes()

        code, lines = taskmgmt.federation(
            tmp_path, Path(ROOT_REGISTER), output_link)

        assert code == 2
        assert "resolves to a register surface" in "\n".join(lines)
        assert (tmp_path / ROOT_REGISTER).read_bytes() == before


class TestFederationRelationships:
    def build_relationship_fixture(self, root: Path) -> list[str]:
        write_register(root / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001",
                     SourceRef="refs.md; TM-APP-001; TM-MISSING-901"),
            closed_row("TM-ROOT-002", SourceRef="TM-APP-002"),
            good_row(ActionItemID="TM-ROOT-003", SourceRef="TM-APP-003"),
            good_row(ActionItemID="TM-ROOT-004", Status="ELEVATED",
                     ElevatedTo="TM-NONE-999"),
            good_row(ActionItemID="TM-ROOT-005"),
        ])
        write_register(root / APP_REGISTER, [
            good_row(ActionItemID="TM-APP-001"),
            good_row(ActionItemID="TM-APP-002"),
            closed_row("TM-APP-003"),
            good_row(ActionItemID="TM-APP-004", Status="ELEVATED",
                     ElevatedTo="TM-ROOT-099"),
            good_row(ActionItemID="TM-APP-005", Status="ELEVATED",
                     ElevatedTo="TM-ROOT-005"),
        ])
        return [ROOT_REGISTER, APP_REGISTER]

    def test_directional_orphan_ack_and_both_closure_echoes(
            self, tmp_path, monkeypatch):
        tracked = self.build_relationship_fixture(tmp_path)
        install_discovery(monkeypatch, tracked)
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 0, lines
        classes = {item["class"] for item in data["findings"]}
        assert {
            "INBOUND_ELEVATION", "FOREIGN_LINK_TO_LOCAL",
            "LOCAL_LINK_TO_FOREIGN", "OUTBOUND_AWAITING_ACK",
            "REMOTE_CLOSED_LOCAL_OPEN", "LOCAL_CLOSED_REMOTE_OPEN",
            "ORPHANED_LINK",
        } <= classes
        echoes = [item for item in data["findings"] if item["class"] in {
            "REMOTE_CLOSED_LOCAL_OPEN", "LOCAL_CLOSED_REMOTE_OPEN"}]
        assert len(echoes) == 2
        assert data["findings"] == data["presented_findings"]

    def test_duplicate_global_id_and_ambiguous_link(self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001", SourceRef="TM-DUP-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-DUP-001")])
        write_register(tmp_path / DOMAIN_REGISTER, [good_row(
            ActionItemID="TM-DUP-001")])
        install_discovery(
            monkeypatch, [ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER])
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 0, lines
        assert data["finding_counts"]["DUPLICATE_GLOBAL_ID"] == 1
        ambiguous = [item for item in data["findings"]
                     if item["class"] == "AMBIGUOUS_REFERENCE"]
        assert len(ambiguous) == 1
        assert ambiguous[0]["remote_id"] == "TM-DUP-001"

    def test_missing_same_namespace_elevation_awaits_ack(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001", Status="ELEVATED",
            ElevatedTo="TM-ROOT-999")])
        install_discovery(monkeypatch, [ROOT_REGISTER])

        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)

        assert code == 0, lines
        assert any(item["class"] == "ORPHANED_LINK"
                   and item["remote_id"] == "TM-ROOT-999"
                   for item in data["findings"])
        assert any(item["class"] == "OUTBOUND_AWAITING_ACK"
                   and item["remote_id"] == "TM-ROOT-999"
                   for item in data["findings"])

    def test_source_tokens_are_exact_and_notes_are_never_joined(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001",
            SourceRef="prefixTM-APP-001suffix TM-APP-001-extra",
            Notes="TM-APP-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 0, lines
        assert not any(item["remote_id"] == "TM-APP-001"
                       for item in data["findings"])

    def test_directional_classes_are_relative_to_invoking_register(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001")])
        write_register(tmp_path / DOMAIN_REGISTER, [
            good_row(ActionItemID="TM-DOMAIN-001",
                     SourceRef="TM-ROOT-001"),
            good_row(ActionItemID="TM-DOMAIN-002", Status="ELEVATED",
                     ElevatedTo="TM-ROOT-999"),
        ])
        install_discovery(
            monkeypatch, [ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER])

        code, lines, data = run_federation(tmp_path, APP_REGISTER)
        assert code == 0, lines
        unrelated_ids = {"TM-DOMAIN-001", "TM-DOMAIN-002", "TM-ROOT-001",
                         "TM-ROOT-999"}
        directional = {
            "INBOUND_ELEVATION", "FOREIGN_LINK_TO_LOCAL",
            "LOCAL_LINK_TO_FOREIGN", "OUTBOUND_AWAITING_ACK",
        }
        assert not any(
            item["class"] in directional
            and ({item["local_id"], item["remote_id"]} & unrelated_ids)
            for item in data["findings"]
        )
        assert any(item["class"] == "ORPHANED_LINK"
                   and item["local_id"] == "TM-DOMAIN-002"
                   for item in data["findings"])


class TestFederationNoticesAndPresentation:
    def test_semicolon_wrappers_working_root_repo_root_missing_and_ambiguous(
            self, tmp_path, monkeypatch):
        project_root = tmp_path / "projects" / "app"
        (project_root / "notices").mkdir(parents=True)
        (project_root / "notices" / "work.md").write_text(
            "work", encoding="utf-8")
        (tmp_path / "root-notice.md").write_text("root", encoding="utf-8")
        (project_root / "shared.md").write_text("project", encoding="utf-8")
        (tmp_path / "shared.md").write_text("root", encoding="utf-8")
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001",
            NoticeRef=("`notices/work.md`; 'root-notice.md'; "
                       "\"shared.md\"; missing.md; NONE"))])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])
        code, lines, data = run_federation(tmp_path, APP_REGISTER)
        assert code == 0, lines
        missing = [item for item in data["findings"]
                   if item["class"] == "MISSING_NOTICE"]
        ambiguous = [item for item in data["findings"]
                     if item["class"] == "AMBIGUOUS_REFERENCE"]
        assert [item["evidence"] for item in missing] == ["missing.md"]
        assert len(ambiguous) == 1
        assert ambiguous[0]["evidence"] == "shared.md"

    def test_non_root_filters_foreign_findings_but_keeps_program_integrity(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001", NoticeRef="root-missing.md")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-DUP-001")])
        write_register(tmp_path / DOMAIN_REGISTER, [good_row(
            ActionItemID="TM-DUP-001")])
        install_discovery(
            monkeypatch, [ROOT_REGISTER, APP_REGISTER, DOMAIN_REGISTER])
        code, lines, data = run_federation(tmp_path, APP_REGISTER)
        assert code == 0, lines
        assert any(item["class"] == "MISSING_NOTICE"
                   for item in data["findings"])
        assert not any(item["class"] == "MISSING_NOTICE"
                       for item in data["presented_findings"])
        assert any(item["class"] == "DUPLICATE_GLOBAL_ID"
                   for item in data["presented_findings"])

    def test_deterministic_bytes_and_register_hash_equality(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / APP_REGISTER, [good_row(
            ActionItemID="TM-APP-001", SourceRef="TM-ROOT-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER, APP_REGISTER])
        register_bytes = {
            path: (tmp_path / path).read_bytes()
            for path in (ROOT_REGISTER, APP_REGISTER)
        }
        out = tmp_path / "stable.json"
        first_code, first_lines = taskmgmt.federation(
            tmp_path, Path(APP_REGISTER), out)
        first = out.read_bytes()
        second_code, second_lines = taskmgmt.federation(
            tmp_path, Path(APP_REGISTER), out)
        assert first_code == second_code == 0, (first_lines, second_lines)
        assert out.read_bytes() == first
        assert all((tmp_path / path).read_bytes() == before
                   for path, before in register_bytes.items())
        data = json.loads(first)
        assert all(item["before_sha256"] == item["after_sha256"]
                   for item in data["registers"])


class TestDedupLoopIdentity:
    """Regression for the cross-loop notice dedup false-negative: same-named
    surfaces routed to different loops must never fold into one candidate."""

    def test_loop_of_source(self):
        assert taskmgmt.loop_of_source(
            "execution/_Coordination/x.md") == "ROOT"
        assert taskmgmt.loop_of_source(
            "projects/app/execution/x.md") == "projects/app"
        assert taskmgmt.loop_of_source(
            "domains/handbook/file.md") == "domains/handbook"
        assert taskmgmt.loop_of_source(
            "_DomainEngines/fixture-engine/_TaskManagement/x.csv") == "_DomainEngines/fixture-engine"

    def test_same_named_notices_in_different_loops_stay_distinct(
            self, tmp_path):
        for loop in ("alpha", "beta"):
            co = tmp_path / "projects" / loop / "execution" / "_Coordination"
            co.mkdir(parents=True)
            (co / "NOTICE_SHARED.md").write_text("# shared\n", encoding="utf-8")
        out = tmp_path / "out.json"
        code, _ = taskmgmt.scan(tmp_path, tmp_path / "missing.csv", out)
        assert code == 0
        data = json.loads(out.read_text())
        kept = [c for c in data["candidates"]
                if c["class"] == "notice-not-in-ledger"]
        assert {c["source"] for c in kept} == {
            "projects/alpha/execution/_Coordination/NOTICE_SHARED.md",
            "projects/beta/execution/_Coordination/NOTICE_SHARED.md",
        }
        assert data["dedup_dropped_copies"] == 0

    def test_intra_loop_canonical_copy_still_folds(self, tmp_path):
        co = tmp_path / "execution" / "_Coordination"
        co.mkdir(parents=True)
        (co / "NOTICE_STATUS_X.csv").write_text(
            "NoticePath,AcknowledgementState\n"
            "a/NOTICE_ONE.md,TRACKED_OPEN\n", encoding="utf-8")
        ev = tmp_path / "execution" / "_Evaluation" / "SNAP"
        ev.mkdir(parents=True)
        (ev / "NOTICE_STATUS_X.csv").write_text(
            (co / "NOTICE_STATUS_X.csv").read_text(), encoding="utf-8")
        out = tmp_path / "out.json"
        code, _ = taskmgmt.scan(tmp_path, tmp_path / "missing.csv", out)
        assert code == 0
        data = json.loads(out.read_text())
        kept = [c for c in data["candidates"]
                if c["class"] == "notice-tracked-open"]
        assert len(kept) == 1
        assert "_Coordination" in kept[0]["source"]
        assert data["dedup_dropped_copies"] == 1


ROOT_ARCHIVE = "execution/_Coordination/_TaskManagement/REGISTER_CLOSED.csv"


class TestArchive:
    def test_moves_closed_rows_and_is_idempotent(self, tmp_path):
        reg = tmp_path / ROOT_REGISTER
        write_register(reg, [
            good_row(ActionItemID="TM-ROOT-001"),
            closed_row("TM-ROOT-002"),
            good_row(ActionItemID="TM-ROOT-003", Status="DEFERRED",
                     Trigger="an event"),
            closed_row("TM-ROOT-004"),
        ])
        code, lines = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code == 0, lines
        live = list(csv.DictReader(open(reg, newline="", encoding="utf-8")))
        assert [r["ActionItemID"] for r in live] == [
            "TM-ROOT-001", "TM-ROOT-003"]
        arch = tmp_path / ROOT_ARCHIVE
        with open(arch, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames == taskmgmt.CANONICAL_COLUMNS
            archived = list(reader)
        assert [r["ActionItemID"] for r in archived] == [
            "TM-ROOT-002", "TM-ROOT-004"]
        assert taskmgmt.validate_register(tmp_path, Path(ROOT_REGISTER))[0] == 0
        assert taskmgmt.validate_register(tmp_path, Path(ROOT_ARCHIVE))[0] == 0
        arch_bytes = arch.read_bytes()
        code2, lines2 = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code2 == 0
        assert "0 CLOSED row(s) moved" in lines2[0]
        assert arch.read_bytes() == arch_bytes

    def test_dry_run_moves_nothing(self, tmp_path):
        reg = tmp_path / ROOT_REGISTER
        write_register(reg, [closed_row("TM-ROOT-001")])
        before = reg.read_bytes()
        code, lines = taskmgmt.archive_register(
            tmp_path, Path(ROOT_REGISTER), dry_run=True)
        assert code == 0
        assert "DRY-RUN" in lines[0]
        assert "1 CLOSED row(s) would move" in lines[0]
        assert reg.read_bytes() == before
        assert not (tmp_path / ROOT_ARCHIVE).exists()

    def test_refuses_invalid_live_register(self, tmp_path):
        reg = tmp_path / ROOT_REGISTER
        write_register(reg, [good_row(Status="IN_PROGRESS")])
        before = reg.read_bytes()
        code, lines = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code == 1
        assert "REFUSED" in lines[0]
        assert reg.read_bytes() == before

    def test_refuses_archive_with_non_closed_row(self, tmp_path):
        write_register(tmp_path / ROOT_REGISTER, [closed_row("TM-ROOT-001")])
        write_register(tmp_path / ROOT_ARCHIVE, [
            good_row(ActionItemID="TM-ROOT-002")])
        code, lines = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code == 1
        assert "non-CLOSED" in "\n".join(lines)

    def test_refuses_duplicate_id_across_live_and_archive(self, tmp_path):
        write_register(tmp_path / ROOT_REGISTER, [closed_row("TM-ROOT-001")])
        write_register(tmp_path / ROOT_ARCHIVE, [closed_row("TM-ROOT-001")])
        code, lines = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code == 1
        assert "both" in "\n".join(lines)

    def test_operational_on_missing_register(self, tmp_path):
        code, lines = taskmgmt.archive_register(tmp_path, Path(ROOT_REGISTER))
        assert code == 2

    def test_cli(self, tmp_path, monkeypatch, capsys):
        write_register(tmp_path / ROOT_REGISTER, [closed_row("TM-ROOT-001")])
        monkeypatch.setattr(taskmgmt, "repo_root", lambda: tmp_path)
        assert taskmgmt.main([
            "archive", "--register", ROOT_REGISTER]) == 0
        assert "archive COMPLETE" in capsys.readouterr().out
        assert (tmp_path / ROOT_ARCHIVE).is_file()


class TestFederationArchive:
    def test_archive_lookalike_exclusions(self):
        canonical, exclusions = taskmgmt.classify_archive_paths(
            [ROOT_ARCHIVE, "tools/fixture/_TaskManagement/REGISTER_CLOSED.csv"],
            ["scratch/_TaskManagement/REGISTER_CLOSED.csv"])
        assert canonical == [ROOT_ARCHIVE]
        assert {item["path"] for item in exclusions} == {
            "tools/fixture/_TaskManagement/REGISTER_CLOSED.csv",
            "scratch/_TaskManagement/REGISTER_CLOSED.csv",
        }

    def test_archived_rows_resolve_links_counts_and_zero_write(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001"),
            good_row(ActionItemID="TM-ROOT-003", Status="DEFERRED",
                     Trigger="an event"),
        ])
        write_register(tmp_path / ROOT_ARCHIVE, [closed_row("TM-ROOT-002")])
        write_register(tmp_path / APP_REGISTER, [
            good_row(ActionItemID="TM-APP-001", SourceRef="TM-ROOT-002")])
        install_discovery(
            monkeypatch, [ROOT_REGISTER, ROOT_ARCHIVE, APP_REGISTER])
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 0, lines
        classes = {item["class"] for item in data["findings"]}
        assert "FOREIGN_LINK_TO_LOCAL" in classes
        assert "LOCAL_CLOSED_REMOTE_OPEN" in classes
        assert "ORPHANED_LINK" not in classes
        root_entry = next(item for item in data["registers"]
                          if item["path"] == ROOT_REGISTER)
        assert root_entry["status_counts"] == {
            "OPEN": 1, "DEFERRED": 1, "ELEVATED": 0, "CLOSED": 0}
        assert root_entry["archive_path"] == ROOT_ARCHIVE
        assert root_entry["archive_tracked"] is True
        assert root_entry["archive_row_count"] == 1
        assert root_entry["archive_validation"] == "PASS"
        assert (root_entry["archive_before_sha256"]
                == root_entry["archive_after_sha256"])
        assert data["zero_write_proof"]["register_writes"] == 0
        assert any(
            "ROOT: OPEN=1 DEFERRED=1 ELEVATED=0 CLOSED=0; archived=1" in line
            for line in lines)

    def test_untracked_archive_sibling_still_attaches(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / ROOT_ARCHIVE, [closed_row("TM-ROOT-002")])
        install_discovery(monkeypatch, [ROOT_REGISTER])
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 0, lines
        root_entry = next(item for item in data["registers"]
                          if item["path"] == ROOT_REGISTER)
        assert root_entry["archive_row_count"] == 1
        assert root_entry["archive_tracked"] is False

    def test_non_closed_archive_row_is_invalid_and_partial(
            self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / ROOT_ARCHIVE, [
            good_row(ActionItemID="TM-ROOT-002")])
        install_discovery(monkeypatch, [ROOT_REGISTER, ROOT_ARCHIVE])
        code, lines, data = run_federation(tmp_path, ROOT_REGISTER)
        assert code == 1, lines
        assert data["coverage"] == "PARTIAL"
        assert any(item["class"] == "INVALID_REGISTER"
                   and ROOT_ARCHIVE in item["register_paths"]
                   for item in data["findings"])

    def test_output_may_not_alias_an_archive(self, tmp_path, monkeypatch):
        write_register(tmp_path / ROOT_REGISTER, [
            good_row(ActionItemID="TM-ROOT-001")])
        write_register(tmp_path / ROOT_ARCHIVE, [closed_row("TM-ROOT-002")])
        install_discovery(monkeypatch, [ROOT_REGISTER, ROOT_ARCHIVE])
        code, lines = taskmgmt.federation(
            tmp_path, Path(ROOT_REGISTER), tmp_path / ROOT_ARCHIVE)
        assert code == 2
        assert "resolves to a register surface" in "\n".join(lines)

    def test_scan_known_refs_include_archived_rows(self, tmp_path):
        au = tmp_path / "projects" / "p" / "_audit"
        au.mkdir(parents=True)
        (au / "X_TBD_Register.csv").write_text(
            "TBDID,Question\nTBD-1,how\n", encoding="utf-8")
        reg = tmp_path / "REGISTER.csv"
        write_register(reg, [good_row()])
        write_register(reg.parent / "REGISTER_CLOSED.csv", [closed_row(
            "TM-TEST-009",
            SourceRef="projects/p/_audit/X_TBD_Register.csv row TBD-1")])
        out = tmp_path / "out.json"
        code, _ = taskmgmt.scan(tmp_path, reg, out)
        assert code == 0
        data = json.loads(out.read_text())
        tbd = [c for c in data["candidates"]
               if c["class"] == "tbd-register-row"]
        assert tbd and tbd[0]["known_to_register"] is True


class TestFederationCliCompatibility:
    def test_validate_scan_and_federation_parsers_coexist(
            self, tmp_path, monkeypatch, capsys):
        write_register(tmp_path / ROOT_REGISTER, [good_row(
            ActionItemID="TM-ROOT-001")])
        install_discovery(monkeypatch, [ROOT_REGISTER])
        monkeypatch.setattr(taskmgmt, "repo_root", lambda: tmp_path)

        assert taskmgmt.main([
            "validate", "--register", ROOT_REGISTER]) == 0
        assert "validate PASS" in capsys.readouterr().out

        scan_out = tmp_path / "scan.json"
        assert taskmgmt.main([
            "scan", "--register", ROOT_REGISTER, "--out", str(scan_out)]) == 0
        assert scan_out.is_file()
        assert "scan COMPLETE" in capsys.readouterr().out

        federation_out = tmp_path / "federation.json"
        assert taskmgmt.main([
            "federation", "--register", ROOT_REGISTER,
            "--out", str(federation_out)]) == 0
        assert federation_out.is_file()
        assert "federation COMPLETE" in capsys.readouterr().out


def test_pec_canonical_home_matches_source_loop():
    register = "projects/pec/execution/_Coordination/_TaskManagement/REGISTER.csv"
    assert taskmgmt.classify_register_paths([register], [])[0] == [register]
    assert taskmgmt.loop_of_source(register) == "projects/pec"
    assert taskmgmt.loop_of_source("projects/pec/execution/PKG-01/file.md") == "projects/pec"
