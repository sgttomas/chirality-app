"""The runner executes only hash-recorded prototypes and rewrites only path strings."""
import hashlib
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_recorded_prototype as subject  # noqa: E402


@pytest.mark.parametrize('relative, changed', [
    ('execution/PKG-09/DEL-09-01/Work/prototype/check_exp.py', 3),
    ('execution/PKG-03/DEL-03-03/Work/prototype/observe_map.py', 5),
])
def test_recorded_bytes_and_only_design_path_strings_change(relative, changed):
    raw = (subject.ROOT / relative).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == subject.RECORDED[relative]
    before = raw.decode().splitlines()
    after = subject.translate(raw.decode()).splitlines()
    differing = [(a, b) for a, b in zip(before, after) if a != b]
    assert len(before) == len(after) and len(differing) == changed
    assert all(a.replace('Design', 'Work') == b for a, b in differing)


def test_rewrite_handles_components_globs_and_leading_paths_only():
    assert subject.rewrite('"Design"') == '"Work"'
    assert subject.rewrite("'PKG-04/DEL-04-03/Design/prototype'") == "'PKG-04/DEL-04-03/Work/prototype'"
    assert subject.rewrite('"Design/x.md"') == '"Work/x.md"'
    for unchanged in ('"Design notes"', '"app/Design/x"', '"DESIGN"', '"Designs"'):
        assert subject.rewrite(unchanged) == unchanged


def test_unrecorded_or_changed_scripts_are_refused(tmp_path, monkeypatch):
    runner = Path(subject.__file__)
    refused = subprocess.run([sys.executable, str(runner), str(runner)], capture_output=True, text=True)
    assert refused.returncode != 0 and 'not a recorded prototype' in refused.stderr
    relative = 'execution/PKG-09/DEL-09-01/Work/prototype/check_exp.py'
    monkeypatch.setitem(subject.RECORDED, relative, '0' * 64)
    with pytest.raises(SystemExit, match='recorded prototype bytes changed'):
        subject.main([str(subject.ROOT / relative)])
