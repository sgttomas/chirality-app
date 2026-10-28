// Exact-string fields: model and provider names, thread, commit and revision
// IDs, names, references and native JSON. The person's text is sent or recorded
// as typed, so the webview must not capitalise, autocorrect, spell-check or
// autofill it. On macOS WebKit, "gpt-6-luna" became "Gpt-6-luna" and "openai"
// became "Open" without these (native witness 2026-10-10, D-2).
export const EXACT_TEXT = { autoCapitalize: "off", autoCorrect: "off", spellCheck: false, autoComplete: "off" } as const;
