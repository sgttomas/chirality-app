// Factory and helpers for matrix-driven generation
import type { Triple, DS, SP, X, M, DocKind } from '@/chirality-core/contracts';
import type { MatrixDocumentGenerator, GenerationContext } from './types';
import { DSGenerator } from './ds';
import { SPGenerator } from './sp';
import { XGenerator } from './x';
import { MGenerator } from './m';

export function createMatrixGenerator(): MatrixDocumentGenerator {
  return {
    ds: new DSGenerator(),
    sp: new SPGenerator(),
    x: new XGenerator(),
    m: new MGenerator(),
  };
}

export async function generateAll(ctx: GenerationContext) {
  const generator = createMatrixGenerator();
  const results: Record<string, any> = {};
  const logs: string[] = [];
  
  // Generate scaffolds in matrix dependency order
  const dsResult = await generator.ds.generate(ctx);
  results.DS = dsResult.triple;
  logs.push(...dsResult.logs.map(log => `[DS] ${log}`));
  
  const spResult = await generator.sp.generate(ctx);
  results.SP = spResult.triple;
  logs.push(...spResult.logs.map(log => `[SP] ${log}`));
  
  const xResult = await generator.x.generate(ctx);
  results.X = xResult.triple;
  logs.push(...xResult.logs.map(log => `[X] ${log}`));
  
  const mResult = await generator.m.generate(ctx);
  results.M = mResult.triple;
  logs.push(...mResult.logs.map(log => `[M] ${log}`));
  
  return {
    triples: results,
    logs,
    generatedAt: new Date().toISOString()
  };
}

// Re-export types
export * from './types';