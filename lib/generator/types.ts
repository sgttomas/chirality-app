// Shared types for matrix-driven document generation
import type { Triple, DS, SP, X, M, DocKind } from '@/chirality-core/contracts';
import type { MatrixCell } from '@/types/framework';

export interface GenerationContext {
  problem: { title: string; statement: string; initialVector: string[] };
  matrices: {
    C: MatrixCell[];
    D: MatrixCell[];
    X: MatrixCell[];
    E: MatrixCell[];
  };
  // Optional switches for strictness, truncation, etc.
  options?: {
    maxItemsPerSection?: number;
  };
}

export interface GeneratorResult<T> {
  triple: Triple<T>;
  logs: string[];
}

export interface DocumentGenerator<T> {
  generate(ctx: GenerationContext): Promise<GeneratorResult<T>>;
}

export type MatrixDocumentGenerator = {
  ds: DocumentGenerator<DS>;
  sp: DocumentGenerator<SP>;
  x: DocumentGenerator<X>;
  m: DocumentGenerator<M>;
};