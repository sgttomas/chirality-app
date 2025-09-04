import type { DS } from '@/chirality-core/contracts';
import type { DocumentGenerator, GenerationContext, GeneratorResult } from './types';

export class DSGenerator implements DocumentGenerator<DS> {
  async generate(ctx: GenerationContext): Promise<GeneratorResult<DS>> {
    const logs: string[] = [];
    
    // Stable ordering: sort by meta.order then by id for deterministic output
    const cCells = ctx.matrices.C
      .slice() // Don't mutate original
      .sort((a, b) => {
        const orderA = a.meta?.order ?? 0;
        const orderB = b.meta?.order ?? 0;
        if (orderA !== orderB) return orderA - orderB;
        return a.id.localeCompare(b.id);
      });
    
    logs.push(`Processing ${cCells.length} C matrix cells for DS generation`);
    
    if (cCells.length === 0) {
      logs.push('Warning: No C matrix cells found, generating minimal DS');
      return {
        triple: {
          text: {
            data_field: 'unknown',
            type: 'string',
            source_refs: []
          },
          terms_used: [],
          warnings: ['No C matrix data available for DS generation']
        },
        logs
      };
    }
    
    // Extract data field from the primary requirements cell
    const primaryCell = cCells[0];
    const dataField = this.extractDataField(primaryCell.text);
    
    // Determine type from text analysis (deterministic rules)
    const type = this.determineFieldType(primaryCell.text);
    
    // Extract units if mentioned
    const units = this.extractUnits(primaryCell.text);
    
    // Map citations to source_refs
    const sourceRefs = cCells.flatMap(cell => cell.citations);
    
    // Extract all terms used across C cells
    const termsUsed = this.extractTermsUsed(cCells);
    
    // Generate warnings for incomplete data
    const warnings: string[] = [];
    if (sourceRefs.length === 0) {
      warnings.push('No source references found in C matrix cells');
    }
    
    logs.push(`Generated DS: field="${dataField}", type="${type}", units="${units || 'none'}"`);
    logs.push(`Extracted ${termsUsed.length} terms and ${sourceRefs.length} source references`);
    
    const ds: DS = {
      data_field: dataField,
      type,
      ...(units && { units }),
      source_refs: sourceRefs,
      ...(warnings.length > 0 && { notes: warnings })
    };
    
    return {
      triple: {
        text: ds,
        terms_used: termsUsed,
        warnings
      },
      logs
    };
  }
  
  private extractDataField(text: string): string {
    // Deterministic extraction of data field name from requirement text
    // Look for patterns like "system must track X" -> "X"
    const patterns = [
      /system must (?:track|store|maintain|handle|process) ([^,.]+)/i,
      /(?:track|store|maintain|handle|process) ([^,.]+)/i,
      /([^,.]+) (?:is|are|must be) (?:tracked|stored|maintained)/i
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1].trim().toLowerCase().replace(/\s+/g, '_');
      }
    }
    
    // Fallback: use first significant noun
    const words = text.split(/\s+/).filter(w => w.length > 3);
    return words[0]?.toLowerCase() || 'unknown_field';
  }
  
  private determineFieldType(text: string): string {
    // Deterministic type inference from text content
    if (/\b(?:number|quantity|amount|count|integer|float)\b/i.test(text)) {
      return 'number';
    }
    if (/\b(?:date|time|timestamp|when)\b/i.test(text)) {
      return 'datetime';
    }
    if (/\b(?:yes|no|true|false|boolean|flag)\b/i.test(text)) {
      return 'boolean';
    }
    if (/\b(?:email|url|link|address)\b/i.test(text)) {
      return 'string';
    }
    if (/\b(?:list|array|multiple|collection)\b/i.test(text)) {
      return 'array';
    }
    
    // Default to string
    return 'string';
  }
  
  private extractUnits(text: string): string | undefined {
    // Look for common units in parentheses or after numbers
    const unitPatterns = [
      /\(([^)]*(?:kg|g|lb|oz|m|cm|mm|ft|in|s|min|h|°|%|$|€|£))\)/i,
      /\d+\s*([a-zA-Z]+)/,
      /measured in ([^,.]+)/i
    ];
    
    for (const pattern of unitPatterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1].trim();
      }
    }
    
    return undefined;
  }
  
  private extractTermsUsed(cells: any[]): string[] {
    // Extract domain-specific terms from all C cells
    const terms = new Set<string>();
    
    for (const cell of cells) {
      const text = cell.text;
      
      // Extract technical terms (words with specific patterns)
      const technicalTerms = text.match(/\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b/g) || [];
      technicalTerms.forEach((term: string) => terms.add(term));
      
      // Extract quoted terms
      const quotedTerms = text.match(/"([^"]+)"/g) || [];
      quotedTerms.forEach((quoted: string) => terms.add(quoted.replace(/"/g, '')));
      
      // Extract domain terms from station and labels
      if (cell.row_label) terms.add(cell.row_label);
      if (cell.col_label) terms.add(cell.col_label);
    }
    
    return Array.from(terms).sort(); // Stable ordering
  }
}