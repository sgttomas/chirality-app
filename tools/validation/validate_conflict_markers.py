#!/usr/bin/env python3
"""Use Git's conflict-marker detection without gating cosmetic whitespace."""

import argparse
import os
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', default='HEAD')
    args = parser.parse_args()
    result = subprocess.run(
        ['git', 'diff', '--no-ext-diff', '--no-color', '--check', args.base, args.head, '--'],
        env={**os.environ, 'LC_ALL': 'C'}, capture_output=True, text=True,
    )
    # Git returns 2 for check findings, including cosmetic whitespace. Other
    # failures must remain failures rather than becoming an empty clean scan.
    if result.returncode not in (0, 2) or result.stderr:
        print(result.stderr or result.stdout or 'Git conflict check failed.')
        return 1
    markers = []
    source_line_follows = False
    for line in result.stdout.splitlines():
        if source_line_follows and line.startswith('+'):
            source_line_follows = False
            continue
        # Whitespace diagnostics emit the offending source line prefixed '+'.
        # Ignore that payload, not diagnostics for valid '+filename' paths.
        source_line_follows = bool(re.search(r':\d+: .*\.$', line)) and not line.endswith(': new blank line at EOF.')
        if re.search(r':\d+: leftover conflict marker$', line):
            markers.append(line)
    if markers:
        print('\n'.join(markers))
        return 1
    print('PASS: no added unresolved conflict markers.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
