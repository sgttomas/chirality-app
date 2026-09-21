'use client';

import React, { useEffect, useRef } from 'react';
import { AppUpdateControls } from './app-update-summary';
import { useAppUpdate } from './app-update-provider';
import { UPDATE_PATH_DESCRIPTION, UPDATE_PRESERVATION_NOTE } from '../../lib/shell/user-data-inventory';
import { version } from '../../../package.json';

/**
 * About Chirality: installed version, update availability and the download
 * action. Opened from the account menu or the macOS application menu. A small
 * modal dialog: Escape and the Close button dismiss it; focus returns to the
 * opener through the caller's own focus management.
 */
export function AboutPanel({ open, onClose }: { open: boolean; onClose: () => void }): JSX.Element | null {
  const update = useAppUpdate();
  const closeRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!open || typeof document === 'undefined') return;
    closeRef.current?.focus();
    const key = (event: KeyboardEvent) => { if (event.key === 'Escape') { event.preventDefault(); onClose(); } };
    document.addEventListener('keydown', key);
    return () => document.removeEventListener('keydown', key);
  }, [open, onClose]);
  if (!open) return null;
  const installed = update.state?.currentVersion ?? version;
  return <div className="about-backdrop" onPointerDown={event => { if (event.target === event.currentTarget) onClose(); }}>
    <section className="about-panel" role="dialog" aria-modal="true" aria-labelledby="about-chirality-title">
      <h2 id="about-chirality-title">Chirality</h2>
      <p className="about-version">Version <code data-installed-version={installed}>{installed}</code></p>
      <AppUpdateControls />
      {update.state && !update.state.releaseSource.configured ? <p className="about-note">Updates are distributed by the owner. This build has no release source to check against.</p> : null}
      {update.state?.status === 'update-available' ? null : <p className="about-note" data-update-note="path">{UPDATE_PATH_DESCRIPTION} {UPDATE_PRESERVATION_NOTE}</p>}
      <div className="about-actions"><button ref={closeRef} type="button" onClick={onClose}>Close</button></div>
    </section>
  </div>;
}
