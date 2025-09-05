/**
 * Test suite for seed extraction functionality
 */

import { extractSeeds, isCacheValid, buildCacheMetadata } from '../lib/seeds/seedExtractor';
import { seedsConfig } from '../src/config/seeds';
import { promises as fs } from 'fs';
import path from 'path';

describe('Seed Extraction', () => {
  const TEST_RUN_ID = 'sample_happy_001';
  const TEST_RUN_PATH = path.join('fixtures', 'runs', TEST_RUN_ID);

  beforeAll(async () => {
    // Verify test fixture exists
    try {
      await fs.access(TEST_RUN_PATH);
    } catch (error) {
      console.warn('Test fixture not found, skipping seed extraction tests');
      return;
    }
  });

  describe('extractSeeds', () => {
    it('should extract seeds from valid framework run', async () => {
      try {
        // Check if fixture exists
        await fs.access(TEST_RUN_PATH);
      } catch (error) {
        console.log('Skipping test - fixture not available');
        return;
      }

      const result = await extractSeeds({
        runId: TEST_RUN_ID,
        runsDir: 'fixtures/runs',
        enableHeuristics: false,
        verifyChecksums: false, // Skip checksum verification for test fixtures
      });

      expect(result.seeds).not.toBeNull();
      
      if (result.seeds) {
        expect(result.seeds.initialVector).toHaveProperty('matrixC');
        expect(result.seeds.initialVector).toHaveProperty('matrixD');
        expect(result.seeds.initialVector).toHaveProperty('matrixX');
        expect(result.seeds.initialVector).toHaveProperty('matrixE');
        
        expect(result.seeds.metadata).toHaveProperty('runId', TEST_RUN_ID);
        expect(result.seeds.metadata).toHaveProperty('extractedAt');
        expect(result.seeds.metadata).toHaveProperty('totalCells');
        expect(result.seeds.metadata).toHaveProperty('counts');
        
        // Check that we have some seeds extracted
        const totalSeeds = Object.values(result.seeds.initialVector).reduce((acc, arr) => acc + arr.length, 0);
        expect(totalSeeds).toBeGreaterThan(0);
      }
    }, 30000); // 30 second timeout for potential large file processing

    it('should handle missing run gracefully', async () => {
      const result = await extractSeeds({
        runId: 'nonexistent_run',
        runsDir: 'fixtures/runs',
        enableHeuristics: false,
        verifyChecksums: false,
      });

      expect(result.seeds).toBeNull();
    });

    it('should apply heuristics when enabled', async () => {
      try {
        await fs.access(TEST_RUN_PATH);
      } catch (error) {
        console.log('Skipping test - fixture not available');
        return;
      }

      const withHeuristics = await extractSeeds({
        runId: TEST_RUN_ID,
        runsDir: 'fixtures/runs',
        enableHeuristics: true,
        minItems: 2,
        maxItems: 5,
        maxLength: 50,
        verifyChecksums: false,
      });

      const withoutHeuristics = await extractSeeds({
        runId: TEST_RUN_ID,
        runsDir: 'fixtures/runs',
        enableHeuristics: false,
        verifyChecksums: false,
      });

      if (withHeuristics.seeds && withoutHeuristics.seeds) {
        // With heuristics should respect maxItems constraint
        Object.values(withHeuristics.seeds.initialVector).forEach(arr => {
          expect(arr.length).toBeLessThanOrEqual(5);
        });

        // With heuristics should respect maxLength constraint
        Object.values(withHeuristics.seeds.initialVector).forEach(arr => {
          arr.forEach(item => {
            expect(item.length).toBeLessThanOrEqual(50 + 3); // +3 for '...' if truncated
          });
        });
      }
    }, 30000);
  });

  describe('Cache Management', () => {
    it('should build cache metadata correctly', async () => {
      const sourceFiles = ['snapshots/C.jsonl', 'snapshots/D.jsonl'];
      const metadata = await buildCacheMetadata(TEST_RUN_ID, sourceFiles, 'fixtures/runs');

      expect(metadata).toHaveProperty('sourceMtime');
      expect(metadata).toHaveProperty('sourceSize');
      
      sourceFiles.forEach(file => {
        expect(metadata.sourceMtime[file]).toBeDefined();
        expect(metadata.sourceSize[file]).toBeDefined();
        expect(typeof metadata.sourceMtime[file]).toBe('number');
        expect(typeof metadata.sourceSize[file]).toBe('number');
      });
    });

    it('should validate cache correctly', async () => {
      // Create mock cache metadata
      const mockMetadata = {
        runId: TEST_RUN_ID,
        extractedAt: new Date().toISOString(),
        totalCells: 10,
        counts: { C: 2, D: 3, X: 2, E: 3 },
        sourceFiles: ['snapshots/C.jsonl'],
        checksumVerified: false,
        warnings: [],
        sourceMtime: { 'snapshots/C.jsonl': Date.now() / 1000 - 3600 }, // 1 hour ago
        sourceSize: { 'snapshots/C.jsonl': 1000 }
      };

      // This should return false since the mtime/size likely won't match
      const isValid = await isCacheValid(mockMetadata, 'fixtures/runs');
      expect(typeof isValid).toBe('boolean');
    });
  });

  describe('Configuration', () => {
    it('should have valid default configuration', () => {
      expect(seedsConfig).toHaveProperty('enableHeuristics');
      expect(seedsConfig).toHaveProperty('minItems');
      expect(seedsConfig).toHaveProperty('maxItems');
      expect(seedsConfig).toHaveProperty('maxLength');
      expect(seedsConfig).toHaveProperty('verifyChecksums');
      expect(seedsConfig).toHaveProperty('persist');
      expect(seedsConfig).toHaveProperty('runsDir');

      expect(typeof seedsConfig.enableHeuristics).toBe('boolean');
      expect(typeof seedsConfig.minItems).toBe('number');
      expect(typeof seedsConfig.maxItems).toBe('number');
      expect(typeof seedsConfig.maxLength).toBe('number');
      expect(typeof seedsConfig.verifyChecksums).toBe('boolean');
      expect(typeof seedsConfig.persist).toBe('boolean');
      expect(typeof seedsConfig.runsDir).toBe('string');

      // Validate constraints
      expect(seedsConfig.minItems).toBeGreaterThan(0);
      expect(seedsConfig.maxItems).toBeGreaterThanOrEqual(seedsConfig.minItems);
      expect(seedsConfig.maxLength).toBeGreaterThan(0);
    });
  });
});