import { Station, STATIONS } from './station';
import { Packet } from './packet';

export interface ValidationError extends Error {
  code: string;
  details?: Record<string, any>;
}

export function createValidationError(
  code: string,
  message: string,
  details?: Record<string, any>
): ValidationError {
  const error = new Error(message) as ValidationError;
  error.code = code;
  error.details = details;
  return error;
}

export function assertStationTransition(from: Station | null, to: Station, allowedStations?: Station[]): void {
  if (from === null && to !== 'S1') {
    throw createValidationError(
      'ERR_STATION_INVALID',
      `First station must be S1, got ${to}`,
      { from, to }
    );
  }

  if (from !== null) {
    // If we have a specific station list, use that for validation
    if (allowedStations) {
      const fromIndex = allowedStations.indexOf(from);
      const toIndex = allowedStations.indexOf(to);
      
      if (fromIndex === -1 || toIndex === -1) {
        throw createValidationError(
          'ERR_STATION_INVALID',
          `Station not in allowed list: ${from} -> ${to}`,
          { from, to, allowedStations }
        );
      }
      
      if (toIndex !== fromIndex + 1) {
        throw createValidationError(
          'ERR_ORDER_VIOLATION',
          `Invalid station transition in sequence from ${from} to ${to}`,
          { from, to, expectedNext: allowedStations[fromIndex + 1] }
        );
      }
    } else {
      // Default behavior: sequential validation
      const fromIndex = STATIONS.indexOf(from);
      const toIndex = STATIONS.indexOf(to);
      
      if (toIndex !== fromIndex + 1) {
        throw createValidationError(
          'ERR_ORDER_VIOLATION',
          `Invalid station transition from ${from} to ${to}`,
          { from, to, expectedNext: STATIONS[fromIndex + 1] }
        );
      }
    }
  }
}

export function assertOrder(packets: Packet[]): void {
  for (let i = 0; i < packets.length - 1; i++) {
    const current = packets[i];
    const next = packets[i + 1];
    
    assertStationTransition(current.station, next.station);
  }
}

export function assertDataDeps(packets: Packet[]): void {
  const packetsByStation = new Map<Station, Packet>();
  
  for (const packet of packets) {
    packetsByStation.set(packet.station, packet);
  }

  // Foundation mode dependencies (S1-S5+S11)
  // S2 (DS) requires J from S1 (only if S1 is present)
  if (packetsByStation.has('S2') && packetsByStation.has('S1')) {
    const s1 = packetsByStation.get('S1');
    if (!s1 || !s1.payload?.J) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S2 (Data Sheet) requires J operation from S1 (Problem Statement)',
        { station: 'S2', dependency: 'J@S1' }
      );
    }
  }

  // S3 (SP) requires DS from S2 (only if S2 is present)
  if (packetsByStation.has('S3') && packetsByStation.has('S2')) {
    const s2 = packetsByStation.get('S2');
    if (!s2 || !s2.payload?.DS) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S3 (Standard Procedure) requires DS operation from S2 (Data Sheet)',
        { station: 'S3', dependency: 'DS@S2' }
      );
    }
  }

  // S4 (GD) requires SP from S3 (only if S3 is present)
  if (packetsByStation.has('S4') && packetsByStation.has('S3')) {
    const s3 = packetsByStation.get('S3');
    if (!s3 || !s3.payload?.SP) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S4 (Guidance Document) requires SP operation from S3 (Standard Procedure)',
        { station: 'S4', dependency: 'SP@S3' }
      );
    }
  }

  // S5 (EC) requires GD from S4 (only if S4 is present)
  if (packetsByStation.has('S5') && packetsByStation.has('S4')) {
    const s4 = packetsByStation.get('S4');
    if (!s4 || !s4.payload?.GD) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S5 (Evaluation Checklist) requires GD operation from S4 (Guidance Document)',
        { station: 'S5', dependency: 'GD@S4' }
      );
    }
  }

  // S11 (Final) in foundation mode requires EC from S5
  if (packetsByStation.has('S11') && !packetsByStation.has('S10')) {
    // Foundation mode: S11 follows S5 directly
    const s5 = packetsByStation.get('S5');
    if (!s5 || !s5.payload?.EC) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S11 (Resolution) in foundation mode requires EC operation from S5 (Evaluation Checklist)',
        { station: 'S11', dependency: 'EC@S5', mode: 'foundation' }
      );
    }
  }

  // Full mode dependencies (S6-S10 are placeholders for future implementation)
  // Note: S6-S10 logic should be updated when those stations are implemented
  if (packetsByStation.has('S11') && packetsByStation.has('S10')) {
    // Full mode: S11 follows S10
    const s10 = packetsByStation.get('S10');
    if (!s10 || !Object.keys(s10.payload).length) {
      throw createValidationError(
        'ERR_MISSING_DEPENDENCY',
        'S11 (Resolution) in full mode requires output from S10',
        { station: 'S11', dependency: 'output@S10', mode: 'full' }
      );
    }
  }
}