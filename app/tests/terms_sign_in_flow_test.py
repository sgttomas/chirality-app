"""Candidate sign-in flow against the flow the retained terms record covers (DEL-01-06 AC-004).

Invented candidate source trees; the retained record and the 0.160.0 schema are copied read-only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('terms_sign_in_flow', ROOT / 'app/packaging/terms/flow.py')
flow = importlib.util.module_from_spec(spec); spec.loader.exec_module(flow)

HOSTING = '''pub const DECLARED_PIN: &str = "{pin}";
    pub(crate) fn account_login_api_key(&self)->Result<SourceRequest,String>{{
        let params=input.into_params();Self::validate_native_result("LoginAccountParams",&params).map_err(|_|"native API-key input shape invalid; sensitive diagnostic withheld".to_string())?;
        let source=self.request_begin_scoped_private("account/login/start",params,json!({{"kind":"person-directed"}}),false,Some(generation),true,None,None)?;
    }}
    pub(crate) fn account_login_oauth(&self)->Result<OAuthLogin,String>{{
        let kind=match mode{{{arms}}};
        let source=self.request_begin_scoped("account/login/start",json!({{"type":kind}}),json!({{"kind":"person-directed"}}),false,Some(generation))?;
        let oauth_mode=if method=="account/login/start" {{None}}else{{None}};
    }}
#[cfg(test)]
#[path = "hosting_tests.rs"]
mod hosting_tests;
#[cfg(test)]
mod tests {{
    fn t(){{ host.request("account/login/start", json!({{"type":"apiKey"}})); }}
}}
'''
ARMS = 'NativeLoginMode::Browser=>"chatgpt",NativeLoginMode::DeviceCode=>"chatgptDeviceCode"'
AUTH = '''    pub(crate) fn into_params(self) -> Value {
        json!({"type":"apiKey","apiKey":self.value})
    }
pub fn generic_guard(method: &str, params: &Value) -> Result<(), String> {
    // A comment naming "account/login/start" is not code.
    if method == "account/login/start"
        && !matches!(
            params["type"].as_str(),
            Some(%s)
        )
    {
        return Err("unsupported".into());
    }
    if matches!(method,"account/login/start"|"account/login/cancel") { return Ok(()); }
}
'''
LOCAL = 'fn start(host:&Host){ host.account_login_api_key_from_native_entry(generation, Some(&policy), || { Ok(None) }); }\n'


class SignInFlow(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.source = self.base / 'candidate'
        self.write_source()
        # The candidate's schema is the baseline schema under an invented pin: same definitions.
        self.schema = self.source / flow.SCHEMA.format(pin='9.9.9')
        self.schema.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / flow.SCHEMA.format(pin='0.160.0'), self.schema)
        for relative in (flow.RETAINED_RECORD, flow.SCHEMA.format(pin='0.160.0')):
            (self.source / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.source / relative)

    def write_source(self, pin='9.9.9', arms=ARMS, allowed='"chatgpt" | "chatgptDeviceCode"', extra=None):
        src = self.source / 'app/src-tauri/src'; src.mkdir(parents=True, exist_ok=True)
        (src / 'hosting.rs').write_text(HOSTING.format(pin=pin, arms=arms))
        (src / 'auth_rpc.rs').write_text(AUTH % allowed)
        (src / 'native_local_provider.rs').write_text(LOCAL)
        (src / 'hosting_tests.rs').write_text('self.request_begin_scoped("account/login/start",json!({"type":"apiKey"}))\n')
        if extra:
            (src / 'extra.rs').write_text(extra)
        elif (src / 'extra.rs').exists():
            (src / 'extra.rs').unlink()

    def edit_schema(self, name, change):
        value = json.loads(self.schema.read_bytes())
        change(value['definitions'][name])
        self.schema.write_text(json.dumps(value))

    def run_flow(self):
        return flow.compare(self.source)

    def test_same_definitions_and_types_are_unchanged(self):
        report = self.run_flow()
        self.assertEqual(report['status'], 'unchanged', report['differences'])
        forms = {(e['file'], e['line']): e['form'] for e in report['candidate']['senders_examined']}
        self.assertEqual(forms, {('hosting.rs', 4): 'API-key sender', ('hosting.rs', 8): 'native sign-in sender',
                                 ('hosting.rs', 9): 'comparison', ('auth_rpc.rs', 6): 'generic route guard',
                                 ('auth_rpc.rs', 14): 'matches! pattern'})
        self.assertEqual(report['candidate']['test_files_not_read'], ['hosting_tests.rs'])
        self.assertTrue(report['rules'])
        self.assertEqual(report['candidate']['account_sign_in_types'], ['chatgpt', 'chatgptDeviceCode'])
        self.assertEqual(report['candidate']['separate_api_key_login']['sent_from'], ['native_local_provider.rs'])
        self.assertNotIn('apiKey', report['candidate']['account_sign_in_types'])
        self.assertEqual(flow.main(['--source-root', str(self.source)]), 0)

    def test_changed_named_definition_is_unresolved(self):
        self.edit_schema('LoginAccountParams', lambda d: d['oneOf'].append({'title': 'Invented', 'type': 'object'}))
        report = self.run_flow()
        self.assertEqual(report['status'], 'unresolved')
        self.assertEqual([d.get('definition') for d in report['differences']], ['LoginAccountParams'])
        self.assertEqual(flow.main(['--source-root', str(self.source)]), 1)

    def test_changed_referenced_definition_is_unresolved(self):
        self.edit_schema('PlanType', lambda d: d['enum'].append('invented'))
        report = self.run_flow()
        self.assertEqual(report['status'], 'unresolved')
        self.assertEqual([d.get('definition') for d in report['differences']], ['PlanType'])
        self.assertTrue(report['named_set_equal'])   # only the closure sees it

    def test_definition_outside_the_flow_does_not_count(self):
        self.edit_schema('ThreadStartParams', lambda d: d.setdefault('properties', {}).update(invented={'type': 'string'}))
        self.assertEqual(self.run_flow()['status'], 'unchanged')

    def test_added_sign_in_type_is_unresolved(self):
        self.write_source(allowed='"chatgpt" | "chatgptDeviceCode" | "chatgptAuthTokens"')
        report = self.run_flow()
        self.assertEqual(report['status'], 'unresolved')
        self.assertIn({'account_sign_in_types': {'baseline': ['chatgpt', 'chatgptDeviceCode'],
                                                 'candidate': ['chatgpt', 'chatgptAuthTokens', 'chatgptDeviceCode']}},
                      report['differences'])
        self.write_source(arms=ARMS + ',NativeLoginMode::Other=>"invented"')
        self.assertEqual(self.run_flow()['status'], 'unresolved')

    # Review probes: each of these once read as unchanged.
    def assertUnaccounted(self, report):
        self.assertEqual(report['status'], 'unresolved')
        self.assertTrue(report['candidate']['unaccounted'], report)

    def test_wildcard_in_generic_route_allowed_types_is_unresolved(self):
        self.write_source(allowed='"chatgpt" | "chatgptDeviceCode" | _')
        self.assertUnaccounted(self.run_flow())

    def test_sender_with_whitespace_before_the_parenthesis_is_unresolved(self):
        for call in ('request_begin_scoped', 'request_begin_scoped_private'):
            with self.subTest(call=call):
                self.write_source(extra='impl Host {\n    fn review_new_login(&self, generation: &Value) -> Result<SourceRequest, String> {\n'
                                  f'        self.{call} ("account/login/start", json!({{"type":"chatgptAuthTokens"}}), json!({{"kind":"person-directed"}}), false, Some(generation))\n'
                                  '    }\n}\n')
                report = self.run_flow()
                self.assertUnaccounted(report)
                self.assertEqual(report['candidate']['unaccounted'][0]['file'], 'extra.rs')

    def test_sender_in_a_nested_module_is_unresolved(self):
        nested = self.source / 'app/src-tauri/src/review_nested'; nested.mkdir()
        (nested / 'mod.rs').write_text('fn f(&self){ self.request_begin_scoped_private("account/login/start", params, x) }\n')
        report = self.run_flow()
        self.assertUnaccounted(report)
        self.assertEqual(report['candidate']['unaccounted'][0]['file'], 'review_nested/mod.rs')

    def test_spelt_differently_stated_form_is_unresolved(self):
        self.write_source(arms=ARMS + ',_=>"chatgpt"')
        self.assertUnaccounted(self.run_flow())

    def test_test_file_named_from_host_code_is_read(self):
        (self.source / 'app/src-tauri/src/hosting_tests.rs').write_text('fn f(){ send("account/login/start"); }\n')
        self.write_source(extra='#[path = "hosting_tests.rs"]\nmod live;\n')
        self.assertUnaccounted(self.run_flow())

    def test_source_outside_the_folder_and_unlexable_source_are_unresolved(self):
        self.write_source(extra='#[path = "../elsewhere.rs"]\nmod outside;\n')
        self.assertUnaccounted(self.run_flow())
        self.write_source(extra='const X: &str = "unterminated;\n')
        self.assertEqual(self.run_flow()['status'], 'unresolved')
        self.write_source(extra='const X: &str = concat!("account/", "login/start");\n')
        self.assertUnaccounted(self.run_flow())

    def test_missing_schema_is_unresolved(self):
        self.schema.unlink()
        report = self.run_flow()
        self.assertEqual(report['status'], 'unresolved')
        self.assertIn('unreadable', report['differences'][0])

    def test_missing_definition_is_unresolved(self):
        value = json.loads(self.schema.read_bytes()); del value['definitions']['LoginAppBrand']
        self.schema.write_text(json.dumps(value))
        self.assertEqual(self.run_flow()['status'], 'unresolved')

    def test_unrecognised_send_site_is_unresolved(self):
        self.write_source(extra='let s=self.request_begin_scoped("account/login/start",json!({"type":"invented"}));\n')
        self.assertEqual(self.run_flow()['status'], 'unresolved')
        self.write_source()
        (self.source / 'app/src-tauri/src/hosting.rs').write_text('pub const DECLARED_PIN: &str = "9.9.9";\n')
        self.assertEqual(self.run_flow()['status'], 'unresolved')

    def test_changed_baseline_inputs_are_unresolved(self):
        baseline = self.source / flow.SCHEMA.format(pin='0.160.0')
        baseline.write_bytes(baseline.read_bytes() + b'\n')
        self.assertEqual(self.run_flow()['status'], 'unresolved')
        shutil.copyfile(ROOT / flow.SCHEMA.format(pin='0.160.0'), baseline)
        (self.source / flow.RETAINED_RECORD).unlink()
        self.assertEqual(self.run_flow()['status'], 'unresolved')

    def test_symbolic_link_input_is_unresolved(self):
        moved = self.base / 'elsewhere.json'; os.replace(self.schema, moved); os.symlink(moved, self.schema)
        self.assertEqual(self.run_flow()['status'], 'unresolved')

    def test_retained_record_is_never_written(self):
        retained = ROOT / 'app/packaging/terms/retained'
        def state():
            return {str(p): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                    for p in sorted(retained.rglob('*')) if p.is_file()}
        before = state()
        flow.compare(ROOT)
        flow.compare(self.source, record_root=ROOT)
        self.assertEqual(state(), before)
        self.assertNotIn('applicability', flow.compare(self.source))   # the owner's statement, never the tool's

    def test_baseline_constants_derive_from_the_recorded_revision(self):
        revision = flow.BASELINE['revision']
        if subprocess.run(['git', '-C', str(ROOT), 'cat-file', '-e', revision + '^{commit}'], capture_output=True).returncode:
            self.skipTest('recorded revision not in this clone\'s history')
        derived = flow.derive(flow.GitRevision(ROOT, revision))
        self.assertEqual(derived['pin'], flow.BASELINE['pin'])
        self.assertEqual(derived['schema_file_sha256'], flow.BASELINE['schema_file_sha256'])
        self.assertEqual(derived['account_sign_in_types'], flow.BASELINE['account_sign_in_types'])


if __name__ == '__main__':
    unittest.main()
