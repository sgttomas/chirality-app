"""Exact catalog-v3 source intake for offline fixtures, never runtime activation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINS_PATH = ROOT / 'execution/PKG-03/DEL-03-02/Work/swbpipe-catalog-v3-pins.json'
RECEIVING_SHA256 = '652ccc0c25263a01ce103a8a7a3e64a7c01833b0588dcbc054ad461301b810ec'
RECEIVING_BYTES = 61618
PINS_SHA256 = 'a2c0f7f127771b55403066ce8eeb4dcfe280e023822772b17fb0d794128949a4'


def selection():
    raw = PINS_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS_SHA256:
        raise ValueError('receiving selection changed')
    return json.loads(raw)


def load_catalog(path=None):
    pins = selection()
    selected = ROOT / pins['snapshot'] if path is None else Path(path)
    with selected.open('rb') as stream:
        raw = stream.read(RECEIVING_BYTES + 1)
    if len(raw) != RECEIVING_BYTES or hashlib.sha256(raw).hexdigest() != RECEIVING_SHA256:
        raise ValueError('catalog does not match the integrated v3 receiving identity')
    value = json.loads(raw)
    if value['catalogVersion'] != 'swbpipe-catalog/3':
        raise ValueError('unsupported receiving catalog version')
    return value
