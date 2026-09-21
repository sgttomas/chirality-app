import json
from pathlib import Path
import pytest
from resolve_workflow import resolve, resolve_tool, command_allowed, normalize_method_selection


@pytest.fixture
def root(tmp_path):
    (tmp_path/'agents').mkdir()
    (tmp_path/'agents/AGENT_TASK.md').write_text('# TASK\n')
    (tmp_path/'agents/registry.json').write_text(json.dumps({'schema_version':1,'roles':{'TASK':{'instruction':'agents/AGENT_TASK.md','type':2,'tools':['read','bash']}}}))
    package=tmp_path/'workflows/example';package.mkdir(parents=True)
    (package/'WORKFLOW.md').write_text('selected workflow')
    (package/'CONTRACT.md').write_text('selected contract')
    (package/'other.md').write_text('unselected')
    (package/'execution.json').write_text(json.dumps({'schema_version':1,'compatible_roles':['TASK'],'tools':{'capabilities':['read','bash'],'commands':['python3 tools/run.py:{scope_path}/**']}}))
    (tmp_path/'workflows/legacy-methods.json').write_text(json.dumps({
        'schema':'chirality-legacy-methods/v1',
        'convertedWorkflowAliases':{
            'converted-skill':{'kind':'skill','name':'converted-skill'},
            'old-workflow':{'kind':'workflow','name':'example'},
        },
        'historicalOnly':[],
        'unknownLegacyBehavior':'error',
    }))
    (tmp_path/'workflows/catalog.yaml').write_text(json.dumps({
        'schema':'chirality-workflow-catalog/v1',
        'library':{'source':'bundled','sourceRootId':'fixture-bundle'},
        'centralWorkflowNames':[],
    }))
    skill=tmp_path/'.agents/skills/converted-skill';skill.mkdir(parents=True)
    (skill/'SKILL.md').write_text('selected skill')
    (skill/'execution.json').write_text(json.dumps({'schema_version':1,'compatible_roles':['TASK'],'tools':{'capabilities':['read']}}))
    (tmp_path/'tools').mkdir();(tmp_path/'tools/run.py').write_text('')
    return tmp_path


def policy():
    return {'bindings':{'scope_path':'output'},'host':{'capabilities':['read','bash'],'commands':['python3 tools/run.py:*']},'brief':{'capabilities':['read']}}


def test_selection_context_and_independent_restrictions(root):
    result=resolve(root,'TASK','old-workflow','old_workflow',['CONTRACT.md'],policy=policy())
    assert result['effective_tools']['capabilities']==['read']
    assert command_allowed(result['effective_tools']['commands'],'python3','tools/run.py',['output/a'])
    assert not command_allowed(result['effective_tools']['commands'],'python3','tools/run.py',['outside/a'])
    assert [x['path'] for x in result['context']]==['agents/AGENT_TASK.md','workflows/example/WORKFLOW.md','workflows/example/CONTRACT.md']
    assert all(len(x['sha256'])==64 for x in result['context'])


def test_conflicts_missing_resource_empty_policy(root):
    with pytest.raises(ValueError,match='conflicting'):resolve(root,'TASK','example','converted-skill')
    with pytest.raises(ValueError,match='missing'):resolve(root,'TASK','example',resources=['missing'])
    p=policy();p['brief']['commands']=[];p['brief']['capabilities']=[]
    result=resolve(root,'TASK','example',policy=p)
    assert result['effective_tools']['capabilities']==[]
    assert not command_allowed(result['effective_tools']['commands'],'python3','tools/run.py',['output/a'])


def test_optional_workflow_cwd_and_path_escape(root,monkeypatch,tmp_path):
    monkeypatch.chdir('/tmp')
    assert resolve_tool(root,'tools/run.py')==str(root/'tools/run.py')
    assert len(resolve(root,'TASK')['context'])==1
    with pytest.raises(ValueError):resolve_tool(root,'tools/../../missing')
    outside=root.parent/'outside-workflow';outside.mkdir(exist_ok=True);(outside/'WORKFLOW.md').write_text('escape')
    (root/'workflows/escape').symlink_to(outside,target_is_directory=True)
    with pytest.raises(ValueError,match='escapes'):resolve(root,'TASK','escape')
    (root/'workflows/example/escape.md').symlink_to(root/'agents/AGENT_TASK.md')
    with pytest.raises(ValueError,match='escaping'):resolve(root,'TASK','example',resources=['escape.md'])


def test_unbound_wrong_role_and_malformed(root):
    with pytest.raises(ValueError,match='unbound'):resolve(root,'TASK','example')
    c=root/'workflows/example/execution.json';c.write_text(json.dumps({'schema_version':1,'compatible_roles':['WORKING_ITEMS']}))
    with pytest.raises(ValueError,match='incompatible'):resolve(root,'TASK','example')
    (root/'agents/registry.json').write_text('[]')
    with pytest.raises(ValueError,match='registry'):resolve(root,'TASK')


def test_cli_fingerprints_both_brief_surfaces_and_policy(root,tmp_path):
    import subprocess
    import sys
    script=Path(__file__).with_name('resolve_workflow.py')
    brief=root/'inline.json';file_brief=root/'INIT-TASK.md';policy_file=root/'policy.json'
    file_brief.write_text('Tasks: [bounded work]\n')
    brief.write_text(json.dumps({'ScopePath':str(root),'InitTaskPath':str(file_brief)}))
    policy_file.write_text('{}')
    proc=subprocess.run([sys.executable,str(script),'--root',str(root),'--role','TASK','--repo-root',str(root),'--brief',str(brief),'--policy',str(policy_file)],text=True,capture_output=True,check=True)
    result=json.loads(proc.stdout)
    basis={item['path']:item for item in result['configuration_basis']}
    assert {'inline.json','INIT-TASK.md','policy.json'}<=basis.keys()
    assert basis['inline.json']['source_root']==str(root)
    assert result['brief']['Tasks']==['bounded work']


def test_dot_target_cannot_escape_command_scope(root):
    result=resolve(root,'TASK','example',policy=policy())
    assert not command_allowed(result['effective_tools']['commands'],'python3','tools/run.py',['output/../outside/a'])


def test_resolved_tool_invokes_outside_instruction_checkout(root,tmp_path):
    import subprocess
    import sys
    (root/'tools/run.py').write_text("print('resolved tool invoked')\n")
    command=resolve_tool(root,'tools/run.py')
    result=subprocess.run([sys.executable,command],cwd='/tmp',text=True,capture_output=True,check=True)
    assert result.stdout.strip()=='resolved tool invoked'


def test_tool_paths_cannot_escape_tools_directory(root):
    (root/'AGENTS.md').write_text('governance')
    with pytest.raises(ValueError,match='tools directory'):resolve_tool(root,'tools/../AGENTS.md')
    (root/'tools/escape.py').symlink_to(root/'AGENTS.md')
    with pytest.raises(ValueError,match='tools directory'):resolve_tool(root,'tools/escape.py')


def test_legacy_normalization_shared_cases(root):
    fixture=Path(__file__).with_name('fixtures')/'legacy_method_normalization_cases.json'
    cases=json.loads(fixture.read_text())['cases']
    for case in cases:
        inputs=case['input']
        if 'error' in case:
            with pytest.raises(ValueError,match=case['error']['messagePattern']):
                normalize_method_selection(root,inputs.get('workflow'),inputs.get('taskSkill'),inputs.get('methods',[]))
            continue
        result=normalize_method_selection(root,inputs.get('workflow'),inputs.get('taskSkill'),inputs.get('methods',[]))
        assert result['methods']==case['outcome']['methods'],case['id']
        assert result['compatibility_inputs']==case['outcome']['compatibilityInputs'],case['id']
        assert result['mapping_decisions']==case['outcome']['decisions'],case['id']


def test_converted_task_skill_loads_skill_and_records_mapping_basis(root):
    result=resolve(root,'TASK',task_skill='converted_skill')
    assert result['methods']==[{'sourceRootId':'fixture-bundle','source':'bundled','kind':'skill','name':'converted-skill'}]
    assert result['workflow'] is None
    assert [x['path'] for x in result['context']]==['agents/AGENT_TASK.md','.agents/skills/converted-skill/SKILL.md']
    assert 'workflows/legacy-methods.json' in [x['path'] for x in result['configuration_basis']]
    assert result['method_selection']['original_inputs']['TaskSkill']=='converted_skill'


def test_explicit_historical_workflow_loads_workflow_package(root):
    result=resolve(root,'TASK',workflow='fixture-bundle:bundled:workflow:example',policy=policy())
    assert result['methods']==[{'sourceRootId':'fixture-bundle','source':'bundled','kind':'workflow','name':'example'}]
    assert result['workflow']=='example'
    assert result['context'][1]['path']=='workflows/example/WORKFLOW.md'


def test_ordered_different_methods_remain_valid(root):
    result=resolve(root,'TASK',workflow='old-workflow',methods=[{'kind':'skill','name':'converted-skill'}],policy=policy())
    assert result['methods']==[
        {'sourceRootId':'fixture-bundle','source':'bundled','kind':'skill','name':'converted-skill'},
        {'sourceRootId':'fixture-bundle','source':'bundled','kind':'workflow','name':'example'},
    ]
    assert [x['path'] for x in result['context'][1:]]==['.agents/skills/converted-skill/SKILL.md','workflows/example/WORKFLOW.md']


def test_foreign_qualified_identity_is_rejected(root):
    with pytest.raises(ValueError,match='outside the declared Root catalog'):
        resolve(root,'TASK',workflow='foreign:user:workflow:example')


def test_same_name_different_origin_is_not_deduplicated(root):
    with pytest.raises(ValueError,match='outside the declared Root catalog'):
        normalize_method_selection(
            root,task_skill='converted-skill',
            methods=[{'sourceRootId':'foreign','source':'user','kind':'skill','name':'converted-skill'}],
        )


def test_catalog_identity_is_recorded_and_controls_qualification(root):
    first=resolve(root,'TASK',task_skill='converted-skill')
    first_basis=next(item for item in first['configuration_basis'] if item['path']=='workflows/catalog.yaml')
    catalog=root/'workflows/catalog.yaml'
    value=json.loads(catalog.read_text());value['library']['sourceRootId']='fixture-bundle-v2';catalog.write_text(json.dumps(value))
    second=resolve(root,'TASK',task_skill='converted-skill')
    second_basis=next(item for item in second['configuration_basis'] if item['path']=='workflows/catalog.yaml')
    assert first_basis['sha256'] != second_basis['sha256']
    assert second['methods'][0]['sourceRootId']=='fixture-bundle-v2'
