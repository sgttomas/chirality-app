import { describe, expect, it } from 'vitest';
import {
  CHAT_ROUTE,
  CHAT_SECTION,
  PORTAL_ROUTE,
  buildDirectChatHref,
  buildPortalPersonaHref
} from '../../lib/shell/loop-first';

describe('loop-first routing helpers', () => {
  it('exposes the /chat route and CHAT section constants', () => {
    expect(PORTAL_ROUTE).toBe('/');
    expect(CHAT_ROUTE).toBe('/chat');
    expect(CHAT_SECTION).toBe('CHAT');
  });

  it('builds the bare /chat href when no persona is given', () => {
    expect(buildDirectChatHref()).toBe('/chat');
    expect(buildDirectChatHref(null)).toBe('/chat');
    expect(buildDirectChatHref('')).toBe('/chat');
    expect(buildDirectChatHref('   ')).toBe('/chat');
  });

  it('pre-selects a persona via ?agent= and url-encodes it', () => {
    expect(buildDirectChatHref('WORKING_ITEMS')).toBe('/chat?agent=WORKING_ITEMS');
    expect(buildDirectChatHref('  REVIEW  ')).toBe('/chat?agent=REVIEW');
    expect(buildDirectChatHref('A B')).toBe('/chat?agent=A%20B');
  });

  it('builds loop-first portal persona hrefs without leaving /', () => {
    expect(buildPortalPersonaHref()).toBe('/');
    expect(buildPortalPersonaHref(null)).toBe('/');
    expect(buildPortalPersonaHref('')).toBe('/');
    expect(buildPortalPersonaHref('WORKING_ITEMS')).toBe('/?agent=WORKING_ITEMS');
    expect(buildPortalPersonaHref('  REVIEW  ')).toBe('/?agent=REVIEW');
    expect(buildPortalPersonaHref('A B')).toBe('/?agent=A%20B');
  });
});
