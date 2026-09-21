/**
 * Renderer-side accessor for the desktop attachment picker exposed by the
 * preload bridge. Paths it returns are canonical, absolute, inside
 * `projectRoot`, and limited to supported extensions; the main process owns
 * that policy. Absent bridge (web build) means the in-app picker is used.
 */
export type NativeAttachmentSelection =
  | { cancelled: true; error?: string }
  | { cancelled: false; paths: string[] };

export type NativeAttachmentBridge = {
  selectFiles: (input: { projectRoot: string }) => Promise<NativeAttachmentSelection>;
};

export function getNativeAttachmentBridge(): NativeAttachmentBridge | undefined {
  if (typeof window === 'undefined') return undefined;
  const bridge = (window as unknown as { chirality?: { attachments?: Partial<NativeAttachmentBridge> } }).chirality?.attachments;
  return typeof bridge?.selectFiles === 'function' ? { selectFiles: bridge.selectFiles } : undefined;
}
