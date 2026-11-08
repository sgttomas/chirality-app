"""Offline S1 value checker. Never observes or executes a supplier distribution.
Trusted attestation selection is an integration input, not proof created here.
"""
import ast
import re
import hashlib
import importlib.util
import json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').exists())
BASIS = json.loads((HERE / 'basis.json').read_text())

def module(name, suffix):
    item = next(x for x in BASIS['reads'] if x['path'].endswith(suffix))
    path = ROOT / item['path']
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError('changed source dependency: ' + suffix)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod

inventory = module('inventory_model', 'distribution_identity/inventory_model.py')
legacy_pkg = module('legacy_pkg', 'prototype/check_pkg.py')
# Load the existing transition table as data; do not import its executable model.
transition_source = next(x for x in BASIS['reads'] if x['path'].endswith('/boundary_model.py'))
transition_bytes = (ROOT / transition_source['path']).read_bytes()
if hashlib.sha256(transition_bytes).hexdigest() != transition_source['sha256']:
    raise ValueError('changed lifecycle transition basis')
TRANSITIONS = next(ast.literal_eval(n.value) for n in ast.parse(transition_bytes).body
                   if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TRANSITIONS' for t in n.targets))

def shape(value, name):
    schema = json.loads((HERE / (name + '.schema.json')).read_text())
    Draft202012Validator(schema).validate(value)

def resolve(ref, directory, name=None):
    """Read exact local artifact bytes, before JSON parsing; no network lookup."""
    if ref is None:
        raise ValueError('missing artifact')
    p = Path(ref['path'])
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('artifact path must be contained and relative')
    base = Path(directory).resolve()
    path = (base / p).resolve()
    if not path.is_relative_to(base):
        raise ValueError('artifact escapes bundle')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('artifact byte digest mismatch')
    if name is None:
        return raw
    value = json.loads(raw)
    shape(value, name)
    return value

def reference(expected_ref, attestation_ref, directory, selected_attestation_sha256):
    e = resolve(expected_ref, directory, 'expected-reference.s1')
    a = resolve(attestation_ref, directory, 'adoption-attestation.s1')
    if attestation_ref['sha256'] != selected_attestation_sha256:
        raise ValueError('attestation not independently selected by consuming build')
    if a['expected_reference'] != expected_ref or a['author'] != e['author']:
        raise ValueError('attestation subject mismatch')
    if a['author'].strip().casefold() == a['independent_reviewer'].strip().casefold():
        raise ValueError('review is not independent')
    if e['pin'] != e['generated']['pin']:
        raise ValueError('reference pin/generated mismatch')
    problems = inventory.validate(e['inventory'])
    if problems:
        raise ValueError(str(problems))
    refs = [e['label_evidence'], e['generation_correspondence'], a['review_evidence'],
            a['adoption']['through_help_human'], a['adoption']['evidence'],
            e['generated']['provenance'], e['generated']['version_advance']]
    refs += [e['archive'][k] for k in ('acquisition_authorization','custody','extraction_procedure')]
    for ref in refs:
        resolve(ref, directory)
    return e

def observed(value, directory, selected_attestation_sha256):
    shape(value, 'observed-verification.s1')
    contradictions = []
    gaps = []
    for name, check in value['checks'].items():
        if check['outcome'] == 'mismatch':
            contradictions.append(name)
        elif check['outcome'] != 'pass':
            gaps.append(name)
        if check['evidence'] is None:
            gaps.append(name + ' evidence')
        else:
            try: resolve(check['evidence'], directory)
            except (ValueError, OSError): gaps.append(name + ' unreadable evidence')
    e = None
    try:
        e = reference(value['expected_reference'], value['adoption_attestation'], directory, selected_attestation_sha256)
    except (ValueError, OSError):
        gaps.append('trusted reference')
    if value['inventory'] is None:
        gaps.append('inventory')
    elif inventory.validate(value['inventory']):
        contradictions.append('invalid inventory')
    if e:
        if e['pin'] != value['pin'] or e['platform'] != value['platform']:
            contradictions.append('pin/platform')
        if value['inventory'] is not None and not inventory.compare(e['inventory'],value['inventory'])['equal']:
            contradictions.append('tree')
        if value['launcher'] != e['launcher']:
            contradictions.append('launcher')
        if value['generated'] is not None and value['generated'] != e['generated']:
            contradictions.append('generated')
    if value['generated'] is None: gaps.append('generated')
    elif value['generated']['pin'] != value['pin']: contradictions.append('generated pin')
    raw = value['raw_version_label']
    parsed = re.fullmatch(r'codex-cli ([0-9]+\.[0-9]+\.[0-9]+)\n?', raw) if raw is not None else None
    if raw is None and value['observed_label'] is not None:
        contradictions.append('label without raw observation')
    elif raw is not None and (parsed is None or parsed.group(1) != value['observed_label']):
        contradictions.append('raw/parsed label')
    if value['observed_label'] is None: gaps.append('label')
    elif value['observed_label'] != value['pin']: contradictions.append('label')
    c = value['configuration']
    if ':' in c['path_prefix'] or '\0' in c['path_prefix']:
        contradictions.append('PATH prefix')
    root = c['resolved_root'].rstrip('/')
    if c['resolved_executable'] != root + '/bin/codex' or c['path_prefix'] != root + '/codex-path':
        contradictions.append('launcher root')
    if c['probe_home'] == c['account_home']:
        contradictions.append('home isolation')
    if not set(value['launcher']['removed_wrapper_variables']) <= set(c['removed_environment_names']):
        contradictions.append('wrapper environment')
    actual = 'mismatch' if contradictions else 'unverifiable' if gaps else 'verified'
    if value['outcome'] != actual:
        raise ValueError('claimed outcome differs: derived ' + actual)
    return actual

def lifecycle(value, directory, selected_attestation_sha256):
    shape(value, 'lifecycle-event.s1')
    e = value['legacy_event']
    if TRANSITIONS.get(e['transitionId']) != (e['fromState'],e['event'],e['toState']):
        raise ValueError('legacy transition table violation')
    if value['verification_artifact'] is None:
        if value['verification_generation'] is not None or e['transitionId'] not in {'LT-01','LT-02','LT-03','LT-15','LT-16','LT-20','LT-21','LT-22'} or 'verificationResult' in e or 'versionIdentity' in e or e.get('supplierStanding') == 'verified-pin':
            raise ValueError('verification artifact required for this event')
        return 'verification-not-yet-available'
    o = resolve(value['verification_artifact'], directory, 'observed-verification.s1')
    outcome = observed(o, directory, selected_attestation_sha256)
    if value['verification_generation'] != o['generation'] or (e['generation'] is not None and e['generation'] != o['generation']):
        raise ValueError('generation mismatch')
    if 'verificationResult' in e and e['verificationResult']['result'] != outcome:
        raise ValueError('lifecycle verification disagreement')
    if e['transitionId'] == 'LT-04' and (outcome != 'verified' or o['phase'] != 'pre-spawn'):
        raise ValueError('LT-04 requires pre-spawn verified')
    if e['transitionId'] == 'LT-24' and (outcome != 'unverifiable' or not o['observed_label'] or not o['raw_version_label'] or o['phase'] != 'pre-spawn'):
        raise ValueError('LT-24 cannot waive contradiction')
    if e.get('supplierStanding') == 'verified-pin' and outcome != 'verified':
        raise ValueError('standing mismatch')
    if 'versionIdentity' in e:
        v = e['versionIdentity']
        if v['declaredPin'] != o['pin'] or v['observedVersionLabel'] != o['observed_label']:
            raise ValueError('version identity disagreement')
    return outcome

def package(value, directory, selected_attestation_sha256):
    shape(value, 'pkg-identity.s1')
    old = value['legacy_package']
    errors = legacy_pkg.identity_violations(old)
    if errors: raise ValueError('legacy obligations: ' + ','.join(errors))
    gaps = []
    mismatches = []
    expected = None
    try:
        expected = reference(value['expected_reference'],value['adoption_attestation'],directory,selected_attestation_sha256)
    except (ValueError,OSError): gaps.append('reference')
    trees = {}
    for name,key in [('published','published_inventory'),('packaged','packaged_inventory')]:
        try:
            tree = resolve(value[key],directory,'inventory-artifact.s1')['inventory']
            if inventory.validate(tree):
                mismatches.append('invalid ' + name + ' inventory')
                continue
            trees[name] = tree
            legacy = old['codex'][name]
            if legacy['manifest_sha256'] != tree['manifest_sha256'] or legacy['files'] != sum(x['kind']=='file' for x in tree['entries']):
                mismatches.append('legacy tree summary')
        except (ValueError,OSError): gaps.append(name)
    if expected:
        if old['codex']['pin'] != expected['pin']: mismatches.append('pin')
        if 'published' in trees and not inventory.compare(expected['inventory'],trees['published'])['equal']:
            mismatches.append('reference/published tree')
    if len(trees)==2 and not inventory.compare(trees['published'],trees['packaged'])['equal']:
        mismatches.append('published/packaged tree')
    paths = value['mach_o_paths']
    executables = old['codex']['executables']
    if len(paths) != len(set(paths)) or set(paths) != {x['path'] for x in executables}:
        raise ValueError('Mach-O coverage mismatch')
    for name,key in [('published','sha256_published'),('packaged','sha256_packaged')]:
        if name not in trees: continue
        files={x['path']:x for x in trees[name]['entries'] if x['kind']=='file'}
        for exe in executables:
            if exe['path'] not in files or files[exe['path']]['sha256'] != exe[key]:
                mismatches.append('Mach-O digest')
    if value['verification_artifact'] is not None:
        o = resolve(value['verification_artifact'],directory,'observed-verification.s1')
        status = observed(o,directory,selected_attestation_sha256)
        subject = {'app_revision':old['app']['revision'],'build_identity':old['app']['build_identity'],
                   'package_record_id':old['record_id'],'installer_sha256_before_notarisation':old['app']['installer']['sha256_before_notarisation']}
        if o['candidate_subject'] != subject:
            raise ValueError('runtime observation is for another App/package candidate')
        if o['expected_reference'] != value['expected_reference'] or o['adoption_attestation'] != value['adoption_attestation']:
            raise ValueError('runtime reference subject mismatch')
        if 'packaged' in trees and o['inventory'] is not None and not inventory.compare(o['inventory'],trees['packaged'])['equal']:
            mismatches.append('runtime/package tree')
        if status == 'mismatch': mismatches.append('runtime observation')
        if status == 'unverifiable': gaps.append('runtime observation')
    actual = 'mismatch' if mismatches else 'unverifiable' if gaps else 'reference-equal'
    if value['distribution_status'] != actual:
        raise ValueError('package distribution status differs: derived ' + actual)
    return actual
