export function validateRunId(runId: string): { valid: boolean; error?: string } {
  // Basic run_id validation - alphanumeric with underscores and dashes
  const runIdRegex = /^[a-zA-Z0-9_-]+$/;
  
  if (!runId) {
    return { valid: false, error: 'run_id cannot be empty' };
  }
  
  if (!runIdRegex.test(runId)) {
    return { valid: false, error: 'run_id must contain only alphanumeric characters, underscores, and dashes' };
  }
  
  if (runId.length > 100) {
    return { valid: false, error: 'run_id must be 100 characters or less' };
  }
  
  return { valid: true };
}