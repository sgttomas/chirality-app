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


def locations(root=ROOT) -> dict[str, str]:
    value = json.loads((Path(root) / "tools/ci/execution-inputs.json").read_bytes())
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


def check(root=ROOT) -> int:
    """Always-on correspondence to declarative authoring sources; no copying."""
    root = Path(root)
    value = json.loads((root / "tools/ci/execution-inputs.json").read_bytes())
    registered = locations(root)
    data_sources = {row['source'] for row in value['data']}
    data_targets = {row['copy'] for row in value['data']}
    for row in value['code']:
        if (root / row['source']).exists():
            raise ValueError('Code registration cannot exempt a retained authoring input: ' + row['source'])
    targets = list(registered.values())
    if len(set(targets)) != len(targets):
        raise ValueError('Ambiguous physical input registration')
    expected = {p for p in targets if p.startswith('app/contract_inputs/')} | {'app/contract_inputs/README.md'}
    actual = {p.relative_to(root).as_posix() for p in (root / 'app/contract_inputs').rglob('*')
              if (p.is_file() or p.is_symlink()) and '__pycache__' not in p.parts}
    if actual != expected:
        raise ValueError('Unregistered or missing App input: ' + ', '.join(sorted(actual ^ expected)))
    for row in value['data']:
        if row['copy'] != 'app/contract_inputs/' + row['source'].removeprefix('execution/'):
            raise ValueError('App input does not match its authoring locator')
    def require_registered(name, *, data=False):
        logical = normalize(name)
        if data and ((logical.startswith('execution/') and logical not in data_sources)
                     or (logical.startswith('app/contract_inputs/') and logical not in data_targets)):
            raise ValueError('Consumer requires data registration: ' + name)
        if logical.startswith('execution/') and logical not in registered:
            raise ValueError('Unregistered consumer input: ' + name)
        if logical.startswith('app/contract_inputs/') and logical not in targets:
            raise ValueError('Unregistered consumer copy: ' + name)
    schema = json.loads((root / 'app/src-tauri/schemas/manifest.json').read_bytes())
    for row in [*schema['resources'], *schema.get('file_fixtures', []), *schema['fixture']['sources']]:
        require_registered(row['source'], data=True)
    # Live profile membership, not historical receipt/provenance rows.
    spec = importlib.util.spec_from_file_location('_registered_examination_inputs', root / 'app/examination/repin.py')
    pins = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pins)
    for name in pins.PROFILES:
        profile = json.loads((root / name).read_bytes())
        for _, _, dependency in pins.slots(name, profile):
            require_registered(dependency)
    spec = importlib.util.spec_from_file_location('_documentary_correspondence', root / 'tools/ci/check_documentary_sources.py')
    correspondence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(correspondence)
    project = correspondence.projector(root)
    selections = {}
    for source, selection in correspondence.projections(root):
        require_registered(source, data=True)
        selections.setdefault(source, []).append(selection['selectors'])
    # This current admission profile deliberately selects full documents.
    full = json.loads((root / 'app/examination/admission/sources.current-v1.json').read_bytes())['sources']
    full = {normalize(source) for source in full}
    for row in value['code']:
        target = root / row['path']
        if not target.is_file():
            raise ValueError('Operational source missing: ' + row['path'])
        if row.get('bound') and hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Bound source bytes changed: ' + row['path'])
    def ordinary(name):
        target = root
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


def sync_selected(sources, root=ROOT):
    """Derive explicitly adopted current copies; never refresh consumer profiles.

    The caller must review the source adoption and the resulting diff. Historical
    code identities, documentary selections and examination pins are untouched.
    All selected inputs are checked before any write; linked paths are refused.
    """
    root = Path(root)
    manifest = root / "tools/ci/execution-inputs.json"
    value = json.loads(manifest.read_bytes())
    rows = {row['source']: row for row in value['data']}
    registered = locations(root)
    pending = []
    for source in sources:
        if source not in rows:
            raise ValueError('Not a selected data source: ' + source)
        row = rows[source]
        if registered[source] != row['copy']:
            raise ValueError('Ambiguous selected copy: ' + source)
        paths = []
        for name in (source, row['copy']):
            path = root
            for part in name.split('/'):
                path = path / part
                if path.is_symlink():
                    raise ValueError('Linked source/input refused: ' + name)
            if not path.is_file():
                raise ValueError('Ordinary source/input required: ' + name)
            paths.append(path)
        if hashlib.sha256(paths[1].read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Selected copy already changed: ' + row['copy'])
        pending.append((row, paths[1], paths[0].read_bytes()))
    for row, target, raw in pending:
        target.write_bytes(raw)
        row['sha256'] = hashlib.sha256(raw).hexdigest()
    manifest.write_text(json.dumps(value, indent=2) + '\n')
    return len(pending)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', nargs='+', metavar='SOURCE',
                        help='Derive only these explicitly adopted current data copies')
    args = parser.parse_args()
    if args.sync:
        print(f"{sync_selected(args.sync)} explicitly selected current copies derived; consumer profiles unchanged")
    else:
        print(f"{check()} selected App inputs match their full or declared projection extents")
