import Link from 'next/link';
import { AppShell } from '../components/shell/app-shell';

export default function NotFoundPage(): JSX.Element {
  return (
    <AppShell
      section="PORTAL"
      title="Route Not Found"
      subtitle="The requested route is not defined. Return to PORTAL to continue."
    >
      <section className="workbench-card">
        <h3>Unknown Route</h3>
        <p>The requested page does not exist in this frontend shell baseline.</p>
        <p>
          <Link href="/">Return to PORTAL</Link>
        </p>
      </section>
    </AppShell>
  );
}
