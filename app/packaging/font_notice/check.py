#!/usr/bin/env python3
"""Check the bundled IBM Plex font notice index; never fetch, build or execute font data."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FORMAT = 'font-notice/2'
FONT_DIR = 'app/src/fonts'
CSS = 'app/src/workspace.css'
HTML = 'app/index.html'
LICENSE_LINK = '<link rel="license" href="/src/fonts/LICENSE-IBM-Plex-OFL.txt" />'
NAME_FIELDS = {'copyright': 0, 'family': 1, 'subfamily': 2, 'version': 5, 'license_url': 14}
WOFF2_TAGS = ['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post', 'cvt ', 'fpgm', 'glyf', 'loca', 'prep',
              'CFF ', 'VORG', 'EBDT', 'EBLC', 'gasp', 'hdmx', 'kern', 'LTSH', 'PCLT', 'VDMX', 'vhea', 'vmtx', 'BASE',
              'GDEF', 'GPOS', 'GSUB', 'EBSC', 'JSTF', 'MATH', 'CBDT', 'CBLC', 'COLR', 'CPAL', 'SVG ', 'sbix', 'acnt',
              'avar', 'bdat', 'bloc', 'bsln', 'cvar', 'fdsc', 'feat', 'fmtx', 'fvar', 'gvar', 'hsty', 'just', 'lcar',
              'mort', 'morx', 'opbd', 'prop', 'trak', 'Zapf', 'Silf', 'Glat', 'Gloc', 'Feat', 'Sill']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'duplicate JSON field: ' + key)
            value[key] = item
        return value
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def exact_file(root, entry):
    path = entry['path']
    require(isinstance(path, str) and PurePosixPath(path).parent == PurePosixPath(FONT_DIR), 'font notice path outside ' + FONT_DIR)
    target = root / path
    require(target.is_file() and not target.is_symlink(), 'font notice input missing or linked: ' + path)
    raw = target.read_bytes()
    require(len(raw) == entry['size_bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256']
            and blob(raw) == entry['git_blob_sha1'], 'font notice bytes differ: ' + path)
    return raw


FAMILIES = ('mono', 'sans', 'serif')
# The @fontsource packages the fonts were taken from; integrities are npm's registry values for these
# exact tarballs (no App lockfile pins them: they are not npm dependencies of the App).
UPSTREAM = {
    'mono': ('@fontsource/ibm-plex-mono', '5.3.0',
             'sha512-eTgnZjZEGk1QtD3ZstF+Vclo2HLAni8YMy34/DxllwZvyz1lR/1RF/xTiAquOBO7MvqBx8D2Ig2WCPMVfdZu7Q=='),
    'sans': ('@fontsource/ibm-plex-sans', '5.3.0',
             'sha512-CbE4CbbEEZJX860XyUiRpsksXIQR8Rp2XDva2VO53NJox9tVNtusrysd2x5YkUEY3ErQ66W1IiiQL8/wihhw5w=='),
    'serif': ('@fontsource/ibm-plex-serif', '5.3.0',
              'sha512-zwPfHB7EJbS5B8qnitPigJYzNdnt6PUeaoOA1gAAt//1pjpTVZN5sOU14NIAZ+C1xypL6GWsUG2VMYJW9bhJqQ=='),
}
# The Sans text keeps its name: the frontend entry links it.
LICENSE_NAMES = {'mono': 'LICENSE-IBM-Plex-Mono-OFL.txt', 'sans': 'LICENSE-IBM-Plex-OFL.txt', 'serif': 'LICENSE-IBM-Plex-Serif-OFL.txt'}
SCOPE = ('IBM Plex WOFF2 files bundled by the App frontend from app/src/fonts and the OFL text of each family; exact bytes, '
         'their @fontsource tarball members and the fonts\' own name-table declarations, not a legal conclusion')
LIMITS = [
    "Each family's licence text is the LICENSE its @fontsource 5.3.0 tarball carries; its header names that family's IBM copyright",
    'No Reserved Font Name appears in the shipped name tables or licence texts; this records strings, not a licensing determination',
    'The frontend build also embeds these fonts and the Sans licence in the App executable; this index is the bundle-visible notice copy',
    'Not release approval or legal advice',
]
FILE_FIELDS = {'path', 'size_bytes', 'sha256', 'git_blob_sha1'}


def family(path):
    name = PurePosixPath(path).name
    found = [f for f in FAMILIES if name.startswith('ibm-plex-' + f + '-')]
    require(len(found) == 1, 'font file names no known family: ' + name)
    return found[0]


def check(root=ROOT):
    root = Path(root)
    index = load(root / 'app/packaging/font_notice/index.json')
    require(set(index) == {'format', 'scope', 'source', 'upstream_packages', 'licenses', 'fonts', 'copyright_notices', 'limits'}
            and index['format'] == FORMAT, 'unknown font notice index shape')
    source = index['source']
    require(set(source) == {'repository', 'revision', 'path', 'added_by_commit', 'declared_upstream', 'declared_upstream_verified',
                            'upstream_evidence'}
            and re.fullmatch('[0-9a-f]{40}', source['revision']) and re.fullmatch('[0-9a-f]{40}', source['added_by_commit'])
            and type(source['declared_upstream_verified']) is bool, 'font source provenance differs')
    verified = source['declared_upstream_verified']
    packages = index['upstream_packages']
    require(packages == ([{'family': f, 'package': p, 'version': v, 'integrity': i} for f, (p, v, i) in sorted(UPSTREAM.items())]
                         if verified else []), 'upstream package list differs from the pinned @fontsource tarballs')
    by_family = {p['family']: p for p in packages}
    def upstream(entry, member):
        if not verified:
            require('upstream' not in entry, 'upstream evidence without a verified claim')
            return
        require(entry.get('upstream') == {'package': by_family[entry['family']]['package'], 'member': member},
                'upstream evidence differs: ' + entry['path'])
    licenses = index['licenses']
    require(isinstance(licenses, list) and [l.get('family') for l in licenses] == sorted({family(f['path']) for f in index['fonts']}),
            'one licence text per bundled font family required')
    for license in licenses:
        require(set(license) - {'upstream'} == FILE_FIELDS | {'family', 'title', 'header_copyright'}
                and license['path'] == FONT_DIR + '/' + LICENSE_NAMES[license['family']], 'unknown license fields')
        text = exact_file(root, license).decode('utf-8')
        require(text.splitlines()[0] == license['header_copyright'] and text.count(license['title']) == 1, 'license header/title differs')
        upstream(license, 'package/LICENSE')
    fonts = index['fonts']
    require(isinstance(fonts, list) and fonts, 'no indexed fonts')
    for font in fonts:
        require(set(font) - {'upstream'} == FILE_FIELDS | {'family', 'name_table'} and font['family'] == family(font['path'])
                and set(font['name_table']) == set(NAME_FIELDS) and font['path'].endswith('.woff2'), 'unknown font fields')
        exact_file(root, font)
        upstream(font, 'package/files/' + PurePosixPath(font['path']).name)
    names = [PurePosixPath(f['path']).name for f in fonts]
    require(len(set(names)) == len(names) and names == sorted(names), 'duplicate or unordered font entries')
    present = {p.name for p in (root / FONT_DIR).iterdir()}
    require(present == set(names) | {PurePosixPath(l['path']).name for l in licenses}, 'unindexed or missing file in ' + FONT_DIR)
    require(index['copyright_notices'] == sorted({f['name_table']['copyright'] for f in fonts}), 'copyright notice list differs')
    check_frontend_sources(root, names)
    return index


def tarball(npm_cache, integrity):
    """Read one cached tarball by integrity (npm's content-addressed cache); read-only, no fallback."""
    import base64
    digest = base64.b64decode(integrity.split('-', 1)[1], validate=True)
    require(integrity.startswith('sha512-'), 'unsupported integrity')
    raw = (Path(npm_cache) / '_cacache/content-v2/sha512' / digest.hex()[:2] / digest.hex()[2:4] / digest.hex()[4:]).read_bytes()
    require(hashlib.sha512(raw).digest() == digest, 'cached tarball differs from its integrity')
    return raw


def members(raw):
    import io, tarfile
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        return {m.name: archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}


def check_upstream(index, npm_cache, root=ROOT):
    """Compare every font and licence byte for byte with its member of the pinned tarball."""
    require(index['source']['declared_upstream_verified'], 'no upstream claim to verify')
    trees = {p['package']: members(tarball(npm_cache, p['integrity'])) for p in index['upstream_packages']}
    count = 0
    for entry in index['licenses'] + index['fonts']:
        require(trees[entry['upstream']['package']].get(entry['upstream']['member']) == (Path(root) / entry['path']).read_bytes(),
                'shipped bytes differ from the tarball member: ' + entry['path'])
        count += 1
    return count


def generate(npm_cache, root=ROOT):
    """Write the per-family licence texts from the tarballs and return the index with its upstream evidence."""
    root = Path(root)
    index = load(root / 'app/packaging/font_notice/index.json')
    trees = {f: members(tarball(npm_cache, i)) for f, (_, _, i) in UPSTREAM.items()}
    def file_entry(path, raw):
        return {'path': path, 'size_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'git_blob_sha1': blob(raw)}
    fonts = []
    for font in index['fonts']:
        name, fam = PurePosixPath(font['path']).name, family(font['path'])
        raw = (root / font['path']).read_bytes()
        require(trees[fam].get('package/files/' + name) == raw, 'font differs from its tarball member: ' + name)
        fonts.append({**file_entry(font['path'], raw), 'family': fam, 'name_table': font['name_table'],
                      'upstream': {'package': UPSTREAM[fam][0], 'member': 'package/files/' + name}})
    licenses = []
    for fam in sorted({f['family'] for f in fonts}):
        raw = trees[fam]['package/LICENSE']
        path = FONT_DIR + '/' + LICENSE_NAMES[fam]
        target = root / path
        if not target.exists() or target.read_bytes() != raw:
            target.write_bytes(raw)
        text = raw.decode('utf-8')
        licenses.append({**file_entry(path, raw), 'family': fam, 'title': 'SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',
                         'header_copyright': text.splitlines()[0], 'upstream': {'package': UPSTREAM[fam][0], 'member': 'package/LICENSE'}})
    source = {k: index['source'][k] for k in ('repository', 'revision', 'path', 'added_by_commit', 'declared_upstream')}
    source.update(declared_upstream_verified=True, upstream_evidence=(
        'Each font file and each licence text equals, byte for byte, the named member of the named @fontsource 5.3.0 '
        'tarball; each tarball was read from a local npm cache and its SHA-512 equals the pinned integrity. '
        'Recheck with --npm-cache.'))
    return {'format': FORMAT, 'scope': SCOPE, 'source': source,
            'upstream_packages': [{'family': f, 'package': p, 'version': v, 'integrity': i} for f, (p, v, i) in sorted(UPSTREAM.items())],
            'licenses': licenses, 'fonts': fonts, 'copyright_notices': index['copyright_notices'], 'limits': LIMITS}


FONT_REFERENCE = re.compile(r'@font-face|\bFontFace\s*\(|\.(?:woff2?|ttf|otf|eot)\b', re.IGNORECASE)
SOURCE_SUFFIXES = {'.css', '.html', '.js', '.jsx', '.mjs', '.ts', '.tsx'}


def strip_comments(text, html=False):
    text = re.sub(r'/\*.*?\*/', ' ', text, flags=re.DOTALL)
    return re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL) if html else text


def check_frontend_sources(root, names):
    """Lexical scope check (not a CSS engine): only workspace.css may declare fonts, exactly the indexed set."""
    css = strip_comments((root / CSS).read_text())
    faces = re.findall(r'@font-face\s*\{([^}]*)\}', css, flags=re.IGNORECASE)
    require(len(faces) == len(re.findall(r'@font-face', css, flags=re.IGNORECASE)), 'unparsed @font-face rule refused')
    used = [u.strip() for face in faces for u in re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', face, flags=re.IGNORECASE)]
    require(sorted(used) == sorted('./fonts/' + n for n in names), 'frontend @font-face sources differ from indexed fonts')
    outside = re.sub(r'@font-face\s*\{[^}]*\}', ' ', css, flags=re.IGNORECASE)
    require(not FONT_REFERENCE.search(outside) and not re.search(r'@import', outside, flags=re.IGNORECASE),
            'font reference or import outside indexed @font-face rules refused')
    for path in sorted([root / HTML, *(root / 'app/src').rglob('*')]):
        relative = path.relative_to(root).as_posix()
        if relative == CSS or relative.startswith(FONT_DIR + '/') or path.suffix not in SOURCE_SUFFIXES or not path.is_file():
            continue
        text = path.read_text()
        text = strip_comments(text, html=path.suffix == '.html') if path.suffix in ('.css', '.html') else text
        require(not FONT_REFERENCE.search(text), 'font source outside ' + CSS + ' refused: ' + relative)
    html = strip_comments((root / HTML).read_text(), html=True)
    require(html.count(LICENSE_LINK) == 1, 'frontend entry no longer links the retained font license')


def brotli_decompress(data):
    node = shutil.which('node')
    require(node is not None, 'name-table check needs node (built-in zlib brotli); no fallback')
    script = "process.stdout.write(require('zlib').brotliDecompressSync(require('fs').readFileSync(0)))"
    return subprocess.run([node, '-e', script], input=data, capture_output=True, check=True).stdout


def base128(data, i):
    value = 0
    for n in range(5):
        byte = data[i]; i += 1
        require(not (n == 0 and byte == 0x80) and not value & 0xFE000000, 'invalid WOFF2 length')
        value = (value << 7) | (byte & 0x7f)
        if not byte & 0x80:
            return value, i
    raise ValueError('invalid WOFF2 length')


def name_table(raw):
    """Read selected Windows-English name records from an untransformed WOFF2 name table."""
    require(len(raw) >= 48, 'truncated WOFF2')
    signature, _, length, count = struct.unpack('>4sIIH', raw[:14])
    compressed = struct.unpack('>I', raw[20:24])[0]
    require(signature == b'wOF2' and length == len(raw), 'not a complete WOFF2 file')
    i, tables = 48, []
    for _ in range(count):
        flags = raw[i]; i += 1
        tag = raw[i:i + 4].decode('latin-1') if flags & 0x3f == 63 else WOFF2_TAGS[flags & 0x3f]
        i += 4 if flags & 0x3f == 63 else 0
        original, i = base128(raw, i)
        transformed = (flags >> 6 == 0) if tag in ('glyf', 'loca') else (flags >> 6 != 0)
        stored = original
        if transformed:
            stored, i = base128(raw, i)
        tables.append((tag, original, stored, transformed))
    stream = brotli_decompress(raw[i:i + compressed])
    offset = 0
    for tag, original, stored, transformed in tables:
        if tag == 'name':
            require(not transformed, 'transformed name table refused')
            table = stream[offset:offset + original]
            break
        offset += stored
    else:
        raise ValueError('WOFF2 has no name table')
    _, records, strings = struct.unpack('>HHH', table[:6])
    found = {}
    for r in range(records):
        platform, _, language, name_id, size, start = struct.unpack('>HHHHHH', table[6 + 12 * r:18 + 12 * r])
        if platform == 3 and language == 0x409:
            found[name_id] = table[strings + start:strings + start + size].decode('utf-16-be')
    return {field: found.get(number) for field, number in NAME_FIELDS.items()}


def check_name_tables(index, root=ROOT):
    for font in index['fonts']:
        require(name_table((Path(root) / font['path']).read_bytes()) == font['name_table'],
                'font name-table declaration differs: ' + font['path'])
    return len(index['fonts'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name-tables', action='store_true', help='Also decode each WOFF2 name table (needs node)')
    parser.add_argument('--npm-cache', type=Path, help='Also compare every file with its member of the pinned tarball')
    parser.add_argument('--generate', action='store_true', help='With --npm-cache: rewrite index.json and the licence texts')
    args = parser.parse_args()
    try:
        if args.generate:
            require(args.npm_cache is not None, '--generate needs --npm-cache')
            (ROOT / 'app/packaging/font_notice/index.json').write_text(json.dumps(generate(args.npm_cache), indent=2) + '\n')
        index = check()
        decoded = check_name_tables(index) if args.name_tables else 0
        upstream = check_upstream(index, args.npm_cache) if args.npm_cache else 0
        print(json.dumps({'font_notice_match': True, 'fonts': len(index['fonts']), 'licenses': len(index['licenses']),
                          'name_tables_checked': decoded, 'upstream_members_checked': upstream,
                          'copyright_notices': index['copyright_notices'],
                          'index_records_upstream_verified': index['source']['declared_upstream_verified'],
                          'upstream_rechecked_now': bool(upstream),
                          'standing': 'notice preparation only; no built candidate, legal determination or release approval'}))
        return 0
    except (ValueError, KeyError, TypeError, OSError, UnicodeDecodeError, struct.error, IndexError,
            subprocess.CalledProcessError) as error:
        print(json.dumps({'font_notice_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
