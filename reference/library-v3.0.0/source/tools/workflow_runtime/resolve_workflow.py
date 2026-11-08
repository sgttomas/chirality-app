#!/usr/bin/env python3
"""Resolve explicitly selected context. This utility reports policy; it is not a sandbox."""
from __future__ import annotations
import argparse
import hashlib
import fnmatch
import posixpath
import json
import re
from pathlib import Path

NAME = re.compile(r'^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$')
SOURCE_ROOT_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$')
SOURCES = {'project', 'user', 'bundled'}
KINDS = {'skill', 'workflow'}
# Roles advertised by the index when a method has no execution companion.
# Legacy custom-role inheritance in the resolver remains unchanged;
# INTERLOCUTOR alone requires explicit compatible_roles.
LEGACY_DEFAULT_ROLES = ('HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS', 'TASK')


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'missing or escaping resource: {relative}')
    return path


def fingerprint(path: Path, root: Path, content: bool = False) -> dict:
    raw = path.read_bytes()
    item = {'path': str(path.relative_to(root)), 'source_root': str(root), 'sha256': hashlib.sha256(raw).hexdigest()}
    if content:
        item['content'] = raw.decode('utf-8')
    return item


def intersect(*policies):
    """None inherits; [] denies. Exact command expressions remain conservative."""
    if any(not isinstance(p, list) or any(not isinstance(x, str) for x in p) for p in policies if p is not None):
        raise ValueError('tool restrictions must be lists of strings')
    present = [set(p) for p in policies if p is not None]
    return sorted(set.intersection(*present)) if present else None


def resolve_tool(tool_root: Path, tool: str) -> str:
    if not tool.startswith('tools/'):
        raise ValueError('repository commands must name tools/ paths')
    resolved = contained(tool_root, tool)
    allowed = (tool_root / 'tools').resolve()
    if not allowed.is_relative_to(tool_root.resolve()) or not resolved.is_relative_to(allowed):
        raise ValueError('command path escapes declared tools directory')
    return str(resolved)


def command_constraints(layers, root, bindings):
    groups = []
    resolved = []
    for layer in layers:
        commands = layer.get('commands')
        if commands is None:
            continue
        if not isinstance(commands, list) or any(not isinstance(x, str) for x in commands):
            raise ValueError('command restrictions must be string lists')
        group = []
        for expression in commands:
            try:
                bound = expression.format_map(bindings)
            except (KeyError, ValueError) as exc:
                raise ValueError(f'unbound command expression: {expression}') from exc
            parts = bound.rsplit(':', 1)
            if len(parts) != 2 or not parts[1] or len(parts[0].split()) != 2:
                raise ValueError(f'invalid command expression: {expression}')
            interpreter, tool = parts[0].split()
            absolute = resolve_tool(root, tool)
            group.append(bound)
            resolved.append({'expression': bound, 'interpreter': interpreter, 'tool': absolute, 'scope': parts[1]})
        groups.append(group)
    return {'all_of': groups}, resolved


def command_allowed(constraints, interpreter, tool, targets):
    """Evaluate explicit command/target claims; a host must extract actual effects.

    Each present policy is conjunctive. Alternatives within one policy are OR.
    Empty policy denies; no policies inherit. Every target must satisfy each layer.
    """
    targets = [posixpath.normpath(target) for target in targets]
    for alternatives in constraints['all_of']:
        matches = []
        for expression in alternatives:
            prefix, scope = expression.rsplit(':', 1)
            if prefix.split() == [interpreter, tool]:
                matches.append(scope)
        if not matches or not targets or not all(any(fnmatch.fnmatchcase(target, scope) for scope in matches) for target in targets):
            return False
    return True


def parse_method_reference(value):
    if isinstance(value, str):
        parts = value.split(':')
        if len(parts) != 4:
            raise ValueError('invalid qualified method identity')
        source_root_id, source, kind, name = parts
        reference = {'sourceRootId': source_root_id, 'source': source, 'kind': kind, 'name': name}
    elif isinstance(value, dict):
        reference = dict(value)
    else:
        raise ValueError('method references must be mappings or qualified identity strings')
    required = {'kind', 'name'}
    qualified = {'sourceRootId', 'source'}
    keys = set(reference)
    if not required <= keys or not (keys <= required or keys == required | qualified):
        raise ValueError('method reference must be unqualified or fully source-qualified')
    if reference['kind'] not in KINDS or not isinstance(reference['name'], str) or not NAME.fullmatch(reference['name']):
        raise ValueError('invalid method reference')
    if qualified <= keys:
        if reference['source'] not in SOURCES or not isinstance(reference['sourceRootId'], str) or not SOURCE_ROOT_ID.fullmatch(reference['sourceRootId']):
            raise ValueError('invalid qualified method identity')
    return reference


def load_catalog_identity(root: Path):
    path = contained(root, 'workflows/catalog.yaml')
    # catalog.yaml is authored in JSON, the YAML 1.2 subset that
    # tools/validation/build_workflow_index.py also reads with json.loads.
    catalog = json.loads(path.read_text(encoding='utf-8'))
    library = catalog.get('library') if isinstance(catalog, dict) else None
    if (catalog.get('schema') != 'chirality-workflow-catalog/v1' or not isinstance(library, dict)
            or set(library) != {'source', 'sourceRootId'} or library.get('source') not in SOURCES
            or not isinstance(library.get('sourceRootId'), str) or not SOURCE_ROOT_ID.fullmatch(library['sourceRootId'])):
        raise ValueError('unsupported workflow catalog')
    return path, library


def qualify_local_method(root: Path, reference: dict) -> dict:
    """Bind an unqualified reference to this resolver's single declared Root."""
    _, library = load_catalog_identity(root)
    expected = {'sourceRootId': library['sourceRootId'], 'source': library['source'], **{k: reference[k] for k in ('kind', 'name')}}
    if 'sourceRootId' in reference and reference != expected:
        raise ValueError('qualified method identity is outside the declared Root catalog')
    return expected


def normalize_method_selection(root: Path, workflow=None, methods=()):
    """Normalize the Workflow compatibility field alongside ordered methods.

    An unqualified Workflow names a workflow package in the declared Root; a
    fully source-qualified Workflow must belong to that Root. Recorded values
    are kept as supplied.
    """
    requested_methods = [parse_method_reference(value) for value in methods]
    resolved_ordered = [qualify_local_method(root, value) for value in requested_methods]
    ordered = [dict(value) for value in requested_methods]
    original = {'Workflow': workflow, 'methods': [dict(value) for value in requested_methods]}
    decisions = []
    if workflow is not None:
        if not isinstance(workflow, str):
            raise ValueError('Workflow must be a string')
        if ':' in workflow:
            reference = parse_method_reference(workflow)
            if reference['kind'] != 'workflow':
                raise ValueError('Workflow qualified identity must select a workflow')
            decision = 'qualified-workflow'
        else:
            if not NAME.fullmatch(workflow):
                raise ValueError('invalid Workflow name')
            reference = {'kind': 'workflow', 'name': workflow}
            decision = 'unqualified-workflow'
        normalized = dict(reference)
        reference = qualify_local_method(root, reference)
        decisions.append({'field': 'Workflow', 'original': workflow, 'mapping': decision, 'resolved': dict(reference)})
        if reference not in resolved_ordered:
            ordered.append(normalized)
            resolved_ordered.append(reference)
    return {
        'methods': ordered,
        'resolved_methods': resolved_ordered,
        'compatibility_inputs': ['Workflow'] if workflow is not None else [],
        'original_inputs': original,
        'mapping_decisions': decisions,
    }


def method_package(root: Path, reference: dict) -> tuple[Path, str]:
    if reference['kind'] == 'workflow':
        package = (root / 'workflows' / reference['name']).resolve()
        directory = (root / 'workflows').resolve()
        entrypoint = 'WORKFLOW.md'
    else:
        package = (root / '.agents' / 'skills' / reference['name']).resolve()
        directory = (root / '.agents' / 'skills').resolve()
        entrypoint = 'SKILL.md'
    if not package.is_relative_to(directory) or not package.is_relative_to(root):
        raise ValueError(f"{reference['kind']} package escapes declared root")
    return package, entrypoint


def resolve(root: Path, role: str, workflow=None, resources=(), policy=None, methods=()):
    root = root.resolve()
    registry_path = contained(root, 'agents/registry.json')
    registry = json.loads(registry_path.read_text())
    if not isinstance(registry, dict) or registry.get('schema_version') != 1 or not isinstance(registry.get('roles'), dict) or role not in registry['roles']:
        raise ValueError('unsupported registry or unknown role')
    selection = normalize_method_selection(root, workflow, methods)
    selected_methods = selection['resolved_methods']
    role_config = registry['roles'][role]
    if not isinstance(role_config, dict) or not isinstance(role_config.get('tools'), list) or not isinstance(role_config.get('instruction'), str):
        raise ValueError('malformed role configuration')
    context = [fingerprint(contained(root, role_config['instruction']), root, True)]
    basis = [fingerprint(registry_path, root)]
    if selected_methods:
        catalog_path, _ = load_catalog_identity(root)
        basis.append(fingerprint(catalog_path, root))
    execution = {}
    method_executions = []
    packages = []
    for reference in selected_methods:
        package, entrypoint = method_package(root, reference)
        packages.append(package)
        context.append(fingerprint(contained(package, entrypoint), root, True))
        companion = package / 'execution.json'
        method_execution = {}
        if companion.exists():
            method_execution = json.loads(contained(package, 'execution.json').read_text())
            if method_execution.get('schema_version') != 1:
                raise ValueError('unsupported execution schema')
            basis.append(fingerprint(companion.resolve(), root))
        compatible = method_execution.get('compatible_roles')
        if role == 'INTERLOCUTOR' and compatible is None:
            raise ValueError('method incompatible with role')
        if compatible is not None:
            if not isinstance(compatible, list) or any(not isinstance(x, str) for x in compatible):
                raise ValueError('malformed compatible_roles')
            if role not in compatible:
                raise ValueError('method incompatible with role')
        method_executions.append({'method': dict(reference), 'execution': method_execution})
    if resources:
        if len(packages) != 1:
            raise ValueError('resources require exactly one selected method')
        for resource in dict.fromkeys(resources):
            context.append(fingerprint(contained(packages[0], resource), root, True))
    execution = method_executions[0]['execution'] if len(method_executions) == 1 else {}
    policy = policy or {}
    if not isinstance(policy,dict):raise ValueError('policy must be a mapping')
    tool_policies = [policy.get('host', {}), {'capabilities': role_config['tools']}]
    tool_policies.extend(item['execution'].get('tools', {}) for item in method_executions)
    tool_policies.append(policy.get('brief', {}))
    if any(not isinstance(p, dict) for p in tool_policies):
        raise ValueError('policy layers must be mappings')
    commands, resolved_commands = command_constraints(tool_policies, root, policy.get('bindings', {}))
    effective = {'capabilities': intersect(*(p.get('capabilities') for p in tool_policies)), 'commands': commands}
    legacy_workflow = selected_methods[0]['name'] if len(selected_methods) == 1 and selected_methods[0]['kind'] == 'workflow' else None
    return {'schema_version':1, 'role':role, 'workflow':legacy_workflow, 'methods':selected_methods,
            'method_selection':{'compatibility_inputs':selection['compatibility_inputs'],
                                'original_inputs':selection['original_inputs'],
                                'normalized_methods':selection['methods'],
                                'mapping_decisions':selection['mapping_decisions']},
            'role_configuration':role_config, 'execution':execution,
            'method_executions':method_executions, 'effective_tools':effective, 'resolved_commands':resolved_commands,
            'context':context, 'configuration_basis':basis, 'instruction_root':str(root), 'tool_root':str(root / 'tools'),
            'context_evidence':'mechanically-recorded resolver inputs; host context delivery unverified',
            'enforcement':'instruction-asserted; host must enforce effective restrictions'}


def bind_write_authority(result, brief):
    """Intersect normalized assignment targets with effective host/tool policy.

    Role capability lists are ceilings, not a grant to edit. Missing assignment
    authorization remains empty; the host still enforces the resulting targets.
    """
    capabilities = result['effective_tools']['capabilities']
    targets = brief.get('AllowedWriteTargets', []) if brief else []
    if capabilities is None or 'write' not in capabilities:
        targets = []
    if brief is not None:
        brief['AllowedWriteTargets'] = targets
    if not targets and capabilities is not None:
        result['effective_tools']['capabilities'] = [c for c in capabilities if c != 'write']
    result['allowed_write_targets'] = targets


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument('--role',required=True)
    p.add_argument('--workflow')
    p.add_argument('--method', action='append', default=[], help='Ordered method reference as JSON or a source-qualified identity')
    p.add_argument('--brief',type=Path,help='Structured inline brief JSON; explicit paths are rooted at --repo-root')
    p.add_argument('--repo-root',type=Path,help='Active writable checkout root, required with --brief')
    p.add_argument('--resource',action='append',default=[]); p.add_argument('--policy',type=Path)
    args=p.parse_args()
    try:
        policy=json.loads(args.policy.read_text()) if args.policy else {}
        brief=None
        if args.brief:
            if __package__:
                from .normalize_brief import load_brief
            else:
                from normalize_brief import load_brief
            if not args.repo_root:raise ValueError('--brief requires --repo-root')
            brief=load_brief(json.loads(args.brief.read_text()),args.repo_root,args.root)
            if brief.get('TaskSkill'):raise ValueError('TaskSkill is retired; select the method with Workflow or methods')
            if args.workflow and brief.get('Workflow') and args.workflow!=brief['Workflow']:raise ValueError('CLI/brief disagree on Workflow')
            args.workflow=args.workflow or brief.get('Workflow')
            policy.setdefault('bindings',{}).update({'scope_path':brief['ScopePath'],'WORKING_ROOT':brief['WorkingRoot'],'INSTRUCTION_ROOT':str(args.root.resolve()),'REPO_ROOT':str(args.repo_root.resolve())})
            if 'AllowedTools' in brief:
                inherited=policy.setdefault('brief',{})
                if 'commands' in inherited and inherited['commands']!=brief['AllowedTools']:raise ValueError('brief command policy has conflicting sources')
                inherited['commands']=brief['AllowedTools']
        methods=[]
        for value in args.method:
            methods.append(json.loads(value) if value.lstrip().startswith('{') else value)
        if brief and brief.get('methods'):
            if methods:raise ValueError('methods supplied by both CLI and brief')
            if not isinstance(brief['methods'],list):raise ValueError('brief methods must be a list')
            methods=brief['methods']
        result=resolve(args.root,args.role,args.workflow,args.resource,policy,methods)
        if args.policy:
            result['configuration_basis'].append(fingerprint(args.policy.resolve(),args.policy.resolve().parent))
        bind_write_authority(result, brief)
        if brief:
            result['brief']=brief
            result['configuration_basis'].append(fingerprint(args.brief.resolve(),args.brief.resolve().parent))
            if brief.get('file_brief'):
                path=Path(brief['file_brief'])
                result['configuration_basis'].append(fingerprint(path,path.parent))
    except (ValueError, KeyError, OSError, TypeError, AttributeError) as exc:
        p.exit(2,f'ERROR: {exc}\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
