import { NextRequest } from 'next/server';
import { POST as traversePost } from '../src/app/api/pipeline/traverse/route';
import { GET as exportGet } from '../src/app/api/export/run/route';

// Mock the orchestrator for testing
jest.mock('../src/core/orchestrator', () => ({
  createOrchestrator: jest.fn(() => Promise.resolve({
    runTraversal: jest.fn(() => Promise.resolve({
      runId: 'run_1234567890_abc123',
      packets: [
        {
          station: 'S1',
          modality: 'problem',
          payload: { J: 'Problem analysis output' },
          meta: { duration: 100, label: 'Problem Statement' }
        },
        {
          station: 'S2', 
          modality: 'systematic',
          payload: { DS: 'Data sheet output' },
          meta: { duration: 200, label: 'Data Sheet' }
        },
        {
          station: 'S11',
          modality: 'resolution', 
          payload: { Final: 'Final resolution output' },
          meta: { duration: 500, label: 'Resolution' }
        }
      ],
      resolution: 'Final resolution output',
      metadata: {
        durations: { S1: 100, S2: 200, S11: 500 },
        totalDuration: 800,
        totalTokens: 150
      }
    }))
  }))
}));

describe('API Endpoints', () => {
  describe('POST /api/pipeline/traverse', () => {
    it('should successfully process a valid traversal request', async () => {
      const requestBody = {
        problem: {
          title: 'Test Problem',
          statement: 'How can we improve team collaboration?'
        }
      };

      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const response = await traversePost(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.traversalId).toBe('run_1234567890_abc123');
      expect(data.stations).toHaveLength(3);
      expect(data.resolution).toBe('Final resolution output');
      expect(data.metadata.totalDuration).toBe(800);
      expect(data.metadata.totalTokens).toBe(150);
    });

    it('should successfully process a foundation mode traversal request', async () => {
      const requestBody = {
        problem: {
          title: 'Test Problem',
          statement: 'How can we improve team collaboration?'
        },
        options: {
          mode: 'foundation' as const
        }
      };

      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const response = await traversePost(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.traversalId).toBe('run_1234567890_abc123');
      expect(data.stations).toHaveLength(3); // Should be same as mock
      expect(data.resolution).toBe('Final resolution output');
    });

    it('should return 400 for missing problem statement', async () => {
      const requestBody = {
        problem: {
          title: 'Test Problem'
          // Missing statement
        }
      };

      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST', 
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const response = await traversePost(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.code).toBe('ERR_MISSING_FIELDS');
      expect(data.message).toContain('problem.title and problem.statement are required');
    });

    it('should return 400 for empty problem statement', async () => {
      const requestBody = {
        problem: {
          title: 'Test Problem',
          statement: '   ' // Empty/whitespace only
        }
      };

      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const response = await traversePost(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.code).toBe('ERR_EMPTY_STATEMENT');
      expect(data.message).toContain('problem.statement cannot be empty');
    });

    it('should return 400 for invalid JSON', async () => {
      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST',
        body: 'invalid json{',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const response = await traversePost(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.code).toBe('ERR_INVALID_JSON');
      expect(data.message).toBe('Invalid JSON in request body');
    });
  });

  describe('GET /api/export/run', () => {
    it('should return 400 for missing runId', async () => {
      const request = new NextRequest('http://localhost:3000/api/export/run');

      const response = await exportGet(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.code).toBe('ERR_MISSING_RUN_ID');
      expect(data.message).toContain('Missing required query parameter: runId');
    });

    it('should return 400 for invalid runId format', async () => {
      const request = new NextRequest('http://localhost:3000/api/export/run?runId=invalid_format');

      const response = await exportGet(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.code).toBe('ERR_INVALID_RUN_ID');
      expect(data.message).toContain('Invalid runId format');
    });

    it('should return 404 for non-existent run', async () => {
      const request = new NextRequest('http://localhost:3000/api/export/run?runId=run_1234567890_nonexist');

      const response = await exportGet(request);
      const data = await response.json();

      expect(response.status).toBe(404);
      expect(data.code).toBe('ERR_RUN_NOT_FOUND');
      expect(data.message).toContain('Run run_1234567890_nonexist not found');
    });
  });
});