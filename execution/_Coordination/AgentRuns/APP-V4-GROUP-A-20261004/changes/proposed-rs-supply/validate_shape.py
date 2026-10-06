"""Offline private suppliedGuidance shape check; no receiving-authority claim."""
import json
from pathlib import Path
import jsonschema
p = Path(__file__).parent
schema = json.loads((p / "RS_RECORD.schema.json").read_text())
validator = jsonschema.Draft202012Validator({"$ref": "#/$defs/suppliedGuidance", "$defs": schema["$defs"]})
native = json.loads((p / "RS_RECORD.valid.native-supply.example.jsonl").read_text())
validator.validate(native["body"])
legacy = dict(native["body"])
legacy.pop("nativeTurn")
legacy["turn"] = 6
legacy["supplyCheck"] = "verified"
validator.validate(legacy)
negative = json.loads((p / "RS_RECORD.invalid.native-supply.examples.json").read_text())
for case in negative:
    assert not validator.is_valid(case["record"]["body"]), case["reason"]
print("PASS: native and ordinal shape; 7 negatives refused. Semantic receiving not executed.")
