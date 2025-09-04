// Risk table export - generates FMEA-like risk analysis from evaluation and guidance matrices
import type { MatrixCell } from '@/types/framework';

export interface RiskTableRow {
  id: string;
  failure_mode: string;
  effect: string;
  cause: string;
  severity: number;      // 1-10 scale
  occurrence: number;    // 1-10 scale  
  detection: number;     // 1-10 scale
  rpn: number;          // Risk Priority Number (S × O × D)
  current_controls?: string;
  recommended_actions?: string;
  source_matrix: 'E' | 'M';
  source_cell_id: string;
}

export interface RiskTableResult {
  json: RiskTableRow[];
  csv: string;
}

/**
 * Generate FMEA-style risk table from evaluation (E) and guidance (M) matrices
 * E matrix: evaluation summaries with risk indicators
 * M matrix: guidance statements with risk mitigations
 */
export function generateRiskTable(matrices: { E: MatrixCell[]; M: MatrixCell[] }): RiskTableResult {
  const riskRows: RiskTableRow[] = [];
  
  // Step 1: Extract risks from E matrix (evaluation/assessment data)
  const evaluationRisks = extractRisksFromEvaluationMatrix(matrices.E);
  riskRows.push(...evaluationRisks);
  
  // Step 2: Extract risks from M matrix (guidance/mitigation data)  
  const guidanceRisks = extractRisksFromGuidanceMatrix(matrices.M);
  riskRows.push(...guidanceRisks);
  
  // Step 3: Sort by RPN (Risk Priority Number) descending
  riskRows.sort((a, b) => b.rpn - a.rpn);
  
  // Step 4: Generate CSV output
  const csvString = generateCSV(riskRows);
  
  return {
    json: riskRows,
    csv: csvString
  };
}

/**
 * Extract risk information from evaluation matrix
 * E matrix contains evaluation summaries that may identify failure modes and effects
 */
function extractRisksFromEvaluationMatrix(eCells: MatrixCell[]): RiskTableRow[] {
  const risks: RiskTableRow[] = [];
  
  for (const cell of eCells) {
    // Look for risk-related text patterns in evaluation content
    const riskIndicators = findRiskIndicators(cell.text);
    
    for (let i = 0; i < riskIndicators.length; i++) {
      const indicator = riskIndicators[i];
      
      const risk: RiskTableRow = {
        id: `${cell.id}_risk_${i + 1}`,
        failure_mode: indicator.failureMode,
        effect: indicator.effect || 'Impact to be determined',
        cause: indicator.cause || 'Root cause analysis required',
        severity: estimateSeverity(indicator.failureMode, cell.text),
        occurrence: estimateOccurrence(indicator.failureMode, cell.text),
        detection: estimateDetection(indicator.failureMode, cell.text),
        rpn: 0, // Will be calculated below
        current_controls: extractCurrentControls(cell.text),
        recommended_actions: extractRecommendedActions(cell.text),
        source_matrix: 'E',
        source_cell_id: cell.id
      };
      
      // Calculate RPN
      risk.rpn = risk.severity * risk.occurrence * risk.detection;
      
      risks.push(risk);
    }
  }
  
  return risks;
}

/**
 * Extract risk information from guidance matrix
 * M matrix contains mitigation guidance that implies risks being addressed
 */
function extractRisksFromGuidanceMatrix(mCells: MatrixCell[]): RiskTableRow[] {
  const risks: RiskTableRow[] = [];
  
  for (const cell of mCells) {
    // Look for mitigation statements that imply underlying risks
    const mitigationIndicators = findMitigationIndicators(cell.text);
    
    for (let i = 0; i < mitigationIndicators.length; i++) {
      const indicator = mitigationIndicators[i];
      
      const risk: RiskTableRow = {
        id: `${cell.id}_mitigation_${i + 1}`,
        failure_mode: indicator.impliedFailure,
        effect: indicator.potentialEffect || 'Negative impact on system',
        cause: indicator.rootCause || 'Underlying system vulnerability',
        severity: estimateSeverity(indicator.impliedFailure, cell.text),
        occurrence: estimateOccurrence(indicator.impliedFailure, cell.text),
        detection: estimateDetection(indicator.impliedFailure, cell.text),
        rpn: 0, // Will be calculated below
        current_controls: indicator.mitigationMeasure,
        recommended_actions: extractRecommendedActions(cell.text),
        source_matrix: 'M',
        source_cell_id: cell.id
      };
      
      // Calculate RPN
      risk.rpn = risk.severity * risk.occurrence * risk.detection;
      
      risks.push(risk);
    }
  }
  
  return risks;
}

/**
 * Find risk indicators in evaluation text
 */
function findRiskIndicators(text: string): Array<{ failureMode: string; effect?: string; cause?: string }> {
  const indicators = [];
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
  
  for (const sentence of sentences) {
    const trimmed = sentence.trim();
    
    // Look for explicit failure mode language
    if (/\\b(?:risk|fail|error|problem|issue|concern|weakness|vulnerability)\\b/i.test(trimmed)) {
      const failureMode = extractFailureMode(trimmed);
      const effect = extractEffect(trimmed);
      const cause = extractCause(trimmed);
      
      if (failureMode) {
        indicators.push({ 
          failureMode, 
          effect: effect || undefined, 
          cause: cause || undefined 
        });
      }
    }
  }
  
  return indicators;
}

/**
 * Find mitigation indicators that imply risks
 */
function findMitigationIndicators(text: string): Array<{ impliedFailure: string; potentialEffect?: string; rootCause?: string; mitigationMeasure: string }> {
  const indicators = [];
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
  
  for (const sentence of sentences) {
    const trimmed = sentence.trim();
    
    // Look for mitigation language that implies risks
    if (/\\b(?:should|must|ensure|prevent|avoid|mitigate|control|guard|protect)\\b/i.test(trimmed)) {
      const impliedFailure = extractImpliedFailure(trimmed);
      const mitigationMeasure = trimmed;
      
      if (impliedFailure) {
        indicators.push({
          impliedFailure,
          mitigationMeasure,
          potentialEffect: extractPotentialEffect(trimmed) || undefined,
          rootCause: extractRootCause(trimmed) || undefined
        });
      }
    }
  }
  
  return indicators;
}

/**
 * Extract failure mode description from text
 */
function extractFailureMode(text: string): string | null {
  // Look for specific failure patterns
  const patterns = [
    /(?:risk of|failure to|unable to|cannot|fails to)\\s+([^,]+)/i,
    /(?:problem with|issue with)\\s+([^,]+)/i,
    /([^\\s]+)\\s+(?:fails|breaks|malfunctions|errors)/i
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  // Fallback: use first part of sentence
  return text.substring(0, 80).trim() + (text.length > 80 ? '...' : '');
}

/**
 * Extract effect description from text
 */
function extractEffect(text: string): string | null {
  const effectPatterns = [
    /(?:resulting in|leads to|causes|impacts?)\\s+([^,]+)/i,
    /effect[:\\s]+([^,]+)/i
  ];
  
  for (const pattern of effectPatterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  return null;
}

/**
 * Extract cause description from text
 */
function extractCause(text: string): string | null {
  const causePatterns = [
    /(?:due to|because of|caused by|stems from)\\s+([^,]+)/i,
    /cause[:\\s]+([^,]+)/i
  ];
  
  for (const pattern of causePatterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  return null;
}

/**
 * Extract implied failure from mitigation text
 */
function extractImpliedFailure(text: string): string | null {
  const patterns = [
    /prevent\\s+([^,]+)/i,
    /avoid\\s+([^,]+)/i,
    /ensure\\s+(?:no|not)\\s+([^,]+)/i,
    /guard against\\s+([^,]+)/i
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  return null;
}

/**
 * Extract potential effect from mitigation text
 */
function extractPotentialEffect(text: string): string | null {
  if (/\\b(?:security|breach|unauthorized)\\b/i.test(text)) {
    return 'Security compromise';
  }
  if (/\\b(?:performance|slow|delay)\\b/i.test(text)) {
    return 'Performance degradation';
  }
  if (/\\b(?:data|loss|corruption)\\b/i.test(text)) {
    return 'Data integrity impact';
  }
  
  return null;
}

/**
 * Extract root cause from mitigation text
 */
function extractRootCause(text: string): string | null {
  if (/\\b(?:configuration|setup|install)\\b/i.test(text)) {
    return 'Configuration issue';
  }
  if (/\\b(?:user|human|operator)\\b/i.test(text)) {
    return 'Human error';
  }
  if (/\\b(?:system|technical|software)\\b/i.test(text)) {
    return 'Technical failure';
  }
  
  return null;
}

/**
 * Estimate severity on 1-10 scale based on text content
 */
function estimateSeverity(failureMode: string, context: string): number {
  const text = (failureMode + ' ' + context).toLowerCase();
  
  if (/\\b(?:catastrophic|critical|fatal|severe)\\b/.test(text)) return 9;
  if (/\\b(?:major|significant|serious)\\b/.test(text)) return 7;
  if (/\\b(?:moderate|medium)\\b/.test(text)) return 5;
  if (/\\b(?:minor|low|small)\\b/.test(text)) return 3;
  
  // Default moderate severity
  return 5;
}

/**
 * Estimate occurrence probability on 1-10 scale
 */
function estimateOccurrence(failureMode: string, context: string): number {
  const text = (failureMode + ' ' + context).toLowerCase();
  
  if (/\\b(?:frequent|often|regularly|common)\\b/.test(text)) return 8;
  if (/\\b(?:occasional|sometimes|periodic)\\b/.test(text)) return 5;
  if (/\\b(?:rare|unlikely|seldom)\\b/.test(text)) return 2;
  
  // Default moderate occurrence
  return 4;
}

/**
 * Estimate detection capability on 1-10 scale (higher = harder to detect)
 */
function estimateDetection(failureMode: string, context: string): number {
  const text = (failureMode + ' ' + context).toLowerCase();
  
  if (/\\b(?:hidden|undetectable|silent)\\b/.test(text)) return 9;
  if (/\\b(?:difficult|hard to detect)\\b/.test(text)) return 7;
  if (/\\b(?:monitoring|alerts|visible)\\b/.test(text)) return 3;
  if (/\\b(?:obvious|clear|evident)\\b/.test(text)) return 2;
  
  // Default moderate detection difficulty
  return 5;
}

/**
 * Extract current control measures from text
 */
function extractCurrentControls(text: string): string | undefined {
  const controlPatterns = [
    /current[ly]?\\s+(?:controls?|measures?)\\s*:?\\s*([^.]+)/i,
    /(?:mitigat|control)(?:ed|ing|ion)\\s+by\\s+([^.]+)/i
  ];
  
  for (const pattern of controlPatterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  return undefined;
}

/**
 * Extract recommended actions from text
 */
function extractRecommendedActions(text: string): string | undefined {
  const actionPatterns = [
    /recommend(?:ed|ation)?\\s*:?\\s*([^.]+)/i,
    /should\\s+([^.]+)/i,
    /action\\s*:?\\s*([^.]+)/i
  ];
  
  for (const pattern of actionPatterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  
  return undefined;
}

/**
 * Generate CSV string from risk table rows
 */
function generateCSV(risks: RiskTableRow[]): string {
  const headers = [
    'ID',
    'Failure Mode',
    'Effect',
    'Cause',
    'Severity',
    'Occurrence', 
    'Detection',
    'RPN',
    'Current Controls',
    'Recommended Actions',
    'Source Matrix',
    'Source Cell ID'
  ];
  
  const csvRows = [headers.join(',')];
  
  for (const risk of risks) {
    const row = [
      escapeCSV(risk.id),
      escapeCSV(risk.failure_mode),
      escapeCSV(risk.effect),
      escapeCSV(risk.cause),
      risk.severity.toString(),
      risk.occurrence.toString(),
      risk.detection.toString(),
      risk.rpn.toString(),
      escapeCSV(risk.current_controls || ''),
      escapeCSV(risk.recommended_actions || ''),
      risk.source_matrix,
      escapeCSV(risk.source_cell_id)
    ];
    
    csvRows.push(row.join(','));
  }
  
  return csvRows.join('\\n');
}

/**
 * Escape CSV field values
 */
function escapeCSV(value: string): string {
  if (!value) return '';
  
  // If contains comma, newline, or quote, wrap in quotes and escape internal quotes
  if (value.includes(',') || value.includes('\\n') || value.includes('"')) {
    return '"' + value.replace(/"/g, '""') + '"';
  }
  
  return value;
}