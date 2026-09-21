'use client';

import React from 'react';
import { LoopTertiaryShell } from '../../components/shell/loop-tertiary-shell';
import { WovenDialogueRoute } from '../../components/woven-dialogue/woven-dialogue-route';

export default function PipelineClient(): JSX.Element {
  return (
    <WovenDialogueRoute
      defaultSurface="pipeline"
      legacy={
        <LoopTertiaryShell
          defaultSidebarTab="pipeline"
          section="PIPELINE"
          title="Pipeline"
          subtitle="Run the live loop while configuring operative DECOMP, PREP, TASK, and AUDIT forms in the sidebar."
        />
      }
    />
  );
}
