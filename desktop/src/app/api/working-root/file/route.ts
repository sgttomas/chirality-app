import path from 'node:path';
import { NextResponse } from 'next/server';
import { assertProjectRootAccessible } from '../../../../lib/harness/session-manager';
import { resolveInstructionRootPath } from '../../../../lib/harness/instruction-root';
import { assertOpenDocumentUnchanged, createCloseOnce, fileError, openDocument, TEXT_LIMIT, FilePolicyError } from './file-policy';
import { createEligiblePdfResponseHeaders } from '../../../../../electron/renderer-window-policy';

export const runtime = 'nodejs';
const TEXT = new Set(['.md', '.markdown', '.txt', '.log', '.csv', '.json', '.yaml', '.yml', '.toml', '.js', '.jsx', '.ts', '.tsx', '.py', '.css', '.html', '.xml', '.sh', '.sql', '.rs', '.go', '.c', '.h', '.cpp', '.java', '.ini', '.cfg']);
const IMAGE_LIMIT = 2 * 1024 * 1024; // Bounded image input default; the text limit is separately owner-ruled.
const IMAGE_MIME: Record<string, string> = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml' };
const OFFICE = new Set(['.docx', '.xlsx', '.pptx']);
export async function GET(request: Request): Promise<Response> {
  let document: Awaited<ReturnType<typeof openDocument>> | undefined;
  try {
    const url = new URL(request.url);
    const allowedSelectors = new Set(['projectRoot', 'path', 'target', 'content']);
    if ([...url.searchParams.keys()].some(key => !allowedSelectors.has(key)) ||
        url.searchParams.getAll('projectRoot').length !== 1 ||
        url.searchParams.getAll('content').length > 1 ||
        url.searchParams.getAll('path').length > 1 || url.searchParams.getAll('target').length > 1 ||
        (url.searchParams.has('path') === url.searchParams.has('target'))) {
      throw new FilePolicyError('INVALID_REQUEST', 400, 'Expected one root, one file selector, and no duplicate or unknown selectors.');
    }
    if (url.searchParams.has('content') && !['pdf', 'image'].includes(url.searchParams.get('content') ?? '')) {
      throw new FilePolicyError('INVALID_REQUEST', 400, 'Unknown content selector.');
    }
    const projectRoot = await assertProjectRootAccessible(url.searchParams.get('projectRoot') ?? '');
    const targetPath = url.searchParams.get('path') ?? url.searchParams.get('target');
    document = await openDocument({ projectRoot, target: targetPath }, resolveInstructionRootPath());
    const { handle, info, target } = document;
    const extension = path.extname(target).toLowerCase();
    const kind = extension === '.pdf' ? 'pdf' : OFFICE.has(extension) ? 'office' : Object.hasOwn(IMAGE_MIME, extension) ? 'image' : TEXT.has(extension) || !extension ? 'text' : 'unsupported';
    const mimeType = kind === 'image' ? IMAGE_MIME[extension] : kind === 'pdf' ? 'application/pdf' : extension === '.csv' ? 'text/csv' : extension === '.md' || extension === '.markdown' ? 'text/markdown' : kind === 'text' ? 'text/plain' : 'application/octet-stream';
    const metadata = { path: target, mtime: info.mtime.toISOString(), mimeType, target, name: path.basename(target), size: info.size, modifiedAt: info.mtime.toISOString(), kind, tooLarge: (kind === 'text' && info.size > TEXT_LIMIT) || (kind === 'image' && info.size > IMAGE_LIMIT) };
    const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
    const binary = url.searchParams.get('content');
    if (binary === 'pdf' || binary === 'image') {
      if (kind !== binary) throw new FilePolicyError('UNSUPPORTED_FORMAT', 415, 'The file does not match the requested preview format.');
      if (binary === 'image' && metadata.tooLarge) throw new FilePolicyError('IMAGE_LIMIT_EXCEEDED', 413, 'Image exceeds the 2 MB preview limit.');
      if (binary === 'pdf') {
        if (info.size <= 0) throw new FilePolicyError('INVALID_PDF', 415, 'PDF preview requires a non-empty PDF file.');
        const signature = Buffer.alloc(5);
        const first = await handle.read(signature, 0, signature.length, 0);
        if (first.bytesRead !== 5 || signature.toString('ascii') !== '%PDF-') {
          throw new FilePolicyError('INVALID_PDF', 415, 'PDF preview requires a PDF signature.');
        }
        await assertOpenDocumentUnchanged(handle, info, 'File changed before reading. Retry the preview.');
      }
      // Descriptor reads are chunked and bounded to the observed size. A changed/truncated
      // resource errors the stream, rather than silently completing a mismatched response.
      let offset = 0;
      const close = createCloseOnce(() => handle.close());
      const stream = new ReadableStream<Uint8Array>({
        async pull(controller) {
          try {
            await assertOpenDocumentUnchanged(handle, info);
            if (offset === info.size) {
              await close(); controller.close(); return;
            }
            const chunk = Buffer.alloc(Math.min(64 * 1024, info.size - offset));
            const { bytesRead } = await handle.read(chunk, 0, chunk.length, offset);
            if (!bytesRead) throw new FilePolicyError('FILE_CHANGED', 409, 'File was truncated while reading.');
            offset += bytesRead; controller.enqueue(chunk.subarray(0, bytesRead));
          } catch (error) { await close(); controller.error(error); }
        },
        cancel: close
      });
      document = undefined;
      const imageName = encodeURIComponent(path.basename(target)).replace(/[!'()*]/g, character => `%${character.charCodeAt(0).toString(16).toUpperCase()}`);
      return new Response(stream, { status: 200, headers: binary === 'pdf' ? createEligiblePdfResponseHeaders(info.size) : {
        ...headers, 'Content-Type': mimeType, 'Content-Length': String(info.size),
        'Content-Disposition': `attachment; filename*=UTF-8''${imageName}`
      } });
    }
    if (kind !== 'text' || metadata.tooLarge) return NextResponse.json({ ...metadata, content: null, reason: metadata.tooLarge ? kind === 'image' ? 'IMAGE_LIMIT_EXCEEDED' : 'TEXT_LIMIT_EXCEEDED' : kind === 'office' ? 'NATIVE_PREVIEW' : kind === 'pdf' ? 'PDF_VIEWER' : kind === 'image' ? 'IMAGE_VIEWER' : 'UNSUPPORTED_FORMAT' }, { headers });
    const buffer = Buffer.alloc(Math.min(info.size + 1, TEXT_LIMIT + 1));
    let offset = 0;
    while (offset < buffer.length) {
      const read = await handle.read(buffer, offset, buffer.length - offset, offset);
      if (!read.bytesRead) break;
      offset += read.bytesRead;
    }
    const after = await handle.stat();
    if (offset > TEXT_LIMIT || after.size !== info.size || after.mtimeMs !== info.mtimeMs) throw new FilePolicyError('FILE_CHANGED', 409, 'File changed while reading. Retry the preview.');
    if (buffer.subarray(0, offset).includes(0)) return NextResponse.json({ ...metadata, kind: 'unsupported' }, { headers });
    return NextResponse.json({ ...metadata, content: buffer.subarray(0, offset).toString('utf8') }, { headers });
  } catch (error) {
    // The existing root policy has its own truthful typed errors.
    const typed = error as { status?: number; code?: string; type?: string; message?: string };
    const errorCode = typed?.code ?? typed?.type;
    const result = typeof typed?.status === 'number' && typeof errorCode === 'string'
      ? { status: typed.status, body: { error: { code: errorCode, message: typed.message } } } : fileError(error);
    return NextResponse.json(result.body, { status: result.status, headers: { 'Cache-Control': 'no-store' } });
  } finally { await document?.handle.close(); }
}
