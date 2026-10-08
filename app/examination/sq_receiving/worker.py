"""Snapshot worker: new SQ selection joins, reusing unchanged source validators."""
import importlib.util
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator
from referencing import Registry

PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / 'app/examination'))
sys.path.insert(0, str(PROJECT / 'app/examination/admission'))
sys.path.insert(0, str(PROJECT / 'app/examination/support_identity'))
from canonical import CanonicalSupport
from admission_check import Support as Admission
from check import Support as Package

LIMITS = [
    'Exact selected file correspondence only; not actual review, producer use or native observation.',
    'Opaque review-set bytes are not a generic EXP evidence resolver; external references remain obligations.',
    'No actual independence, signing, authority, complete affectedness, qualification or release established.',
    'Best-effort link checks do not establish hostile concurrent-filesystem isolation or native-held custody.',
]


def check(selection_path, expected):
    canonical = CanonicalSupport()
    api = canonical.legacy
    exact, require, parse = api.exact, api.require, api.parse
    pins = parse((PROJECT / 'reader-pins.json').read_bytes())
    spec = importlib.util.spec_from_file_location('selected_sq', PROJECT / pins['sq_prototype'])
    sq = importlib.util.module_from_spec(spec); spec.loader.exec_module(sq)
    admission, package = Admission(), Package()
    schema = parse((PROJECT / pins['sq_schema']).read_bytes())
    sq_validator = Draft202012Validator(schema, registry=Registry())
    step_map = parse((PROJECT / pins['sq_step_map']).read_bytes())
    root = selection_path.parent
    require(not any(p.is_symlink() for p in (root, *root.parents)), 'selection parent link refused')
    raw_selection = api.relative_file(root, selection_path.name)
    api.checked_digest(expected)
    require(api.sha(raw_selection) == expected, 'selection digest mismatch')
    selected = parse(raw_selection)
    exact(selected, ('format', 'purpose', 'support', 'candidate', 'dossier', 'case_definition',
                     'artifacts', 'steps', 'review', 'packages', 'changes'), 'SQ selection')
    require(selected['format'] == 'sq-exp-receiving-selection.v1', 'unsupported selection format')
    purpose = selected['purpose']
    require(purpose in ('current_producer_declaration', 'historical_correspondence'), 'unsupported purpose')
    require(selected['support'] == {'declaration_sha256': canonical.declaration_sha256,
                                   'support_identity': canonical.identity}, 'mixed or caller-selected support')
    exact(selected['candidate'], ('revision', 'build_identity', 'codex_pin'), 'candidate')
    for val in selected['candidate'].values():
        require(isinstance(val, str) and bool(val.strip()), 'invalid candidate value')
    errors, missing, unsupported, external, checks = [], [], [], [], []
    paths, artifacts, records, used, identities = {}, {}, {}, set(), {}

    def report(consistent):
        return {'selection_consistent': consistent and not errors,
                'coverage': 'incomplete' if missing or errors else ('unsupported' if unsupported else 'complete'),
                'errors': errors, 'missing_selected_inputs': sorted(set(missing)),
                'unsupported_joins': sorted(set(unsupported)), 'unresolved_external_references': external,
                'existing_checks': checks, 'selection_sha256': expected,
                'fixed_support': selected['support'],
                'reported_outcomes': {slot: v['outcome'] for slot, v in records.items() if 'outcome' in v},
                'reported_currency': {'dossier': dossier.get('currency') if dossier else None,
                                      **{slot: v['currency'] for slot, v in records.items() if 'currency' in v}},
                'current_reliance': False, 'qualification_established': False,
                'actual_producer_use_verified': False, 'native_observation_verified': False,
                'publication_authority_authenticated': False, 'method_adoption_authenticated': False,
                'limits': LIMITS}

    def array(value, label):
        require(isinstance(value, list), label + ' must be an array')
        return value

    def file(ref, role):
        exact(ref, ('path', 'sha256'), 'file reference')
        api.checked_digest(ref['sha256'])
        path = ref['path']
        require(isinstance(path, str), 'invalid file path')
        require(path not in paths, 'duplicate or conflicting file path')
        paths[path] = role
        try:
            data = api.relative_file(root, path)
        except FileNotFoundError:
            missing.append(role + ': selected file missing')
            return None
        require(api.sha(data) == ref['sha256'], 'exact-byte mismatch: ' + role)
        return data

    def record(slot, kind):
        require(isinstance(slot, str) and slot in artifacts, 'unknown artifact slot')
        require(artifacts[slot]['kind'] == kind, 'artifact kind mismatch')
        used.add(slot)
        return records.get(slot)

    def schema_errors(validator, value, label):
        found = [{'scope': label, 'code': 'SCHEMA', 'path': list(e.path), 'message': e.message}
                 for e in validator.iter_errors(value)]
        errors.extend(found)
        return bool(found)

    def existing(label, found, unresolved=()):
        checks.append({'scope': label, 'errors': found, 'unresolved_other_references': list(unresolved)})
        errors.extend({'scope': label, **e} for e in found)

    dossier_bytes = file(selected['dossier'], 'dossier')
    dossier = parse(dossier_bytes) if dossier_bytes is not None else None
    definition = selected['case_definition']
    exact(definition, ('ref', 'path', 'sha256'), 'case definition')
    require(isinstance(definition['ref'], str) and definition['ref'], 'invalid case definition ref')
    file({k: definition[k] for k in ('path', 'sha256')}, 'case definition')
    for a in array(selected['artifacts'], 'artifacts'):
        exact(a, ('slot', 'kind', 'record', 'binding'), 'artifact')
        slot = a['slot']; kind = a['kind']
        require(isinstance(slot, str) and slot and slot not in artifacts, 'duplicate or invalid slot')
        require(kind in ('result', 'review', 'change', 'package'), 'unknown artifact kind')
        artifacts[slot] = a
        raw = file(a['record'], slot + '/record'); binding = file(a['binding'], slot + '/binding')
        if raw is None or binding is None:
            continue
        bound = parse(binding)
        require(not list(canonical.validator.iter_errors(bound)), 'invalid canonical binding')
        require(bound == canonical.binding(kind, raw, purpose), 'canonical binding identity mismatch')
        # Reuse exact existing single-record support correspondence; internal
        # unpublished sidecar is never returned as an authority-bearing artifact.
        old_binding = canonical.support.binding(kind, raw)
        value = canonical.support.bound_record(kind, raw, json.dumps(old_binding).encode())
        records[slot] = value
        identities.setdefault(value['record_id'], []).append(slot)
        if kind == 'package':
            existing(slot, package.validate(kind, value))
        elif kind != 'change':
            existing(slot, admission.validate(kind, value))
        else:
            schema_errors(admission.validators['change'], value, slot)
    if dossier is None:
        missing.append('dossier unavailable: joins not evaluated')
        return report(False)
    if schema_errors(sq_validator, dossier, 'dossier') or errors:
        return report(False)
    require(dossier['record_id'] not in identities, 'dossier ID collides with artifact')
    require(dossier['support_revision'] == canonical.identity['exp_version'], 'dossier support mismatch')
    require({k: dossier['candidate'][k] for k in selected['candidate']} == selected['candidate'], 'dossier candidate mismatch')
    require(dossier['case_definition']['ref'] == definition['ref'] and
            dossier['case_definition']['sha256'] == 'sha256:' + definition['sha256'], 'case definition mismatch')
    existing('SQ', [{'code': code} for code in sq.violations(dossier, step_map)])
    mapped = {}
    for item in array(selected['steps'], 'steps'):
        exact(item, ('scenario', 'step', 'result_slot'), 'step mapping')
        key = (item['scenario'], item['step'])
        require(all(isinstance(v, str) for v in key) and key not in mapped, 'duplicate or invalid step mapping')
        require(item['result_slot'] not in mapped.values(), 'duplicate direct result slot')
        mapped[key] = item['result_slot']
    expected_steps = {(s['scenario'], st['step']): st for s in dossier['scenarios'] for st in s['steps'] if st['state'] == 'recorded'}
    require(set(mapped) == set(expected_steps), 'recorded step mapping mismatch')
    direct = set(mapped.values())
    candidate = selected['candidate']
    for key, slot in mapped.items():
        value = record(slot, 'result')
        if value is None:
            continue
        st = expected_steps[key]
        require(value['record_id'] == st['result_record'], 'step result ID mismatch')
        require(value['outcome'] == st['outcome'], 'step outcome mismatch')
        require(value['case'] == {'owner_deliverable': 'DEL-09-02', 'case_id': key[1], 'scenario': key[0]}, 'unsupported direct case mapping')
        require(value['run_basis'] == 'candidate', 'direct result is not candidate basis')
        app = value['subject'].get('app_candidate', {})
        require(all(app.get(k) == candidate[k] for k in ('revision', 'build_identity')) and
                value['configuration']['codex_pin'] == candidate['codex_pin'], 'direct candidate mismatch')
        require(value['configuration']['route']['kind'] in ('native_development', 'native_packaged'), 'direct route is not native')
        evidence = list(value['evidence']) + [e for part in value.get('parts', []) for e in part.get('evidence', [])]
        external.extend({'scope': slot, 'ref': e['ref'], 'kind': 'result evidence'} for e in evidence)
        if value['criterion'].get('disposition_ref'):
            external.append({'scope': slot, 'ref': value['criterion']['disposition_ref'], 'kind': 'criterion disposition'})
        form = value['configuration']['route'].get('native_route', {}).get('form_ref')
        if form:
            external.append({'scope': slot, 'ref': form, 'kind': 'native form'})
    if any(st['state'] != 'recorded' for s in dossier['scenarios'] for st in s['steps']):
        missing.append('non-recorded steps: examination obligations outstanding')

    review_selection = selected['review']
    citation = dossier['examiner'].get('review_record')
    if review_selection is None:
        require(citation is None, 'cited primary review has no selection')
        missing.append('primary review absent; SQ-SEQ7 remains outstanding')
    else:
        exact(review_selection, ('slot', 'subject_alias', 'reviewer_identity', 'author_identities', 'review_kind',
                                 'reported_as_independent', 'results', 'evidence'), 'primary review selection')
        rev = record(review_selection['slot'], 'review')
        require(isinstance(review_selection['results'], dict), 'review results must be a mapping')
        require(set(review_selection['results']) <= direct, 'review maps a non-direct result')
        if set(review_selection['results']) != direct:
            missing.append('review does not cover all recorded direct results')
        require(review_selection['review_kind'] == 'v4_ops_34', 'primary review must be v4_ops_34')
        ev = {}
        for item in array(review_selection['evidence'], 'review evidence'):
            exact(item, ('ref', 'target'), 'review evidence entry')
            ref = item['ref']; target = item['target']
            require(isinstance(ref, str) and ref and ref not in ev, 'duplicate or invalid evidence citation')
            require(isinstance(target, dict), 'invalid evidence target')
            for flag in ('dossier', 'case_definition'):
                if flag in target:
                    require(type(target[flag]) is bool and target[flag], 'invalid evidence target flag')
            ev[ref] = target
            if ref == dossier['record_id']:
                require(target == {'dossier': True}, 'contradictory dossier review target')
            elif 'dossier' in target:
                raise ValueError('dossier citation must equal complete dossier ID')
            if ref in identities:
                require(set(target) == {'slot'} and target['slot'] in identities[ref], 'selected record masquerades as opaque or conflicting evidence')
                direct_targets = [slot for slot in identities[ref] if slot in direct]
                if direct_targets:
                    require(direct_targets == [target['slot']], 'review maps a different snapshot than the direct result')
            if set(target) == {'slot'}:
                slot = target['slot']
                require(slot in artifacts, 'unknown evidence slot')
                value = record(slot, artifacts[slot]['kind'])
                if value is not None:
                    require(value['record_id'] == ref, 'evidence record ID mismatch')
            elif target == {'dossier': True}:
                pass
            elif target == {'case_definition': True}:
                require(ref == definition['ref'], 'case definition evidence citation mismatch')
            elif set(target) == {'path', 'sha256'}:
                file(target, 'opaque review evidence: ' + ref)
            else:
                raise ValueError('invalid review evidence target')
        if rev is not None:
            require(citation == rev['record_id'], 'primary review ID mismatch')
            require(rev['subject']['kind'] == 'candidate' and rev['subject']['identity'] == review_selection['subject_alias'], 'review subject mismatch')
            require(rev['reviewer']['identity'] == review_selection['reviewer_identity'] and
                    sorted(a['identity'] for a in rev['authors']) == sorted(review_selection['author_identities']) and
                    rev['review_kind'] == review_selection['review_kind'] and
                    type(review_selection['reported_as_independent']) is bool and
                    rev['reported_as_independent'] == review_selection['reported_as_independent'], 'review selection mismatch')
            require(len(rev['evidence_set']) == len(set(rev['evidence_set'])), 'duplicate review evidence')
            require(set(ev) <= set(rev['evidence_set']), 'uncited review evidence mapping')
            if set(ev) != set(rev['evidence_set']):
                missing.append('review evidence mapping incomplete')
            if dossier['record_id'] not in rev['evidence_set'] or dossier['record_id'] not in ev:
                missing.append('exact dossier review citation absent')
            if dossier['handoff']['reported_as_independent']:
                require(rev['reported_as_independent'], 'dossier/review independence mismatch')
            for slot, basis in review_selection['results'].items():
                value = record(slot, 'result')
                if value is None:
                    continue
                args = {k: review_selection[k] for k in ('subject_alias', 'reviewer_identity', 'author_identities', 'review_kind', 'reported_as_independent')}
                args['basis'] = basis
                found, unresolved = admission.review_join(rev, value, args)
                existing('review/' + slot, found, unresolved)
                # Keep original helper output; closure is this receiver's own join.
                if any(ref not in ev for ref in unresolved):
                    missing.append('unresolved selected review evidence')

    # Citation-conditional package records. No package is manufactured for development.
    package_refs = {}
    if 'package_record' in dossier['candidate']:
        package_refs[dossier['candidate']['package_record']] = set()
    for slot in direct:
        value = records.get(slot)
        if value:
            ref = value['subject']['app_candidate'].get('package_record')
            if ref:
                package_refs.setdefault(ref, set()).add(slot)
    seen_packages = set()
    for item in array(selected['packages'], 'packages'):
        exact(item, ('ref', 'slot', 'result_slots'), 'package selection')
        ref = item['ref']; slots = array(item['result_slots'], 'package result slots')
        require(isinstance(ref, str) and ref in package_refs and ref not in seen_packages, 'uncited or duplicate package selection')
        require(len(slots) == len(set(slots)) and set(slots) == package_refs[ref], 'package result mapping mismatch')
        seen_packages.add(ref); pkg = record(item['slot'], 'package')
        if pkg is None:
            continue
        require(pkg['record_id'] == ref and all(pkg['app'][k] == candidate[k] for k in ('revision', 'build_identity')) and
                pkg['codex']['pin'] == candidate['codex_pin'], 'package candidate/reference mismatch')
        for slot in slots:
            value = records.get(slot)
            if value is None:
                continue
            if value['configuration']['route']['kind'] != 'native_packaged' or value['currency']['state'] != 'current' or value['subject']['app_candidate'].get('packaged') is not True:
                unsupported.append('package-link not evaluated: ' + slot)
                continue
            found, gaps = package.package_link(value, pkg, candidate['revision'], candidate['build_identity'], candidate['codex_pin'], ref)
            existing('package/' + slot, found)
            checks[-1]['reported_prerequisite_gaps'] = gaps
        if not slots:
            unsupported.append('package-link has no selected packaged result')
    if set(package_refs) != seen_packages:
        missing.append('cited package selection missing')

    changes = array(selected['changes'], 'changes'); change_refs = set()
    for value in [dossier, *[v for v in records.values() if v.get('record_kind') == 'exam_result']]:
        if value['currency'].get('change_ref'):
            change_refs.add(value['currency']['change_ref'])
    seen_changes, allowed_duplicates = set(), set()
    for item in changes:
        exact(item, ('slot', 'from_alias', 'to_alias', 'pairs'), 'change selection')
        change = record(item['slot'], 'change')
        pairs = array(item['pairs'], 'change pairs'); priors = {}; covered = set()
        if change is not None:
            require(change['record_id'] in change_refs and change['record_id'] not in seen_changes, 'uncited or duplicate change')
            require(change['from'] == item['from_alias'] and change['to'] == item['to_alias'], 'change alias mismatch')
            seen_changes.add(change['record_id'])
        for pair in pairs:
            exact(pair, ('before_slot', 'after_slot', 'rerun_slot', 'before_basis', 'rerun_basis'), 'change pair')
            before = record(pair['before_slot'], 'result'); after = record(pair['after_slot'], 'result')
            require(pair['before_slot'] != pair['after_slot'], 'change snapshots require distinct slots')
            allowed_duplicates.add(frozenset((pair['before_slot'], pair['after_slot'])))
            rerun = record(pair['rerun_slot'], 'result') if pair['rerun_slot'] is not None else None
            if before is None or after is None or (pair['rerun_slot'] is not None and rerun is None) or change is None:
                missing.append('change pair bytes unavailable'); continue
            require(before['record_id'] == after['record_id'], 'change snapshot IDs differ')
            require(after['record_id'] not in priors, 'duplicate change prior pair')
            priors[after['record_id']] = after; covered.add(after['record_id'])
            args = {'from_alias': item['from_alias'], 'to_alias': item['to_alias'], 'before_basis': pair['before_basis'], 'rerun_basis': pair['rerun_basis']}
            found, unresolved = admission.change_join(change, before, after, args, rerun)
            existing('change/' + pair['after_slot'], found, unresolved)
        if change is not None:
            rows = {row['prior_result'] for row in change['affected']}
            require(covered <= rows and len(rows) == len(change['affected']), 'duplicate or unselected change rows')
            if covered != rows:
                missing.append('change prior snapshots incomplete')
            else:
                existing('change/' + item['slot'], admission.validate('change', change, priors))
    if change_refs != seen_changes:
        missing.append('cited change selection missing')
    for identity, slots in identities.items():
        if len(slots) > 1:
            require(len(slots) == 2 and frozenset(slots) in allowed_duplicates, 'ambiguous duplicate record ID')
    require(used == set(artifacts), 'unreferenced selected artifacts')
    for scenario in dossier['scenarios']:
        for st in scenario['steps']:
            for stimulus in st.get('stimuli', []):
                if stimulus.get('evidence'):
                    external.append({'scope': st['step'], 'ref': stimulus['evidence'], 'kind': 'stimulus'})
            for supplier in st['supplier_cases']:
                if supplier.get('result_ref'):
                    external.append({'scope': st['step'], 'ref': supplier['result_ref'], 'kind': 'supplier result'})
    return report(not errors)



if __name__ == '__main__':
    try:
        output = check(Path(sys.argv[1]), sys.argv[2])
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as error:
        output = {'selection_consistent': False, 'coverage': 'incomplete', 'input_error': str(error),
                  'current_reliance': False, 'qualification_established': False,
                  'actual_producer_use_verified': False, 'native_observation_verified': False,
                  'publication_authority_authenticated': False, 'method_adoption_authenticated': False,
                  'limits': LIMITS}
    print(json.dumps(output))
