export type TaskScopeMode = 'DELIVERABLES' | 'KNOWLEDGE_TYPES';

export type TaskKnowledgeType = {
  id: string;
  matchingDeliverableKeys: string[];
};

export type TaskSelectionSnapshot = {
  scopeMode: TaskScopeMode;
  scopeKey: string;
  targetDeliverableKey: string;
};

export function buildDeliverableCompositeKey(pkg: string, deliverableId: string): string {
  return `${pkg}::${deliverableId}`;
}

export function normalizeTaskScopeMode(
  rawMode: string | null | undefined,
  knowledgeDecompositionEnabled: boolean
): TaskScopeMode {
  const normalized = (rawMode ?? '').trim().toUpperCase();
  if (normalized === 'KNOWLEDGE_TYPES' && knowledgeDecompositionEnabled) {
    return 'KNOWLEDGE_TYPES';
  }
  return 'DELIVERABLES';
}

export function sanitizeTaskSelection(
  snapshot: TaskSelectionSnapshot,
  options: {
    knowledgeDecompositionEnabled: boolean;
    deliverableKeys: string[];
    knowledgeTypes: TaskKnowledgeType[];
  }
): TaskSelectionSnapshot {
  const deliverableKeySet = new Set(options.deliverableKeys.filter(Boolean));

  if (snapshot.scopeMode === 'KNOWLEDGE_TYPES') {
    if (!options.knowledgeDecompositionEnabled) {
      return {
        scopeMode: 'DELIVERABLES',
        scopeKey: '',
        targetDeliverableKey: ''
      };
    }

    const selectedKnowledgeType = options.knowledgeTypes.find(
      (candidate) => candidate.id === snapshot.scopeKey
    );
    if (!selectedKnowledgeType) {
      return {
        scopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: '',
        targetDeliverableKey: ''
      };
    }

    const availableTargetKeys = selectedKnowledgeType.matchingDeliverableKeys.filter((key) =>
      deliverableKeySet.has(key)
    );
    if (availableTargetKeys.length === 0) {
      return {
        scopeMode: 'KNOWLEDGE_TYPES',
        scopeKey: selectedKnowledgeType.id,
        targetDeliverableKey: ''
      };
    }

    return {
      scopeMode: 'KNOWLEDGE_TYPES',
      scopeKey: selectedKnowledgeType.id,
      targetDeliverableKey: availableTargetKeys.includes(snapshot.targetDeliverableKey)
        ? snapshot.targetDeliverableKey
        : ''
    };
  }

  return {
    scopeMode: 'DELIVERABLES',
    scopeKey: deliverableKeySet.has(snapshot.scopeKey) ? snapshot.scopeKey : '',
    targetDeliverableKey: ''
  };
}
