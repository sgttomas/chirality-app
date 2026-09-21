/**
 * Hermetic scratch pec server helper (D-APP-52 rider 8; brief §3 tests-only
 * carve-out): seeds a D-PEC-06-guarded scratch DB, provisions the bridge
 * rehearsal actors script-side (instance setup, not workflow acts), and
 * spawns/tears down a loopback-only pec server from `projects/pec` in this
 * repository. Used ONLY by the opt-in integration test (`PEC_BRIDGE_IT=1`)
 * and the D-APP-52 rehearsal driver — never by shipped runtime code. The
 * harness never starts, stops, or owns the owner's real server or DB.
 *
 * Requires Node >= 23.6 (pec's type-stripping runtime; ADR-002).
 */

import { spawn, spawnSync } from 'node:child_process';
import { randomBytes, scryptSync } from 'node:crypto';
import { existsSync, rmSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

// Resolved via createRequire so bundler-driven test runtimes (vite) do not try
// to transform the builtin specifier.
const requireBuiltin = createRequire(import.meta.url);

export function repoRootFrom(cwd) {
  const result = spawnSync('git', ['rev-parse', '--show-toplevel'], {
    cwd,
    encoding: 'utf8'
  });
  if (result.status !== 0) {
    throw new Error(`cannot resolve repo root from ${cwd}: ${result.stderr}`);
  }
  return result.stdout.trim();
}

export function assertTypeStrippingNode() {
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (major < 23 || (major === 23 && minor < 6)) {
    throw new Error(
      `pec scratch server requires Node >= 23.6 (type stripping); running ${process.versions.node}`
    );
  }
}

/** Same salt:hash scrypt format as projects/pec/server/src/auth.ts hashPassword. */
export function hashPecPassword(password) {
  const salt = randomBytes(16).toString('hex');
  const hash = scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
}

/**
 * Seed the scratch DB via pec's own D-PEC-06-guarded seed (refuses any target
 * outside the OS tmpdir that lacks a scratch/demo path token).
 */
export function seedScratchDb({ repoRoot, dbPath }) {
  const pecRoot = path.join(repoRoot, 'projects', 'pec');
  const result = spawnSync('npm', ['run', 'seed'], {
    cwd: pecRoot,
    encoding: 'utf8',
    env: { ...process.env, PEC_DB: dbPath }
  });
  if (result.status !== 0) {
    throw new Error(`pec seed failed for ${dbPath}:\n${result.stdout}\n${result.stderr}`);
  }
}

/**
 * Basis prep (rehearsal-01 pattern, disclosed as instance setup): provision the
 * owner-provisioned agent person (`is_admin=0`, coordinator) and a synthetic
 * project, and give the seeded admin/viewer personas roles on it. Direct DB
 * writes are instance setup only — every workflow act goes through the live
 * HTTP API afterwards.
 */
export async function provisionBridgeActors({ dbPath, agentEmail, agentPasswordHash }) {
  const { DatabaseSync } = requireBuiltin('node:sqlite');
  const db = new DatabaseSync(dbPath);
  try {
    const person = (email) => {
      const row = db.prepare('SELECT id FROM person WHERE email = ?').get(email);
      if (!row) {
        throw new Error(`seeded person not found: ${email}`);
      }
      return Number(row.id);
    };
    const adminPersonId = person('admin@aurora.dev');
    const viewerPersonId = person('viewer@aurora.dev');

    const nowIso = new Date().toISOString();
    db.prepare(
      'INSERT INTO person (name, email, password_hash, is_admin, discipline, created_at) VALUES (?, ?, ?, 0, NULL, ?)'
    ).run('PEC Bridge Agent', agentEmail, agentPasswordHash, nowIso);
    const agentPersonId = Number(
      db.prepare('SELECT id FROM person WHERE email = ?').get(agentEmail).id
    );

    db.prepare('INSERT INTO project (code, name, timezone) VALUES (?, ?, ?)').run(
      'SYN',
      'Synthetic Bridge Rehearsal',
      'America/Chicago'
    );
    const projectId = Number(db.prepare('SELECT id FROM project WHERE code = ?').get('SYN').id);

    const addRole = db.prepare(
      'INSERT INTO project_role (project_id, person_id, role) VALUES (?, ?, ?)'
    );
    addRole.run(projectId, agentPersonId, 'coordinator');
    addRole.run(projectId, adminPersonId, 'admin');
    addRole.run(projectId, viewerPersonId, 'viewer');

    return { projectId, agentPersonId, adminPersonId, viewerPersonId };
  } finally {
    db.close();
  }
}

/** Spawn the pec server on a loopback port against the scratch DB; poll until it answers. */
export async function startScratchServer({ repoRoot, dbPath, port, timeoutMs = 30000 }) {
  assertTypeStrippingNode();
  const pecRoot = path.join(repoRoot, 'projects', 'pec');
  const child = spawn(
    process.execPath,
    ['--disable-warning=ExperimentalWarning', path.join('server', 'src', 'index.ts')],
    {
      cwd: pecRoot,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, PEC_DB: dbPath, PEC_PORT: String(port) }
    }
  );
  let spawnFailure = '';
  child.stderr.on('data', (chunk) => {
    spawnFailure += chunk.toString();
  });

  const deadline = Date.now() + timeoutMs;
  for (;;) {
    if (child.exitCode !== null) {
      throw new Error(`pec scratch server exited early (${child.exitCode}):\n${spawnFailure}`);
    }
    try {
      const response = await fetch(`http://127.0.0.1:${port}/api/people`, {
        redirect: 'error'
      });
      await response.arrayBuffer().catch(() => undefined);
      break; // any HTTP answer (401 expected) means the server is listening
    } catch {
      if (Date.now() > deadline) {
        child.kill('SIGKILL');
        throw new Error(`pec scratch server did not answer on 127.0.0.1:${port} in ${timeoutMs}ms`);
      }
      await new Promise((resolve) => setTimeout(resolve, 250));
    }
  }

  return {
    child,
    async stop() {
      if (child.exitCode === null) {
        child.kill('SIGTERM');
        await new Promise((resolve) => {
          const timer = setTimeout(() => {
            child.kill('SIGKILL');
            resolve(undefined);
          }, 5000);
          child.once('exit', () => {
            clearTimeout(timer);
            resolve(undefined);
          });
        });
      }
    }
  };
}

/** Delete the scratch DB and its WAL/SHM companions after capture (rider 9). */
export function deleteScratchDb(dbPath) {
  for (const candidate of [dbPath, `${dbPath}-wal`, `${dbPath}-shm`]) {
    if (existsSync(candidate)) {
      rmSync(candidate);
    }
  }
}
