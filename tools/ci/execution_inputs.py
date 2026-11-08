"""Physical locations of retained logical inputs, separate from source identity.

The manifest records reviewed moves and selected, byte-identical App copies.
It does not change a historical digest or make an unregistered input available.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).with_name("execution-inputs.json")


def normalize(relative: str) -> str:
    prefix = "projects/chirality-app-v4/"
    if relative.startswith(prefix):
        relative = relative[len(prefix):]
    return re.sub(r"^(execution/PKG-\d+/DEL-\d+-\d+)/Design/", r"\1/Work/", relative)


def locations() -> dict[str, str]:
    value = json.loads(MANIFEST.read_bytes())
    if value["format"] != "chirality.app.execution-input-locations/1":
        raise ValueError("Unknown execution input location format")
    result = {}
    for kind, field in (("code", "path"), ("data", "copy")):
        for row in value[kind]:
            source, target = row["source"], row[field]
            if not source.startswith('execution/') or any(part in ('', '.', '..') for part in source.split('/')):
                raise ValueError('Non-contained authoring input location')
            if source in result or not target.startswith(("app/", "tools/")):
                raise ValueError("Ambiguous or non-operational input location")
            if any(part in ("", ".", "..") for part in target.split("/")):
                raise ValueError("Non-contained physical input location")
            result[source] = target
    return result


def physical_relative(relative: str) -> str:
    logical = normalize(relative)
    if not logical.startswith("execution/"):
        return logical
    try:
        return locations()[logical]
    except KeyError:
        raise ValueError("Unregistered execution input: " + relative) from None


def physical(root: Path, relative: str) -> Path:
    return Path(root) / physical_relative(relative)


def check() -> int:
    """Always-on correspondence to declarative authoring sources; no copying."""
    value = json.loads(MANIFEST.read_bytes())
    locations()
    spec = importlib.util.spec_from_file_location('_documentary_correspondence', ROOT / 'tools/ci/check_documentary_sources.py')
    correspondence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(correspondence)
    project = correspondence.projector(ROOT)
    selections = {}
    for source, selection in correspondence.projections(ROOT):
        selections.setdefault(source, []).append(selection['selectors'])
    # This current admission profile deliberately selects full documents.
    full = json.loads((ROOT / 'app/examination/admission/sources.current-v1.json').read_bytes())['sources']
    full = {normalize(source) for source in full}
    for row in value['code']:
        target = ROOT / row['path']
        if not target.is_file():
            raise ValueError('Operational source missing: ' + row['path'])
        if row.get('bound') and hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Bound source bytes changed: ' + row['path'])
    def ordinary(name):
        target = ROOT
        for part in name.split('/'):
            target = target / part
            if target.is_symlink():
                raise ValueError('Linked source/input refused: ' + name)
        if not target.is_file():
            raise ValueError('Ordinary source/input required: ' + name)
        return target
    for row in value["data"]:
        source, copied = ordinary(row["source"]), ordinary(row["copy"])
        raw, selected = source.read_bytes(), copied.read_bytes()
        if hashlib.sha256(selected).hexdigest() != row["sha256"]:
            raise ValueError("Selected App input changed: " + row["copy"])
        selectors = selections.get(row['source']) if row['source'] not in full else None
        equal = (all(project(raw, extent) == project(selected, extent) for extent in selectors)
                 if selectors else raw == selected)
        if not equal:
            raise ValueError("App input copy needs reviewed reconciliation: " + row["source"])
    return len(value["data"])


if __name__ == "__main__":
    print(f"{check()} selected App inputs match their full or declared projection extents")
