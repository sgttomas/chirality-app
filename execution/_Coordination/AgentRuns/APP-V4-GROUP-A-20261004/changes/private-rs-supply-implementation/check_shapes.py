"""python3 check_shapes.py /absolute/private/app -- no network retrieval."""
import json, sys
from pathlib import Path
import jsonschema
from referencing import Registry, Resource
root = Path(sys.argv[1]) / 'src-tauri/schemas'
def no_retrieval(uri):
    raise RuntimeError('retrieval forbidden: ' + uri)
registry = Registry(retrieve=no_retrieval)
for path in root.glob('*.schema.json'):
    schema = json.loads(path.read_text())
    registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
schema = json.loads((root / 'RS_RECORD.schema.json').read_text())
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(schema, registry=registry)
validator.validate(json.loads((root / 'fixtures/native-supply.example.jsonl').read_text()))
negative = json.loads((root / 'fixtures/native-supply.invalid.json').read_text())
for case in negative:
    assert not validator.is_valid(case['record']), case['reason']
rows = json.loads((root / 'fixtures/valid-records.json').read_text())
if isinstance(rows, dict):
    rows = rows.get('records', [])
legacy = [r for r in rows if r.get('kind') == 'supplied_guidance']
for row in legacy:
    validator.validate(row)
print(json.dumps({'native': 'PASS', 'negative_refused': len(negative), 'legacy_valid': len(legacy)}))
