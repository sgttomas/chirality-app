/**
 * Matrix normalization utilities for framework ingestion
 * 
 * Handles inconsistencies between framework output and pipeline requirements
 */

import { MatrixCellRaw, MatrixCell, NormalizationResult } from './types';

/**
 * Normalize raw matrix cells to ensure consistent coordinate system
 * 
 * Normalization rules:
 * - Trim whitespace from all string fields
 * - Case-sensitive label matching 
 * - 1-based indexing for coordinates
 * - Per-file enumeration for missing coordinates
 * - Validate producer coordinates if present and warn on mismatch
 */
export function normalizeMatrixCells(
  rawCells: MatrixCellRaw[], 
  matrixKind: string
): NormalizationResult {
  const warnings: string[] = [];
  let normalizedCoordinates = 0;
  
  // Step 1: Build label-to-coordinate mappings
  const rowLabels = new Set<string>();
  const colLabels = new Set<string>();
  
  // First pass: collect all unique labels
  rawCells.forEach(cell => {
    rowLabels.add(cell.row_label.trim());
    colLabels.add(cell.col_label.trim());
  });
  
  // Create sorted arrays for consistent 1-based indexing
  const sortedRowLabels = Array.from(rowLabels).sort();
  const sortedColLabels = Array.from(colLabels).sort();
  
  // Step 2: Normalize each cell
  const normalizedCells: MatrixCell[] = rawCells.map((rawCell, index) => {
    // Trim whitespace from text fields
    const trimmedRowLabel = rawCell.row_label.trim();
    const trimmedColLabel = rawCell.col_label.trim();
    const trimmedText = rawCell.text.trim();
    const trimmedId = rawCell.id.trim();
    const trimmedStation = rawCell.station.trim();
    
    // Derive coordinates from labels (1-based)
    const derivedRow = sortedRowLabels.indexOf(trimmedRowLabel) + 1;
    const derivedCol = sortedColLabels.indexOf(trimmedColLabel) + 1;
    
    // Use producer coordinates if provided, otherwise use derived
    let finalRow = derivedRow;
    let finalCol = derivedCol;
    
    if (rawCell.row !== undefined && rawCell.col !== undefined) {
      // Validate producer coordinates
      if (rawCell.row !== derivedRow || rawCell.col !== derivedCol) {
        warnings.push(
          `${matrixKind} cell ${index + 1}: Producer coordinates (${rawCell.row}, ${rawCell.col}) ` +
          `don't match derived coordinates (${derivedRow}, ${derivedCol}) for labels ` +
          `"${trimmedRowLabel}" × "${trimmedColLabel}". Using derived coordinates.`
        );
      } else {
        // Producer coordinates match - use them
        finalRow = rawCell.row;
        finalCol = rawCell.col;
      }
    } else {
      // Missing producer coordinates - use derived
      normalizedCoordinates++;
    }
    
    // Trim citations and refs arrays
    const trimmedCitations = rawCell.citations.map(c => c.trim()).filter(Boolean);
    const trimmedRefs = rawCell.refs.map(r => r.trim()).filter(Boolean);
    
    return {
      id: trimmedId,
      matrix: rawCell.matrix,
      row: finalRow,
      col: finalCol,
      row_label: trimmedRowLabel,
      col_label: trimmedColLabel,
      station: trimmedStation,
      text: trimmedText,
      citations: trimmedCitations,
      refs: trimmedRefs,
      meta: rawCell.meta
    };
  });
  
  // Step 3: Apply stable ordering (meta.order then id)
  normalizedCells.sort((a, b) => {
    // First, sort by meta.order if present
    const orderA = a.meta?.order ?? Number.MAX_SAFE_INTEGER;
    const orderB = b.meta?.order ?? Number.MAX_SAFE_INTEGER;
    
    if (orderA !== orderB) {
      return orderA - orderB;
    }
    
    // Then by id (lexicographic)
    return a.id.localeCompare(b.id);
  });
  
  return {
    cells: normalizedCells,
    metrics: {
      totalCells: rawCells.length,
      normalizedCoordinates,
      warnings
    }
  };
}

/**
 * Validate that a raw cell has the minimum required structure
 */
export function validateRawCell(cell: any, lineNumber: number): cell is MatrixCellRaw {
  const requiredStringFields = ['id', 'matrix', 'row_label', 'col_label', 'station', 'text'];
  const requiredArrayFields = ['citations', 'refs'];
  
  for (const field of requiredStringFields) {
    if (typeof cell[field] !== 'string') {
      throw new Error(
        `Line ${lineNumber}: Field '${field}' must be a string, got ${typeof cell[field]}`
      );
    }
  }
  
  for (const field of requiredArrayFields) {
    if (!Array.isArray(cell[field])) {
      throw new Error(
        `Line ${lineNumber}: Field '${field}' must be an array, got ${typeof cell[field]}`
      );
    }
  }
  
  // Validate matrix kind
  if (!['C', 'D', 'X', 'E'].includes(cell.matrix)) {
    throw new Error(
      `Line ${lineNumber}: Invalid matrix kind '${cell.matrix}', must be C, D, X, or E`
    );
  }
  
  // If row/col are provided, they must be numbers
  if (cell.row !== undefined && typeof cell.row !== 'number') {
    throw new Error(
      `Line ${lineNumber}: Field 'row' must be a number if provided, got ${typeof cell.row}`
    );
  }
  
  if (cell.col !== undefined && typeof cell.col !== 'number') {
    throw new Error(
      `Line ${lineNumber}: Field 'col' must be a number if provided, got ${typeof cell.col}`
    );
  }
  
  return true;
}