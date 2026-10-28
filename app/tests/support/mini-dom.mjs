// A minimal in-memory document, enough for react-dom/client to mount, update
// and remove the App's plain elements in Node tests. It has no layout, no
// events beyond registration and no CSS; it exists so a test can observe what
// React actually leaves in the tree after a re-render (no DOM package is
// installed and none is downloaded).

class Node {
  constructor(ownerDocument, nodeType, nodeName) {
    this.ownerDocument = ownerDocument; this.nodeType = nodeType; this.nodeName = nodeName;
    this.childNodes = []; this.parentNode = null; this.listeners = [];
  }
  get firstChild() { return this.childNodes[0] ?? null; }
  get lastChild() { return this.childNodes[this.childNodes.length - 1] ?? null; }
  get nextSibling() { const s = this.parentNode?.childNodes; return s ? s[s.indexOf(this) + 1] ?? null : null; }
  get previousSibling() { const s = this.parentNode?.childNodes; return s ? s[s.indexOf(this) - 1] ?? null : null; }
  appendChild(child) { return this.insertBefore(child, null); }
  insertBefore(child, before) {
    if (child.parentNode) child.parentNode.removeChild(child);
    const at = before ? this.childNodes.indexOf(before) : -1;
    if (at < 0) this.childNodes.push(child); else this.childNodes.splice(at, 0, child);
    child.parentNode = this; return child;
  }
  removeChild(child) {
    const at = this.childNodes.indexOf(child);
    if (at < 0) throw new Error('removeChild: not a child');
    this.childNodes.splice(at, 1); child.parentNode = null; return child;
  }
  contains(other) { for (let n = other; n; n = n.parentNode) if (n === this) return true; return false; }
  addEventListener(type, listener, options) { this.listeners.push({ type, listener, options }); }
  removeEventListener(type, listener) { this.listeners = this.listeners.filter(l => l.type !== type || l.listener !== listener); }
  get textContent() { return this.childNodes.map(c => c.textContent).join(''); }
  set textContent(value) {
    for (const c of this.childNodes) c.parentNode = null;
    this.childNodes = [];
    if (value !== '' && value !== null && value !== undefined) this.appendChild(this.ownerDocument.createTextNode(String(value)));
  }
}

class Text extends Node {
  constructor(doc, data) { super(doc, 3, '#text'); this.nodeValue = data; }
  get data() { return this.nodeValue; } set data(v) { this.nodeValue = v; }
  get textContent() { return this.nodeValue; } set textContent(v) { this.nodeValue = String(v); }
}

class Comment extends Node {
  constructor(doc, data) { super(doc, 8, '#comment'); this.nodeValue = data; }
  get textContent() { return ''; } set textContent(_v) {}
}

class Element extends Node {
  constructor(doc, tagName, namespaceURI = 'http://www.w3.org/1999/xhtml') {
    super(doc, 1, tagName.toUpperCase());
    this.tagName = tagName.toUpperCase(); this.localName = tagName.toLowerCase(); this.namespaceURI = namespaceURI;
    this.attributes = new Map(); this.style = { setProperty(name, value) { this[name] = value; }, removeProperty(name) { delete this[name]; } };
  }
  setAttribute(name, value) { this.attributes.set(String(name).toLowerCase(), String(value)); }
  setAttributeNS(_ns, name, value) { this.setAttribute(name, value); }
  getAttribute(name) { return this.attributes.has(String(name).toLowerCase()) ? this.attributes.get(String(name).toLowerCase()) : null; }
  hasAttribute(name) { return this.attributes.has(String(name).toLowerCase()); }
  removeAttribute(name) { this.attributes.delete(String(name).toLowerCase()); }
  removeAttributeNS(_ns, name) { this.removeAttribute(name); }
  get options() { return this.querySelectorAll(e => e.localName === 'option'); }
  /** Depth-first descendants matching a predicate. */
  querySelectorAll(match) {
    const out = []; const walk = n => { for (const c of n.childNodes) { if (c.nodeType === 1 && match(c)) out.push(c); walk(c); } };
    walk(this); return out;
  }
}

class OptionElement extends Element {
  get value() { return this.hasAttribute('value') ? this.getAttribute('value') : this.textContent; }
  set value(v) { this.setAttribute('value', v); }
}

class Document extends Node {
  constructor() {
    super(null, 9, '#document'); this.ownerDocument = null;
    this.documentElement = this.createElement('html'); this.appendChild(this.documentElement);
    this.body = this.createElement('body'); this.documentElement.appendChild(this.body);
  }
  createElement(tag) { return tag.toLowerCase() === 'option' ? new OptionElement(this, tag) : new Element(this, tag); }
  createElementNS(ns, tag) { return new Element(this, tag, ns); }
  createTextNode(data) { return new Text(this, data); }
  createComment(data) { return new Comment(this, data); }
  get activeElement() { return this.body; }
}

/** Installs a fresh document as the global `window.document` for react-dom. */
export function installMiniDom() {
  const document = new Document();
  const window = { document, event: undefined, addEventListener() {}, removeEventListener() {}, navigator: { userAgent: 'node' }, HTMLIFrameElement: class {}, location: { protocol: 'file:' } };
  document.defaultView = window;
  Object.assign(globalThis, { window, document, IS_REACT_ACT_ENVIRONMENT: true });
  return document;
}
