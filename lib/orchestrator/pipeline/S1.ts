/**
 * Station S1: Systematic Modality
 * 
 * Structures the problem - constraints, givens, invariants.
 * Produces DS (Data Sheet) document.
 */

import { StationInput } from '../prompts/station-template';
import { DS } from '../../../src/types/framework';
import { Packet, createPacket, addTerms } from '../../utils/packets';
import { S1Prompt } from '../prompts/S1';
import { callJSON } from '../../../src/chirality-core/vendor/llm';
import { guard } from '../../../src/chirality-core/validators';

/**
 * S1: Systematic structuring → DS document
 * Matrix injection point for C (requirements) matrix
 */
export async function runS1(input: StationInput): Promise<Packet<DS[]>> {
  console.log('[S1] Systematic modality - structuring problem');
  
  if (input.matrixInjection) {
    console.log('[S1] Using C matrix for requirements scaffolding');
  }
  
  // For testing and development, use fallback mode
  if (process.env.NODE_ENV === 'test' || !process.env.OPENAI_API_KEY) {
    console.log('[S1] Running in fallback mode (no LLM call)');
    
    const fallbackDS: DS[] = [{
      data_field: 'problem_domain',
      type: 'categorical', 
      notes: ['Generated in fallback mode']
    }];
    
    return createPacket(fallbackDS);
  }
  
  const prompt = new S1Prompt();
  const userPrompt = prompt.buildPrompt(input);
  
  const systemPrompt = [
    'You are executing Station S1 of the semantic valley traversal.',
    'MODALITY: Systematic - Structure problems into data specifications.',
    'OUTPUT: Strict JSON only with DS document structure.',
    'Focus on data fields, types, constraints, and validation requirements.'
  ].join('\n');
  
  try {
    // Call LLM with systematic modality prompts
    const result = await callJSON(systemPrompt, userPrompt, { 
      temperature: 0.6 
    });
    
    // Validate the DS structure
    if (!result.text || !Array.isArray(result.text)) {
      throw new Error('S1 must produce array of DS items');
    }
    
    // Validate each DS item
    for (const item of result.text) {
      if (!guard.DS(item)) {
        throw new Error(`Invalid DS item structure: ${JSON.stringify(item)}`);
      }
    }
    
    // Create packet (no warnings needed for systematic modality)
    let packet = createPacket(result.text as DS[]);
    
    // Add terms only if they provide semantic value
    if (result.terms_used && result.terms_used.length > 0) {
      packet = addTerms(packet, result.terms_used);
    }
    
    console.log(`[S1] Generated ${result.text.length} DS items`);
    return packet;
    
  } catch (error) {
    console.error('[S1] Generation failed:', error);
    
    // Return minimal valid DS structure
    const fallbackDS: DS[] = [{
      data_field: 'error_systematic',
      type: 'error',
      notes: ['S1 systematic analysis failed']
    }];
    
    return createPacket(fallbackDS);
  }
}