import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import { CHIRALITY_ROLES } from '@chirality/runtime-contracts/v3';
import { RoleDirectoryPanel } from '../../components/portal/agent-matrix';

const directRoles = CHIRALITY_ROLES.filter(role => role.directEntry);

describe('legacy Portal role directory', () => {
  it('renders the three direct-entry roles without ladder or workflow-rung controls', () => {
    const html = renderToStaticMarkup(createElement(RoleDirectoryPanel, { loading: false, error: null, roles: directRoles }));
    expect(html).toContain('Help Human');
    expect(html).toContain('Helps Humans');
    expect(html).toContain('Working Items');
    expect(html).not.toMatch(/GUIDING|APPLYING|JUDGING|REVIEWING|Pipeline|Matrix launches/);
  });

  it('renders Runtime loading and failure states without fallback roles', () => {
    expect(renderToStaticMarkup(createElement(RoleDirectoryPanel, { loading: true, error: null, roles: [] }))).toContain('Loading roles');
    const failed = renderToStaticMarkup(createElement(RoleDirectoryPanel, { loading: false, error: 'Runtime unavailable', roles: [] }));
    expect(failed).toContain('Runtime unavailable');
    expect(failed).not.toContain('Help Human');
  });
});
