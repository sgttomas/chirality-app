'use client';

import React, { useId, useState } from 'react';

/** A user prompt longer than this collapses behind "Show more". */
export const USER_MESSAGE_COLLAPSE_CHARS = 700;
export const USER_MESSAGE_COLLAPSE_LINES = 10;

export function shouldCollapseUserMessage(text: string): boolean {
  return text.length > USER_MESSAGE_COLLAPSE_CHARS || text.split('\n').length > USER_MESSAGE_COLLAPSE_LINES;
}

/**
 * One turn in the conversation. User prompts sit on a restrained, narrower,
 * right-aligned surface with left-aligned text; assistant replies stay open and
 * document-like. The speaker label and the article's accessible name carry the
 * distinction, so it never relies on colour alone.
 */
export function ConversationMessage({ id, role, presentation, speaker, persona, streaming = false, phase, body, activity, children }: {
  id: string;
  role: 'operator' | 'assistant';
  presentation?: 'woven';
  speaker: string;
  persona?: string;
  streaming?: boolean;
  phase?: 'commentary' | 'final_answer' | null;
  /** Assistant markdown, or the user's raw text. */
  body: React.ReactNode | string | null;
  /** The per-turn activity disclosure (assistant only). */
  activity?: React.ReactNode;
  children?: React.ReactNode;
}): JSX.Element {
  const [expanded, setExpanded] = useState(false);
  const bodyId = useId();
  const userText = role === 'operator' && typeof body === 'string' ? body : null;
  const collapsible = userText !== null && shouldCollapseUserMessage(userText);
  const collapsed = collapsible && !expanded;
  return <article id={`message-${id}`} className={`chat-bubble chat-bubble--${role}${streaming ? ' chat-bubble--streaming' : ''}${collapsed ? ' chat-bubble--collapsed' : ''}`} data-role={role} data-message-phase={phase ?? undefined} aria-label={role === 'operator' ? 'Your message' : `${speaker} reply`}>
    {presentation === 'woven' ? <p className="chat-speaker" title={role === 'assistant' ? persona : undefined}>{speaker}</p> : null}
    {role === 'assistant' && activity && streaming ? activity : null}
    {body !== null ? (userText !== null
      ? <div id={bodyId} className="chat-user-text"><p>{userText}</p>{collapsed ? <span className="chat-user-fade" aria-hidden="true" /> : null}</div>
      : body) : null}
    {collapsible ? <button type="button" className="chat-show-more" aria-expanded={!collapsed} aria-controls={bodyId} onClick={() => setExpanded(current => !current)}>{collapsed ? 'Show more' : 'Show less'}</button> : null}
    {children}
    {role === 'assistant' && activity && !streaming ? activity : null}
  </article>;
}
