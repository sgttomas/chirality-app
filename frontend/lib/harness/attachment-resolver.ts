import { promises as fs } from "node:fs";
import path from "node:path";
import type { Attachment, AttachmentType } from "./types";

type TextBlock = { type: "text"; text: string };
type ImageBlock = { type: "image"; source: { type: "base64"; media_type: string; data: string } };
type DocumentBlock = { type: "document"; source: { type: "base64"; media_type: string; data: string } };
export type ContentBlock = TextBlock | ImageBlock | DocumentBlock;

const MAX_PER_FILE = 10 * 1024 * 1024; // 10 MB per file
const MAX_TOTAL = 18 * 1024 * 1024; // 18 MB raw → ~24MB base64+JSON (stays under API limits)

const MIME_MAP: Record<string, { mime: string; type: AttachmentType }> = {
  ".png": { mime: "image/png", type: "image" },
  ".jpg": { mime: "image/jpeg", type: "image" },
  ".jpeg": { mime: "image/jpeg", type: "image" },
  ".gif": { mime: "image/gif", type: "image" },
  ".webp": { mime: "image/webp", type: "image" },
  ".pdf": { mime: "application/pdf", type: "document" },
  ".txt": { mime: "text/plain", type: "text" },
  ".md": { mime: "text/markdown", type: "text" },
  ".csv": { mime: "text/csv", type: "text" },
};

/** Server-side classification from path. Uses path.extname() for cross-platform safety. */
export function classifyFile(filePath: string): Attachment | null {
  const ext = path.extname(filePath).toLowerCase();
  const entry = MIME_MAP[ext];
  if (!entry) return null;
  return { path: filePath, name: path.basename(filePath), mimeType: entry.mime, type: entry.type };
}

export interface ResolveResult {
  blocks: ContentBlock[];
  errors: string[];
}

/** Async file reading with per-file and total budget enforcement. */
export async function resolveAttachmentsToContentBlocks(
  textMessage: string,
  attachmentPaths: string[],
): Promise<ResolveResult> {
  const blocks: ContentBlock[] = [];
  const errors: string[] = [];
  let totalBytes = 0;

  for (const filePath of attachmentPaths) {
    const att = classifyFile(filePath);
    if (!att) {
      errors.push(`Unsupported file type: ${filePath}`);
      continue;
    }

    let stats;
    try {
      stats = await fs.stat(filePath);
    } catch {
      errors.push(`File not found: ${filePath}`);
      continue;
    }
    if (!stats.isFile()) {
      errors.push(`Not a regular file: ${filePath}`);
      continue;
    }

    if (stats.size > MAX_PER_FILE) {
      errors.push(`File too large (${Math.round(stats.size / 1024 / 1024)}MB, max 10MB): ${att.name}`);
      continue;
    }
    if (totalBytes + stats.size > MAX_TOTAL) {
      errors.push(`Total attachment budget exceeded at: ${att.name}`);
      continue;
    }
    totalBytes += stats.size;

    try {
      if (att.type === "image") {
        const data = (await fs.readFile(filePath)).toString("base64");
        blocks.push({ type: "image", source: { type: "base64", media_type: att.mimeType, data } });
      } else if (att.type === "document") {
        const data = (await fs.readFile(filePath)).toString("base64");
        blocks.push({ type: "document", source: { type: "base64", media_type: att.mimeType, data } });
      } else {
        const content = await fs.readFile(filePath, "utf-8");
        blocks.push({ type: "text", text: `[File: ${att.name}]\n${content}` });
      }
    } catch (err) {
      errors.push(`Failed to read: ${att.name} (${err instanceof Error ? err.message : "unknown error"})`);
    }
  }

  const hasTextMessage = textMessage.trim().length > 0;

  // Surface failures whenever the turn can still proceed (resolved attachments and/or user text).
  if (errors.length > 0 && (blocks.length > 0 || hasTextMessage)) {
    blocks.unshift({ type: "text", text: `[Attachment warnings: ${errors.join("; ")}]` });
  }

  if (hasTextMessage) {
    blocks.push({ type: "text", text: textMessage });
  }

  return { blocks, errors };
}
