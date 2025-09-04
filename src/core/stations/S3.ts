import { SemanticContext, LLMService } from '../llm/service';
import { StationResult } from './S1';

export async function processS3(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  const request = {
    modality: 'process' as const,
    operation: 'Standard Procedure Generation (SP from Matrix D)',
    context,
    matrixGuidance: initialVector?.matrixD || [],
    systemPrompt: `You are performing SP Operation: Standard Procedure Generation using Matrix D elements. Create a comprehensive procedural workflow that:

1. Defines step-by-step actionable procedures for problem resolution
2. Establishes clear prerequisites, resources, and success criteria
3. Identifies decision points and branching logic
4. Specifies roles, responsibilities, and timelines
5. Includes risk mitigation and error handling procedures
6. Maps procedural steps to data requirements from the DS Operation

Generate an operational procedure that transforms the systematic data sheet into actionable workflow.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Standard Procedure (SP from Matrix D):

${llmResponse.content}

---
Ontological Modality: Process
Semantic Operation: SP (Standard Procedure Generation from Matrix D)
Status: Procedural workflow defined - ready for guidance integration`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S3] LLM standard procedure generation failed:', error);
    
    // Fallback to structured template
    const output = `Standard Procedure (SP from Matrix D) - Fallback:

Based on Problem Analysis and Data Sheet:

PROCEDURAL WORKFLOW:

Phase 1: Setup and Preparation
- Gather required data inputs as specified in Data Sheet
- Verify prerequisites and resource availability
- Initialize processing environment

Phase 2: Data Collection and Validation
- Execute data collection procedures
- Apply validation criteria from Data Sheet
- Handle data quality issues and exceptions

Phase 3: Core Processing and Analysis
- Apply problem-specific analysis methods
- Process data according to systematic requirements
- Generate intermediate results and checkpoints

Phase 4: Solution Development
- Synthesize analysis results into solution components
- Validate solution against problem requirements
- Iterate and refine as needed

Phase 5: Implementation and Verification
- Deploy solution components
- Test against success criteria
- Document results and lessons learned

Phase 6: Delivery and Closure
- Prepare final deliverables
- Transfer knowledge to stakeholders
- Close out project activities

PROCESS FRAMEWORK:
- Prerequisites: Requirements that must be met before starting
- Resources: Personnel, tools, and systems needed
- Decision Points: Key checkpoints for go/no-go decisions
- Risk Mitigation: Identified risks and mitigation strategies
- Quality Gates: Validation points throughout process

---
Ontological Modality: Process
Semantic Operation: SP (Standard Procedure Generation from Matrix D)
Status: Fallback procedure - LLM generation failed
Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}