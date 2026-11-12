import { useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");

/** One place in the list: where the Library's own index puts the workflow. */
type Section = { key: string; label: string; note?: string; order: number; entries: Json[] };

const START = "start", OTHER = "other", REPLACED = "replaced";
const tierRank = (entry: Json) => (entry?.navigation?.tier === "supporting" ? 1 : 0);
const orderOf = (entry: Json) => (Number.isFinite(entry?.navigation?.order) ? entry.navigation.order : Number.MAX_SAFE_INTEGER);
const byPlace = (a: Json, b: Json) => tierRank(a) - tierRank(b) || orderOf(a) - orderOf(b) || text(a.name).localeCompare(text(b.name));

/**
 * The included workflows in the Library's own grouping: its core workflows
 * first, then its groups in its order, then any without a group, then the ones
 * it marks superseded. Nothing here is the App's judgment of a workflow.
 */
export function includedSections(entries: Json[]): Section[] {
  const sections = new Map<string, Section>();
  const place = (key: string, label: string, order: number, entry: Json, note?: string) => {
    if (!sections.has(key)) sections.set(key, { key, label, note, order, entries: [] });
    sections.get(key)!.entries.push(entry);
  };
  for (const entry of entries) {
    const navigation = entry?.navigation ?? {};
    const group = navigation.group;
    if (navigation.category === "superseded") place(REPLACED, "Replaced by newer workflows", Number.MAX_SAFE_INTEGER, entry, "The Library keeps these for work that already uses them.");
    else if (navigation.category === "core") place(START, "Start here", -1, entry, "The Library's core workflows.");
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

/** Where the included workflows come from, as the catalogue states it. */
export function librarySourceWords(source: Json): string {
  const tag = text(source?.tag);
  const version = /^library-v(.+)$/.exec(tag)?.[1];
  return version ? `Chirality Library ${version}` : tag ? `Chirality Library (${tag})` : "";
}

function About({ entry, source }: { entry: Json; source: Json }) {
  const paths = list(entry?.libraryPathsNamed).filter(path => typeof path === "string");
  const roles = list(entry?.roles).filter(role => typeof role === "string");
  const from = librarySourceWords(source);
  return <details><summary>About {text(entry.name)}</summary>
    <p>Source: {from ? `${from}, included with the App` : "included with the App"}. Revision <code title={text(entry.revision)}>{text(entry.revision).slice(0, 12)}…</code></p>
    {roles.length > 0 && <p>The Library lists it for these roles: {roles.join(", ")}.</p>}
    {entry?.compatibility === "legacy" && <p>The Library marks it as legacy.</p>}
    {paths.length > 0 && <>
      <p>This workflow's text names Chirality Library tools that are not included in the App ({paths.length} {paths.length === 1 ? "path" : "paths"}, for example <code>{paths[0]}</code>). Steps that use them need those files present at the same paths, obtained from {from || "the Chirality Library"}. The Library does not say which of them a run requires.</p>
      {paths.length > 1 && <details><summary>All {paths.length} paths</summary><ul>{paths.map(path => <li key={path}><code>{path}</code></li>)}</ul></details>}
    </>}
  </details>;
}

/**
 * The workflows included with the App, grouped and searchable, each with the
 * Library's one-sentence description. Choosing calls the guide's own command;
 * nothing here reads requirements from a workflow's text.
 */
export function IncludedWorkflows({ catalog, chosen, disabled, needsConversation, choose }: {
  catalog: Json; chosen?: Json; disabled: boolean; needsConversation: boolean; choose: (name: string) => void;
}) {
  const [search, setSearch] = useState("");
  const entries = list(catalog?.entries);
  if (!entries.length) return null;
  const from = librarySourceWords(catalog?.source);
  const found = entries.filter(entry => matchesSearch(entry, search));
  const sections = includedSections(found);
  const searching = search.trim() !== "";
  const isChosen = (entry: Json) => chosen?.identity?.origin === "bundled" && chosen.identity?.name === entry.name && chosen.identity?.revision === entry.revision;
  const row = (entry: Json) => {
    const shownName = text(entry?.navigation?.displayName) || text(entry.name);
    return <li key={text(entry.name)} aria-label={`Included workflow ${text(entry.name)}`}>
      <strong>{shownName}</strong>{shownName !== entry.name && <> (<code>{text(entry.name)}</code>)</>}{entry.description ? <> — {text(entry.description)}</> : null}{" "}
      {isChosen(entry) ? <em>Chosen.</em>
        : entry.runnable === true ? <button disabled={disabled || needsConversation} onClick={() => choose(entry.name)}>Use {text(entry.name)}</button>
        : <small>Can't be used in this App: {text(entry.runLimit) || text(catalog?.standing) || "the App reports it as not runnable"}.</small>}
      <About entry={entry} source={catalog?.source}/>
    </li>;
  };
  return <div aria-label="Workflows included with the App">
    <p>Included with the App: {entries.length === 1 ? "1 workflow" : `${entries.length} workflows`}{from ? ` from ${from}` : ""}.{needsConversation ? " Choose a conversation above to use one." : ""}</p>
    {entries.length > 6 && <label>Find a workflow <input type="search" value={search} onChange={event => setSearch(event.target.value)} spellCheck={false} autoCapitalize="off" autoCorrect="off"/></label>}
    {searching && <p role="status">{found.length === 0 ? "No included workflow matches. Try fewer or other words." : `${found.length} of ${entries.length} match.`}</p>}
    {entries.length <= 6 ? <ul>{[...found].sort(byPlace).map(row)}</ul>
      : sections.map(section => <details key={section.key} open={searching || section.key === START || section.entries.some(isChosen) ? true : undefined}>
        <summary>{section.label} ({section.entries.length})</summary>
        {section.note && <p><small>{section.note}</small></p>}
        <ul>{section.entries.map(row)}</ul>
      </details>)}
  </div>;
}
