/**
 * Tests for the new /api/pipeline/traverse endpoint
 */

import { POST, GET } from '../src/app/api/pipeline/traverse/route';
import { NextRequest } from 'next/server';

describe('/api/pipeline/traverse', () => {
  const createMockRequest = (body: any): NextRequest => {
    return {
      json: async () => body,
      headers: new Headers(),
      url: 'http://localhost:3001/api/pipeline/traverse',
      method: 'POST'
    } as NextRequest;
  };
  
  describe('Feature Flag Gating', () => {
    it('should reject when NEW_PIPELINE_ENABLED is false', async () => {
      // Ensure flag is disabled
      const originalFlag = process.env.NEW_PIPELINE_ENABLED;
      process.env.NEW_PIPELINE_ENABLED = 'false';
      
      const request = createMockRequest({
        problem: { title: 'Test', statement: 'Test problem' }
      });
      
      const response = await POST(request);
      const data = await response.json();
      
      expect(response.status).toBe(503);
      expect(data.error).toContain('not enabled');
      
      // Restore original flag
      process.env.NEW_PIPELINE_ENABLED = originalFlag;
    });
    
    it('should accept when NEW_PIPELINE_ENABLED is true', async () => {
      // Enable flag for this test
      const originalFlag = process.env.NEW_PIPELINE_ENABLED;
      process.env.NEW_PIPELINE_ENABLED = 'true';
      
      const request = createMockRequest({
        problem: { title: 'Test', statement: 'Test problem' }
      });
      
      const response = await POST(request);
      const data = await response.json();
      
      // Should not be rejected by feature flag
      expect(response.status).not.toBe(503);
      expect(data.traversalId).toBeDefined();
      
      // Restore original flag
      process.env.NEW_PIPELINE_ENABLED = originalFlag;
    });
  });
  
  describe('Request Validation', () => {
    beforeEach(() => {
      process.env.NEW_PIPELINE_ENABLED = 'true';
    });
    
    afterEach(() => {
      delete process.env.NEW_PIPELINE_ENABLED;
    });
    
    it('should validate required problem fields', async () => {
      const invalidRequests = [
        {},  // missing problem
        { problem: {} },  // missing title and statement
        { problem: { title: 'Test' } },  // missing statement
        { problem: { statement: 'Test' } }  // missing title
      ];
      
      for (const invalidBody of invalidRequests) {
        const request = createMockRequest(invalidBody);
        const response = await POST(request);
        
        expect(response.status).toBe(400);
        const data = await response.json();
        expect(data.error).toContain('required');
      }
    });
    
    it('should accept valid problem structure', async () => {
      const request = createMockRequest({
        problem: { 
          title: 'Valid Test Problem',
          statement: 'This is a valid test problem statement'
        }
      });
      
      const response = await POST(request);
      expect(response.status).toBe(200);
      
      const data = await response.json();
      expect(data.traversalId).toBeDefined();
      expect(data.stations).toBeDefined();
      expect(data.resolution).toBeDefined();
      expect(data.metadata).toBeDefined();
    });
  });
  
  describe('API Response Structure', () => {
    beforeEach(() => {
      process.env.NEW_PIPELINE_ENABLED = 'true';
    });
    
    afterEach(() => {
      delete process.env.NEW_PIPELINE_ENABLED;
    });
    
    it('should return correct response structure', async () => {
      const request = createMockRequest({
        problem: { 
          title: 'Test Problem',
          statement: 'Test statement'
        },
        startStation: 'S0',
        endStation: 'S2'
      });
      
      const response = await POST(request);
      const data = await response.json();
      
      // Check response structure matches specification
      expect(data).toHaveProperty('traversalId');
      expect(data).toHaveProperty('stations');
      expect(data).toHaveProperty('resolution');
      expect(data).toHaveProperty('metadata');
      
      // Check metadata structure
      expect(data.metadata).toHaveProperty('durationMs');
      expect(data.metadata).toHaveProperty('matrixInjections');
      expect(typeof data.metadata.durationMs).toBe('number');
      expect(Array.isArray(data.metadata.matrixInjections)).toBe(true);
      
      // Check that only requested stations are populated
      expect(data.stations.S0).toBeDefined();
      expect(data.stations.S1).toBeDefined();
      expect(data.stations.S2).toBeDefined();
      expect(data.stations.S3).toBeUndefined();
    });
    
    it('should handle matrix injections', async () => {
      const request = createMockRequest({
        problem: { 
          title: 'Test Problem',
          statement: 'Test statement'
        },
        matrices: {
          C: [{ test: 'requirements matrix' }],
          D: [{ test: 'objectives matrix' }]
        },
        startStation: 'S1',
        endStation: 'S2'
      });
      
      const response = await POST(request);
      const data = await response.json();
      
      // Should report matrix injections
      expect(data.metadata.matrixInjections).toContain('C');
      expect(data.metadata.matrixInjections).toContain('D');
    });
  });
  
  describe('GET endpoint', () => {
    it('should return pipeline configuration', async () => {
      const response = await GET();
      const data = await response.json();
      
      expect(data).toHaveProperty('pipelineEnabled');
      expect(data).toHaveProperty('version');
      expect(data).toHaveProperty('stations');
      expect(data).toHaveProperty('modalities');
      expect(data).toHaveProperty('matrixInjectionPoints');
      
      expect(data.stations).toHaveLength(9);
      expect(data.stations).toContain('S0');
      expect(data.stations).toContain('S8');
    });
  });
});