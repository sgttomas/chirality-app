#!/usr/bin/env python3
"""Inventory every definition at the 0.167.0/0.169.0 boundary; classify nothing.

This writes comparison inputs and exact differences, never compatibility or
qualification. Authored consumer dispositions and the independent reading are
separate. Historical inputs are bound to their accepted bytes, including the
old npm generator's stated non-equivalence to the archive tree. New input
admission uses same_basis's whole-record checks and retains its FORM_ONLY limit.
Stable/experimental membership here means generated filenames, not every
method variant or nested field inside those files. No supplier is executed.
"""
import argparse
import json
import os
import re
from pathlib import Path

import intake
import same_basis as admission

OLD_FILES = {
    "CANONICAL_DISTRIBUTION.json": "e6b0cd48c3d77728c44f2b79a2eb319686615b4521abb8585e9267694d380f61",
    "GENERATION.json": "09c339f148d90034f1dba511c7a5b8e18545291e96a1fc96be744d2f17f24026",
    "MANIFEST.sha256": "353ab01c4d92b18c8939c985ea1a8529e70a8d8ee58c8f9818545a13ed5dcc51",
    intake.BUNDLES[0]: "486c7c8daa5dc7f3ab2a1fb56de5316804caf7a4210fda1dc28d3f0f4e90cfe1",
    intake.BUNDLES[1]: "b1e5d17224b9d9732b5976012438ba78e2cf7e418b67f8f8a5f5cffe301b875d",
}


def digest(value):
    return admission.sha256(admission.canonical(value).encode("utf-8"))


def escape(value):
    return value.replace("~", "~0").replace("/", "~1")


def differences(before, after, path=""):
    """Exact JSON differences, preserving null/missing, bool/int and array order."""
    if type(before) is not type(after):
        return [{"path": path, "before": before, "after": after}]
    if isinstance(before, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            at = path + "/" + escape(key)
            if key not in before:
                result.append({"path": at, "added": after[key]})
            elif key not in after:
                result.append({"path": at, "removed": before[key]})
            else:
                result.extend(differences(before[key], after[key], at))
        return result
    if isinstance(before, list) and len(before) == len(after):
        return [change for i, (old, new) in enumerate(zip(before, after))
                for change in differences(old, new, path + "/" + str(i))]
    return [] if before == after else [{"path": path, "before": before, "after": after}]


def references(document):
    rows = []
    def visit(value, path):
        if isinstance(value, dict):
            for key, item in value.items():
                at = path + "/" + escape(key)
                if key in ("$ref", "$dynamicRef", "$recursiveRef"):
                    admission.require(key == "$ref" and isinstance(item, str) and item.startswith("#/"),
                                      "unresolved reference at " + at)
                    target = document
                    try:
                        for token in item[2:].split("/"):
                            admission.require(not re.search(r"~(?![01])", token) and "%" not in token,
                                              "unsupported pointer spelling at " + at)
                            token = token.replace("~1", "/").replace("~0", "~")
                            if isinstance(target, list):
                                admission.require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None,
                                                  "invalid array pointer at " + at)
                            target = target[int(token)] if isinstance(target, list) else target[token]
                    except (KeyError, IndexError, ValueError, TypeError):
                        raise admission.Refused("unresolved reference " + item + " at " + at) from None
                    rows.append({"at": at, "target": item, "target_sha256": digest(target)})
                else:
                    visit(item, at)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                visit(item, path + "/" + str(i))
    visit(document, "")
    return sorted(rows, key=lambda row: row["at"])


def definitions(document, main):
    value = document.get("definitions")
    admission.require(isinstance(value, dict) and value, "definitions absent or malformed")
    result = {}
    for name, definition in value.items():
        if main and name == "v2":
            admission.require(isinstance(definition, dict), "main v2 namespace malformed")
            for child, schema in definition.items():
                result["/definitions/v2/" + escape(child)] = schema
        else:
            result["/definitions/" + escape(name)] = definition
    for pointer, schema in result.items():
        admission.require(isinstance(schema, (dict, bool)), "definition is not a schema: " + pointer)
    return result


def normalize_v2_refs(value):
    if isinstance(value, dict):
        return {key: (item.replace("#/definitions/v2/", "#/definitions/", 1)
                      if key == "$ref" and isinstance(item, str) else normalize_v2_refs(item))
                for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_v2_refs(item) for item in value]
    return value


def methods(document):
    result = {}
    for name in ("ClientRequest", "ServerRequest", "ClientNotification", "ServerNotification"):
        definition = document["definitions"].get(name)
        if definition is None:
            continue
        variants = definition.get("oneOf")
        admission.require(isinstance(variants, list), name + " variants could not be read")
        rows = []
        for variant in variants:
            enum = variant.get("properties", {}).get("method", {}).get("enum")
            admission.require(isinstance(enum, list) and len(enum) == 1 and isinstance(enum[0], str),
                              name + " contains an unread method variant")
            rows.append({"method": enum[0], "variant_sha256": digest(variant)})
        admission.require(len({row["method"] for row in rows}) == len(rows), name + " repeats a method")
        result[name] = sorted(rows, key=lambda row: row["method"])
    return result


def read_basis(pin):
    folder = Path(intake.RESOURCES) / pin
    admission.require(not os.path.lexists(folder / "SUPPLEMENT.json"), "supplement needs its own comparison")
    raw = {name: admission.read(folder / name) for name in OLD_FILES}
    identities = {name: admission.sha256(data) for name, data in raw.items()}
    if pin == "0.167.0":
        admission.expect(identities, OLD_FILES, "accepted historical input bytes")
        # Strictly parse the full retained records too; their immutable-byte
        # binding does not turn the old npm tree into the archive tree.
        record = admission.strict_json(raw["CANONICAL_DISTRIBUTION.json"], "old distribution")
        generation = admission.strict_json(raw["GENERATION.json"], "old generation")
        admission.require(record["generator_join"]["main_sha256"] == generation["supplier"]["main_sha256"],
                          "historical generator/binary join differs")
    else:
        record = admission.admit_distribution(pin, raw["CANONICAL_DISTRIBUTION.json"])
        generation = admission.admit_generation(pin, raw["GENERATION.json"], record, raw["MANIFEST.sha256"],
            {name: identities[name] for name in intake.BUNDLES}, sum(len(raw[name]) for name in intake.BUNDLES))
    variants = admission.manifest_variants(raw["MANIFEST.sha256"], {name: identities[name] for name in intake.BUNDLES})
    manifest = {variant: {line.strip().split("  ", 1)[1]: line.split("  ", 1)[0] for line in lines}
                for variant, lines in variants.items()}
    bundles = {name: admission.strict_json(raw[name], name) for name in intake.BUNDLES}
    main, v2 = (bundles[name] for name in intake.BUNDLES)
    nested = main["definitions"]["v2"]
    shared = sorted(nested.keys() & v2["definitions"].keys())
    mismatches = [name for name in shared if differences(normalize_v2_refs(nested[name]), v2["definitions"][name])]
    admission.require(not mismatches, "main/v2 disagree after reference-prefix normalization: " + ", ".join(mismatches))
    return bundles, {"files": identities, "generation": generation, "distribution": record,
        "manifest_membership": manifest,
        "main_v2_agreement": {"shared_definitions": shared, "mismatches": mismatches,
            "standalone_only": sorted(v2["definitions"].keys() - nested.keys()),
            "main_nested_only": sorted(nested.keys() - v2["definitions"].keys()),
            "normalization": "only $ref #/definitions/v2/ becomes #/definitions/"},
        "references": {name: references(doc) for name, doc in bundles.items()},
        "method_sets": {name: methods(doc) for name, doc in bundles.items()}}


def compare():
    old, old_inputs = read_basis("0.167.0")
    new, new_inputs = read_basis("0.169.0")
    inventory, findings = [], []
    for index, name in enumerate(intake.BUNDLES):
        old_defs, new_defs = definitions(old[name], index == 0), definitions(new[name], index == 0)
        for pointer in sorted(old_defs.keys() | new_defs.keys()):
            before, after = old_defs.get(pointer), new_defs.get(pointer)
            state = "added" if pointer not in old_defs else "removed" if pointer not in new_defs else (
                "changed" if differences(before, after) else "unchanged")
            row = {"bundle": name, "pointer": pointer, "state": state,
                   "before_sha256": digest(before) if pointer in old_defs else None,
                   "after_sha256": digest(after) if pointer in new_defs else None}
            inventory.append(row)
            if state != "unchanged":
                findings.append({**row, "id": "VA169-" + digest(row)[:16],
                    "differences": [{state: after if state == "added" else before, "path": ""}]
                    if state in ("added", "removed") else differences(before, after)})
        metadata = lambda doc: {key: value for key, value in doc.items() if key != "definitions"}
        changes = differences(metadata(old[name]), metadata(new[name]))
        if changes:
            findings.append({"id": "VA169-meta-" + str(index), "bundle": name,
                             "pointer": "", "state": "metadata changed", "differences": changes})
    return {"format": "chirality.app-v4.full-definition-comparison.v1", "from": "0.167.0", "to": "0.169.0",
        "result": "inventory only; consumer dispositions and independent reading required",
        "inputs": {"0.167.0": old_inputs, "0.169.0": new_inputs}, "supplement": "absent at both pins",
        "definitions": inventory, "findings": findings,
        "limits": ["Every definition in both retained compiled bundles is inventoried; no relied-on subset is inferred from source text.",
            "No automatic compatibility classification or consumer disposition.",
            "Stable/experimental filename membership does not establish every method variant or nested field's standing.",
            "The old generation used the retained npm distribution; its whole tree was not the official archive tree.",
            "Stable inputs assumed; concurrent writers and consistent forgery excluded.",
            "This comparison does not establish runtime behaviour, level rows, the two settings, contacts, lasting rules and trust, sign-in or candidate qualification."],
        "new_records_admitted_by_form_only": admission.FORM_ONLY}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = compare()
    Path(args.out).write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"definitions": len(result["definitions"]), "findings": len(result["findings"]),
                      "result": result["result"]}))
