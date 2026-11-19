import { numberWords, wordOf } from "./AgentText";
import { type ReactNode } from "react";

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
/** The Library's workflow groups in the edition the App ships (resources/production_workflows/MANIFEST.json), as the
 * App's own table: a section is named from it only when an entry's group key and label are both in it. Any other
 * group is shown under "Other workflows", so a section heading holds only the App's words. */
export const LIBRARY_GROUPS = {
  "plan-organize": "Plan & organize", "research-understand": "Research & understand", "extract-documents": "Extract from documents",
  "build-maintain-software": "Build & maintain software", "estimate-cost": "Estimate & cost", "review-check": "Review & check",
  "manage-changes": "Manage changes", "author-publish": "Author & publish",
} as const;
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
    else if (group && wordOf(LIBRARY_GROUPS, group.key) !== null && wordOf(LIBRARY_GROUPS, group.key) === group.label) place(`group:${group.key}`, wordOf(LIBRARY_GROUPS, group.key) ?? "", Number.isFinite(group.order) ? group.order : Number.MAX_SAFE_INTEGER - 2, entry);
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
 * LIM-008 of the release's limitations: the workflow ships as its text,
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
export function LibraryPathsBesideWorkflow({ entry, source, all = false }: { entry: Json; source: Json; all?: boolean }) {
  const paths = libraryPathsOf(entry);
  if (!entry || !paths.length) return null;
  return <>
    <p role="note" aria-label="Library paths the workflow names">{libraryPathsSentence(paths, librarySourceWords(source))}</p>
    {/* Every path, where the card's Details are read (the former Run a workflow guide's About listed them). */}
    {all && paths.length > 1 && <details><summary>All {numberWords(paths.length)} paths</summary><ul>{paths.map(path => <li key={path}><code>{path}</code></li>)}</ul></details>}
  </>;
}
