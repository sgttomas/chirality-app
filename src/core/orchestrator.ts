import { Station, STATIONS, STATION_META } from '../domain/station';
import { Packet, createPacket } from '../domain/packet';
import { assertStationTransition, assertDataDeps } from '../domain/validators';
import { RunState, initRunState, updateStation, updateDocument, addPacket, completeRun } from './state';
import { LLMService, SemanticContext } from './llm/service';
import { Exporter } from './exporter';

// Import station processors
import { processS1 } from './stations/S1';
import { processS2 } from './stations/S2';
import { processS3 } from './stations/S3';
import { processS4 } from './stations/S4';
import { processS5 } from './stations/S5';
import { processS6 } from './stations/S6';
import { processS7 } from './stations/S7';
import { processS8 } from './stations/S8';
import { processS9 } from './stations/S9';
import { processS10 } from './stations/S10';
import { processS11 } from './stations/S11';

export type TraversalMode = 'full' | 'foundation';

export interface TraversalOptions {
  mode?: TraversalMode; // 'full' = S1-S11, 'foundation' = S1-S5+S11 (default)
  onProgress?: (station: Station, duration: number) => void;
  maxTokensPerStation?: number;
  temperature?: number;
  exportRun?: boolean; // Whether to export run files after completion
  llmOptional?: boolean; // Allow fallback mode without valid API key (foundation mode only)
}

export interface TraversalResult {
  runId: string;
  packets: Packet[];
  resolution: string;
  metadata: {
    durations: Record<Station, number>;
    totalDuration: number;
    totalTokens: number;
  };
}

export interface ProblemRequest {
  title: string;
  statement: string;
  initialVector?: Record<string, any>;
}

const stationProcessors = {
  S1: processS1,
  S2: processS2,
  S3: processS3,
  S4: processS4,
  S5: processS5,
  S6: processS6,
  S7: processS7,
  S8: processS8,
  S9: processS9,
  S10: processS10,
  S11: processS11
};

export class Orchestrator {
  private llmService: LLMService;
  private exporter: Exporter;

  constructor(llmService: LLMService, runsDir: string = 'runs') {
    this.llmService = llmService;
    this.exporter = new Exporter(runsDir);
  }

  async runTraversal(
    problem: ProblemRequest,
    options: TraversalOptions = {}
  ): Promise<TraversalResult> {
    const runId = this.generateRunId();
    let state = initRunState(runId, problem.statement, problem.initialVector);
    
    const durations: Record<Station, number> = {} as Record<Station, number>;
    let totalTokens = 0;

    // Determine which stations to execute based on mode
    const mode = options.mode || 'foundation'; // Default to foundation mode
    const stationsToExecute = this.getStationsForMode(mode);

    console.log(`[Orchestrator] Starting ${mode} traversal with stations:`, stationsToExecute);

    try {
      // Execute stations based on selected mode
      for (const station of stationsToExecute) {
        const startTime = Date.now();
        
        // Validate station transition with allowed stations for this mode
        assertStationTransition(state.currentStation, station, stationsToExecute);
        
        // Build semantic context for this station
        const context = this.buildSemanticContext(state, station);
        
        // Process the station
        const processor = stationProcessors[station];
        const result = await processor(context, this.llmService, state.initialVector);
        
        const duration = Date.now() - startTime;
        durations[station] = duration;
        
        // Update state with station result
        state = updateStation(state, station, result.output, duration, result.tokens);
        
        // Update document state for S2-S5
        if (station === 'S2') {
          state = updateDocument(state, 'dataSheet', result.output);
        } else if (station === 'S3') {
          state = updateDocument(state, 'standardProcedure', result.output);
        } else if (station === 'S4') {
          state = updateDocument(state, 'guidanceDocument', result.output);
        } else if (station === 'S5') {
          state = updateDocument(state, 'evaluationChecklist', result.output);
        }
        
        // Create and add packet
        const stationMeta = STATION_META[station];
        const packet = createPacket(
          station,
          stationMeta.modality,
          { [stationMeta.operation]: result.output },
          { duration, tokens: result.tokens }
        );
        state = addPacket(state, packet);
        
        // Track tokens
        if (result.tokens) {
          totalTokens += result.tokens.total;
        }
        
        // Call progress callback
        if (options.onProgress) {
          options.onProgress(station, duration);
        }
        
        console.log(`[Orchestrator] Completed ${station} (${stationMeta.label}) in ${duration}ms`);
      }
      
      console.log(`[Orchestrator] ${mode} traversal completed with ${stationsToExecute.length} stations`);
      
      // Validate data dependencies between stations
      try {
        assertDataDeps(state.packets);
        console.log(`[Orchestrator] Data dependency validation passed`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown validation error';
        console.warn(`[Orchestrator] Data dependency validation failed:`, errorMessage);
        // Don't fail traversal for dependency issues in current implementation
        // TODO: Make this stricter once station payload structures are finalized
      }
      
      // Complete the run
      state = completeRun(state);
      
      // Export run if requested (default to true)
      if (options.exportRun !== false) {
        try {
          await this.exporter.writeRun(state);
          console.log(`[Orchestrator] Exported run ${state.runId} to files`);
        } catch (error) {
          console.warn(`[Orchestrator] Failed to export run ${state.runId}:`, error);
          // Don't fail the traversal if export fails
        }
      }
      
      // Extract resolution from S11
      const s11Packet = state.packets.find(p => p.station === 'S11');
      const resolution = s11Packet?.payload?.Final || 'No resolution generated';
      
      return {
        runId,
        packets: state.packets,
        resolution,
        metadata: {
          durations,
          totalDuration: state.totalDuration || 0,
          totalTokens
        }
      };
      
    } catch (error) {
      console.error(`[Orchestrator] Traversal failed at ${state.currentStation}:`, error);
      throw error;
    }
  }

  private getStationsForMode(mode: TraversalMode): Station[] {
    switch (mode) {
      case 'full':
        // Complete 11-station traversal
        return ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11'];
      
      case 'foundation':
        // Foundation traversal: 4 core documents + resolution
        return ['S1', 'S2', 'S3', 'S4', 'S5', 'S11'];
      
      default:
        throw new Error(`Unknown traversal mode: ${mode}`);
    }
  }

  private buildSemanticContext(state: RunState, station: Station): SemanticContext {
    const context: SemanticContext = {
      problemStatement: state.problemStatement
    };
    
    // Add accumulated documents
    if (state.documents.dataSheet) context.dataSheet = state.documents.dataSheet;
    if (state.documents.standardProcedure) context.standardProcedure = state.documents.standardProcedure;
    if (state.documents.guidanceDocument) context.guidanceDocument = state.documents.guidanceDocument;
    if (state.documents.evaluationChecklist) context.evaluationChecklist = state.documents.evaluationChecklist;
    if (state.documents.solutionStatements) context.solutionStatements = state.documents.solutionStatements;
    
    // Add iteration context for refinement cycles
    if (station === 'S7' || station === 'S8' || station === 'S9') {
      context.iterationNumber = state.iterationNumber + 1;
    }
    
    return context;
  }

  private generateRunId(): string {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 8);
    return `run_${timestamp}_${random}`;
  }
}

export async function createOrchestrator(apiKey?: string, allowFallback?: boolean): Promise<Orchestrator> {
  const key = apiKey || process.env.OPENAI_API_KEY;
  
  if (!key) {
    if (allowFallback) {
      console.warn('[Orchestrator] No API key provided - using disabled LLM mode');
      // Create LLM service with disabled flag - no network calls will be made
      const llmService = new LLMService({ apiKey: 'disabled', disabled: true });
      return new Orchestrator(llmService);
    }
    throw new Error('OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass apiKey parameter.');
  }
  
  const llmService = new LLMService({ apiKey: key });
  
  // Validate API key unless fallback is allowed
  if (!allowFallback) {
    const isValid = await llmService.validateApiKey();
    if (!isValid) {
      throw new Error('Invalid OpenAI API key provided');
    }
  } else {
    // In fallback mode, try validation but don't fail if invalid - switch to disabled mode
    try {
      const isValid = await llmService.validateApiKey();
      if (!isValid) {
        console.warn('[Orchestrator] Invalid API key provided - switching to disabled LLM mode');
        return new Orchestrator(new LLMService({ apiKey: 'disabled', disabled: true }));
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown validation error';
      console.warn('[Orchestrator] API key validation failed - switching to disabled LLM mode:', errorMessage);
      return new Orchestrator(new LLMService({ apiKey: 'disabled', disabled: true }));
    }
  }
  
  return new Orchestrator(llmService);
}