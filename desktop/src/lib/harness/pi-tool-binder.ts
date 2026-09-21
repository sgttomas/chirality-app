import type { ToolDefinition } from '@earendil-works/pi-coding-agent';
import type { ImageContent, TextContent } from '@modelcontextprotocol/sdk/types.js';
import type { ChiralityToolDefinition } from './chirality-tool-bridge';

export type BoundPiChiralityTool = ToolDefinition<any, {
  source: 'chirality-tool-bridge';
  chiralityToolName: string;
  toolUseId: string;
}> & {
  chirality: {
    descriptorName: string;
    permissions: readonly string[];
    pathScope: string;
    readOnly: boolean;
    evidenceSource: 'chirality-tool-bridge';
  };
};

function assertUniqueDefinitions(definitions: readonly ChiralityToolDefinition[]): void {
  const names = new Set<string>();
  for (const definition of definitions) {
    if (names.has(definition.name)) {
      throw new Error(`Duplicate Chirality tool definition '${definition.name}'.`);
    }
    names.add(definition.name);
  }
}

function modelContent(
  toolName: string,
  content: readonly unknown[]
): Array<TextContent | ImageContent> {
  return content.map((item) => {
    if (
      item &&
      typeof item === 'object' &&
      (item as { type?: unknown }).type === 'text' &&
      typeof (item as { text?: unknown }).text === 'string'
    ) {
      return item as TextContent;
    }
    if (
      item &&
      typeof item === 'object' &&
      (item as { type?: unknown }).type === 'image' &&
      typeof (item as { data?: unknown }).data === 'string' &&
      typeof (item as { mimeType?: unknown }).mimeType === 'string'
    ) {
      return item as ImageContent;
    }
    throw new Error(`Chirality tool '${toolName}' returned unsupported model content.`);
  });
}

export function bindChiralityToolsForPi(
  definitions: readonly ChiralityToolDefinition[]
): BoundPiChiralityTool[] {
  assertUniqueDefinitions(definitions);
  return definitions.map((definition) => ({
    name: definition.name,
    label: definition.label,
    description: definition.description,
    parameters: definition.inputSchema as BoundPiChiralityTool['parameters'],
    executionMode: 'parallel',
    chirality: {
      descriptorName: definition.permission.descriptorName,
      permissions: [...definition.permission.permissions],
      pathScope: definition.permission.pathScope,
      readOnly:
        definition.permission.permissions.length === 1 &&
        definition.permission.permissions[0] === 'read',
      evidenceSource: definition.evidence.source
    },
    execute: async (toolUseId, params, signal) => {
      const result = await definition.execute(params, { toolUseId, signal });
      return {
        content: modelContent(definition.name, result.content),
        details: {
          source: 'chirality-tool-bridge',
          chiralityToolName: definition.name,
          toolUseId
        }
      };
    }
  }));
}
