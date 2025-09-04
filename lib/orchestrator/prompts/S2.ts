/**
 * Station S2 Prompt: Process Modality
 * 
 * Operational pathfinding - procedures, actors, inputs/outputs.
 * Produces SP (Standard Procedure) v1 document.
 */

import { StationPrompt, StationInput } from './station-template';

export class S2Prompt implements StationPrompt {
  station = 'S2' as const;
  modality = 'process' as const;
  expectedOutput = 'document' as const;
  requiresRiskAssessment = false;

  buildPrompt(input: StationInput): string {
    const sections: string[] = [];
    
    // Core instruction
    sections.push(
      'You are executing Station S2 of the semantic valley traversal.',
      'MODALITY: Process - Define operational pathfinding with procedures, actors, inputs/outputs.',
      'OUTPUT: SP (Standard Procedure) v1 document with step-by-step workflows.'
    );
    
    // Problem context
    sections.push(`Problem Statement:\n${input.problem.statement}`);
    
    // Matrix injection (D matrix if available)
    if (input.matrixInjection) {
      sections.push(
        'Matrix Scaffolding (D - Objectives):',
        'Use the following matrix cells as structured input for process design:',
        JSON.stringify(input.matrixInjection, null, 2)
      );
    }
    
    // Previous stations context
    if (input.previousStations?.S0) {
      sections.push(`Normalized Problem: ${input.previousStations.S0.normalized}`);
    }
    
    if (input.previousStations?.S1) {
      sections.push(
        'Systematic Foundation (from S1):',
        'Build procedures that operate on these data structures:',
        JSON.stringify(input.previousStations.S1.text, null, 2)
      );
    }
    
    // Output specification
    sections.push(
      'Generate SP items following this structure:',
      '{ step: string, purpose?: string, inputs?: string[], outputs?: string[], preconditions?: string[], postconditions?: string[], refs?: string[] }',
      '',
      'Focus on:',
      '- Sequential, executable procedures',
      '- Clear inputs and outputs for each step',
      '- Realistic preconditions and postconditions',
      '- References to S1 data structures where applicable',
      '',
      'OUTPUT JSON ONLY (no prose):',
      '{ "text": [SP items array] }'
    );
    
    return sections.join('\n\n');
  }
}