/**
 * Unit tests for the Packet type system and adapters
 */

import {
  Packet,
  Triple,
  tripleToPacket,
  packetToTriple,
  isPacket,
  createPacket,
  addRiskFlag,
  addTerms,
  addNotes
} from '../lib/utils/packets';

describe('Packet Type System', () => {
  describe('Type Compatibility', () => {
    it('should allow Triple to be used as Packet', () => {
      // Triple is now an alias for Packet, so this should compile
      const triple: Triple<{ data: string }> = {
        text: { data: 'test' },
        terms_used: ['term1'],
        warnings: ['warning1']
      };
      
      const packet: Packet<{ data: string }> = triple;
      expect(packet.text).toEqual({ data: 'test' });
    });
  });
  
  describe('tripleToPacket', () => {
    it('should convert a Triple with all fields to a Packet', () => {
      const triple: Triple<{ field: string }> = {
        text: { field: 'value' },
        terms_used: ['term1', 'term2'],
        warnings: ['warning1', 'warning2']
      };
      
      const packet = tripleToPacket(triple);
      
      expect(packet.text).toEqual({ field: 'value' });
      expect(packet.context?.terms).toEqual(['term1', 'term2']);
      expect(packet.context?.notes).toEqual(['warning1', 'warning2']);
    });
    
    it('should handle empty terms_used and warnings', () => {
      const triple: Triple<{ field: string }> = {
        text: { field: 'value' },
        terms_used: [],
        warnings: []
      };
      
      const packet = tripleToPacket(triple);
      
      expect(packet.text).toEqual({ field: 'value' });
      expect(packet.context).toBeUndefined();
    });
    
    it('should handle partial fields', () => {
      const triple: Triple<{ field: string }> = {
        text: { field: 'value' },
        terms_used: ['term1'],
        warnings: []
      };
      
      const packet = tripleToPacket(triple);
      
      expect(packet.context?.terms).toEqual(['term1']);
      expect(packet.context?.notes).toBeUndefined();
    });
  });
  
  describe('packetToTriple', () => {
    it('should convert a Packet to a Triple', () => {
      const packet: Packet<{ field: string }> = {
        text: { field: 'value' },
        context: {
          terms: ['term1', 'term2'],
          notes: ['note1', 'note2']
        },
        flags: { risk: true }
      };
      
      const triple = packetToTriple(packet);
      
      expect(triple.text).toEqual({ field: 'value' });
      expect(triple.terms_used).toEqual(['term1', 'term2']);
      expect(triple.warnings).toEqual(['note1', 'note2']);
    });
    
    it('should handle minimal Packet', () => {
      const packet: Packet<{ field: string }> = {
        text: { field: 'value' }
      };
      
      const triple = packetToTriple(packet);
      
      expect(triple.text).toEqual({ field: 'value' });
      expect(triple.terms_used).toEqual([]);
      expect(triple.warnings).toEqual([]);
    });
    
    it('should preserve round-trip conversion', () => {
      const originalTriple: Triple<{ data: string }> = {
        text: { data: 'test' },
        terms_used: ['term1', 'term2'],
        warnings: ['warning1']
      };
      
      const packet = tripleToPacket(originalTriple);
      const resultTriple = packetToTriple(packet);
      
      expect(resultTriple.text).toEqual(originalTriple.text);
      expect(resultTriple.terms_used).toEqual(originalTriple.terms_used);
      expect(resultTriple.warnings).toEqual(originalTriple.warnings);
    });
  });
  
  describe('isPacket', () => {
    it('should validate a valid Packet', () => {
      const packet: Packet<any> = {
        text: { field: 'value' },
        context: { terms: ['term1'], notes: ['note1'] },
        flags: { risk: true }
      };
      
      expect(isPacket(packet)).toBe(true);
    });
    
    it('should validate a minimal Packet', () => {
      const packet = { text: 'simple' };
      expect(isPacket(packet)).toBe(true);
    });
    
    it('should reject invalid structures', () => {
      expect(isPacket(null)).toBe(false);
      expect(isPacket(undefined)).toBe(false);
      expect(isPacket({})).toBe(false); // missing text
      expect(isPacket({ text: 'value', context: 'invalid' })).toBe(false);
      expect(isPacket({ text: 'value', flags: { risk: 'not-boolean' } })).toBe(false);
    });
    
    it('should accept partial context and flags', () => {
      expect(isPacket({ text: 'value', context: { terms: ['term1'] } })).toBe(true);
      expect(isPacket({ text: 'value', context: { notes: ['note1'] } })).toBe(true);
      expect(isPacket({ text: 'value', flags: {} })).toBe(true);
    });
  });
  
  describe('Helper Functions', () => {
    describe('createPacket', () => {
      it('should create a minimal packet', () => {
        const text = { field: 'value' };
        const packet = createPacket(text);
        
        expect(packet).toEqual({ text });
        expect(packet.context).toBeUndefined();
        expect(packet.flags).toBeUndefined();
      });
    });
    
    describe('addRiskFlag', () => {
      it('should add risk flag to packet', () => {
        const packet = createPacket({ field: 'value' });
        const withRisk = addRiskFlag(packet, true);
        
        expect(withRisk.flags?.risk).toBe(true);
        expect(withRisk.text).toEqual(packet.text);
      });
      
      it('should preserve existing flags', () => {
        const packet: Packet<any> = {
          text: { field: 'value' },
          flags: { risk: false }
        };
        
        const updated = addRiskFlag(packet, true);
        expect(updated.flags?.risk).toBe(true);
      });
    });
    
    describe('addTerms', () => {
      it('should add terms to packet', () => {
        const packet = createPacket({ field: 'value' });
        const withTerms = addTerms(packet, ['term1', 'term2']);
        
        expect(withTerms.context?.terms).toEqual(['term1', 'term2']);
      });
      
      it('should append to existing terms', () => {
        const packet: Packet<any> = {
          text: { field: 'value' },
          context: { terms: ['existing'] }
        };
        
        const updated = addTerms(packet, ['new1', 'new2']);
        expect(updated.context?.terms).toEqual(['existing', 'new1', 'new2']);
      });
      
      it('should handle empty terms array', () => {
        const packet = createPacket({ field: 'value' });
        const unchanged = addTerms(packet, []);
        
        expect(unchanged).toEqual(packet);
      });
    });
    
    describe('addNotes', () => {
      it('should add notes to packet', () => {
        const packet = createPacket({ field: 'value' });
        const withNotes = addNotes(packet, ['note1', 'note2']);
        
        expect(withNotes.context?.notes).toEqual(['note1', 'note2']);
      });
      
      it('should append to existing notes', () => {
        const packet: Packet<any> = {
          text: { field: 'value' },
          context: { notes: ['existing'] }
        };
        
        const updated = addNotes(packet, ['new1', 'new2']);
        expect(updated.context?.notes).toEqual(['existing', 'new1', 'new2']);
      });
      
      it('should preserve other context fields', () => {
        const packet: Packet<any> = {
          text: { field: 'value' },
          context: { terms: ['term1'] }
        };
        
        const updated = addNotes(packet, ['note1']);
        expect(updated.context?.terms).toEqual(['term1']);
        expect(updated.context?.notes).toEqual(['note1']);
      });
    });
  });
  
  describe('Migration Scenarios', () => {
    it('should handle DS document type', () => {
      const dsTriple: Triple<any> = {
        text: { data_field: 'user_id', type: 'string' },
        terms_used: ['identifier', 'primary key'],
        warnings: []
      };
      
      const packet = tripleToPacket(dsTriple);
      expect(packet.text.data_field).toBe('user_id');
      expect(packet.context?.terms).toEqual(['identifier', 'primary key']);
    });
    
    it('should handle M document with risk assessment', () => {
      const mPacket = createPacket({
        statement: 'Security review required',
        residual_risk: ['SQL injection', 'XSS']
      });
      
      const withRisk = addRiskFlag(mPacket, true);
      const withNotes = addNotes(withRisk, ['High priority review needed']);
      
      expect(withNotes.flags?.risk).toBe(true);
      expect(withNotes.context?.notes).toContain('High priority review needed');
    });
  });
});