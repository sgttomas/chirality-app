import { randomUUID } from 'node:crypto';
import { rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';

export type AtomicTextWriteResult = {
  strategy: 'same-directory-rename';
  tempFilePath: string;
};

export async function writeTextFileAtomically(
  filePath: string,
  content: string
): Promise<AtomicTextWriteResult> {
  const directory = path.dirname(filePath);
  const baseName = path.basename(filePath);
  const tempFilePath = path.join(
    directory,
    `.${baseName}.${Date.now()}.${randomUUID()}.tmp`
  );
  let renamed = false;

  try {
    await writeFile(tempFilePath, content, 'utf8');
    await rename(tempFilePath, filePath);
    renamed = true;
    return {
      strategy: 'same-directory-rename',
      tempFilePath
    };
  } finally {
    if (!renamed) {
      await rm(tempFilePath, { force: true });
    }
  }
}
