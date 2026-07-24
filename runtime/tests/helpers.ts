import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

export async function createProjectFixture(root: string, projectId = "fixture") {
  await mkdir(join(root, "agents"), { recursive: true });
  await mkdir(join(root, "execution"), { recursive: true });
  await mkdir(join(root, "legacy-sessions"), { recursive: true });
  await writeFile(
    join(root, "agents", "AGENT_HELP_HUMAN.md"),
    "[[DOC:AGENT_INSTRUCTIONS]]\n# HELP_HUMAN\nAGENT_TYPE: 0\nAGENT_CLASS: SUPERVISING\n",
    "utf8"
  );
  await writeFile(
    join(root, "agents", "AGENT_WORKING_ITEMS.md"),
    "[[DOC:AGENT_INSTRUCTIONS]]\n# WORKING_ITEMS\nAGENT_TYPE: 1\nAGENT_CLASS: WORKING\n",
    "utf8"
  );
  await writeFile(
    join(root, "agents", "AGENT_TASK.md"),
    "[[DOC:AGENT_INSTRUCTIONS]]\n# TASK\nAGENT_TYPE: 2\nAGENT_CLASS: TASK\n",
    "utf8"
  );
  const manifest = {
    schemaVersion: "chirality.project/v1",
    projectId,
    displayName: "Fixture",
    workingRoot: ".",
    instructionRoot: ".",
    agentsOverlay: "agents/AGENT_WORKING_ITEMS.md",
    defaultExecutionRoot: "execution",
    profiles: { domain: [], capability: [], dataBoundary: [] },
    enabledAdapterIds: ["stub", "pi"],
    embeddedUi: { declared: false },
    legacySessionRoots: ["legacy-sessions"]
  };
  const manifestPath = join(root, "chirality.project.json");
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  return { manifest, manifestPath };
}
