// For a mounted tree (tests/support/mini-dom.mjs): the conversation choices a view draws (ConversationChoices,
// src/AgentText.tsx), which radio button is chosen, and choosing one as a person's click would (its own onChange).
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const classes = node => (node.getAttribute?.('class') ?? '').split(' ');

/** Every conversation choice list inside a node, in document order. */
export const choiceLists = node => node.querySelectorAll(n => n.localName === 'fieldset' && classes(n).includes('conversation-choices'));
/** The legend's words of a choice list. */
export const legendOf = list => list.querySelectorAll(n => n.localName === 'legend')[0]?.textContent ?? '';
/** The choice list whose legend begins with these words. */
export const choiceList = (node, legend) => choiceLists(node).find(list => legendOf(list).startsWith(legend.trim()));
/** A list's radio buttons. */
export const radios = list => list.querySelectorAll(n => n.localName === 'input' && props(n)?.type === 'radio');
/** The key of the chosen radio button, or "" when none is chosen. */
export const chosenIn = list => { const chosen = radios(list).find(r => props(r).checked === true); return chosen ? props(chosen).value : ''; };
/** The radio button submitting this key's own change handler, as a click on it would call it; there must be one. */
export function chooser(list, key) {
  const radio = radios(list).find(r => props(r).value === key);
  if (!radio) throw new Error(`no conversation choice with the key ${JSON.stringify(key)}`);
  const onChange = props(radio).onChange;
  return () => onChange({target: {value: key, checked: true}});
}
/** Choose the radio button submitting this key; there must be one. Returns what its onChange returns. */
export const chooseIn = (list, key) => chooser(list, key)();
/** The keys offered, in order. */
export const keysIn = list => radios(list).map(r => props(r).value);
/** The row of the choice submitting this key: its radio button and label, and what stands beside them. */
export const rowOf = (list, key) => list.querySelectorAll(n => classes(n).includes('conversation-choice')).find(row => radios(row).some(r => props(r).value === key));
/** The words of the label naming the choice submitting this key (the radio button's accessible name). */
export const labelOf = (list, key) => rowOf(list, key)?.querySelectorAll(n => n.localName === 'label')[0]?.textContent.trim();

// For rendered markup (renderToStaticMarkup): each radio button of a choice list with its submitted key, whether it
// is chosen, and its label's words.
const unescape = text => text.replace(/<!-- -->/g, '').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
export const choicesInMarkup = html => [...html.matchAll(/<label><input type="radio"([^>]*)\/>(.*?)<\/label>/g)].map(([, attributes, label]) => ({
  key: unescape(attributes.match(/ value="([^"]*)"/)?.[1] ?? ''), chosen: / checked=""/.test(attributes), label: unescape(label).trim(),
}));
/** The chosen radio button's key and label in rendered markup, or null when none is chosen. */
export const chosenInMarkup = html => choicesInMarkup(html).find(choice => choice.chosen) ?? null;
