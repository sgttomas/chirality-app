import { useState, type ReactNode } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");

/** One place in the list: where the Library's own index puts the workflow. */
type Section = { key: string; label: string; order: number; entries: Json[] };

const START = "start", OTHER = "other", REPLACED = "replaced";
const tierRank = (entry: Json) => (entry?.navigation?.tier === "supporting" ? 1 : 0);
const orderOf = (entry: Json) => (Number.isFinite(entry?.navigation?.order) ? entry.navigation.order : Number.MAX_SAFE_INTEGER);
const byPlace = (a: Json, b: Json) => tierRank(a) - tierRank(b) || orderOf(a) - orderOf(b) || text(a.name).localeCompare(text(b.name));

/**
 * The included workflows in the Library's own grouping: the ones its index
 * marks core first, then its groups in its order, then any without a group,
 * then the ones it marks superseded. Each heading says only what the index
 * says; nothing here is the App's judgment of a workflow or advice to use one.
 */
export function includedSections(entries: Json[]): Section[] {
  const sections = new Map<string, Section>();
  const place = (key: string, label: string, order: number, entry: Json) => {
    if (!sections.has(key)) sections.set(key, { key, label, order, entries: [] });
    sections.get(key)!.entries.push(entry);
  };
  for (const entry of entries) {
    const navigation = entry?.navigation ?? {};
    const group = navigation.group;
    if (navigation.category === "superseded") place(REPLACED, "Marked superseded by the Library", Number.MAX_SAFE_INTEGER, entry);
    else if (navigation.category === "core") place(START, "The Library's core workflows", -1, entry);
    else if (group && typeof group.key === "string" && typeof group.label === "string") place(`group:${group.key}`, group.label, Number.isFinite(group.order) ? group.order : Number.MAX_SAFE_INTEGER - 2, entry);
    else place(OTHER, "Other workflows", Number.MAX_SAFE_INTEGER - 1, entry);
  }
  return [...sections.values()].sort((a, b) => a.order - b.order || a.label.localeCompare(b.label)).map(section => ({ ...section, entries: [...section.entries].sort(byPlace) }));
}

/** Every word typed appears in the workflow's name, description or group. */
export function matchesSearch(entry: Json, search: string): boolean {
  const words = search.toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return true;
  const hay = [entry?.name, entry?.navigation?.displayName, entry?.description, entry?.navigation?.group?.label].map(text).join(" ").toLowerCase();
  return words.every(word => hay.includes(word));
}

const IDENTITY_FIELDS = ["kind", "origin", "source_root", "name", "revision", "revision_method"];
/**
 * The catalogue entry a selection is, by its whole source-qualified identity
 * as the host gives both. A matching name, origin or revision alone is not
 * the same workflow, and an entry or selection without an identity matches nothing.
 */
export function includedEntryOf(catalog: Json, selection: Json): Json | undefined {
  const chosen = selection?.identity;
  if (!chosen || typeof chosen !== "object") return undefined;
  return list(catalog?.entries).find(entry => entry?.identity && typeof entry.identity === "object"
    && IDENTITY_FIELDS.every(field => typeof chosen[field] === "string" && chosen[field] === entry.identity[field]));
}

/**
 * The conversation's role beside the roles the Library lists for the chosen
 * workflow: two facts side by side, with no judgment of fit. The role is the
 * App's own record of what it supplied at the conversation's start; where
 * this App process holds none, that is said. Shown only for a selection that
 * is a catalogue entry, since only the catalogue carries the Library's list.
 */
export function RoleBesideWorkflow({ entry, conversation }: { entry: Json; conversation: Json }) {
  const roles = list(entry?.roles).filter(role => typeof role === "string");
  if (!entry || !roles.length) return null;
  const appRole = conversation?.appRole;
  const role = appRole?.standing !== "app-observed" ? "This conversation's role is not known to this App process."
    : typeof appRole.role === "string" && appRole.role ? `This conversation is in the role ${appRole.role}.` : "This conversation was started with no role.";
  return <p aria-label="Role and the workflow's listed roles">{role} The Library lists {text(entry.name)} for: {roles.join(", ")}.</p>;
}

/** Where the included workflows come from, as the catalogue states it. */
export function librarySourceWords(source: Json): string {
  const tag = text(source?.tag);
  const version = /^library-v(.+)$/.exec(tag)?.[1];
  return version ? `Chirality Library ${version}` : tag ? `Chirality Library (${tag})` : "";
}

/** The Library paths a catalogue entry's files name that the App does not include. */
const libraryPathsOf = (entry: Json): string[] => list(entry?.libraryPathsNamed).filter(path => typeof path === "string");
/**
 * The About disclosure's sentence for those paths, the place a person meets
 * LIM-008 (docs/RELEASE_LIMITATIONS_4.0.0.md): the workflow ships as its text,
 * without the Library's tools it names. One sentence, used in About and beside
 * the chosen workflow, so the two never say it differently.
 */
function libraryPathsSentence(paths: string[], from: string): ReactNode {
  return <>This workflow's files name {paths.length === 1 ? "1 path" : `${paths.length} paths`} of {from || "the Chirality Library"} that {paths.length === 1 ? "is" : "are"} not included in the App (for example <code>{paths[0]}</code>). The App has not checked whether a run uses {paths.length === 1 ? "it" : "them"}.</>;
}
/**
 * Beside the chosen workflow: the same sentence as its About, for a catalogue
 * entry whose files name Library paths. Nothing for an entry that names none,
 * or for a selection that is not a catalogue entry.
 */
export function LibraryPathsBesideWorkflow({ entry, source }: { entry: Json; source: Json }) {
  const paths = libraryPathsOf(entry);
  if (!entry || !paths.length) return null;
  return <p role="note" aria-label="Library paths the workflow names">{libraryPathsSentence(paths, librarySourceWords(source))}</p>;
}

function About({ entry, source, textControl, open }: { entry: Json; source: Json; textControl?: ReactNode; open: boolean }) {
  const paths = libraryPathsOf(entry);
  const roles = list(entry?.roles).filter(role => typeof role === "string");
  const from = librarySourceWords(source);
  return <details open={open ? true : undefined}><summary>About {text(entry.name)}</summary>
    <p>Source: {from ? `${from}, included with the App` : "included with the App"}. Revision <code title={text(entry.revision)}>{text(entry.revision).slice(0, 12)}…</code></p>
    {textControl}
    {roles.length > 0 && <p>The Library lists it for these roles: {roles.join(", ")}.</p>}
    {entry?.compatibility === "legacy" && <p>The Library marks it as legacy.</p>}
    {paths.length > 0 && <>
      <p>{libraryPathsSentence(paths, from)}</p>
      {paths.length > 1 && <details><summary>All {paths.length} paths</summary><ul>{paths.map(path => <li key={path}><code>{path}</code></li>)}</ul></details>}
    </>}
  </details>;
}

/**
 * The workflows included with the App, grouped and searchable, each with the
 * Library's one-sentence description. Choosing calls the guide's own command;
 * nothing here reads requirements from a workflow's text. Where the guide
 * offers it, each entry's About holds the control to read the workflow's own
 * text (`readText`); an entry whose text is held (`holdsText`) is shown open,
 * so that text is still in view when the list is drawn again.
 */
export function IncludedWorkflows({ catalog, chosen, disabled, needsConversation, choose, readText, holdsText }: {
  catalog: Json; chosen?: Json; disabled: boolean; needsConversation: boolean; choose: (name: string) => void;
  readText?: (entry: Json) => ReactNode; holdsText?: (entry: Json) => boolean;
}) {
  const [search, setSearch] = useState("");
  const entries = list(catalog?.entries);
  if (!entries.length) return null;
  const from = librarySourceWords(catalog?.source);
  const searching = search.trim() !== "";
  const found = entries.filter(entry => matchesSearch(entry, search));
  const sections = includedSections(found);
  // Chosen is said only of the entry the selection is, by its whole identity,
  // and only when the host admits that selection to run. A copy with the same
  // identity that the host does not admit leaves the included entry's Use.
  const chosenEntry = chosen?.runnable === true ? includedEntryOf(catalog, chosen) : undefined;
  const isChosen = (entry: Json) => chosenEntry === entry;
  const holds = (entry: Json) => holdsText?.(entry) === true;
  const row = (entry: Json) => {
    const shownName = text(entry?.navigation?.displayName) || text(entry.name);
    return <li key={text(entry.name)} aria-label={`Included workflow ${text(entry.name)}`}>
      <strong>{shownName}</strong>{shownName !== entry.name && <> (<code>{text(entry.name)}</code>)</>}{entry.description ? <> — {text(entry.description)}</> : null}{" "}
      {isChosen(entry) ? <em>Chosen.</em>
        : entry.runnable === true ? <button disabled={disabled || needsConversation} onClick={() => choose(entry.name)}>Use {text(entry.name)}</button>
        : entry.runnable === false ? <small>Can't be used in this App: {text(entry.runLimit) || text(catalog?.standing) || "the App reports it as not runnable"}.</small>
        : <small>The App hasn't reported whether this workflow can be used here.</small>}
      <About entry={entry} source={catalog?.source} textControl={readText?.(entry)} open={holds(entry)}/>
    </li>;
  };
  return <div aria-label="Workflows included with the App">
    <p>Included with the App: {entries.length === 1 ? "1 workflow" : `${entries.length} workflows`}{from ? ` from ${from}` : ""}.{needsConversation ? " Choose a conversation above to use one." : ""}</p>
    {(entries.length > 6 || searching) && <label>Find a workflow <input type="search" value={search} onChange={event => setSearch(event.target.value)} spellCheck={false} autoCapitalize="off" autoCorrect="off"/></label>}
    {searching && <p role="status">{found.length === 0 ? "No included workflow matches. Try fewer or other words." : `${found.length} of ${entries.length} match.`}</p>}
    {entries.length <= 6 ? <ul>{[...found].sort(byPlace).map(row)}</ul>
      : sections.map(section => <details key={section.key} open={searching || section.key === START || section.entries.some(isChosen) || section.entries.some(holds) ? true : undefined}>
        <summary>{section.label} ({section.entries.length})</summary>
        <ul>{section.entries.map(row)}</ul>
      </details>)}
  </div>;
}
