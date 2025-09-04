import { promises as fs } from 'fs';
import path from 'path';
import { RunState } from './state';
import { Packet } from '../domain/packet';
import { Station } from '../domain/station';

export interface RunExport {
  runId: string;
  problemStatement: string;
  startTime: string;
  endTime: string;
  totalDuration: number;
  metadata: {
    stationCount: number;
    totalTokens: number;
    durations: Record<Station, number>;
    iterationNumber: number;
  };
  summary: {
    documentsGenerated: string[];
    resolution: string;
  };
}

export interface ExportResult {
  runJsonPath: string;
  packetsJsonlPath: string;
  filesWritten: number;
  totalBytes: number;
}

export interface ExportOptions {
  runsDir?: string;
  ensureDirExists?: boolean;
}

export class Exporter {
  private runsDir: string;

  constructor(runsDir: string = 'runs') {
    this.runsDir = path.resolve(runsDir);
  }

  async writeRun(state: RunState, options: ExportOptions = {}): Promise<ExportResult> {
    const {
      ensureDirExists = true
    } = options;

    if (!state.endTime || !state.totalDuration) {
      throw new Error('Cannot export incomplete run. State must have endTime and totalDuration.');
    }

    const runDir = path.join(this.runsDir, state.runId);
    const runJsonPath = path.join(runDir, 'run.json');
    const packetsJsonlPath = path.join(runDir, 'packets.jsonl');

    // Ensure directory exists
    if (ensureDirExists) {
      await fs.mkdir(runDir, { recursive: true });
    }

    // Calculate metadata
    const totalTokens = state.stationResults.reduce((sum, result) => {
      return sum + (result.tokens?.total || 0);
    }, 0);

    const durations = state.stationResults.reduce((acc, result) => {
      acc[result.station] = result.duration;
      return acc;
    }, {} as Record<Station, number>);

    const documentsGenerated = [];
    if (state.documents.dataSheet) documentsGenerated.push('Data Sheet');
    if (state.documents.standardProcedure) documentsGenerated.push('Standard Procedure');
    if (state.documents.guidanceDocument) documentsGenerated.push('Guidance Document');
    if (state.documents.evaluationChecklist) documentsGenerated.push('Evaluation Checklist');
    if (state.documents.solutionStatements) documentsGenerated.push('Solution Statements');

    // Find resolution from S11 packet
    const s11Packet = state.packets.find(p => p.station === 'S11');
    const resolution = s11Packet?.payload?.Final || 'No resolution generated';

    // Create run summary
    const runExport: RunExport = {
      runId: state.runId,
      problemStatement: state.problemStatement,
      startTime: state.startTime,
      endTime: state.endTime,
      totalDuration: state.totalDuration,
      metadata: {
        stationCount: state.packets.length,
        totalTokens,
        durations,
        iterationNumber: state.iterationNumber
      },
      summary: {
        documentsGenerated,
        resolution
      }
    };

    // Write run.json
    const runJsonContent = JSON.stringify(runExport, null, 2);
    await fs.writeFile(runJsonPath, runJsonContent, 'utf8');

    // Write packets.jsonl (one packet per line)
    const packetsJsonlLines = state.packets.map(packet => JSON.stringify(packet));
    const packetsJsonlContent = packetsJsonlLines.join('\n') + '\n';
    await fs.writeFile(packetsJsonlPath, packetsJsonlContent, 'utf8');

    // Calculate total bytes
    const runJsonStats = await fs.stat(runJsonPath);
    const packetsJsonlStats = await fs.stat(packetsJsonlPath);
    const totalBytes = runJsonStats.size + packetsJsonlStats.size;

    console.log(`[Exporter] Exported run ${state.runId}:`, {
      runJsonSize: runJsonStats.size,
      packetsJsonlSize: packetsJsonlStats.size,
      totalBytes,
      packetCount: state.packets.length
    });

    return {
      runJsonPath,
      packetsJsonlPath,
      filesWritten: 2,
      totalBytes
    };
  }

  async readRun(runId: string): Promise<{ runExport: RunExport; packets: Packet[] }> {
    const runDir = path.join(this.runsDir, runId);
    const runJsonPath = path.join(runDir, 'run.json');
    const packetsJsonlPath = path.join(runDir, 'packets.jsonl');

    try {
      // Read run.json
      const runJsonContent = await fs.readFile(runJsonPath, 'utf8');
      const runExport: RunExport = JSON.parse(runJsonContent);

      // Read packets.jsonl
      const packetsJsonlContent = await fs.readFile(packetsJsonlPath, 'utf8');
      const packets: Packet[] = packetsJsonlContent
        .trim()
        .split('\n')
        .filter(line => line.trim())
        .map(line => JSON.parse(line));

      return { runExport, packets };

    } catch (error) {
      throw new Error(`Failed to read run ${runId}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async listRuns(): Promise<string[]> {
    try {
      const entries = await fs.readdir(this.runsDir, { withFileTypes: true });
      const runIds = entries
        .filter(entry => entry.isDirectory() && entry.name.startsWith('run_'))
        .map(entry => entry.name)
        .sort();

      return runIds;
    } catch (error) {
      if ((error as any).code === 'ENOENT') {
        return [];
      }
      throw error;
    }
  }

  async runExists(runId: string): Promise<boolean> {
    const runDir = path.join(this.runsDir, runId);
    const runJsonPath = path.join(runDir, 'run.json');
    const packetsJsonlPath = path.join(runDir, 'packets.jsonl');

    try {
      await Promise.all([
        fs.access(runJsonPath),
        fs.access(packetsJsonlPath)
      ]);
      return true;
    } catch {
      return false;
    }
  }

  async getRunSize(runId: string): Promise<{ runJson: number; packetsJsonl: number; total: number }> {
    const runDir = path.join(this.runsDir, runId);
    const runJsonPath = path.join(runDir, 'run.json');
    const packetsJsonlPath = path.join(runDir, 'packets.jsonl');

    try {
      const [runJsonStats, packetsJsonlStats] = await Promise.all([
        fs.stat(runJsonPath),
        fs.stat(packetsJsonlPath)
      ]);

      return {
        runJson: runJsonStats.size,
        packetsJsonl: packetsJsonlStats.size,
        total: runJsonStats.size + packetsJsonlStats.size
      };
    } catch (error) {
      throw new Error(`Failed to get size for run ${runId}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }
}