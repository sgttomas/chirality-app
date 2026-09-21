#!/usr/bin/env python3
"""Validate explicitly discoverable workflow entrypoints and optional execution policy."""
import argparse
import json
import re
from pathlib import Path
import yaml
from build_workflow_index import _frontmatter

ROLES={'HELP_HUMAN','HELPS_HUMANS','WORKING_ITEMS','TASK'}
NAME_RE=re.compile(r'^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$')


def validate_workflow_dir(folder, repo_root):
    issues=[]
    try:
        data=_frontmatter(folder/'WORKFLOW.md')
        if data.get('name')!=folder.name or not NAME_RE.fullmatch(folder.name):
            issues.append('name must match the lowercase-hyphen folder name')
        if not isinstance(data.get('description'),str) or not data['description'].strip():
            issues.append('description must be a nonempty string')
        companion=folder/'execution.json'
        if companion.exists():
            config=json.loads(companion.read_text())
            if config.get('schema_version')!=1: issues.append('execution schema_version must be 1')
            if 'stages' in config: issues.append('stage role overrides are unsupported; select a bounded workflow or brief')
            stages={}
            if not isinstance(stages,dict): raise ValueError('stages must be a mapping')
            for item in [config,*stages.values()]:
                compatible=item.get('compatible_roles')
                if compatible is not None and (not isinstance(compatible,list) or not set(compatible)<=ROLES): issues.append('invalid compatible_roles')
                tools=item.get('tools',{})
                if not isinstance(tools,dict) or set(tools)-{'capabilities','commands'}: raise ValueError('invalid tools mapping')
                for kind,values in tools.items():
                    if not isinstance(values,list) or any(not isinstance(x,str) for x in values): raise ValueError('tool restrictions must be string lists')
                    if kind=='commands':
                        for command in values:
                            parts=command.rsplit(':',1)
                            if len(parts)!=2 or len(parts[0].split())!=2 or not parts[1]: raise ValueError('invalid command/scope expression')
                            tool=parts[0].split()[1]
                            path=(repo_root/tool).resolve()
                            if not tool.startswith('tools/') or not path.is_relative_to((repo_root/'tools').resolve()) or not path.is_file(): issues.append(f'unresolved command: {tool}')
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        issues.append(str(exc))
    return {'workflow':folder.name,'valid':not issues,'issues':issues}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[2]/'workflows')
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args(); root=args.root.resolve()
    if not root.is_dir(): parser.exit(2,f'ERROR: missing workflows root {root}\n')
    if (root/'catalog.yaml').is_file():
        try:
            from build_workflow_index import validate_and_build
            index=validate_and_build(root.parent)
            generated=root/'index.json'
            expected=json.dumps(index,indent=2,sort_keys=False)+'\n'
            if not generated.is_file() or generated.read_text()!=expected:
                parser.exit(1,'FAIL workflow index: workflows/index.json is missing or stale\n')
        except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError,yaml.YAMLError) as exc:
            parser.exit(1,f'FAIL workflow catalog: {exc}\n')
    results=[validate_workflow_dir(p,root.parent) for p in sorted(root.iterdir()) if p.is_dir() and not p.name.startswith('.')]
    report={'checked_workflow_count':len(results),'invalid_workflow_count':sum(not r['valid'] for r in results),'results':results}
    print(json.dumps(report,indent=2) if args.json else '\n'.join(f"{'PASS' if r['valid'] else 'FAIL'} {r['workflow']}: {'; '.join(r['issues'])}" for r in results))
    return int(bool(report['invalid_workflow_count'] or not results))

if __name__=='__main__': raise SystemExit(main())
