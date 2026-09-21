// Fake `chirality-runtime-service` used by runtime-service-host.test.ts.
//
// Speaks the `chirality-app-owned/v1` contract from the App's side: it reads
// the config path from `daemon --config <path>`, prints exactly one ready line
// `{"ready":true,"role":"daemon","socketPath":"...","clientTokenFile":"..."}`
// and stays alive until SIGTERM. Behaviour switches come from the environment
// so one script covers every lifecycle branch.
import { readFileSync } from 'node:fs';

const [role, flag, configPath] = process.argv.slice(2);
process.stderr.write(`fake service argv ${JSON.stringify(process.argv.slice(2))}\n`);
if (role !== 'daemon' || flag !== '--config' || !configPath) {
  process.stderr.write('usage: daemon --config <path>\n');
  process.exit(2);
}
const config = JSON.parse(readFileSync(configPath, 'utf8'));
const mode = process.env.FAKE_SERVICE_MODE ?? 'ready';

// Installed before any output so a SIGTERM that follows the ready line can never
// find the default handler (which would exit at once and look like a clean stop).
process.on('SIGTERM', () => {
  if (process.env.FAKE_SERVICE_IGNORE_SIGTERM === '1') {
    process.stderr.write('ignoring SIGTERM\n');
    return;
  }
  process.stderr.write('stopping on SIGTERM\n');
  process.exit(0);
});

if (process.env.FAKE_SERVICE_STDERR) {
  process.stderr.write(`${process.env.FAKE_SERVICE_STDERR}\n`);
}

if (mode === 'exit-before-ready') {
  process.exit(Number(process.env.FAKE_SERVICE_EXIT_CODE ?? '3'));
}

if (mode === 'never-ready') {
  setInterval(() => {}, 1000);
} else {
  process.stdout.write(`${JSON.stringify({
    ready: true,
    role: 'daemon',
    socketPath: config.socketPath,
    clientTokenFile: config.clientTokenFile
  })}\n`);
  const exitAfter = Number(process.env.FAKE_SERVICE_EXIT_AFTER_MS ?? '0');
  if (exitAfter > 0) {
    setTimeout(() => process.exit(Number(process.env.FAKE_SERVICE_EXIT_CODE ?? '7')), exitAfter);
  }
  setInterval(() => {}, 1000);
}
