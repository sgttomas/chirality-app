export const PLAN_EXPORT_DIALOG_CHANNEL = 'chirality:plan-export-dialog';
export type PlanExportTargetResult = { cancelled: true; error?: string } | { cancelled: false; targetRelativePath: string };
