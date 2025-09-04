/**
 * Packet type system for the semantic valley traversal pipeline
 * 
 * This module provides the new Packet<T> data structure that will replace Triple<T>,
 * along with compatibility adapters to ensure a smooth migration.
 */

/**
 * The new core data structure for generated content.
 * More flexible than Triple, with optional context and flags.
 */
export interface Packet<T> {
  /**
   * The main content of the document (DS, SP, X, or M structure)
   */
  text: T;
  
  /**
   * Optional semantic context for the generation
   */
  context?: {
    /**
     * Semantic terms used in generation (replaces terms_used)
     * Only include when genuinely useful for understanding
     */
    terms?: string[];
    
    /**
     * Justified notes about the generation (replaces warnings)
     * Only for actionable content, not default noise
     */
    notes?: string[];
  };
  
  /**
   * Optional flags for specific semantic properties
   */
  flags?: {
    /**
     * Risk assessment flag - only set by alethic stations (S6, S8)
     */
    risk?: boolean;
  };
}

/**
 * Legacy Triple type for backward compatibility
 * Maintains the exact structure expected by existing code
 */
export interface LegacyTriple<T> {
  text: T;
  terms_used: string[];
  warnings: string[];
}

/**
 * Re-export the original Triple type to maintain compatibility
 * This will be used during migration period
 */
export type Triple<T> = LegacyTriple<T>;

/**
 * Convert a Triple (old format) to a Packet (new format)
 * Transforms the legacy structure to the new flexible structure
 */
export function tripleToPacket<T>(triple: Triple<T>): Packet<T> {
  const packet: Packet<T> = {
    text: triple.text,
  };
  
  // Only include context if there's meaningful content
  const hasTerms = triple.terms_used && triple.terms_used.length > 0;
  const hasNotes = triple.warnings && triple.warnings.length > 0;
  
  if (hasTerms || hasNotes) {
    packet.context = {};
    if (hasTerms) {
      packet.context.terms = triple.terms_used;
    }
    if (hasNotes) {
      packet.context.notes = triple.warnings;
    }
  }
  
  return packet;
}

/**
 * Convert a Packet (new format) to a Triple (old format)
 * Ensures backward compatibility with existing consumers
 */
export function packetToTriple<T>(packet: Packet<T>): Triple<T> {
  // Ensure the structure matches the old Triple expectations
  return {
    text: packet.text,
    terms_used: packet.context?.terms || [],
    warnings: packet.context?.notes || []
  };
}

/**
 * Type guard to check if a value is a valid Packet
 */
export function isPacket<T>(value: unknown): value is Packet<T> {
  return (
    typeof value === 'object' &&
    value !== null &&
    'text' in value &&
    // Context and flags are optional
    (!('context' in value) || 
      (typeof (value as any).context === 'object' &&
       (!('terms' in (value as any).context) || Array.isArray((value as any).context.terms)) &&
       (!('notes' in (value as any).context) || Array.isArray((value as any).context.notes)))) &&
    (!('flags' in value) ||
      (typeof (value as any).flags === 'object' &&
       (!('risk' in (value as any).flags) || typeof (value as any).flags.risk === 'boolean')))
  );
}

/**
 * Helper to create a minimal valid Packet
 */
export function createPacket<T>(text: T): Packet<T> {
  return { text };
}

/**
 * Helper to add risk flag (only for alethic stations)
 */
export function addRiskFlag<T>(packet: Packet<T>, hasRisk: boolean): Packet<T> {
  return {
    ...packet,
    flags: {
      ...packet.flags,
      risk: hasRisk
    }
  };
}

/**
 * Helper to add semantic terms to a packet
 */
export function addTerms<T>(packet: Packet<T>, terms: string[]): Packet<T> {
  if (!terms || terms.length === 0) return packet;
  
  return {
    ...packet,
    context: {
      ...packet.context,
      terms: [...(packet.context?.terms || []), ...terms]
    }
  };
}

/**
 * Helper to add notes to a packet
 */
export function addNotes<T>(packet: Packet<T>, notes: string[]): Packet<T> {
  if (!notes || notes.length === 0) return packet;
  
  return {
    ...packet,
    context: {
      ...packet.context,
      notes: [...(packet.context?.notes || []), ...notes]
    }
  };
}