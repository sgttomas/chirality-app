import { useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type NativePath = { encoding: "unix_bytes"; bytes: number[] };
type Location = { displayPath: string; nativePath: NativePath };
type Resource = { name: string; state: string; source?: string; limit?: string | null };
export type DesktopSetupView = {
  launch: { state: string; reason?: string; standing?: string };
  appData?: string; appDataProblem?: string; custodyProblem?: string;
  activeResources?: Resource[] | null; activeResourceProblem?: string | null;
  retainProject?: { available: boolean; accountHome?: string; reason?: string };
  supplier: { selection: string; path?: string; standing: string };
  pending?: { state: string; accountHome: string; project?: string; resources: Resource[]; standing: string };
  nextLaunch: string;
};
type Preview = { token: string; kind: string; affirmative: string; accountHome: string; effects: string[]; project?: string; resources: Resource[]; standing: string };
const typedLocation = (text: string): Location => ({ displayPath: text, nativePath: { encoding: "unix_bytes", bytes: Array.from(new TextEncoder().encode(text)) } });

/** Pending setup owns only its local fields/preview; no live App choice setter. */
export function DesktopSetupPanel({ view }: { view?: DesktopSetupView | null }) {
  const [paths, setPaths] = useState<Array<Location | null>>([null, null, null]);
  const [mode, setMode] = useState("");
  const [projectMode, setProjectMode] = useState("");
  const [project, setProject] = useState<Location | null>(null);
  const [supplier, setSupplier] = useState("");
  const [preview, setPreview] = useState<Preview | null>(null);
  const [saved, setSaved] = useState<DesktopSetupView | null>(null);
  const [message, setMessage] = useState("");
  const [failed, setFailed] = useState(false);
  const [busy, setBusy] = useState(false);
  const revision = useRef(0);
  const pending = useRef(false);
  const mounted = useRef(true);
  const [progress, setProgress] = useState("");
  const reviewButton = useRef<HTMLButtonElement>(null);
  const effectsHeading = useRef<HTMLHeadingElement>(null);
  const feedback = useRef<HTMLParagraphElement>(null);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; revision.current++; }; }, []);
  useEffect(() => { if (preview) effectsHeading.current?.focus?.(); }, [preview]);
  useEffect(() => { if (message) feedback.current?.focus?.(); }, [message]);
  const begin = (text: string) => { if (pending.current) return false; pending.current = true; setBusy(true); setProgress(text); setMessage(""); setFailed(false); return true; };
  const finish = () => { pending.current = false; if (mounted.current) { setBusy(false); setProgress(""); } };

  if (!view) return null;
  const shown = { ...view, pending: saved?.pending ?? view.pending, retainProject: saved?.retainProject ?? view.retainProject };
  const changed = () => { revision.current++; setPreview(null); setMessage(""); };
  const setPath = (index: number, location: Location) => { changed(); setPaths(current => current.map((p, i) => i === index ? location : p)); };
  const pick = async (kind: string, index?: number) => {
    if (!begin("Choose a location in the system dialog…")) return;
    const original = revision.current;
    try {
      const selected = await invoke<Location | null>("desktop_setup_pick", { kind });
      if (mounted.current && selected && original === revision.current) {
        if (index !== undefined) setPath(index, selected);
        else { changed(); setProject(selected); }
      }
    } catch (error) { if (mounted.current) { setFailed(true); setMessage(String(error)); } }
    finally { finish(); }
  };
  const review = async () => {
    if (!ready || !begin("Checking the selected locations…")) return;
    const original = revision.current;
    setPreview(null);
    try {
      const result = mode === "retain" ? await invoke<Preview>("desktop_setup_project_preview", {
        projectPath: projectMode === "chosen" ? project?.nativePath : null,
      }) : await invoke<Preview>("desktop_setup_preview", {
        sharedPaths: paths.map(p => p?.nativePath),
        projectPath: projectMode === "chosen" ? project?.nativePath : null,
        supplierSelection: supplier,
      });
      if (mounted.current && original === revision.current) setPreview(result);
    } catch (error) { if (mounted.current) { setFailed(true); setMessage(String(error)); } }
    finally { finish(); }
  };
  const prepare = async () => {
    if (!preview || !begin("Waiting for the native confirmation and setup result…")) return;
    try {
      const result = await invoke<DesktopSetupView | { state: string }>("desktop_setup_prepare", { previewToken: preview.token });
      if (!mounted.current) return;
      setPreview(null);
      if ("launch" in result) { setSaved(result); setMessage("Setup saved for your next launch. Your current workspace has not changed."); }
      else setMessage(result.state);
    } catch (error) { if (mounted.current) { setPreview(null); setFailed(true); setMessage(String(error)); } }
    finally { finish(); }
  };
  const editChoices = () => { if (pending.current) return; changed(); reviewButton.current?.focus?.(); };
  const ready = !busy && (mode === "retain" ? shown.retainProject?.available === true : mode === "new" && paths.every(p => !!p?.displayPath) && supplier !== "") && (projectMode === "none" || (projectMode === "chosen" && !!project?.displayPath));
  const nextStep = busy ? progress : !mode ? "Choose whether to prepare a new account home or keep your current account."
    : mode === "retain" && !shown.retainProject?.available ? "Keeping this account is unavailable. See the reason below."
    : mode === "new" && paths.some(p => !p?.displayPath) ? "Choose all three shared locations. You can also enter an absolute path."
    : !projectMode ? "Choose a project for the next launch, or choose No project."
    : projectMode === "chosen" && !project?.displayPath ? "Choose the project directory."
    : mode === "new" && !supplier ? "Choose the supplier for the next launch."
    : "Your choices are ready to review. Nothing is saved until you confirm.";
  return <details className="workspace-disclosure" open={shown.launch.state === "setup-required"} aria-label="Desktop setup">
    <summary><strong>Desktop setup</strong><span>{shown.launch.state === "setup-required" ? "Choose explicit inputs before Codex can start" : "Changes apply on the next launch"}</span></summary>
    <section className="workspace-disclosure-content" aria-label="Desktop setup inputs" aria-busy={busy}>
      <div className="setup-state">
        <h2>{shown.pending ? "Setup saved for the next launch" : shown.launch.state === "setup-required" ? "Set up your workspace" : "Plan your next workspace"}</h2>
        <p>{shown.pending ? "Keep working here. The saved choices take effect after you quit and open the App again." : "Choose your shared settings and project, review the effects, then confirm in the App’s native dialog."}</p>
      </div>
      {shown.custodyProblem && <p role="alert">Setup is unavailable: {shown.custodyProblem}</p>}
      {shown.activeResourceProblem && <p role="alert">Shared settings could not be checked: {shown.activeResourceProblem}</p>}
      <div className="setup-steps">
      <fieldset className="setup-step" disabled={busy}><legend>1. Account and shared settings</legend>
      <p><label>Desktop setup action <select aria-label="Desktop setup action" disabled={busy} value={mode} onChange={event => { changed(); setMode(event.target.value); }}>
        <option value="">Choose explicitly</option><option value="new">Prepare a new account home</option><option value="retain" disabled={!shown.retainProject?.available}>Keep the admitted account; change next project</option>
      </select></label></p>
      {!shown.retainProject?.available && <p>Keep-account project change unavailable: {shown.retainProject?.reason ?? "No currently admitted saved-desktop account"}</p>}
      {mode === "retain" ? <p>{shown.retainProject?.available ? `Keep the currently admitted account home ${shown.retainProject.accountHome}.` : "The retained-source project choice is currently unavailable."} Choose only its project for the next launch. No home, link or credential is created or migrated; shared references and supplier remain unchanged.</p> : <p>Prepare a new App-owned account home. Choose each shared reference explicitly; enter an absolute path when its target does not exist yet. Setup checks paths and metadata only. It imports no credentials and never adopts an existing home.</p>}
      {mode !== "retain" && (["Shared config.toml", "Shared AGENTS.md", "Shared skills directory"] as const).map((label, index) => <div className="setup-field" key={label}>
        <label>{label} <input aria-label={label} value={paths[index]?.displayPath ?? ""} disabled={busy} onChange={event => setPath(index, typedLocation(event.target.value))}/></label>{" "}
        <button disabled={busy} onClick={() => pick(["config", "agents", "skills"][index], index)}>Browse {label}</button>
      </div>)}
      </fieldset>
      <fieldset className="setup-step" disabled={busy}><legend>2. Project and supplier</legend>
      <p><label>Project on next launch <select aria-label="Project on next launch" disabled={busy} value={projectMode} onChange={event => { changed(); setProjectMode(event.target.value); }}>
        <option value="">Choose explicitly</option><option value="none">No project</option><option value="chosen">Choose a project directory</option>
      </select></label></p>
      {projectMode === "chosen" && <p><label>Next project directory <input aria-label="Next project directory" disabled={busy} value={project?.displayPath ?? ""} onChange={event => { changed(); setProject(typedLocation(event.target.value)); }}/></label>{" "}<button disabled={busy} onClick={() => pick("project")}>Browse next project</button></p>}
      {mode !== "retain" && <p><label>Supplier for next launch <select aria-label="Supplier for next launch" disabled={busy} value={supplier} onChange={event => { changed(); setSupplier(event.target.value); }}>
        <option value="">Choose explicitly</option><option value={shown.supplier.selection}>Bundled supplier — unqualified owner-use development</option>
      </select></label></p>}
      </fieldset>
      </div>
      <div className="setup-actions">
        <p id="desktop-setup-next-step" className="setup-guidance" role="status" aria-live="polite">{nextStep}</p>
        <button ref={reviewButton} className="setup-primary" disabled={!ready} aria-describedby="desktop-setup-next-step" onClick={review}>Review setup effects</button>
      </div>
      {preview && <div className="setup-effects" aria-label="Desktop setup effects" onKeyDown={event => {
        if (event.key === "Escape" && !pending.current) { event.preventDefault(); event.stopPropagation(); editChoices(); }
      }}>
        <h3 tabIndex={-1} ref={effectsHeading}>Review before saving</h3>
        <p>Check these effects. The next action opens the native confirmation; this review alone changes nothing.</p>
        <ul>{preview.effects.map(effect => <li key={effect}>{effect}</li>)}</ul>
        <p>{preview.standing}</p>
        <ul>{preview.resources.map(resource => <li key={resource.name}>{resource.name}: {resource.source ?? resource.state}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
        <button className="setup-primary" disabled={busy} onClick={prepare}>{preview.affirmative}</button>{" "}
        <button disabled={busy} onClick={editChoices}>Edit setup choices</button>
      </div>}
      {shown.pending && <div role="status" aria-label="Pending desktop setup">
        <p>Saved for next launch: {shown.pending.accountHome}. Project: {shown.pending.project ?? "explicitly absent"}.</p>
        <p>{shown.pending.standing}</p>
        <ul>{shown.pending.resources.map(resource => <li key={resource.name}>{resource.name}: {resource.state}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
      </div>}
      {message && <p ref={feedback} tabIndex={-1} role={failed ? "alert" : "status"} aria-live={failed ? "assertive" : "polite"}>{failed ? "Setup could not finish. " : ""}{message}</p>}
      <details className="setup-diagnostics"><summary>Setup details and source status</summary>
      <p>Current launch: {shown.launch.state}. {shown.launch.reason ?? shown.launch.standing}</p>
      <p>App data: {shown.appData ?? shown.appDataProblem ?? "unavailable"}</p>
      {shown.activeResources && <div aria-label="Current desktop resource metadata">
        <p>Current shared-resource metadata; this does not establish native content discovery.</p>
        <ul>{shown.activeResources.map(resource => <li key={resource.name}>{resource.name}: {resource.state}{resource.source ? ` — ${resource.source}` : ""}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul>
      </div>}
      <p>Bundled supplier source: {shown.supplier.path ?? "unavailable"}. {shown.supplier.standing}</p>
      </details>
      <p>{shown.nextLaunch}</p>
    </section>
  </details>;
}
