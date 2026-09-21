export const FILE_TREE_POLL_INTERVAL_MS = 15_000;
export const FILE_TREE_REFRESH_DEBOUNCE_MS = 350;

type TimerHandle = ReturnType<typeof setTimeout>;

type RefreshSchedulerOptions = {
  debounceMs?: number;
  onRefresh: () => void;
  onAfterRefresh?: () => void;
};

export type RefreshScheduler = {
  schedule: () => void;
  cancel: () => void;
};

export function createRefreshScheduler(options: RefreshSchedulerOptions): RefreshScheduler {
  const debounceMs = options.debounceMs ?? FILE_TREE_REFRESH_DEBOUNCE_MS;
  let timeout: TimerHandle | null = null;

  const cancel = (): void => {
    if (timeout === null) {
      return;
    }

    clearTimeout(timeout);
    timeout = null;
  };

  const schedule = (): void => {
    cancel();
    timeout = setTimeout(() => {
      timeout = null;
      options.onRefresh();
      options.onAfterRefresh?.();
    }, debounceMs);
  };

  return { schedule, cancel };
}

export function shouldRefreshForVisibilityState(state: string): boolean {
  return state === 'visible';
}

export function shouldPollWhenHidden(hidden: boolean): boolean {
  return !hidden;
}
