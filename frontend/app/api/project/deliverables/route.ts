import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export type Deliverable = {
  id: string;
  name: string;
  pkg: string;
  status: "open" | "in-progress" | "checking" | "issued";
  path: string;
};

export type KnowledgeTypeOption = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

type KnowledgeTypeAccumulator = {
  id: string;
  label: string;
  matchingDeliverableKeys: Set<string>;
};

const KNOWLEDGE_DECOMPOSITION_MARKER_REGEX = /(knowledge\s+categories?|knowledge\s+types?|knowledge\s+decomposition)/i;

const KNOWLEDGE_TYPE_DEFINITIONS: Array<{
  id: string;
  label: string;
  matches: (deliverablePath: string) => boolean;
}> = [
  {
    id: "datasheet",
    label: "Datasheet",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "Datasheet.md")),
  },
  {
    id: "specification",
    label: "Specification",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "Specification.md")),
  },
  {
    id: "guidance",
    label: "Guidance",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "Guidance.md")),
  },
  {
    id: "procedure",
    label: "Procedure",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "Procedure.md")),
  },
  {
    id: "dependencies",
    label: "Dependencies",
    matches: (deliverablePath) => {
      return (
        fs.existsSync(path.join(deliverablePath, "_DEPENDENCIES.md")) ||
        fs.existsSync(path.join(deliverablePath, "Dependencies.csv"))
      );
    },
  },
  {
    id: "references",
    label: "References",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "_REFERENCES.md")),
  },
  {
    id: "context",
    label: "Context",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "_CONTEXT.md")),
  },
  {
    id: "status",
    label: "Status",
    matches: (deliverablePath) => fs.existsSync(path.join(deliverablePath, "_STATUS.md")),
  },
  {
    id: "semantic",
    label: "Semantic",
    matches: (deliverablePath) => {
      return (
        fs.existsSync(path.join(deliverablePath, "_SEMANTIC.md")) ||
        fs.existsSync(path.join(deliverablePath, "_SEMANTIC_LENSING.md"))
      );
    },
  },
  {
    id: "memory",
    label: "Memory",
    matches: (deliverablePath) => {
      return fs.existsSync(path.join(deliverablePath, "_MEMORY.md")) || fs.existsSync(path.join(deliverablePath, "MEMORY.md"));
    },
  },
];

function getStatusFromContent(content: string): Deliverable["status"] {
  if (content.includes("ISSUED")) return "issued";
  if (content.includes("CHECKING")) return "checking";
  if (content.includes("IN_PROGRESS")) return "in-progress";
  return "open";
}

function detectKnowledgeDecomposition(rootPath: string): { enabled: boolean; markerFile: string | null } {
  const decompositionDir = path.join(rootPath, "_Decomposition");
  if (!fs.existsSync(decompositionDir)) {
    return { enabled: false, markerFile: null };
  }

  const stack = [decompositionDir];

  while (stack.length > 0) {
    const currentDir = stack.pop();
    if (!currentDir) {
      continue;
    }

    let entries: fs.Dirent[] = [];
    try {
      entries = fs.readdirSync(currentDir, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const entry of entries) {
      const entryPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        stack.push(entryPath);
        continue;
      }

      const lowerName = entry.name.toLowerCase();
      if (!lowerName.endsWith(".md") && !lowerName.endsWith(".txt")) {
        continue;
      }

      try {
        const content = fs.readFileSync(entryPath, "utf-8");
        if (KNOWLEDGE_DECOMPOSITION_MARKER_REGEX.test(content)) {
          return {
            enabled: true,
            markerFile: path.relative(rootPath, entryPath),
          };
        }
      } catch {
        // Non-readable files are skipped by design.
      }
    }
  }

  return { enabled: false, markerFile: null };
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const rootPath = searchParams.get("path");

  if (!rootPath || !fs.existsSync(rootPath)) {
    return NextResponse.json({ error: "Invalid project path" }, { status: 400 });
  }

  const deliverables: Deliverable[] = [];
  const knowledgeTypeAccumulator = new Map<string, KnowledgeTypeAccumulator>();
  for (const definition of KNOWLEDGE_TYPE_DEFINITIONS) {
    knowledgeTypeAccumulator.set(definition.id, {
      id: definition.id,
      label: definition.label,
      matchingDeliverableKeys: new Set<string>(),
    });
  }

  try {
    const packages = fs
      .readdirSync(rootPath, { withFileTypes: true })
      .filter((entry) => entry.isDirectory() && entry.name.startsWith("PKG-"));

    for (const pkg of packages) {
      const workingDir = path.join(rootPath, pkg.name, "1_Working");
      if (!fs.existsSync(workingDir)) {
        continue;
      }

      const packageDeliverables = fs
        .readdirSync(workingDir, { withFileTypes: true })
        .filter((entry) => entry.isDirectory() && entry.name.startsWith("DEL-"));

      for (const deliverableEntry of packageDeliverables) {
        const deliverablePath = path.join(workingDir, deliverableEntry.name);
        const statusPath = path.join(deliverablePath, "_STATUS.md");
        let status: Deliverable["status"] = "open";

        if (fs.existsSync(statusPath)) {
          const content = fs.readFileSync(statusPath, "utf-8");
          status = getStatusFromContent(content);
        }

        const parts = deliverableEntry.name.split("_");
        const id = parts[0];
        const name = parts.slice(1).join(" ").replace(/([A-Z])/g, " $1").trim() || "Untitled Deliverable";
        const deliverableKey = `${pkg.name}::${id}`;

        deliverables.push({
          id,
          name,
          pkg: pkg.name,
          status,
          path: deliverablePath,
        });

        for (const definition of KNOWLEDGE_TYPE_DEFINITIONS) {
          if (!definition.matches(deliverablePath)) {
            continue;
          }
          const accumulator = knowledgeTypeAccumulator.get(definition.id);
          if (accumulator) {
            accumulator.matchingDeliverableKeys.add(deliverableKey);
          }
        }
      }
    }

    const knowledgeDecomposition = detectKnowledgeDecomposition(rootPath);

    const knowledgeTypes: KnowledgeTypeOption[] = knowledgeDecomposition.enabled
      ? Array.from(knowledgeTypeAccumulator.values())
          .map((entry) => ({
            id: entry.id,
            label: entry.label,
            matchingDeliverableKeys: Array.from(entry.matchingDeliverableKeys.values()).sort(),
          }))
          .filter((entry) => entry.matchingDeliverableKeys.length > 0)
      : [];

    return NextResponse.json({
      deliverables,
      knowledgeDecomposition,
      knowledgeTypes,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown scan error.";
    console.error("Scan Error:", error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
