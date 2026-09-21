/**
 * Shared IPC sender-authorization policy for privileged main-process handlers.
 *
 * One policy, used by both the runtime-control channels and the credential
 * channels (DEL-09-06-V3-01): an `ipcMain.handle` invocation is honoured only
 * when the sending frame's URL has exactly the renderer origin the main process
 * created the window for. Anything else — no sender frame, an unparseable URL,
 * a different scheme, host, or port — fails closed.
 *
 * The structural event type keeps the policy testable without an Electron
 * runtime; `IpcMainInvokeEvent` satisfies it directly.
 */

export type IpcSenderEvent = {
  senderFrame?: { url?: string } | null;
};

export function isAuthorizedSender(event: IpcSenderEvent, rendererOrigin: string): boolean {
  const senderUrl = event.senderFrame?.url;
  if (!senderUrl) return false;
  try {
    return new URL(senderUrl).origin === rendererOrigin;
  } catch {
    return false;
  }
}

/**
 * Non-secret description of a sender for diagnostics: the origin only, never
 * the full URL (a path or query string is not something a log should retain).
 */
export function describeIpcSender(event: IpcSenderEvent): string {
  const senderUrl = event.senderFrame?.url;
  if (!senderUrl) return 'no-sender-frame';
  try {
    return new URL(senderUrl).origin;
  } catch {
    return 'unparseable-sender-url';
  }
}
