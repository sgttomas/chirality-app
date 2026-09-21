import { Suspense } from 'react';
import PipelineClient from './pipeline-client';

export default function PipelinePage(): JSX.Element {
  return (
    <Suspense fallback={<main className="shell">Loading pipeline...</main>}>
      <PipelineClient />
    </Suspense>
  );
}
