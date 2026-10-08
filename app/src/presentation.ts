// Display helpers for the App's own views (J6 D-1, D-2, D-3). Presentation
// only: nothing here is sent to the host, and identities and comparisons keep
// the exact values the host reported.

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Json = any;

/** Readable text for a native path identity reported by the host
 * (`attachments::native_path_identity`), or null when `v` is not one. Valid
 * UTF-8 (or UTF-16) is shown as itself; otherwise the invalid units are shown
 * escaped behind an explicit marker. */
export function nativePathText(v: Json): string | null {
  if (v === null || typeof v !== "object" || Array.isArray(v)) return null;
  if ((v.encoding === "unix_bytes" || v.encoding === "native_encoded_bytes") && Array.isArray(v.bytes)) {
    if (!v.bytes.every((b: Json) => Number.isInteger(b) && b >= 0 && b <= 255)) return null;
    const bytes = Uint8Array.from(v.bytes as number[]);
    try {
      return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    } catch {
      return `[path is not valid UTF-8; invalid bytes shown as \\xNN] ${escapeInvalidUtf8(bytes)}`;
    }
  }
  if (v.encoding === "windows_utf16" && Array.isArray(v.codeUnits)) {
    if (!v.codeUnits.every((u: Json) => Number.isInteger(u) && u >= 0 && u <= 0xffff)) return null;
    let out = "";
    let lone = false;
    const units: number[] = v.codeUnits;
    for (let i = 0; i < units.length; i++) {
      const u = units[i];
      const next = units[i + 1];
      if (u >= 0xd800 && u <= 0xdbff && next !== undefined && next >= 0xdc00 && next <= 0xdfff) {
        out += String.fromCharCode(u, next);
        i++;
      } else if (u >= 0xd800 && u <= 0xdfff) {
        out += `\\u{${u.toString(16).padStart(4, "0")}}`;
        lone = true;
      } else {
        out += String.fromCharCode(u);
      }
    }
    return lone ? `[path is not valid UTF-16; unpaired code units shown as \\u{NNNN}] ${out}` : out;
  }
  return null;
}

function escapeInvalidUtf8(bytes: Uint8Array): string {
  const decoder = new TextDecoder("utf-8", { fatal: true });
  let out = "";
  let i = 0;
  while (i < bytes.length) {
    const b = bytes[i];
    const width = b < 0x80 ? 1 : b >= 0xc2 && b <= 0xdf ? 2 : b >= 0xe0 && b <= 0xef ? 3 : b >= 0xf0 && b <= 0xf4 ? 4 : 0;
    if (width > 0 && i + width <= bytes.length) {
      try {
        out += decoder.decode(bytes.subarray(i, i + width));
        i += width;
        continue;
      } catch {
        // fall through: show the lead byte escaped and resynchronize
      }
    }
    out += `\\x${b.toString(16).padStart(2, "0")}`;
    i++;
  }
  return out;
}

/** A copy of `v` for display, with every native path identity replaced by its
 * readable text. Never use the result as an identity or for comparison. */
export function readablePaths(v: Json): Json {
  const path = nativePathText(v);
  if (path !== null) return path;
  if (Array.isArray(v)) return v.map(readablePaths);
  if (v !== null && typeof v === "object") {
    return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, readablePaths(x)]));
  }
  return v;
}

function compareCodePoints(a: string, b: string): number {
  const x = Array.from(a);
  const y = Array.from(b);
  for (let i = 0; i < Math.min(x.length, y.length); i++) {
    const d = x[i].codePointAt(0)! - y[i].codePointAt(0)!;
    if (d !== 0) return d;
  }
  return x.length - y.length;
}

function canonicalString(s: string): string {
  let out = '"';
  for (const c of s) {
    const code = c.codePointAt(0)!;
    if (c === '"') out += '\\"';
    else if (c === "\\") out += "\\\\";
    else if (code === 0x08) out += "\\b";
    else if (c === "\t") out += "\\t";
    else if (c === "\n") out += "\\n";
    else if (code === 0x0c) out += "\\f";
    else if (c === "\r") out += "\\r";
    else if (code < 0x20) out += `\\u${code.toString(16).padStart(4, "0")}`;
    else out += c;
  }
  return out + '"';
}

/** The `aac-offer-digest/0.1` canonical serialization (canonical.rs): keys in
 * code-point order, no whitespace, the listed escapes, integers only. */
export function canonicalJson(v: Json): string {
  if (v === null) return "null";
  if (typeof v === "boolean") return v ? "true" : "false";
  if (typeof v === "number") {
    if (!Number.isSafeInteger(v)) throw new Error("not an exactly representable integer");
    return String(v);
  }
  if (typeof v === "string") return canonicalString(v);
  if (Array.isArray(v)) return `[${v.map(canonicalJson).join(",")}]`;
  if (typeof v === "object") {
    const keys = Object.keys(v).sort(compareCodePoints);
    return `{${keys.map((k) => `${canonicalString(k)}:${canonicalJson(v[k])}`).join(",")}}`;
  }
  throw new Error(`unsupported value ${typeof v}`);
}

export async function sha256Hex(text: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

/** The complete review's digest, as the native A15 statement names it. */
export function reviewDigest(presentation: Json): Promise<string> {
  return sha256Hex(canonicalJson(presentation));
}

/** D-2: the run summary's supply reading follows the latest supply check, as
 * its check row does; before any check it keeps the run's own status. */
export function suppliedSummary(run: Json): string {
  const checks: Json[] = Array.isArray(run?.checks) ? run.checks : [];
  const latest = checks[checks.length - 1];
  if (latest) {
    const of = checks.length > 1 ? ` (latest of ${checks.length} checks)` : "";
    return `${latest.state} (${latest.supplyReading}) at ${latest.readAt}${of}`;
  }
  return run?.status?.supplied ?? "see checks";
}
