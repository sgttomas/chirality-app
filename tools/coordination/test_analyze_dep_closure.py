import csv
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("closure_audit", Path(__file__).with_name("analyze_dep_closure.py"))
closure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(closure)


def put(root, unit, target=None, **extra):
    path = root / f"PKG-01_A/1_Working/{unit}/Dependencies.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {name: "" for name in closure.REQUIRED_COLUMNS}
    row.update(RegisterSchemaVersion="v3.1", DependencyID="D-1", FromDeliverableID=unit.split("_")[0], DependencyClass="EXECUTION", AnchorType="NOT_APPLICABLE",
        Direction="UPSTREAM", DependencyType="PREREQUISITE", TargetType="DELIVERABLE", TargetDeliverableID=target or "DEL-01-01", Explicitness="EXPLICIT",
        SatisfactionStatus="TBD", Confidence="HIGH", Origin="DECLARED", Status="ACTIVE", EvidenceFile="source.md")
    row.update(extra)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=closure.REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(row)
    return path


def test_registerless_isolated_and_missing_target_are_separate(tmp_path):
    put(tmp_path, "DEL-01-01_A", "DEL-01-99")
    (tmp_path / "PKG-01_A/1_Working/DEL-01-02_B").mkdir()
    summary, data = closure.analyze(tmp_path)
    assert summary["orphan_count"] == 1
    assert data["orphans"][0]["TargetDeliverableID"] == "DEL-01-99"
    assert data["isolated"] == ["DEL-01-02"]
    assert data["coverage"][1]["HasDependencyCsv"] == "N"
    assert summary["schema_invalid"] == 1


def test_scope_status_normalization_and_threshold(tmp_path):
    put(tmp_path, "DEL-01-01_A", "DEL-01-02_Label", Status="RETIRED")
    put(tmp_path, "DEL-01-02_B", "DEL-01-01")
    summary, data = closure.analyze(tmp_path, ["DEL-01-01"], active_only=False, hub_threshold=1)
    assert summary["graph_edges"] == 1 and summary["orphan_count"] == 0
    assert summary["outside_scope_count"] == 1 and summary["normalization_count"] == 1
    assert summary["hub_count"] == 2
    assert closure.analyze(tmp_path, ["DEL-01-01"])[0]["graph_edges"] == 0
    assert closure.analyze(tmp_path, active_only=False, normalize_ids=False)[0]["orphan_count"] == 1


def test_malformed_rows_excluded_and_cycle_bounded(tmp_path):
    path = put(tmp_path, "DEL-01-01_A", "DEL-01-02")
    with path.open("a") as stream:
        stream.write("bad,row\n")
    put(tmp_path, "DEL-01-02_B", "DEL-01-01")
    summary, data = closure.analyze(tmp_path, max_cycles=0)
    assert summary["schema_invalid"] == 1
    assert summary["graph_edges"] == 2
    assert summary["scc_count"] == 1 and data["cycles"] == []
    assert summary["cycles_truncated"]
    path.write_text(path.read_text().replace("Direction", "WrongColumn"))
    assert closure.analyze(tmp_path)[0]["graph_edges"] == 1


def test_self_cycle_and_large_graph():
    graph = {str(i): {str(i+1)} for i in range(3000)}
    graph["3000"] = {"0"}
    assert len(closure.find_sccs(graph, set(graph))[0]) == 3001
    assert closure.find_sccs({"A": {"A"}}, {"A"}) == [["A"]]


def test_cli_outputs_and_prior_comparison(tmp_path, capsys):
    put(tmp_path, "DEL-01-01_A", "DEL-01-01")
    output = tmp_path / "reports"
    assert closure.main([str(tmp_path), "--output-dir", str(output), "--hub-threshold", "1", "--max-cycles", "1"]) == 0
    assert (output / "cycles_sample.csv").is_file()
    summary = json.loads((output / "closure_summary.json").read_text())
    assert summary["run_status"] == "COMPLETE" and summary["subject_status"] == "FAIL"
    assert closure.main([str(tmp_path), "--prior-summary", str(output / "closure_summary.json")]) == 0
    assert closure.main([str(tmp_path), "--scope", "DEL-99-99"]) == 2
