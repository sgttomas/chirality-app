import { useEffect, useRef, useState } from "react";
import { invoke } from "./hostReads";
import type { DesktopSetupView } from "./DesktopSetupPanel";

type NativePath = { encoding: "unix_bytes"; bytes: number[] };
type Location = { displayPath: string; nativePath: NativePath };
type Preview = { token: string; kind: string; affirmative: string; effects: string[]; standing: string; locations?: Array<{ name: string; path: string }> };
/** Effect text with any absolute path shown as a quieter, wrapping path. */
const Effect = ({ text }: { text: string }) => {
  const at = text.search(/(^|[\s:→])\//);
  if (at < 0) return <>{text}</>;
  const cut = text[at] === "/" ? at : at + 1;
  return <>{text.slice(0, cut)}<code className="first-use-path">{text.slice(cut)}</code></>;
};
const typedLocation = (text: string): Location => ({ displayPath: text, nativePath: { encoding: "unix_bytes", bytes: Array.from(new TextEncoder().encode(text)) } });
/**
 * The one project choice. The field shows and the review sends from this same
 * value: typed text is sent exactly as typed (never trimmed, expanded,
 * resolved or created); a picked folder keeps the picker's native reference
 * untouched until the person edits the field, which makes it typed text.
 */
type ProjectChoice = { kind: "unset" } | { kind: "none" } | { kind: "typed"; text: string } | { kind: "picked"; location: Location };
/** Local shape only; whether the folder exists and can be used is the host's review. */
const typedProblem = (text: string) =>
  text === "" ? null
  : text.includes("\0") ? "This path contains a character that cannot be used in a folder path. Remove it or choose Browse…."
  : new TextDecoder("utf-8", { ignoreBOM: true }).decode(new TextEncoder().encode(text)) !== text ? "This path contains an incomplete character. Enter or paste it again, or choose Browse…."
  : !text.startsWith("/") ? "Use the folder's full path, starting with /. Paths such as ~/Projects or Projects/app aren't expanded or looked up."
  : null;
const SHARED = [
  { label: "Your config.toml", kind: "config" },
  { label: "Your AGENTS.md", kind: "agents" },
  { label: "Your skills folder", kind: "skills" },
] as const;

/**
 * First use while setup is required: one focused surface instead of the
 * workspace. Every effect is the host's: the person picks a project, chooses
 * new App-owned settings or their existing ones, reviews the host's effects and
 * confirms in the native dialog. Nothing is saved, signed in or started here.
 */
export function FirstUseSetup({ view }: { view: DesktopSetupView }) {
  const [project, setProject] = useState<ProjectChoice>({ kind: "unset" });
  const [route, setRoute] = useState<"new" | "existing" | "keep">("new");
  const [paths, setPaths] = useState<Array<Location | null>>([null, null, null]);
  const [preview, setPreview] = useState<Preview | null>(null);
  const [saved, setSaved] = useState<DesktopSetupView | null>(null);
  const [message, setMessage] = useState("");
  const [failed, setFailed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState("");
  const pending = useRef(false);
  const mounted = useRef(true);
  const revision = useRef(0);
  const effectsHeading = useRef<HTMLHeadingElement>(null);
  const feedback = useRef<HTMLParagraphElement>(null);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; revision.current++; }; }, []);
  useEffect(() => { if (preview) effectsHeading.current?.focus?.(); }, [preview]);
  useEffect(() => { if (message) feedback.current?.focus?.(); }, [message]);
  const begin = (text: string) => { if (pending.current) return false; pending.current = true; setBusy(true); setProgress(text); setMessage(""); setFailed(false); return true; };
  const finish = () => { pending.current = false; if (mounted.current) { setBusy(false); setProgress(""); } };
  const changed = () => { revision.current++; setPreview(null); setMessage(""); };
  // Handlers retained from an earlier render act only while nothing has changed since.
  const seen = revision.current;
  const current = () => seen === revision.current;
  const fail = (error: unknown) => { if (mounted.current) { setFailed(true); setMessage(String(error)); } };

  const shown = { ...view, pending: saved?.pending ?? view.pending, retainProject: saved?.retainProject ?? view.retainProject };
  const keepAvailable = shown.retainProject?.available === true;
  const noProject = project.kind === "none";
  const projectText = project.kind === "typed" ? project.text : project.kind === "picked" ? project.location.displayPath : "";
  const projectProblem = project.kind === "typed" ? typedProblem(project.text) : null;
  const projectChosen = noProject || project.kind === "picked" || (project.kind === "typed" && project.text !== "" && !projectProblem);
  const routeReady = route === "new" || route === "keep" ? true : paths.every(p => !!p?.displayPath);
  const ready = !busy && !shown.custodyProblem && projectChosen && routeReady && (route !== "keep" || keepAvailable);
  const next = busy ? progress
    : shown.pending ? "Setup is saved. Quit Chirality and open it again to start working."
    : projectProblem ? "Check the project folder path using the guidance below it."
    : !projectChosen ? "Choose the folder you want to work in, or continue without a project."
    : !routeReady ? "Choose your config.toml, AGENTS.md and skills folder, or start with new settings."
    : "Ready to review. Nothing is created or saved until you confirm.";

  const pick = async (kind: string, index?: number) => {
    if (!begin("Choose a location in the system dialog…")) return;
    const original = revision.current;
    try {
      const selected = await invoke<Location | null>("desktop_setup_pick", { kind });
      if (mounted.current && selected && original === revision.current) {
        changed();
        if (index === undefined) setProject({ kind: "picked", location: selected });
        else setPaths(current => current.map((p, i) => i === index ? selected : p));
      }
    } catch (error) { fail(error); }
    finally { finish(); }
  };
  const review = async () => {
    if (!ready || !current() || !begin("Checking your choices…")) return;
    const original = revision.current;
    const projectPath = project.kind === "picked" ? project.location.nativePath
      : project.kind === "typed" ? typedLocation(project.text).nativePath
      : null;
    setPreview(null);
    try {
      const result = route === "new" ? await invoke<Preview>("desktop_setup_new_settings_preview", { projectPath })
        : route === "keep" ? await invoke<Preview>("desktop_setup_project_preview", { projectPath })
        : await invoke<Preview>("desktop_setup_preview", { sharedPaths: paths.map(p => p?.nativePath), projectPath, supplierSelection: view.supplier.selection });
      if (mounted.current && original === revision.current) setPreview(result);
    } catch (error) { fail(error); }
    finally { finish(); }
  };
  const confirm = async () => {
    if (!preview || !current() || !begin("Waiting for your confirmation in the App's dialog…")) return;
    try {
      const result = await invoke<DesktopSetupView | { state: string }>("desktop_setup_prepare", { previewToken: preview.token });
      if (!mounted.current) return;
      setPreview(null);
      if ("launch" in result) setSaved(result);
      else setMessage(result.state.startsWith("cancelled") ? "Not saved — you cancelled in the dialog. Your choices are still here." : result.state);
    } catch (error) { if (mounted.current) setPreview(null); fail(error); }
    finally { finish(); }
  };

  // Another process holds this App data (which one is not known): nothing
  // operational started and setup cannot run, so the host's reason is the
  // whole surface.
  if (view.launch?.state === "data-held") return <section className="first-use" aria-label="Welcome">
    <h1>This App's data is in use</h1>
    <p className="first-use-lead" role="alert">{view.launch.reason}</p>
  </section>;
  // A Codex home the saved setup names is held: setup is not what is needed,
  // and nothing operational started, so the host's reason is the whole surface.
  if (view.launch?.state === "home-held") return <section className="first-use" aria-label="Welcome">
    <h1>A Codex home this App uses is held</h1>
    <p className="first-use-lead" role="alert">{view.launch.reason}</p>
    <p>Nothing operational was started. This launch did not change your saved setup. Quit this Chirality instance (⌘Q), then reopen it after the process holding the home has released it.</p>
  </section>;
  // Something else is where Chirality keeps its folder for conversations without
  // a project: only the person can move it, so the host's reason, with its path,
  // is the whole surface. Nothing is removed or replaced for them.
  if (view.launch?.state === "set-aside-occupied") return <section className="first-use" aria-label="Welcome">
    <h1>A folder Chirality keeps is taken</h1>
    <p className="first-use-lead" role="alert">{view.launch.reason}</p>
    <p>Nothing operational was started. This launch did not change your saved setup.</p>
  </section>;
  return <section className="first-use" aria-label="Welcome" aria-busy={busy}>
    <h1>Welcome to Chirality</h1>
    <p className="first-use-lead">Chirality runs Codex on this Mac to do project work with you, and to turn work that goes well into workflows you can run again.{shown.pending ? "" : " First, choose a project folder and how Codex is set up. Your choices take effect when you next open the App."}</p>
    {shown.custodyProblem && <p role="alert">Setup can't continue: {shown.custodyProblem}</p>}
    {shown.pending ? <div className="first-use-saved" role="status" aria-label="Setup saved">
      <h2>You're set up</h2>
      <p><strong>Next: quit Chirality (⌘Q) and open it again.</strong> Reopening loads your saved project and Codex settings. Then open Connection &amp; access to sign in with your ChatGPT account or prepare the oMLX connection. After connecting, choose a model and start a conversation.</p>
      <p>Project: {shown.pending.project ? <code className="first-use-path">{shown.pending.project}</code> : "none"}</p>
    </div> : <>
    <ol className="first-use-steps">
      <li><h2>Your project folder</h2>
        <p>The folder you want to work in. Workflows are kept in its <code>.chirality</code> folder, and work you run there writes its results there.</p>
        <p><label htmlFor="first-use-project">Project folder</label>{" "}
          <input id="first-use-project" aria-label="Project folder" value={projectText} disabled={busy} spellCheck={false} autoCapitalize="off" autoCorrect="off"
            placeholder="/full/path/to/your/project" style={{ width: "min(100%, 30rem)", fontFamily: "var(--font-code)" }}
            aria-invalid={projectProblem ? true : undefined} aria-describedby={projectProblem ? "first-use-project-problem first-use-project-help" : "first-use-project-help"}
            onChange={event => { changed(); setProject({ kind: "typed", text: event.target.value }); }}/>{" "}
          <button className={projectChosen ? "" : "setup-primary"} aria-label="Browse for project folder" disabled={busy} onClick={() => { void pick("project"); }}>Browse…</button></p>
        {projectProblem && <p id="first-use-project-problem" className="setup-guidance">{projectProblem}</p>}
        <p id="first-use-project-help"><small>Type or paste the folder's full path, or use Browse… to choose it. Whether the folder exists and can be used is checked when you review; nothing is created.</small></p>
        {noProject && <p>No project for now. You can still have conversations, and choose a project later in Desktop setup.</p>}
        {noProject && <p>Conversations without a project work in one folder that Chirality sets aside. What a conversation creates there stays between launches and is shared by every conversation without a project, including any instructions a conversation writes there.</p>}
        {!noProject && <p><button disabled={busy} onClick={() => { changed(); setProject({ kind: "none" }); }}>Continue without a project</button></p>}
      </li>
      <li><h2>Codex settings</h2>
        <fieldset disabled={busy} className="first-use-routes"><legend className="visually-plain">How Codex is set up for this App</legend>
          <label><input type="radio" name="first-use-route" checked={route === "new"} onChange={() => { changed(); setRoute("new"); }}/> <strong>Start with new settings</strong> (recommended)
            <br/><small>The App creates its own empty Codex settings, instructions file and skills folder inside its data folder. Your existing Codex settings aren't read or changed, and the App doesn't use them.</small></label>
          <label><input type="radio" name="first-use-route" checked={route === "existing"} onChange={() => { changed(); setRoute("existing"); }}/> <strong>Use my existing Codex settings</strong>
            <br/><small>For people who already use Codex: the App links to your own settings, instructions and skills so it sees the same models, providers and tools. It never reads or copies your sign-in.</small></label>
          {keepAvailable && <label><input type="radio" name="first-use-route" checked={route === "keep"} onChange={() => { changed(); setRoute("keep"); }}/> <strong>Keep my current sign-in and settings</strong>; change only the project</label>}
        </fieldset>
        {route === "existing" && <div aria-label="Your existing Codex settings">
          {SHARED.map((item, index) => <p key={item.kind}><label>{item.label} <input aria-label={item.label} value={paths[index]?.displayPath ?? ""} disabled={busy} spellCheck={false} autoCapitalize="off" autoCorrect="off"
            onChange={event => { changed(); const value = typedLocation(event.target.value); setPaths(current => current.map((p, i) => i === index ? value : p)); }}/></label>{" "}
            <button disabled={busy} onClick={() => { void pick(item.kind, index); }}>Choose…</button></p>)}
          <p><small>Choose each one with Choose…, or type its full path. They are usually in the <code>.codex</code> folder in your home folder.</small></p>
        </div>}
      </li>
      <li><h2>Review and confirm</h2>
        <p id="first-use-next" className="setup-guidance" role="status" aria-live="polite">{next}</p>
        <button className="setup-primary" disabled={!ready} aria-describedby="first-use-next" onClick={() => { void review(); }}>Review setup</button>
        {preview && <div className="setup-effects" aria-label="What setup will do" onKeyDown={event => { if (event.key === "Escape" && !pending.current) { event.preventDefault(); changed(); } }}>
          <h3 tabIndex={-1} ref={effectsHeading}>What setup will do</h3>
          <ul>{preview.effects.map(effect => <li key={effect}><Effect text={effect}/></li>)}</ul>
          {preview.locations && preview.locations.length > 0 && <details><summary>Exact locations</summary>
            <dl>{preview.locations.map(location => <div key={location.name}><dt>{location.name}</dt><dd><code className="first-use-path">{location.path}</code></dd></div>)}</dl></details>}
          <p>{preview.standing}</p>
          <p><button className="setup-primary" disabled={busy} onClick={() => { void confirm(); }}>{preview.affirmative}…</button>{" "}
            <button disabled={busy} onClick={changed}>Change my choices</button></p>
          <p><small>The App asks you to confirm in its own dialog. Your current window keeps working until you reopen the App.</small></p>
        </div>}
      </li>
    </ol></>}
    {message && <p ref={feedback} tabIndex={-1} role={failed ? "alert" : "status"}>{failed ? "Setup couldn't finish: " : ""}{message}</p>}
    <details className="setup-diagnostics"><summary>Technical details</summary>
      <p>Launch: {shown.launch.state}. {shown.launch.reason ?? shown.launch.standing}</p>
      <p>App data: {shown.appData ?? shown.appDataProblem ?? "unavailable"}</p>
      <p>Conversations without a project work in: {shown.noProjectFolder ?? "unavailable"}</p>
      <p>Working files (the version check's folders, the connector's folder and Codex's temporary folders): {shown.workingFiles ?? "unavailable"}</p>
      <p>Codex: the copy included with this App ({shown.supplier.path ?? "location unavailable"}). {shown.supplier.standing}</p>
      {!keepAvailable && shown.retainProject?.reason && <p>Keeping an existing sign-in isn't available: {shown.retainProject.reason}</p>}
      {shown.activeResourceProblem && <p>Shared settings could not be checked: {shown.activeResourceProblem}</p>}
      {shown.pending && <><p>{shown.pending.standing}</p><ul>{shown.pending.resources.map(resource => <li key={resource.name}>{resource.name}: {resource.state}{resource.limit ? ` — ${resource.limit}` : ""}</li>)}</ul></>}
      <p>{shown.nextLaunch}</p>
    </details>
  </section>;
}
