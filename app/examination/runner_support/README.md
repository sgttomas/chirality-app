# Offline interface runner support

This maintained tool supplies partial EXP §8.3 DC-R1–R4 checks against an invented interface
seam in WebKit and Chromium. It observes and aborts page requests outside its
local fixture origin, including a deliberate guard probe. DC-R5 remains
inconclusive: page interception is not whole-process socket observation.
Consequently this tool **never admits a runner** and never emits a canonical
EXP admission record. No App candidate, native journey, human act, shipping
history, supplier qualification or SEAL-2 conclusion follows from its fixture.

Use an already installed Playwright module and cached browsers only:

```sh
node examination/runner_support/runner.mjs NEW_OUTPUT_DIR INSTALLED_PLAYWRIGHT_DIR [CHROMIUM_EXECUTABLE WEBKIT_EXECUTABLE]
node --test tests/group_b_runner_test.mjs
```

Paths are local invocation parameters, not recorded machine identities. No
package install or download is performed. Optional executables select existing
cache files; a mismatched module/browser combination may fail and is not a
qualified dependency combination. The report records the browser API version label and whether overrides were used, plus the Playwright version, fixture
hash and runner hash. Missing engines or module, incompatible protocols and
launch refusals produce blocked reports with a cause. Raw browser diagnostics
are deliberately excluded because they can contain private machine details.

Set `RUNNER_PLAYWRIGHT_DIR`, and optionally `RUNNER_CHROMIUM` and
`RUNNER_WEBKIT`, to run the actual browser integration test. Without the module
selection it reports an explicit skip; the missing-module and guard tests still
run. The integration test uses the same maintained runner path as the CLI.

Each project retains screenshots for the known-pass, deliberately wrong
expectation and missing-target probes, and JSON observations, with relative
paths and SHA-256 hashes. Blocked projects retain JSON observations. Digests are
verified before report publication. Output directories must be new; failures
cannot overwrite earlier evidence. CLI exit 1 means the supported probes ran
but admission remains incomplete; exit 2 means blocked/failed work or an
operational error. Exit 0 is never returned by the CLI.

The report is a support artifact for an examiner to cite and map into the
unchanged EXP result contract. Chromium DC-R1 uses the queried engine identity. WebKit DC-R1 remains
inconclusive because the inspected Playwright implementation returns a module
constant from browser.version(), which cannot identify an overridden engine. DC-R4 covers the captures in this support report. Neither
claims that a canonical EXP record has been authored or admitted. Whole-process
network observation, full definition-check record assembly, independent review
and any candidate/interface seam extension remain separate work. Browser
routing is a guard for this trusted invented fixture, not a general network
sandbox for arbitrary content.
