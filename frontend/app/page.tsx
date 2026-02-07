import { HexGrid } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";

export default function Home() {
  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Header */}
      <header className="flex justify-between items-center p-6 shrink-0">
        <div className="text-3xl font-extrabold tracking-widest uppercase">
          CHIRALITY // <span className="text-[var(--color-accent-orange)]">COMMAND</span>
        </div>
        <div className="mono text-sm text-[var(--color-text-dim)] tracking-wider">
          SYSTEM_RECOVERY: SUCCESS
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex p-5 gap-5 overflow-hidden">
        {/* Left: Hex Grid */}
        <HexGrid />

        {/* Right: Dashboard */}
        <div className="shrink-0">
            <DashboardList />
        </div>
      </main>
    </div>
  );
}