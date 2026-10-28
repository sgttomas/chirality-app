"""Invented six-record consumer cohort; no examination or package event occurred."""
import copy
import importlib.util
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('_s4_existing_invented_records', APP / 'tests/group_b_support_identity_canonical_test.py')
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


def write(root, support, candidate):
    records, selection = fixtures.selection_for(support)
    # Preserve different before/after and rerun candidates required by the actual
    # change protocol. Only the current rerun/package cohort receives this App.
    records['rerun']['subject']['app_candidate'].update(
        revision=candidate['revision'], build_identity=candidate['buildIdentity'])
    records['package']['app'].update(revision=candidate['revision'], build_identity=candidate['buildIdentity'])
    selection['package_selection'].update(revision=candidate['revision'], build=candidate['buildIdentity'])
    for field in ('subject', 'configuration', 'criterion'):
        selection['review_selection']['basis'][field] = copy.deepcopy(records['rerun'][field])
        selection['change_selection']['rerun_basis'][field] = copy.deepcopy(records['rerun'][field])
    return fixtures.write_bundle(root, support, records, selection)
