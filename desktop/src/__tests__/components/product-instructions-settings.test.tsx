import React from 'react';
import renderer, { act, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import { ProductInstructionsSettings } from '../../components/settings/product-instructions-settings';

let tree: ReactTestRenderer | undefined;
afterEach(() => {
  act(() => tree?.unmount());
  tree = undefined;
  delete (globalThis as { window?: unknown }).window;
});

it('opens instructions and refreshes customization status on return from the editor', async () => {
  const defaults = { ok: true as const, state: { path: '/App/instructions/AGENTS.md', modified: false } };
  const edited = { ok: true as const, state: { ...defaults.state, modified: true } };
  const get = vi.fn().mockResolvedValue(defaults);
  const open = vi.fn().mockResolvedValue(defaults);
  const restore = vi.fn().mockResolvedValue(defaults);
  let onFocus: (() => Promise<void>) | undefined;
  Object.assign(globalThis, { window: {
    chirality: { instructions: { get, open, restore } },
    addEventListener: (_: string, listener: () => Promise<void>) => { onFocus = listener; },
    removeEventListener: vi.fn()
  } });
  await act(async () => { tree = renderer.create(<ProductInstructionsSettings />); });
  const buttons = tree!.root.findAllByType('button');
  expect(buttons[1].props.disabled).toBe(true);
  await act(async () => { buttons[0].props.onClick(); });
  expect(open).toHaveBeenCalledOnce();
  get.mockResolvedValue(edited);
  await act(async () => { await onFocus!(); });
  expect(buttons[1].props.disabled).toBe(false);
  await act(async () => { buttons[1].props.onClick(); });
  expect(restore).toHaveBeenCalledOnce();
  expect(buttons[1].props.disabled).toBe(true);
});

it('reports unavailable instructions and omits Desktop controls when no bridge exists', async () => {
  Object.assign(globalThis, { window: {
    chirality: { instructions: { get: vi.fn().mockResolvedValue({ ok: false, error: 'Check the instructions folder.' }), open: vi.fn(), restore: vi.fn() } },
    addEventListener: vi.fn(), removeEventListener: vi.fn()
  } });
  await act(async () => { tree = renderer.create(<ProductInstructionsSettings />); });
  expect(tree!.root.findByProps({ role: 'alert' }).children).toEqual(['Check the instructions folder.']);
  act(() => tree!.unmount());
  delete window.chirality;
  await act(async () => { tree = renderer.create(<ProductInstructionsSettings />); });
  expect(tree!.toJSON()).toBeNull();
});
