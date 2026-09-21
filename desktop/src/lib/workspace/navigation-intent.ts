export type NavigationIntentScheduler = {
  schedule: (target: string) => void;
  cancel: () => void;
};

type NavigationIntentSchedulerOptions = {
  onNavigate: (target: string) => void;
};

export function createNavigationIntentScheduler(
  options: NavigationIntentSchedulerOptions
): NavigationIntentScheduler {
  let pendingTarget: string | null = null;
  let flushScheduled = false;
  let cancelGeneration = 0;
  let pendingGeneration = 0;

  const cancel = (): void => {
    pendingTarget = null;
    cancelGeneration += 1;
  };

  const schedule = (target: string): void => {
    const normalizedTarget = target.trim();
    if (!normalizedTarget) {
      return;
    }

    pendingTarget = normalizedTarget;
    pendingGeneration = cancelGeneration;

    if (flushScheduled) {
      return;
    }

    flushScheduled = true;
    queueMicrotask(() => {
      flushScheduled = false;
      if (pendingGeneration !== cancelGeneration) {
        return;
      }

      const targetToNavigate = pendingTarget;
      pendingTarget = null;
      if (!targetToNavigate) {
        return;
      }

      options.onNavigate(targetToNavigate);
    });
  };

  return { schedule, cancel };
}
