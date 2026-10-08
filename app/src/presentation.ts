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

const pointer = (at: string, key: string | number) =>
  `${at}/${String(key).replace(/~/g, "~0").replace(/\//g, "~1")}`;

/** The `aac-offer-digest/0.1` canonical serialization (canonical.rs): keys in
 * code-point order, no whitespace, the listed escapes, integers only. A
 * non-integer is refused with its location (AAC §5.1 defines integers only).
 * An integer beyond 2^53 is refused too: JSON parsing in this view has
 * already rounded it, so only the host's digest is exact (V14 F2). */
export function canonicalJson(v: Json, at = ""): string {
  if (v === null) return "null";
  if (typeof v === "boolean") return v ? "true" : "false";
  if (typeof v === "number") {
    if (!Number.isInteger(v)) {
      throw new Error(`non-integer number at ${at || "/"}; the aac-offer-digest/0.1 canonical form (AAC §5.1) defines integers only`);
    }
    if (!Number.isSafeInteger(v)) {
      throw new Error(`integer at ${at || "/"} is beyond 2^53, which this view cannot hold exactly; use the digest the host reports`);
    }
    return String(v);
  }
  if (typeof v === "string") return canonicalString(v);
  if (Array.isArray(v)) return `[${v.map((x, i) => canonicalJson(x, pointer(at, i))).join(",")}]`;
  if (typeof v === "object") {
    const keys = Object.keys(v).sort(compareCodePoints);
    return `{${keys.map((k) => `${canonicalString(k)}:${canonicalJson(v[k], pointer(at, k))}`).join(",")}}`;
  }
  throw new Error(`unsupported value ${typeof v} at ${at || "/"}`);
}

/** The digest of one review: as the host reports it (named by the native A15
 * statement), and as this view recomputed it from the review it shows. */
export type ReviewDigestView = { host?: string; hostUnavailable?: string; app?: string; appUnavailable?: string };

/** V14 F8: the digest is a reading aid. The binding is checked host-side. */
export const DIGEST_LIMIT =
  "The digest is a reading aid: this view could show other bytes beside it, so the binding is checked by the host at capture, not here.";

export function digestComparison(d: ReviewDigestView): string {
  const host = d.host
    ? `Complete review digest reported by the host (sha-256, named in the native confirmation): ${d.host}.`
    : `Host digest unavailable: ${d.hostUnavailable ?? "not reported"}.`;
  const app = d.app
    ? d.host
      ? d.app === d.host
        ? "This view recomputed the same digest from the review it shows."
        : `This view recomputed a different digest (${d.app}) from the review it shows: do not rely on this view; compare in the native confirmation and review again.`
      : `This view recomputed ${d.app}.`
    : `This view cannot recompute it (${d.appUnavailable ?? "no review"}).`;
  return `${host} ${app} ${DIGEST_LIMIT}`;
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
 * its check row does, including a pending check record (V14 F10); before any
 * check it keeps the run's own status. */
export function suppliedSummary(run: Json): string {
  const checks: Json[] = Array.isArray(run?.checks) ? run.checks : [];
  const latest = checks[checks.length - 1];
  if (latest) {
    const of = checks.length > 1 ? ` (latest of ${checks.length} checks)` : "";
    const record = latest.published === false
      ? `; check record pending${latest.publicationLimit ? ` — ${typeof latest.publicationLimit === "string" ? latest.publicationLimit : JSON.stringify(latest.publicationLimit)}` : ""}`
      : "";
    return `${latest.state} (${latest.supplyReading}) at ${latest.readAt}${of}${record}`;
  }
  return run?.status?.supplied ?? "see checks";
}
