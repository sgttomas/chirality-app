import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  createRefreshScheduler,
  shouldPollWhenHidden,
  shouldRefreshForVisibilityState
} from '../../lib/workspace/file-tree-refresh';

describe('workspace file-tree refresh helpers', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.useRealTimers();
  });

  it('debounces repeated schedule calls to a single refresh', () => {
    const onRefresh = vi.fn();
    const onAfterRefresh = vi.fn();
    const scheduler = createRefreshScheduler({
      debounceMs: 200,
      onRefresh,
      onAfterRefresh
    });

    scheduler.schedule();
    scheduler.schedule();
    scheduler.schedule();

    vi.advanceTimersByTime(199);
    expect(onRefresh).not.toHaveBeenCalled();
    expect(onAfterRefresh).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);
    expect(onRefresh).toHaveBeenCalledTimes(1);
    expect(onAfterRefresh).toHaveBeenCalledTimes(1);
  });

  it('cancels pending refresh callbacks', () => {
    const onRefresh = vi.fn();
    const scheduler = createRefreshScheduler({
      debounceMs: 150,
      onRefresh
    });

    scheduler.schedule();
    scheduler.cancel();
    vi.advanceTimersByTime(200);

    expect(onRefresh).not.toHaveBeenCalled();
  });

  it('treats only visible state as a refresh signal', () => {
    expect(shouldRefreshForVisibilityState('visible')).toBe(true);
    expect(shouldRefreshForVisibilityState('hidden')).toBe(false);
    expect(shouldRefreshForVisibilityState('prerender')).toBe(false);
  });

  it('skips polling while the window is hidden', () => {
    expect(shouldPollWhenHidden(true)).toBe(false);
    expect(shouldPollWhenHidden(false)).toBe(true);
  });
});
