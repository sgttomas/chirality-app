import { Suspense } from 'react';
import { PortalLoopShell } from '../components/shell/portal-loop-shell';
import { WovenDialogueRoute } from '../components/woven-dialogue/woven-dialogue-route';

export default function PortalPage(): JSX.Element {
  return (
    <Suspense fallback={<main className="shell">Loading live loop portal...</main>}>
      <WovenDialogueRoute defaultSurface="dialogue" legacy={<PortalLoopShell />} />
    </Suspense>
  );
}
