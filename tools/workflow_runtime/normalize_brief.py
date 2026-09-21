#!/usr/bin/env python3
"""Normalize structured inline/file briefs; no returned field grants host permissions."""
from pathlib import Path

PATH_FIELDS=('ScopePath','DeliverablePath','InitTaskPath','INIT_TASK_PATH','WorkingRoot','WORKING_ROOT')


def expand(value, bindings):
    if not isinstance(value,str): raise ValueError('path fields must be strings')
    for key, replacement in bindings.items():
        value=value.replace('${'+key+'}',str(replacement)).replace('{'+key+'}',str(replacement))
    if '{' in value or '}' in value: raise ValueError(f'unresolved path token: {value}')
    return value


def normalize(inline, repo_root, instruction_root, file_values=None):
    """Inline wins except disagreeing path fields. File parsing belongs to caller.

    Both roots are explicit, independently validated directories. A host adapter
    derives repo_root from its active checkout; process cwd supplies neither root.
    """
    if not isinstance(inline,dict) or (file_values is not None and not isinstance(file_values,dict)):
        raise ValueError('briefs must be mappings')
    repo_root=Path(repo_root).resolve(); instruction_root=Path(instruction_root).resolve()
    if not repo_root.is_dir() or not instruction_root.is_dir():raise ValueError('declared roots must exist')
    files=file_values or {}; merged={**files,**inline}
    bindings={'REPO_ROOT':repo_root,'INSTRUCTION_ROOT':instruction_root}
    def path(value):
        return (repo_root/expand(value,bindings)).resolve()
    explicit=merged.get('WorkingRoot',merged.get('WORKING_ROOT'))
    if explicit:
        working=path(explicit)
    else:
        anchor=merged.get('ScopePath',merged.get('DeliverablePath'))
        working=repo_root
        if anchor and '{WORKING_ROOT}' not in anchor and '${WORKING_ROOT}' not in anchor:
            concrete=path(anchor)
            if concrete.is_relative_to(repo_root):
                parts=concrete.relative_to(repo_root).parts
                if len(parts)>=2 and parts[0] in ('projects','domains'):working=repo_root/parts[0]/parts[1]
    if not working.is_relative_to(repo_root):raise ValueError('WORKING_ROOT outside active checkout')
    bindings['WORKING_ROOT']=working
    for key in PATH_FIELDS:
        if key in inline and key in files and path(inline[key])!=path(files[key]):raise ValueError(f'inline and file brief disagree on {key}')
        if key in merged:merged[key]=str(path(merged[key]))
    for left,right in [('InitTaskPath','INIT_TASK_PATH'),('WorkingRoot','WORKING_ROOT')]:
        if left in merged and right in merged and merged[left]!=merged[right]:raise ValueError(f'conflicting aliases: {left}/{right}')
    merged['ScopePath']=merged.get('ScopePath',merged.get('DeliverablePath'))
    if not merged['ScopePath']:raise ValueError('ScopePath is required')
    scope=Path(merged['ScopePath'])
    if not scope.exists():raise ValueError('ScopePath does not exist')
    if not scope.is_relative_to(working):raise ValueError('SCOPE_OUTSIDE_WORKTREE')
    for key in ('InitTaskPath','INIT_TASK_PATH'):
        if key in merged and not Path(merged[key]).is_file():raise ValueError('InitTaskPath does not exist')
    if merged.get('TaskProfile') not in (None,'','NONE','DELIVERABLE_TASK'):raise ValueError('unsupported TaskProfile')
    if not isinstance(merged.get('ApplyEdits',False),bool):raise ValueError('ApplyEdits must be boolean')
    if 'AllowedWriteTargets' in inline and 'AllowedWriteTargets' in files:
        if not isinstance(inline['AllowedWriteTargets'],list) or not isinstance(files['AllowedWriteTargets'],list):raise ValueError('AllowedWriteTargets must be lists')
        if sorted(str(path(x)) for x in inline['AllowedWriteTargets']) != sorted(str(path(x)) for x in files['AllowedWriteTargets']):raise ValueError('inline and file brief disagree on AllowedWriteTargets')
    targets=merged.get('AllowedWriteTargets',[])
    if not isinstance(targets,list):raise ValueError('AllowedWriteTargets must be a list')
    resolved=[]
    for target in targets:
        value=path(target)
        # Resolve the static prefix too: an existing symlink before a glob cannot escape.
        if not value.is_relative_to(working):raise ValueError('WRITE_TARGET_OUTSIDE_WORKTREE')
        resolved.append(str(value))
    merged['AllowedWriteTargets']=resolved if merged.get('ApplyEdits',False) else []
    merged['WorkingRoot']=str(working)
    merged['InstructionRoot']=str(instruction_root)
    merged['write_authority']='explicit normalized targets, subject to host enforcement'
    return merged


def load_brief(inline, repo_root, instruction_root):
    """Read JSON or YAML structured INIT-TASK input, filling omitted inline fields."""
    import json
    import yaml
    bindings={'REPO_ROOT':Path(repo_root).resolve(),'INSTRUCTION_ROOT':Path(instruction_root).resolve()}
    working=inline.get('WorkingRoot',inline.get('WORKING_ROOT'))
    bindings['WORKING_ROOT']=(Path(repo_root)/expand(working,bindings)).resolve() if working else Path(repo_root).resolve()
    explicit=inline.get('InitTaskPath',inline.get('INIT_TASK_PATH'))
    candidate=None
    if explicit:
        candidate=(Path(repo_root)/expand(explicit,bindings)).resolve()
        if not candidate.is_file():raise ValueError('InitTaskPath does not exist')
    else:
        for key in ('ScopePath','DeliverablePath'):
            if inline.get(key):
                trial=Path(repo_root)/expand(inline[key],bindings)/'INIT-TASK.md'
                if trial.is_file():candidate=trial;break
    file_values=None
    if candidate:
        raw=candidate.read_text()
        if raw.startswith('---\n'):raw=raw.split('---',2)[1]
        file_values=yaml.safe_load(raw)
        if not isinstance(file_values,dict):raise ValueError('file brief requires a structured YAML mapping or YAML frontmatter')
    result=normalize(inline,repo_root,instruction_root,file_values)
    result['file_brief']=str(candidate) if candidate else None
    return result
