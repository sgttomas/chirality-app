"""Offline catalog projection and correspondence specimen; no supplier or host IO.

This is a fixture oracle, not production schema validation or an ingress adapter.
Only standard-library imports; no child processes, network, model or filesystem writes.
"""
import copy
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "execution/PKG-09/DEL-09-06/Work/SWBPIPE_CATALOG_PROPOSAL.json"


def expand(catalog, schema):
    if isinstance(schema, list):
        return [expand(catalog, item) for item in schema]
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        prefix = "#/definitions/"
        if not schema["$ref"].startswith(prefix):
            raise ValueError("external reference")
        return expand(catalog, catalog["definitions"][schema["$ref"][len(prefix):]])
    return {key: expand(catalog, value) for key, value in schema.items()}


def declarations(catalog):
    return [{"type": "function", "name": t["name"], "description": t["description"],
             "inputSchema": expand(catalog, t["inputSchema"])} for t in catalog["tools"]]


def validate(value, schema):
    """Small fixture-only evaluator for the keywords used in this proposal."""
    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            try:
                validate(value, branch)
                return
            except ValueError:
                pass
        raise ValueError("anyOf")
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        raise ValueError("const")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError("enum")
    kind = schema.get("type")
    valid_type = {"object": isinstance(value, dict), "array": isinstance(value, list),
                  "string": isinstance(value, str), "integer": type(value) is int,
                  "number": type(value) in (int, float) and math.isfinite(value) if type(value) in (int, float) else False,
                  "null": value is None}
    if kind and not valid_type[kind]:
        raise ValueError("type")
    if kind == "object":
        if len(value) > schema.get("maxProperties", float("inf")):
            raise ValueError("maxProperties")
        if not set(schema.get("required", [])) <= value.keys():
            raise ValueError("required")
        props = schema.get("properties", {})
        for key, item in value.items():
            rule = props.get(key, schema.get("additionalProperties", True))
            if rule is False:
                raise ValueError("additionalProperties")
            if isinstance(rule, dict):
                validate(item, rule)
    if kind == "array":
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            raise ValueError("uniqueItems")
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", float("inf")):
            raise ValueError("items")
        for item in value:
            validate(item, schema["items"])
    if kind == "string":
        if not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", float("inf")):
            raise ValueError("length")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            raise ValueError("pattern")
    if kind in ("integer", "number") and not schema.get("minimum", -float("inf")) <= value <= schema.get("maximum", float("inf")):
        raise ValueError("range")


def decode(raw, cap):
    if len(raw) > cap:
        raise ValueError("byte admission")
    def bad_constant(_):
        raise ValueError("nonfinite")
    return json.loads(raw, parse_constant=bad_constant)


def response(catalog, tool, result):
    validate(result, expand(catalog, tool["outputSchema"]))
    if result["status"] in ("ok", "completed", "pending_review", "applied") and result["data"] is None:
        raise ValueError("missing outcome data")
    data = result["data"]
    if data and "values" in data:
        for row in data["values"]:
            if row["availability"] != "available" and (row["value"] is not None or row["exactDecimal"] is not None or not row["reason"]):
                raise ValueError("withheld value")
    text = json.dumps(result, allow_nan=False, separators=(",", ":"))
    if len(text.encode()) > catalog["limits"]["resultBytes"]:
        raise ValueError("result byte admission")
    # Internal result is separate from descriptors and from the dynamic wire.
    internal = {"content": [{"type": "text", "text": text}],
                "structuredContent": result, "isError": result["status"] == "execution_error"}
    return {"contentItems": [{"type": "inputText", "text": internal["content"][0]["text"]}],
            "success": not internal["isError"]}


def validate_assumptions(operations, assumptions):
    operation_ids = [op["operation_id"] for op in operations]
    if len(set(operation_ids)) != len(operation_ids):
        raise ValueError("ambiguous operation ids")
    ids = [a["assumptionId"] for a in assumptions]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate assumption ids")
    for assumption in assumptions:
        if not set(assumption["affectedOperationIds"]) <= set(operation_ids):
            raise ValueError("unknown affected operation")


class Pending:
    """One invented pending call. Production must also own queues, cursors and budgets."""
    def __init__(self, catalog, binding, args_raw, current_basis, current_units=None, retained_record=None):
        self.catalog = catalog
        if catalog["catalogVersion"] not in ("swbpipe-catalog-proposal/1", "swbpipe-catalog/1", "swbpipe-catalog/2"):
            raise ValueError("unsupported catalog version")
        self.retained_policy = catalog["catalogVersion"] == "swbpipe-catalog/2"
        historical = self.retained_policy and binding.get("tool") in (
            "swbpipe_observe_proposal", "swbpipe_read_results")
        captured_basis = current_basis
        if historical:
            if retained_record is None:
                raise ValueError("missing retained record")
            captured_basis = retained_record["basis"]
            validate(captured_basis, expand(catalog, catalog["definitions"]["basis"]))
            for key in ("workspaceHandle", "applicationGeneration"):
                if captured_basis[key] != current_basis[key]:
                    raise ValueError("retained session mismatch")
        self.binding = copy.deepcopy(binding)
        validate(current_basis, expand(catalog, catalog["definitions"]["basis"]))
        if set(binding) != set(catalog["hostPolicy"]["binding"]):
            raise ValueError("binding fields")
        for key in ("workspaceHandle", "applicationGeneration", "modelRevision"):
            if type(binding[key]) is not type(captured_basis[key]) or binding[key] != captured_basis[key]:
                raise ValueError("binding basis")
        for key in ("requestRef", "threadId", "turnId", "callId", "tool"):
            if not isinstance(binding[key], str) or not binding[key]:
                raise ValueError("binding identity")
        if type(binding["rpcId"]) not in (str, int):
            raise ValueError("RPC identity")
        self.tool = next(t for t in catalog["tools"] if t["name"] == binding["tool"])
        self.args = decode(args_raw, catalog["limits"]["argumentBytes"])
        validate(self.args, expand(catalog, self.tool["inputSchema"]))
        self.basis = copy.deepcopy(captured_basis)
        if historical:
            handle_key = "proposalHandle" if binding["tool"] == "swbpipe_observe_proposal" else "runHandle"
            if self.args[handle_key] != retained_record["handle"]:
                raise ValueError("retained handle mismatch")
        if self.args.get("workspaceHandle", current_basis["workspaceHandle"]) != current_basis["workspaceHandle"]:
            raise ValueError("workspace")
        if self.args.get("basis", captured_basis) != captured_basis:
            raise ValueError("stale basis")
        if "claimedModelHash" in self.args and (self.args["claimedModelHash"] != current_basis["modelHash"]):
            raise ValueError("claimed hash")
        if len(self.args.get("operations", [])) > catalog["limits"]["proposalOperations"]:
            raise ValueError("configured batch limit")
        if self.retained_policy and "operations" in self.args:
            validate_assumptions(self.args["operations"], self.args["assumptions"])
        if "operations" in self.args:
            if not current_units or not current_units.get("length"):
                raise ValueError("units unavailable")
            for intent in self.args["operations"]:
                if intent["change"]["unit"] != current_units["length"]:
                    raise ValueError("document unit mismatch")
        self.completed = False

    def complete(self, binding, result, current_basis, retained_record=None, session_attached=True):
        if not session_attached:
            raise ValueError("detached session")
        if self.completed:
            raise ValueError("duplicate")
        if binding != self.binding:
            raise ValueError("correspondence")
        for key in ("workspaceHandle", "applicationGeneration"):
            if current_basis[key] != self.basis[key] or result["basis"][key] != self.basis[key]:
                raise ValueError("session changed")
        historical_completion = self.retained_policy and self.binding["tool"] not in (
            "swbpipe_read_model_summary", "swbpipe_read_nodes")
        for key in ("modelRevision", "modelHash"):
            if result["basis"][key] != self.basis[key]:
                raise ValueError("result rebased")
            if not historical_completion and current_basis[key] != self.basis[key]:
                raise ValueError("basis changed")
        if historical_completion and result["data"] is not None:
            # Fixture-only host-owned record, supplied separately from the untrusted completion.
            # This is NOT an extra field in the webview completion wire.
            if retained_record is None or retained_record["binding"] != self.binding:
                raise ValueError("missing or mismatched retained completion")
            if retained_record["basis"] != self.basis or retained_record["result"] != result:
                raise ValueError("forged retained outcome")
        wire = response(self.catalog, self.tool, result)
        self.completed = True
        return {"id": self.binding["rpcId"], "result": wire}
