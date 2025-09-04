import { SemanticContext, LLMService } from '../llm/service';
import { StationResult } from './S1';

export async function processS11(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  // Simple resolution generator using prompt engineering
  const request = {
    modality: 'resolution' as const,
    operation: 'Final Resolution',
    context,
    systemPrompt: `You are generating a final resolution to a problem statement. Synthesize all available documents into a coherent, actionable solution.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Final Resolution:

Problem Statement: "${context.problemStatement}"

SOLUTION:
${llmResponse.content}

---
Generated using semantic synthesis of:
- ${context.dataSheet ? 'Data Sheet' : '(No Data Sheet)'}
- ${context.standardProcedure ? 'Standard Procedure' : '(No Standard Procedure)'}
- ${context.guidanceDocument ? 'Guidance Document' : '(No Guidance Document)'}  
- ${context.evaluationChecklist ? 'Evaluation Checklist' : '(No Evaluation Checklist)'}
- ${context.solutionStatements ? 'Solution Statements' : '(No Solution Statements)'}`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S11] LLM resolution generation failed:', error);
    
    // Fallback to simple synthesis
    const output = `Final Resolution (Fallback):

Problem Statement: "${context.problemStatement}"

Based on the available documents, a resolution has been synthesized. However, LLM generation failed.

Available Context:
${context.dataSheet ? `- Data Sheet: Present\n` : ''}${context.standardProcedure ? `- Standard Procedure: Present\n` : ''}${context.guidanceDocument ? `- Guidance Document: Present\n` : ''}${context.evaluationChecklist ? `- Evaluation Checklist: Present\n` : ''}${context.solutionStatements ? `- Solution Statements: Present\n` : ''}

Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}