// Guard 2 (the sweep): the App's controls and accessible names hold only the App's words.
//
// It parses every view in app/src with the TypeScript parser and looks at
//   - each JSX expression inside <summary>, <button>, <option>, <a>, <label> or <legend>, and
//   - each title, aria-label, alt or placeholder attribute given as an expression, anywhere.
// An expression passes only if it is built from forms on a closed list of App-made forms (below) or is
// listed, exactly, with its reason in controls-guard-exceptions.json. Anything else fails, including a form
// the guard has never seen: it never passes an expression by checking only the forms it knows to be bad.
import ts from 'typescript';
import {readdirSync, readFileSync} from 'node:fs';

export const CONTROLS = new Set(['summary', 'button', 'option', 'a', 'label', 'legend']);
export const NAMING_ATTRIBUTES = new Set(['title', 'aria-label', 'alt', 'placeholder']);
/** Helpers whose result is always the App's words, a count or a checked identifier (each one read in its source).
 *  AgentText's helpers count only where the file imports them by these names from ./AgentText, and a file's own
 *  helper only in the file that defines it, so a different function under the same name is never trusted. */
export const AGENT_TEXT_HELPERS = new Set(['plainId', 'idWords', 'safeName']);
export const LOCAL_HELPERS = {'RecordsStorePanel.tsx': ['count'], 'WorkflowText.tsx': ['size']};
/** The helpers trusted in one source file. */
export function helpersOf(name, sf) {
  const trusted = new Set(LOCAL_HELPERS[name] ?? []);
  for (const statement of sf.statements) {
    if (!ts.isImportDeclaration(statement) || !ts.isStringLiteral(statement.moduleSpecifier) || statement.moduleSpecifier.text !== './AgentText') continue;
    const bindings = statement.importClause?.namedBindings;
    if (bindings && ts.isNamedImports(bindings)) for (const element of bindings.elements) {
      // `import { other as idWords }` is not AgentText's idWords.
      if (!element.propertyName && AGENT_TEXT_HELPERS.has(element.name.text)) trusted.add(element.name.text);
    }
  }
  return trusted;
}

const normal = text => text.replace(/\s+/g, ' ').trim();

/** Whether an expression is built only from the closed list of App-made forms. */
/** One file's program, so an identifier is resolved to its own declaration rather than trusted by its name. */
function parsed(name, text) {
  const options = {noLib: true, noResolve: true, jsx: ts.JsxEmit.Preserve, target: ts.ScriptTarget.Latest, allowJs: false};
  const source = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const host = ts.createCompilerHost(options);
  host.getSourceFile = file => file === name ? source : undefined;
  host.fileExists = file => file === name;
  host.readFile = file => file === name ? text : undefined;
  const program = ts.createProgram([name], options, host);
  return {sf: program.getSourceFile(name), checker: program.getTypeChecker()};
}
/** An identifier is App-made only by what it is declared as: the index parameter of a .map callback (a count),
 *  or a const in the same file whose own initializer is App-made. Its name alone is never trusted. */
function trustedIdentifier(node, context) {
  if (!context.checker || context.seen.has(node.text)) return false;
  const symbol = context.checker.getSymbolAtLocation(node);
  const declaration = symbol?.valueDeclaration ?? symbol?.declarations?.[0];
  if (!declaration || declaration.getSourceFile() !== node.getSourceFile()) return false;
  if (ts.isParameter(declaration)) {
    const fn = declaration.parent, call = fn.parent;
    return (ts.isArrowFunction(fn) || ts.isFunctionExpression(fn)) && fn.parameters.indexOf(declaration) === 1 && ts.isIdentifier(declaration.name)
      && ts.isCallExpression(call) && call.arguments[0] === fn && ts.isPropertyAccessExpression(call.expression) && call.expression.name.text === 'map';
  }
  if (ts.isVariableDeclaration(declaration) && ts.isIdentifier(declaration.name) && declaration.initializer
    && ts.isVariableDeclarationList(declaration.parent) && (declaration.parent.flags & ts.NodeFlags.Const)) {
    context.seen.add(node.text);
    try { return appMade(declaration.initializer, context); } finally { context.seen.delete(node.text); }
  }
  return false;
}
export function appMade(node, context = {helpers: new Set(), checker: null, seen: new Set()}) {
  const made = child => appMade(child, context);
  const helpers = context.helpers;
  if (ts.isParenthesizedExpression(node) || ts.isAsExpression(node) || ts.isNonNullExpression(node)) return made(node.expression);
  if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node) || ts.isNumericLiteral(node)) return true;
  if (node.kind === ts.SyntaxKind.NullKeyword || node.kind === ts.SyntaxKind.TrueKeyword || node.kind === ts.SyntaxKind.FalseKeyword) return true;
  if (ts.isTemplateExpression(node)) return node.templateSpans.every(span => made(span.expression));
  // A choice shows one of its branches; its condition is not shown.
  if (ts.isConditionalExpression(node)) return made(node.whenTrue) && made(node.whenFalse);
  if (ts.isBinaryExpression(node)) {
    const op = node.operatorToken.kind;
    // `a && b` shows b (or a false or empty a, which renders nothing; a number a is a count by the next rule or fails).
    if (op === ts.SyntaxKind.AmpersandAmpersandToken) return made(node.right) && (isCondition(node.left) || made(node.left));
    if (op === ts.SyntaxKind.BarBarToken || op === ts.SyntaxKind.QuestionQuestionToken || op === ts.SyntaxKind.PlusToken) return made(node.left) && made(node.right);
    if ([ts.SyntaxKind.MinusToken, ts.SyntaxKind.AsteriskToken, ts.SyntaxKind.SlashToken].includes(op)) return made(node.left) && made(node.right);
    return false;
  }
  // A count: the length of something. An identifier stands for what it is declared as (trustedIdentifier).
  if (ts.isPropertyAccessExpression(node) && node.name.text === 'length') return true;
  if (ts.isIdentifier(node)) return trustedIdentifier(node, context);
  if (ts.isCallExpression(node) && ts.isIdentifier(node.expression) && helpers.has(node.expression.text)) return true;
  return false;
}
const hasJsx = node => { let found = false; const walk = n => { if (found) return; if (ts.isJsxElement(n) || ts.isJsxSelfClosingElement(n) || ts.isJsxFragment(n)) { found = true; return; } ts.forEachChild(n, walk); }; walk(node); return found; };
/** A condition: a comparison or negation, never itself rendered as text. */
function isCondition(node) {
  if (ts.isParenthesizedExpression(node)) return isCondition(node.expression);
  if (ts.isPrefixUnaryExpression(node) && node.operator === ts.SyntaxKind.ExclamationToken) return true;
  if (ts.isBinaryExpression(node)) {
    const op = node.operatorToken.kind;
    if ([ts.SyntaxKind.EqualsEqualsEqualsToken, ts.SyntaxKind.ExclamationEqualsEqualsToken, ts.SyntaxKind.EqualsEqualsToken, ts.SyntaxKind.ExclamationEqualsToken,
      ts.SyntaxKind.LessThanToken, ts.SyntaxKind.GreaterThanToken, ts.SyntaxKind.LessThanEqualsToken, ts.SyntaxKind.GreaterThanEqualsToken].includes(op)) return true;
    if (op === ts.SyntaxKind.AmpersandAmpersandToken || op === ts.SyntaxKind.BarBarToken) return isCondition(node.left) && isCondition(node.right);
  }
  return false;
}

/** Every expression the guard looks at in one source text: { line, where, expr }. */
export function findings(name, text) {
  const {sf, checker} = parsed(name, text);
  const out = [];
  const context = {helpers: helpersOf(name, sf), checker, seen: new Set()};
  const at = node => sf.getLineAndCharacterOfPosition(node.getStart()).line + 1;
  const attributes = props => { for (const a of props) if (ts.isJsxAttribute(a) && NAMING_ATTRIBUTES.has(a.name.getText()) && a.initializer && ts.isJsxExpression(a.initializer) && a.initializer.expression)
    out.push({line: at(a), where: `@${a.name.getText()}`, node: a.initializer.expression}); };
  // A JSX expression inside a control: its JSX parts are visited as elements; what it can show as text is recorded.
  const collect = (expr, control) => {
    if (ts.isParenthesizedExpression(expr)) return collect(expr.expression, control);
    if (ts.isJsxElement(expr) || ts.isJsxSelfClosingElement(expr) || ts.isJsxFragment(expr)) return visit(expr, control);
    if (ts.isConditionalExpression(expr)) { collect(expr.whenTrue, control); collect(expr.whenFalse, control); return; }
    if (ts.isBinaryExpression(expr) && expr.operatorToken.kind === ts.SyntaxKind.AmpersandAmpersandToken && hasJsx(expr.right)) return collect(expr.right, control);
    if (ts.isCallExpression(expr) && ts.isPropertyAccessExpression(expr.expression) && expr.expression.name.text === 'map' && expr.arguments.length && hasJsx(expr.arguments[0])) {
      const fn = expr.arguments[0];
      if ((ts.isArrowFunction(fn) || ts.isFunctionExpression(fn)) && !ts.isBlock(fn.body)) return collect(fn.body, control);
    }
    out.push({line: at(expr), where: `<${control}>`, node: expr});
  };
  const visit = (node, control) => {
    if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
      const opening = ts.isJsxElement(node) ? node.openingElement : node;
      const tag = opening.tagName.getText();
      attributes(opening.attributes.properties);
      // A component inside a control (AgentText, say) puts whatever it draws into the control's name: it is listed or it fails.
      if (control && /^[A-Z]/.test(tag)) out.push({line: at(node), where: `<${control}>`, node: opening.tagName, component: tag});
      if (ts.isJsxElement(node)) for (const child of node.children) visit(child, CONTROLS.has(tag) ? tag : control);
      return;
    }
    if (ts.isJsxFragment(node)) { for (const child of node.children) visit(child, control); return; }
    if (ts.isJsxExpression(node) && node.expression) { if (control) collect(node.expression, control); else ts.forEachChild(node, child => visit(child, control)); return; }
    ts.forEachChild(node, child => visit(child, control));
  };
  visit(sf, null);
  return out.map(({line, where, node, component}) => ({line, where, expr: component ? `<${component}>` : normal(node.getText()), node: component ? null : node, context}));
}

/** The failures in the views: each expression neither App-made nor listed with its reason. */
export function guardFailures(srcDir, exceptions) {
  const listed = new Set(exceptions.map(e => `${e.file}|${e.where}|${normal(e.expr)}`));
  const failures = [], used = new Set();
  for (const name of readdirSync(srcDir).filter(n => n.endsWith('.tsx') && n !== 'AgentText.tsx').sort()) {
    for (const f of findings(name, readFileSync(new URL(name, srcDir), 'utf8'))) {
      if (f.node && appMade(f.node, f.context)) continue;
      const key = `${name}|${f.where}|${f.expr}`;
      if (listed.has(key)) used.add(key); else failures.push(`${name}:${f.line} ${f.where} ${f.expr}`);
    }
  }
  // A listed exception that no longer matches an expression the guard would fail is stale: it is removed, not kept.
  for (const key of listed) if (!used.has(key)) failures.push(`stale exception ${key}`);
  return failures;
}
