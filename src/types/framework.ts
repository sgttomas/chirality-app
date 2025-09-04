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
