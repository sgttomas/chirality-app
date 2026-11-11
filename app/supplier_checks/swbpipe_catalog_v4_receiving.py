"""Explicit integrated v4 source selection; preserves the independent v3 reader."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Supplier source snapshots; each source row names its snapshot below this folder.
FIXTURES = HERE / 'fixtures'
CATALOG_SNAPSHOT = 'swbpipe-catalog-v4/agent-capability-catalog.json'
CATALOG_PATH = FIXTURES / CATALOG_SNAPSHOT
CATALOG_SHA256 = '8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17'
CATALOG_BYTES = 50864
# The catalog at its two supplier paths; every v4 edition received the same bytes.
CATALOG_SOURCES = [
    {'path': 'execution/PKG-16/DEL-16-06/Work/agent-capability-catalog.json',
     'snapshot': CATALOG_SNAPSHOT, 'bytes': CATALOG_BYTES, 'sha256': CATALOG_SHA256},
    {'path': 'apps/desktop/src-tauri/resources/agent-capability-catalog.json',
     'snapshot': CATALOG_SNAPSHOT, 'bytes': CATALOG_BYTES, 'sha256': CATALOG_SHA256},
]
# The supplier's edition these fixtures receive, with the supplier sources read at it.
SELECTION = {
    'repository': 'sgttomas/SWBPIPE',
    'commit': '9b6281e7eaca924e6166336b87b6d25937c1ca04',
    'checked_head': '2cd052e6746aa4404f852a39d8630b70fabf696c',
    'pull_request': 'https://github.com/sgttomas/SWBPIPE/pull/27',
    'catalog_version': 'swbpipe-catalog/4',
    'snapshot': CATALOG_SNAPSHOT,
    'sources': CATALOG_SOURCES + [
        {'path': 'execution/PKG-16/DEL-16-06/Work/embedded-agent-host.md',
         'snapshot': 'swbpipe-catalog-v4/embedded-agent-host.source.md',
         'bytes': 53735,
         'sha256': '6342146e130b67e8ecd2b9ebee311dde6a665370d7771f2ce4e862d0cbb7003c'},
        {'path': 'apps/desktop/src/services/embeddedAgentSession.ts',
         'snapshot': 'swbpipe-catalog-v4/embeddedAgentSession.source.ts.txt',
         'bytes': 33432,
         'sha256': 'd766442debf2e49bff3b2e45da9013828e324e4b97824639b9224006b0230492'},
        {'path': 'apps/desktop/src/services/embeddedAgentM2.test.ts',
         'snapshot': 'swbpipe-catalog-v4/embeddedAgentM2.test.source.ts.txt',
         'bytes': 8878,
         'sha256': 'f4a78e9a634fc0fd177f63d360d82e4f4f8c548e3735f2054695d1524c22b478'},
    ],
}


def checked_selection(value, fixtures, label):
    """Return the edition after confirming every received source snapshot is unchanged."""
    for source in value['sources']:
        with (fixtures / source['snapshot']).open('rb') as stream:
            data = stream.read(source['bytes'] + 1)
        if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError(label + ' selected source changed: ' + source['path'])
    return copy.deepcopy(value)


def read_catalog(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(CATALOG_BYTES + 1)
    if len(raw) != CATALOG_BYTES or hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise ValueError('not integrated v4 catalog')
    value = json.loads(raw)
    if value['catalogVersion'] != 'swbpipe-catalog/4':
        raise ValueError('unknown v4 catalog version')
    return value


def selection():
    return checked_selection(SELECTION, FIXTURES, 'v4')


def load_catalog(path=None):
    pins = selection()
    return read_catalog(FIXTURES / pins['snapshot'] if path is None else path)
