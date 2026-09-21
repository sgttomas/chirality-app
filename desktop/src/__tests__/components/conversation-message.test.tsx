import React from 'react';
import { act, create } from 'react-test-renderer';
import { describe, expect, it } from 'vitest';
import { ConversationMessage, shouldCollapseUserMessage } from '../../components/shell/conversation-message';

const text = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : child && typeof child === 'object' && 'children' in child ? text(child as { children: unknown[] }) : '').join('');

describe('ConversationMessage', () => {
  it('marks user and assistant turns by role, label, and accessible name, not colour alone', () => {
    const tree = create(<>
      <ConversationMessage id="u1" role="operator" presentation="woven" speaker="You" body="Short prompt" />
      <ConversationMessage id="a1" role="assistant" presentation="woven" speaker="Help Human" persona="HELP_HUMAN" body={<p>Reply</p>} />
    </>);
    const articles = tree.root.findAllByType('article');
    expect(articles.map(node => [node.props.className, node.props['data-role'], node.props['aria-label']])).toEqual([
      ['chat-bubble chat-bubble--operator', 'operator', 'Your message'],
      ['chat-bubble chat-bubble--assistant', 'assistant', 'Help Human reply']
    ]);
    expect(articles[0].findByProps({ className: 'chat-speaker' }).children.join('')).toBe('You');
    expect(articles[0].findAllByType('button')).toHaveLength(0);
  });

  it('collapses a long user prompt behind Show more and keeps the full text reachable', () => {
    const long = Array.from({ length: 14 }, (_, index) => `line ${index + 1}`).join('\n');
    expect(shouldCollapseUserMessage(long)).toBe(true);
    expect(shouldCollapseUserMessage('x'.repeat(700))).toBe(false);
    expect(shouldCollapseUserMessage('x'.repeat(701))).toBe(true);
    const tree = create(<ConversationMessage id="u2" role="operator" presentation="woven" speaker="You" body={long} />);
    const article = () => tree.root.findByType('article');
    expect(article().props.className).toContain('chat-bubble--collapsed');
    expect(text(article())).toContain('line 14');
    const toggle = () => tree.root.findByType('button');
    expect(toggle().children.join('')).toBe('Show more');
    expect(toggle().props['aria-expanded']).toBe(false);
    expect(toggle().props['aria-controls']).toBe(tree.root.findByProps({ className: 'chat-user-text' }).props.id);
    act(() => toggle().props.onClick());
    expect(article().props.className).not.toContain('chat-bubble--collapsed');
    expect(toggle().children.join('')).toBe('Show less');
    expect(toggle().props['aria-expanded']).toBe(true);
  });

  it('places the activity disclosure above a streaming reply and below a finished one', () => {
    const activity = <details className="turn-activity"><summary>Working</summary></details>;
    const streaming = create(<ConversationMessage id="a2" role="assistant" presentation="woven" speaker="Assistant" streaming body={<p>partial</p>} activity={activity} />);
    const finished = create(<ConversationMessage id="a3" role="assistant" presentation="woven" speaker="Assistant" body={<p>done</p>} activity={activity} />);
    const order = (tree: ReturnType<typeof create>) => tree.root.findByType('article').children.map(child => typeof child === 'string' ? child : (child as { type: unknown }).type);
    expect(order(streaming)).toEqual(['p', 'details', 'p']);
    expect(order(finished)).toEqual(['p', 'p', 'details']);
  });
});
