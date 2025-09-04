/**
 * Station S2: Process Modality
 * 
 * Operational pathfinding - procedures, actors, inputs/outputs.
 * Produces SP (Standard Procedure) v1 document.
 */

import { StationInput } from '../prompts/station-template';
import { SP } from '../../../src/types/framework';
import { Packet, createPacket, addTerms } from '../../utils/packets';
import { S2Prompt } from '../prompts/S2';
import { callJSON } from '../../../src/chirality-core/vendor/llm';
import { guard } from '../../../src/chirality-core/validators';

/**
 * S2: Process modality → SP document v1
 * Matrix injection point for D (objectives) matrix
 */
export async function runS2(input: StationInput): Promise<Packet<SP[]>> {
  console.log('[S2] Process modality - operational pathfinding');
  
  if (input.matrixInjection) {
    console.log('[S2] Using D matrix for objectives scaffolding');
  }
  
  // For testing and development, use fallback mode
  if (process.env.NODE_ENV === 'test' || !process.env.OPENAI_API_KEY) {
    console.log('[S2] Running in fallback mode (no LLM call)');
    
    const fallbackSP: SP[] = [{
      step: 'Initialize process',
      purpose: 'Establish operational context',
      inputs: ['problem_domain from S1']
    }];
    
    return createPacket(fallbackSP);
  }
  
  const prompt = new S2Prompt();
  const userPrompt = prompt.buildPrompt(input);
  
  const systemPrompt = [
    'You are executing Station S2 of the semantic valley traversal.',
    'MODALITY: Process - Define operational procedures and workflows.',
    'OUTPUT: Strict JSON only with SP document structure.',
    'Focus on executable steps, clear inputs/outputs, and workflow logic.'
  ].join('\n');
  
  try {
    // Call LLM with process modality prompts
    const result = await callJSON(systemPrompt, userPrompt, { 
      temperature: 0.6 
    });
    
    // Validate the SP structure
    if (!result.text || !Array.isArray(result.text)) {
      throw new Error('S2 must produce array of SP items');
    }
    
    // Validate each SP item
    for (const item of result.text) {
      if (!guard.SP(item)) {
        throw new Error(`Invalid SP item structure: ${JSON.stringify(item)}`);
      }
    }
    
    // Create packet (no warnings needed for process modality)
    let packet = createPacket(result.text as SP[]);
    
    // Add terms only if they provide semantic value
    if (result.terms_used && result.terms_used.length > 0) {
      packet = addTerms(packet, result.terms_used);
    }
    
    console.log(`[S2] Generated ${result.text.length} SP items`);
    return packet;
    
  } catch (error) {
    console.error('[S2] Generation failed:', error);
    
    // Return minimal valid SP structure
    const fallbackSP: SP[] = [{
      step: 'error_process',
      purpose: 'S2 process analysis failed'
    }];
    
    return createPacket(fallbackSP);
  }
}