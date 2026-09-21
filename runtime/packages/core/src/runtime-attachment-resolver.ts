import { constants } from "node:fs";
import { open } from "node:fs/promises";
import { join } from "node:path";
import { RuntimeError, type IAttachmentResolver, type ResolvedAttachments } from "@chirality/runtime-contracts";
import { assertSafeIdentifier } from "./fs.js";
import { assertAttachmentCount, assertAttachmentSourcePath, captureAttachmentDirectory, ensureAttachmentDirectory, readAttachmentBytes, writeAttachmentCopy } from "./attachment-copy.js";

/** Stages explicitly selected files into immutable, project-contained conversation custody. */
export class RuntimeAttachmentResolver implements IAttachmentResolver {
  async resolveAttachmentsToContentBlocks(
    message: string,
    attachmentPaths: string[],
    context?: { projectId: string; sessionId: string; projectRoot: string }
  ): Promise<ResolvedAttachments> {
    if (!context) throw new RuntimeError("INVALID_REQUEST", "Hosted attachment staging requires project and session context");
    assertSafeIdentifier(context.projectId, "projectId"); assertSafeIdentifier(context.sessionId, "sessionId");
    // Reject all external raw inputs before any source metadata or bytes are read.
    assertAttachmentCount(attachmentPaths);
    for (const source of attachmentPaths) assertAttachmentSourcePath(source, context.projectRoot);
    const rootGuard = await captureAttachmentDirectory(context.projectRoot);
    const contentBlocks: ResolvedAttachments["contentBlocks"] = message.trim() ? [{ type: "text", text: message }] : [];
    const guards = [rootGuard];
    const revalidateStaging = async () => { for (const guard of guards) await guard(); };
    const chiralityDirectory = join(context.projectRoot, ".chirality");
    const attachmentDirectory = join(chiralityDirectory, "attachments");
    const sessionDirectory = join(attachmentDirectory, context.sessionId);
    for (const directory of [chiralityDirectory, attachmentDirectory, sessionDirectory]) {
      await revalidateStaging();
      guards.push(await ensureAttachmentDirectory(directory));
    }
    const budget = { bytes: 0 };
    for (const sourcePath of attachmentPaths) {
      await revalidateStaging();
      const attachment = await readAttachmentBytes(sourcePath, budget);
      const { sha256, bytes, mimeType, name } = attachment;
      const stagedName = `${sha256}${attachment.extension}`;
      const stagedPath = await writeAttachmentCopy(sessionDirectory, stagedName, attachment, revalidateStaging);
      const historyPath = join(sessionDirectory, "history.jsonl");
      await revalidateStaging();
      const history = await open(historyPath, constants.O_CREAT | constants.O_APPEND | constants.O_WRONLY | (constants.O_NOFOLLOW ?? 0), 0o600).catch(() => undefined);
      if (!history) throw new RuntimeError("FORBIDDEN", "Attachment history path is unsafe", 403);
      try {
        if (!(await history.stat()).isFile()) throw new RuntimeError("FORBIDDEN", "Attachment history path is unsafe", 403);
        await history.appendFile(`${JSON.stringify({ stagedName, name, sha256, bytes: bytes.byteLength, mimeType, recordedAt: new Date().toISOString() })}\n`, "utf8");
        await history.sync();
      } finally { await history.close(); }
      contentBlocks.push({ type: "file", path: stagedPath, mimeType, name, sha256, bytes: bytes.byteLength });
    }
    return { contentBlocks, errors: [] };
  }
}
