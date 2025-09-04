/**
 * Main pipeline orchestrator for the semantic valley traversal
 */

import { Packet, createPacket } from '../../utils/packets';
import { 
  StationId, 
  StationInput,
  STATION_OUTPUTS,
  MATRIX_INJECTION_POINTS,
  V_COMPATIBILITY_MAP,
  getStationModality
} from '../prompts/station-template';

// Import station handlers (to be implemented)
import { runS0 } from './S0';
import { runS1 } from './S1';
import { runS2 } from './S2';
import { runS3 } from './S3';
import { runS4 } from './S4';
import { runS5 } from './S5';
import { runS6 } from './S6';
import { runS7 } from './S7';
import { runS8 } from './S8';

/**
 * Map of station handlers
 */
const STATION_HANDLERS: Record<StationId, (input: StationInput) => Promise<any>> = {
  S0: runS0,
  S1: runS1,
  S2: runS2,
  S3: runS3,
  S4: runS4,
  S5: runS5,
  S6: runS6,
  S7: runS7,
  S8: runS8
};

/**
 * Traversal state tracking
 */
export interface TraversalState {
  problemId: string;
  problem: { title: string; statement: string };
  stations: {
    S0?: any;
    S1?: any;
    S2?: any;
    S3?: any;
    S4?: any;
    S5?: any;
    S6?: any;
    S7?: any;
    S8?: any;
  };
  currentStation: StationId;
  matrices?: Record<string, any>;
  metadata?: {
    startTime: number;
    endTime?: number;
    matrixInjections: string[];
  };
}

/**
 * Run a single station in the pipeline
 */
export async function runStation(
  stationId: StationId, 
  input: StationInput
): Promise<any> {
  console.log(`[Pipeline] Running station ${stationId} (${getStationModality(stationId)} modality)`);
  
  const handler = STATION_HANDLERS[stationId];
  if (!handler) {
    throw new Error(`No handler registered for station ${stationId}`);
  }
  
  try {
    const result = await handler(input);
    console.log(`[Pipeline] Station ${stationId} completed successfully`);
    return result;
  } catch (error) {
    console.error(`[Pipeline] Station ${stationId} failed:`, error);
    throw error;
  }
}

/**
 * Run the complete semantic valley traversal
 */
export async function runTraversal(
  problem: { title: string; statement: string },
  options?: {
    matrices?: Record<string, any>;
    startStation?: StationId;
    endStation?: StationId;
    onProgress?: (state: TraversalState) => void;
  }
): Promise<TraversalState> {
  const startStation = options?.startStation || 'S0';
  const endStation = options?.endStation || 'S8';
  
  // Initialize traversal state
  const state: TraversalState = {
    problemId: generateProblemId(),
    problem,
    stations: {},
    currentStation: startStation,
    matrices: options?.matrices,
    metadata: {
      startTime: Date.now(),
      matrixInjections: []
    }
  };
  
  console.log(`[Pipeline] Starting semantic valley traversal: ${startStation} → ${endStation}`);
  
  // Define the station sequence
  const stationSequence: StationId[] = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'];
  const startIdx = stationSequence.indexOf(startStation);
  const endIdx = stationSequence.indexOf(endStation);
  
  if (startIdx === -1 || endIdx === -1 || startIdx > endIdx) {
    throw new Error(`Invalid station range: ${startStation} → ${endStation}`);
  }
  
  // Execute stations in sequence
  for (let i = startIdx; i <= endIdx; i++) {
    const stationId = stationSequence[i];
    state.currentStation = stationId;
    
    // Check for matrix injection at this station
    const matrixKey = Object.entries(MATRIX_INJECTION_POINTS).find(
      ([_, targetStation]) => targetStation === stationId
    )?.[0];
    
    const matrixInjection = matrixKey && state.matrices?.[matrixKey];
    if (matrixInjection) {
      console.log(`[Pipeline] Injecting ${matrixKey} matrix at station ${stationId}`);
      state.metadata!.matrixInjections.push(matrixKey);
    }
    
    // Prepare station input
    const stationInput: StationInput = {
      problem: state.problem,
      previousStations: { ...state.stations },
      matrixInjection
    };
    
    // Run the station
    const result = await runStation(stationId, stationInput);
    state.stations[stationId] = result;
    
    // Report progress
    if (options?.onProgress) {
      options.onProgress({ ...state });
    }
  }
  
  // Mark completion
  state.metadata!.endTime = Date.now();
  const duration = state.metadata!.endTime - state.metadata!.startTime;
  console.log(`[Pipeline] Traversal completed in ${duration}ms`);
  
  return state;
}

/**
 * Compatibility layer: Run old V1/V2/V3 orchestration through new pipeline
 */
export async function runCompatibilityMode(
  version: 'V1' | 'V2' | 'V3',
  problem: { title: string; statement: string },
  previousResults?: any
): Promise<Record<string, any>> {
  const stations = V_COMPATIBILITY_MAP[version];
  console.log(`[Compatibility] Running ${version} as stations: ${stations.join(', ')}`);
  
  const results: Record<string, any> = {};
  
  for (const stationId of stations) {
    const input: StationInput = {
      problem,
      previousStations: { ...previousResults, ...results },
      matrixInjection: undefined
    };
    
    const result = await runStation(stationId, input);
    results[stationId] = result;
    
    // Map to document type for compatibility
    const docType = STATION_OUTPUTS[stationId];
    if (docType) {
      results[docType] = result;
    }
  }
  
  return results;
}

/**
 * Generate a unique problem ID
 */
function generateProblemId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 9);
  return `trav_${timestamp}_${random}`;
}