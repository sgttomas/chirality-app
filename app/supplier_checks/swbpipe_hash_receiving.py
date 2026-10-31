"""Offline PR40 evidence correspondence, not workspace/hash computation or ingress."""
import copy
import re


def engine_hash(value):
    if not isinstance(value, dict) or not isinstance(value.get('value'), str) or re.fullmatch(r'sha256:[0-9a-f]{64}', value['value']) is None:
        raise ValueError('AGENT-ENGINE-HASH-FORM-REFUSED')
    return value


def catalog_hash(value):
    if not isinstance(value, dict) or not isinstance(value.get('value'), str) or re.fullmatch(r'[0-9a-f]{64}', value['value']) is None:
        raise ValueError('AGENT-CATALOG-HASH-FORM-REFUSED')
    return value


def check_hash_pair(engine, catalog):
    """Verify supplied forms plus all metadata; never manufacture a missing hash."""
    engine_hash(engine); catalog_hash(catalog)
    expected = copy.deepcopy(engine)
    expected['value'] = engine['value'][7:]
    if expected != catalog:
        raise ValueError('engine/catalog hash correspondence mismatch')


def check_batch(engine, catalog_basis, batch_source_model_hash, validation_hash):
    check_hash_pair(engine, catalog_basis['modelHash'])
    if batch_source_model_hash != engine['value'] or validation_hash != engine:
        raise ValueError('operation batch must preserve exact engine evidence')


def check_snapshot(publication, evidence):
    """Compare a supplied snapshot to invented owner evidence. No React simulation.

    evidence names both counters independently, so equality of unrelated UI and
    model counters is never treated as readiness. None means hash unavailable.
    """
    keys = ('generation', 'live_generation', 'ui_revision', 'owner_generation',
            'owner_ui_revision', 'computed_model_revision', 'model_revision')
    if any(type(evidence.get(k)) is not int for k in keys):
        raise ValueError('invalid owned revision evidence')
    ready = (evidence['generation'] == evidence['live_generation'] == evidence['owner_generation']
             and evidence['ui_revision'] == evidence['owner_ui_revision']
             and evidence['computed_model_revision'] == evidence['model_revision'])
    if (type(publication.get('revision')) is not int or type(publication.get('generation')) is not int
            or publication['revision'] != evidence['model_revision']
            or publication['generation'] != evidence['live_generation']):
        raise ValueError('snapshot revision or generation rebound')
    expected = evidence['engine_hash'] if ready else None
    if 'hash' not in publication:
        raise ValueError('snapshot hash evidence missing')
    if publication['hash'] != expected:
        raise ValueError('snapshot publishes stale or unrelated hash')
    # Missing/pending hash never becomes ready just because counters match.
    if expected is not None:
        engine_hash(expected)


def check_retained_result(captured_basis, result, engine_outcome):
    if result['basis'] != captured_basis:
        raise ValueError('retained basis rebound')
    data = result['data']
    if not isinstance(data, dict) or sum(key in data for key in ('outcomeModelHash', 'evaluatedModelHash')) != 1:
        raise ValueError('exactly one retained hash role required')
    if 'evaluatedModelHash' in data:
        actual = data['evaluatedModelHash']
        catalog_hash(captured_basis['modelHash'])
        if actual != captured_basis['modelHash']:
            raise ValueError('evaluated hash rebound from captured basis')
    else:
        # Application may create a new model; its outcome is not the solve basis.
        actual = data['outcomeModelHash']
    if engine_outcome is None:
        if actual is not None:
            raise ValueError('unavailable engine outcome fabricated')
    else:
        check_hash_pair(engine_outcome, actual)
