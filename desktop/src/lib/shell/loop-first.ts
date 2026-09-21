/**
 * Pure routing helpers for the loop-first / direct-chat surface (`/chat`).
 *
 * D-APP-28/30: loop-first surfaces drive the mounted live loop by setting
 * `?agent=` instead of navigating to route-as-main screens. D-APP-24: direct
 * chat persona pickers are restricted to Type-0/Type-1; the picker drives the
 * surface by setting `?agent=`, which `chat-panel` already resolves.
 */

export const PORTAL_ROUTE = '/';
export const CHAT_ROUTE = '/chat';
export const CHAT_SECTION = 'CHAT';

/**
 * Build the `/chat` href, optionally pre-selecting a persona via `?agent=`. The
 * portal "start session" entry uses the bare route; the persona picker uses the
 * `agent` form to drive `chat-panel`'s route-free `resolvePersona`.
 */
export function buildDirectChatHref(persona?: string | null): string {
  const trimmed = persona?.trim();
  if (!trimmed) {
    return CHAT_ROUTE;
  }
  return `${CHAT_ROUTE}?agent=${encodeURIComponent(trimmed)}`;
}

/**
 * Build the loop-first portal href for a selected Type-0/Type-1 persona. The
 * portal page itself stays mounted; changing only `?agent=` lets the existing
 * ChatPanel resolve the persona for the next turn.
 */
export function buildPortalPersonaHref(persona?: string | null): string {
  const trimmed = persona?.trim();
  if (!trimmed) {
    return PORTAL_ROUTE;
  }
  return `${PORTAL_ROUTE}?agent=${encodeURIComponent(trimmed)}`;
}
