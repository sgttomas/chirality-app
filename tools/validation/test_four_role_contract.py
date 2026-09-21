import json
from pathlib import Path
import validate_agent_instructions as agents
import validate_workflow_metadata as workflows
import validate_enum


def fixture(tmp_path):
    root=Path(__file__).resolve().parents[2]
    (tmp_path/'agents').mkdir()
    registry=json.loads((root/'agents/registry.json').read_text())
    for role,cfg in registry['roles'].items():
        (tmp_path/cfg['instruction']).write_text('# '+role+'\n\n'+'\n\n'.join('## '+heading+'\n\nRole behavior.' for heading in ['PROTOCOL','SPEC','STRUCTURE','RATIONALE']))
    (tmp_path/'agents/registry.json').write_text(json.dumps(registry))
    return registry


def test_roster_entry_and_non_delegation(tmp_path):
    registry=fixture(tmp_path)
    assert agents.validate_registry(tmp_path)==[]
    registry['roles']['TASK']['delegates_to']=['TASK']
    registry['roles']['TASK']['tools'].append('delegate_agent')
    (tmp_path/'agents/registry.json').write_text(json.dumps(registry))
    codes={x.code for x in agents.validate_registry(tmp_path)}
    assert {'ROLE_DELEGATION','TYPE2_DELEGATION'}<=codes
    (tmp_path/'agents/AGENT_OLD.md').write_text('old')
    assert 'ROLE_ROSTER' in {x.code for x in agents.validate_registry(tmp_path)}


def test_optional_workflow_resources_and_restricted_metadata(tmp_path):
    folder=tmp_path/'workflows/example';folder.mkdir(parents=True)
    (folder/'WORKFLOW.md').write_text('---\nname: example\ndescription: Example work\n---\nMethod')
    assert workflows.validate_workflow_dir(folder,tmp_path)['valid']
    (folder/'execution.json').write_text(json.dumps({'schema_version':1,'compatible_roles':['OLD']}))
    assert not workflows.validate_workflow_dir(folder,tmp_path)['valid']


def test_retired_is_a_valid_lifecycle_state():
    assert 'RETIRED' in validate_enum.ENUMS['LIFECYCLE_STATE']


def test_malformed_registry_shapes(tmp_path):
    import pytest
    fixture(tmp_path)
    path=tmp_path/'agents/registry.json'
    for value in ([],{'roles':[]}):
        path.write_text(json.dumps(value))
        with pytest.raises(ValueError,match='mapping'):agents.validate_registry(tmp_path)
    path.write_text(json.dumps({'schema_version':1,'roles':{'TASK':[]}}))
    assert 'ROLE_SHAPE' in {x.code for x in agents.validate_registry(tmp_path)}
