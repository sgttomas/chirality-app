import { Station } from '../domain/station';
import { Packet } from '../domain/packet';

export interface DocumentState {
  dataSheet?: string;
  standardProcedure?: string;
  guidanceDocument?: string;
  evaluationChecklist?: string;
  solutionStatements?: string;
}

export interface StationResult {
  station: Station;
  output: string;
  duration: number;
  tokens?: {
    prompt: number;
    completion: number;
    total: number;
  };
}

export interface RunState {
  runId: string;
  problemStatement: string;
  initialVector?: Record<string, any>;
  currentStation: Station | null;
  documents: DocumentState;
  stationResults: StationResult[];
  packets: Packet[];
  startTime: string;
  endTime?: string;
  totalDuration?: number;
  iterationNumber: number;
}

export function initRunState(
  runId: string,
  problemStatement: string,
  initialVector?: Record<string, any>
): RunState {
  return {
    runId,
    problemStatement,
    initialVector,
    currentStation: null,
    documents: {},
    stationResults: [],
    packets: [],
    startTime: new Date().toISOString(),
    iterationNumber: 0
  };
}

export function updateStation(
  state: RunState,
  station: Station,
  output: string,
  duration: number,
  tokens?: { prompt: number; completion: number; total: number }
): RunState {
  const result: StationResult = {
    station,
    output,
    duration,
    tokens
  };

  return {
    ...state,
    currentStation: station,
    stationResults: [...state.stationResults, result]
  };
}

export function updateDocument(
  state: RunState,
  documentType: keyof DocumentState,
  content: string
): RunState {
  return {
    ...state,
    documents: {
      ...state.documents,
      [documentType]: content
    }
  };
}

export function addPacket(state: RunState, packet: Packet): RunState {
  return {
    ...state,
    packets: [...state.packets, packet]
  };
}

export function incrementIteration(state: RunState): RunState {
  return {
    ...state,
    iterationNumber: state.iterationNumber + 1
  };
}

export function completeRun(state: RunState): RunState {
  const endTime = new Date().toISOString();
  const totalDuration = new Date(endTime).getTime() - new Date(state.startTime).getTime();

  return {
    ...state,
    endTime,
    totalDuration,
    currentStation: null
  };
}

// Selectors for data dependencies
export function getXFromS4(state: RunState): string | null {
  const s4Result = state.stationResults.find(r => r.station === 'S4');
  return s4Result?.output || null;
}

export function getZFromS5(state: RunState): string | null {
  const s5Result = state.stationResults.find(r => r.station === 'S5');
  return s5Result?.output || null;
}

export function getPFromS6(state: RunState): string | null {
  const s6Result = state.stationResults.find(r => r.station === 'S6');
  return s6Result?.output || null;
}

export function getWFromS8(state: RunState): string | null {
  const s8Result = state.stationResults.find(r => r.station === 'S8');
  return s8Result?.output || null;
}

export function getUFromS9(state: RunState): string | null {
  const s9Result = state.stationResults.find(r => r.station === 'S9');
  return s9Result?.output || null;
}

export function getNFromS10(state: RunState): string | null {
  const s10Result = state.stationResults.find(r => r.station === 'S10');
  return s10Result?.output || null;
}