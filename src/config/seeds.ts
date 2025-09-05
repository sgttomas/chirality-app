/**
 * Configuration for seed extraction functionality
 * Reads environment variables with defaults as specified in the plan
 */

export interface SeedsConfig {
  enableHeuristics: boolean;
  minItems: number;
  maxItems: number;
  maxLength: number;
  verifyChecksums: boolean;
  persist: boolean;
  runsDir: string;
}

export const seedsConfig: SeedsConfig = {
  enableHeuristics: process.env.SEEDS_ENABLE_HEURISTICS === 'true',
  minItems: parseInt(process.env.SEEDS_MIN_ITEMS || '6', 10),
  maxItems: parseInt(process.env.SEEDS_MAX_ITEMS || '12', 10),
  maxLength: parseInt(process.env.SEEDS_MAX_LEN || '120', 10),
  verifyChecksums: process.env.SEEDS_VERIFY_CHECKSUMS !== 'false', // default true
  persist: process.env.SEEDS_PERSIST !== 'false', // default true
  runsDir: process.env.CHIRALITY_RUNS_DIR || 'runs',
};

// Validation function to ensure config values are sensible
export function validateSeedsConfig(config: SeedsConfig): string[] {
  const errors: string[] = [];

  if (config.minItems < 1) {
    errors.push('SEEDS_MIN_ITEMS must be at least 1');
  }

  if (config.maxItems < config.minItems) {
    errors.push('SEEDS_MAX_ITEMS must be greater than or equal to SEEDS_MIN_ITEMS');
  }

  if (config.maxLength < 10) {
    errors.push('SEEDS_MAX_LEN must be at least 10 characters');
  }

  if (!config.runsDir || config.runsDir.trim() === '') {
    errors.push('CHIRALITY_RUNS_DIR cannot be empty');
  }

  return errors;
}

// Runtime validation - log warnings for invalid config
const configErrors = validateSeedsConfig(seedsConfig);
if (configErrors.length > 0) {
  console.warn('[Seeds Config] Invalid configuration detected:');
  configErrors.forEach(error => console.warn(`  - ${error}`));
}