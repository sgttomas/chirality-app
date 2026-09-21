'use client';

import React from 'react';
import { useAppUpdate } from './app-update-provider';
import { useLiveWork } from '../../lib/shell/live-work-store';
import { UPDATE_PATH_DESCRIPTION, UPDATE_PRESERVATION_NOTE, UPDATE_RUNNING_WORK_NOTE } from '../../lib/shell/user-data-inventory';

/** Human wording for each update state. Never claims availability that was not checked, and never that an update was installed. */
export function appUpdateStatusText(state: { status: string; available?: { version: string }; failure?: { message: string }; releaseSource: { configured: boolean; description: string } } | null, bridgeAvailable: boolean): string {
  if (!bridgeAvailable || !state) return 'Update checks are available in Chirality Desktop.';
  switch (state.status) {
    case 'checking': return 'Checking for updates…';
    case 'up-to-date': return 'Chirality is up to date.';
    case 'update-available': return `Version ${state.available?.version ?? ''} is available to download.`.replace('  ', ' ');
    case 'failed': return state.failure?.message ?? 'The update check did not complete.';
    default: return state.releaseSource.configured ? 'Not checked yet.' : state.releaseSource.description;
  }
}

/**
 * Check for Updates… plus the resulting state, shared by the account menu and
 * the About panel. Checking and download access only: the download opens an
 * installer in the browser and the user installs it; nothing here installs,
 * relaunches, or touches user data. While a turn is live in this window the
 * controls say so, because quitting to install stops it.
 */
export function AppUpdateControls({ compact = false }: { compact?: boolean }): JSX.Element {
  const { state, bridgeAvailable, check, openDownload } = useAppUpdate();
  const liveWork = useLiveWork();
  const checking = state?.status === 'checking';
  const available = state?.status === 'update-available' ? state.available : undefined;
  return <div className="app-update-controls" data-update-status={state?.status ?? 'unavailable'} data-live-work={liveWork ? 'true' : 'false'}>
    <button type="button" disabled={!bridgeAvailable || checking} onClick={() => { void check(); }} title={bridgeAvailable ? 'Ask the release source whether a newer Chirality is available. Nothing is downloaded or installed by checking.' : 'Update checks run only in Chirality Desktop.'}>{checking ? 'Checking…' : 'Check for Updates…'}</button>
    <p role="status" className={compact ? 'app-update-status app-update-status--compact' : 'app-update-status'}>{appUpdateStatusText(state, bridgeAvailable)}</p>
    {available ? <>
      <button type="button" onClick={() => { void openDownload(); }} title={`Open the download for Chirality ${available.version} in your browser. ${UPDATE_PATH_DESCRIPTION}`}>Download {available.version}</button>
      {compact ? null : <p className="app-update-note" data-update-note="path">{UPDATE_PATH_DESCRIPTION} {UPDATE_PRESERVATION_NOTE}</p>}
      {liveWork ? <p className="app-update-note app-update-note--live" role="status" data-update-note="running-work">{UPDATE_RUNNING_WORK_NOTE}</p> : null}
    </> : null}
  </div>;
}
