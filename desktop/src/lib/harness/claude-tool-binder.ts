import {
  tool,
  type SdkMcpToolDefinition
} from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod/v4';
import type { ChiralityToolDefinition } from './chirality-tool-bridge';

function assertUniqueDefinitions(definitions: readonly ChiralityToolDefinition[]): void {
  const names = new Set<string>();
  for (const definition of definitions) {
    if (names.has(definition.name)) {
      throw new Error(`Duplicate Chirality tool definition '${definition.name}'.`);
    }
    names.add(definition.name);
  }
}

export function bindChiralityToolsForClaude(
  definitions: readonly ChiralityToolDefinition[]
): SdkMcpToolDefinition<any>[] {
  assertUniqueDefinitions(definitions);
  return definitions.map((definition) => {
    const schema = z.fromJSONSchema(definition.inputSchema);
    if (!(schema instanceof z.ZodObject)) {
      throw new Error(`Chirality tool '${definition.name}' must use an object input schema.`);
    }
    return tool(
      definition.name,
      definition.description,
      schema.shape,
      (args) => definition.execute(args)
    );
  });
}
