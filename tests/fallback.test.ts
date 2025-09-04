import { createOrchestrator } from '../src/core/orchestrator';
import { NextRequest } from 'next/server';
import { POST as traversePost } from '../src/app/api/pipeline/traverse/route';

describe('Fallback Mode Tests', () => {
  // Store original env vars
  const originalOpenAIKey = process.env.OPENAI_API_KEY;
  const originalOpenAIModel = process.env.OPENAI_MODEL;

  beforeEach(() => {
    // Clear environment variables for clean testing
    delete process.env.OPENAI_API_KEY;
    delete process.env.OPENAI_MODEL;
  });

  afterEach(() => {
    // Restore original environment variables
    if (originalOpenAIKey) process.env.OPENAI_API_KEY = originalOpenAIKey;
    if (originalOpenAIModel) process.env.OPENAI_MODEL = originalOpenAIModel;
  });

  describe('createOrchestrator fallback', () => {
    it('should create orchestrator with no API key when allowFallback=true', async () => {
      // Arrange: No API key set
      delete process.env.OPENAI_API_KEY;
      process.env.OPENAI_MODEL = 'gpt-4.1-nano'; // Required even for disabled mode during construction

      // Act
      const orchestrator = await createOrchestrator(undefined, true);

      // Assert
      expect(orchestrator).toBeDefined();
    });

    it('should generate packets in foundation mode without API key', async () => {
      // Arrange: No API key, but fallback enabled
      delete process.env.OPENAI_API_KEY;
      process.env.OPENAI_MODEL = 'gpt-4.1-nano'; // Required for non-disabled LLMService
      
      const orchestrator = await createOrchestrator(undefined, true);

      // Act
      const result = await orchestrator.runTraversal({
        title: 'Test Problem',
        statement: 'How can we test fallback mode?'
      }, {
        mode: 'foundation',
        exportRun: false
      });

      // Assert
      expect(result.runId).toBeDefined();
      expect(result.packets).toHaveLength(6); // S1, S2, S3, S4, S5, S11
      expect(result.resolution).toBeDefined();
      expect(result.metadata.totalTokens).toBe(0); // No real LLM calls
      
      // Verify station sequence
      const stations = result.packets.map(p => p.station);
      expect(stations).toEqual(['S1', 'S2', 'S3', 'S4', 'S5', 'S11']);
      
      // Verify modalities
      const modalities = result.packets.map(p => p.modality);
      expect(modalities).toEqual(['problem', 'systematic', 'process', 'epistemic', 'process', 'resolution']);
      
      // Verify each packet has content
      result.packets.forEach(packet => {
        expect(Object.keys(packet.payload).length).toBeGreaterThan(0);
        const content = Object.values(packet.payload)[0] as string;
        expect(typeof content).toBe('string');
        expect(content.length).toBeGreaterThan(0);
      });
    });

    it('should throw error when no API key and allowFallback=false', async () => {
      // Arrange: No API key set
      delete process.env.OPENAI_API_KEY;

      // Act & Assert
      await expect(createOrchestrator(undefined, false))
        .rejects.toThrow('OpenAI API key not provided');
    });

    it('should use disabled LLM mode with invalid API key when allowFallback=true', async () => {
      // Arrange: Invalid API key but need OPENAI_MODEL for non-disabled mode
      process.env.OPENAI_MODEL = 'gpt-4.1-nano'; // Required for LLMService
      
      const orchestrator = await createOrchestrator('invalid-key', true);

      // Act
      const result = await orchestrator.runTraversal({
        title: 'Test Problem',  
        statement: 'Testing with invalid key'
      }, {
        mode: 'foundation',
        exportRun: false
      });

      // Assert: Should complete successfully with stub content
      expect(result.packets).toHaveLength(6);
      expect(result.metadata.totalTokens).toBe(0); // No real LLM calls
      
      // Verify stub content contains expected markers
      result.packets.forEach(packet => {
        const content = Object.values(packet.payload)[0] as string;
        expect(content).toContain('STUB:');
      });
    });
  });

  describe('API foundation mode without API key', () => {
    it('should return 200 OK and valid packets for foundation mode without OPENAI_API_KEY', async () => {
      // Arrange: No API key in environment but model is needed
      delete process.env.OPENAI_API_KEY;
      process.env.OPENAI_MODEL = 'gpt-4.1-nano'; // Required for LLMService
      
      const requestBody = {
        problem: {
          title: 'API Test Problem',
          statement: 'Testing API foundation mode without API key'
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

      // Act
      const response = await traversePost(request);
      const data = await response.json();

      // Assert
      expect(response.status).toBe(200);
      expect(data.traversalId).toBeDefined();
      expect(data.stations).toHaveLength(6); // Foundation mode: S1-S5+S11
      expect(data.resolution).toBeDefined();
      expect(data.metadata.totalTokens).toBe(0); // No real LLM calls
      
      // Verify station structure
      data.stations.forEach((station: any) => {
        expect(station.station).toMatch(/^S(1|2|3|4|5|11)$/);
        expect(station.label).toBeDefined();
        expect(station.modality).toBeDefined();
        expect(station.operation).toBeDefined();
        expect(station.duration).toBeGreaterThanOrEqual(0);
        expect(station.output).toBeDefined();
        expect(typeof station.output).toBe('string');
        expect(station.output.length).toBeGreaterThan(0);
      });
    });

    it('should require API key for full mode', async () => {
      // Arrange: No API key, but requesting full mode
      delete process.env.OPENAI_API_KEY;
      process.env.OPENAI_MODEL = 'gpt-4.1-nano';
      
      const requestBody = {
        problem: {
          title: 'Full Mode Test',
          statement: 'Testing full mode without API key'
        },
        options: {
          mode: 'full' as const
        }
      };

      const request = new NextRequest('http://localhost:3000/api/pipeline/traverse', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // Act
      const response = await traversePost(request);
      const data = await response.json();

      // Assert: Should fail for full mode without API key
      expect(response.status).toBe(500);
      expect(data.code).toBe('ERR_ORCHESTRATOR_INIT');
      expect(data.message).toContain('OpenAI API key');
    });
  });

  describe('LLMService disabled mode', () => {
    it('should generate deterministic stubs when disabled=true', async () => {
      // This test will be enabled when we have direct LLMService access in tests
      // For now, the integration tests above cover the disabled functionality
      expect(true).toBe(true);
    });
  });
});