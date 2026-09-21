'use client';

import React from 'react';

import type { AccountConsentSettingsViewProps } from '../settings/account-consent-settings';
import { describeAccountIdentity } from '../../lib/consent/hosted-engine-consent-port';

export function accountTitle(account: AccountConsentSettingsViewProps): string {
  const snapshot = account.snapshot;
  if (!snapshot) return 'Account unavailable';
  return snapshot.account.status === 'loggedIn'
    ? `Account ${describeAccountIdentity(snapshot.account.identity)}` : 'Sign in';
}

/**
 * Non-hosted builds only. Daemon and residency reports do not attest external
 * oMLX server health, so the row states "unknown" and explains why on hover.
 */
export function LocalModelStatus(): JSX.Element {
  return <span title="The existing runtime connection does not report oMLX server availability.">
    <span data-local-model-status="unknown" aria-hidden="true" />Local model · unknown
  </span>;
}
