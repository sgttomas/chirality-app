// Imported for its effect by the presentation tests that run Rust fixtures
// through `cargo test --lib`. It compiles the lib test target once, under its
// own generous limit, before any fixture runs, so each fixture's timeout bounds
// the fixture rather than a cold compile. When the target is already built (CI
// compiles it first) this is a quick freshness check; concurrent test files
// wait on Cargo's build lock. Set CHIRALITY_RUST_PREBUILD=0 to skip it.
import {spawnSync} from 'node:child_process';

const BUILD_TIMEOUT_MS = 45 * 60 * 1000;

if (process.env.CHIRALITY_RUST_PREBUILD !== '0') {
  const result = spawnSync('cargo', ['test', '--offline', '--locked', '--lib', '--no-run'], {
    cwd: new URL('../../src-tauri/', import.meta.url),
    encoding: 'utf8',
    timeout: BUILD_TIMEOUT_MS,
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error || result.status !== 0) {
    throw new Error(`Rust lib test target did not build: ${result.error?.message ?? ''}\n${result.stderr?.slice(-4000) ?? ''}`);
  }
}
