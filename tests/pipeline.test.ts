/**
 * Tests for the semantic valley traversal pipeline skeleton
 */

import { runStation, runTraversal, runCompatibilityMode } from '../lib/orchestrator/pipeline';
import { StationId } from '../lib/orchestrator/prompts/station-template';
import { isPacket } from '../lib/utils/packets';

describe('Pipeline Skeleton', () => {
  const testProblem = {
    title: 'Test Problem',
    statement: 'This is a test problem statement for the pipeline'
  };
  
  describe('Individual Stations', () => {
    const stations: StationId[] = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'];
    
    stations.forEach(stationId => {
      it(`should run station ${stationId} without error`, async () => {
        const input = {
          problem: testProblem,
          previousStations: {},
          matrixInjection: undefined
        };
        
        const result = await runStation(stationId, input);
        expect(result).toBeDefined();
        
        // S0 returns normalized string, others return Packets
        if (stationId === 'S0') {
          expect(result.normalized).toBeDefined();
        } else {
          expect(isPacket(result)).toBe(true);
        }
      });
    });
  });
  
  describe('Full Traversal', () => {
    it('should complete a full traversal from S0 to S8', async () => {
      const state = await runTraversal(testProblem);
      
      expect(state.problemId).toBeDefined();
      expect(state.problem).toEqual(testProblem);
      expect(state.currentStation).toBe('S8');
      expect(state.stations.S0).toBeDefined();
      expect(state.stations.S8).toBeDefined();
      expect(state.metadata?.endTime).toBeDefined();
    });
    
    it('should support partial traversal', async () => {
      const state = await runTraversal(testProblem, {
        startStation: 'S1',
        endStation: 'S3'
      });
      
      expect(state.stations.S0).toBeUndefined();
      expect(state.stations.S1).toBeDefined();
      expect(state.stations.S2).toBeDefined();
      expect(state.stations.S3).toBeDefined();
      expect(state.stations.S4).toBeUndefined();
    });
    
    it('should handle matrix injection', async () => {
      const matrices = {
        'C': { test: 'requirements matrix' },
        'D': { test: 'objectives matrix' }
      };
      
      const state = await runTraversal(testProblem, {
        matrices,
        startStation: 'S1',
        endStation: 'S2'
      });
      
      expect(state.metadata?.matrixInjections).toContain('C');
      expect(state.metadata?.matrixInjections).toContain('D');
    });
    
    it('should call progress callback', async () => {
      const progressStates: string[] = [];
      
      await runTraversal(testProblem, {
        startStation: 'S0',
        endStation: 'S2',
        onProgress: (state) => {
          progressStates.push(state.currentStation);
        }
      });
      
      expect(progressStates).toEqual(['S0', 'S1', 'S2']);
    });
  });
  
  describe('Compatibility Mode', () => {
    it('should run V1 compatibility mode', async () => {
      const results = await runCompatibilityMode('V1', testProblem);
      
      // V1 maps to S1, S2, S3
      expect(results.S1).toBeDefined();
      expect(results.S2).toBeDefined();
      expect(results.S3).toBeDefined();
      
      // Should also have document type mappings
      expect(results.DS).toBeDefined(); // S1 → DS
      expect(results.SP).toBeDefined(); // S2 → SP
      expect(results.X).toBeDefined();  // S3 → X
    });
    
    it('should run V2 compatibility mode', async () => {
      const results = await runCompatibilityMode('V2', testProblem);
      
      // V2 maps to S4, S5, S6
      expect(results.S4).toBeDefined();
      expect(results.S5).toBeDefined();
      expect(results.S6).toBeDefined();
      
      // Document mappings
      expect(results.SP).toBeDefined(); // S4 → SP
      expect(results.X).toBeDefined();  // S5 → X
      expect(results.M).toBeDefined();  // S6 → M
    });
    
    it('should run V3 compatibility mode', async () => {
      const results = await runCompatibilityMode('V3', testProblem);
      
      // V3 maps to S7, S8
      expect(results.S7).toBeDefined();
      expect(results.S8).toBeDefined();
      
      // Document mappings
      expect(results.X).toBeDefined();  // S7 → X
      expect(results.M).toBeDefined();  // S8 → M
    });
  });
  
  describe('Risk Assessment', () => {
    it('should set risk flag only in alethic stations (S6, S8)', async () => {
      const state = await runTraversal(testProblem);
      
      // S6 and S8 should have risk flags
      expect(state.stations.S6?.flags?.risk).toBeDefined();
      expect(state.stations.S8?.flags?.risk).toBeDefined();
      
      // Other stations should not have risk flags
      expect(state.stations.S1?.flags?.risk).toBeUndefined();
      expect(state.stations.S2?.flags?.risk).toBeUndefined();
      expect(state.stations.S3?.flags?.risk).toBeUndefined();
      expect(state.stations.S4?.flags?.risk).toBeUndefined();
      expect(state.stations.S5?.flags?.risk).toBeUndefined();
      expect(state.stations.S7?.flags?.risk).toBeUndefined();
    });
  });
  
  describe('Error Handling', () => {
    it('should reject invalid station ranges', async () => {
      await expect(
        runTraversal(testProblem, {
          startStation: 'S5',
          endStation: 'S2'
        })
      ).rejects.toThrow('Invalid station range');
    });
    
    it('should handle station failures gracefully', async () => {
      // This will be tested more thoroughly once stations have real implementation
      // For now, just verify the structure is in place
      expect(runStation).toBeDefined();
      expect(runTraversal).toBeDefined();
    });
  });
});