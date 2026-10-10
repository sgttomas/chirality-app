// Loads an App source module (src/<name>.tsx or .ts) for Node tests: each
// module is transpiled alone to CommonJS, and a relative import is served by
// loading that sibling the same way (once per test process).
import {readFileSync, existsSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';

const cache = new Map();

export function loadSrc(name) {
  if (cache.has(name)) return cache.get(name);
  const file = ['.tsx', '.ts'].map(ext => new URL(`../../src/${name}${ext}`, import.meta.url)).find(url => existsSync(url));
  if (!file) throw new Error(`no App source module ${name}`);
  const compiled = ts.transpileModule(readFileSync(file, 'utf8'), {compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, jsx: ts.JsxEmit.ReactJSX}});
  const exports = {};
  cache.set(name, exports);
  const base = createRequire(file);
  new Function('require', 'exports', compiled.outputText)(localRequire(base), exports);
  return exports;
}

/** A require that serves `./sibling` imports from src/ and everything else from `base`. */
export const localRequire = base => spec => spec.startsWith('./') ? loadSrc(spec.slice(2)) : base(spec);
