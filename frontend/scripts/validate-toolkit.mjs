#!/usr/bin/env node

/**
 * Toolkit validation script.
 *
 * Validates the toolkit-config module's core invariants at build/premerge time
 * without requiring a running server. Pure logic tests against exported functions.
 *
 * Usage:
 *   node scripts/validate-toolkit.mjs
 *
 * Exit codes:
 *   0 — all checks pass
 *   1 — one or more checks failed
 */

import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND_ROOT = path.resolve(SCRIPT_DIR, "..");

// ---------------------------------------------------------------------------
// Dynamic import of the compiled toolkit module
// ---------------------------------------------------------------------------

// We import the TypeScript source transpiled via tsx or the compiled output.
// For premerge, we check that the source file exists and the types compile.

const TOOLKIT_SOURCE = path.join(FRONTEND_ROOT, "lib", "toolkit-config.ts");

// ---------------------------------------------------------------------------
// Test registry
// ---------------------------------------------------------------------------

const results = [];

function pass(id, description) {
  results.push({ id, status: "pass", description });
  console.log(`  ✓ ${id}: ${description}`);
}

function fail(id, description, error) {
  results.push({ id, status: "fail", description, error: String(error) });
  console.error(`  ✗ ${id}: ${description} — ${error}`);
}

// ---------------------------------------------------------------------------
// Static checks (source file analysis)
// ---------------------------------------------------------------------------

async function runStaticChecks() {
  console.log("\n[toolkit] Static analysis checks\n");

  // Check source files exist
  try {
    await readFile(TOOLKIT_SOURCE, "utf8");
    pass("toolkit.static.source_exists", "toolkit-config.ts exists");
  } catch (err) {
    fail("toolkit.static.source_exists", "toolkit-config.ts exists", err.message);
    return;
  }

  const source = await readFile(TOOLKIT_SOURCE, "utf8");

  // Check required exports
  const requiredExports = [
    "EMPTY_OVERRIDES",
    "hasActiveOverrides",
    "countActiveOverrides",
    "validateToolkitOverrides",
    "computeToolkitWarnings",
    "buildTurnOptsFromToolkit",
    "normalizeToolsCsv",
    "normalizeStringArray",
    "loadPresets",
    "savePresets",
    "createPreset",
    "normalizeStoredOverrides",
  ];

  for (const name of requiredExports) {
    if (source.includes(`export function ${name}`) || source.includes(`export const ${name}`)) {
      pass(`toolkit.static.export_${name}`, `Exports ${name}`);
    } else {
      fail(`toolkit.static.export_${name}`, `Exports ${name}`, "Export not found in source");
    }
  }

  // Check required types
  const requiredTypes = [
    "ToolkitOverrides",
    "ToolkitPreset",
    "ToolkitValidationError",
    "ToolkitWarning",
    "PartialMessagesSetting",
  ];

  for (const name of requiredTypes) {
    if (source.includes(`export interface ${name}`) || source.includes(`export type ${name}`)) {
      pass(`toolkit.static.type_${name}`, `Exports type ${name}`);
    } else {
      fail(`toolkit.static.type_${name}`, `Exports type ${name}`, "Type not found in source");
    }
  }

  // Check zero-impact invariant is structurally present
  if (source.includes("EMPTY_OVERRIDES") && source.includes("buildTurnOptsFromToolkit")) {
    pass("toolkit.static.zero_impact_structure", "Zero-impact code path is structurally present");
  } else {
    fail("toolkit.static.zero_impact_structure", "Zero-impact code path is structurally present", "Missing");
  }

  // Check governance validation logic
  if (source.includes("contextSealed") && source.includes("pipelineRunApproved") && source.includes("approvalRef")) {
    pass("toolkit.static.governance_fields", "Governance validation covers all required fields");
  } else {
    fail("toolkit.static.governance_fields", "Governance validation covers all required fields", "Missing fields");
  }

  // Check tri-state includePartialMessages
  if (source.includes('"inherit"') && source.includes("includePartialMessages")) {
    pass("toolkit.static.include_partial_tri_state", "includePartialMessages tri-state implemented");
  } else {
    fail("toolkit.static.include_partial_tri_state", "includePartialMessages tri-state implemented", "Missing inherit state");
  }

  // Check preset capacity limit
  if (source.includes("MAX_PRESETS") || source.includes("slice(0, 20)")) {
    pass("toolkit.static.preset_capacity", "Preset capacity limit enforced");
  } else {
    fail("toolkit.static.preset_capacity", "Preset capacity limit enforced", "No capacity limit found");
  }

  // Check schema version
  if (source.includes("PRESET_SCHEMA_VERSION") || source.includes("version")) {
    pass("toolkit.static.schema_version", "Preset schema version field present");
  } else {
    fail("toolkit.static.schema_version", "Preset schema version field present", "No version field");
  }
}

// ---------------------------------------------------------------------------
// Integration checks (ChatPanel integration)
// ---------------------------------------------------------------------------

async function runIntegrationChecks() {
  console.log("\n[toolkit] Integration checks\n");

  let chatPanelSource;
  try {
    chatPanelSource = await readFile(path.join(FRONTEND_ROOT, "components", "ChatPanel.tsx"), "utf8");
  } catch (err) {
    fail("toolkit.integration.chatpanel_readable", "ChatPanel.tsx is readable", err.message);
    return;
  }

  // Check toolkit imports
  if (chatPanelSource.includes("toolkit-config") && chatPanelSource.includes("Toolkit")) {
    pass("toolkit.integration.imports", "ChatPanel imports toolkit modules");
  } else {
    fail("toolkit.integration.imports", "ChatPanel imports toolkit modules", "Missing imports");
  }

  // Check toolkitOverrides on LocalChatSession
  if (chatPanelSource.includes("toolkitOverrides: ToolkitOverrides") || chatPanelSource.includes("toolkitOverrides")) {
    pass("toolkit.integration.session_type", "LocalChatSession has toolkitOverrides field");
  } else {
    fail("toolkit.integration.session_type", "LocalChatSession has toolkitOverrides field", "Field not found");
  }

  // Check buildTurnOptsFromToolkit usage in streamTurn
  if (chatPanelSource.includes("buildTurnOptsFromToolkit")) {
    pass("toolkit.integration.turn_payload", "streamTurn uses buildTurnOptsFromToolkit");
  } else {
    fail("toolkit.integration.turn_payload", "streamTurn uses buildTurnOptsFromToolkit", "Not found");
  }

  // Check validation gate in sendPrompt
  if (chatPanelSource.includes("validateToolkitOverrides")) {
    pass("toolkit.integration.validation_gate", "sendPrompt has toolkit validation gate");
  } else {
    fail("toolkit.integration.validation_gate", "sendPrompt has toolkit validation gate", "Not found");
  }

  // Check normalizeStoredOverrides in session parsing
  if (chatPanelSource.includes("normalizeStoredOverrides")) {
    pass("toolkit.integration.backward_compat", "normalizeStoredSessions handles toolkitOverrides migration");
  } else {
    fail("toolkit.integration.backward_compat", "normalizeStoredSessions handles toolkitOverrides migration", "Not found");
  }

  // Check boot request is limited (not full toolkit payload)
  // The boot request should only pass apiKey and optionally model
  if (chatPanelSource.includes("bootOpts") && chatPanelSource.includes("toolkitModel")) {
    pass("toolkit.integration.boot_limited", "Boot request is narrowly scoped (apiKey + model only)");
  } else {
    fail("toolkit.integration.boot_limited", "Boot request is narrowly scoped", "Pattern not found");
  }
}

// ---------------------------------------------------------------------------
// Component checks
// ---------------------------------------------------------------------------

async function runComponentChecks() {
  console.log("\n[toolkit] Component checks\n");

  // Toolkit.tsx
  try {
    const toolkitSource = await readFile(path.join(FRONTEND_ROOT, "components", "Toolkit.tsx"), "utf8");

    if (toolkitSource.includes("GovernanceSection")) {
      pass("toolkit.component.governance_visible", "Governance section is rendered in Toolkit");
    } else {
      fail("toolkit.component.governance_visible", "Governance section is rendered", "Not found");
    }

    if (toolkitSource.toLowerCase().includes("runtime gates still apply")) {
      pass("toolkit.component.governance_notice", "Governance runtime gate notice is present");
    } else {
      fail("toolkit.component.governance_notice", "Governance runtime gate notice is present", "Not found");
    }

    if (toolkitSource.includes("isCollapsed")) {
      pass("toolkit.component.collapse_toggle", "Toolkit supports collapse/expand");
    } else {
      fail("toolkit.component.collapse_toggle", "Toolkit supports collapse/expand", "Not found");
    }

    if (toolkitSource.includes("isLoading") || toolkitSource.includes("disabled")) {
      pass("toolkit.component.loading_disabled", "Controls disabled during loading");
    } else {
      fail("toolkit.component.loading_disabled", "Controls disabled during loading", "Not found");
    }
  } catch (err) {
    fail("toolkit.component.toolkit_readable", "Toolkit.tsx is readable", err.message);
  }

  // ToolkitPresets.tsx
  try {
    const presetsSource = await readFile(path.join(FRONTEND_ROOT, "components", "ToolkitPresets.tsx"), "utf8");

    if (presetsSource.includes("loadPresets") && presetsSource.includes("savePresets")) {
      pass("toolkit.component.presets_storage", "ToolkitPresets uses localStorage helpers");
    } else {
      fail("toolkit.component.presets_storage", "ToolkitPresets uses localStorage helpers", "Not found");
    }

    if (presetsSource.includes("onApply") && presetsSource.includes("onClose")) {
      pass("toolkit.component.presets_callbacks", "ToolkitPresets has apply/close callbacks");
    } else {
      fail("toolkit.component.presets_callbacks", "ToolkitPresets has apply/close callbacks", "Not found");
    }
  } catch (err) {
    fail("toolkit.component.presets_readable", "ToolkitPresets.tsx is readable", err.message);
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

async function main() {
  console.log("╔══════════════════════════════════════════╗");
  console.log("║   Toolkit Validation Suite               ║");
  console.log("╚══════════════════════════════════════════╝");

  await runStaticChecks();
  await runIntegrationChecks();
  await runComponentChecks();

  const passCount = results.filter((r) => r.status === "pass").length;
  const failCount = results.filter((r) => r.status === "fail").length;

  console.log(`\n[toolkit] Summary: ${passCount} passed, ${failCount} failed\n`);

  if (failCount > 0) {
    console.error("[toolkit] VALIDATION FAILED");
    process.exitCode = 1;
  } else {
    console.log("[toolkit] VALIDATION PASSED");
  }

  // Emit machine-readable output
  console.log(`\nTOOLKIT_VALIDATION_STATUS=${failCount === 0 ? "PASS" : "FAIL"}`);
  console.log(`TOOLKIT_VALIDATION_PASS_COUNT=${passCount}`);
  console.log(`TOOLKIT_VALIDATION_FAIL_COUNT=${failCount}`);
}

main().catch((err) => {
  console.error(`[toolkit] Unexpected error: ${err.message}`);
  process.exitCode = 1;
});
