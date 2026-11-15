// Provider clauses are closed product words. Unknown input never becomes an
// assurance claim and never selects text supplied by a record.
export function sealProviderClause(value: unknown): string {
  switch (value) {
    case "file-key": return "sealed with the App's key file, not your keychain";
    case "keychain": return "sealed with your keychain";
    default: return "seal provider not recorded";
  }
}
