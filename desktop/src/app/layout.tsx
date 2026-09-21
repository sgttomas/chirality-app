import type { Metadata } from 'next';
import localFont from 'next/font/local';
import { headers } from 'next/headers';
import './globals.css';
import { WorkspaceProvider } from '../components/workspace/workspace-provider';
import { ToolkitProvider } from '../components/workspace/toolkit-provider';
import { DeliverablesProvider } from '../components/workspace/deliverables-provider';
import { HarnessEventsProvider } from '../components/workspace/harness-events-provider';
import { RuntimeConnectivityProvider } from '../components/shell/runtime-connectivity-provider';
import { AppUpdateProvider } from '../components/shell/app-update-provider';
import { WOVEN_WORKSPACE_STORAGE_KEY } from '../lib/woven-dialogue/woven-workspace-state';

// IBM Plex ships with the app: the woff2 files under `src/fonts/` are bundled
// by `next/font/local`, so the declared type identity resolves without any
// runtime network fetch (F-APP-1 untouched).
const plexSans = localFont({
  src: [
    { path: '../fonts/ibm-plex-sans-latin-400-normal.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/ibm-plex-sans-latin-400-italic.woff2', weight: '400', style: 'italic' },
    { path: '../fonts/ibm-plex-sans-latin-500-normal.woff2', weight: '500', style: 'normal' },
    { path: '../fonts/ibm-plex-sans-latin-600-normal.woff2', weight: '600', style: 'normal' },
    { path: '../fonts/ibm-plex-sans-latin-700-normal.woff2', weight: '700', style: 'normal' }
  ],
  variable: '--font-sans',
  display: 'swap',
  fallback: ['Avenir Next', 'Segoe UI', 'system-ui', 'sans-serif']
});

const plexSerif = localFont({
  src: [
    { path: '../fonts/ibm-plex-serif-latin-400-normal.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/ibm-plex-serif-latin-400-italic.woff2', weight: '400', style: 'italic' },
    { path: '../fonts/ibm-plex-serif-latin-600-normal.woff2', weight: '600', style: 'normal' }
  ],
  variable: '--font-serif',
  display: 'swap',
  fallback: ['Iowan Old Style', 'Palatino', 'Georgia', 'serif']
});

const plexMono = localFont({
  src: [
    { path: '../fonts/ibm-plex-mono-latin-400-normal.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/ibm-plex-mono-latin-500-normal.woff2', weight: '500', style: 'normal' }
  ],
  variable: '--font-mono',
  display: 'swap',
  fallback: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace']
});

// Light is the persisted default (§3.1 rule 3). This stamp runs before first
// paint so a stored `dark`/`system` choice never flashes light first; it is
// deliberately tiny, defensive, and never throws.
const THEME_BOOTSTRAP_SCRIPT = `(function(){var d=document.documentElement;var t="light";try{var raw=window.localStorage.getItem(${JSON.stringify(
  WOVEN_WORKSPACE_STORAGE_KEY
)});if(raw){var parsed=JSON.parse(raw);if(parsed&&(parsed.theme==="dark"||parsed.theme==="system"||parsed.theme==="light")){t=parsed.theme;}}}catch(e){t="light";}d.setAttribute("data-theme",t);})();`;

export const metadata: Metadata = {
  title: 'Chirality',
  description: 'PORTAL, PIPELINE, and WORKBENCH shell for local agent execution'
};

const CSP_HEADER = 'content-security-policy';
const CSP_NONCE_SOURCE_PATTERN = /^'nonce-([A-Za-z0-9+/_-]+={0,2})'$/;

function nonceFromContentSecurityPolicy(policy: string | null): string | undefined {
  const scriptDirective = policy
    ?.split(';')
    .map((directive) => directive.trim())
    .find((directive) => directive.startsWith('script-src '));
  for (const source of scriptDirective?.split(/\s+/).slice(1) ?? []) {
    const match = source.match(CSP_NONCE_SOURCE_PATTERN);
    if (match) return match[1];
  }
  return undefined;
}

export default async function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Reading request headers deliberately makes all four operator routes
  // dynamic. The packaged server presents Next and this layout with the exact
  // policy it attaches to the response; development sends no CSP request
  // header and keeps its previous policy posture.
  const nonce = nonceFromContentSecurityPolicy((await headers()).get(CSP_HEADER));

  return (
    <html
      lang="en"
      className={`${plexSans.variable} ${plexSerif.variable} ${plexMono.variable}`}
      data-theme="light"
      suppressHydrationWarning
    >
      <body>
        <script nonce={nonce} dangerouslySetInnerHTML={{ __html: THEME_BOOTSTRAP_SCRIPT }} />
        {/* Outermost so every runtime-backed pane below can depend on the
            reconnect epoch, and so the top bar and the data panes read one
            shared connectivity snapshot rather than two subscriptions that
            could disagree. */}
        <RuntimeConnectivityProvider>
          <AppUpdateProvider>
          <WorkspaceProvider>
            <DeliverablesProvider>
              <ToolkitProvider>
                <HarnessEventsProvider>{children}</HarnessEventsProvider>
              </ToolkitProvider>
            </DeliverablesProvider>
          </WorkspaceProvider>
          </AppUpdateProvider>
        </RuntimeConnectivityProvider>
      </body>
    </html>
  );
}
