/**
 * Station S3 Prompt: Epistemic Modality
 * 
 * Generates knowledge claims and evidence requirements.
 * Produces X (Solution Template) v1 document.
 */
import { MatrixCell } from '../../../src/types/framework';
import { StationInput, StationPrompt } from './station-template';

export class S3Prompt implements StationPrompt {
  station: 'S3' = 'S3';
  modality: 'epistemic' = 'epistemic';
  expectedOutput: 'document' = 'document';
  requiresRiskAssessment = false;

  buildPrompt(input: StationInput): string {
    let prompt = 'Analyze the following problem statement and initial requirements. ';
    prompt += 'Based on this, generate a set of knowledge claims and evidence requirements that would be necessary to formulate a complete solution. ';
    prompt += 'Focus on identifying key entities, their relationships, and the assertions that must be true for a solution to be valid.\n\n';

    prompt += 'Problem Statement: ' + input.problem.statement + '\n';

    if (input.matrixInjection?.X) {
      prompt += '\nConsider the following verification criteria from the X-Matrix:\n';
      input.matrixInjection.X.forEach((cell: MatrixCell) => {
        prompt += `- ${cell.text}\n`;
      });
    }

    prompt += '\nReturn your analysis as an array of JSON objects conforming to the X (Solution Template) structure.';
    return prompt;
  }
}