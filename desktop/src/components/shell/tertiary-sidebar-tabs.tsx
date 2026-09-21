'use client';

import { AgentMatrix } from '../portal/agent-matrix';
import { PipelineSurface } from '../pipeline/pipeline-surface';
import { WorkbenchSurface } from '../workbench/workbench-surface';

export function createTertiarySidebarTabs(): {
  portalTab: JSX.Element;
  pipelineTab: JSX.Element;
  workbenchTab: JSX.Element;
} {
  return {
    portalTab: <AgentMatrix />,
    pipelineTab: <PipelineSurface />,
    workbenchTab: <WorkbenchSurface />
  };
}
