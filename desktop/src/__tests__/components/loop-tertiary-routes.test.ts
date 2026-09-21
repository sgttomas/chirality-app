import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';

vi.mock('../../components/woven-dialogue/woven-dialogue-shell', async () => {
  const React = await import('react');
  return {
    WovenDialogueShell: ({ defaultSurface }: { defaultSurface: string }) =>
      React.createElement('section', { 'data-woven-surface': defaultSurface }, 'Continuing conversation')
  };
});

describe('LoopTertiaryShell route clients', () => {
  it('opens the Workbench deep link in the continuing conversation', async () => {
    const { default: WorkbenchClient } = await import('../../app/workbench/workbench-client');
    const html = renderToStaticMarkup(createElement(WorkbenchClient));

    expect(html).toContain('data-woven-surface="workbench"');
    expect(html).toContain('Continuing conversation');
  });

  it('opens the Pipeline deep link in the continuing conversation', async () => {
    const { default: PipelineClient } = await import('../../app/pipeline/pipeline-client');
    const html = renderToStaticMarkup(createElement(PipelineClient));

    expect(html).toContain('data-woven-surface="pipeline"');
    expect(html).toContain('Continuing conversation');
  });
});
