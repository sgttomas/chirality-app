// The presentation guard: a syntactic check, on each guarded view (GUARDED_VIEWS), of the forms listed below, under
// named assumptions. Its aim is that a value the App did not write reaches the page only through one of the approved
// presentations, and that a control or heading holds only the App's words; it does not prove that page property. It
// checks the forms it knows, and its known limitations are listed below. The page property rests on the rendered
// regression in presentation-guard.test.mjs and on review.
//
// It parses each guarded view with the TypeScript parser and its checker, one file at a time, and judges an
// identifier by the declaration it resolves to in that file, never by its name: an approved presentation (TRUSTED)
// is recognised only where the identifier is bound to the import of that name from its module, so a local, a
// parameter or a destructured prop that shadows the name is not. It looks at
//   - every expression drawn as a child of an element, anywhere in the view;
//   - every attribute that names, describes or holds a value: title, alt, placeholder, label, a text field's value
//     and defaultValue, and every aria- attribute; and every attribute of an approved presentation other than the
//     value it presents;
//   - aria-labelledby, aria-describedby, aria-details and aria-errormessage, which pass only as a literal list of
//     ids each naming exactly one element written in the same file whose content is only the App's words;
//   - the contents of every attribute: an element written in an attribute is judged where it is written, a
//     children attribute is judged as drawn, and a function in an attribute (an event handler, a ref callback) is
//     searched for writes to the page like the rest of the view;
//   - every spread of attributes, which passes only as object literals whose keys are on SPREAD_KEYS (apart from a
//     listed exception, with its reason); a key written as a name, a string or a computed string literal is read as
//     that key; a computed key that is not a literal fails as an ordinary finding;
//   - the elements that hold only the App's words (APP_ONLY tags, and any element whose role, read as a
//     space-separated list of tokens, holds a token in APP_ONLY_ROLES: a heading or a control role), in which no
//     approved presentation that may draw a box is allowed; a role attribute not built of literals fails;
//   - every component the view draws: one written in this file is judged where its JSX is written, one imported
//     from another guarded view is judged in that view, and any other fails unless it is listed.
// An expression passes only if it is built from the closed list of forms below (appMade); anything else fails,
// including a form the guard has never seen. That is a syntactic default, not a proof of where a value came from.
// These fail and cannot be listed: raw HTML (dangerouslySetInnerHTML) as an attribute, or in a spread under a name, a
// string or a computed string-literal key; an assignment to a property in FORBIDDEN_PROPERTIES (element text, value,
// id and the like) written as a direct property access or a string-literal element access; a call of a method in
// FORBIDDEN_CALLS.
// A listed exception (presentation-guard-exceptions.json) names one expression exactly, with its reason. A listed
// exception whose expression no longer appears as a failing finding is itself a failure. That detects the
// expression disappearing; it does not detect its reason becoming untrue: if the code that produces an excepted
// value changes (a notice factory that starts copying supplied text, a listed constant that is replaced), the guard
// still passes. Each reason is checked by reading that code.
//
// Known limitations include, by design of a one-file syntactic check:
//   - a const table or object field mutated after its declaration (the guard reads the initializer);
//   - a fabricated event object: a field's state counts as the person's typing when it is set from any
//     `<x>.target.value`, whatever made `<x>`;
//   - data read back from the DOM through a ref (an attribute or text read from an element and drawn);
//   - numbers taken by method name: a .map or .flatMap callback's second argument, and the result of findIndex,
//     indexOf, lastIndexOf or findLastIndex, even when the method is a supplied object's own;
//   - a write to the page through a computed property name held in a variable, or through Object.assign;
//   - raw HTML in a spread under a computed key that is not a literal: it fails as an ordinary finding, so an
//     exception listed for it would rest on its reviewed reason alone.
// It does not prove what an approved presentation does with its value: those are the examined implementations
// named in TRUSTED (AgentText.tsx), and their own tests show what they draw. The rendered regression in
// presentation-guard.test.mjs draws the views on valid fixtures with each enumerated leaf and key poisoned in turn;
// it covers those fixtures, not every shape or state a host could send.
import ts from 'typescript';
import {readFileSync} from 'node:fs';

/** The approved presentations, by the module they must be imported from under these names. */
export const TRUSTED = {
  './AgentText': {
    // Functions whose result is the App's words, a checked identifier or a checked number: plainId (an identifier
    // checked against PLAIN_ID, else null) and idWords (the same, else fixed App words); wordOf (the App's word for a key of the App's own
    // table, else null); numberWords (a finite number, else null); isoSeconds (a valid time in seconds, as ISO 8601);
    // clockWords (a time the App holds, as HH:MM:SS; non-finite or invalid gives null).
    functions: ['plainId', 'idWords', 'wordOf', 'numberWords', 'isoSeconds', 'clockWords'],
    // Components that draw a supplied value: boxed, or as the App's words only for a value they check at run time.
    components: ['AgentText', 'SuppliedId', 'Word', 'Num', 'Flag'],
  },
};
/** Anchor builders: an element id made from a supplied identity as a 32-bit FNV-style hash of its serialized form
 * plus that form's length, both in base 36 (letters and digits only), never shown as text. Trusted only in attributes
 * that hold an id or a link target. */
export const ANCHOR_FUNCTIONS = {'./NativeActivity': ['itemAnchorId', 'requestAnchorId']};
const ID_ATTRIBUTES = new Set(['id', 'href', 'htmlFor', 'aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-owns', 'aria-activedescendant', 'aria-details', 'aria-errormessage', 'aria-flowto']);
const VALUE_ATTRIBUTES = new Set(['title', 'alt', 'placeholder', 'label']);
/** A value attribute is drawn only by a text field; an option's, a select's or a button's value is not shown. */
const DRAWN_VALUE_TAGS = new Set(['input', 'textarea']);
const shownAttribute = (name, tag) => VALUE_ATTRIBUTES.has(name) || name.startsWith('aria-') || ID_ATTRIBUTES.has(name) || (['value', 'defaultValue'].includes(name) && DRAWN_VALUE_TAGS.has(tag));
/** Attributes of an approved presentation that only style or key it. */
const STYLE_ATTRIBUTES = new Set(['style', 'key', 'className', 'block']);
/** Property writes and calls that put text or markup on the page outside React's rendering. */
const FORBIDDEN_PROPERTIES = new Set(['innerHTML', 'outerHTML', 'textContent', 'innerText', 'outerText', 'nodeValue', 'value', 'defaultValue', 'placeholder', 'title', 'data', 'id']);
/** Attributes that name or describe an element by another's id: only a literal id of an App-only element passes. */
const REFERENCE_ATTRIBUTES = new Set(['aria-labelledby', 'aria-describedby', 'aria-details', 'aria-errormessage']);
/** The only keys a spread of attributes may carry; any other key (children, a ref, an event handler, a value, raw
 * HTML) fails, and raw HTML cannot be listed. */
const SPREAD_KEYS = new Set(['id', 'key', 'className', 'style', 'hidden', 'disabled', 'tabIndex', 'title', 'alt', 'placeholder', 'aria-label', 'aria-hidden']);
const FORBIDDEN_CALLS = new Set(['insertAdjacentHTML', 'insertAdjacentText', 'insertAdjacentElement', 'write', 'writeln', 'setAttribute', 'setAttributeNS', 'createTextNode', 'append', 'prepend', 'appendChild', 'insertBefore', 'replaceChildren', 'replaceWith', 'before', 'after', 'execCommand', 'setHTMLUnsafe', 'createContextualFragment']);

const normal = text => text.replace(/\s+/g, ' ').trim();
/** Elements whose content is a control's or a heading's name: they hold only the App's words, never a box, so an
 * approved presentation that can draw a supplied value boxed is not allowed inside them. */
export const APP_ONLY = new Set(['button', 'a', 'summary', 'label', 'legend', 'option', 'select', 'textarea', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']);
/** Roles that make any element a control or a heading: such an element holds only the App's words, as the tags do. */
export const APP_ONLY_ROLES = new Set(['heading', 'button', 'link', 'checkbox', 'radio', 'menuitem', 'menuitemcheckbox', 'menuitemradio', 'option', 'tab', 'switch',
  'textbox', 'searchbox', 'combobox', 'slider', 'spinbutton', 'treeitem', 'columnheader', 'rowheader']);

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

/** The import an identifier is bound to, by its declaration: { module, imported } when the identifier resolves to an
 * import specifier of this file, else null. A local, a parameter or a destructured prop that shadows an imported
 * name resolves to its own declaration, so it is never taken for the import, whatever its name. */
function importOf(node, context) {
  node = node && unwrap(node);
  if (!node || !ts.isIdentifier(node)) return null;
  const declaration = context.checker.getSymbolAtLocation(node)?.declarations?.[0];
  if (!declaration || !ts.isImportSpecifier(declaration) || declaration.isTypeOnly) return null;
  const statement = declaration.parent?.parent?.parent;
  if (!statement || !ts.isImportDeclaration(statement) || !ts.isStringLiteral(statement.moduleSpecifier) || statement.importClause?.isTypeOnly) return null;
  return {module: statement.moduleSpecifier.text, imported: (declaration.propertyName ?? declaration.name).text};
}
/** Whether an identifier is bound to the import of an approved presentation under its own name. */
const isTrusted = (context, node, kind) => {
  const from = importOf(node, context);
  return !!from && from.imported === node.text && (TRUSTED[from.module]?.[kind] ?? []).includes(node.text);
};
const isAnchor = (context, node) => {
  if (!ts.isIdentifier(node)) return false;
  const from = importOf(node, context);
  if (from) return from.imported === node.text && (ANCHOR_FUNCTIONS[from.module] ?? []).includes(node.text);
  // In the module that defines them: the identifier must resolve to that module's own top-level const.
  const declaration = declarationOf(node, context);
  return !!declaration && isConst(declaration) && declaration.parent.parent?.parent === context.sf
    && Object.entries(ANCHOR_FUNCTIONS).some(([module, names]) => `${module.replace(/^\.\//, '')}.tsx` === context.name && names.includes(node.text));
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
  const from = importOf(node, context);
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
    if (ts.isIdentifier(callee) && isTrusted(context, callee, 'functions')) {
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
  const context = {name, sf, checker, seen: new Set()};
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
      if (ts.isJsxSpreadAttribute(a)) {
        const verdict = spreadVerdict(a.expression, tag);
        if (verdict === 'forbidden') record(a.expression, '{...} with dangerouslySetInnerHTML', {forbidden: true});
        else if (verdict !== 'ok') record(a.expression, '{...}');
        continue;
      }
      const attribute = a.name.getText();
      if (attribute === 'dangerouslySetInnerHTML') { record(a, '@dangerouslySetInnerHTML', {forbidden: true}); continue; }
      // A reference that names or describes an element: only a literal id of an element in this file that holds
      // only the App's words.
      if (REFERENCE_ATTRIBUTES.has(attribute)) { if (!referenceMade(a.initializer)) record(a.initializer ?? a.name, `@${attribute}`, {rule: true}); continue; }
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
  // A spread of attributes: object literals (or a choice between them) whose every key is on SPREAD_KEYS and whose
  // shown attributes are App-made: 'ok'; raw HTML anywhere in it: 'forbidden'; anything else: 'fail'.
  const spreadVerdict = (expr, tag) => {
    expr = unwrap(expr);
    if (ts.isConditionalExpression(expr)) {
      const both = [spreadVerdict(expr.whenTrue, tag), spreadVerdict(expr.whenFalse, tag)];
      return both.includes('forbidden') ? 'forbidden' : both.every(v => v === 'ok') ? 'ok' : 'fail';
    }
    if (!ts.isObjectLiteralExpression(expr)) return 'fail';
    let verdict = 'ok';
    for (const p of expr.properties) {
      // A key written as a name, a string, or a computed string literal (["dangerouslySetInnerHTML"]) is read as that
      // key; a computed key that is not a literal is unknown, and fails.
      const computed = p.name && ts.isComputedPropertyName(p.name) ? unwrap(p.name.expression) : null;
      const key = !p.name ? null : computed ? (ts.isStringLiteral(computed) || ts.isNoSubstitutionTemplateLiteral(computed) ? computed.text : null) : p.name.getText().replace(/^["']|["']$/g, '');
      if (key === 'dangerouslySetInnerHTML') return 'forbidden';
      if (!ts.isPropertyAssignment(p) || key === null || !SPREAD_KEYS.has(key)) { verdict = 'fail'; continue; }
      if (!shownAttribute(key, tag)) continue;
      if (!(ID_ATTRIBUTES.has(key) ? idValue(p.initializer) : appMade(p.initializer, context))) verdict = 'fail';
    }
    return verdict;
  };
  // Elements by the literal id they carry, for the reference attributes.
  const literalIds = new Map();
  const literalText = initializer => {
    if (!initializer) return null;
    if (ts.isStringLiteral(initializer)) return initializer.text;
    const e = ts.isJsxExpression(initializer) && initializer.expression ? unwrap(initializer.expression) : null;
    return e && (ts.isStringLiteral(e) || ts.isNoSubstitutionTemplateLiteral(e)) ? e.text : null;
  };
  const openingOf = node => ts.isJsxElement(node) ? node.openingElement : node;
  (function index(node) {
    if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
      const id = openingOf(node).attributes.properties.find(a => ts.isJsxAttribute(a) && a.name.getText() === 'id');
      const value = id ? literalText(id.initializer) : null;
      if (value !== null) literalIds.set(value, [...(literalIds.get(value) ?? []), node]);
    }
    ts.forEachChild(node, index);
  })(sf);
  // An element whose content is only the App's words: plain elements, App-made text, no component (an approved
  // presentation may draw a box), no ref, no spread and no raw HTML anywhere in it.
  const appOnlyContent = node => {
    const opening = openingOf(node);
    if (/^[A-Z]/.test(opening.tagName.getText()) || opening.tagName.getText().includes('.')) return false;
    if (opening.attributes.properties.some(a => ts.isJsxSpreadAttribute(a) || ['ref', 'dangerouslySetInnerHTML', 'children'].includes(a.name.getText()))) return false;
    if (!ts.isJsxElement(node)) return true;
    return node.children.every(child => ts.isJsxText(child)
      || (ts.isJsxExpression(child) ? !child.expression || (!hasJsx(child.expression) && appMade(child.expression, context))
        : (ts.isJsxElement(child) || ts.isJsxSelfClosingElement(child)) && appOnlyContent(child)));
  };
  // aria-labelledby, aria-describedby…: a literal list of ids, each naming exactly one element in this file whose
  // content is only the App's words. Anything else fails.
  const referenceMade = initializer => {
    const value = literalText(initializer);
    const ids = value === null ? [] : value.trim().split(/\s+/).filter(Boolean);
    return ids.length > 0 && ids.every(id => (literalIds.get(id) ?? []).length === 1 && appOnlyContent(literalIds.get(id)[0]));
  };
  // The roles an element's role attribute can take: its literal values; null when it is not built of literals.
  const rolesOf = opening => {
    const attribute = opening.attributes.properties.find(a => ts.isJsxAttribute(a) && a.name.getText() === 'role');
    if (!attribute) return [];
    if (attribute.initializer && ts.isStringLiteral(attribute.initializer)) return [attribute.initializer.text];
    const literals = e => {
      e = unwrap(e);
      if (ts.isStringLiteral(e) || ts.isNoSubstitutionTemplateLiteral(e)) return [e.text];
      if (ts.isConditionalExpression(e)) { const a = literals(e.whenTrue), b = literals(e.whenFalse); return a && b ? [...a, ...b] : null; }
      if (ts.isBinaryExpression(e) && e.operatorToken.kind === ts.SyntaxKind.AmpersandAmpersandToken) return literals(e.right);
      if (e.kind === ts.SyntaxKind.UndefinedKeyword || (ts.isIdentifier(e) && e.text === 'undefined')) return [];
      return null;
    };
    return attribute.initializer && ts.isJsxExpression(attribute.initializer) && attribute.initializer.expression ? literals(attribute.initializer.expression) : null;
  };
  // An id or link target: App-made, an anchor builder, or a template of those.
  const idValue = expr => {
    const node = unwrap(expr);
    const anchorCall = n => { n = unwrap(n); return ts.isCallExpression(n) && ts.isIdentifier(unwrap(n.expression)) && isAnchor(context, unwrap(n.expression)); };
    return anchorCall(node) || appMade(node, context) || (ts.isTemplateExpression(node) && node.templateSpans.every(span => anchorCall(span.expression) || appMade(span.expression, context)));
  };
  const visit = (node, inside = null) => {
    if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
      const opening = ts.isJsxElement(node) ? node.openingElement : node;
      const tag = opening.tagName.getText();
      const component = /^[A-Z]/.test(tag) || tag.includes('.');
      const trustedComponent = component && ts.isIdentifier(opening.tagName) && isTrusted(context, opening.tagName, 'components');
      attributes(tag, opening.attributes.properties, trustedComponent);
      // Inside a control or a heading, no presentation that may draw a box; a same-file component drawn there is
      // judged where its JSX is written, which the guard does not follow into this place, so it is listed or fails.
      if (inside && component) record(opening.tagName, `<${tag}> inside <${inside}>`, {component: true});
      if (component && !trustedComponent) {
        const declared = ts.isIdentifier(opening.tagName) ? declarationOf(opening.tagName, context) : null;
        const local = functionOf(opening.tagName, context) ?? (declared && ts.isClassDeclaration(declared) ? declared : null);
        const from = importOf(opening.tagName, context);
        // A component in this file is judged where its JSX is written; one from another guarded view is judged
        // there. Any other component draws what it is given unseen: it is listed, with its reason, or it fails.
        if (!local && !(from && GUARDED_VIEWS.has(`${from.module.replace(/^\.\//, '')}.tsx`) && from.imported === tag)) record(opening.tagName, `<${tag}>`, {component: true});
      }
      // A role that makes the element a control or a heading counts as that element; a role not built of literals
      // cannot be judged and fails.
      const roles = rolesOf(opening);
      if (roles === null) record(opening.tagName, `<${tag}> with a role not built of literals`, {rule: true});
      // A role value is a space-separated list of tokens ("heading note"): any token that is a control or heading role counts.
      const role = (roles ?? []).flatMap(r => r.trim().split(/\s+/)).find(r => APP_ONLY_ROLES.has(r));
      const within = APP_ONLY.has(tag) ? tag : role ? `role="${role}"` : inside;
      // Attribute contents are visited as children are: an element written in an attribute (a children attribute, a
      // render prop) is judged where it is written, and a function in an attribute (an event handler, a ref
      // callback) is searched for writes to the page. A children attribute is drawn.
      for (const a of opening.attributes.properties) {
        const init = ts.isJsxSpreadAttribute(a) ? a.expression : a.initializer;
        const expr = !init || ts.isStringLiteral(init) ? null : ts.isJsxExpression(init) ? init.expression : init;
        if (!expr) continue;
        if (ts.isJsxAttribute(a) && a.name.getText() === 'children' && !trustedComponent) drawn(expr);
        visit(expr, within);
      }
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
export const GUARDED_VIEWS = new Set(['RequestCards.tsx', 'NativeActivity.tsx', 'NativeHistory.tsx', 'RunOffers.tsx']);

/** One view's failures, given its source: each finding neither App-made nor listed, each forbidden write (never
 * listable), and the listed keys it used. */
export function sourceFailures(name, text, exceptions = []) {
  const listed = new Set(exceptions.map(e => `${e.file}|${e.where}|${normal(e.expr)}`));
  const failures = [], used = new Set();
  for (const f of findings(name, text)) {
    if (f.forbidden) { failures.push(`${name}:${f.line} ${f.where} ${f.expr} (cannot be listed)`); continue; }
    // A finding that breaks a rule (an unseen component, a spread, a reference, a role) fails whatever its expression.
    if (!f.component && !f.rule && f.where !== '{...}' && appMade(f.node, f.context)) continue;
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
