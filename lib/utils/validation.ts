/**
 * Validation utilities for agent orchestration
 */

/**
 * Validate run_id format: ^[a-z0-9-_]{1,64}$
 * Forbids /, .., and \
 */
export function validateRunId(runId: string): { valid: boolean; error?: string } {
  // Check basic pattern
  if (!/^[a-z0-9-_]{1,64}$/.test(runId)) {
    return { 
      valid: false, 
      error: 'run_id must be 1-64 characters, lowercase letters, numbers, hyphens, and underscores only' 
    };
  }
  
  // Forbid dangerous characters
  if (runId.includes('/') || runId.includes('..') || runId.includes('\\')) {
    return { 
      valid: false, 
      error: 'run_id cannot contain /, .., or \\' 
    };
  }
  
  return { valid: true };
}

/**
 * Generate a valid run_id if framework doesn't provide one
 */
export function generateRunId(prefix: string = ''): string {
  const timestamp = new Date().toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .substring(0, 19); // YYYY-MM-DD_HH-MM-SS
  
  const random = Math.random().toString(36).substring(2, 8);
  
  const runId = prefix 
    ? `${prefix}_${timestamp}_${random}`
    : `run_${timestamp}_${random}`;
  
  // Ensure it's valid (should always be)
  const validation = validateRunId(runId);
  if (!validation.valid) {
    throw new Error(`Generated invalid run_id: ${validation.error}`);
  }
  
  return runId;
}

/**
 * Extract run_id from framework stdout if available
 * Framework should output line like: "RUN_ID: sample-run-001"
 */
export function extractRunIdFromFrameworkOutput(stdout: string): string | null {
  const lines = stdout.split('\n');
  
  for (const line of lines) {
    const match = line.match(/RUN_ID:\s*([a-z0-9-_]+)/i);
    if (match && match[1]) {
      const runId = match[1].toLowerCase();
      const validation = validateRunId(runId);
      return validation.valid ? runId : null;
    }
  }
  
  return null;
}