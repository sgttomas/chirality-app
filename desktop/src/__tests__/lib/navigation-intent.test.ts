import { describe, expect, it, vi } from 'vitest';
import { createNavigationIntentScheduler } from '../../lib/workspace/navigation-intent';

async function flushMicrotaskQueue(): Promise<void> {
  await Promise.resolve();
}

describe('navigation intent scheduler', () => {
  it('coalesces same-turn requests and navigates only the latest target', async () => {
    const onNavigate = vi.fn();
    const scheduler = createNavigationIntentScheduler({ onNavigate });

    scheduler.schedule('/pipeline?scopeKey=first');
    scheduler.schedule('/pipeline?scopeKey=second');
    scheduler.schedule('/pipeline?scopeKey=third');

    expect(onNavigate).not.toHaveBeenCalled();
    await flushMicrotaskQueue();

    expect(onNavigate).toHaveBeenCalledTimes(1);
    expect(onNavigate).toHaveBeenCalledWith('/pipeline?scopeKey=third');
  });

  it('navigates once per turn when requests are separated across turns', async () => {
    const onNavigate = vi.fn();
    const scheduler = createNavigationIntentScheduler({ onNavigate });

    scheduler.schedule('/workbench?agent=HELP');
    await flushMicrotaskQueue();

    scheduler.schedule('/workbench?agent=CHANGE');
    await flushMicrotaskQueue();

    expect(onNavigate).toHaveBeenCalledTimes(2);
    expect(onNavigate).toHaveBeenNthCalledWith(1, '/workbench?agent=HELP');
    expect(onNavigate).toHaveBeenNthCalledWith(2, '/workbench?agent=CHANGE');
  });

  it('drops pending navigation after cancel and still allows future scheduling', async () => {
    const onNavigate = vi.fn();
    const scheduler = createNavigationIntentScheduler({ onNavigate });

    scheduler.schedule('/pipeline?category=TASK');
    scheduler.cancel();
    await flushMicrotaskQueue();

    expect(onNavigate).not.toHaveBeenCalled();

    scheduler.schedule('/pipeline?category=AUDIT');
    await flushMicrotaskQueue();

    expect(onNavigate).toHaveBeenCalledTimes(1);
    expect(onNavigate).toHaveBeenCalledWith('/pipeline?category=AUDIT');
  });
});
