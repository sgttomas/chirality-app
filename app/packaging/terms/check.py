"""Opt-in terms-position/v1 consistency reader. Never grants release authority."""
import argparse
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / 'execution/PKG-01/DEL-01-06/Work/terms-position-v1/schema.json'
MAX_BYTES = 2 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON field: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Evidence:
    """Bounded no-follow reads in a caller-selected stable evidence directory."""
    def __init__(self, root):
        self.root = Path(os.path.abspath(root))
        for path in (self.root, *self.root.parents):
            require(not path.is_symlink(), 'evidence root has symlink ancestry')
        self.seen = {}

    def read(self, relative):
        path = PurePosixPath(relative)
        require(relative and not path.is_absolute() and '\\' not in relative
                and all(p not in ('', '.', '..') for p in relative.split('/')),
                'evidence path must be contained, canonical and relative')
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
        fd = os.open(self.root, flags | os.O_DIRECTORY)
        try:
            for part in path.parts[:-1]:
                child = os.open(part, flags | os.O_DIRECTORY, dir_fd=fd)
                os.close(fd)
                fd = child
            leaf = os.open(path.name, flags, dir_fd=fd)
            try:
                before = os.fstat(leaf)
                require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                        'evidence must be an ordinary unlinked regular file')
                require(before.st_size <= MAX_BYTES, 'evidence exceeds size bound')
                chunks = []
                size = 0
                while chunk := os.read(leaf, min(65536, MAX_BYTES + 1 - size)):
                    chunks.append(chunk)
                    size += len(chunk)
                    require(size <= MAX_BYTES, 'evidence exceeds size bound')
                after = os.fstat(leaf)
                require((before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                        == (after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                        'evidence changed while reading')
                raw = b''.join(chunks)
            finally:
                os.close(leaf)
        finally:
            os.close(fd)
        sha = digest(raw)
        require(relative not in self.seen or self.seen[relative] == sha,
                'evidence changed during check')
        self.seen[relative] = sha
        return raw

    def artifact(self, reference):
        raw = self.read(reference['path'])
        require(digest(raw) == reference['sha256'], 'artifact digest mismatch')
        return raw

    def recheck(self):
        for path in list(self.seen):
            self.read(path)


def actor(value):
    normalized = value.strip().casefold()
    require(bool(normalized), 'empty actor')
    return normalized


def validate(value, schema, kind=None):
    selected = schema if kind is None else {'$ref': '#/$defs/' + kind, '$defs': schema['$defs']}
    Draft202012Validator(selected, format_checker=FormatChecker()).validate(value)


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def check_capture(position, evidence, schema):
    capture = parse(evidence.artifact(position['content']))
    validate(capture, schema, 'publication_capture' if position['kind'] == 'official_publication' else 'response_capture')
    require(capture['supplier'] == position['supplier'], 'capture supplier mismatch')
    require(capture['sha256'] == position['full_content_sha256'], 'source content digest mismatch')
    if position['kind'] == 'official_publication':
        require('response_text' not in capture, 'reply cannot be relabelled as publication')
        require(capture['requested_url'] == position['source_url'], 'publication URL mismatch')
        require(capture['retrieved_at'] == position['retrieved_or_received_at'], 'retrieval date mismatch')
        require(capture['publication_date'] == position['publication_or_response_date'], 'publication date mismatch')
        require(capture['capture_actor'] == position['captured_by'], 'capture actor mismatch')
        require(bool(capture['excerpts']), 'missing retained publication content')
        for excerpt in capture['excerpts']:
            require(digest(excerpt['html'].encode()) == excerpt['html_sha256'], 'excerpt digest mismatch')
            parser = Text()
            parser.feed(excerpt['html'])
            require(''.join(parser.parts) == excerpt['text'], 'excerpt text mismatch')
    else:
        require(capture['format'] == 'chirality.supplier-response-capture/v1', 'unknown response capture')
        require(capture['source_url'] == position['source_url'], 'response source mismatch')
        require(capture['received_at'] == position['retrieved_or_received_at'], 'receipt date mismatch')
        require(capture['response_date'] == position['publication_or_response_date'], 'response date mismatch')
        require(capture['captured_by'] == position['captured_by'], 'capture actor mismatch')
        require(digest(capture['response_text'].encode()) == capture['sha256'], 'response content mismatch')
    return capture


def owner_answer(evidence, reference, timestamp, schema):
    answer = parse(evidence.artifact(reference))
    validate(answer, schema, 'owner_answer')
    require(answer['format'] == 'chirality.terms-owner-answer/v1'
            and answer['created_by'] == 'user', 'not a recorded owner answer')
    require(answer['recorded_timestamp'] == timestamp, 'owner event timestamp mismatch')
    require(bool(answer['message_id']) and bool(answer['thread']), 'owner event locator missing')
    return answer


def check(record_path, evidence_root):
    schema = parse(SCHEMA.read_bytes())
    evidence = Evidence(evidence_root)
    raw = evidence.read(record_path)
    record = parse(raw)
    validate(record, schema)
    recorder = actor(record['recorded_by'])
    supplier = actor(record['supplier'])
    require(recorder != supplier, 'supplier cannot be the packaging recorder')
    position = record['position']
    approval = None
    applicability_answer = None
    if position is not None:
        require(position['supplier'] == record['supplier'], 'position supplier mismatch')
        require(actor(position['captured_by']) != supplier, 'supplier authorship is not capture')
        check_capture(position, evidence, schema)
    owner = record['owner_disposition']
    if owner is not None:
        require(actor(owner['actor']) not in {recorder, supplier},
                'owner applicability must remain distinct from recorder/supplier')
        approval = parse(evidence.artifact(owner['approval']))
        validate(approval, schema, 'approval')
        for key in ('supplier', 'scope'):
            require(approval[key] == record[key], 'approval ' + key + ' mismatch')
        for key in ('content', 'full_content_sha256', 'conditions', 'exclusions'):
            require(approval[key] == position[key], 'approval ' + key + ' mismatch')
        require(approval['source_kind'] == position['kind'], 'approval source kind mismatch')
        require(approval['actor'] == owner['actor'] and approval['act'] == owner['act'], 'owner act mismatch')
        proposal = approval['approved_proposal']
        evidence.artifact(proposal['artifact'])
        answer = owner_answer(evidence, approval['owner_answer'], approval['decided_at'], schema)
        applicability_answer = answer
        require(answer['content'].endswith('\n' + approval['answer']), 'owner answer mismatch')
        require(proposal['revision'] in answer['content'], 'approved revision absent from question')
        require(datetime.fromisoformat(approval['decided_at'].replace('Z', '+00:00'))
                >= datetime.fromisoformat(position['retrieved_or_received_at'].replace('Z', '+00:00')),
                'owner adoption predates evidence capture')
    decision = record['distribution_decision']
    if decision != 'not_made':
        require(actor(decision['actor']) not in {recorder, supplier}, 'recorder/supplier cannot decide release')
        release = parse(evidence.artifact(decision['evidence']))
        validate(release, schema, 'release')
        require(release['actor'] == decision['actor'] and release['scope'] == record['scope'], 'release subject mismatch')
        release_answer = owner_answer(evidence, release['owner_answer'], release['decided_at'], schema)
        require(release_answer['content'].endswith('\n' + release['answer']), 'release answer mismatch')
        if approval:
            require(release['actor'] == approval['actor'], 'release owner differs from applicability owner')
            require((release_answer['thread'], release_answer['message_id'])
                    != (applicability_answer['thread'], applicability_answer['message_id']),
                    'applicability answer is not release approval')
    evidence.recheck()
    return {'format': 'chirality.terms-position-check/v1', 'record_sha256': digest(raw),
            'recorded_state': record['state'], 'source_kind': position['kind'] if position else None,
            'distribution_decision_recorded': decision != 'not_made',
            'release_authorized': False, 'artifacts': evidence.seen,
            'standing': 'retained evidence and value consistency only; no authentication of actors, legal judgment or release authority'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', required=True, help='Path relative to the explicit evidence root')
    parser.add_argument('--evidence-root', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.record, args.evidence_root), indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, ValidationError) as error:
        print(json.dumps({'standing': 'refused', 'error': str(error), 'release_authorized': False}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
