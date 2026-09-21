const PIPELINE_QUERY_KEYS = ['category', 'taskScopeMode', 'scopeKey', 'targetDeliverableKey'];

type SearchParamSource = string | URLSearchParams | { toString: () => string };

/**
 * Fold a matrix target into the mounted loop shell route. This preserves the
 * active surface while still carrying persona or Pipeline intent through query
 * params.
 */
export function mergeMatrixTargetIntoCurrentUrl(
  target: string,
  pathname: string,
  currentSearchParams: SearchParamSource
): string {
  try {
    const targetUrl = new URL(target, 'http://chirality.local');
    const nextParams = new URLSearchParams(currentSearchParams.toString());

    if (targetUrl.pathname === '/pipeline') {
      for (const key of PIPELINE_QUERY_KEYS) {
        nextParams.delete(key);
      }
    }

    targetUrl.searchParams.forEach((value, key) => {
      nextParams.set(key, value);
    });

    const nextQuery = nextParams.toString();
    return nextQuery ? `${pathname}?${nextQuery}` : pathname;
  } catch {
    return target;
  }
}
