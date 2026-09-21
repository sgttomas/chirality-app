from pathlib import Path
import pytest
from normalize_brief import normalize, load_brief


def test_roots_inline_and_explicit_authority(tmp_path):
    scope=tmp_path/'projects/demo/output';scope.mkdir(parents=True)
    brief={'ScopePath':'{REPO_ROOT}/projects/demo/output','ApplyEdits':True,'AllowedWriteTargets':['{WORKING_ROOT}/output/result.md'],'TaskProfile':'DELIVERABLE_TASK'}
    result=normalize(brief,tmp_path,tmp_path,{'Tasks':['file task']})
    assert result['WorkingRoot']==str(tmp_path/'projects/demo')
    assert result['AllowedWriteTargets']==[str(scope/'result.md')]
    assert result['Tasks']==['file task']
    assert normalize({'ScopePath':str(scope)},tmp_path,tmp_path)['AllowedWriteTargets']==[]
    with pytest.raises(ValueError,match='disagree'):normalize(brief,tmp_path,tmp_path,{'ScopePath':str(tmp_path)})
    with pytest.raises(ValueError,match='OUTSIDE'):normalize({**brief,'AllowedWriteTargets':['{REPO_ROOT}/projects/other/file']},tmp_path,tmp_path)


def test_legacy_fallback_file_and_readonly(tmp_path):
    (tmp_path/'INIT-TASK.md').write_text('Tasks: [file task]\nApplyEdits: true\nAllowedWriteTargets: [result.md]\n')
    result=load_brief({'DeliverablePath':str(tmp_path),'ApplyEdits':False},tmp_path,tmp_path)
    assert result['ScopePath']==str(tmp_path)
    assert result['AllowedWriteTargets']==[]
    assert result['Tasks']==['file task']
    with pytest.raises(ValueError,match='unsupported'):normalize({'ScopePath':str(tmp_path),'TaskProfile':'SPECIAL'},tmp_path,tmp_path)


def test_symlink_write_and_alias_conflict(tmp_path):
    outside=tmp_path.parent/'outside';outside.mkdir(exist_ok=True)
    (tmp_path/'link').symlink_to(outside,target_is_directory=True)
    with pytest.raises(ValueError,match='OUTSIDE'):normalize({'ScopePath':str(tmp_path),'ApplyEdits':True,'AllowedWriteTargets':['link/*']},tmp_path,tmp_path)
    child=tmp_path/'child';child.mkdir()
    with pytest.raises(ValueError,match='conflicting'):normalize({'ScopePath':str(child),'WorkingRoot':str(tmp_path),'WORKING_ROOT':str(child)},tmp_path,tmp_path)


def test_apply_edits_rejects_numeric_boolean(tmp_path):
    for value in (0,1,'true'):
        with pytest.raises(ValueError,match='boolean'):
            normalize({'ScopePath':str(tmp_path),'ApplyEdits':value},tmp_path,tmp_path)
