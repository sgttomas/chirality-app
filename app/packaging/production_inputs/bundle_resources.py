"""The copy routes a production preparation gives the bundler, readable without preparing.

`prepare.py` builds its plan from `selected()`, and `notices/coverage.py` reads the same function to require that
every mapped resource is named in the notice coverage account. `selected()` starts from the resources of the base
`app/src-tauri/tauri.conf.json`, which the bundler merges with the plan's `--config`, so the plan states every
resource mapping of the effective configuration. Two mappings depend on the preparation's inputs and are added by
`prepare.py` itself: the selected vendor tree at VENDOR_DESTINATION, and an explicitly selected upstream notice
supplement under SUPPLEMENT_DESTINATION.

Only these copy routes are supported: `bundle.resources` in object form, `bundle.icon` (accounted for by the icon
rows) and, in a production plan only, the validated provisioning profile `prepare.py` places through
`bundle.macOS.files`. Any other route the bundler would follow is refused rather than accounted for: a platform or
alternate Tauri configuration beside `tauri.conf.json` (which the bundler merges or reads instead), and any other key
under `bundle` or `bundle.macOS` (for example `bundle.macOS.files` in the base configuration, `bundle.macOS.frameworks`
or `bundle.externalBin`). Frontend assets the build embeds in the executable are not a copy route and are outside
this rule. Executes nothing.
"""
import json
from pathlib import Path
import posixpath
import re

OVERLAYS = ('tauri.attested-reference.conf.json', 'tauri.notices.conf.json')
SQLITE = ('index.json', 'libsqlite3-sys.LICENSE', 'sqlite3-source-header.txt', 'README.md')
SQLITE_DESTINATION = 'third-party-notices/sqlite-preparation/'
FONT_DESTINATION = 'third-party-notices/fonts/'
VENDOR_DESTINATION = 'codex/'
SUPPLEMENT_DESTINATION = 'third-party-notices/upstream/'
SUPPLEMENT_FILES = ('manifest.json', 'LICENSE.md')
# The release's limitations list, byte for byte, as the bundle resource the host reads (DEL-01-06 AC-008).
LIMITATIONS = ('../../docs/RELEASE_LIMITATIONS_4.0.0.md', 'release/LIMITATIONS.md')
# Sources of the two caller-selected mappings, as the account and the plan both name them.
VENDOR_SOURCE = 'selected:vendor-tree/'
SUPPLEMENT_SOURCE = 'selected:upstream-notice-supplement/'
BASE_CONFIG = 'tauri.conf.json'
PROFILE_FILE = 'embedded.provisionprofile'
# Keys of the effective bundle configuration this preparation supports; any other key is an unaccounted route.
BUNDLE_KEYS = {'active', 'targets', 'icon', 'resources', 'macOS'}
MACOS_KEYS = {'minimumSystemVersion', 'signingIdentity', 'files'}
# tauri.conf.json5, Tauri.toml, tauri.<platform>.conf.json[5] and Tauri.<platform>.toml, in any letter case.
ALTERNATE_CONFIG = re.compile(r'^tauri(\.[A-Za-z0-9_-]+)?\.(conf\.json5?|toml)$', re.IGNORECASE)


def _json(path):
    return json.loads(Path(path).read_bytes())


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _add(resources, src, dst, what):
    if src in resources and resources[src] != dst:
        raise ValueError(what + ' resource mapping conflict')
    resources[src] = dst


def merge_patch(target, patch):
    """JSON merge patch (RFC 7386), the way the bundler merges a --config file into the base configuration."""
    if not isinstance(patch, dict):
        return patch
    value = dict(target) if isinstance(target, dict) else {}
    for key, item in patch.items():
        if item is None:
            value.pop(key, None)
        else:
            value[key] = merge_patch(value.get(key), item)
    return value


def check_routes(bundle, *, profile=None):
    """Refuse every copy route of an effective bundle configuration other than resources, icon and the validated profile."""
    _require(isinstance(bundle, dict), 'bundle configuration must be an object')
    unsupported = sorted(set(bundle) - BUNDLE_KEYS)
    _require(not unsupported, 'unsupported bundle configuration (a copy route the notice account does not cover): '
             + ', '.join('bundle.' + k for k in unsupported))
    _require(isinstance(bundle.get('resources', {}), dict), 'bundle.resources must be an object of source to destination')
    macos = bundle.get('macOS', {})
    _require(isinstance(macos, dict), 'bundle.macOS must be an object')
    unsupported = sorted(set(macos) - MACOS_KEYS)
    _require(not unsupported, 'unsupported bundle configuration (a copy route the notice account does not cover): '
             + ', '.join('bundle.macOS.' + k for k in unsupported))
    files = macos.get('files', {})
    _require(files == ({} if profile is None else {PROFILE_FILE: profile}),
             'bundle.macOS.files may only place the validated provisioning profile of a production plan')


def base_bundle(app, load=_json):
    """The base configuration's bundle section, refusing a platform or alternate configuration the bundler would read."""
    src_tauri = Path(app) / 'src-tauri'
    alternates = sorted(p.name for p in src_tauri.iterdir() if p.name != BASE_CONFIG and ALTERNATE_CONFIG.match(p.name))
    _require(not alternates, 'platform or alternate Tauri configuration is not a supported copy route: ' + ', '.join(alternates))
    bundle = load(src_tauri / BASE_CONFIG).get('bundle', {})
    check_routes(bundle)
    return bundle


def selected(app, font_license_paths, load=_json):
    """Source (relative to app/src-tauri) -> bundle destination, for every mapping that is not caller-selected."""
    app = Path(app)
    resources = {}
    for src, dst in base_bundle(app, load).get('resources', {}).items():
        _add(resources, src, dst, 'base configuration')
    for name in OVERLAYS:
        for src, dst in load(app / 'packaging/unsigned' / name)['bundle']['resources'].items():
            _add(resources, src, dst, 'overlay')
    for name in SQLITE:
        _add(resources, '../packaging/sqlite_notice/' + name, SQLITE_DESTINATION + name, 'SQLite')
    _add(resources, *LIMITATIONS, 'limitations')
    # Bundle-visible copies of the frontend font notices.
    _add(resources, '../packaging/font_notice/index.json', FONT_DESTINATION + 'index.json', 'font notice')
    for path in font_license_paths:
        _add(resources, '../' + path.removeprefix('app/'), FONT_DESTINATION + Path(path).name, 'font notice')
    for src, dst in resources.items():
        _require('*' not in src and '*' not in dst, 'glob resource mapping refused')
    destinations = list(resources.values())
    _require(len(destinations) == len(set(destinations)), 'duplicate resource destination (two sources map to one bundle destination)')
    return resources


def repository_source(src):
    """A source relative to app/src-tauri as a repository path (a folder keeps its trailing /)."""
    _require(not src.startswith('/') and '\\' not in src, 'source resource mapping must be repository-relative: ' + src)
    path = posixpath.normpath(posixpath.join('app/src-tauri', src))
    _require(path != '.' and not path.startswith('../') and path != '..', 'source resource mapping escapes the repository: ' + src)
    return path + ('/' if src.endswith('/') else '')


def pairs(resources):
    """Each static mapping as (repository source, destination)."""
    return sorted((repository_source(src), dst) for src, dst in resources.items())
