// For a mounted App (tests/support/mini-dom.mjs): the conversation view as the person meets it, the centre
// (#conversation: the transcript, the composer and the settings line) and the conversation's tools in the right
// panel's "Conversation tools" tab (#conversation-tools-content), read as one node. Where the conversation view is
// mounted on its own, its tools are drawn inside it, and the centre alone is that node.
const byId = (container, id) => container.querySelectorAll(node => node.getAttribute?.('id') === id)[0];

export function conversationView(container) {
  const centre = byId(container, 'conversation');
  if (!centre) return undefined;
  const tools = byId(container, 'conversation-tools-content');
  if (!tools || centre.contains(tools)) return centre;
  const parts = [centre, tools];
  return {
    querySelectorAll: match => parts.flatMap(part => part.querySelectorAll(match)),
    get textContent() { return parts.map(part => part.textContent).join(''); },
    getAttribute: name => centre.getAttribute(name),
    contains: node => parts.some(part => part.contains(node)),
    get childNodes() { return parts; },
    localName: 'div',
  };
}
/** The centre alone: the transcript, the composer and its dock, and the settings line. */
export const conversationCentre = container => byId(container, 'conversation');
/** The conversation's tools, wherever they are drawn. */
export const conversationTools = container => byId(container, 'conversation-tools-content');
/** The conversation's message field (the composer's text area, "Chat input"). */
export const chatInput = container => byId(container, 'ordinary-composer-text');
/** The left region's "New chat": the empty conversation, no conversation chosen. */
export const newChatButton = container => container.querySelectorAll(node => node.localName === 'button' && node.getAttribute('class') === 'woven-new-chat')[0];
/** The composer's Send (its aria-label is "Send text", or "Send text only" with attachments selected). */
export const sendButton = container => byId(container, 'conversation')?.querySelectorAll(node => node.localName === 'button' && node.getAttribute('type') === 'submit')[0];
/** A button by its shown text or, for an icon button, its accessible name. */
export const named = (node, label) => node.textContent === label || node.getAttribute?.('aria-label') === label;
const reactProps = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
/**
 * The new conversation's start as a person makes it: "New chat", the first message in the message box (left as it is
 * when it already holds text), then Send, which runs thread_start and, on a confirmed start, the ordinary send.
 */
export async function startWithFirstMessage(container, act, { text = 'First message', newChat = true } = {}) {
  if (newChat) await act(async () => { reactProps(newChatButton(container)).onClick(); });
  const field = chatInput(container);
  if (!reactProps(field).value) await act(async () => { reactProps(field).onChange({ target: { value: text } }); });
  const send = sendButton(container);
  if (reactProps(send).disabled) return false;
  await act(async () => { reactProps(send).onClick(); });
  return true;
}
/** The settings line under the composer ("Chat context"). */
export const settingsLine = container => container.querySelectorAll(node => node.getAttribute?.('aria-label') === 'Chat context')[0];
/** A settings-line button by the start of its accessible name: "Role", "Mode", "Access level", "Model", "Reasoning effort". */
export const settingButton = (container, name) => settingsLine(container)?.querySelectorAll(node => node.localName === 'button' && ((node.getAttribute('aria-label') ?? '').startsWith(`${name}:`) || (node.getAttribute('aria-label') ?? '').startsWith(`${name}, as `)))[0];
/** Opens a settings-line panel, as a person pressing its button; an open panel is left open. */
export async function openSetting(container, act, name) {
  const control = settingButton(container, name);
  if (!control) throw Error(`no ${name} setting in the settings line`);
  if (reactProps(control)['aria-expanded']) return;
  await act(async () => { reactProps(control).onClick(); });
}
/** Whether a node is in view: no ancestor of it is hidden (a closed panel, a folded entry), and none is a closed
 * disclosure holding it outside its summary. */
export const inView = node => {
  for (let n = node, child = null; n; child = n, n = n.parentNode) {
    if (reactProps(n)?.hidden || n.hasAttribute?.('hidden')) return false;
    if (n.localName === 'details' && child && child.localName !== 'summary' && !(n.open ?? n.hasAttribute('open'))) return false;
  }
  return !!node;
};
/** The settings line's panel by its name ("Role", "Mode", "Access level", "Model", "Reasoning effort"). */
export const settingPanel = (container, name) => settingsLine(container)?.querySelectorAll(node => node.getAttribute?.('role') === 'dialog' && node.getAttribute('aria-label') === name)[0];
/**
 * A control in a settings-line panel as a person reaches it: the panel opened by its button first, then the control
 * found inside that panel, which must be in view. `match` picks the control among the panel's elements.
 */
export async function inSetting(container, act, name, match) {
  await openSetting(container, act, name);
  const panel = settingPanel(container, name);
  if (!panel || !inView(panel)) throw Error(`the ${name} panel is not in view after its button was pressed`);
  const found = panel.querySelectorAll(match)[0];
  if (found && !inView(found)) throw Error(`the control found in the ${name} panel is not in view`);
  return found;
}
/** The new conversation's typed model field, reached as a person reaches it: the settings line's Model panel opened,
 * then its "Advanced: enter a model ID yourself" disclosure opened (its summary pressed), then the field, in view. */
export async function startModelField(container, act) {
  const advanced = await inSetting(container, act, 'Model', node => node.localName === 'details' && node.querySelectorAll(n => n.localName === 'summary')[0]?.textContent === 'Advanced: enter a model ID yourself');
  if (!advanced) throw Error('no "Advanced: enter a model ID yourself" in the open Model panel');
  if (!(advanced.open ?? advanced.hasAttribute('open'))) await act(async () => { advanced.open = true; });
  const field = advanced.querySelectorAll(node => node.localName === 'input' && node.parentNode?.textContent?.startsWith('Model '))[0];
  if (!field || !inView(field)) throw Error('the model field is not in view in the open Model panel');
  return field;
}
