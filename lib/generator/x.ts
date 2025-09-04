import type { X } from '@/chirality-core/contracts';
import type { DocumentGenerator, GenerationContext, GeneratorResult } from './types';

export class XGenerator implements DocumentGenerator<X> {
  async generate(ctx: GenerationContext): Promise<GeneratorResult<X>> {
    const logs: string[] = [];
    
    // Stable ordering for both X and E matrices
    const xCells = ctx.matrices.X
      .slice()
      .sort((a, b) => {
        const orderA = a.meta?.order ?? 0;
        const orderB = b.meta?.order ?? 0;
        if (orderA !== orderB) return orderA - orderB;
        return a.id.localeCompare(b.id);
      });
    
    const eCells = ctx.matrices.E
      .slice()
      .sort((a, b) => {
        const orderA = a.meta?.order ?? 0;
        const orderB = b.meta?.order ?? 0;
        if (orderA !== orderB) return orderA - orderB;
        return a.id.localeCompare(b.id);
      });
    
    logs.push(`Processing ${xCells.length} X matrix cells and ${eCells.length} E matrix cells for X generation`);
    
    if (xCells.length === 0 && eCells.length === 0) {
      logs.push('Warning: No X or E matrix cells found, generating minimal X');
      return {
        triple: {
          text: {
            heading: 'Unknown Solution Template',
            narrative: 'No verification or evaluation data available',
            refs: []
          },
          terms_used: [],
          warnings: ['No X or E matrix data available for X generation']
        },
        logs
      };
    }
    
    // Extract heading from primary verification or evaluation cell
    const primaryCell = xCells[0] || eCells[0];
    const heading = this.extractHeading(primaryCell.text, ctx.problem.title);
    
    // Build narrative from verification and evaluation insights
    const narrative = this.buildNarrative(xCells, eCells);
    
    // Extract precedents from verification cells
    const precedents = this.extractPrecedents(xCells);
    
    // Extract successors from evaluation cells
    const successors = this.extractSuccessors(eCells);
    
    // Build context notes combining insights from both matrices
    const contextNotes = this.extractContextNotes(xCells, eCells);
    
    // Collect all references and citations
    const refs = [...xCells, ...eCells].flatMap(cell => [...cell.refs, ...cell.citations]);
    
    // Extract terms used
    const termsUsed = this.extractTermsUsed([...xCells, ...eCells]);
    
    // Generate warnings
    const warnings: string[] = [];
    if (xCells.length === 0) {
      warnings.push('No X matrix verification data available');
    }
    if (eCells.length === 0) {
      warnings.push('No E matrix evaluation data available');
    }
    
    logs.push(`Generated X: heading="${heading}"`);
    logs.push(`Built narrative with ${narrative.length} characters`);
    logs.push(`Extracted ${precedents.length} precedents, ${successors.length} successors`);
    logs.push(`Found ${contextNotes.length} context notes`);
    
    const x: X = {
      heading,
      narrative,
      ...(precedents.length > 0 && { precedents }),
      ...(successors.length > 0 && { successors }),
      ...(contextNotes.length > 0 && { context_notes: contextNotes }),
      refs
    };
    
    return {
      triple: {
        text: x,
        terms_used: termsUsed,
        warnings
      },
      logs
    };
  }
  
  private extractHeading(text: string, problemTitle: string): string {
    // Extract solution template heading from verification/evaluation text
    const patterns = [
      /^([^.!?]{10,60})(?:[.!?]|$)/,  // First meaningful sentence
      /solution\s*(?:template|approach):\s*([^.!?]+)/i,
      /template\s*for\s*([^.!?]+)/i,
      /verification\s*of\s*([^.!?]+)/i
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match && match[1].trim().length > 5) {
        return match[1].trim();
      }
    }
    
    // Fallback: derive from problem title
    return `Solution Template for ${problemTitle}`;
  }
  
  private buildNarrative(xCells: any[], eCells: any[]): string {
    const narrativeParts: string[] = [];
    
    // Start with verification insights if available
    if (xCells.length > 0) {
      const verificationInsights = xCells
        .map(cell => this.extractKeyInsight(cell.text))
        .filter(insight => insight.length > 10);
      
      if (verificationInsights.length > 0) {
        narrativeParts.push('Verification analysis reveals:');
        narrativeParts.push(...verificationInsights.map(insight => `• ${insight}`));
      }
    }
    
    // Add evaluation insights if available
    if (eCells.length > 0) {
      const evaluationInsights = eCells
        .map(cell => this.extractKeyInsight(cell.text))
        .filter(insight => insight.length > 10);
      
      if (evaluationInsights.length > 0) {
        if (narrativeParts.length > 0) narrativeParts.push('');
        narrativeParts.push('Evaluation considerations include:');
        narrativeParts.push(...evaluationInsights.map(insight => `• ${insight}`));
      }
    }
    
    return narrativeParts.length > 0 
      ? narrativeParts.join('\n')
      : 'No detailed verification or evaluation insights available.';
  }
  
  private extractKeyInsight(text: string): string {
    // Extract the most important sentence or insight from cell text
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
    
    // Prioritize sentences with key verification/evaluation terms
    const keyTerms = /\b(?:must|should|requires?|ensures?|verifies?|validates?|tests?|checks?|evaluates?|assesses?|confirms?)\b/i;
    
    for (const sentence of sentences) {
      if (keyTerms.test(sentence)) {
        return sentence.trim();
      }
    }
    
    // Fallback to first meaningful sentence
    return sentences[0]?.trim() || text.substring(0, 100).trim();
  }
  
  private extractPrecedents(xCells: any[]): string[] {
    const precedents = new Set<string>();
    
    for (const cell of xCells) {
      const text = cell.text;
      
      // Look for precedent patterns in verification text
      const precedentPatterns = [
        /(?:before|prior to|prerequisite|depends on|requires)\s+([^.!?]+)/gi,
        /precedent:\s*([^.!?]+)/gi,
        /must\s+first\s+([^.!?]+)/gi
      ];
      
      for (const pattern of precedentPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const precedent = match[1].trim();
          if (precedent && precedent.length > 5) {
            precedents.add(precedent);
          }
        });
      }
    }
    
    return Array.from(precedents).sort();
  }
  
  private extractSuccessors(eCells: any[]): string[] {
    const successors = new Set<string>();
    
    for (const cell of eCells) {
      const text = cell.text;
      
      // Look for successor patterns in evaluation text
      const successorPatterns = [
        /(?:then|next|following|leads to|enables)\s+([^.!?]+)/gi,
        /successor:\s*([^.!?]+)/gi,
        /will\s+(?:allow|enable|permit)\s+([^.!?]+)/gi
      ];
      
      for (const pattern of successorPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const successor = match[1].trim();
          if (successor && successor.length > 5) {
            successors.add(successor);
          }
        });
      }
    }
    
    return Array.from(successors).sort();
  }
  
  private extractContextNotes(xCells: any[], eCells: any[]): string[] {
    const contextNotes = new Set<string>();
    
    // Extract important context from both matrices
    const allCells = [...xCells, ...eCells];
    
    for (const cell of allCells) {
      const text = cell.text;
      
      // Look for context patterns
      const contextPatterns = [
        /(?:note|context|important|consider|remember):\s*([^.!?]+)/gi,
        /(?:however|although|despite|nevertheless)\s+([^.!?]+)/gi,
        /(?:limitation|constraint|assumption):\s*([^.!?]+)/gi
      ];
      
      for (const pattern of contextPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const note = match[1].trim();
          if (note && note.length > 10) {
            contextNotes.add(note);
          }
        });
      }
      
      // Add station information as context if meaningful
      if (cell.station && cell.station !== 'Verification' && cell.station !== 'Evaluation') {
        contextNotes.add(`Context from ${cell.station}: ${cell.row_label} - ${cell.col_label}`);
      }
    }
    
    return Array.from(contextNotes).sort();
  }
  
  private extractTermsUsed(cells: any[]): string[] {
    const terms = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Extract technical terms
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