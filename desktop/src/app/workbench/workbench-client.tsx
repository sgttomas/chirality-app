'use client';

import React from 'react';
import { LoopTertiaryShell } from '../../components/shell/loop-tertiary-shell';
import { WovenDialogueRoute } from '../../components/woven-dialogue/woven-dialogue-route';

export default function WorkbenchClient(): JSX.Element {
  return (
    <WovenDialogueRoute
      defaultSurface="workbench"
      legacy={
        <LoopTertiaryShell
          defaultSidebarTab="workbench"
          section="WORKBENCH"
          title="Workbench"
          subtitle="Run the live loop while reviewing persona context and deliverable contracts in the sidebar."
        />
      }
    />
  );
}
