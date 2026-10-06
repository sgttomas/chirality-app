import ast,json,pathlib,tempfile,tomllib,unittest
from witness_common import sha,save
from parent_launch import create_codex_homes,validate_compiled
HERE=pathlib.Path(__file__).resolve().parent
BUILT=pathlib.Path('/private/tmp/chirality-wf-bound-compile-dxb5u0js')
ROOT=pathlib.Path(tempfile.mkdtemp(prefix='chirality-wf-final-controls-',dir='/private/tmp')).resolve()
def parsed_config(path):
    tree=ast.parse(path.read_text());node=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='config' for t in n.targets))
    class Port(ast.NodeTransformer):
        def visit_FormattedValue(self,node):return ast.Constant(value='12345')
    expression=ast.fix_missing_locations(ast.Expression(Port().visit(node)))
    return tomllib.loads(eval(compile(expression,str(path),'eval'),{'__builtins__':{}}))
class Tests(unittest.TestCase):
    def test_actual_mktemp_moves_preserve_identity(self):
        root=ROOT/'homes';root.mkdir();records=create_codex_homes(root)
        self.assertEqual(len(records),2)
        for record in records:
            self.assertEqual(record['command'][:2],['/usr/bin/mktemp','-d']);self.assertEqual(record['returncode'],0)
            target=pathlib.Path(record['usedAt']);self.assertEqual((target.stat().st_dev,target.stat().st_ino),(record['device'],record['inode']))
            self.assertFalse(pathlib.Path(record['movedFrom']).exists());self.assertEqual(record['mode'],'0o700');self.assertFalse(any(target.iterdir()))
        with self.assertRaisesRegex(ValueError,'already exists'):create_codex_homes(root)
    def test_file_store_explicit_original_negative(self):
        old=parsed_config(HERE/'parent-final-preimage/parent_launch.py');new=parsed_config(HERE/'parent_launch.py')
        self.assertNotIn('cli_auth_credentials_store',old);self.assertEqual(new.pop('cli_auth_credentials_store'),'file');self.assertEqual(new,old)
    def test_old_binding_refuses_new_launcher(self):
        with self.assertRaisesRegex(ValueError,'launcher/helper differs'):validate_compiled(BUILT/'compiled-binding.json')
    def test_successor_binds_unchanged_binary_and_rust(self):
        before=json.loads((BUILT/'compiled-binding.json').read_text());after,binary=validate_compiled(BUILT/'launcher-successor-binding.json')
        self.assertEqual(before['executableSha256'],sha(binary));self.assertEqual(before['injectedSources'],after['injectedSources']);self.assertEqual(before['fixtureSha256'],after['fixtureSha256'])
        self.assertNotEqual(sha(BUILT/'compiled-binding.json'),sha(BUILT/'launcher-successor-binding.json'))
    def test_successor_rejects_unrelated_change(self):
        data=json.loads((BUILT/'launcher-successor-binding.json').read_text());data['resolvedCandidate']='invented'
        path=BUILT/'negative-successor-control.json';save(path,data)
        try:
            with self.assertRaisesRegex(ValueError,'changes more'):validate_compiled(path)
        finally:path.unlink()
if __name__=='__main__':print('SYNTHETIC_ROOT='+str(ROOT),flush=True);unittest.main(verbosity=2)
