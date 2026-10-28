import { conversationName, conversationReference, findConversation } from "./TrialComposer";
import { nativePathText } from "./presentation";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const nonempty = (value: Json): value is string => typeof value === "string" && value.length > 0;

/** Selector keys are complete references, never a saved bare-ID lookup. */
export function conversationFromKey(key: string): Json | null {
  try {
    const value = JSON.parse(key);
    return Array.isArray(value) && value.length === 2 ? conversationReference({ generation: value[0], threadId: value[1] }) : null;
  } catch { return null; }
}
export function workflowSourceLimit(host: Json): string | null {
  const context = host?.workflowRoot?.context;
  if (!nonempty(context?.sourceRef)) return "current workflow source is unavailable";
  if (context.generation === null && host?.generation === null) return null; // library inspection before a native generation
  return findConversation([{ generation: host?.generation, threadId: "source-check" }], { generation: context?.generation, threadId: "source-check" })
    ? null : "workflow source and native generation do not correspond";
}

/** Read-only context; the caller owns the choice and its lifetime. */
export function ConversationContext({ label, host, reference, empty, limit, workflow = false }: {
  label: string; host: Json; reference: Json; empty?: string; limit?: string | null; workflow?: boolean;
}) {
  const ref = conversationReference(reference);
  const unavailable = limit || (workflow ? workflowSourceLimit(host) : null)
    || (!ref ? (empty ? null : "a complete conversation reference is unavailable")
      : host?.generationClosed === true || host?.state !== "ready" ? "the native generation is closed or unavailable"
      : !findConversation([{ generation: host?.generation, threadId: ref.threadId }], ref) ? "the chosen home or generation is not current"
      : !findConversation(host?.threads, ref) ? "the exact conversation is not loaded" : null);
  return <div aria-label={label}>
    <b>{label}:</b> {unavailable ? `Unavailable — ${unavailable}.` : ref ? `Conversation ${conversationName(ref)}` : empty}
    {ref && <details><summary>Exact conversation reference{unavailable ? " (original choice)" : ""}</summary>
      <dl><dt>Conversation</dt><dd>{ref.threadId}</dd><dt>Home</dt><dd>{ref.generation.home}</dd>
        <dt>App session</dt><dd>{ref.generation.appSession}</dd><dt>Generation</dt><dd>{ref.generation.spawnCounter}</dd>
        {workflow && <><dt>Current workflow source</dt><dd>{host?.workflowRoot?.context?.sourceRef ?? "unavailable"}</dd></>}
      </dl>
    </details>}
  </div>;
}

/** Fixed project and opened library are Root observations, independent of a
 * supplier closing. Neither projectLibraryAvailable nor native cwd is a path. */
export function ProjectLibraryContext({ host }: { host: Json }) {
  const project = host?.currentAppProjectContext;
  const projectLimit = host?.currentAppProjectContextLimit;
  const knownProject = !projectLimit && nonempty(project?.reference);
  const launch = host?.attachmentSelections?.launchAppProjectObservation;
  const launchPath = nativePathText(launch?.nativeRoot);
  // Both producers receive the same launch workspace. Use that path only when
  // its exact projection agrees with the frozen reference; never decode an
  // opaque reference or infer an accepted REC/native/actor association.
  const projectPath = knownProject && launch?.source === "explicit App launch CHIRALITY_WORKSPACE" && launchPath !== null
    && (project.reference === launchPath || project.reference === JSON.stringify(launch.nativeRoot)) ? launchPath : null;
  const root = host?.workflowRoot;
  const libraries = Array.isArray(root?.libraries) ? root.libraries : [];
  const matches = nonempty(root?.activeLibrary) ? libraries.filter((library: Json) => library?.reference === root.activeLibrary) : [];
  const library = matches.length === 1 ? matches[0] : null;
  const path = nativePathText(library?.root);
  return <dl aria-label="Project and opened library">
    <dt>Fixed App project</dt><dd><span aria-label="Fixed App project display">{knownProject
      ? projectPath !== null ? <code>{projectPath}</code> : `${project.sourceCaption || "Known explicit App project"}; folder display unavailable — exact reference below.`
      : `Unavailable — ${projectLimit || "explicit App project reference not established"}.`}</span>
      {knownProject && <details><summary>Exact App project reference</summary><code>{project.reference}</code><p>{project.sourceCaption}. {project.standing}</p>
        {projectPath !== null && <p>{launch.associationStanding}</p>}
      </details>}
    </dd>
    <dt>Opened workflow library</dt><dd>{!root ? "Unavailable — workflow library view is unavailable."
      : root.activeLibrary === null || root.activeLibrary === "" ? "No library opened."
      : !library ? "Unavailable — active library reference is missing or ambiguous."
      : path === null ? "Unavailable — opened library folder identity is not readable."
      : <>{nonempty(library.origin) ? library.origin : "Origin unavailable"} library · <code>{path}</code></>}
      {library && <details><summary>Exact opened library identity</summary><dl>
        <dt>Library reference</dt><dd>{library.reference}</dd><dt>Source root</dt><dd>{nonempty(library.sourceRoot) ? library.sourceRoot : "unavailable"}</dd>
      </dl></details>}
    </dd>
  </dl>;
}
