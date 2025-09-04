import type { SP } from '@/chirality-core/contracts';
import type { DocumentGenerator, GenerationContext, GeneratorResult } from './types';

export class SPGenerator implements DocumentGenerator<SP> {
  async generate(ctx: GenerationContext): Promise<GeneratorResult<SP>> {
    const logs: string[] = [];
    
    // Stable ordering: sort by meta.order then by id for deterministic output
    const dCells = ctx.matrices.D
      .slice()
      .sort((a, b) => {
        const orderA = a.meta?.order ?? 0;
        const orderB = b.meta?.order ?? 0;
        if (orderA !== orderB) return orderA - orderB;
        return a.id.localeCompare(b.id);
      });
    
    logs.push(`Processing ${dCells.length} D matrix cells for SP generation`);
    
    if (dCells.length === 0) {
      logs.push('Warning: No D matrix cells found, generating minimal SP');
      return {
        triple: {
          text: {
            step: 'unknown_procedure',
            purpose: 'Purpose not specified',
            inputs: [],
            outputs: [],
            refs: []
          },
          terms_used: [],
          warnings: ['No D matrix data available for SP generation']
        },
        logs
      };
    }
    
    // Extract step from primary objective cell
    const primaryCell = dCells[0];
    const step = this.extractStepName(primaryCell.text);
    
    // Extract purpose from objective description
    const purpose = this.extractPurpose(primaryCell.text);
    
    // Derive inputs from text analysis
    const inputs = this.extractInputs(dCells);
    
    // Derive outputs from text analysis
    const outputs = this.extractOutputs(dCells);
    
    // Extract preconditions and postconditions from constraint analysis
    const { preconditions, postconditions } = this.extractConditions(dCells);
    
    // Collect references and citations
    const refs = [...dCells.flatMap(cell => cell.refs), ...dCells.flatMap(cell => cell.citations)];
    
    // Extract terms used
    const termsUsed = this.extractTermsUsed(dCells);
    
    // Generate warnings
    const warnings: string[] = [];
    if (inputs.length === 0) {
      warnings.push('No inputs identified from D matrix analysis');
    }
    if (outputs.length === 0) {
      warnings.push('No outputs identified from D matrix analysis');
    }
    
    logs.push(`Generated SP: step="${step}", purpose="${purpose}"`);
    logs.push(`Identified ${inputs.length} inputs, ${outputs.length} outputs`);
    logs.push(`Extracted ${preconditions.length} preconditions, ${postconditions.length} postconditions`);
    
    const sp: SP = {
      step,
      purpose,
      inputs,
      outputs,
      ...(preconditions.length > 0 && { preconditions }),
      ...(postconditions.length > 0 && { postconditions }),
      refs
    };
    
    return {
      triple: {
        text: sp,
        terms_used: termsUsed,
        warnings
      },
      logs
    };
  }
  
  private extractStepName(text: string): string {
    // Extract procedure step name from objective text
    const patterns = [
      /^([^.!?]+)(?:[.!?]|$)/,  // First sentence
      /(?:step|procedure|process):\s*([^.!?]+)/i,
      /to\s+([^.!?]+?)(?:\s+in order|\s+by|\s+through|$)/i
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1].trim().toLowerCase().replace(/\s+/g, '_');
      }
    }
    
    return 'unnamed_step';
  }
  
  private extractPurpose(text: string): string {
    // Extract the purpose or goal from the objective description
    const patterns = [
      /in order to\s+([^.!?]+)/i,
      /so that\s+([^.!?]+)/i,
      /to ensure\s+([^.!?]+)/i,
      /purpose:\s*([^.!?]+)/i
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1].trim();
      }
    }
    
    // Fallback: use the first sentence as purpose
    const firstSentence = text.match(/^([^.!?]+)/);
    return firstSentence ? firstSentence[1].trim() : 'Purpose not specified';
  }
  
  private extractInputs(cells: any[]): string[] {
    const inputs = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Look for input patterns
      const inputPatterns = [
        /(?:requires?|needs?|takes?|accepts?|inputs?)\s+([^.!?]+)/gi,
        /given\s+([^.!?]+)/gi,
        /with\s+([a-zA-Z][^.!?]*?)(?:\s+(?:and|or|,)|$)/gi
      ];
      
      for (const pattern of inputPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const input = match[1].trim();
          if (input && input.length > 2) {
            inputs.add(input);
          }
        });
      }
    }
    
    return Array.from(inputs).sort();
  }
  
  private extractOutputs(cells: any[]): string[] {
    const outputs = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Look for output patterns
      const outputPatterns = [
        /(?:produces?|generates?|creates?|outputs?|results? in)\s+([^.!?]+)/gi,
        /will\s+(?:have|be|create|generate)\s+([^.!?]+)/gi,
        /resulting\s+in\s+([^.!?]+)/gi
      ];
      
      for (const pattern of outputPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const output = match[1].trim();
          if (output && output.length > 2) {
            outputs.add(output);
          }
        });
      }
    }
    
    return Array.from(outputs).sort();
  }
  
  private extractConditions(cells: any[]): { preconditions: string[], postconditions: string[] } {
    const preconditions = new Set<string>();
    const postconditions = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Precondition patterns
      const prePatterns = [
        /(?:before|prior to|requires? that|assumes?|if)\s+([^.!?]+)/gi,
        /precondition:\s*([^.!?]+)/gi,
        /must\s+(?:have|be|exist)\s+([^.!?]+)/gi
      ];
      
      for (const pattern of prePatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const condition = match[1].trim();
          if (condition && condition.length > 3) {
            preconditions.add(condition);
          }
        });
      }
      
      // Postcondition patterns  
      const postPatterns = [
        /(?:after|following|ensures?|guarantees?)\s+([^.!?]+)/gi,
        /postcondition:\s*([^.!?]+)/gi,
        /will\s+(?:ensure|guarantee)\s+([^.!?]+)/gi
      ];
      
      for (const pattern of postPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const condition = match[1].trim();
          if (condition && condition.length > 3) {
            postconditions.add(condition);
          }
        });
      }
    }
    
    return {
      preconditions: Array.from(preconditions).sort(),
      postconditions: Array.from(postconditions).sort()
    };
  }
  
  private extractTermsUsed(cells: any[]): string[] {
    const terms = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Extract technical terms and domain concepts
      const technicalTerms = text.match(/\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b/g) || [];
      technicalTerms.forEach((term: string) => terms.add(term));
      
      // Extract quoted terms
      const quotedTerms = text.match(/"([^"]+)"/g) || [];
      quotedTerms.forEach((quoted: string) => terms.add(quoted.replace(/"/g, '')));
      
      // Extract terms from labels
      if (cell.row_label) terms.add(cell.row_label);
      if (cell.col_label) terms.add(cell.col_label);
      if (cell.station) terms.add(cell.station);
    }
    
    return Array.from(terms).sort();
  }
}