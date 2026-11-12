"""The resource mappings a production preparation selects from a source tree, readable without preparing.

`prepare.py` builds its plan from `selected()`, and `notices/coverage.py` reads the same function to require that
every mapped resource is named in the notice coverage account. Two mappings depend on the preparation's inputs and
are added by `prepare.py` itself: the selected vendor tree at VENDOR_DESTINATION, and an explicitly selected
upstream notice supplement under SUPPLEMENT_DESTINATION. Executes nothing.
"""
import json
from pathlib import Path

OVERLAYS = ('tauri.attested-reference.conf.json', 'tauri.notices.conf.json')
SQLITE = ('index.json', 'libsqlite3-sys.LICENSE', 'sqlite3-source-header.txt', 'README.md')
SQLITE_DESTINATION = 'third-party-notices/sqlite-preparation/'
FONT_DESTINATION = 'third-party-notices/fonts/'
VENDOR_DESTINATION = 'codex/'
SUPPLEMENT_DESTINATION = 'third-party-notices/upstream/'


def _json(path):
    return json.loads(Path(path).read_bytes())


def _add(resources, src, dst, what):
    if src in resources and resources[src] != dst:
        raise ValueError(what + ' resource mapping conflict')
    resources[src] = dst


def selected(app, font_license_paths, load=_json):
    """Source (relative to app/src-tauri) -> bundle destination, for every mapping that is not caller-selected."""
    app = Path(app)
    resources = {}
    for name in OVERLAYS:
        for src, dst in load(app / 'packaging/unsigned' / name)['bundle']['resources'].items():
            _add(resources, src, dst, 'overlay')
    for name in SQLITE:
        _add(resources, '../packaging/sqlite_notice/' + name, SQLITE_DESTINATION + name, 'SQLite')
    # Bundle-visible copies of the frontend font notices.
    _add(resources, '../packaging/font_notice/index.json', FONT_DESTINATION + 'index.json', 'font notice')
    for path in font_license_paths:
        _add(resources, '../' + path.removeprefix('app/'), FONT_DESTINATION + Path(path).name, 'font notice')
    return resources
