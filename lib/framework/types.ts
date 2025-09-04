/**
 * Framework integration types and normalization contracts
 */

export type MatrixKind = 'C' | 'D' | 'X' | 'E';

/**
 * Raw MatrixCell as produced by chirality-framework
 * This reflects what actually comes from the JSONL files
 */
export interface MatrixCellRaw {
  id: string;
  matrix: MatrixKind;
  row_label: string;
  col_label: string;
  station: string;
  text: string;
  citations: string[];
  refs: string[];
  meta?: { order?: number; [k: string]: unknown };
  // Note: row and col numeric fields may be missing from framework output
  row?: number;
  col?: number;
}

/**
 * Normalized MatrixCell with guaranteed numeric coordinates
 * This is what the pipeline expects after normalization
 */
export interface MatrixCell {
  id: string;
  matrix: MatrixKind;
  row: number;          // Normalized numeric coordinate
  col: number;          // Normalized numeric coordinate  
  row_label: string;
  col_label: string;
  station: string;
  text: string;
  citations: string[];
  refs: string[];
  meta?: { order?: number; [k: string]: unknown };
}

/**
 * Normalization result with metrics
 */
export interface NormalizationResult {
  cells: MatrixCell[];
  metrics: {
    totalCells: number;
    normalizedCoordinates: number;
    warnings: string[];
  };
}