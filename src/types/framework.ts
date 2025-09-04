// src/types/framework.ts

export interface FrameworkRunManifest {
  run_id: string;
  created_at: string; // ISO 8601
  tool: { name: string; version: string };
  framework_schema_version: string; // e.g., "1.0.0"
  problem: { title: string; statement: string };
  durations: { total_ms: number; [k: string]: number | undefined };
  matrices: {
    C: MatrixFileMeta;
    D: MatrixFileMeta;
    X: MatrixFileMeta;
    E: MatrixFileMeta;
  };
}

export interface MatrixFileMeta {
  path: string;     // e.g., "snapshots/C.jsonl"
  format?: string;  // e.g., "cells-jsonl-v1"
  records: number;  // number of lines
  sha256: string;   // hex-encoded sha256 of raw file
  bytes?: number;   // optional size
}

export type MatrixKind = 'C' | 'D' | 'X' | 'E';

// Core Chirality document types (centralized from contracts.ts)
export type DS = { 
  data_field: string; 
  units?: string; 
  type?: string; 
  source_refs?: string[]; 
  notes?: string[] 
};

export type SP = { 
  step: string; 
  purpose?: string; 
  inputs?: string[]; 
  outputs?: string[]; 
  preconditions?: string[]; 
  postconditions?: string[]; 
  refs?: string[] 
};

export type X = { 
  heading: string; 
  narrative: string; 
  precedents?: string[]; 
  successors?: string[]; 
  context_notes?: string[]; 
  refs?: string[] 
};

export type M = { 
  statement: string; 
  justification?: string; 
  trace_back?: string[]; 
  assumptions?: string[]; 
  residual_risk?: string[] 
};

export type DocKind = 'DS' | 'SP' | 'X' | 'M';

// Legacy MatrixCell interface (will use lib/framework/types.ts going forward)
export interface MatrixCell {
  id: string;
  matrix: MatrixKind;
  row: number;
  col: number;
  row_label: string;
  col_label: string;
  station: string;
  text: string;
  citations: string[];
  refs: string[];
  meta?: { order?: number; [k: string]: unknown };
}
