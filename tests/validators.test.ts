import {
  assertStationTransition,
  assertOrder,
  assertDataDeps,
  createValidationError
} from '../src/domain/validators';
import { createPacket } from '../src/domain/packet';

describe('Validators', () => {
  describe('createValidationError', () => {
    it('should create error with code and details', () => {
      const error = createValidationError('ERR_TEST', 'test message', { key: 'value' });
      
      expect(error.code).toBe('ERR_TEST');
      expect(error.message).toBe('test message');
      expect(error.details).toEqual({ key: 'value' });
    });
  });

  describe('assertStationTransition', () => {
    it('should allow null to S1 transition', () => {
      expect(() => assertStationTransition(null, 'S1')).not.toThrow();
    });

    it('should reject null to non-S1 transition', () => {
      expect(() => assertStationTransition(null, 'S2')).toThrow('First station must be S1');
    });

    it('should allow valid sequential transitions', () => {
      expect(() => assertStationTransition('S1', 'S2')).not.toThrow();
      expect(() => assertStationTransition('S5', 'S6')).not.toThrow();
      expect(() => assertStationTransition('S10', 'S11')).not.toThrow();
    });

    it('should reject invalid transitions', () => {
      expect(() => assertStationTransition('S1', 'S3')).toThrow('Invalid station transition');
      expect(() => assertStationTransition('S5', 'S8')).toThrow('Invalid station transition');
    });
  });

  describe('assertOrder', () => {
    it('should validate correct packet sequence', () => {
      const packets = [
        createPacket('S1', 'problem', { J: 'problem' }),
        createPacket('S2', 'systematic', { D: 'requirements' }),
        createPacket('S3', 'process', { C: 'objectives' })
      ];

      expect(() => assertOrder(packets)).not.toThrow();
    });

    it('should reject incorrect packet sequence', () => {
      const packets = [
        createPacket('S1', 'problem', { J: 'problem' }),
        createPacket('S3', 'process', { C: 'objectives' })
      ];

      expect(() => assertOrder(packets)).toThrow('Invalid station transition');
    });
  });

  describe('assertDataDeps', () => {
    it('should validate foundation mode dependency chain (S1-S5+S11)', () => {
      const validFoundationPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' }),
        createPacket('S3', 'process', { SP: 'standard procedure' }),
        createPacket('S4', 'epistemic', { GD: 'guidance document' }),
        createPacket('S5', 'process', { EC: 'evaluation checklist' }),
        createPacket('S11', 'resolution', { Final: 'resolution' })
      ];

      expect(() => assertDataDeps(validFoundationPackets)).not.toThrow();
    });

    it('should validate S2 depends on J from S1', () => {
      const validPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' })
      ];

      expect(() => assertDataDeps(validPackets)).not.toThrow();

      const invalidPackets = [
        createPacket('S1', 'problem', { other: 'data' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' })
      ];

      expect(() => assertDataDeps(invalidPackets)).toThrow('S2 (Data Sheet) requires J operation from S1');
    });

    it('should validate S3 depends on DS from S2', () => {
      const validPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' }),
        createPacket('S3', 'process', { SP: 'standard procedure' })
      ];

      expect(() => assertDataDeps(validPackets)).not.toThrow();

      const invalidPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { other: 'data' }),
        createPacket('S3', 'process', { SP: 'standard procedure' })
      ];

      expect(() => assertDataDeps(invalidPackets)).toThrow('S3 (Standard Procedure) requires DS operation from S2');
    });

    it('should validate S5 depends on GD from S4', () => {
      const validPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' }),
        createPacket('S3', 'process', { SP: 'standard procedure' }),
        createPacket('S4', 'epistemic', { GD: 'guidance document' }),
        createPacket('S5', 'process', { EC: 'evaluation checklist' })
      ];

      expect(() => assertDataDeps(validPackets)).not.toThrow();

      const invalidPackets = [
        createPacket('S1', 'problem', { J: 'problem analysis' }),
        createPacket('S2', 'systematic', { DS: 'data sheet' }),
        createPacket('S3', 'process', { SP: 'standard procedure' }),
        createPacket('S4', 'epistemic', { other: 'data' }),
        createPacket('S5', 'process', { EC: 'evaluation checklist' })
      ];

      expect(() => assertDataDeps(invalidPackets)).toThrow('S5 (Evaluation Checklist) requires GD operation from S4');
    });

    it('should validate S11 foundation mode depends on EC from S5', () => {
      // Test only S5 and S11 (foundation mode direct jump)
      const validFoundationPackets = [
        createPacket('S5', 'process', { EC: 'evaluation checklist' }),
        createPacket('S11', 'resolution', { Final: 'resolution' })
      ];

      expect(() => assertDataDeps(validFoundationPackets)).not.toThrow();

      const invalidFoundationPackets = [
        createPacket('S5', 'process', { other: 'data' }),
        createPacket('S11', 'resolution', { Final: 'resolution' })
      ];

      expect(() => assertDataDeps(invalidFoundationPackets)).toThrow('S11 (Resolution) in foundation mode requires EC operation from S5');
    });

    it('should pass when dependent stations are not present', () => {
      const packets = [
        createPacket('S1', 'problem', { J: 'problem' }),
        createPacket('S2', 'systematic', { DS: 'requirements' })
      ];

      expect(() => assertDataDeps(packets)).not.toThrow();
    });
  });
});