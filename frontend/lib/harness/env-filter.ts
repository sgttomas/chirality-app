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

export function isSensitiveKey(key: string): boolean {
  return HARD_DENYLIST.some((pattern) => pattern.test(key));
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
