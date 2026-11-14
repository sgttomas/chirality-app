// Provider clauses are closed product words. Unknown input never becomes an
// assurance claim and never selects text supplied by a record.
export function sealProviderClause(value: unknown): string {
  switch (value) {
    case "file-key": return "sealed with the key file, which a process on this account could forge";
    case "keychain": return "sealed with the keychain key";
    default: return "seal provider not recorded";
  }
}

// Legacy captures lack an authenticated historical provider. Say only which
// provider verified their original bytes on this observation.
export function verifiedProviderClause(value: unknown): string {
  switch (value) {
    case "file-key": return "verified here using the key file, which a process on this account could forge";
    case "keychain": return "verified here using the keychain key";
    default: return "verifying provider not established";
  }
}
