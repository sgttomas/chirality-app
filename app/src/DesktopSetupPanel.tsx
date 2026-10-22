import { useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type NativePath = { encoding: "unix_bytes"; bytes: number[] };
type Location = { displayPath: string; nativePath: NativePath };
type Resource = { name: string; state: string; source?: string; limit?: string | null };
export type DesktopSetupView = {
  launch: { state: string; reason?: string; standing?: string };
  appData?: string; appDataProblem?: string; custodyProblem?: string;
  activeResources?: Resource[] | null; activeResourceProblem?: string | null;
  supplier: { selection: string; path?: string; standing: string };
  pending?: { state: string; accountHome: string; project?: string; resources: Resource[]; standing: string };
  nextLaunch: string;
};
type Preview = { token: string; accountHome: string; effects: string[]; project?: string; resources: Resource[]; standing: string };
const typedLocation = (text: string): Location => ({ displayPath: text, nativePath: { encoding: "unix_bytes", bytes: Array.from(new TextEncoder().encode(text)) } });

/** Pending setup owns only its local fields/preview; no live App choice setter. */
export function DesktopSetupPanel({ view }: { view?: DesktopSetupView | null }) {
  const [paths, setPaths] = useState<Array<Location | null>>([null, null, null]);
  const [projectMode, setProjectMode] = useState("");
  const [project, setProject] = useState<Location | null>(null);
  const [supplier, setSupplier] = useState("");
  const [preview, setPreview] = useState<Preview | null>(null);
  const [saved, setSaved] = useState<DesktopSetupView | null>(null);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const revision = useRef(0);
  if (!view) return null;
  const shown = { ...view, pending: saved?.pending ?? view.pending };
  const changed = () => { revision.current++; setPreview(null); setMessage(""); };
  const setPath = (index: number, location: Location) => { changed(); setPaths(current => current.map((p, i) => i === index ? location : p)); };
  const pick = async (kind: string, index?: number) => {
    const original = revision.current;
    setBusy(true); setMessage("");
    try {
      const selected = await invoke<Location | null>("desktop_setup_pick", { kind });
      if (selected && original === revision.current) {
        if (index !== undefined) setPath(index, selected);
        else { changed(); setProject(selected); }
      }
    } catch (error) { setMessage(String(error)); }
    finally { setBusy(false); }
  };
  const review = async () => {
    const original = revision.current;
    setPreview(null); setBusy(true); setMessage("");
    try {
      const result = await invoke<Preview>("desktop_setup_preview", {
        sharedPaths: paths.map(p => p?.nativePath),
        projectPath: projectMode === "chosen" ? project?.nativePath : null,
        supplierSelection: supplier,
      });
      if (original === revision.current) setPreview(result);
    } catch (error) { setMessage(String(error)); }
    finally { setBusy(false); }
  };
  const prepare = async () => {
    if (!preview) return;
    setBusy(true); setMessage("");
    try {
      const result = await invoke<DesktopSetupView | { state: string }>("desktop_setup_prepare", { previewToken: preview.token });
      setPreview(null);
      if ("launch" in result) setSaved(result);
      else setMessage(result.state);
    } catch (error) { setPreview(null); setMessage(String(error)); }
    finally { setBusy(false); }
  };
  const ready = !busy && paths.every(p => !!p?.displayPath) && supplier !== "" && (projectMode === "none" || (projectMode === "chosen" && !!project?.displayPath));
  return <details className="workspace-disclosure" open={shown.launch.state === "setup-required"} aria-label="Desktop setup">
    <summary><strong>Desktop setup</strong><span>{shown.launch.state === "setup-required" ? "Choose explicit inputs before Codex can start" : "Changes apply on the next launch"}</span></summary>
    <section className="workspace-disclosure-content" aria-label="Desktop setup inputs">
      <p>Current launch: {shown.launch.state}. {shown.launch.reason ?? shown.launch.standing}</p>
      <p>App data: {shown.appData ?? shown.appDataProblem ?? "unavailable"}</p>
      {shown.custodyProblem && <p role="alert">Desktop custody: {shown.custodyProblem}</p>}
      {shown.activeResourceProblem && <p role="alert">Current resource metadata unavailable: {shown.activeResourceProblem}</p>}
      {shown.activeResources && <div aria-label="Current desktop resource metadata">
        <p>Current shared-resource metadata; this does not establish native content discovery.</p>
        <ul>{shown.activeResources.map(resource => <li key={resource.name}>{resource.name}: {resource.state}{resource.source ? ` — ${resource.source}` : ""}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
      </div>}
      <p>Prepare a new App-owned account home. Choose each shared reference explicitly; enter an absolute path when its target does not exist yet. Setup checks paths and metadata only. It imports no credentials and never adopts an existing home.</p>
      {(["Shared config.toml", "Shared AGENTS.md", "Shared skills directory"] as const).map((label, index) => <p key={label}>
        <label>{label} <input aria-label={label} value={paths[index]?.displayPath ?? ""} disabled={busy} onChange={event => setPath(index, typedLocation(event.target.value))}/></label>{" "}
        <button disabled={busy} onClick={() => pick(["config", "agents", "skills"][index], index)}>Browse {label}</button>
      </p>)}
      <p><label>Project on next launch <select aria-label="Project on next launch" disabled={busy} value={projectMode} onChange={event => { changed(); setProjectMode(event.target.value); }}>
        <option value="">Choose explicitly</option><option value="none">No project</option><option value="chosen">Choose a project directory</option>
      </select></label></p>
      {projectMode === "chosen" && <p><label>Next project directory <input aria-label="Next project directory" disabled={busy} value={project?.displayPath ?? ""} onChange={event => { changed(); setProject(typedLocation(event.target.value)); }}/></label>{" "}<button disabled={busy} onClick={() => pick("project")}>Browse next project</button></p>}
      <p><label>Supplier for next launch <select aria-label="Supplier for next launch" disabled={busy} value={supplier} onChange={event => { changed(); setSupplier(event.target.value); }}>
        <option value="">Choose explicitly</option><option value={shown.supplier.selection}>Bundled supplier — unqualified owner-use development</option>
      </select></label></p>
      <p>Bundled supplier source: {shown.supplier.path ?? "unavailable"}. {shown.supplier.standing}</p>
      <button disabled={!ready} onClick={review}>Review setup effects</button>
      {preview && <div aria-label="Desktop setup effects">
        <ul>{preview.effects.map(effect => <li key={effect}>{effect}</li>)}</ul>
        <p>{preview.standing}</p>
        <ul>{preview.resources.map(resource => <li key={resource.name}>{resource.name}: {resource.source ?? resource.state}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
        <button disabled={busy} onClick={prepare}>Prepare home and save for next launch</button>
      </div>}
      {shown.pending && <div role="status" aria-label="Pending desktop setup">
        <p>Saved for next launch: {shown.pending.accountHome}. Project: {shown.pending.project ?? "explicitly absent"}.</p>
        <p>{shown.pending.standing}</p>
        <ul>{shown.pending.resources.map(resource => <li key={resource.name}>{resource.name}: {resource.state}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
      </div>}
      {message && <p role="alert">{message}</p>}
      <p>{shown.nextLaunch}</p>
    </section>
  </details>;
}
