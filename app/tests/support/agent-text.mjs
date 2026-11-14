// Reads rendered markup with each AgentText box (src/AgentText.tsx) written as
// ⟦label value⟧, its marks as shown and a block's lines joined by line breaks
// without their numbers, so assertions can say where the agent's text sits
// beside the App's words. A box this cannot read is left as markup.
const attr = '="[^"]*"';
const mark = `<span class="agent-text-mark" style${attr}>([^<]*)</span>`;
const valueText = value => value.replace(new RegExp(mark, 'g'), '$1');
const inline = new RegExp(`<span role="group" aria-label${attr} class="agent-text" style${attr}><span class="agent-text-label" style${attr}>([^<]*)</span> <span class="agent-text-value" style${attr}>((?:[^<]|${mark.replace('([^<]*)', '[^<]*')})*)</span></span>`, 'g');
const line = `<div class="agent-text-line"><span class="agent-text-line-number" style${attr}>\\d+</span>((?:[^<]|${mark.replace('([^<]*)', '[^<]*')})*)</div>`;
const block = new RegExp(`<div role="group" aria-label${attr} class="agent-text agent-text-block" style${attr}><div class="agent-text-label" style${attr}>([^<]*)</div><div class="agent-text-value" style${attr}>((?:${line.replace('((?:', '(?:').replace(')*)</div>', ')*</div>')})*)</div></div>`, 'g');

export function agentPlain(html) {
  return html
    .replace(block, (_, label, lines) => `⟦${label}\n${[...lines.matchAll(new RegExp(line, 'g'))].map(m => valueText(m[1]).replace(/⏎$/, '')).join('\n')}⟧`)
    .replace(inline, (_, label, value) => `⟦${label} ${valueText(value)}⟧`);
}

/** The accessibility names of every AgentText box in the markup. */
export const agentBoxNames = html => [...html.matchAll(/<(?:span|div) role="group" aria-label="([^"]*)" class="agent-text/g)].map(m => m[1]);
