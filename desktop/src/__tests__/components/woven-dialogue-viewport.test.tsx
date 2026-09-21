import React, { useEffect } from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { describe, expect, it } from 'vitest';
import { DialogueViewport } from '../../components/woven-dialogue/dialogue-viewport';

describe('Woven Dialogue viewport', () => {
  it('keeps one visible primary controller through updates with no focused surface', () => {
    let mounted = 0;
    let unmounted = 0;
    function Primary(): JSX.Element {
      useEffect(() => { mounted++; return () => { unmounted++; }; }, []);
      return <input data-chat-input="primary" />;
    }
    let tree!: ReactTestRenderer;
    act(() => { tree = create(<DialogueViewport primaryDialogue={<Primary />} />); });
    const controller = tree.root.findByType(Primary);
    act(() => { tree.update(<DialogueViewport primaryDialogue={<Primary />} />); });
    expect(tree.root.findByType(Primary)).toBe(controller);
    const viewport = tree.root.findByProps({ 'data-primary-dialogue-mounted': 'true' });
    expect(viewport.props.hidden).toBeUndefined();
    expect(viewport.props['aria-hidden']).toBeUndefined();
    expect(tree.root.findAll(node => Boolean(node.props['data-focused-surface']))).toHaveLength(0);
    expect(tree.root.findAllByType('button')).toHaveLength(0);
    expect(mounted).toBe(1);
    expect(unmounted).toBe(0);
    act(() => { tree.unmount(); });
    expect(unmounted).toBe(1);
  });
});
