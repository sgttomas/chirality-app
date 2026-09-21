import { Suspense } from 'react';
import WorkbenchClient from './workbench-client';

export default function WorkbenchPage(): JSX.Element {
  return (
    <Suspense fallback={<main className="shell">Loading workbench...</main>}>
      <WorkbenchClient />
    </Suspense>
  );
}
