"""Root-only H01-H06 component checks; shared authority is tested separately."""
import hashlib
from pathlib import Path

import pytest
import yaml

import adapter_loader
import adapter_project
import cmd_brief
import cmd_next
import root_historical_status as historical
from harness_common import HarnessOperationalError
from test_root_adoption import ROOT_ADAPTER_YAML

PRE = "# Status: DEL-01-01\n\n**Current State:** INITIALIZED\n\n## History\n- 2026-07-25 — State set to INITIALIZED (TASK)\n"
RECORD = "\n## SCA-005 retirement record\n\n[RETIRED — SCA-005] Historical source carrier; stable ID remains reserved. Successor: execution/_Coordination/GovernanceControls/GOV-01-01.md. No completion follows.\n"
POST = PRE.replace('**Current State:** INITIALIZED', '**Current State:** RETIRED') + RECORD


def fixture(tmp_path, monkeypatch, stage='effective', count=1):
    rows = []
    for index in range(count):
        rel = f'execution/PKG-01/1_Working/DEL-01-{index + 1:02d}_Fixture/_STATUS.md'
        path = tmp_path / rel
        path.parent.mkdir(parents=True)
        path.write_text(PRE if stage == 'prepared' else POST)
        rows.append(dict(path=rel, source_id=f'DEL-01-{index+1:02d}', source_package='PKG-01',
                         preimage_sha256=hashlib.sha256(PRE.encode()).hexdigest(),
                         postimage_sha256=hashlib.sha256(POST.encode()).hexdigest()))
    state = dict(stage=stage, source_statuses=rows)
    monkeypatch.setattr(historical, 'resolve_state', lambda root, config: state)
    data = yaml.safe_load(ROOT_ADAPTER_YAML.format(product='chirality-root', working_root='.',
        status_files=count, status_mismatch=0, pinned_at='fixture'))
    data.update(mode='governance-only', parser_dialect='root-historical-v1', states=['RETIRED'],
                governance_state={'path': 'fixture.json', 'sha256': '0'*64})
    adapter = tmp_path / 'execution/_harness/adapter.yaml'
    adapter.parent.mkdir(parents=True)
    adapter.write_text(yaml.safe_dump(data))
    return adapter_loader.load_adapter(tmp_path), state, tmp_path / rows[0]['path']


@pytest.mark.parametrize('stage', ['effective', 'applied_pending_confirmation'])
def test_historical_exact_census_is_not_active(tmp_path, monkeypatch, stage):
    manifest, state, path = fixture(tmp_path, monkeypatch, stage, count=53)
    assert len(adapter_project.collect_status_files(manifest)) == 53
    results = [adapter_project.analyze_status_file(p, manifest, tmp_path)
               for p in adapter_project.collect_status_files(manifest)]
    assert all(r.current_state == 'RETIRED' and not r.mismatch for r in results)
    assert all(r.assertion.rule == 'root_historical_retirement' for r in results)


def test_prepared_reads_preimage_without_retirement_claim(tmp_path, monkeypatch):
    manifest, state, path = fixture(tmp_path, monkeypatch, 'prepared')
    result = adapter_project.analyze_status_file(path, manifest, tmp_path)
    assert result.current_state == 'INITIALIZED'
    assert not result.mismatch
    path.write_text(POST)
    with pytest.raises(HarnessOperationalError, match='preimage'):
        adapter_project.analyze_status_file(path, manifest, tmp_path)


@pytest.mark.parametrize('mutation', ['record_missing', 'record_altered', 'current_wrong', 'trailing_assertion'])
def test_reject_bad_retirement_assertion_even_if_digest_matches(tmp_path, monkeypatch, mutation):
    manifest, state, path = fixture(tmp_path, monkeypatch)
    text = POST
    if mutation == 'record_missing': text = text.split('## SCA-005')[0]
    if mutation == 'record_altered': text = text.replace('[RETIRED — SCA-005]', '[retired]')
    if mutation == 'current_wrong': text = text.replace('**Current State:** RETIRED', '**Current State:** INITIALIZED')
    if mutation == 'trailing_assertion': text += '\n## History\n- 2026-09-06 — State set to INITIALIZED (TASK)\n'
    path.write_text(text)
    state['source_statuses'][0]['postimage_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    with pytest.raises(HarnessOperationalError):
        adapter_project.analyze_status_file(path, manifest, tmp_path)


def test_refuse_hash_and_census_mutations(tmp_path, monkeypatch):
    manifest, state, path = fixture(tmp_path, monkeypatch)
    path.write_text(POST + 'changed')
    with pytest.raises(HarnessOperationalError, match='postimage'):
        adapter_project.analyze_status_file(path, manifest, tmp_path)
    state['source_statuses'] = []
    with pytest.raises(HarnessOperationalError, match='census'):
        adapter_project.collect_status_files(manifest)


@pytest.mark.parametrize('stage', ['prepared', 'effective', 'applied_pending_confirmation'])
def test_direct_production_calls_refused(tmp_path, monkeypatch, stage):
    fixture(tmp_path, monkeypatch, stage)
    with pytest.raises(HarnessOperationalError, match='production'):
        cmd_next.run_next(tmp_path, [tmp_path], {})
    with pytest.raises(HarnessOperationalError, match='production'):
        cmd_brief.run_brief(tmp_path, tmp_path, [], 'DEL-01-01', None, None, tmp_path/'out')
    assert not (tmp_path/'out').exists()


def test_missing_effect_is_not_readable(tmp_path, monkeypatch):
    manifest, state, path = fixture(tmp_path, monkeypatch)
    monkeypatch.undo()
    with pytest.raises(HarnessOperationalError):
        adapter_loader.load_adapter(tmp_path)


def test_historical_symlink_escape_refused_before_read(tmp_path, monkeypatch):
    manifest, state, path = fixture(tmp_path, monkeypatch)
    path.unlink()
    path.symlink_to(tmp_path.parent / 'foreign-nonexistent-status')
    with pytest.raises(HarnessOperationalError, match='census'):
        historical.parse_historical_status(path, tmp_path, state)


def test_historical_status_and_drift_report_census(tmp_path, monkeypatch):
    import cmd_status
    import cmd_drift
    fixture(tmp_path, monkeypatch, count=53)
    report = cmd_status.run_status_project(tmp_path, tmp_path)
    text = report.render_markdown()
    assert 'Historical source census (not active workload)' in text
    assert '| RETIRED | 53 |' in text
    drift = cmd_drift.run_drift(tmp_path, [tmp_path])
    assert drift.summary['files_total'] == 53
    assert drift.summary['mismatches_total'] == 0
