"""Explicit approved-terms successor; frozen v2 projection algorithm is unchanged."""
import hashlib
import importlib.util
import json
from pathlib import Path

METHOD = 'selected-documentary-source-condition/v3-terms'
# Generated digests; re-derive with `python3 app/examination/repin.py` (examination/README.md).
PIN_LOCK_PATH = Path(__file__).resolve().parents[1] / 'pins.lock.json'


def locked_digest(section, path):
    """The pin lock's digest for path, or None when the lock is unreadable or lacks it.

    None never equals a digest, so the reader's own check refuses through its usual report.
    """
    try:
        value = json.loads(PIN_LOCK_PATH.read_bytes())[section][path]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return value if isinstance(value, str) else None


PROJECTION_SHA256 = locked_digest('current', 'app/examination/documentary_condition.py')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate documentary field')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


class Condition:
    def __init__(self, root, manifest_bytes, read_source):
        self.root = Path(root)
        self.raw = manifest_bytes
        self.read_source = read_source
        self.manifest = parse(manifest_bytes)
        require(self.manifest['format'] == 'documentary-source-condition/3'
                and self.manifest['method'] == METHOD, 'unknown documentary source condition')
        path = Path(__file__).resolve().parents[1] / 'documentary_condition.py'
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == PROJECTION_SHA256, 'documentary projection helper changed')
        spec = importlib.util.spec_from_file_location('_terms_v2_projection', path)
        self.projection = importlib.util.module_from_spec(spec)
        exec(compile(raw, str(path), 'exec'), self.projection.__dict__)

    def capture(self, group):
        # Only the exact retained owner disposition and supplier capture are
        # adopted. This is correspondence to recorded acts, not authentication.
        adoption = self.manifest['terms_adoption']
        require(adoption['approved_revision'] == '6421c323408b010cfba575ecd8fa24865f403c00'
                and adoption['distribution_decision'] == 'not_made'
                and adoption['release_authorized'] is False, 'unsupported terms adoption')
        captured = {}
        for path, expected in adoption['artifacts'].items():
            raw = self.read_source(self.root, path)
            require(hashlib.sha256(raw).hexdigest() == expected, 'terms adoption source changed: ' + path)
            captured[path] = raw
        record = parse(captured[adoption['record']])
        require(record['format'] == 'chirality.distribution-terms-position/v1'
                and record['state'] == 'applicable_position_retained'
                and record['distribution_decision'] == 'not_made', 'unapproved terms position')
        approval_ref = record['owner_disposition']['approval']
        approval_raw = captured[approval_ref['path']]
        require(hashlib.sha256(approval_raw).hexdigest() == approval_ref['sha256'], 'terms approval mismatch')
        approval = parse(approval_raw)
        require(approval['actor_role'] == 'owner' and approval['actor'] == 'App owner'
                and approval['actor'] == record['owner_disposition']['actor']
                and approval['applicability'] == 'accepted'
                and approval['release_authorized'] is False
                and approval['purpose'] == 'terms_applicability_only'
                and approval['scope'] == record['scope']
                and approval['scope']['includes_first_public_distribution'] is True
                and approval['approved_proposal']['revision'] == adoption['approved_revision'],
                'terms actor, scope or applicability mismatch')
        # Reuse the unchanged v2 selector evaluator, with only the separately
        # selected successor manifest's expected projection.
        projected_manifest = dict(self.manifest, method=self.projection.METHOD)
        documents, report = self.projection.Condition(
            self.root, json.dumps(projected_manifest).encode(), self.read_source).capture(group)
        captured.update(documents)
        report.update(method=METHOD, manifest_sha256=hashlib.sha256(self.raw).hexdigest(),
                      terms_adoption={'record': adoption['record'],
                                      'artifacts': dict(adoption['artifacts']),
                                      'recorded_applicability': 'accepted',
                                      'distribution_decision': 'not_made',
                                      'release_authorized': False,
                                      'authority_authenticated': False})
        return captured, report
