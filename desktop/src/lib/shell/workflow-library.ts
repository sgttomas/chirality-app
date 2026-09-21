import type { MethodDescriptor } from '../harness/method-selection-client';

/**
 * Pure grouping of the Runtime method catalog for the Workflows tab. The
 * categories come from each descriptor's `navigation` (authored in the Root
 * workflow catalog and emitted into `workflows/index.json`); the App adds no
 * interpretation of its own. Project and user workflows carry no navigation
 * and are grouped by their source-qualified origin only.
 */
export type SpecialistGroup = { key: string; label: string; order: number; primary: MethodDescriptor[]; supporting: MethodDescriptor[] };

export type WorkflowLibrary = {
  core: MethodDescriptor[];
  specialist: SpecialistGroup[];
  /** Workflows saved in the current project (`.chirality/workflows`), including plans saved as workflows. */
  projectSpecific: MethodDescriptor[];
  /** The user's own library (`~/.chirality/workflows`): personal, not project-local. */
  personal: MethodDescriptor[];
  superseded: MethodDescriptor[];
  /** Bundled workflows the catalog did not place; shown so nothing is hidden. */
  unplaced: MethodDescriptor[];
};

function byOrderThenName(left: MethodDescriptor, right: MethodDescriptor): number {
  const leftOrder = left.navigation?.order ?? Number.MAX_SAFE_INTEGER;
  const rightOrder = right.navigation?.order ?? Number.MAX_SAFE_INTEGER;
  return leftOrder - rightOrder || left.name.localeCompare(right.name);
}

function byName(left: MethodDescriptor, right: MethodDescriptor): number {
  return left.name.localeCompare(right.name);
}

export function workflowDisplayName(method: MethodDescriptor): string {
  return method.navigation?.displayName?.trim() || method.name;
}

export function groupWorkflowLibrary(methods: readonly MethodDescriptor[]): WorkflowLibrary {
  const library: WorkflowLibrary = { core: [], specialist: [], projectSpecific: [], personal: [], superseded: [], unplaced: [] };
  const groups = new Map<string, SpecialistGroup>();
  for (const method of methods) {
    if (method.kind !== 'workflow') continue;
    if (method.source === 'project') { library.projectSpecific.push(method); continue; }
    if (method.source === 'user') { library.personal.push(method); continue; }
    const navigation = method.navigation;
    if (!navigation) { library.unplaced.push(method); continue; }
    if (navigation.category === 'core') { library.core.push(method); continue; }
    if (navigation.category === 'superseded') { library.superseded.push(method); continue; }
    const key = navigation.group?.key ?? 'other';
    const group = groups.get(key) ?? { key, label: navigation.group?.label ?? 'Other', order: navigation.group?.order ?? Number.MAX_SAFE_INTEGER, primary: [], supporting: [] };
    (navigation.tier === 'supporting' ? group.supporting : group.primary).push(method);
    groups.set(key, group);
  }
  library.core.sort(byOrderThenName);
  library.superseded.sort(byOrderThenName);
  library.projectSpecific.sort(byName);
  library.personal.sort(byName);
  library.unplaced.sort(byName);
  library.specialist = [...groups.values()].sort((left, right) => left.order - right.order || left.label.localeCompare(right.label))
    .map(group => ({ ...group, primary: [...group.primary].sort(byOrderThenName), supporting: [...group.supporting].sort(byOrderThenName) }));
  return library;
}

/** Case-insensitive match over identifier, display name, description and metadata text. */
export function methodMatchesQuery(method: MethodDescriptor, query: string): boolean {
  const needle = query.trim().toLowerCase();
  if (!needle) return true;
  const haystack = [method.name, workflowDisplayName(method), method.description, method.navigation?.group?.label ?? '',
    ...Object.values(method.metadata ?? {}).flatMap(value => typeof value === 'string' ? [value] : Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : [])]
    .join('\n').toLowerCase();
  return haystack.includes(needle);
}
