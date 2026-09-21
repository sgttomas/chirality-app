import React from 'react';

/**
 * Outlined account glyph: a placeholder until user profiles exist. It is not a
 * brand mark and never implies a real avatar. Decorative (`aria-hidden`); the
 * enclosing control carries the accessible name.
 */
export function AccountIcon({ className }: { className?: string }): JSX.Element {
  return <svg className={className} viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="8.5" r="3.5" />
    <path d="M4.5 20c.9-3.6 3.8-5.5 7.5-5.5s6.6 1.9 7.5 5.5" />
  </svg>;
}
