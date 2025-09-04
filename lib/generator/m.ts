import type { M } from '@/chirality-core/contracts';
import type { DocumentGenerator, GenerationContext, GeneratorResult } from './types';

export class MGenerator implements DocumentGenerator<M> {
  async generate(ctx: GenerationContext): Promise<GeneratorResult<M>> {
    const logs: string[] = [];
    
    // Stable ordering: sort by meta.order then by id for deterministic output
    const eCells = ctx.matrices.E
      .slice()
      .sort((a, b) => {
        const orderA = a.meta?.order ?? 0;
        const orderB = b.meta?.order ?? 0;
        if (orderA !== orderB) return orderA - orderB;
        return a.id.localeCompare(b.id);
      });
    
    logs.push(`Processing ${eCells.length} E matrix cells for M generation`);
    
    if (eCells.length === 0) {
      logs.push('Warning: No E matrix cells found, generating minimal M');
      return {
        triple: {
          text: {
            statement: 'No strategic guidance available',
            justification: 'Insufficient evaluation data for guidance generation',
            trace_back: []
          },
          terms_used: [],
          warnings: ['No E matrix data available for M generation']
        },
        logs
      };
    }
    
    // Extract strategic statement from primary evaluation cell
    const primaryCell = eCells[0];
    const statement = this.extractStatement(primaryCell.text, ctx.problem.title);
    
    // Build justification from evaluation analysis
    const justification = this.buildJustification(eCells);
    
    // Extract assumptions from evaluation cells
    const assumptions = this.extractAssumptions(eCells);
    
    // Assess residual risks from evaluation data
    const residualRisk = this.extractResidualRisk(eCells);
    
    // Create trace_back from citations and refs
    const traceBack = this.buildTraceBack(eCells);
    
    // Extract terms used
    const termsUsed = this.extractTermsUsed(eCells);
    
    // Generate warnings
    const warnings: string[] = [];
    if (assumptions.length === 0) {
      warnings.push('No assumptions identified from E matrix analysis');
    }
    if (residualRisk.length === 0) {
      warnings.push('No residual risks identified from evaluation data');
    }
    
    logs.push(`Generated M: statement="${statement}"`);
    logs.push(`Built justification with ${justification.length} characters`);
    logs.push(`Identified ${assumptions.length} assumptions, ${residualRisk.length} residual risks`);
    logs.push(`Created ${traceBack.length} trace-back references`);
    
    const m: M = {
      statement,
      justification,
      ...(assumptions.length > 0 && { assumptions }),
      ...(residualRisk.length > 0 && { residual_risk: residualRisk }),
      trace_back: traceBack
    };
    
    return {
      triple: {
        text: m,
        terms_used: termsUsed,
        warnings
      },
      logs
    };
  }
  
  private extractStatement(text: string, problemTitle: string): string {
    // Extract strategic guidance statement from evaluation text
    const patterns = [
      /^([^.!?]{20,120})(?:[.!?]|$)/,  // First substantial sentence
      /guidance:\s*([^.!?]+)/i,
      /recommendation:\s*([^.!?]+)/i,
      /strategic\s*(?:approach|guidance):\s*([^.!?]+)/i,
      /key\s*(?:insight|finding):\s*([^.!?]+)/i
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match && match[1].trim().length > 15) {
        return match[1].trim();
      }
    }
    
    // Fallback: derive strategic statement from problem
    return `Strategic guidance for ${problemTitle} requires comprehensive evaluation of all factors`;
  }
  
  private buildJustification(eCells: any[]): string {
    const justificationParts: string[] = [];
    
    // Extract key evaluation findings
    const findings = eCells
      .map(cell => this.extractKeyFinding(cell.text))
      .filter(finding => finding.length > 15);
    
    if (findings.length > 0) {
      justificationParts.push('This guidance is justified by the following evaluation findings:');
      findings.forEach((finding, index) => {
        justificationParts.push(`${index + 1}. ${finding}`);
      });
    }
    
    // Add risk-benefit analysis if available
    const riskBenefitAnalysis = this.extractRiskBenefitAnalysis(eCells);
    if (riskBenefitAnalysis) {
      justificationParts.push('');
      justificationParts.push('Risk-benefit analysis:');
      justificationParts.push(riskBenefitAnalysis);
    }
    
    return justificationParts.length > 0 
      ? justificationParts.join('\n')
      : 'Justification based on available evaluation data and risk assessment.';
  }
  
  private extractKeyFinding(text: string): string {
    // Extract the most important finding from evaluation text
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 15);
    
    // Prioritize sentences with evaluative terms
    const evaluativeTerms = /\b(?:shows|indicates|demonstrates|reveals|suggests|implies|proves|confirms|analysis|evaluation|assessment|finding)\b/i;
    
    for (const sentence of sentences) {
      if (evaluativeTerms.test(sentence)) {
        return sentence.trim();
      }
    }
    
    // Fallback to first meaningful sentence
    return sentences[0]?.trim() || text.substring(0, 100).trim();
  }
  
  private extractRiskBenefitAnalysis(eCells: any[]): string | null {
    for (const cell of eCells) {
      const text = cell.text;
      
      // Look for risk-benefit patterns
      const patterns = [
        /risk[s]?\s*(?:vs|versus|against)\s*benefit[s]?[:\s]*([^.!?]{20,})/i,
        /benefit[s]?\s*(?:vs|versus|against)\s*risk[s]?[:\s]*([^.!?]{20,})/i,
        /(?:overall|net)\s*(?:benefit|advantage|risk)[:\s]*([^.!?]{20,})/i
      ];
      
      for (const pattern of patterns) {
        const match = text.match(pattern);
        if (match && match[1].trim().length > 20) {
          return match[1].trim();
        }
      }
    }
    
    return null;
  }
  
  private extractAssumptions(eCells: any[]): string[] {
    const assumptions = new Set<string>();
    
    for (const cell of eCells) {
      const text = cell.text;
      
      // Look for assumption patterns
      const assumptionPatterns = [
        /(?:assumes?|assuming|assumption):\s*([^.!?]+)/gi,
        /(?:given that|provided that|if)\s+([^.!?]+)/gi,
        /(?:we assume|it is assumed)\s+([^.!?]+)/gi,
        /(?:presuming|presupposes?)\s+([^.!?]+)/gi
      ];
      
      for (const pattern of assumptionPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const assumption = match[1].trim();
          if (assumption && assumption.length > 10) {
            assumptions.add(assumption);
          }
        });
      }
    }
    
    return Array.from(assumptions).sort();
  }
  
  private extractResidualRisk(eCells: any[]): string[] {
    const residualRisks = new Set<string>();
    
    for (const cell of eCells) {
      const text = cell.text;
      
      // Look for residual risk patterns
      const riskPatterns = [
        /(?:residual|remaining|outstanding)\s*risk[s]?:\s*([^.!?]+)/gi,
        /(?:risk[s]?\s*(?:remain|persist|continue)[s]?):\s*([^.!?]+)/gi,
        /(?:however|despite|although).*risk[s]?\s*([^.!?]+)/gi,
        /(?:potential|possible)\s*(?:issue|problem|risk)[s]?:\s*([^.!?]+)/gi
      ];
      
      for (const pattern of riskPatterns) {
        const matches = [...text.matchAll(pattern)];
        matches.forEach(match => {
          const risk = match[1].trim();
          if (risk && risk.length > 10) {
            residualRisks.add(risk);
          }
        });
      }
      
      // Also look for explicit risk indicators
      if (/\b(?:warning|caution|concern|danger|hazard|threat)\b/i.test(text)) {
        const riskSentences = text.split(/[.!?]+/).filter((s: string) => 
          /\b(?:risk|warning|caution|concern|danger|hazard|threat)\b/i.test(s) && s.trim().length > 15
        );
        riskSentences.forEach((sentence: string) => residualRisks.add(sentence.trim()));
      }
    }
    
    return Array.from(residualRisks).sort();
  }
  
  private buildTraceBack(eCells: any[]): string[] {
    const traceBack = new Set<string>();
    
    // Collect citations and references from E cells
    for (const cell of eCells) {
      cell.citations?.forEach((citation: string) => traceBack.add(citation));
      cell.refs?.forEach((ref: string) => traceBack.add(ref));
    }
    
    // Add cell identifiers for traceability
    eCells.forEach(cell => {
      if (cell.id) {
        traceBack.add(`E-matrix:${cell.id}`);
      }
    });
    
    return Array.from(traceBack).sort();
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
      
      // Extract terms from labels and stations
      if (cell.row_label) terms.add(cell.row_label);
      if (cell.col_label) terms.add(cell.col_label);
      if (cell.station) terms.add(cell.station);
    }
    
    return Array.from(terms).sort();
  }
}