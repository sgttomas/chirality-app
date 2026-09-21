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


def load_legacy_methods(root: Path):
    path = contained(root, 'workflows/legacy-methods.json')
    document = json.loads(path.read_text())
    aliases = document.get('convertedWorkflowAliases') if isinstance(document, dict) else None
    if not isinstance(document, dict) or document.get('schema') != 'chirality-legacy-methods/v1' or not isinstance(aliases, dict):
        raise ValueError('unsupported legacy method mapping')
    normalized = {}
    for alias, target in aliases.items():
        if not isinstance(alias, str) or not NAME.fullmatch(alias):
            raise ValueError('invalid legacy method alias')
        normalized[alias] = parse_method_reference(target)
        if set(normalized[alias]) != {'kind', 'name'}:
            raise ValueError('legacy method targets must be unqualified')
    if document.get('unknownLegacyBehavior') != 'error':
        raise ValueError('unsupported unknown legacy method behavior')
    return path, normalized


def load_catalog_identity(root: Path):
    path = contained(root, 'workflows/catalog.yaml')
    catalog = json.loads(path.read_text())
    library = catalog.get('library') if isinstance(catalog, dict) else None
    if (catalog.get('schema') != 'chirality-workflow-catalog/v1' or not isinstance(library, dict)
            or set(library) != {'source', 'sourceRootId'} or library.get('source') not in SOURCES
            or not isinstance(library.get('sourceRootId'), str) or not SOURCE_ROOT_ID.fullmatch(library['sourceRootId'])):
        raise ValueError('unsupported workflow catalog')
    return path, library


def qualify_local_method(root: Path, reference: dict) -> dict:
    """Bind an unqualified reference to this resolver's single declared Root."""
    _, library = load_catalog_identity(root)
    if reference['kind'] == 'skill' and reference['name'] == 'chirality-change':
        expected = {'sourceRootId': f"{library['sourceRootId']}-project", 'source': 'project', **{k: reference[k] for k in ('kind', 'name')}}
    else:
        expected = {'sourceRootId': library['sourceRootId'], 'source': library['source'], **{k: reference[k] for k in ('kind', 'name')}}
    if 'sourceRootId' in reference and reference != expected:
        raise ValueError('qualified method identity is outside the declared Root catalog')
    return expected


def normalize_method_selection(root: Path, workflow=None, task_skill=None, methods=()):
    """Normalize compatibility fields without rewriting their recorded values.

    Unqualified Workflow and TaskSkill values use the explicit conversion ledger.
    A fully source-qualified Workflow is an intentional historical workflow
    selection and is therefore never redirected through that ledger.
    """
    requested_methods = [parse_method_reference(value) for value in methods]
    resolved_ordered = [qualify_local_method(root, value) for value in requested_methods]
    ordered = [dict(value) for value in requested_methods]
    original = {'Workflow': workflow, 'TaskSkill': task_skill, 'methods': [dict(value) for value in requested_methods]}
    decisions = []
    mapping_path = None
    aliases = None

    def converted(alias):
        nonlocal mapping_path, aliases
        if aliases is None:
            mapping_path, aliases = load_legacy_methods(root)
        target = aliases.get(alias)
        if target is None:
            raise ValueError(f'unknown legacy method alias: {alias}')
        return dict(target)

    compatibility = []
    compatibility_normalized = []
    if workflow is not None:
        if not isinstance(workflow, str):
            raise ValueError('Workflow must be a string')
        if ':' in workflow:
            reference = parse_method_reference(workflow)
            if reference['kind'] != 'workflow':
                raise ValueError('Workflow qualified identity must select a workflow')
            decision = 'explicit-qualified-historical-workflow'
        else:
            if not NAME.fullmatch(workflow):
                raise ValueError('invalid Workflow name')
            if aliases is None:
                mapping_path, aliases = load_legacy_methods(root)
            if workflow in aliases:
                reference = dict(aliases[workflow])
                decision = 'converted-alias'
            else:
                reference = {'kind': 'workflow', 'name': workflow}
                decision = 'unmapped-canonical-workflow'
        reference = qualify_local_method(root, reference)
        compatibility.append(reference)
        compatibility_normalized.append(parse_method_reference(workflow) if ':' in workflow else {'kind': reference['kind'], 'name': reference['name']})
        decisions.append({'field': 'Workflow', 'original': workflow, 'mapping': decision, 'resolved': dict(reference)})
    if task_skill is not None:
        if not isinstance(task_skill, str):
            raise ValueError('TaskSkill must be a string')
        alias = task_skill.replace('_', '-')
        if not NAME.fullmatch(alias):
            raise ValueError('invalid TaskSkill alias')
        reference = converted(alias)
        reference = qualify_local_method(root, reference)
        compatibility.append(reference)
        compatibility_normalized.append({'kind': reference['kind'], 'name': reference['name']})
        decisions.append({'field': 'TaskSkill', 'original': task_skill, 'normalizedAlias': alias,
                          'mapping': 'converted-alias', 'resolved': dict(reference)})
    if compatibility and any(value != compatibility[0] for value in compatibility[1:]):
        raise ValueError('conflicting Workflow/TaskSkill selections after legacy normalization')
    selected = compatibility[0] if compatibility else None
    if selected and selected not in resolved_ordered:
        ordered.append(compatibility_normalized[0])
        resolved_ordered.append(selected)
    return {
        'methods': ordered,
        'resolved_methods': resolved_ordered,
        'compatibility_inputs': [key for key in ('Workflow', 'TaskSkill') if original[key] is not None],
        'original_inputs': original,
        'mapping_decisions': decisions,
        'mapping_path': mapping_path,
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


def resolve(root: Path, role: str, workflow=None, task_skill=None, resources=(), stage=None, policy=None, legacy_agent=None, methods=()):
    root = root.resolve()
    registry_path = contained(root, 'agents/registry.json')
    registry = json.loads(registry_path.read_text())
    if not isinstance(registry, dict) or registry.get('schema_version') != 1 or not isinstance(registry.get('roles'), dict) or role not in registry['roles']:
        raise ValueError('unsupported registry or unknown role')
    alias = None
    if legacy_agent:
        aliases = json.loads(contained(root, 'workflows/legacy-agents.json').read_text())
        alias = aliases['aliases'].get(legacy_agent)
        if alias is None or alias['role'] != role:
            raise ValueError('unknown legacy agent or incompatible target role')
        if alias.get('workflow'):
            if workflow is not None:
                raise ValueError('conflicting Workflow/legacy-agent selections')
            _, library = load_catalog_identity(root)
            workflow = f"{library['sourceRootId']}:{library['source']}:workflow:{alias['workflow']}"
        if stage and alias.get('stage') and stage != alias['stage']:
            raise ValueError('conflicting legacy stage')
        stage = stage or alias.get('stage')
    selection = normalize_method_selection(root, workflow, task_skill, methods)
    selected_methods = selection['resolved_methods']
    role_config = registry['roles'][role]
    if not isinstance(role_config, dict) or not isinstance(role_config.get('tools'), list) or not isinstance(role_config.get('instruction'), str):
        raise ValueError('malformed role configuration')
    context = [fingerprint(contained(root, role_config['instruction']), root, True)]
    basis = [fingerprint(registry_path, root)]
    if selected_methods:
        catalog_path, _ = load_catalog_identity(root)
        basis.append(fingerprint(catalog_path, root))
    if selection['mapping_path']:
        basis.append(fingerprint(selection['mapping_path'], root))
    if legacy_agent:
        basis.append(fingerprint(contained(root, 'workflows/legacy-agents.json'), root))
    execution = {}
    method_executions = []
    stage_config = {}
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
        if compatible is not None and role not in compatible:
            raise ValueError('method incompatible with role')
        method_executions.append({'method': dict(reference), 'execution': method_execution})
    if stage:
        raise ValueError('select bounded workflow resources explicitly; stage overrides are unsupported')
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
    tool_policies.extend([stage_config.get('tools', {}), policy.get('brief', {})])
    if not isinstance(policy, dict) or any(not isinstance(p, dict) for p in tool_policies):
        raise ValueError('policy layers must be mappings')
    commands, resolved_commands = command_constraints(tool_policies, root, policy.get('bindings', {}))
    effective = {'capabilities': intersect(*(p.get('capabilities') for p in tool_policies)), 'commands': commands}
    legacy_workflow = selected_methods[0]['name'] if len(selected_methods) == 1 and selected_methods[0]['kind'] == 'workflow' else None
    return {'schema_version':1, 'role':role, 'workflow':legacy_workflow, 'methods':selected_methods,
            'method_selection':{'compatibility_inputs':selection['compatibility_inputs'],
                                'original_inputs':selection['original_inputs'],
                                'normalized_methods':selection['methods'],
                                'mapping_decisions':selection['mapping_decisions']},
            'stage':stage, 'legacy_alias':alias, 'role_configuration':role_config, 'execution':execution,
            'method_executions':method_executions, 'effective_tools':effective, 'resolved_commands':resolved_commands,
            'context':context, 'configuration_basis':basis, 'instruction_root':str(root), 'tool_root':str(root / 'tools'),
            'context_evidence':'mechanically-recorded resolver inputs; host context delivery unverified',
            'enforcement':'instruction-asserted; host must enforce effective restrictions'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument('--role',required=True)
    p.add_argument('--workflow'); p.add_argument('--task-skill'); p.add_argument('--legacy-agent')
    p.add_argument('--method', action='append', default=[], help='Ordered method reference as JSON or a source-qualified identity')
    p.add_argument('--brief',type=Path,help='Structured inline brief JSON; explicit paths are rooted at --repo-root')
    p.add_argument('--repo-root',type=Path,help='Active writable checkout root, required with --brief')
    p.add_argument('--resource',action='append',default=[]); p.add_argument('--policy',type=Path)
    args=p.parse_args()
    try:
        policy=json.loads(args.policy.read_text()) if args.policy else {}
        brief=None
        if args.brief:
            from normalize_brief import load_brief
            if not args.repo_root:raise ValueError('--brief requires --repo-root')
            brief=load_brief(json.loads(args.brief.read_text()),args.repo_root,args.root)
            for cli, field in [('workflow','Workflow'),('task_skill','TaskSkill')]:
                supplied=getattr(args,cli)
                if supplied and brief.get(field) and supplied!=brief[field]:raise ValueError(f'CLI/brief disagree on {field}')
                setattr(args,cli,supplied or brief.get(field))
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
        result=resolve(args.root,args.role,args.workflow,args.task_skill,args.resource,None,policy,args.legacy_agent,methods)
        if args.policy:
            result['configuration_basis'].append(fingerprint(args.policy.resolve(),args.policy.resolve().parent))
        if brief:
            if result['role_configuration'].get('write_scope') == 'none':
                brief['AllowedWriteTargets'] = []
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
