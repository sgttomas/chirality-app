/**
 * Station S1 Prompt: Systematic Modality
 * 
 * Structures the problem into constraints, givens, and invariants.
 * Produces DS (Data Sheet) document.
 */

import { StationPrompt, StationInput } from './station-template';

export class S1Prompt implements StationPrompt {
  station = 'S1' as const;
  modality = 'systematic' as const;
  expectedOutput = 'document' as const;
  requiresRiskAssessment = false;

  buildPrompt(input: StationInput): string {
    const sections: string[] = [];
    
    // Core instruction
    sections.push(
      'You are executing Station S1 of the semantic valley traversal.',
      'MODALITY: Systematic - Structure the problem into constraints, givens, and invariants.',
      'OUTPUT: DS (Data Sheet) document with data fields, types, and specifications.'
    );
    
    // Problem context
    sections.push(`Problem Statement:\n${input.problem.statement}`);
    
    // Matrix injection (C matrix if available)
    if (input.matrixInjection) {
      sections.push(
        'Matrix Scaffolding (C - Requirements):',
        'Use the following matrix cells as structured input for systematic analysis:',
        JSON.stringify(input.matrixInjection, null, 2)
      );
    }
    
    // Previous stations context
    if (input.previousStations?.S0) {
      sections.push(`Normalized Problem: ${input.previousStations.S0.normalized}`);
    }
    
    // Output specification
    sections.push(
      'Generate DS items following this structure:',
      '{ data_field: string, type?: string, units?: string, source_refs?: string[], notes?: string[] }',
      '',
      'Focus on:',
      '- Core data elements required for this problem',
      '- Proper data types and validation requirements', 
      '- Source references when using matrix content',
      '- Technical specifications and constraints',
      '',
      'OUTPUT JSON ONLY (no prose):',
      '{ "text": [DS items array] }'
    );
    
    return sections.join('\n\n');
  }
}