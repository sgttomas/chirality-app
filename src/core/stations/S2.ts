import { SemanticContext, LLMService } from '../llm/service';
import { StationResult } from './S1';

export async function processS2(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  const request = {
    modality: 'systematic' as const,
    operation: 'Data Sheet Generation (DS from Matrix C)',
    context,
    matrixGuidance: initialVector?.matrixC || [],
    systemPrompt: `You are performing DS Operation: Data Sheet Generation using Matrix C elements. Create a comprehensive data specification that:

1. Defines all required user inputs and data sources needed for problem resolution
2. Categorizes data by priority (primary, supporting, validation)
3. Specifies data formats, structures, and validation criteria
4. Identifies data collection methods and sources
5. Establishes data quality standards and verification procedures
6. Maps data requirements to problem components from the J Operation analysis

Generate a systematic data sheet that serves as the foundation for all subsequent processing.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Data Sheet (DS from Matrix C):

${llmResponse.content}

---
Ontological Modality: Systematic
Semantic Operation: DS (Data Sheet Generation from Matrix C)
Status: Data requirements systematically defined - ready for procedure development`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S2] LLM data sheet generation failed:', error);
    
    // Fallback to structured template
    const output = `Data Sheet (DS from Matrix C) - Fallback:

Based on Problem Analysis: "${context.problemStatement}"

REQUIRED DATA INPUTS:
- Primary Data: Core information essential for problem resolution
- Supporting Data: Additional context and background information
- Validation Data: Information needed to verify solution effectiveness

DATA CATEGORIES:
1. User Inputs: Information to be provided by stakeholders
2. System Data: Information available from existing systems
3. External Data: Information required from outside sources
4. Derived Data: Information calculated from other data sources

DATA SPECIFICATIONS:
- Format Requirements: How data should be structured
- Quality Standards: Accuracy, completeness, timeliness criteria
- Collection Methods: How to gather required information
- Validation Procedures: How to verify data quality

DATA SOURCES:
- Internal systems and databases
- User interviews and surveys
- External APIs and services
- Documentation and records

---
Ontological Modality: Systematic
Semantic Operation: DS (Data Sheet Generation from Matrix C)
Status: Fallback data sheet - LLM generation failed
Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}