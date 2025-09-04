/**
 * Station S3: Epistemic Modality
 * 
 * Knowledge claims and evidence requirements.
 * Produces X (Solution Template) v1 document.
 */

import { StationInput } from '../prompts/station-template';
import { X } from '../../../src/types/framework';
import { Packet, createPacket, addTerms } from '../../utils/packets';
import { S3Prompt } from '../prompts/S3';
import { callJSON } from '../../../src/chirality-core/vendor/llm';
import { guard } from '../../../src/chirality-core/validators';

/**
 * S3: Epistemic modality → X document v1
 * Matrix injection point for X (verification) matrix
 */
export async function runS3(input: StationInput): Promise<Packet<X[]>> {
  console.log('[S3] Epistemic modality - knowledge claims');
  
  if (input.matrixInjection?.X) {
    console.log('[S3] Using X matrix for verification scaffolding');
  }
  
  // For testing and development, use fallback mode
  if (process.env.NODE_ENV === 'test' || !process.env.OPENAI_API_KEY) {
    console.log('[S3] Running in fallback mode (no LLM call)');
    
    const fallbackX: X[] = [{
      heading: 'Initial Solution Framework',
      narrative: 'Knowledge synthesis from S1 and S2',
      precedents: ['S1:systematic', 'S2:process']
    }];
    
    return createPacket(fallbackX);
  }
  
  const prompt = new S3Prompt();
  const userPrompt = prompt.buildPrompt(input);
  
  const systemPrompt = [
    'You are executing Station S3 of the semantic valley traversal.',
    'MODALITY: Epistemic - Generate knowledge claims and evidence requirements.',
    'OUTPUT: Strict JSON only with X (Solution Template) document structure.',
    'Focus on entities, relationships, and assertions required for a valid solution.'
  ].join('\n');
  
  try {
    // Call LLM with epistemic modality prompts
    const result = await callJSON(systemPrompt, userPrompt, { 
      temperature: 0.5 
    });
    
    // Validate the X structure
    if (!result.text || !Array.isArray(result.text)) {
      throw new Error('S3 must produce array of X items');
    }
    
    // Validate each X item
    for (const item of result.text) {
      if (!guard.X(item)) {
        throw new Error(`Invalid X item structure: ${JSON.stringify(item)}`);
      }
    }
    
    // Create packet
    let packet = createPacket(result.text as X[]);
    
    if (result.terms_used && result.terms_used.length > 0) {
      packet = addTerms(packet, result.terms_used);
    }
    
    console.log(`[S3] Generated ${result.text.length} X items`);
    return packet;
    
  } catch (error) {
    console.error('[S3] Generation failed:', error);
    
    // Return minimal valid X structure
    const fallbackX: X[] = [{
      heading: 'Initial Solution Framework',
      narrative: 'Knowledge synthesis from S1 and S2',
      precedents: ['S1:systematic', 'S2:process']
    }];
    
    return createPacket(fallbackX);
  }
}