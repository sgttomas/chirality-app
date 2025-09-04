export type Station = 'S1' | 'S2' | 'S3' | 'S4' | 'S5' | 'S6' | 'S7' | 'S8' | 'S9' | 'S10' | 'S11';

export type Modality = 'problem' | 'systematic' | 'process' | 'epistemic' | 'alethic' | 'resolution';

export const STATIONS: Station[] = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11'];

export const EXEC_GROUP: Record<Station, string> = {
  S1: 'G1',
  S2: 'G2', 
  S3: 'G3',
  S4: 'G4',
  S5: 'G4',
  S6: 'G5',
  S7: 'G6',
  S8: 'G7',
  S9: 'G8',
  S10: 'G8',
  S11: 'G9'
};

export interface StationMeta {
  station: Station;
  label: string;
  modality: Modality;
  operation: string;
  group: string;
}

export const STATION_META: Record<Station, StationMeta> = {
  S1: {
    station: 'S1',
    label: 'Problem Statement',
    modality: 'problem',
    operation: 'J',
    group: 'G1'
  },
  S2: {
    station: 'S2', 
    label: 'Data Sheet',
    modality: 'systematic',
    operation: 'DS',
    group: 'G2'
  },
  S3: {
    station: 'S3',
    label: 'Standard Procedure', 
    modality: 'process',
    operation: 'SP',
    group: 'G3'
  },
  S4: {
    station: 'S4',
    label: 'Guidance Document',
    modality: 'epistemic',
    operation: 'GD',
    group: 'G4'
  },
  S5: {
    station: 'S5',
    label: 'Evaluation Checklist',
    modality: 'process', 
    operation: 'EC',
    group: 'G4'
  },
  S6: {
    station: 'S6',
    label: 'Evaluation',
    modality: 'process',
    operation: 'P',
    group: 'G5'
  },
  S7: {
    station: 'S7',
    label: 'Assessment',
    modality: 'epistemic',
    operation: 'M',
    group: 'G6'
  },
  S8: {
    station: 'S8',
    label: 'Implementation',
    modality: 'alethic',
    operation: 'W',
    group: 'G7'
  },
  S9: {
    station: 'S9',
    label: 'Integration',
    modality: 'epistemic',
    operation: 'U',
    group: 'G8'
  },
  S10: {
    station: 'S10',
    label: 'Reflection',
    modality: 'alethic',
    operation: 'N',
    group: 'G8'
  },
  S11: {
    station: 'S11',
    label: 'Resolution',
    modality: 'resolution',
    operation: 'Final',
    group: 'G9'
  }
};