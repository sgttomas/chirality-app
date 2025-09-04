import { SemanticContext, LLMService } from '../llm/service';
import { StationResult } from './S1';

export async function processS5(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  const request = {
    modality: 'process' as const,
    operation: 'Evaluation Checklist Generation (EC from Matrix E)',
    context,
    matrixGuidance: initialVector?.matrixE || [],
    systemPrompt: `You are performing EC Operation: Evaluation Checklist Generation using Matrix E elements. Create a comprehensive evaluation checklist that:

1. Defines step-by-step evaluation procedures and validation processes
2. Identifies critical areas and criteria for task/problem completion
3. Establishes measurable checkpoints and quality control processes
4. Creates systematic verification workflows and testing procedures
5. Maps evaluation processes to all prior documents (J, DS, SP, GD)
6. Provides operational framework for assessing solution effectiveness

Generate an evaluation checklist focused on procedural validation and process control.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Evaluation Checklist (EC from Matrix E):

${llmResponse.content}

---
Ontological Modality: Process
Semantic Operation: EC (Evaluation Checklist Generation from Matrix E)
Status: Evaluation processes defined - ready for resolution synthesis`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S5] LLM evaluation checklist generation failed:', error);
    
    // Fallback to structured template
    const output = `Evaluation Checklist (EC from Matrix E) - Fallback:

Based on Problem Analysis, Data Sheet, Standard Procedure, and Guidance Document:

EVALUATION PROCEDURES:

Phase 1: Pre-Evaluation Setup
□ Gather all documentation from J, DS, SP, and GD operations
□ Prepare evaluation environment and testing resources
□ Assemble evaluation team and assign responsibilities
□ Establish evaluation timeline and milestone checkpoints

Phase 2: Problem Resolution Validation Process
□ Execute systematic review of problem statement coverage
□ Validate solution completeness against original requirements
□ Test solution effectiveness using defined success criteria
□ Verify stakeholder needs are addressed through solution

Phase 3: Data and Information Validation Process
□ Execute data quality verification procedures from Data Sheet
□ Validate data collection processes and information accuracy
□ Test data sources for reliability and current validity
□ Verify derived calculations and data transformation processes

Phase 4: Procedure Compliance Validation Process
□ Execute step-by-step review of Standard Procedure adherence
□ Validate prerequisite completion and dependency management
□ Test decision point logic and branching procedures
□ Verify risk mitigation implementation and effectiveness

Phase 5: Strategic Guidance Implementation Process
□ Execute review of guidance document recommendation integration
□ Validate contextual considerations and impact assessments
□ Test long-term sustainability and scalability procedures
□ Verify organizational alignment and stakeholder engagement processes

Phase 6: Quality Assurance and Final Validation Process
□ Execute comprehensive solution testing procedures
□ Validate functional and non-functional requirement compliance
□ Test security, compliance, and governance implementation
□ Execute user acceptance testing and feedback incorporation procedures

PROCESS CONTROL CHECKPOINTS:
- Document completion and accuracy verification procedures
- Stakeholder sign-off and approval processes
- Independent review and audit procedures
- Testing and validation execution workflows
- Issue tracking and resolution processes

---
Ontological Modality: Process
Semantic Operation: EC (Evaluation Checklist Generation from Matrix E)
Status: Fallback evaluation processes - LLM generation failed
Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}