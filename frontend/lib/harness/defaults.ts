import type { SettingSource } from "@anthropic-ai/claude-agent-sdk";

import type { TurnOpts } from "./types";

export const DEFAULT_MAX_TURNS = 25;
export const DEFAULT_PERMISSION_MODE: NonNullable<TurnOpts["permissionMode"]> = "dontAsk";
export const DEFAULT_INCLUDE_PARTIAL_MESSAGES = true;
export const DEFAULT_VERBOSE = true;
export const DEFAULT_SETTING_SOURCES: SettingSource[] = ["user", "project", "local"];
export const CLAUDE_CODE_SYSTEM_PROMPT_PRESET = "claude_code";
export const CLAUDE_CODE_TOOLS_PRESET = "claude_code";

export const PROMPT_TOKEN_BUDGET = 16_000;
export const DEFAULT_SYSTEM_PROMPT = "You are operating within the Chirality Command Center.";

export const LOG_ROTATE_BYTES = 10 * 1024 * 1024;
export const LOG_DIR_RELATIVE = ".chirality/logs";
export const LOG_FILE_NAME = "harness.log";
export const LOG_ROTATED_FILE_NAME = "harness.log.1";

export const LOG_TRUNCATE_USER_TEXT = 200;
export const LOG_TRUNCATE_STREAM_LINE = 500;
