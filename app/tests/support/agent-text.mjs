// Reads rendered markup with each AgentText box (src/AgentText.tsx) and each AgentProse box written as
// ⟦label value⟧, its marks as shown and a block's lines joined by line breaks
// without their numbers, so assertions can say where the agent's text sits
// beside the App's words. A box this cannot read is left as markup.
const attr = '="[^"]*"';
const mark = `<span class="agent-text-mark" style${attr}>([^<]*)</span>`;
const valueText = value => value.replace(new RegExp(mark, 'g'), '$1');
const inline = new RegExp(`<span role="group" aria-label${attr} class="agent-text" style${attr}><span class="agent-text-label" style${attr}>([^<]*)</span> <span class="agent-text-value" style${attr}>((?:[^<]|${mark.replace('([^<]*)', '[^<]*')})*)</span></span>`, 'g');
const line = `<div class="agent-text-line"><span class="agent-text-line-number" style${attr}>\\d+</span>((?:[^<]|${mark.replace('([^<]*)', '[^<]*')})*)</div>`;
const block = new RegExp(`<div role="group" aria-label${attr} class="agent-text agent-text-block" style${attr}><div class="agent-text-label" style${attr}>([^<]*)</div><div class="agent-text-value" style${attr}>((?:${line.replace('((?:', '(?:').replace(')*)</div>', ')*</div>')})*)</div></div>`, 'g');

// An AgentProse box (an agent's message in the transcript) or a PersonText box (the person's own message there): its
// rendered text kept as markup inside ⟦label: …⟧, its marks as shown. The box holds no div, so it ends at the first closing div.
const prose = new RegExp(`<div role="group" aria-label="([^"]*)" class="agent-prose (?:chat-markdown|person-text)">((?:(?!</div>)[\\s\\S])*)</div>`, 'g');

export function agentPlain(html) {
  return html
    .replace(prose, (_, label, inner) => `⟦${label}: ${valueText(inner)}⟧`)
    .replace(block, (_, label, lines) => `⟦${label}\n${[...lines.matchAll(new RegExp(line, 'g'))].map(m => valueText(m[1]).replace(/⏎$/, '')).join('\n')}⟧`)
    .replace(inline, (_, label, value) => `⟦${label} ${valueText(value)}⟧`);
}

/** The accessibility names of every AgentText box in the markup. */
export const agentBoxNames = html => [...html.matchAll(/<(?:span|div) role="group" aria-label="([^"]*)" class="agent-(?:text|prose)/g)].map(m => m[1]);

// For a mounted tree (tests/support/mini-dom.mjs): the AgentText blocks (block text, recorded text, recorded data)
// inside a node, and a block's text read back as it was given (its label, line numbers and line-break marks taken
// away; marks standing for control or format characters stay as shown).
const classes = node => (node.getAttribute?.('class') ?? '').split(' ');
export const agentBlocks = node => node.querySelectorAll(n => classes(n).includes('agent-text-block'));
export function agentBlockText(block) {
  return block.querySelectorAll(n => classes(n).includes('agent-text-line'))
    .map(line => line.childNodes.filter(c => !classes(c).includes('agent-text-line-number')).map(c => c.textContent).join('').replace(/⏎$/, ''))
    .join('\n');
}
