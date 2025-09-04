import { SemanticContext, LLMService } from '../llm/service';
import { StationResult } from './S1';

export async function processS4(
  context: SemanticContext,
  llmService: LLMService,
  initialVector?: Record<string, any>
): Promise<StationResult> {
  
  const request = {
    modality: 'epistemic' as const,
    operation: 'Guidance Document Generation (GD from Matrix X)',
    context,
    matrixGuidance: initialVector?.matrixX || [],
    systemPrompt: `You are performing GD Operation: Guidance Document Generation using Matrix X elements. Create comprehensive strategic guidance that:

1. Analyzes prerequisites, dependencies, and successors for the solution
2. Provides strategic recommendations and best practices
3. Identifies risks, challenges, and mitigation strategies
4. Establishes quality standards and success criteria
5. Integrates the solution within wider organizational/system context
6. Connects procedural steps to strategic knowledge and decision-making

Generate epistemic guidance that elevates the procedural workflow to strategic knowledge.`
  };

  try {
    const llmResponse = await llmService.generateSemanticContent(request);
    
    const output = `Guidance Document (GD from Matrix X):

${llmResponse.content}

---
Ontological Modality: Epistemic
Semantic Operation: GD (Guidance Document Generation from Matrix X)
Status: Strategic guidance integrated - ready for evaluation framework`;

    return {
      output,
      tokens: llmResponse.tokens
    };
    
  } catch (error) {
    console.error('[S4] LLM guidance document generation failed:', error);
    
    // Fallback to structured template
    const output = `Guidance Document (GD from Matrix X) - Fallback:

Based on Problem Analysis, Data Sheet, and Standard Procedure:

CONTEXTUAL ANALYSIS:

Prerequisites:
- Organizational readiness and stakeholder alignment
- Technical infrastructure and resource availability
- Data quality standards and validation procedures
- Process maturity and capability assessment

Dependencies:
- External system integrations and APIs
- Third-party service availability and reliability
- Regulatory compliance and approval processes
- Stakeholder participation and cooperation

Successors:
- Solution deployment and rollout activities
- User training and change management programs
- Performance monitoring and optimization cycles
- Future enhancement and evolution planning

STRATEGIC GUIDANCE:

Approach Recommendations:
- Adopt iterative development and validation cycles
- Implement robust testing and quality assurance practices
- Establish clear communication channels with stakeholders
- Maintain comprehensive documentation throughout process

Risk Considerations:
- Technical risks: system failures, integration issues, performance problems
- Process risks: resource constraints, timeline pressures, scope creep
- Organizational risks: resistance to change, skill gaps, competing priorities
- External risks: market changes, regulatory shifts, vendor dependencies

Quality Standards:
- Solution must meet functional and non-functional requirements
- Documentation must be complete, accurate, and maintainable
- User experience must meet accessibility and usability standards
- Security and compliance requirements must be fully satisfied

WIDER CONTEXT INTEGRATION:

Organizational Impact:
- Alignment with strategic objectives and business priorities
- Integration with existing systems and processes
- Impact on organizational culture and ways of working
- Resource allocation and budget considerations

Long-term Implications:
- Scalability and extensibility requirements
- Evolution pathway and upgrade planning
- Knowledge transfer and capability building
- Lessons learned and best practice capture

---
Ontological Modality: Epistemic
Semantic Operation: GD (Guidance Document Generation from Matrix X)
Status: Fallback guidance - LLM generation failed
Error: ${error instanceof Error ? error.message : 'Unknown error'}`;

    return {
      output,
      tokens: { prompt: 0, completion: 0, total: 0 }
    };
  }
}