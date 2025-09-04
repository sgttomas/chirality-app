export interface FrameworkRunManifest {
  framework_schema_version: string;
  matrices: {
    C: MatrixManifest;
    D: MatrixManifest;
    X: MatrixManifest;
    E: MatrixManifest;
  };
}

interface MatrixManifest {
  path: string;
  records: number;
  sha256: string;
}