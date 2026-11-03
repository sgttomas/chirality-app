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
FORMAT = 'font-notice/1'
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


def check(root=ROOT):
    root = Path(root)
    index = load(root / 'app/packaging/font_notice/index.json')
    require(set(index) == {'format', 'scope', 'source', 'license', 'fonts', 'copyright_notices', 'limits'}
            and index['format'] == FORMAT, 'unknown font notice index shape')
    source = index['source']
    require(set(source) == {'repository', 'revision', 'path', 'added_by_commit', 'declared_upstream', 'declared_upstream_verified'}
            and re.fullmatch('[0-9a-f]{40}', source['revision']) and re.fullmatch('[0-9a-f]{40}', source['added_by_commit'])
            and source['declared_upstream_verified'] is False, 'font source provenance differs')
    license = index['license']
    require(set(license) == {'path', 'size_bytes', 'sha256', 'git_blob_sha1', 'title', 'header_copyright'}, 'unknown license fields')
    text = exact_file(root, license).decode('utf-8')
    require(text.splitlines()[0] == license['header_copyright'] and text.count(license['title']) == 1, 'license header/title differs')
    fonts = index['fonts']
    require(isinstance(fonts, list) and fonts, 'no indexed fonts')
    for font in fonts:
        require(set(font) == {'path', 'size_bytes', 'sha256', 'git_blob_sha1', 'name_table'}
                and set(font['name_table']) == set(NAME_FIELDS) and font['path'].endswith('.woff2'), 'unknown font fields')
        exact_file(root, font)
    names = [PurePosixPath(f['path']).name for f in fonts]
    require(len(set(names)) == len(names) and names == sorted(names), 'duplicate or unordered font entries')
    present = {p.name for p in (root / FONT_DIR).iterdir()}
    require(present == set(names) | {PurePosixPath(license['path']).name}, 'unindexed or missing file in ' + FONT_DIR)
    require(index['copyright_notices'] == sorted({f['name_table']['copyright'] for f in fonts}), 'copyright notice list differs')
    css = (root / CSS).read_text()
    faces = re.findall(r'@font-face\s*\{[^}]*\}', css)
    used = [m for face in faces for m in re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', face)]
    require(sorted(used) == sorted('./fonts/' + n for n in names), 'frontend @font-face sources differ from indexed fonts')
    require(not re.search(r'@import[^;]*fonts\.|https?://[^)"\']*\.(woff2?|ttf|otf)', css), 'remote or imported font source refused')
    require(LICENSE_LINK in (root / HTML).read_text(), 'frontend entry no longer links the retained font license')
    return index


def brotli_decompress(data):
    node = shutil.which('node')
    require(node is not None, 'name-table check needs node (built-in zlib brotli); no fallback')
    script = "process.stdout.write(require('zlib').brotliDecompressSync(require('fs').readFileSync(0)))"
    return subprocess.run([node, '-e', script], input=data, capture_output=True, check=True).stdout


def base128(data, i):
    value = 0
    for n in range(5):
        byte = data[i]; i += 1
        require(not (n == 0 and byte == 0x80), 'invalid WOFF2 length')
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
    args = parser.parse_args()
    try:
        index = check()
        decoded = check_name_tables(index) if args.name_tables else 0
        print(json.dumps({'font_notice_match': True, 'fonts': len(index['fonts']), 'name_tables_checked': decoded,
                          'copyright_notices': index['copyright_notices'], 'declared_upstream_verified': False,
                          'standing': 'notice preparation only; no built candidate, legal determination or release approval'}))
        return 0
    except (ValueError, KeyError, TypeError, OSError, UnicodeDecodeError, struct.error, IndexError,
            subprocess.CalledProcessError) as error:
        print(json.dumps({'font_notice_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
