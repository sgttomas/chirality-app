import sys

import tools.retrieval.scaffold_research_packet as scaffold
import tools.source_catalog.research_packet as rp


def run(argv, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["scaffold_research_packet.py", *argv])
    return scaffold.main()


def test_scaffold_creates_immutable_packet_with_canonical_headers(tmp_path, monkeypatch):
    root = tmp_path / "_Research"
    rc = run(
        ["--research-root", str(root), "--slug", "Demo Topic!", "--utc", "20260101T000000Z"],
        monkeypatch,
    )
    assert rc == 0
    packet = root / "RCH_20260101T000000Z_demo_topic"
    expected = {
        "RESEARCH_NOTE.md", "Query_Log.csv", "Evidence_Map.csv",
        "Amendment_Candidates.csv", "Open_Questions.csv", "Conflicts.csv",
        "HANDOFF_STATE.md",
    }
    assert {p.name for p in packet.iterdir()} == expected

    # CSV headers exactly match the single-source-of-truth schema.
    em_header = (packet / "Evidence_Map.csv").read_text(encoding="utf-8").splitlines()[0]
    assert em_header == ",".join(rp.EVIDENCE_MAP_COLUMNS)
    ql_header = (packet / "Query_Log.csv").read_text(encoding="utf-8").splitlines()[0]
    assert ql_header == ",".join(rp.QUERY_LOG_COLUMNS)

    # _LATEST.md points at the packet.
    latest = (root / "_LATEST.md").read_text(encoding="utf-8")
    assert "RCH_20260101T000000Z_demo_topic" in latest


def test_scaffold_refuses_to_overwrite_existing_packet(tmp_path, monkeypatch):
    root = tmp_path / "_Research"
    args = ["--research-root", str(root), "--slug", "demo", "--utc", "20260101T000000Z"]
    assert run(args, monkeypatch) == 0
    sentinel = root / "RCH_20260101T000000Z_demo" / "RESEARCH_NOTE.md"
    sentinel.write_text("EDITED", encoding="utf-8")
    # second identical call must refuse and not clobber
    assert run(args, monkeypatch) == 1
    assert sentinel.read_text(encoding="utf-8") == "EDITED"


def test_no_update_latest_flag(tmp_path, monkeypatch):
    root = tmp_path / "_Research"
    rc = run(
        ["--research-root", str(root), "--slug", "x", "--utc", "20260101T000000Z", "--no-update-latest"],
        monkeypatch,
    )
    assert rc == 0
    assert not (root / "_LATEST.md").exists()


def test_exact_output_and_pointer_ownership(tmp_path, monkeypatch):
    root=tmp_path/'research';root.mkdir()
    (root/'_LATEST.md').write_text('accepted pointer')
    output=root/'nested'/'authorized-output'
    assert run(['--research-root',str(root),'--slug','demo','--output-dir',str(output),'--no-update-latest'],monkeypatch)==0
    assert (output/'RESEARCH_NOTE.md').is_file()
    assert (root/'_LATEST.md').read_text()=='accepted pointer'
    import pytest
    with pytest.raises(SystemExit):run(['--research-root',str(root),'--slug','demo','--output-dir',str(tmp_path/'elsewhere')],monkeypatch)



def test_output_containment_independent_of_pointer_flag(tmp_path, monkeypatch):
    import pytest
    root=tmp_path/'research';root.mkdir()
    outside=tmp_path/'outside';outside.mkdir()
    (root/'escape').symlink_to(outside,target_is_directory=True)
    for output in (outside/'packet',root/'escape'/'packet'):
        for pointer_flags in ([],['--no-update-latest']):
            with pytest.raises(SystemExit) as caught:
                run(['--research-root',str(root),'--slug','demo','--output-dir',str(output),*pointer_flags],monkeypatch)
            assert caught.value.code==2
            assert not output.exists()
    assert not (root/'_LATEST.md').exists()
