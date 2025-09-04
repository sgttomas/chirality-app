import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { readFileSync } from 'fs';
import path from 'path';
import { createPacket } from '../src/domain/packet';
import { Exporter } from '../src/core/exporter';
import { initRunState, updateStation, addPacket, completeRun } from '../src/core/state';

describe('Schema Validation', () => {
  let ajv: Ajv;
  let packetSchema: any;

  beforeAll(() => {
    // Load and compile schema
    const schemaPath = path.join(__dirname, '../schemas/packet.json');
    const schemaContent = readFileSync(schemaPath, 'utf8');
    packetSchema = JSON.parse(schemaContent);
    
    ajv = new Ajv({ strict: false });
    addFormats(ajv);
    ajv.addSchema(packetSchema, 'packet');
  });

  describe('Packet Schema Validation', () => {
    it('should validate a valid S1 packet (J operation)', () => {
      const packet = createPacket('S1', 'problem', { J: 'Problem analysis output' });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(true);
      expect(validate!.errors).toBeNull();
    });

    it('should validate a valid S2 packet (DS operation)', () => {
      const packet = createPacket('S2', 'systematic', { DS: 'Data sheet content' });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(true);
      expect(validate!.errors).toBeNull();
    });

    it('should validate a valid S11 packet (Final operation)', () => {
      const packet = createPacket('S11', 'resolution', { Final: 'Final resolution content' });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(true);
      expect(validate!.errors).toBeNull();
    });

    it('should accept packet with any valid payload operation (schema allows all)', () => {
      // Note: Our current schema uses oneOf which allows any valid operation
      // This is by design for flexibility across stations
      const packet = createPacket('S2', 'systematic', { J: 'Any operation content' });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(true);
    });

    it('should reject packet with empty payload operation', () => {
      const packet = createPacket('S1', 'problem', { J: '' });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(false);
      expect(validate!.errors).toBeTruthy();
      expect(validate!.errors![0].message).toContain('fewer than 1 characters');
    });

    it('should reject packet with invalid station', () => {
      const invalidPacket = {
        ...createPacket('S1', 'problem', { J: 'Valid content' }),
        station: 'S99' // Invalid station
      };
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(invalidPacket);
      
      expect(valid).toBe(false);
      expect(validate!.errors).toBeTruthy();
    });

    it('should reject packet with invalid modality', () => {
      const invalidPacket = {
        ...createPacket('S1', 'problem', { J: 'Valid content' }),
        modality: 'invalid' // Invalid modality
      };
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(invalidPacket);
      
      expect(valid).toBe(false);
      expect(validate!.errors).toBeTruthy();
    });

    it('should reject packet with missing required fields', () => {
      const invalidPacket = {
        id: 'S1-test123',
        // Missing: createdAt, station, modality, payload
      };
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(invalidPacket);
      
      expect(valid).toBe(false);
      expect(validate!.errors).toBeTruthy();
      expect(validate!.errors!.length).toBeGreaterThan(0);
    });

    it('should reject packet with additional properties at root level', () => {
      const invalidPacket = {
        ...createPacket('S1', 'problem', { J: 'Valid content' }),
        extraProperty: 'not allowed'
      };
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(invalidPacket);
      
      expect(valid).toBe(false);
      expect(validate!.errors).toBeTruthy();
      expect(validate!.errors![0].keyword).toBe('additionalProperties');
    });

    it('should allow valid meta properties', () => {
      const packet = createPacket('S1', 'problem', { J: 'Valid content' }, {
        duration: 500,
        tokens: { prompt: 100, completion: 50, total: 150 },
        label: 'Problem Statement'
      });
      
      const validate = ajv.getSchema('packet');
      const valid = validate!(packet);
      
      expect(valid).toBe(true);
      expect(validate!.errors).toBeNull();
    });
  });

  describe('Exporter Integration with Schema Validation', () => {
    it('should export packets that validate against schema', async () => {
      // Create a complete run state
      let state = initRunState('run_test_1234567890_abc123', 'Test problem statement');
      
      // Add some packets
      const s1Packet = createPacket('S1', 'problem', { J: 'Problem analysis' });
      const s2Packet = createPacket('S2', 'systematic', { DS: 'Data sheet content' });
      const s11Packet = createPacket('S11', 'resolution', { Final: 'Final resolution' });
      
      state = addPacket(state, s1Packet);
      state = addPacket(state, s2Packet);
      state = addPacket(state, s11Packet);
      
      // Add station results
      state = updateStation(state, 'S1', 'Problem analysis', 100);
      state = updateStation(state, 'S2', 'Data sheet content', 200);
      state = updateStation(state, 'S11', 'Final resolution', 300);
      
      // Add a small delay to ensure different timestamps
      await new Promise(resolve => setTimeout(resolve, 10));
      
      // Complete the run (this sets endTime and totalDuration)
      state = completeRun(state);
      
      // Verify state has required fields before export
      expect(state.endTime).toBeDefined();
      expect(state.totalDuration).toBeDefined();
      expect(state.totalDuration).toBeGreaterThanOrEqual(0);
      
      // Export the run to a temporary directory
      const tempDir = path.join(__dirname, '../temp-test-runs');
      const exporter = new Exporter(tempDir);
      
      await exporter.writeRun(state);
      
      // Read back the packets and validate against schema
      const { packets } = await exporter.readRun(state.runId);
      
      const validate = ajv.getSchema('packet');
      
      for (const packet of packets) {
        const valid = validate!(packet);
        expect(valid).toBe(true);
        if (!valid) {
          console.error('Validation errors:', validate!.errors);
        }
      }
      
      // Clean up
      const { promises: fs } = require('fs');
      await fs.rm(tempDir, { recursive: true, force: true });
    });
  });

  describe('Schema Edge Cases', () => {
    it('should validate all supported station operations', () => {
      const operations = [
        { station: 'S1', modality: 'problem', payload: { J: 'Content' } },
        { station: 'S2', modality: 'systematic', payload: { DS: 'Content' } },
        { station: 'S3', modality: 'process', payload: { SP: 'Content' } },
        { station: 'S4', modality: 'epistemic', payload: { GD: 'Content' } },
        { station: 'S5', modality: 'epistemic', payload: { EC: 'Content' } },
        { station: 'S6', modality: 'process', payload: { P: 'Content' } },
        { station: 'S7', modality: 'epistemic', payload: { M: 'Content' } },
        { station: 'S8', modality: 'alethic', payload: { W: 'Content' } },
        { station: 'S9', modality: 'epistemic', payload: { U: 'Content' } },
        { station: 'S10', modality: 'alethic', payload: { N: 'Content' } },
        { station: 'S11', modality: 'resolution', payload: { Final: 'Content' } }
      ];

      const validate = ajv.getSchema('packet');
      
      for (const op of operations) {
        const packet = createPacket(
          op.station as any, 
          op.modality as any, 
          op.payload
        );
        
        const valid = validate!(packet);
        expect(valid).toBe(true);
        if (!valid) {
          console.error(`Failed for ${op.station}:`, validate!.errors);
        }
      }
    });
  });
});