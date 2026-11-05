// Structural reads of App source through the TypeScript parser. Tests use these
// to check bindings (which command, which prop, which guard) without depending
// on formatting, attribute order or display wording.
import {readFileSync} from 'node:fs';
import ts from 'typescript';

export function parse(...names) {
  return names.map(name => {
    const text = readFileSync(new URL(`../../src/${name}`, import.meta.url), 'utf8');
    return ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  });
}

export function nodes(files, test) {
  const found = [];
  for (const file of files) {
    const visit = node => { if (test(node)) found.push({node, file}); ts.forEachChild(node, visit); };
    visit(file);
  }
  return found;
}

export const text = ({node, file}) => node.getText(file);

// Calls of a plain identifier, e.g. calls(files, 'act').
export const calls = (files, name) => nodes(files, node => ts.isCallExpression(node)
  && ts.isIdentifier(node.expression) && node.expression.text === name);

// String literal command names passed as the first argument of `name(...)`.
export const commands = (files, name) => calls(files, name)
  .map(({node}) => node.arguments[0])
  .filter(arg => arg && ts.isStringLiteralLike(arg))
  .map(arg => arg.text);

export const stringLiterals = files => nodes(files, ts.isStringLiteralLike).map(({node}) => node.text);

// JSX opening or self-closing elements with the given tag.
export const elements = (files, tag) => nodes(files, node =>
  (ts.isJsxSelfClosingElement(node) || ts.isJsxOpeningElement(node)) && node.tagName.getText() === tag);

// The source text of an attribute's value: a string literal's text or a JSX
// expression's text; null when the attribute is absent.
export function attribute({node, file}, name) {
  const found = node.attributes.properties.find(a => ts.isJsxAttribute(a) && a.name.getText(file) === name);
  if (!found) return null;
  const init = found.initializer;
  if (!init) return true;
  if (ts.isStringLiteral(init)) return init.text;
  return init.expression ? init.expression.getText(file) : null;
}

// Identifiers read by an expression node.
export function identifiers(node) {
  const names = new Set();
  const visit = n => { if (ts.isIdentifier(n)) names.add(n.text); ts.forEachChild(n, visit); };
  visit(node);
  return names;
}

export const variable = (files, name) => nodes(files, node =>
  ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.name.text === name);

export {ts};
