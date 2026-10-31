import type { EditorOperationIntent, PreviewModel } from "../../types";

// The node, pipe and support removal intents. The inspector's Delete panels and the context
// menus (B9) queue these same intents; the builders moved here unchanged from
// PropertyInspector.tsx, so their source_ref still names the inspector, the editor that owns
// the command.

function safeToken(value: string): string {
  return value.replace(/[^A-Za-z0-9_.:-]+/g, "-");
}

// A deletion's `before` must equal the summary the operation applier compares
// byte for byte (operation_applier lib.rs `node_delete_display`,
// `pipe_delete_display` and the support's trimmed label), or the deletion is
// refused as stale (`OP-STALE-BEFORE-VALUE`). Every deletion of these records
// builds its `before` here.

/** The applier's `display_number`: an integral value below 1e15 as an integer,
 * any other in Rust's shortest round-trip decimal, which never uses an exponent
 * (1e-7 is `0.0000001`, 2.5e21 is `2500000000000000000000`). */
export function applierDisplayNumber(value: number): string {
  if (Number.isInteger(value) && Math.abs(value) < 1e15) return String(value);
  const text = String(value);
  const match = /^(-?)(\d)(?:\.(\d+))?e([+-]\d+)$/.exec(text);
  if (!match) return text;
  const [, sign, lead, fraction = "", exponent] = match;
  const digits = lead + fraction;
  const point = 1 + Number(exponent);
  if (point <= 0) return `${sign}0.${"0".repeat(-point)}${digits}`;
  if (point >= digits.length) return sign + digits + "0".repeat(point - digits.length);
  return `${sign}${digits.slice(0, point)}.${digits.slice(point)}`;
}

export function nodeDeletionSummary(node: PreviewModel["nodes"][number]): string {
  const { x, y, z } = node.position;
  return `${node.label.trim()}; x=${applierDisplayNumber(x)}; y=${applierDisplayNumber(y)}; z=${applierDisplayNumber(z)}`;
}

export function pipeDeletionSummary(pipe: PreviewModel["pipe_segments"][number]): string {
  return `${pipe.label.trim()}; ${pipe.from.trim()}->${pipe.to.trim()}; material=${pipe.material.trim()}`;
}

export function supportDeletionSummary(support: PreviewModel["supports"][number]): string {
  return support.label.trim();
}

export function buildDeleteSupportIntent(
  support: PreviewModel["supports"][number],
  model: PreviewModel
): EditorOperationIntent {
  const supportId = support.id.trim();
  return {
    operation_id: `op:delete-support-${safeToken(supportId)}`,
    operation_kind: "delete",
    operation_status: "proposed",
    author_type: "user",
    source: {
      source_ref: "apps/desktop/src/features/model-tree/PropertyInspector.tsx",
      source_channel: "local_desktop_preview",
      source_role: "gui_editor"
    },
    target: {
      object_type: "Support",
      ref: supportId
    },
    change: {
      change_id: `change:delete-support:${safeToken(supportId)}`,
      change_kind: "delete_support",
      field_label: "Explicit support deletion",
      field_path: "supports",
      before: supportDeletionSummary(support),
      after: "not_present",
      unit: "none",
      dimension: "dimensionless",
      source_note: "explicit user-entered support deletion; reference integrity required"
    },
    validation: {
      schema_validation: "not_run",
      constraint_validation: "not_run",
      unit_validation: "not_required_dimensionless",
      diff_preview_status: "not_generated",
      application_status: "not_applied"
    },
    audit_boundary: {
      mutation_route: "structured_operations_only",
      direct_model_mutation_allowed: false,
      requires_user_acceptance: true,
      mutates_accepted_model_state: false
    },
    professional_boundary: {
      human_review_required: true,
      software_makes_compliance_claim: false,
      software_makes_certification_claim: false,
      software_makes_sealing_claim: false,
      software_makes_approval_claim: false,
      software_makes_authentication_claim: false
    },
    rationale: `explicit user-entered support deletion for ${model.project.id}; requires reference validation before durable model change.`
  };
}

export function buildDeleteNodeIntent(node: PreviewModel["nodes"][number], model: PreviewModel): EditorOperationIntent {
  const nodeId = node.id.trim();
  const before = nodeDeletionSummary(node);
  return {
    operation_id: `op:delete-node-${safeToken(nodeId)}`,
    operation_kind: "delete",
    operation_status: "proposed",
    author_type: "user",
    source: {
      source_ref: "apps/desktop/src/features/model-tree/PropertyInspector.tsx",
      source_channel: "local_desktop_preview",
      source_role: "gui_editor"
    },
    target: {
      object_type: "Node",
      ref: nodeId
    },
    change: {
      change_id: `change:delete-node:${safeToken(nodeId)}`,
      change_kind: "delete_node",
      field_label: "Explicit node deletion",
      field_path: "nodes",
      before,
      after: "not_present",
      unit: "none",
      dimension: "dimensionless",
      source_note: "explicit user-entered node deletion; endpoint and load reference integrity required"
    },
    validation: {
      schema_validation: "not_run",
      constraint_validation: "not_run",
      unit_validation: "not_required_dimensionless",
      diff_preview_status: "not_generated",
      application_status: "not_applied"
    },
    audit_boundary: {
      mutation_route: "structured_operations_only",
      direct_model_mutation_allowed: false,
      requires_user_acceptance: true,
      mutates_accepted_model_state: false
    },
    professional_boundary: {
      human_review_required: true,
      software_makes_compliance_claim: false,
      software_makes_certification_claim: false,
      software_makes_sealing_claim: false,
      software_makes_approval_claim: false,
      software_makes_authentication_claim: false
    },
    rationale: `explicit user-entered node deletion for ${model.project.id}; requires reference validation before durable model change.`
  };
}

export function buildDeletePipeIntent(
  pipe: PreviewModel["pipe_segments"][number],
  model: PreviewModel
): EditorOperationIntent {
  const pipeId = pipe.id.trim();
  const before = pipeDeletionSummary(pipe);
  return {
    operation_id: `op:delete-pipe-${safeToken(pipeId)}`,
    operation_kind: "delete",
    operation_status: "proposed",
    author_type: "user",
    source: {
      source_ref: "apps/desktop/src/features/model-tree/PropertyInspector.tsx",
      source_channel: "local_desktop_preview",
      source_role: "gui_editor"
    },
    target: {
      object_type: "Element",
      ref: pipeId
    },
    change: {
      change_id: `change:delete-pipe:${safeToken(pipeId)}`,
      change_kind: "delete_pipe_run",
      field_label: "Explicit pipe deletion",
      field_path: "pipe_segments",
      before,
      after: "not_present",
      unit: "none",
      dimension: "dimensionless",
      source_note: "explicit user-entered pipe deletion; primitive-load reference integrity required"
    },
    validation: {
      schema_validation: "not_run",
      constraint_validation: "not_run",
      unit_validation: "not_required_dimensionless",
      diff_preview_status: "not_generated",
      application_status: "not_applied"
    },
    audit_boundary: {
      mutation_route: "structured_operations_only",
      direct_model_mutation_allowed: false,
      requires_user_acceptance: true,
      mutates_accepted_model_state: false
    },
    professional_boundary: {
      human_review_required: true,
      software_makes_compliance_claim: false,
      software_makes_certification_claim: false,
      software_makes_sealing_claim: false,
      software_makes_approval_claim: false,
      software_makes_authentication_claim: false
    },
    rationale: `explicit user-entered pipe deletion for ${model.project.id}; requires reference validation before durable model change.`
  };
}
