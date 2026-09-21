export type RuntimeShutdownState = {
  shutdownStarted: boolean;
  shutdownCompleted: boolean;
  hasOwnedResources: boolean;
};

/**
 * Keep native quit requests from bypassing teardown, while allowing the
 * process's owned exit once teardown has settled.
 */
export function shouldPreventNativeQuit(state: RuntimeShutdownState): boolean {
  return !state.shutdownCompleted && (state.shutdownStarted || state.hasOwnedResources);
}
