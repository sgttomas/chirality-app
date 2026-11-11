"""Exact catalog-v3 source intake for offline fixtures, never runtime activation."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG_PATH = HERE / 'fixtures/swbpipe-catalog-v3/agent-capability-catalog.json'
# The supplier's edition of the catalog these fixtures receive.
SELECTION = {
    'repository': 'sgttomas/SWBPIPE',
    'commit': '4d8cb7b0c8f101d5102813e634e23ecba29b310e',
    'checked_head': 'aa62c3dc7bf14d50b925a1b480ff54fb1b8bf3c2',
    'pull_request': 'https://github.com/sgttomas/SWBPIPE/pull/15',
    'catalog_version': 'swbpipe-catalog/3',
}
RECEIVING_SHA256 = '652ccc0c25263a01ce103a8a7a3e64a7c01833b0588dcbc054ad461301b810ec'
RECEIVING_BYTES = 61618


def selection():
    return dict(SELECTION)


def load_catalog(path=None):
    selected = CATALOG_PATH if path is None else Path(path)
    with selected.open('rb') as stream:
        raw = stream.read(RECEIVING_BYTES + 1)
    if len(raw) != RECEIVING_BYTES or hashlib.sha256(raw).hexdigest() != RECEIVING_SHA256:
        raise ValueError('catalog does not match the integrated v3 receiving identity')
    value = json.loads(raw)
    if value['catalogVersion'] != SELECTION['catalog_version']:
        raise ValueError('unsupported receiving catalog version')
    return value
