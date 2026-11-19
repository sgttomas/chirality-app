import { boundedTitle, choiceLabels, ChoiceTitle, CHOICE_TITLES_ATTRIBUTION } from "./AgentText";
import { threadChoices } from "./presentation";

type Json = any;

/** One conversation listed in the navigator. */
export type NavigatorEntry = {
  /** The conversation's key, as the conversation view keys its choices: [generation, threadId]. */
  key: string;
  threadId: string;
  /** The App's words naming it, as the conversation view's chooser names it (choiceLabels). */
  title: string;
  /** The title Codex supplies for it, if any: shown beside the entry, marked, by the component every conversation choice uses. */
  suppliedTitle: unknown;
  /** Codex reports a turn under way in it (its status type is "active"). */
  live: boolean;
  /** The host status holds a request for it that waits for the person's answer. */
  needsAnswer: boolean;
  /** The folder Codex reports the conversation working in; null where the row carries none. */
  folder: string | null;
};
/** One project: a folder and the conversations listed under it. */
export type NavigatorProject = {
  /** The folder's path; null when the App has not established it. */
  folder: string | null;
  entries: NavigatorEntry[];
};

const sameGeneration = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);
export const conversationKey = (row: Json) => JSON.stringify([row?.generation, row?.threadId]);

/** The loaded conversations of the current generation (the host's thread rows), as navigator entries. `waiting` holds
 * each conversation with a request that waits for the person's answer, read as "Waiting on you" reads it. */
export function navigatorEntries(host: Json, waiting: ReadonlySet<string>): NavigatorEntry[] {
  const rows = (Array.isArray(host?.threads) ? host.threads : []).filter((t: Json) => sameGeneration(t?.generation, host?.generation) && typeof t?.threadId === "string");
  const choices = threadChoices(rows, conversationKey);
  const labels = choiceLabels(choices);
  return rows.map((row: Json, i: number) => ({
    key: conversationKey(row), threadId: row.threadId, title: labels[i], suppliedTitle: choices[i].title,
    live: row?.status?.type === "active", needsAnswer: waiting.has(row.threadId),
    folder: typeof row?.cwd === "string" && row.cwd ? row.cwd : null,
  }));
}

/** The same path as written, but for one trailing separator. Two spellings of one folder (an alias) do not match. */
const samePath = (a: string, b: string) => a.replace(/\/$/, "") === b.replace(/\/$/, "");
/**
 * The entries by project. Only the App's own project, the one it has established, gets a heading, and a conversation
 * is listed under it only where Codex reports it working in exactly that folder. Every other conversation (one
 * continued from another folder, one whose folder is not reported, any conversation while the App has no project) is
 * listed under no heading: a reported path alone does not establish a project. The App's project comes first, listed
 * even when empty.
 */
export function navigatorProjects(appFolder: string | null, entries: readonly NavigatorEntry[]): NavigatorProject[] {
  const inProject = (entry: NavigatorEntry) => appFolder !== null && entry.folder !== null && samePath(appFolder, entry.folder);
  const projects: NavigatorProject[] = appFolder !== null ? [{ folder: appFolder, entries: entries.filter(inProject) }] : [];
  const unplaced = entries.filter(entry => !inProject(entry));
  return unplaced.length ? [...projects, { folder: null, entries: unplaced }] : projects;
}

/** The folder's name: the last part of its path. */
export function folderName(path: string): string {
  const parts = path.split(/[\\/]+/).filter(Boolean);
  return parts.length ? parts[parts.length - 1] : path;
}

function EntryRow({ entry, selected, disabled, choose, answer }: { entry: NavigatorEntry; selected: boolean; disabled: boolean; choose: (key: string) => void; answer: (entry: NavigatorEntry) => void }) {
  return <li>
    <div className="woven-navigator-session-row">
      <button type="button" className={`woven-navigator-session${entry.live ? " woven-navigator-session--live" : ""}`} data-session-id={entry.threadId} disabled={disabled} aria-pressed={selected} onClick={() => { if (!disabled) choose(entry.key); }}>
        <span className="woven-navigator-session-heading">{entry.live ? <span className="woven-navigator-session-dot" role="img" aria-label="Live session"/> : null}<span className="woven-navigator-session-title">{entry.title}</span></span>
      </button>
      {/* The supplied title stands beside the entry, outside its name and its clickable area: no control holds supplied text. */}
      {boundedTitle(entry.suppliedTitle) !== null ? <span className="navigator-entry-title"><ChoiceTitle value={entry.suppliedTitle}/></span> : null}
      {entry.needsAnswer ? <button type="button" className="button-muted" aria-label={`Needs answer: ${entry.title}`} onClick={() => answer(entry)}>Needs answer</button> : null}
    </div>
  </li>;
}

/** A project: its folder's heading, as 3.0.1 draws it, and its conversations. The folder's name is the person's, not
 * the App's words, so the heading is not a control here; a folder the App has not established has no heading. */
function ProjectSection({ project, selectedKey, disabled, choose, answer }: { project: NavigatorProject; selectedKey: string; disabled: boolean; choose: (key: string) => void; answer: (entry: NavigatorEntry) => void }) {
  return <section className={project.folder !== null ? "woven-chat-section woven-chat-section--folder" : "woven-chat-section"}>
    {project.folder !== null ? <div className="woven-chat-section-heading woven-chat-section-heading--folder">
      <span><span aria-hidden="true">▱ </span>{folderName(project.folder)}</span><span>{project.entries.length}</span>
    </div> : null}
    <ul className="woven-navigator-session-list">
      {project.entries.map(entry => <EntryRow key={entry.key} entry={entry} selected={entry.key === selectedKey} disabled={disabled} choose={choose} answer={answer}/>)}
    </ul>
  </section>;
}

/** The account row's place at the foot of the navigator: here it opens Settings & tools. */
export function AccountRow({ open }: { open: () => void }) {
  return <div className="account-controls-root">
    <button type="button" className="account-controls-row" aria-label="Settings & tools" onClick={open}>
      <span className="account-controls-avatar" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="8.5" r="3.5"/><path d="M4.5 20c.9-3.6 3.8-5.5 7.5-5.5s6.6 1.9 7.5 5.5"/></svg></span>
      <span className="account-controls-identity"><strong>Settings &amp; tools</strong></span>
    </button>
  </div>;
}

/**
 * The left region: the brand, New chat, each project's conversations and the account row. It shows only what the
 * App can back. `choose` is the conversation view's own choice (null while that view takes no choice); `answer`
 * reveals a conversation's waiting requests as "Waiting on you" does.
 */
export function Navigator({ projects, selectedKey, choose, answer, newChat, openSettings }: {
  projects: readonly NavigatorProject[]; selectedKey: string; choose: ((key: string) => void) | null;
  answer: (entry: NavigatorEntry) => void; newChat: () => void; openSettings: () => void;
}) {
  return <nav className="woven-navigator" aria-label="Workspace Navigator">
    <h1 className="woven-navigator-brand">Chirality</h1>
    <div className="woven-navigator-sections">
      <button type="button" className="woven-new-chat" onClick={newChat}><span aria-hidden="true">＋</span> New chat</button>
      {projects.some(project => project.entries.some(entry => boundedTitle(entry.suppliedTitle) !== null)) ? <p className="conversation-choices-attribution"><small>{CHOICE_TITLES_ATTRIBUTION}</small></p> : null}
      <div className="woven-navigator-sessions">
        {projects.map((project, i) => <ProjectSection key={project.folder ?? `project-${i}`} project={project} selectedKey={selectedKey} disabled={!choose} choose={key => choose?.(key)} answer={answer}/>)}
      </div>
    </div>
    <footer className="woven-compatibility"><AccountRow open={openSettings}/></footer>
  </nav>;
}
