// V&V scaffolds - generates verification and validation checklists with coverage metrics
import type { SP } from '@/chirality-core/contracts';
import type { MatrixCell } from '@/types/framework';

export interface VVCoverageResult {
  sp: SP;
  coverage: {
    covered: number;
    total: number;
    percent: number;
  };
}

/**
 * Generate V&V checklist by mapping requirements to verification steps
 * From D objectives and X verification criteria, ensure each requirement has verification coverage
 */
export function generateVVChecklist(matrices: { C: MatrixCell[]; D: MatrixCell[]; X: MatrixCell[] }): VVCoverageResult {
  // Step 1: Extract requirements from C matrix (if available) or derive from D objectives
  const requirements = extractRequirements(matrices.C, matrices.D);
  
  // Step 2: Extract verification steps from X matrix and D objectives
  const verificationSteps = extractVerificationSteps(matrices.X, matrices.D);
  
  // Step 3: Map requirements to verification steps for coverage analysis
  const { mappedRequirements, unmappedCount } = mapRequirementsToVerification(requirements, verificationSteps);
  
  // Step 4: Build SP structure for verification procedure
  const sp: SP = {
    step: 'verification_and_validation_checklist',
    purpose: 'Ensure all requirements are verified through systematic testing and validation',
    inputs: [
      'System requirements from analysis',
      'Verification criteria from design',
      'Test objectives from objectives matrix'
    ],
    outputs: [
      'Verification checklist with coverage metrics',
      'Requirement traceability matrix',
      'Test completion status'
    ],
    preconditions: [
      'Requirements have been documented and reviewed',
      'Verification criteria have been established',
      'Test environment is available'
    ],
    postconditions: [
      'All requirements have associated verification steps',
      'Coverage metrics are calculated and documented',
      'Verification gaps are identified and addressed'
    ],
    refs: [
      ...matrices.C.flatMap(cell => [...cell.refs, ...cell.citations]),
      ...matrices.D.flatMap(cell => [...cell.refs, ...cell.citations]),
      ...matrices.X.flatMap(cell => [...cell.refs, ...cell.citations])
    ]
  };
  
  // Step 5: Calculate coverage statistics
  const totalRequirements = requirements.length;
  const coveredRequirements = totalRequirements - unmappedCount;
  const coveragePercent = totalRequirements > 0 
    ? Math.round((coveredRequirements / totalRequirements) * 100)
    : 100;
  
  return {
    sp,
    coverage: {
      covered: coveredRequirements,
      total: totalRequirements,
      percent: coveragePercent
    }
  };
}

/**
 * Extract requirements from C matrix or derive from D objectives
 */
function extractRequirements(cCells: MatrixCell[], dCells: MatrixCell[]): Array<{ id: string; text: string; source: 'C' | 'D' }> {
  const requirements: Array<{ id: string; text: string; source: 'C' | 'D' }> = [];
  
  // Primary source: C matrix requirements
  for (const cell of cCells) {
    if (cell.text && cell.text.length > 10) {
      requirements.push({
        id: cell.id,
        text: cell.text,
        source: 'C'
      });
    }
  }
  
  // Fallback: derive requirements from D objectives if C matrix is sparse
  if (requirements.length === 0) {
    for (const cell of dCells) {
      // Look for objective statements that imply requirements
      if (/\\b(?:must|shall|should|requires?)\\b/i.test(cell.text)) {
        requirements.push({
          id: `${cell.id}_req`,
          text: cell.text,
          source: 'D'
        });
      }
    }
  }
  
  return requirements;
}

/**
 * Extract verification steps from X matrix and D objectives
 */
function extractVerificationSteps(xCells: MatrixCell[], dCells: MatrixCell[]): Array<{ id: string; text: string; keywords: string[] }> {
  const steps: Array<{ id: string; text: string; keywords: string[] }> = [];
  
  // Primary source: X matrix verification criteria
  for (const cell of xCells) {
    const keywords = extractVerificationKeywords(cell.text);
    if (keywords.length > 0) {
      steps.push({
        id: cell.id,
        text: cell.text,
        keywords
      });
    }
  }
  
  // Secondary source: test-related objectives from D matrix
  for (const cell of dCells) {
    if (/\\b(?:test|verify|validate|check|confirm)\\b/i.test(cell.text)) {
      const keywords = extractVerificationKeywords(cell.text);
      steps.push({
        id: `${cell.id}_verify`,
        text: cell.text,
        keywords
      });
    }
  }
  
  return steps;
}

/**
 * Extract verification keywords from text for mapping
 */
function extractVerificationKeywords(text: string): string[] {
  const keywords = new Set<string>();
  
  // Extract technical terms
  const technicalTerms = text.match(/\\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\\b/g) || [];
  technicalTerms.forEach(term => keywords.add(term.toLowerCase()));
  
  // Extract action words
  const actionWords = text.match(/\\b(?:test|verify|validate|check|confirm|ensure|measure|assess|evaluate)\\b/gi) || [];
  actionWords.forEach(action => keywords.add(action.toLowerCase()));
  
  // Extract domain concepts
  const domainTerms = text.match(/"([^"]+)"/g) || [];
  domainTerms.forEach(quoted => keywords.add(quoted.replace(/"/g, '').toLowerCase()));
  
  return Array.from(keywords);
}

/**
 * Map requirements to verification steps based on keyword overlap and semantic similarity
 */
function mapRequirementsToVerification(
  requirements: Array<{ id: string; text: string; source: 'C' | 'D' }>,
  verificationSteps: Array<{ id: string; text: string; keywords: string[] }>
): { mappedRequirements: Array<{ requirement: any; verificationSteps: any[] }>; unmappedCount: number } {
  const mappedRequirements = [];
  let unmappedCount = 0;
  
  for (const requirement of requirements) {
    const reqKeywords = extractVerificationKeywords(requirement.text);
    const matchingSteps = [];
    
    // Find verification steps with keyword overlap
    for (const step of verificationSteps) {
      const overlap = calculateKeywordOverlap(reqKeywords, step.keywords);
      
      // Consider it a match if there's significant keyword overlap or semantic indicators
      if (overlap > 0.3 || hasSemanticMatch(requirement.text, step.text)) {
        matchingSteps.push({
          ...step,
          overlapScore: overlap
        });
      }
    }
    
    // Sort by overlap score and take top matches
    matchingSteps.sort((a, b) => b.overlapScore - a.overlapScore);
    
    if (matchingSteps.length > 0) {
      mappedRequirements.push({
        requirement,
        verificationSteps: matchingSteps.slice(0, 3) // Top 3 matches
      });
    } else {
      unmappedCount++;
    }
  }
  
  return { mappedRequirements, unmappedCount };
}

/**
 * Calculate keyword overlap between requirement and verification step
 */
function calculateKeywordOverlap(reqKeywords: string[], stepKeywords: string[]): number {
  if (reqKeywords.length === 0 || stepKeywords.length === 0) {
    return 0;
  }
  
  const reqSet = new Set(reqKeywords);
  const stepSet = new Set(stepKeywords);
  const intersection = new Set([...reqSet].filter(k => stepSet.has(k)));
  
  const union = new Set([...reqSet, ...stepSet]);
  
  return intersection.size / union.size;
}

/**
 * Check for semantic matches between requirement and verification text
 */
function hasSemanticMatch(requirementText: string, verificationText: string): boolean {
  const req = requirementText.toLowerCase();
  const ver = verificationText.toLowerCase();
  
  // Look for direct semantic relationships
  const semanticPairs = [
    { req: /\\bstore\\b/, ver: /\\b(?:retrieve|query|database)\\b/ },
    { req: /\\bsecurity\\b/, ver: /\\b(?:authentication|authorization|encrypt)\\b/ },
    { req: /\\bperformance\\b/, ver: /\\b(?:speed|latency|throughput)\\b/ },
    { req: /\\binterface\\b/, ver: /\\b(?:ui|user|interaction)\\b/ },
    { req: /\\bdata\\b/, ver: /\\b(?:input|output|validation)\\b/ }
  ];
  
  for (const pair of semanticPairs) {
    if (pair.req.test(req) && pair.ver.test(ver)) {
      return true;
    }
  }
  
  return false;
}