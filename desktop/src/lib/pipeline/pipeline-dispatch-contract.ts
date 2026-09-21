export type PipelineCategory = 'DECOMP' | 'PREP' | 'TASK' | 'AUDIT';
export type PipelineTaskScopeMode = 'DELIVERABLES' | 'KNOWLEDGE_TYPES';

export type PipelineDispatchOption = {
  value: string;
  label: string;
  enabled: boolean;
};

export const PIPELINE_CATEGORY_ORDER: readonly PipelineCategory[] = [
  'DECOMP',
  'PREP',
  'TASK',
  'AUDIT'
];

export const PIPELINE_CATEGORY_OPTIONS: Readonly<
  Record<PipelineCategory, readonly PipelineDispatchOption[]>
> = {
  DECOMP: [
    { value: 'SOFTWARE', label: 'SOFTWARE', enabled: true },
    { value: 'PROJECT', label: 'PROJECT', enabled: true },
    { value: 'DOMAIN', label: 'DOMAIN', enabled: true },
    { value: 'BASE', label: 'BASE (create new)', enabled: false }
  ],
  PREP: [
    { value: 'PREPARATION', label: 'PREPARATION', enabled: true },
    { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true },
    { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
    { value: 'CHIRALITY_LENS', label: 'CHIRALITY_LENS', enabled: true }
  ],
  TASK: [
    { value: 'SCOPE_CHANGE', label: 'SCOPE_CHANGE', enabled: true },
    { value: 'SCOPE_PREP', label: 'SCOPE_PREP', enabled: true },
    { value: 'ESTIMATE_PREP', label: 'ESTIMATE_PREP', enabled: true },
    { value: 'AUDIT_PREP', label: 'AUDIT_PREP', enabled: true },
    { value: 'SCHEDULE_PREP', label: 'SCHEDULE_PREP', enabled: true },
    { value: 'ESTIMATING', label: 'ESTIMATING', enabled: false },
    { value: 'SCHEDULING', label: 'SCHEDULING', enabled: false }
  ],
  AUDIT: [
    { value: 'AGENTS', label: 'AGENTS', enabled: true },
    { value: 'DEPENDENCIES', label: 'DEPENDENCIES', enabled: true },
    { value: 'ESTIMATES', label: 'ESTIMATES', enabled: false },
    { value: 'REFERENCES', label: 'REFERENCES', enabled: true },
    { value: 'SCHEDULES', label: 'SCHEDULES', enabled: false },
    { value: 'SCOPE', label: 'SCOPE', enabled: true }
  ]
};

export type PipelineDispatchIssueCode =
  | 'UNKNOWN_CATEGORY'
  | 'UNKNOWN_OPTION'
  | 'OPTION_DISABLED'
  | 'UNKNOWN_SCOPE_MODE'
  | 'SCOPE_NOT_RECORDED'
  | 'KNOWLEDGE_DECOMPOSITION_DISABLED'
  | 'KNOWLEDGE_TYPE_NOT_RECORDED'
  | 'TARGET_DELIVERABLE_REQUIRED'
  | 'TARGET_DELIVERABLE_NOT_RECORDED';

export type PipelineDispatchIssue = {
  code: PipelineDispatchIssueCode;
  message: string;
};

export type PipelineDispatchIntent = {
  kind: 'PIPELINE_DISPATCH_INTENT';
  executionAuthorized: false;
  category: PipelineCategory;
  option: string;
  taskScope?: {
    mode: PipelineTaskScopeMode;
    scopeKey: string;
    targetDeliverableKey?: string;
  };
};

export type PipelineDispatchRequest = {
  category: string;
  option: string;
  taskScopeMode?: string;
  scopeKey?: string;
  targetDeliverableKey?: string;
};

export type PipelineDispatchContext = {
  knowledgeDecompositionEnabled: boolean;
  deliverableKeys: readonly string[];
  knowledgeTypes: readonly {
    id: string;
    matchingDeliverableKeys: readonly string[];
  }[];
};

export type PipelineDispatchValidation =
  | {
      valid: true;
      intent: PipelineDispatchIntent;
      issues: [];
    }
  | {
      valid: false;
      issues: PipelineDispatchIssue[];
    };

function normalized(value: string | null | undefined): string {
  return value?.trim().toUpperCase() ?? '';
}

export function normalizePipelineCategory(
  value: string | null | undefined
): PipelineCategory {
  const candidate = normalized(value);
  return PIPELINE_CATEGORY_ORDER.includes(candidate as PipelineCategory)
    ? (candidate as PipelineCategory)
    : 'DECOMP';
}

export function validatePipelineDispatchIntent(
  request: PipelineDispatchRequest,
  context: PipelineDispatchContext
): PipelineDispatchValidation {
  const issues: PipelineDispatchIssue[] = [];
  const categoryCandidate = normalized(request.category);
  if (!PIPELINE_CATEGORY_ORDER.includes(categoryCandidate as PipelineCategory)) {
    return {
      valid: false,
      issues: [
        {
          code: 'UNKNOWN_CATEGORY',
          message: `Unknown Pipeline category: ${request.category}`
        }
      ]
    };
  }
  const category = categoryCandidate as PipelineCategory;
  const option = normalized(request.option);
  const optionDefinition = PIPELINE_CATEGORY_OPTIONS[category].find(
    (candidate) => candidate.value === option
  );
  if (!optionDefinition) {
    issues.push({
      code: 'UNKNOWN_OPTION',
      message: `Option ${request.option} is not recorded for ${category}.`
    });
  } else if (!optionDefinition.enabled) {
    issues.push({
      code: 'OPTION_DISABLED',
      message: `Option ${optionDefinition.value} is visible but disabled.`
    });
  }

  let taskScope: PipelineDispatchIntent['taskScope'];
  if (category === 'TASK') {
    const scopeMode = normalized(request.taskScopeMode);
    if (scopeMode !== 'DELIVERABLES' && scopeMode !== 'KNOWLEDGE_TYPES') {
      issues.push({
        code: 'UNKNOWN_SCOPE_MODE',
        message: `Unknown TASK scope mode: ${request.taskScopeMode ?? ''}`
      });
    } else if (scopeMode === 'DELIVERABLES') {
      const scopeKey = request.scopeKey?.trim() ?? '';
      if (!scopeKey || !context.deliverableKeys.includes(scopeKey)) {
        issues.push({
          code: 'SCOPE_NOT_RECORDED',
          message: 'TASK deliverable scope must name an admitted deliverable key.'
        });
      } else {
        taskScope = {
          mode: 'DELIVERABLES',
          scopeKey
        };
      }
    } else if (!context.knowledgeDecompositionEnabled) {
      issues.push({
        code: 'KNOWLEDGE_DECOMPOSITION_DISABLED',
        message: 'KNOWLEDGE_TYPES is visible only when the recorded marker is enabled.'
      });
    } else {
      const scopeKey = request.scopeKey?.trim() ?? '';
      const knowledgeType = context.knowledgeTypes.find(
        (candidate) => candidate.id === scopeKey
      );
      if (!knowledgeType) {
        issues.push({
          code: 'KNOWLEDGE_TYPE_NOT_RECORDED',
          message: 'TASK knowledge scope must name an admitted knowledge type.'
        });
      } else {
        const targetDeliverableKey = request.targetDeliverableKey?.trim() ?? '';
        if (!targetDeliverableKey) {
          issues.push({
            code: 'TARGET_DELIVERABLE_REQUIRED',
            message: 'KNOWLEDGE_TYPES dispatch requires a target deliverable.'
          });
        } else if (
          !context.deliverableKeys.includes(targetDeliverableKey) ||
          !knowledgeType.matchingDeliverableKeys.includes(targetDeliverableKey)
        ) {
          issues.push({
            code: 'TARGET_DELIVERABLE_NOT_RECORDED',
            message:
              'Target deliverable must be recorded in both the active deliverable scan and the selected knowledge type.'
          });
        } else {
          taskScope = {
            mode: 'KNOWLEDGE_TYPES',
            scopeKey,
            targetDeliverableKey
          };
        }
      }
    }
  }

  if (issues.length > 0 || !optionDefinition) {
    return {
      valid: false,
      issues
    };
  }

  return {
    valid: true,
    intent: Object.freeze({
      kind: 'PIPELINE_DISPATCH_INTENT',
      executionAuthorized: false,
      category,
      option: optionDefinition.value,
      ...(taskScope ? { taskScope: Object.freeze(taskScope) } : {})
    }),
    issues: []
  };
}

export type PipelineQueryPatch = {
  category?: string | null;
  taskScopeMode?: string | null;
  scopeKey?: string | null;
  targetDeliverableKey?: string | null;
};

type SearchParamSource = string | URLSearchParams | { toString: () => string };

export function mergePipelineQueryParameters(
  current: SearchParamSource,
  patch: PipelineQueryPatch
): URLSearchParams {
  const next = new URLSearchParams(current.toString());
  for (const [key, value] of Object.entries(patch)) {
    if (value === undefined) {
      continue;
    }
    if (value === null || value.trim() === '') {
      next.delete(key);
    } else {
      next.set(key, value);
    }
  }
  return next;
}
