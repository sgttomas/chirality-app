import { mkdtemp, mkdir, rename, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file' | 'symlink';
  children?: TreeNode[];
};

let tmpRoot = '';
let projectRoot = '';

function collectPaths(node: TreeNode): Set<string> {
  const paths = new Set<string>([node.path]);
  for (const child of node.children ?? []) {
    for (const childPath of collectPaths(child)) {
      paths.add(childPath);
    }
  }
  return paths;
}

async function importRouteModule(): Promise<typeof import('../../../app/api/working-root/tree/route')> {
  vi.resetModules();
  return import('../../../app/api/working-root/tree/route');
}

async function requestTree(
  route: typeof import('../../../app/api/working-root/tree/route'),
  rootPath: string
): Promise<{ status: number; body: { root?: TreeNode; error?: { type?: string } } }> {
  const response = await route.GET(
    new Request(
      `http://localhost/api/working-root/tree?projectRoot=${encodeURIComponent(rootPath)}&depth=4`
    )
  );
  return {
    status: response.status,
    body: (await response.json()) as { root?: TreeNode; error?: { type?: string } }
  };
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-working-root-tree-route-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
  tmpRoot = '';
  projectRoot = '';
});

describe('GET /api/working-root/tree', () => {
  it('reflects external create, rename, and delete changes across refresh calls', async () => {
    const route = await importRouteModule();
    const alpha = path.join(projectRoot, 'alpha.txt');
    const renamed = path.join(projectRoot, 'alpha-renamed.txt');
    const beta = path.join(projectRoot, 'beta.txt');
    const nestedDir = path.join(projectRoot, 'nested');
    const nestedFile = path.join(nestedDir, 'inside.txt');

    await mkdir(nestedDir, { recursive: true });
    await writeFile(alpha, 'alpha', 'utf8');
    await writeFile(nestedFile, 'inside', 'utf8');

    const first = await requestTree(route, projectRoot);
    expect(first.status).toBe(200);
    const firstPaths = collectPaths(first.body.root as TreeNode);
    expect(firstPaths.has(alpha)).toBe(true);
    expect(firstPaths.has(beta)).toBe(false);
    expect(firstPaths.has(nestedFile)).toBe(true);

    await rename(alpha, renamed);
    await writeFile(beta, 'beta', 'utf8');

    const second = await requestTree(route, projectRoot);
    expect(second.status).toBe(200);
    const secondPaths = collectPaths(second.body.root as TreeNode);
    expect(secondPaths.has(alpha)).toBe(false);
    expect(secondPaths.has(renamed)).toBe(true);
    expect(secondPaths.has(beta)).toBe(true);

    await rm(beta);
    const third = await requestTree(route, projectRoot);
    expect(third.status).toBe(200);
    const thirdPaths = collectPaths(third.body.root as TreeNode);
    expect(thirdPaths.has(beta)).toBe(false);
    expect(thirdPaths.has(renamed)).toBe(true);
  });

  it('displays symlinks as leaf nodes with kind symlink and does not traverse them', async () => {
    const route = await importRouteModule();

    const targetDir = path.join(projectRoot, 'real-dir');
    const targetFile = path.join(targetDir, 'secret.txt');
    await mkdir(targetDir, { recursive: true });
    await writeFile(targetFile, 'secret', 'utf8');

    const linkToDir = path.join(projectRoot, 'link-to-dir');
    const linkToFile = path.join(projectRoot, 'link-to-file.txt');
    await symlink(targetDir, linkToDir, 'dir');
    await writeFile(path.join(projectRoot, 'regular.txt'), 'regular', 'utf8');
    await symlink(path.join(projectRoot, 'regular.txt'), linkToFile, 'file');

    const result = await requestTree(route, projectRoot);
    expect(result.status).toBe(200);

    const root = result.body.root as TreeNode;
    const children = root.children ?? [];

    const dirLink = children.find((child) => child.name === 'link-to-dir');
    expect(dirLink).toBeDefined();
    expect(dirLink?.kind).toBe('symlink');
    expect(dirLink?.children).toBeUndefined();

    const fileLink = children.find((child) => child.name === 'link-to-file.txt');
    expect(fileLink).toBeDefined();
    expect(fileLink?.kind).toBe('symlink');

    const realDir = children.find((child) => child.name === 'real-dir');
    expect(realDir).toBeDefined();
    expect(realDir?.kind).toBe('directory');

    const allPaths = collectPaths(root);
    expect(allPaths.has(targetFile)).toBe(true);
    expect(allPaths.has(path.join(linkToDir, 'secret.txt'))).toBe(false);
  });

  it('hides the engine scratch directory but keeps other dot-directories', async () => {
    const route = await importRouteModule();
    const scratch = path.join(projectRoot, '.chirality-scratch-Q6MuOO');
    await mkdir(scratch, { recursive: true });
    await writeFile(path.join(scratch, '.gitignore'), '*\n');
    await mkdir(path.join(projectRoot, '.chirality', 'attachments'), { recursive: true });
    await writeFile(path.join(projectRoot, 'README.md'), '# trial\n');

    const response = await requestTree(route, projectRoot);
    expect(response.status).toBe(200);
    const names = (response.body.root?.children ?? []).map((child) => child.name);
    expect(names).toContain('.chirality');
    expect(names).toContain('README.md');
    expect(names).not.toContain('.chirality-scratch-Q6MuOO');
    expect(collectPaths(response.body.root as TreeNode).has(scratch)).toBe(false);
  });

  it('returns typed accessibility errors for missing roots', async () => {
    const route = await importRouteModule();
    const response = await requestTree(route, path.join(projectRoot, 'missing-root'));

    expect(response.status).toBe(404);
    expect(response.body).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });
});
