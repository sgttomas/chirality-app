"""Carrier detection must not promote quoted text or a damaged call shape."""
import copy
import unittest

from records_delivery import named_tools, reported_route

DEFINITION = {"type": "function", "name": "fixture_records", "description": "Invented quoted evidence tool.",
    "inputSchema": {"type": "object", "additionalProperties": False, "required": ["operation"],
        "properties": {"operation": {"type": "string", "enum": ["list", "read"]},
            "limit": {"type": "integer", "minimum": 1, "maximum": 50}}}}
DECLARATION = 'declare const tools: { fixture_records(args: { limit?: number; operation: "list" | "read"; }): Promise<unknown>; };'
SECTION = f"### `fixture_records`\n{DEFINITION['description']}\n\nexec tool declaration:\n```ts\n{DECLARATION}\n```"


def code_body(section):
    return {"input": [{"type": "additional_tools", "tools": [{"type": "namespace", "name": "functions",
        "tools": [{"type": "custom", "name": "exec", "description": section}]}]}]}


class CarrierDetection(unittest.TestCase):
    def test_actual_carriers_retain_definition(self):
        self.assertEqual(len(named_tools(code_body(SECTION), DEFINITION)), 1)
        direct = dict(DEFINITION)
        direct["parameters"] = direct.pop("inputSchema")
        self.assertEqual(len(named_tools({"tools": [direct]}, DEFINITION)), 1)

    def test_quoted_objects_and_declarations_confer_no_carriage(self):
        body = {"input": [{"type": "message", "role": "developer", "content": [DEFINITION,
            {"type": "custom", "name": "exec", "description": SECTION}]}]}
        self.assertEqual(named_tools(body, DEFINITION), [])
        wrong_namespace = code_body(SECTION)
        wrong_namespace["input"][0]["tools"][0]["name"] = "quoted"
        self.assertEqual(named_tools(wrong_namespace, DEFINITION), [])

    def test_damaged_argument_shape_or_description_fails(self):
        for wrong in (SECTION.replace('limit?: number; operation: "list" | "read";', ''),
                SECTION.replace('"list" | "read"', '"list"'),
                SECTION.replace(DEFINITION["description"], "Another description.")):
            self.assertEqual(named_tools(code_body(wrong), DEFINITION), [])
        direct = copy.deepcopy(DEFINITION)
        direct["inputSchema"]["required"] = []
        self.assertEqual(named_tools({"tools": [direct]}, DEFINITION), [])

    def test_observed_flat_scalar_projection_is_distinct_from_exact_schema(self):
        bounded = copy.deepcopy(DEFINITION)
        bounded["inputSchema"]["properties"]["cursor"] = {"type":"string", "minLength":1, "maxLength":32}
        parameters = copy.deepcopy(bounded["inputSchema"])
        parameters["properties"]["cursor"] = {"type":"string"}
        parameters["properties"]["limit"] = {"type":"integer"}
        tool = {"type":"function", "name":bounded["name"], "description":bounded["description"],
            "strict":False, "parameters":parameters}
        found = named_tools({"tools":[tool]}, bounded)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["representation"], "function")
        self.assertEqual(found[0]["schemaRendering"], "stock-scalar-projection")
        self.assertEqual(found[0]["path"], ["tools", 0])
        self.assertEqual(tool["parameters"]["properties"]["cursor"], {"type":"string"})
        self.assertEqual(bounded["inputSchema"]["properties"]["cursor"]["maxLength"], 32)

    def test_flat_projection_preserves_call_shape_and_unknown_facets(self):
        projected = {"type":"function", "name":DEFINITION["name"], "description":DEFINITION["description"],
            "parameters":{"type":"object", "additionalProperties":False, "required":["operation"],
                "properties":{"operation":{"type":"string", "enum":["list", "read"]}, "limit":{"type":"integer"}}}}
        for mutate in (
                lambda p: p.update(required=[]),
                lambda p: p.update(additionalProperties=True),
                lambda p: p["properties"]["operation"].update(enum=["list"]),
                lambda p: p["properties"]["limit"].update(type="number"),
                lambda p: p["properties"]["limit"].update(minimum=2),
                lambda p: p.update(unexpected="field")):
            damaged = copy.deepcopy(projected)
            mutate(damaged["parameters"])
            self.assertEqual(named_tools({"tools":[damaged]}, DEFINITION), [])
        unknown = copy.deepcopy(DEFINITION)
        unknown["inputSchema"]["properties"]["operation"]["pattern"] = "list|read"
        self.assertEqual(named_tools({"tools":[projected]}, unknown), [])
        damaged_description = copy.deepcopy(projected)
        damaged_description["description"] = "Another description."
        self.assertEqual(named_tools({"tools":[damaged_description]}, DEFINITION), [])
        quoted = {"input":[{"type":"message", "role":"developer", "content":[projected]}]}
        self.assertEqual(named_tools(quoted, DEFINITION), [])

    def test_duplicate_real_carriers_remain_visible(self):
        direct = dict(DEFINITION)
        direct["parameters"] = direct.pop("inputSchema")
        self.assertEqual(len(named_tools({"tools":[direct, copy.deepcopy(direct)]}, DEFINITION)), 2)

    def test_namespace_capability_is_reported_and_never_inferred_from_provider(self):
        config = {"config":{"model":"fixture-model", "model_provider":"lmstudio"}}
        self.assertEqual(reported_route(config, {"namespaceTools":True}, "fixture-model", "lmstudio")["namespaceTools"], True)
        self.assertEqual(reported_route(config, {"namespaceTools":False}, "fixture-model", "lmstudio")["namespaceTools"], False)
        for capabilities in ({}, {"namespaceTools":None}, {"namespaceTools":"false"}, {"namespaceTools":0}):
            with self.assertRaises(RuntimeError):
                reported_route(config, capabilities, "fixture-model", "lmstudio")
        for model, provider in (("different-model", "lmstudio"), ("fixture-model", "fixture")):
            with self.assertRaises(RuntimeError):
                reported_route(config, {"namespaceTools":True}, model, provider)


if __name__ == "__main__":
    unittest.main()
