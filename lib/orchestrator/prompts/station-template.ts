/**
 * Station template interface for the semantic valley traversal pipeline
 */

export type StationId = 'S0' | 'S1' | 'S2' | 'S3' | 'S4' | 'S5' | 'S6' | 'S7' | 'S8';
export type Modality = 'systematic' | 'process' | 'epistemic' | 'alethic';

/**
 * Input structure for a station in the pipeline
 */
export interface StationInput {
  problem: { title: string; statement: string };
  previousStations?: Record<string, any>;
  matrixInjection?: any;
}

/**
 * Contract for each station's prompt generation and processing
 */
export interface StationPrompt {
  /**
   * Unique identifier for this station
   */
  station: StationId;
  
  /**
   * The ontological modality this station operates in
   */
  modality: Modality;
  
  /**
   * Build the prompt for this station given the input
   */
  buildPrompt(input: StationInput): string;
  
  /**
   * The expected output type from this station
   */
  expectedOutput: 'document' | 'analysis' | 'resolution';
  
  /**
   * Whether this station should assess risk (only true for alethic stations S6, S8)
   */
  requiresRiskAssessment: boolean;
}

/**
 * Station output document type mappings
 * Null means the station doesn't produce a document
 */
export const STATION_OUTPUTS = {
  S0: null,  // Problem normalization
  S1: 'DS',  // Systematic → Data Sheet
  S2: 'SP',  // Process → Standard Procedure v1
  S3: 'X',   // Epistemic → Solution Template v1  
  S4: 'SP',  // Process → Standard Procedure v2
  S5: 'X',   // Epistemic → Solution Template v2
  S6: 'M',   // Alethic → Guidance v1
  S7: 'X',   // Epistemic → Solution Template v3
  S8: 'M'    // Alethic → Guidance v2 + Resolution
} as const;

/**
 * Matrix injection points - where external framework matrices are applied
 */
export const MATRIX_INJECTION_POINTS = {
  'C': 'S1' as StationId,  // Requirements matrix → Systematic station
  'D': 'S2' as StationId,  // Objectives matrix → Process station
  'X': 'S3' as StationId,  // Verification matrix → Epistemic station
  'E': 'S6' as StationId   // Evaluation matrix → Alethic station
} as const;

/**
 * Compatibility mapping from old V1/V2/V3 passes to new stations
 */
export const V_COMPATIBILITY_MAP = {
  V1: ['S1', 'S2', 'S3'] as StationId[],
  V2: ['S4', 'S5', 'S6'] as StationId[],
  V3: ['S7', 'S8'] as StationId[]
} as const;

/**
 * Valid station transitions for state machine validation
 */
export const VALID_TRANSITIONS: Record<StationId, StationId[]> = {
  'S0': ['S1'],
  'S1': ['S2'],
  'S2': ['S3'],
  'S3': ['S4'],
  'S4': ['S5'],
  'S5': ['S6'],
  'S6': ['S7'],
  'S7': ['S8'],
  'S8': []  // Terminal station
};

/**
 * Get the modality for a given station
 */
export function getStationModality(station: StationId): Modality {
  const modalityMap: Record<StationId, Modality> = {
    'S0': 'systematic',  // Problem normalization
    'S1': 'systematic',  // Structure the problem
    'S2': 'process',     // Operational pathfinding
    'S3': 'epistemic',   // Knowledge claims
    'S4': 'process',     // Refined procedures
    'S5': 'epistemic',   // Updated knowledge
    'S6': 'alethic',     // Necessity/possibility
    'S7': 'epistemic',   // Reconcile claims
    'S8': 'alethic'      // Final synthesis
  };
  return modalityMap[station];
}

/**
 * Check if a station requires risk assessment
 */
export function requiresRiskAssessment(station: StationId): boolean {
  return station === 'S6' || station === 'S8';
}