import { SemanticContext, LLMService, LLMRequest } from '../llm/service';

export interface StationResult {
  output: string;
  tokens?: {
    prompt: number;
    completion: number;
    total: number;
  };
}

export async function processS1(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  const request = {
    modality: 'problem' as const,
    operation: 'Problem Statement Analysis (J Operation)',
    context,
    systemPrompt: `You are performing J Operation: Problem Statement Analysis. Analyze the problem statement to:

1. Parse the problem semantically and identify core components
2. Categorize the problem by domain, complexity, and scope
3. Extract key constraints, requirements, and success criteria
4. Identify stakeholders and their needs
5. Determine the problem context and environment

Generate a structured analysis that will guide the subsequent document generation phases.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Problem Analysis (J Operation):

${llmResponse.content}

---
Ontological Modality: Problem
Semantic Operation: J (Problem Statement Analysis)
Status: Analysis complete - ready for systematic document generation`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S1] LLM problem analysis failed:', error);
    
    // Fallback to structured placeholder
    const output = `Problem Analysis (J Operation) - Fallback:

Problem Statement: "${context.problemStatement}"

STRUCTURAL ANALYSIS:
- Core Issue: Extracted from problem statement
- Constraints: Identified limitations and boundaries  
- Requirements: Key needs that must be addressed
- Success Criteria: How to measure problem resolution

CATEGORIZATION:
- Domain: Problem area classification
- Complexity: Assessment of solution difficulty
- Scope: Range of impact and stakeholders affected

NEXT STEPS:
- Data requirements analysis (Matrix C)
- Procedure development (Matrix D)
- Guidance generation (Matrix X)
- Evaluation criteria (Matrix E)

---
Ontological Modality: Problem
Semantic Operation: J (Problem Statement Analysis)
Status: Fallback analysis - LLM generation failed
Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}