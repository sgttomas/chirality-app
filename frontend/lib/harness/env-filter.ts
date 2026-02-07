const HARD_DENYLIST: RegExp[] = [
  /_SECRET$/i,
  /_PASSWORD$/i,
  /_CREDENTIAL$/i,
  /_KEY$/i,
  /_TOKEN$/i,
  /_API_KEY$/i,
  /^DATABASE_URL$/i,
  /^REDIS_URL$/i,
];

const EXPLICIT_WHITELIST = new Set([
  "ANTHROPIC_API_KEY",
  "PATH",
  "HOME",
  "USER",
  "SHELL",
  "TERM",
  "NODE_ENV",
  "NODE_OPTIONS",
  "PWD",
  "LANG",
  "LC_ALL",
  "LC_CTYPE",
  "TMPDIR",
  "TEMP",
  "TMP",
]);

export function isSensitiveKey(key: string): boolean {
  return HARD_DENYLIST.some((pattern) => pattern.test(key));
}

export function filterChildEnv(env: NodeJS.ProcessEnv): NodeJS.ProcessEnv {
  const filtered = {} as NodeJS.ProcessEnv;

  for (const [key, value] of Object.entries(env)) {
    if (typeof value === "undefined") {
      continue;
    }

    if (isSensitiveKey(key)) {
      continue;
    }

    filtered[key] = value;
  }

  for (const key of EXPLICIT_WHITELIST) {
    const value = env[key];
    if (typeof value !== "undefined") {
      filtered[key] = value;
    }
  }

  return filtered;
}

export function redactForLogs(value: string): string {
  if (!value) {
    return "[REDACTED]";
  }

  const trimmed = value.trim();
  if (trimmed.length <= 8) {
    return "[REDACTED]";
  }

  return `${trimmed.slice(0, 2)}...[REDACTED]...${trimmed.slice(-2)}`;
}

export function redactSecretsInText(text: string): string {
  return text
    .replace(/sk-ant-[A-Za-z0-9_-]+/g, "[REDACTED]")
    .replace(/\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+/gi, "[REDACTED]");
}
