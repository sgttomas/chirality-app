'use client';

import React from 'react';

import type { AccountConsentSettingsViewProps } from '../settings/account-consent-settings';
import type { HostedBootstrapController } from '../settings/hosted-bootstrap-controller';
import { HostedBootstrapView } from '../settings/hosted-bootstrap-view';
import { accountTitle } from './account-settings-controls';
import { AppUpdateControls } from './app-update-summary';
import { useAppUpdate } from './app-update-provider';
import { ThemeControl } from './theme-control';
import styles from './account-controls.module.css';
import { version } from '../../../package.json';

export type AccountPopoverProps = {
  account: AccountConsentSettingsViewProps;
  folder: string | null;
  onOpenSettings: (group?: 'folder' | 'local-model') => void;
  hosted?: HostedBootstrapController;
  /** Opens the About panel (installed version, update availability, download). */
  onOpenAbout?: () => void;
};

/** Exactly: account/sign-in, Settings…, Appearance, Check for Updates…, About. Runtime controls stay inside Settings. */
export function AccountPopover({ account, hosted, folder, onOpenSettings, onOpenAbout }: AccountPopoverProps): JSX.Element {
  const update = useAppUpdate();
  const installedVersion = update.state?.currentVersion ?? version;
  return <>
    {hosted ? <section className={styles.group}><HostedBootstrapView controller={hosted} compact /></section> : <section className={styles.group} aria-label="Account">
      <strong>{accountTitle(account)}</strong>
      {account.snapshot ? null : <p>Account service unavailable in this build.</p>}
      {account.snapshot ? <button type="button" disabled={account.busy} onClick={account.snapshot.account.status === 'loggedIn' ? account.onLogout : account.onLogin}>
        {account.snapshot.account.status === 'loggedIn' ? 'Sign out' : 'Sign in'}
      </button> : null}
      {folder ? <><p>Consent for {folder.split('/').filter(Boolean).pop() || folder}: {account.snapshot?.consent.status ?? 'unavailable'}</p><button type="button" onClick={() => onOpenSettings('folder')}>This folder…</button></> : null}
      {account.error ? <p role="alert">{account.error}</p> : null}
    </section>}
    <section className={styles.group} aria-label="App controls">
      <button type="button" className={styles.menuAction} onClick={() => onOpenSettings()}>Settings…</button>
      <details><summary>Appearance</summary><ThemeControl /></details>
      <AppUpdateControls compact />
      {onOpenAbout
        ? <button type="button" className={styles.menuAction} onClick={onOpenAbout}>About Chirality</button>
        : <details><summary>About Chirality</summary><p>Chirality {installedVersion}</p></details>}
    </section>
  </>;
}
