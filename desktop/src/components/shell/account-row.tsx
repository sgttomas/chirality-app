'use client';

import React from 'react';

import { useCallback, useEffect, useId, useRef, useState } from 'react';
import { AccountIcon } from './account-icon';
import { AccountPopover, type AccountPopoverProps } from './account-popover';
import { accountTitle, LocalModelStatus } from './account-settings-controls';
import { useAppUpdate } from './app-update-provider';
import { hostedBootstrapStates, hostedBootstrapSummary, hostedBootstrapTitle } from '../settings/hosted-bootstrap-view';
import styles from './account-controls.module.css';

export function AccountRow(props: AccountPopoverProps): JSX.Element {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const panel = useRef<HTMLDivElement>(null);
  const id = useId();
  const update = useAppUpdate();
  const updateAvailable = update.state?.status === 'update-available';
  const position = useCallback(() => {
    if (!trigger.current || !panel.current) return;
    const rect = trigger.current.getBoundingClientRect();
    const width = Math.min(300, window.innerWidth - 24);
    const above = rect.top - 16;
    const below = window.innerHeight - rect.bottom - 16;
    Object.assign(panel.current.style, { width: `${width}px`, left: `${Math.max(12, Math.min(rect.left, window.innerWidth - width - 12))}px`,
      top: above >= below ? 'auto' : `${rect.bottom + 8}px`, bottom: above >= below ? `${window.innerHeight - rect.top + 8}px` : 'auto',
      maxHeight: `${Math.max(100, above >= below ? above : below)}px` });
  }, []);
  const dismiss = useCallback(() => { setOpen(false); trigger.current?.focus(); }, []);
  useEffect(() => {
    if (!open || typeof document === 'undefined') return;
    position();
    panel.current?.focus();
    const outside = (event: PointerEvent) => { if (event.target instanceof Node && !root.current?.contains(event.target)) setOpen(false); };
    const key = (event: KeyboardEvent) => { if (event.key === 'Escape') { event.preventDefault(); dismiss(); } else if ((event.metaKey || event.ctrlKey) && event.key === ',') { setOpen(false); } };
    document.addEventListener('pointerdown', outside);
    document.addEventListener('keydown', key);
    window.addEventListener('resize', position);
    window.addEventListener('scroll', position, true);
    return () => { document.removeEventListener('pointerdown', outside); document.removeEventListener('keydown', key); window.removeEventListener('resize', position); window.removeEventListener('scroll', position, true); };
  }, [open, position, dismiss]);
  useEffect(() => { setOpen(false); }, [props.folder]);
  // A sign-in that completes while the menu is open closes it: the ceremony
  // has finished and the row now reports the state. Failure and cancellation
  // keep the menu open so the alert and the retry action stay reachable.
  const ceremony = props.hosted?.snapshot?.registration === 'registered' ? props.hosted.snapshot.status.ceremony : undefined;
  const previousCeremony = useRef(ceremony);
  useEffect(() => {
    const previous = previousCeremony.current;
    previousCeremony.current = ceremony;
    if (previous === 'pending' && ceremony === 'signed-in') setOpen(false);
  }, [ceremony]);
  // Sign-in is an account fact: it holds across folder changes and folder
  // failures, so the avatar does not flicker to signed-out while a folder loads.
  const signedIn = props.hosted ? hostedBootstrapStates(props.hosted).auth === 'signed-in' : props.account.snapshot?.account.status === 'loggedIn';
  return <div ref={root} className={styles.root} onBlur={event => {
    if (event.relatedTarget instanceof Node && !event.currentTarget.contains(event.relatedTarget)) setOpen(false);
  }}>
    <button ref={trigger} type="button" className={styles.row} aria-label={updateAvailable ? 'Account and settings, update available' : 'Account and settings'} aria-expanded={open} aria-controls={id} aria-haspopup="dialog" onClick={() => {
      // Opening is the moment the operator looks at account state: ask the
      // daemon again rather than show what was last written optimistically.
      if (!open) props.hosted?.onRefresh();
      setOpen(!open);
    }}>
      <span className={signedIn ? `${styles.avatar} ${styles.avatarSignedIn}` : styles.avatar} data-signed-in={signedIn ? 'true' : 'false'} aria-hidden="true"><AccountIcon />{updateAvailable ? <span className={styles.updateDot} title="Update available" /> : null}</span>
      <span className={styles.identity}><strong>{props.hosted ? hostedBootstrapTitle(props.hosted) : accountTitle(props.account)}</strong><small>{props.hosted ? hostedBootstrapSummary(props.hosted) : <LocalModelStatus />}{updateAvailable ? <span className={styles.updateNote}> · Update available</span> : null}</small></span><span aria-hidden="true">⌃</span>
    </button>
    {open ? <div ref={panel} id={id} role="dialog" aria-label="Account and settings" tabIndex={-1} className={styles.popover}>
      <AccountPopover {...props} onOpenSettings={group => { dismiss(); props.onOpenSettings(group); }} onOpenAbout={props.onOpenAbout ? () => { dismiss(); props.onOpenAbout?.(); } : undefined} />
    </div> : null}
  </div>;
}
