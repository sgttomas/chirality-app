// The presentation guard: on a guarded view, a value the App did not write reaches the page only through one
// of the approved presentations.
//
// It parses each guarded view with the TypeScript parser and its checker (one file at a time, so an identifier
// is judged by what it is declared as, never by its name), and looks at
//   - every expression drawn as a child of an element, anywhere in the view;
//   - every attribute that names, describes or holds a value: title, alt, placeholder, value, defaultValue and
//     every aria- attribute, and every attribute of an approved presentation other than the value it presents;
//   - every spread of attributes;
//   - every component the view draws.
// An expression passes only if it is built from the closed list of forms below. Anything else fails, including a
// form the guard has never seen: it never passes an expression by checking only the forms it knows to be bad.
// A listed exception (presentation-guard-exceptions.json) names one expression exactly, with its reason; a listed
// exception that no longer matches a failing expression is itself a failure, so the list cannot drift.
// Writes to the page that bypass React's rendering (raw HTML, assigning DOM text or values, DOM insertion) fail
// and cannot be listed.
//
// What the guard proves is that every drawn expression takes an approved form. It does not prove what an approved
// presentation does with its value: those are the examined implementations named in TRUSTED (AgentText.tsx), and
// their own tests show what they draw.
import ts from 'typescript';
import {readFileSync} from 'node:fs';

/** The approved presentations, by the module they must be imported from under these names. */
export const TRUSTED = {
  './AgentText': {
    // Functions whose result is the App's words, a checked identifier or a checked number.
    functions: ['plainId', 'idWords', 'wordOf', 'numberWords', 'isoSeconds', 'clockWords'],
    // Components that draw a supplied value: boxed, or as the App's words only for a value they check at run time.
    components: ['AgentText', 'SuppliedId', 'Word', 'Num', 'Flag'],
  },
};
/** Anchor builders: an element id made from a supplied identity by hex encoding, never shown as text. Trusted only in
 * attributes that hold an id or a link target. */
export const ANCHOR_FUNCTIONS = {'./NativeActivity': ['itemAnchorId', 'requestAnchorId', 'runEvidenceAnchor']};
const ID_ATTRIBUTES = new Set(['id', 'href', 'htmlFor', 'aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-owns', 'aria-activedescendant', 'aria-details', 'aria-errormessage', 'aria-flowto']);
const VALUE_ATTRIBUTES = new Set(['title', 'alt', 'placeholder', 'label']);
/** A value attribute is drawn only by a text field; an option's, a select's or a button's value is not shown. */
const DRAWN_VALUE_TAGS = new Set(['input', 'textarea']);
const shownAttribute = (name, tag) => VALUE_ATTRIBUTES.has(name) || name.startsWith('aria-') || ID_ATTRIBUTES.has(name) || (['value', 'defaultValue'].includes(name) && DRAWN_VALUE_TAGS.has(tag));
/** Attributes of an approved presentation that only style or key it. */
const STYLE_ATTRIBUTES = new Set(['style', 'key', 'className', 'block']);
/** Property writes and calls that put text or markup on the page outside React's rendering. */
const FORBIDDEN_PROPERTIES = new Set(['innerHTML', 'outerHTML', 'textContent', 'innerText', 'outerText', 'nodeValue', 'value', 'defaultValue', 'placeholder', 'title', 'data']);
const FORBIDDEN_CALLS = new Set(['insertAdjacentHTML', 'insertAdjacentText', 'insertAdjacentElement', 'write', 'writeln', 'setAttribute', 'setAttributeNS', 'createTextNode', 'append', 'prepend', 'appendChild', 'insertBefore', 'replaceChildren', 'replaceWith', 'before', 'after', 'execCommand', 'setHTMLUnsafe', 'createContextualFragment']);

const normal = text => text.replace(/\s+/g, ' ').trim();
/** Elements whose content is a control's or a heading's name: they hold only the App's words, never a box, so an
 * approved presentation that can draw a supplied value boxed is not allowed inside them. */
export const APP_ONLY = new Set(['button', 'a', 'summary', 'label', 'legend', 'option', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']);

/** One file's program, so that an identifier resolves to its own declaration. */
export function parsed(name, text) {
  const options = {noLib: true, noResolve: true, jsx: ts.JsxEmit.Preserve, target: ts.ScriptTarget.Latest};
  const source = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const host = ts.createCompilerHost(options);
  host.getSourceFile = file => file === name ? source : undefined;
  host.fileExists = file => file === name;
  host.readFile = file => file === name ? text : undefined;
  const program = ts.createProgram([name], options, host);
  return {sf: program.getSourceFile(name), checker: program.getTypeChecker()};
}

/** The names a file imports, by local name: { module, imported }. */
function importsOf(sf) {
  const out = new Map();
  for (const statement of sf.statements) {
    if (!ts.isImportDeclaration(statement) || !ts.isStringLiteral(statement.moduleSpecifier)) continue;
    const bindings = statement.importClause?.namedBindings;
    if (bindings && ts.isNamedImports(bindings)) for (const element of bindings.elements)
      out.set(element.name.text, {module: statement.moduleSpecifier.text, imported: (element.propertyName ?? element.name).text});
  }
  return out;
}
const isTrusted = (context, local, kind) => {
  const from = context.imports.get(local);
  return !!from && from.imported === local && (TRUSTED[from.module]?.[kind] ?? []).includes(local);
};
const isAnchor = (context, local) => {
  const from = context.imports.get(local);
  if (from) return from.imported === local && (ANCHOR_FUNCTIONS[from.module] ?? []).includes(local);
  // In the module that defines them.
  return Object.entries(ANCHOR_FUNCTIONS).some(([module, names]) => `${module.replace(/^\.\//, '')}.tsx` === context.name && names.includes(local));
};

/** The declaration an identifier resolves to, in this file only. */
function declarationOf(node, context) {
  const symbol = context.checker.getSymbolAtLocation(node);
  const declaration = symbol?.valueDeclaration ?? symbol?.declarations?.[0];
  return declaration && declaration.getSourceFile() === context.sf ? declaration : null;
}
const unwrap = node => { while (ts.isParenthesizedExpression(node) || ts.isAsExpression(node) || ts.isNonNullExpression(node) || ts.isSatisfiesExpression?.(node)) node = node.expression; return node; };
const isConst = declaration => ts.isVariableDeclaration(declaration) && ts.isVariableDeclarationList(declaration.parent) && !!(declaration.parent.flags & ts.NodeFlags.Const);

/** The module of the App's word tables for Codex's fixed vocabularies; wordTableFailures checks it. */
export const WORD_TABLE_MODULE = './nativeWords';
/** A table of the App's words: one imported under its own name from the word-table module, or a const object
 * literal in this file whose every value is a string literal. */
function isWordTable(node, context) {
  node = unwrap(node);
  if (ts.isPropertyAccessExpression(node) || !ts.isIdentifier(node)) return false;
  const from = context.imports.get(node.text);
  if (from) return from.module === WORD_TABLE_MODULE && from.imported === node.text;
  const declaration = declarationOf(node, context);
  if (!declaration || !isConst(declaration) || !declaration.initializer) return false;
  const value = unwrap(declaration.initializer);
  return ts.isObjectLiteralExpression(value) && value.properties.every(p => ts.isPropertyAssignment(p) && (ts.isStringLiteral(unwrap(p.initializer)) || ts.isNoSubstitutionTemplateLiteral(unwrap(p.initializer))));
}

/** The function a same-file call or component name resolves to, if it is one. */
function functionOf(node, context) {
  const declaration = ts.isIdentifier(node) ? declarationOf(node, context) : null;
  if (!declaration) return null;
  if (ts.isFunctionDeclaration(declaration)) return declaration;
  if (isConst(declaration) && declaration.initializer) {
    const value = unwrap(declaration.initializer);
    if (ts.isArrowFunction(value) || ts.isFunctionExpression(value)) return value;
  }
  return null;
}
/** Every value a function returns. */
function returnsOf(fn) {
  if (!ts.isBlock(fn.body)) return [fn.body];
  const out = [];
  const walk = node => { if (node !== fn && (ts.isFunctionLike(node))) return; if (ts.isReturnStatement(node)) out.push(node.expression ?? null); ts.forEachChild(node, walk); };
  ts.forEachChild(fn.body, walk);
  return out;
}

/** Whether an expression is built only from App-made forms. */
export function appMade(node, context) {
  node = unwrap(node);
  const made = child => appMade(child, context);
  if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node) || ts.isNumericLiteral(node)) return true;
  if ([ts.SyntaxKind.NullKeyword, ts.SyntaxKind.TrueKeyword, ts.SyntaxKind.FalseKeyword, ts.SyntaxKind.UndefinedKeyword].includes(node.kind)) return true;
  if (ts.isIdentifier(node) && node.text === 'undefined') return true;
  if (ts.isTemplateExpression(node)) return node.templateSpans.every(span => made(span.expression));
  // A choice draws one of its branches; its condition is not drawn.
  if (ts.isConditionalExpression(node)) return made(node.whenTrue) && made(node.whenFalse);
  if (ts.isBinaryExpression(node)) {
    const op = node.operatorToken.kind;
    // `a && b` draws b, or a when a is falsy: a falsy value draws nothing, or only "0", "NaN", "false", "null" or
    // "undefined" inside a string, never supplied words. So a is not judged.
    if (op === ts.SyntaxKind.AmpersandAmpersandToken) return made(node.right);
    if ([ts.SyntaxKind.BarBarToken, ts.SyntaxKind.QuestionQuestionToken, ts.SyntaxKind.PlusToken, ts.SyntaxKind.MinusToken, ts.SyntaxKind.AsteriskToken, ts.SyntaxKind.SlashToken].includes(op)) return made(node.left) && made(node.right);
    return false;
  }
  // A count: the length of an array the App holds is a number. Only a call's or an array literal's length, or
  // the length of something read through list(), is a count; a supplied object's "length" field is not.
  if (ts.isPropertyAccessExpression(node) && node.name.text === 'length') return isArrayExpression(node.expression, context);
  if (ts.isIdentifier(node)) return trustedIdentifier(node, context);
  // A named entry of a const object literal in this file, whose entry is itself App-made.
  if (ts.isPropertyAccessExpression(node) && ts.isIdentifier(unwrap(node.expression))) {
    const declaration = declarationOf(unwrap(node.expression), context);
    const value = declaration && isConst(declaration) && declaration.initializer ? unwrap(declaration.initializer) : null;
    const entry = value && ts.isObjectLiteralExpression(value) ? value.properties.find(p => ts.isPropertyAssignment(p) && p.name.getText().replace(/^["']|["']$/g, '') === node.name.text) : null;
    if (entry) return guarded(context, entry, () => appMade(entry.initializer, context));
  }
  if (ts.isCallExpression(node)) {
    const callee = unwrap(node.expression);
    if (ts.isIdentifier(callee) && isTrusted(context, callee.text, 'functions')) {
      // A word table must be the App's own.
      return callee.text !== 'wordOf' || isWordTable(node.arguments[0], context);
    }
    // A position found in an array is a number.
    if (ts.isPropertyAccessExpression(callee) && ['findIndex', 'indexOf', 'lastIndexOf', 'findLastIndex'].includes(callee.name.text)) return true;
    // String(n) of a count; JSON.stringify never passes.
    if (ts.isIdentifier(callee) && callee.text === 'String' && node.arguments.length === 1) return made(node.arguments[0]);
    // A same-file function whose every return is App-made (its parameters are not).
    const fn = ts.isIdentifier(callee) ? functionOf(callee, context) : null;
    if (fn) return guarded(context, fn, () => returnsOf(fn).every(r => r === null || made(r)));
  }
  return false;
}
/** An array expression: a literal, a filter/map/slice of one, or list(...) (which returns an array). */
function isArrayExpression(node, context) {
  node = unwrap(node);
  if (ts.isArrayLiteralExpression(node)) return true;
  if (ts.isCallExpression(node)) {
    const callee = unwrap(node.expression);
    if (ts.isIdentifier(callee) && callee.text === 'list') return true;
    if (ts.isPropertyAccessExpression(callee) && ['filter', 'map', 'slice', 'flatMap', 'concat'].includes(callee.name.text)) return isArrayExpression(callee.expression, context);
    if (ts.isPropertyAccessExpression(callee) && ['keys', 'values', 'entries'].includes(callee.name.text) && ts.isIdentifier(callee.expression) && callee.expression.text === 'Object') return true;
    if (ts.isPropertyAccessExpression(callee) && callee.name.text === 'from' && ts.isIdentifier(callee.expression) && callee.expression.text === 'Array') return true;
  }
  if (ts.isIdentifier(node)) {
    const declaration = declarationOf(node, context);
    return !!declaration && isConst(declaration) && !!declaration.initializer && isArrayExpression(declaration.initializer, context);
  }
  return false;
}
function guarded(context, key, check) {
  if (context.seen.has(key)) return false;
  context.seen.add(key);
  try { return check(); } finally { context.seen.delete(key); }
}
/** An identifier stands for what it is declared as: the index of a .map callback (a count); a const whose own
 * value is App-made; or a prop of a component in this file that every use in this file passes App-made (and that
 * no other file can use, since the component is not exported). Its name alone is never trusted. */
function trustedIdentifier(node, context) {
  const declaration = declarationOf(node, context);
  if (!declaration) return false;
  if (ts.isParameter(declaration)) {
    const fn = declaration.parent, call = fn.parent;
    return (ts.isArrowFunction(fn) || ts.isFunctionExpression(fn)) && fn.parameters.indexOf(declaration) === 1 && ts.isIdentifier(declaration.name)
      && ts.isCallExpression(call) && call.arguments[0] === fn && ts.isPropertyAccessExpression(call.expression) && ['map', 'flatMap'].includes(call.expression.name.text);
  }
  if (isConst(declaration) && ts.isIdentifier(declaration.name) && declaration.initializer) return guarded(context, declaration, () => appMade(declaration.initializer, context));
  if (ts.isBindingElement(declaration)) return propPassedAppMade(declaration, context);
  return false;
}
/** A destructured prop named children, or declared as ReactNode in the component's props type. */
function nodeProp(binding) {
  const name = (binding.propertyName ?? binding.name).getText();
  if (name === 'children') return true;
  const parameter = binding.parent?.parent;
  const type = parameter && ts.isParameter(parameter) ? parameter.type : null;
  if (!type || !ts.isTypeLiteralNode(type)) return false;
  const member = type.members.find(m => ts.isPropertySignature(m) && m.name.getText() === name);
  return !!member?.type && member.type.getText() === 'ReactNode';
}
/** A destructured prop of a same-file, unexported component: App-made only if every use passes it App-made, or
 * leaves it to an App-made default. */
function propPassedAppMade(binding, context) {
  const pattern = binding.parent, parameter = pattern?.parent;
  if (!ts.isObjectBindingPattern(pattern) || !ts.isParameter(parameter)) return false;
  const fn = parameter.parent;
  const name = ts.isFunctionDeclaration(fn) ? fn.name?.text : ts.isVariableDeclaration(fn.parent) && ts.isIdentifier(fn.parent.name) ? fn.parent.name.text : null;
  if (!name || fn.parameters[0] !== parameter) return false;
  const exported = ts.isFunctionDeclaration(fn) ? fn.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword) : fn.parent?.parent?.parent?.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword);
  if (exported) return false;
  const prop = (binding.propertyName ?? binding.name).getText();
  return guarded(context, binding, () => {
    let ok = true, used = false;
    const walk = node => {
      if (!ok) return;
      if ((ts.isJsxOpeningElement(node) || ts.isJsxSelfClosingElement(node)) && node.tagName.getText() === name) {
        used = true;
        const attribute = node.attributes.properties.find(a => ts.isJsxAttribute(a) && a.name.getText() === prop);
        if (node.attributes.properties.some(a => ts.isJsxSpreadAttribute(a))) ok = false;
        else if (!attribute) ok = !binding.initializer || appMade(binding.initializer, context);
        else if (!attribute.initializer || ts.isStringLiteral(attribute.initializer)) ok = true;
        else ok = ts.isJsxExpression(attribute.initializer) && !!attribute.initializer.expression && appMade(attribute.initializer.expression, context);
      } else if (ts.isIdentifier(node) && node.text === name && !ts.isJsxOpeningElement(node.parent) && !ts.isJsxSelfClosingElement(node.parent) && !ts.isJsxClosingElement(node.parent)
        && node.parent !== fn && !(ts.isVariableDeclaration(node.parent) && node.parent.name === node) && !(ts.isFunctionDeclaration(node.parent) && node.parent.name === node)) {
        // Called or passed some other way: its props cannot be followed.
        ok = false;
      }
      ts.forEachChild(node, walk);
    };
    walk(context.sf);
    return ok && used;
  });
}
/** A condition: a comparison or negation, never itself drawn as text. */
function isCondition(node) {
  node = unwrap(node);
  if (ts.isPrefixUnaryExpression(node) && node.operator === ts.SyntaxKind.ExclamationToken) return true;
  if (ts.isBinaryExpression(node)) {
    const op = node.operatorToken.kind;
    if ([ts.SyntaxKind.EqualsEqualsEqualsToken, ts.SyntaxKind.ExclamationEqualsEqualsToken, ts.SyntaxKind.EqualsEqualsToken, ts.SyntaxKind.ExclamationEqualsToken,
      ts.SyntaxKind.LessThanToken, ts.SyntaxKind.GreaterThanToken, ts.SyntaxKind.LessThanEqualsToken, ts.SyntaxKind.GreaterThanEqualsToken, ts.SyntaxKind.InstanceOfKeyword, ts.SyntaxKind.InKeyword].includes(op)) return true;
    if (op === ts.SyntaxKind.AmpersandAmpersandToken || op === ts.SyntaxKind.BarBarToken) return isCondition(node.left) && isCondition(node.right);
  }
  return false;
}
const hasJsx = node => { let found = false; const walk = n => { if (found) return; if (ts.isJsxElement(n) || ts.isJsxSelfClosingElement(n) || ts.isJsxFragment(n)) { found = true; return; } ts.forEachChild(n, walk); }; walk(node); return found; };

/** Every expression the guard judges in one view: { line, where, expr, node, context, forbidden? }. */
export function findings(name, text) {
  const {sf, checker} = parsed(name, text);
  const context = {name, sf, checker, imports: importsOf(sf), seen: new Set()};
  const out = [];
  const at = node => sf.getLineAndCharacterOfPosition(node.getStart()).line + 1;
  const record = (node, where, extra = {}) => out.push({line: at(node), where, expr: normal(node.getText()), node, context, ...extra});

  // What a child expression can draw: its JSX parts are elements, visited where written; the rest is judged.
  const drawn = (expr, sink = record) => {
    expr = unwrap(expr);
    const again = e => drawn(e, sink);
    if (ts.isJsxElement(expr) || ts.isJsxSelfClosingElement(expr) || ts.isJsxFragment(expr)) return;
    if (ts.isConditionalExpression(expr)) { again(expr.whenTrue); again(expr.whenFalse); return; }
    // `a && b` draws b, or a falsy a, which draws nothing or only "0" or "NaN": a is not judged (see appMade).
    if (ts.isBinaryExpression(expr) && expr.operatorToken.kind === ts.SyntaxKind.AmpersandAmpersandToken) return again(expr.right);
    if (ts.isBinaryExpression(expr) && [ts.SyntaxKind.BarBarToken, ts.SyntaxKind.QuestionQuestionToken].includes(expr.operatorToken.kind) && hasJsx(expr)) { again(expr.left); again(expr.right); return; }
    // A list drawn by a callback: what each callback returns is drawn.
    if (ts.isCallExpression(expr) && ts.isPropertyAccessExpression(expr.expression) && ['map', 'flatMap'].includes(expr.expression.name.text) && expr.arguments.length) {
      const fn = unwrap(expr.arguments[0]);
      if (ts.isArrowFunction(fn) || ts.isFunctionExpression(fn)) { for (const r of returnsOf(fn)) if (r) again(r); return; }
    }
    // A same-file function drawn by call: each value it returns is drawn (its JSX is visited where written).
    if (ts.isCallExpression(expr) && ts.isIdentifier(unwrap(expr.expression))) {
      // Judged at the call: it fails here when anything it returns would fail.
      const fn = functionOf(unwrap(expr.expression), context);
      if (fn) {
        let failed = false;
        const ok = guarded(context, fn, () => { returnsOf(fn).forEach(r => { if (r) drawn(r, () => { failed = true; }); }); return true; });
        if (ok && !failed) return;
        return sink(expr, 'drawn');
      }
    }
    if (ts.isIdentifier(expr)) {
      const declaration = declarationOf(expr, context);
      // A component's children, or a prop declared as ReactNode, is drawn where its caller writes it, and judged
      // there when the caller is a guarded view (a caller elsewhere is outside this boundary).
      if (declaration && ts.isBindingElement(declaration) && nodeProp(declaration)) return;
      // A const is drawn as its own value.
      if (declaration && isConst(declaration) && declaration.initializer && hasJsx(declaration.initializer)) {
        if (guarded(context, declaration, () => (again(declaration.initializer), true))) return;
      }
    }
    if (!appMade(expr, context)) sink(expr, 'drawn');
  };
  const attributes = (tag, props, trustedComponent) => {
    for (const a of props) {
      if (ts.isJsxSpreadAttribute(a)) { if (!spreadMade(a.expression, tag)) record(a.expression, '{...}'); continue; }
      const attribute = a.name.getText();
      if (attribute === 'dangerouslySetInnerHTML') { record(a, '@dangerouslySetInnerHTML', {forbidden: true}); continue; }
      if (!a.initializer || ts.isStringLiteral(a.initializer) || !ts.isJsxExpression(a.initializer) || !a.initializer.expression) continue;
      const expr = a.initializer.expression;
      // An approved presentation takes any value to present; its other attributes (label, name, words…) are the App's.
      if (trustedComponent) {
        if (attribute === 'value' || STYLE_ATTRIBUTES.has(attribute)) continue;
        if (attribute === 'words' && isWordTable(expr, context)) continue;
        if (!appMade(expr, context)) record(expr, `@${attribute}`);
        continue;
      }
      if (!shownAttribute(attribute, tag)) continue;
      if (ID_ATTRIBUTES.has(attribute)) { if (!idValue(expr)) record(expr, `@${attribute}`); continue; }
      // A text field shows what the person types: its state must be set only from this kind of field's own input.
      if (['value', 'defaultValue'].includes(attribute) && personTyped(expr)) continue;
      if (!appMade(expr, context)) record(expr, `@${attribute}`);
    }
  };
  // A text field's value from state that only the person's typing sets: `const [x, setX] = useState(<App-made>)`,
  // and every call of setX passes `<event>.target.value`, an App-made value, or an updater returning an object that
  // spreads its own argument and sets entries only to `<event>.target.value` or App-made values. `x`, `x[key]` and
  // `x[key] ?? <App-made>` read it.
  const personTyped = expr => {
    let node = unwrap(expr);
    if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.QuestionQuestionToken && appMade(node.right, context)) node = unwrap(node.left);
    if (ts.isElementAccessExpression(node)) node = unwrap(node.expression);
    if (!ts.isIdentifier(node)) return false;
    const declaration = declarationOf(node, context);
    if (!declaration || !ts.isBindingElement(declaration) || !ts.isArrayBindingPattern(declaration.parent)) return false;
    const pattern = declaration.parent, holder = pattern.parent;
    if (pattern.elements.indexOf(declaration) !== 0 || !ts.isVariableDeclaration(holder) || !holder.initializer) return false;
    const init = unwrap(holder.initializer);
    const empty = v => { v = unwrap(v); return (ts.isObjectLiteralExpression(v) || ts.isArrayLiteralExpression(v)) && (ts.isObjectLiteralExpression(v) ? v.properties : v.elements).length === 0; };
    if (!ts.isCallExpression(init) || unwrap(init.expression).getText() !== 'useState' || (init.arguments[0] && !appMade(init.arguments[0], context) && !empty(init.arguments[0]))) return false;
    const setter = pattern.elements[1];
    if (!setter || !ts.isBindingElement(setter) || !ts.isIdentifier(setter.name)) return false;
    const targetValue = v => ts.isPropertyAccessExpression(v) && v.name.text === 'value' && ts.isPropertyAccessExpression(v.expression) && v.expression.name.text === 'target';
    const typed = v => {
      v = unwrap(v);
      if (targetValue(v) || appMade(v, context)) return true;
      // A const holding the field's own typing.
      const declaration = ts.isIdentifier(v) ? declarationOf(v, context) : null;
      return !!declaration && isConst(declaration) && !!declaration.initializer && targetValue(unwrap(declaration.initializer));
    };
    const update = arg => {
      arg = unwrap(arg);
      if (typed(arg) || (ts.isObjectLiteralExpression(arg) && arg.properties.length === 0)) return true;
      if (!(ts.isArrowFunction(arg) || ts.isFunctionExpression(arg)) || arg.parameters.length !== 1) return false;
      const own = arg.parameters[0].name.getText();
      if (ts.isBlock(arg.body)) {
        // Removing entries: `{ const next = { ...own }; delete next[key]; return next; }` and nothing else.
        const [copy, ...rest] = arg.body.statements;
        if (!copy || !ts.isVariableStatement(copy) || copy.declarationList.declarations.length !== 1) return false;
        const d = copy.declarationList.declarations[0], init = d.initializer && unwrap(d.initializer), local = d.name.getText();
        if (!init || !ts.isObjectLiteralExpression(init) || init.properties.length !== 1 || !ts.isSpreadAssignment(init.properties[0]) || unwrap(init.properties[0].expression).getText() !== own) return false;
        const last = rest.pop();
        return !!last && ts.isReturnStatement(last) && last.expression?.getText() === local
          && rest.every(st => ts.isExpressionStatement(st) && ts.isDeleteExpression(st.expression) && ts.isElementAccessExpression(st.expression.expression) && unwrap(st.expression.expression.expression).getText() === local);
      }
      const body = unwrap(arg.body);
      return ts.isObjectLiteralExpression(body) && body.properties.every(p => (ts.isSpreadAssignment(p) && unwrap(p.expression).getText() === own) || (ts.isPropertyAssignment(p) && typed(p.initializer)));
    };
    let ok = true;
    const walk = n => {
      if (!ok) return;
      if (ts.isIdentifier(n) && n.text === setter.name.text && n !== setter.name) {
        const call = n.parent;
        ok = ts.isCallExpression(call) && call.expression === n && call.arguments.length === 1 && update(call.arguments[0]);
      }
      ts.forEachChild(n, walk);
    };
    walk(context.sf);
    return ok;
  };
  // A spread of attributes: object literals (or a choice between them) whose shown attributes are App-made.
  const spreadMade = (expr, tag) => {
    expr = unwrap(expr);
    if (ts.isConditionalExpression(expr)) return spreadMade(expr.whenTrue, tag) && spreadMade(expr.whenFalse, tag);
    if (!ts.isObjectLiteralExpression(expr)) return false;
    return expr.properties.every(p => {
      if (!ts.isPropertyAssignment(p) || ts.isComputedPropertyName(p.name)) return false;
      const key = p.name.getText().replace(/^["']|["']$/g, '');
      if (!shownAttribute(key, tag)) return true;
      if (ID_ATTRIBUTES.has(key)) return idValue(p.initializer);
      return appMade(p.initializer, context);
    });
  };
  // An id or link target: App-made, an anchor builder, or a template of those.
  const idValue = expr => {
    const node = unwrap(expr);
    const anchorCall = n => { n = unwrap(n); return ts.isCallExpression(n) && ts.isIdentifier(unwrap(n.expression)) && isAnchor(context, unwrap(n.expression).text); };
    return anchorCall(node) || appMade(node, context) || (ts.isTemplateExpression(node) && node.templateSpans.every(span => anchorCall(span.expression) || appMade(span.expression, context)));
  };
  const visit = (node, inside = null) => {
    if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
      const opening = ts.isJsxElement(node) ? node.openingElement : node;
      const tag = opening.tagName.getText();
      const component = /^[A-Z]/.test(tag) || tag.includes('.');
      const trustedComponent = component && isTrusted(context, tag, 'components');
      attributes(tag, opening.attributes.properties, trustedComponent);
      // Inside a control or a heading, no presentation that may draw a box; a same-file component drawn there is
      // judged where its JSX is written, which the guard does not follow into this place, so it is listed or fails.
      if (inside && component) record(opening.tagName, `<${tag}> inside <${inside}>`, {component: true});
      if (component && !trustedComponent) {
        const declared = ts.isIdentifier(opening.tagName) ? declarationOf(opening.tagName, context) : null;
        const local = functionOf(opening.tagName, context) ?? (declared && ts.isClassDeclaration(declared) ? declared : null);
        const from = context.imports.get(tag);
        // A component in this file is judged where its JSX is written; one from another guarded view is judged
        // there. Any other component draws what it is given unseen: it is listed, with its reason, or it fails.
        if (!local && !(from && GUARDED_VIEWS.has(`${from.module.replace(/^\.\//, '')}.tsx`) && from.imported === tag)) record(opening.tagName, `<${tag}>`, {component: true});
      }
      const within = APP_ONLY.has(tag) ? tag : inside;
      if (ts.isJsxElement(node)) for (const child of node.children) visitChild(child, within);
      return;
    }
    if (ts.isJsxFragment(node)) { for (const child of node.children) visitChild(child, inside); return; }
    // Writes to the page outside React's rendering.
    if (ts.isBinaryExpression(node) && node.operatorToken.kind >= ts.SyntaxKind.FirstAssignment && node.operatorToken.kind <= ts.SyntaxKind.LastAssignment
      && (ts.isPropertyAccessExpression(node.left) && FORBIDDEN_PROPERTIES.has(node.left.name.text)
        || ts.isElementAccessExpression(node.left) && ts.isStringLiteralLike(node.left.argumentExpression) && FORBIDDEN_PROPERTIES.has(node.left.argumentExpression.text))) record(node, 'write to the page', {forbidden: true});
    if (ts.isCallExpression(node) && ts.isPropertyAccessExpression(node.expression) && FORBIDDEN_CALLS.has(node.expression.name.text)) record(node, 'write to the page', {forbidden: true});
    ts.forEachChild(node, child => visit(child, inside));
  };
  const visitChild = (child, inside) => {
    if (ts.isJsxExpression(child)) { if (child.expression) { drawn(child.expression); visit(child.expression, inside); } return; }
    if (ts.isJsxText(child)) return;
    visit(child, inside);
  };
  visit(sf);
  return out;
}

/** The views on which every supplied value takes an approved presentation. */
export const GUARDED_VIEWS = new Set(['RequestCards.tsx', 'NativeActivity.tsx', 'NativeHistory.tsx']);

/** One view's failures, given its source: each finding neither App-made nor listed, each forbidden write (never
 * listable), and the listed keys it used. */
export function sourceFailures(name, text, exceptions = []) {
  const listed = new Set(exceptions.map(e => `${e.file}|${e.where}|${normal(e.expr)}`));
  const failures = [], used = new Set();
  for (const f of findings(name, text)) {
    if (f.forbidden) { failures.push(`${name}:${f.line} ${f.where} ${f.expr} (cannot be listed)`); continue; }
    if (!f.component && f.where !== '{...}' && appMade(f.node, f.context)) continue;
    const key = `${name}|${f.where}|${f.expr}`;
    if (listed.has(key)) used.add(key); else failures.push(`${name}:${f.line} ${f.where} ${f.expr}`);
  }
  return {failures, used};
}

/** The failures across the guarded views, and each listed exception that no longer matches a failing finding. */
export function guardFailures(srcDir, exceptions, views = GUARDED_VIEWS) {
  const failures = [], used = new Set();
  for (const name of [...views].sort()) {
    const result = sourceFailures(name, readFileSync(new URL(name, srcDir), 'utf8'), exceptions);
    failures.push(...result.failures);
    for (const key of result.used) used.add(key);
  }
  for (const e of exceptions) { const key = `${e.file}|${e.where}|${normal(e.expr)}`; if (!used.has(key)) failures.push(`stale exception ${key}`); }
  return failures;
}

/** The word-table module holds only tables of literal words: each export a const object literal whose every value
 * is a string literal. */
export function wordTableFailures(srcDir) {
  const name = `${WORD_TABLE_MODULE.replace(/^\.\//, '')}.ts`;
  const sf = ts.createSourceFile(name, readFileSync(new URL(name, srcDir), 'utf8'), ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const failures = [];
  for (const statement of sf.statements) {
    const exported = statement.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword);
    if (!exported) { failures.push(`${name}: a statement that is not an exported table: ${normal(statement.getText()).slice(0, 80)}`); continue; }
    if (!ts.isVariableStatement(statement) || !(statement.declarationList.flags & ts.NodeFlags.Const)) { failures.push(`${name}: an export that is not a const table`); continue; }
    for (const d of statement.declarationList.declarations) {
      const value = d.initializer && unwrap(d.initializer);
      if (!value || !ts.isObjectLiteralExpression(value) || !value.properties.every(p => ts.isPropertyAssignment(p) && !ts.isComputedPropertyName(p.name) && ts.isStringLiteral(unwrap(p.initializer))))
        failures.push(`${name}: ${d.name.getText()} is not a table of literal words`);
    }
  }
  return failures;
}
