#!/usr/bin/env python3
"""Invented inventory computation only; prints JSON, never records a human act."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

MODE = 'revision-1'

def tally(path):
    data = path.read_bytes()
    reader = csv.DictReader(io.StringIO(data.decode('utf-8')))
    if reader.fieldnames != ['item', 'material', 'pieces']:
        raise ValueError('expected item,material,pieces header')
    rows = list(reader)
    seen, groups = set(), {}
    for row in rows:
        if set(row) != {'item', 'material', 'pieces'} or not row['item'] or not row['material']:
            raise ValueError('incomplete row')
        if not row['pieces'] or not row['pieces'].isascii() or not row['pieces'].isdigit():
            raise ValueError('pieces must be a nonnegative integer')
        if MODE == 'revision-3' and row['item'] in seen:
            raise ValueError('duplicate item identifier')
        seen.add(row['item'])
        groups[row['material']] = groups.get(row['material'], 0) + int(row['pieces'])
    result = {'input_sha256': hashlib.sha256(data).hexdigest(), 'standing': 'computed invented count; no act or qualification'}
    if MODE == 'user-collision':
        result['rows'] = len(rows)
    else:
        result['pieces'] = sum(groups.values())
        if MODE in ('revision-2', 'revision-3'):
            result['by_material'] = groups
    return result

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('usage: python3 tally.py INPUT.csv')
        print(json.dumps(tally(Path(sys.argv[1])), sort_keys=True))
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
