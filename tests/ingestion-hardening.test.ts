/**
 * Tests for hardened framework ingestion compliance with INTERFACE.md
 */

import { loadFrameworkRun } from '../lib/framework/ingest';
import { validateRunId } from '../lib/utils/validation';
import { normalizeMatrixCells, validateRawCell } from '../lib/framework/normalizeMatrix';

describe('Framework Ingestion Hardening', () => {
  describe('Run ID Validation', () => {
    it('should validate correct run_id patterns', () => {
      const validIds = [
        'sample-happy-001',
        'test_run_123',
        'abc123def',
        'run-with-dashes',
        'run_with_underscores',
        'a',  // minimum length
        'a'.repeat(64)  // maximum length
      ];
      
      validIds.forEach(id => {
        const result = validateRunId(id);
        expect(result.valid).toBe(true);
        expect(result.error).toBeUndefined();
      });
    });
    
    it('should reject invalid run_id patterns', () => {
      const invalidIds = [
        '',  // empty
        'a'.repeat(65),  // too long
        'UPPERCASE',  // uppercase
        'with spaces',  // spaces
        'with/slash',  // slash
        'with\\backslash',  // backslash
        'with..dots',  // double dots
        'with@symbol',  // invalid characters
        '../traversal'  // path traversal attempt
      ];
      
      invalidIds.forEach(id => {
        const result = validateRunId(id);
        expect(result.valid).toBe(false);
        expect(result.error).toBeDefined();
      });
    });
  });
  
  describe('Matrix Normalization', () => {
    it('should normalize cells with missing coordinates', () => {
      const rawCells = [
        {
          id: 'C:row1:col1',
          matrix: 'C' as const,
          row_label: '  Normative  ',  // whitespace
          col_label: 'Completeness',
          station: 'Requirements',
          text: '  Define criteria  ',  // whitespace
          citations: ['  CIT:doc#p1  '],  // whitespace in array
          refs: [],
          meta: { order: 1 }
        },
        {
          id: 'C:row2:col1', 
          matrix: 'C' as const,
          row_label: 'Operative',
          col_label: 'Completeness',
          station: 'Requirements',
          text: 'Ensure coverage',
          citations: [],
          refs: [],
          meta: { order: 2 }
        }
      ];
      
      const result = normalizeMatrixCells(rawCells, 'C');
      
      expect(result.cells).toHaveLength(2);
      expect(result.metrics.totalCells).toBe(2);
      expect(result.metrics.normalizedCoordinates).toBe(2);
      
      // Check normalization
      expect(result.cells[0].row_label).toBe('Normative');  // trimmed
      expect(result.cells[0].text).toBe('Define criteria');  // trimmed
      expect(result.cells[0].citations[0]).toBe('CIT:doc#p1');  // trimmed
      
      // Check coordinate assignment (1-based)
      expect(result.cells[0].row).toBe(1);  // Normative = first label = 1
      expect(result.cells[0].col).toBe(1);  // Completeness = first label = 1
      expect(result.cells[1].row).toBe(2);  // Operative = second label = 2
      expect(result.cells[1].col).toBe(1);  // Same column
    });
    
    it('should validate producer coordinates when provided', () => {
      const rawCells = [
        {
          id: 'C:test',
          matrix: 'C' as const,
          row: 5,  // Producer coordinate
          col: 3,  // Producer coordinate
          row_label: 'TestRow',
          col_label: 'TestCol',
          station: 'Test',
          text: 'Test content',
          citations: [],
          refs: []
        }
      ];
      
      const result = normalizeMatrixCells(rawCells, 'C');
      
      // Should warn about mismatch (derived would be 1,1 but producer says 5,3)
      expect(result.metrics.warnings).toHaveLength(1);
      expect(result.metrics.warnings[0]).toContain('Producer coordinates');
      
      // Should use derived coordinates despite producer mismatch
      expect(result.cells[0].row).toBe(1);
      expect(result.cells[0].col).toBe(1);
    });
    
    it('should enforce stable ordering', () => {
      const rawCells = [
        { id: 'C:z', matrix: 'C' as const, row_label: 'A', col_label: 'A', station: 'S', text: 'Z', citations: [], refs: [], meta: { order: 2 } },
        { id: 'C:a', matrix: 'C' as const, row_label: 'A', col_label: 'A', station: 'S', text: 'A', citations: [], refs: [], meta: { order: 1 } },
        { id: 'C:m2', matrix: 'C' as const, row_label: 'A', col_label: 'A', station: 'S', text: 'M2', citations: [], refs: [] },
        { id: 'C:m1', matrix: 'C' as const, row_label: 'A', col_label: 'A', station: 'S', text: 'M1', citations: [], refs: [] }
      ];
      
      const result = normalizeMatrixCells(rawCells, 'C');
      
      // Should be ordered by meta.order first, then by id
      expect(result.cells[0].id).toBe('C:a');   // order: 1
      expect(result.cells[1].id).toBe('C:z');   // order: 2
      expect(result.cells[2].id).toBe('C:m1');  // no order, id comes first
      expect(result.cells[3].id).toBe('C:m2');  // no order, id comes second
    });
  });
  
  describe('Framework Ingestion', () => {
    it('should load and normalize sample_happy_001 fixture', async () => {
      const result = await loadFrameworkRun('sample_happy_001', {
        runsDir: 'fixtures/runs',
        verifyChecksums: false
      });
      
      expect(result.manifest.run_id).toBe('sample_happy_001');
      expect(result.manifest.framework_schema_version).toBe('1.0.0');
      
      expect(result.matrices.C).toBeDefined();
      expect(result.matrices.D).toBeDefined();
      expect(result.matrices.X).toBeDefined();
      expect(result.matrices.E).toBeDefined();
      
      // All cells should now have numeric coordinates
      Object.values(result.matrices).forEach(matrix => {
        matrix.forEach(cell => {
          expect(cell.row).toBeDefined();
          expect(typeof cell.row).toBe('number');
          expect(cell.col).toBeDefined();
          expect(typeof cell.col).toBe('number');
          expect(cell.row).toBeGreaterThan(0);  // 1-based
          expect(cell.col).toBeGreaterThan(0);  // 1-based
        });
      });
    });
    
    it('should reject invalid run_id during ingestion', async () => {
      await expect(
        loadFrameworkRun('invalid/run/id', {
          runsDir: 'fixtures/runs',
          verifyChecksums: false
        })
      ).rejects.toThrow('Invalid run_id');
    });
    
    it('should validate MatrixCellRaw structure', () => {
      const validCell = {
        id: 'test',
        matrix: 'C',
        row_label: 'Test',
        col_label: 'Test',
        station: 'Test',
        text: 'Test content',
        citations: [],
        refs: []
      };
      
      expect(() => validateRawCell(validCell, 1)).not.toThrow();
      
      // Test missing required fields
      const invalidCell = { ...validCell };
      delete (invalidCell as any).text;
      
      expect(() => validateRawCell(invalidCell, 1)).toThrow('must be a string');
    });
  });
});