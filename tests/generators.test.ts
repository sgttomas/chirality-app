import { createMatrixGenerator } from '@/lib/generator';
import type { GenerationContext } from '@/lib/generator/types';
import type { MatrixCell } from '@/types/framework';

// Mock matrix data for deterministic scaffold testing
const mockMatrices: { C: MatrixCell[], D: MatrixCell[], X: MatrixCell[], E: MatrixCell[] } = {
  C: [
    {
      id: 'C:requirements:completeness:1',
      matrix: 'C',
      row: 0,
      col: 0,
      row_label: 'Requirements',
      col_label: 'Completeness', 
      station: 'Problem Requirements',
      text: 'System must handle user authentication with two-factor verification',
      citations: ['CIT:spec#p5'],
      refs: ['DS:auth'],
      meta: { order: 1 }
    }
  ],
  D: [
    {
      id: 'D:objectives:workflow:1', 
      matrix: 'D',
      row: 0,
      col: 0,
      row_label: 'Objectives',
      col_label: 'Workflow',
      station: 'Solution Objectives',
      text: 'Implement secure login flow with credential validation and session management',
      citations: ['CIT:design#p3'],
      refs: ['SP:login'],
      meta: { order: 1 }
    }
  ],
  X: [
    {
      id: 'X:verification:testing:1',
      matrix: 'X',
      row: 0,
      col: 0, 
      row_label: 'Verification',
      col_label: 'Testing',
      station: 'Verification',
      text: 'Unit tests must cover authentication edge cases and failure modes',
      citations: ['CIT:test#p2'],
      refs: ['X:test'],
      meta: { order: 1 }
    }
  ],
  E: [
    {
      id: 'E:evaluation:risk:1',
      matrix: 'E',
      row: 0,
      col: 0,
      row_label: 'Evaluation', 
      col_label: 'Risk',
      station: 'Evaluation',
      text: 'Consider brute force attack vectors and account lockout policies',
      citations: ['CIT:security#p4'],
      refs: ['M:security'],
      meta: { order: 1 }
    }
  ]
};

const mockContext: GenerationContext = {
  problem: {
    title: 'Authentication System',
    statement: 'Design a secure user authentication system',
    initialVector: ['security', 'auth', 'login']
  },
  matrices: mockMatrices,
  options: { maxItemsPerSection: 5 }
};

// NOTE: All generators now implement actual logic with deterministic scaffolding
describe('matrix generators (deterministic scaffolds)', () => {
  const generators = createMatrixGenerator();
  
  test('DS generator produces valid data sheet structure', async () => {
    // Arrange: use mockContext with C matrix
    const result = await generators.ds.generate(mockContext);
    
    // Assert: DS structure and content
    expect(result.triple.text.data_field).toBeDefined();
    expect(result.triple.text.type).toBeDefined();
    expect(result.triple.text.source_refs).toBeInstanceOf(Array);
    expect(result.triple.text.source_refs).toContain('CIT:spec#p5');
    expect(result.triple.terms_used).toBeInstanceOf(Array);
    expect(result.logs.length).toBeGreaterThan(0);
    expect(result.logs[0]).toContain('Processing 1 C matrix cells for DS generation');
  });
  
  test('SP generator produces valid procedure structure', async () => {
    // Arrange: use mockContext with D matrix
    const result = await generators.sp.generate(mockContext);
    
    // Assert: SP structure and content
    expect(result.triple.text.step).toBeDefined();
    expect(result.triple.text.purpose).toBeDefined();
    expect(result.triple.text.inputs).toBeInstanceOf(Array);
    expect(result.triple.text.outputs).toBeInstanceOf(Array);
    expect(result.triple.text.refs).toBeInstanceOf(Array);
    expect(result.triple.text.refs).toContain('CIT:design#p3');
    expect(result.logs.length).toBeGreaterThan(0);
    expect(result.logs[0]).toContain('Processing 1 D matrix cells for SP generation');
  });
  
  test('X generator produces valid solution template structure', async () => {
    // Arrange: use mockContext with X+E matrices
    const result = await generators.x.generate(mockContext);
    
    // Assert: X structure and content
    expect(result.triple.text.heading).toBeDefined();
    expect(result.triple.text.narrative).toBeDefined();
    expect(result.triple.text.refs).toBeInstanceOf(Array);
    expect(result.triple.text.refs).toContain('CIT:test#p2');
    expect(result.triple.text.refs).toContain('CIT:security#p4');
    expect(result.logs.length).toBeGreaterThan(0);
    expect(result.logs[0]).toContain('Processing 1 X matrix cells and 1 E matrix cells for X generation');
  });
  
  test('M generator produces valid guidance structure', async () => {
    // Arrange: use mockContext with E matrix
    const result = await generators.m.generate(mockContext);
    
    // Assert: M structure and content
    expect(result.triple.text.statement).toBeDefined();
    expect(result.triple.text.justification).toBeDefined();
    expect(result.triple.text.trace_back).toBeInstanceOf(Array);
    expect(result.triple.text.trace_back).toContain('CIT:security#p4');
    expect(result.triple.text.trace_back).toContain('E-matrix:E:evaluation:risk:1');
    expect(result.logs.length).toBeGreaterThan(0);
    expect(result.logs[0]).toContain('Processing 1 E matrix cells for M generation');
  });
  
  test('all generators handle empty matrices gracefully', async () => {
    // Arrange: empty matrix context
    const emptyContext: GenerationContext = {
      ...mockContext,
      matrices: { C: [], D: [], X: [], E: [] }
    };
    
    // Act & Assert: Each generator should produce minimal valid output
    const dsResult = await generators.ds.generate(emptyContext);
    expect(dsResult.triple.text.data_field).toBe('unknown');
    expect(dsResult.triple.warnings).toContain('No C matrix data available for DS generation');
    
    const spResult = await generators.sp.generate(emptyContext);
    expect(spResult.triple.text.step).toBe('unknown_procedure');
    expect(spResult.triple.warnings).toContain('No D matrix data available for SP generation');
    
    const xResult = await generators.x.generate(emptyContext);
    expect(xResult.triple.text.heading).toBe('Unknown Solution Template');
    expect(xResult.triple.warnings).toContain('No X or E matrix data available for X generation');
    
    const mResult = await generators.m.generate(emptyContext);
    expect(mResult.triple.text.statement).toBe('No strategic guidance available');
    expect(mResult.triple.warnings).toContain('No E matrix data available for M generation');
  });
  
  test('generators produce deterministic output with stable ordering', async () => {
    // Arrange: Context with multiple cells that test ordering
    const multiCellContext: GenerationContext = {
      ...mockContext,
      matrices: {
        ...mockMatrices,
        C: [
          { ...mockMatrices.C[0], id: 'C:b', meta: { order: 2 } },
          { ...mockMatrices.C[0], id: 'C:a', meta: { order: 1 } },
          { ...mockMatrices.C[0], id: 'C:c', meta: { order: 1 } } // Same order, should sort by id
        ]
      }
    };
    
    // Act: Generate twice to verify consistency
    const result1 = await generators.ds.generate(multiCellContext);
    const result2 = await generators.ds.generate(multiCellContext);
    
    // Assert: Identical output (deterministic)
    expect(result1.triple.text).toEqual(result2.triple.text);
    expect(result1.triple.terms_used).toEqual(result2.triple.terms_used);
    expect(result1.logs).toEqual(result2.logs);
  });
});

describe('generator determinism', () => {
  const generators = createMatrixGenerator();
  
  test('generators produce identical output for same input', async () => {
    // Arrange: Run multiple times with identical input
    const runs = await Promise.all([
      generators.ds.generate(mockContext),
      generators.sp.generate(mockContext),
      generators.x.generate(mockContext),
      generators.m.generate(mockContext)
    ]);
    
    // Act: Run again with same input
    const runs2 = await Promise.all([
      generators.ds.generate(mockContext),
      generators.sp.generate(mockContext),
      generators.x.generate(mockContext),
      generators.m.generate(mockContext)
    ]);
    
    // Assert: Identical outputs (critical for deterministic scaffold requirement)
    expect(runs[0].triple.text).toEqual(runs2[0].triple.text);
    expect(runs[1].triple.text).toEqual(runs2[1].triple.text);
    expect(runs[2].triple.text).toEqual(runs2[2].triple.text);
    expect(runs[3].triple.text).toEqual(runs2[3].triple.text);
  });
  
  test('generators extract refs and citations correctly', async () => {
    // Act: Generate documents from all generators
    const dsResult = await generators.ds.generate(mockContext);
    const spResult = await generators.sp.generate(mockContext);
    const xResult = await generators.x.generate(mockContext);
    const mResult = await generators.m.generate(mockContext);
    
    // Assert: Citations and refs are properly extracted
    expect(dsResult.triple.text.source_refs).toContain('CIT:spec#p5');
    expect(spResult.triple.text.refs).toContain('CIT:design#p3');
    expect(xResult.triple.text.refs).toContain('CIT:test#p2');
    expect(xResult.triple.text.refs).toContain('CIT:security#p4');
    expect(mResult.triple.text.trace_back).toContain('CIT:security#p4');
    
    // Verify terms extraction includes matrix metadata
    expect(dsResult.triple.terms_used).toContain('Requirements');
    expect(spResult.triple.terms_used).toContain('Objectives');
    expect(xResult.triple.terms_used).toContain('Verification');
    expect(mResult.triple.terms_used).toContain('Evaluation');
  });
});