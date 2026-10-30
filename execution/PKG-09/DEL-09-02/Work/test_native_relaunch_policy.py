"""macOS B-policy feasibility fixtures; never launch the App or supplier.

These checks establish limits of proposed containment, not execution admission.
All children are short-lived invented fixtures and waited by their creator.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(sys.platform == 'darwin', 'macOS sandbox policy')
class RelaunchPolicy(unittest.TestCase):
    def probe(self, body, deny_fork):
        with tempfile.TemporaryDirectory(prefix='app-B-policy-',
                                         dir='/Users/ryan/dev/chirality-t3/scratch') as temp:
            python = str(Path(sys.executable).resolve())
            policy = '(version 1)(allow default)(deny network*)'
            policy += '(deny file-read* (subpath "/Users/ryan/.codex"))'
            policy += '(deny file-write* (subpath "/Users/ryan/.codex"))'
            policy += '(deny process-exec)'
            policy += '(allow process-exec (literal ' + json.dumps(python) + ') (literal "/usr/bin/true"))'
            if deny_fork:
                policy += '(deny process-fork)'
            result = subprocess.run(
                ['/usr/bin/sandbox-exec', '-p', policy, python, '-c', body],
                env={'PATH': '/usr/bin:/bin', 'HOME': temp, 'CODEX_HOME': temp,
                     'TMPDIR': temp, 'PYTHONDONTWRITEBYTECODE': '1'},
                capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

    def test_fork_denial_also_denies_allowlisted_posix_spawn(self):
        facts = self.probe('''import os,json
facts={}
for name,options in [('plain',{}),('group',{'setpgroup':0}),('session',{'setsid':True})]:
    try:
        pid=os.posix_spawn('/usr/bin/true',['true'],{'PATH':'/usr/bin:/bin'},**options)
    except OSError as error:
        facts[name]={'errno':error.errno}
    else:
        facts[name]={'waitStatus':os.waitpid(pid,0)[1]}
print(json.dumps(facts))
''', deny_fork=True)
        self.assertEqual(facts, {name: {'errno': 1} for name in ('plain', 'group', 'session')})

    def test_allowlist_with_fork_allowed_admits_no_exec_group_escape(self):
        facts = self.probe('''import os,json
parent_group=os.getpgrp()
pid=os.fork()
if pid==0:
    try:
        os.setsid()
        os._exit(0 if os.getpgrp()!=parent_group else 3)
    except BaseException:
        os._exit(4)
_,status=os.waitpid(pid,0)
print(json.dumps({'childExit':os.waitstatus_to_exitcode(status)}))
''', deny_fork=False)
        self.assertEqual(facts, {'childExit': 0})

    def test_allowlist_with_fork_allowed_admits_same_binary_new_session(self):
        facts = self.probe('''import os,sys,json
pid=os.posix_spawn(sys.executable,[sys.executable,'-c',
    'import os; os._exit(0 if os.getsid(0)==os.getpid() else 3)'],
    dict(os.environ),setsid=True)
_,status=os.waitpid(pid,0)
print(json.dumps({'childExit':os.waitstatus_to_exitcode(status)}))
''', deny_fork=False)
        self.assertEqual(facts, {'childExit': 0})


if __name__ == '__main__':
    unittest.main()
