import { Suspense } from 'react';
import { LoopShell } from '../../components/shell/loop-shell';
import { WovenDialogueRoute } from '../../components/woven-dialogue/woven-dialogue-route';

export default function ChatPage(): JSX.Element {
  return (
    <Suspense fallback={<main className="shell">Loading direct chat...</main>}>
      <WovenDialogueRoute defaultSurface="dialogue" legacy={<LoopShell />} />
    </Suspense>
  );
}
