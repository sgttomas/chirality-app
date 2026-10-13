"""Carrier detection must not promote quoted text or a damaged call shape."""
import copy
import unittest

from records_delivery import named_tools

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


if __name__ == "__main__":
    unittest.main()
