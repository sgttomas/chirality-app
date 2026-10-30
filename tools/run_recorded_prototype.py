#!/usr/bin/env python3
"""Run a hash-recorded deliverable prototype from today's Work/ layout.

A few prototypes keep their pre-rename bytes because those bytes are recorded
identities (the examination support identity and packaged external_trace
examples). This runner checks the recorded hash, then executes the script with
a deliverable's former `Design` path components read as `Work`
(loop/LOOP_INIT.md). The file on disk is never changed.

    python3 tools/run_recorded_prototype.py execution/PKG-09/DEL-09-01/Work/prototype/check_exp.py
    python3 tools/run_recorded_prototype.py execution/PKG-03/DEL-03-03/Work/prototype/observe_map.py --run DIR
"""
import hashlib
import io
from pathlib import Path
import re
import sys
import tokenize

ROOT = Path(__file__).resolve().parents[1]
RECORDED = {
    'execution/PKG-09/DEL-09-01/Work/prototype/check_exp.py':
        'f55ad634a418ceefce4c6fa170d61400f0bee59d9d3521ce410b09b79f8e34ce',
    'execution/PKG-03/DEL-03-03/Work/prototype/observe_map.py':
        'cf7ba7b4d4218d660d53dc89fe48b37c797041b5d6864e3f28adf342e5d193d6',
}
COMPONENT = re.compile(r'''^([rRbBuUfF]*)(["'])Design\2$''')
INNER = re.compile(r'''((?:DEL-[\w*\[\]-]*|\*)/)Design(?=/|["'])''')
LEADING = re.compile(r'''^([rRbBuUfF]*["'])Design/''')


def rewrite(literal):
    literal = COMPONENT.sub(r'\1\2Work\2', literal)
    return LEADING.sub(r'\1Work/', INNER.sub(r'\1Work', literal))


def translate(source):
    """Rewrite string tokens only; comments and code are untouched."""
    lines = source.splitlines(keepends=True)
    edits = [(t.start, t.end, rewrite(t.string))
             for t in tokenize.generate_tokens(io.StringIO(source).readline)
             if t.type == tokenize.STRING and rewrite(t.string) != t.string]
    for (srow, scol), (erow, ecol), new in reversed(edits):
        head, tail = lines[srow - 1][:scol], lines[erow - 1][ecol:]
        lines[srow - 1:erow] = [head + new + tail]
    return ''.join(lines)


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    script = Path(argv[0]).resolve()
    try:
        relative = script.relative_to(ROOT).as_posix()
    except ValueError:
        raise SystemExit('not a recorded prototype: ' + argv[0])
    if relative not in RECORDED:
        raise SystemExit('not a recorded prototype: ' + relative)
    raw = script.read_bytes()
    if hashlib.sha256(raw).hexdigest() != RECORDED[relative]:
        raise SystemExit('recorded prototype bytes changed: ' + relative)
    sys.argv = [str(script), *argv[1:]]
    sys.path.insert(0, str(script.parent))
    code = compile(translate(raw.decode('utf-8')), str(script), 'exec')
    exec(code, {'__name__': '__main__', '__file__': str(script), '__builtins__': __builtins__})


if __name__ == '__main__':
    main(sys.argv[1:])
