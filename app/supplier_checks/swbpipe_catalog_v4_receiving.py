"""Explicit integrated v4 source selection; preserves the independent v3 reader."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINS = ROOT / 'execution/PKG-03/DEL-03-02/Work/swbpipe-catalog-v4-pins.json'
PINS_SHA256 = 'aca47c5a2ab94dc6be7e6ffa758e5575c489dee5e55e6469bfa439554b644300'
CATALOG_SHA256 = '8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17'
CATALOG_BYTES = 50864


def selection():
    raw = PINS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS_SHA256:
        raise ValueError('v4 source selection changed')
    value = json.loads(raw)
    for source in value['sources']:
        with (ROOT / source['snapshot']).open('rb') as stream:
            data = stream.read(source['bytes'] + 1)
        if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError('v4 selected source changed: ' + source['path'])
    return value


def load_catalog(path=None):
    pins = selection()
    with (ROOT / pins['snapshot'] if path is None else Path(path)).open('rb') as stream:
        raw = stream.read(CATALOG_BYTES + 1)
    if len(raw) != CATALOG_BYTES or hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise ValueError('not integrated v4 catalog')
    value = json.loads(raw)
    if value['catalogVersion'] != 'swbpipe-catalog/4':
        raise ValueError('unknown v4 catalog version')
    return value
