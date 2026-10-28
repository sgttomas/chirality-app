#!/usr/bin/env python3
"""Read deliverable inputs and derive local dependency views as JSON."""
from __future__ import annotations

import argparse
from collections import Counter
from fnmatch import fnmatchcase
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

import yaml

try:
    from .graph import find_sccs
except ImportError:
    from graph import find_sccs

ID = re.compile(r"DEL-\d+-\d+$")
LOCALITY_ID = re.compile(r"(DEL-\d+-\d+)(?:[_-].*)?$")
TARGET = re.compile(r"(?:DEL-\d+-\d+|(?:external|doc|package):\S.*|unknown)$")


class Invalid(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject ambiguous duplicate YAML keys rather than silently losing a need."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key, value in node.value:
        name = loader.construct_object(key, deep=deep)
        if not isinstance(name, str) or name in result:
            raise Invalid(f"duplicate or non-string YAML key at line {key.start_mark.line + 1}")
        result[name] = loader.construct_object(value, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def run(args, cwd):
    # Decode without universal-newline translation: Git paths may contain CR.
    process = subprocess.run(args, cwd=cwd, capture_output=True)
    if process.returncode:
        raise Invalid(process.stderr.decode('utf-8', errors='replace').strip() or f"command failed: {args[0]}")
    return process.stdout.decode('utf-8')


def revision(repo, ref):
    return run(['git', 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}'], repo).strip()


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise Invalid('path must be a nonempty project-relative POSIX path')
    path = PurePosixPath(value.split('::', 1)[0].split('#', 1)[0])
    if path.is_absolute() or '..' in path.parts or value.startswith('~'):
        raise Invalid(f'path escapes the project: {value}')
    return path.as_posix()


def parse(text, source, expected_id=None):
    try:
        obj = yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise Invalid(f'{source}: {exc}') from exc
    if not isinstance(obj, dict) or not isinstance(obj.get('id'), str) or not ID.fullmatch(obj['id']):
        raise Invalid(f'{source}: expected a stable DEL-nn-nn id')
    if expected_id is not None and obj['id'] != expected_id:
        raise Invalid(f'{source}: id {obj["id"]} disagrees with deliverable identity {expected_id}')
    if not isinstance(obj.get('needs'), list):
        raise Invalid(f'{source}: needs must be a list')
    if 'name' in obj and not isinstance(obj['name'], str):
        raise Invalid(f'{source}: name must be text')
    for field in ('code_paths', 'checks'):
        values = obj.get(field, [])
        if not isinstance(values, list):
            raise Invalid(f'{source}: {field} must be a list')
        for value in values:
            safe_path(value)
    for index, need in enumerate(obj['needs']):
        location = f'{source}#needs[{index}]'
        if not isinstance(need, dict) or not isinstance(need.get('from'), str) or not TARGET.fullmatch(need['from']):
            raise Invalid(f'{location}: malformed supplier identity')
        if not isinstance(need.get('condition'), str) or not need['condition'].strip():
            raise Invalid(f'{location}: condition must be nonempty text')
        if 'gating' in need and not isinstance(need['gating'], bool):
            raise Invalid(f'{location}: gating must be a boolean')
        if need.get('direction', 'upstream') not in ('upstream', 'downstream'):
            raise Invalid(f'{location}: direction must be upstream or downstream')
        if need.get('direction') == 'downstream' and ID.fullmatch(need['from']):
            raise Invalid(f'{location}: native consumers declare their own needs; downstream is for nonlocal obligations')
        if 'when' in need and not isinstance(need['when'], str):
            raise Invalid(f'{location}: when must be text')
        if need['from'].startswith('doc:'):
            safe_path(need['from'][4:])
        if 'evidence' in need:
            safe_path(need['evidence'])
    return obj


def load(repo, project, ref=None):
    """Read working files or Git blobs, including pre-flattening folder layouts."""
    relative = project.relative_to(repo).as_posix()
    documents, errors = {}, []
    if ref:
        entries = run(['git', 'ls-tree', '-r', '-z', ref, '--', relative], repo).split('\0')
        sources = []
        for entry in filter(None, entries):
            info, path = entry.split('\t', 1)
            if path.endswith('/deliverable.yaml'):
                if not info.startswith('100'):
                    errors.append(f'{path}: metadata must be a regular file')
                else:
                    sources.append((path, run(['git', 'show', f'{ref}:{path}'], repo)))
    else:
        sources = []
        for path in sorted(project.rglob('deliverable.yaml')):
            relative_path = path.relative_to(repo).as_posix()
            if not path.resolve().is_relative_to(project) or path.is_symlink():
                errors.append(f'{relative_path}: metadata must be a contained regular file')
                continue
            try:
                sources.append((relative_path, path.read_text()))
            except (OSError, UnicodeError) as exc:
                errors.append(f'{relative_path}: {exc}')
    for source, text in sources:
        try:
            locality = LOCALITY_ID.fullmatch(PurePosixPath(source).parent.name)
            obj = parse(text, source, expected_id=locality.group(1) if locality else None)
            if obj['id'] in documents:
                raise Invalid(f'{source}: duplicate identity {obj["id"]}')
            documents[obj['id']] = dict(obj, source=source)
        except (Invalid, RecursionError) as exc:
            errors.append(f'{source}: {exc}')
    return documents, errors


def path_fact(project, value):
    pattern = safe_path(value)
    found = []
    for path in project.glob(pattern):
        if not path.resolve().is_relative_to(project):
            return {'state': 'unknown', 'reason': 'reference resolves outside project', 'reference': value}
        if path.exists():
            found.append(path.relative_to(project).as_posix())
    return {'state': 'observed' if found else 'unknown', 'reference': value,
            'paths': sorted(found), 'meaning': 'path presence only; no check executed or condition verified'}


def needs(documents, project):
    rows = []
    for consumer, obj in sorted(documents.items()):
        for index, need in enumerate(obj['needs']):
            target = need['from']
            fact = {'state': 'unknown', 'reason': 'external or unresolved input'}
            if ID.fullmatch(target):
                fact = ({'state': 'observed', 'source': documents[target]['source'], 'meaning': 'supplier declaration exists'}
                        if target in documents else {'state': 'unknown', 'reason': 'supplier declaration absent'})
            elif target.startswith('doc:'):
                fact = path_fact(project, target[4:])
            row = dict(need, consumer=consumer, source=f'{obj["source"]}#needs[{index}]',
                       suitability='unknown', supplier=fact)
            if 'evidence' in need:
                row['evidence_fact'] = path_fact(project, need['evidence'])
            rows.append(row)
    return rows


def graph_of(rows, ids):
    return {identifier: {row['from'] for row in rows if row['consumer'] == identifier and row['from'] in ids and row.get('direction') != 'downstream'}
            for identifier in ids}


def semantic_edges(documents):
    # Preserve multiplicity and all condition fields; source locations are not semantics.
    return Counter(json.dumps(dict(need, consumer=identifier), sort_keys=True)
                   for identifier, obj in documents.items() for need in obj['needs'])


def changed_paths(repo, value):
    selection = {}
    if value.startswith('PR:') or value.startswith('https://github.com/'):
        pr = value[3:] if value.startswith('PR:') else value
        # GitHub's file list is truncated (gh returns at most 100 files), so
        # diff the PR's base and head locally: complete, or an explicit error.
        data = json.loads(run(['gh', 'pr', 'view', pr, '--json', 'baseRefOid,headRefOid,url'], repo))
        url = data.get('url', pr) if isinstance(data, dict) else pr
        for role in ('base', 'head'):
            oid = data.get(role + 'RefOid') if isinstance(data, dict) else None
            if not isinstance(oid, str) or not re.fullmatch(r'[0-9a-f]{40,64}', oid):
                raise Invalid(f'{url}: gh returned no {role} commit')
            try:
                selection[role] = revision(repo, oid)
            except Invalid:
                raise Invalid(f'{url}: {role} commit {oid} is not in this repository; '
                              f'fetch it (for example `git fetch origin {oid}`) and retry') from None
        selection['pr'] = url
        value = f'{selection["base"]}...{selection["head"]}'
    if value.startswith('-'):
        raise Invalid('diff must be a revision or revision range')
    # A single revision means that commit's change, never the working tree.
    if '..' not in value and not value.endswith(('^!', '^@')):
        commit = revision(repo, value)
        parents = run(['git', 'rev-list', '--parents', '-n', '1', commit], repo).split()[1:]
        if parents:
            args = ['git', 'diff', '--no-renames', '--name-only', '-z', parents[0], commit, '--']
        else:
            args = ['git', 'diff-tree', '--root', '--no-commit-id', '-r', '--no-renames', '--name-only', '-z', commit, '--']
        selection = {'commit': commit, 'parent': parents[0] if parents else None}
    else:
        args = ['git', 'diff', '--no-renames', '--name-only', '-z', value, '--']
        selection['diff'] = value
    paths = run(args, repo).split('\0')
    return sorted(filter(None, paths)), selection


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('neighborhood', 'impact'):
        sub.add_parser(command).add_argument('id')
    sub.add_parser('touches').add_argument('diff_or_pr')
    sub.add_parser('dag-diff').add_argument('tag')
    sub.add_parser('check')
    args = parser.parse_args(argv)
    try:
        repo = Path(run(['git', 'rev-parse', '--show-toplevel'], Path.cwd()).strip()).resolve()
        project = (repo / args.project).resolve()
        if not project.is_relative_to(repo) or not project.is_dir():
            raise Invalid('project must be an existing directory within this repository')
        head = revision(repo, 'HEAD')
        dirty = run(['git', 'status', '--porcelain=v1', '--untracked-files=all', '--', project.relative_to(repo).as_posix()], repo).splitlines()
        documents, errors = load(repo, project)
        rows = needs(documents, project)
        result = {'command': args.command, 'basis': {'revision': head, 'working_tree_changes': dirty,
                  'project': project.relative_to(repo).as_posix()}, 'errors': errors}
        references = {identifier: {field: [path_fact(project, value) for value in doc.get(field, [])]
                                     for field in ('code_paths', 'checks')}
                      for identifier, doc in documents.items()}
        if args.command == 'check':
            graph = graph_of(rows, documents)
            result.update(deliverables=len(documents), needs=rows, references=references,
                          cycles=find_sccs(graph, documents),
                          unknown=[row['source'] for row in rows if row['supplier']['state'] == 'unknown'])
        elif args.command in ('neighborhood', 'impact'):
            if not ID.fullmatch(args.id):
                raise Invalid('malformed deliverable identity')
            if args.id not in documents:
                result.update(state='unknown', reason='deliverable declaration absent', id=args.id)
            else:
                result['deliverable'] = documents[args.id]
                result['references'] = references[args.id]
                if args.command == 'neighborhood':
                    result.update(upstream=[row for row in rows if row['consumer'] == args.id and row.get('direction') != 'downstream'],
                                  outputs=[row for row in rows if row['consumer'] == args.id and row.get('direction') == 'downstream'],
                                  downstream=[row for row in rows if row['from'] == args.id])
                else:
                    reached, pending = set(), [args.id]
                    while pending:
                        target = pending.pop()
                        for row in rows:
                            if row.get('direction') != 'downstream' and row['from'] == target and row['consumer'] not in reached and row['consumer'] != args.id:
                                reached.add(row['consumer']); pending.append(row['consumer'])
                    result.update(affected=sorted(reached), relationships=[row for row in rows if row['consumer'] in reached])
        elif args.command == 'touches':
            paths, selection = changed_paths(repo, args.diff_or_pr)
            project_rel = project.relative_to(repo).as_posix()
            prefix = '' if project_rel == '.' else project_rel + '/'
            matched = {}
            for identifier, doc in documents.items():
                folder = str(PurePosixPath(doc['source']).parent) + '/'
                hits = [path for path in paths if path.startswith(folder) or (path.startswith(prefix) and any(
                    fnmatchcase(path[len(prefix):], pattern) for pattern in doc.get('code_paths', [])))]
                if hits:
                    matched[identifier] = hits
            result.update(selection=selection, relevant=matched,
                          unmapped_paths=[path for path in paths if not any(path in hits for hits in matched.values())],
                          unknown_deliverables=sorted(identifier for identifier, doc in documents.items() if not doc.get('code_paths')),
                          meaning='relevance only; no exclusive ownership or fulfilment claim')
        else:
            baseline = revision(repo, args.tag)
            previous, old_errors = load(repo, project, baseline)
            result['errors'].extend(old_errors)
            if not previous:
                result['baseline_state'] = 'unknown'
                result['baseline_reason'] = 'no deliverable metadata at baseline'
            before, after = semantic_edges(previous), semantic_edges(documents)
            result.update(baseline={'revision': baseline, 'reference': args.tag},
                          added=[json.loads(row) for row in sorted((after-before).elements())],
                          removed=[json.loads(row) for row in sorted((before-after).elements())],
                          added_deliverables=sorted(documents.keys()-previous.keys()),
                          removed_deliverables=sorted(previous.keys()-documents.keys()))
        if not documents:
            result.update(state='unknown', reason='no deliverable metadata found')
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if result['errors'] else 0
    except (Invalid, OSError, ValueError) as exc:
        print(json.dumps({'command': args.command, 'errors': [str(exc)]}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
