import { Station, Modality } from './station';

export interface Packet<T = any> {
  id: string;
  createdAt: string;
  station: Station;
  modality: Modality;
  payload: T;
  meta?: Record<string, any>;
}

export function createPacket<T>(
  station: Station,
  modality: Modality,
  payload: T,
  meta?: Record<string, any>
): Packet<T> {
  const content = JSON.stringify({ station, modality, payload });
  const hash = Buffer.from(content).toString('base64').slice(0, 12);
  
  return {
    id: `${station}-${hash}`,
    createdAt: new Date().toISOString(),
    station,
    modality,
    payload,
    meta
  };
}