function isRowEmpty(row: string[]): boolean {
  return row.every((value) => value.trim() === '');
}

export function parseCsv(content: string): string[][] {
  const rows: string[][] = [];
  let currentRow: string[] = [];
  let field = '';
  let inQuotes = false;

  for (let index = 0; index < content.length; index += 1) {
    const char = content[index];

    if (inQuotes) {
      if (char === '"') {
        const nextChar = content[index + 1];
        if (nextChar === '"') {
          field += '"';
          index += 1;
          continue;
        }
        inQuotes = false;
        continue;
      }

      field += char;
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      continue;
    }

    if (char === ',') {
      currentRow.push(field);
      field = '';
      continue;
    }

    if (char === '\n') {
      currentRow.push(field);
      if (!isRowEmpty(currentRow)) {
        rows.push(currentRow);
      }
      currentRow = [];
      field = '';
      continue;
    }

    if (char === '\r') {
      continue;
    }

    field += char;
  }

  currentRow.push(field);
  if (!isRowEmpty(currentRow)) {
    rows.push(currentRow);
  }

  return rows;
}

function escapeCsvCell(value: string): string {
  const needsQuotes = /[",\n\r]/.test(value);
  if (!needsQuotes) {
    return value;
  }

  return `"${value.replace(/"/g, '""')}"`;
}

export function serializeCsv(headers: string[], rows: Record<string, string>[]): string {
  const lines: string[] = [];
  lines.push(headers.join(','));

  for (const row of rows) {
    const cells = headers.map((header) => escapeCsvCell(row[header] ?? ''));
    lines.push(cells.join(','));
  }

  return `${lines.join('\n')}\n`;
}
