import { useRef, useState } from "react";
import { nativePathText } from "./presentation";

type Json = any;
type Act = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const words = (value: Json): string => typeof value === "string" ? value : "not established";

/** ME-1: only an explicit refresh reads the opened library again. Picks name
 * held observations; the host rechecks them before opening the existing review. */
export function LibraryEntries({ library, busy, available, act }: { library: Json; busy: boolean; available: boolean; act: Act }) {
  const [chosen, setChosen] = useState<string[]>([]);
  const [pending, setPending] = useState(false);
  const operation = useRef(false);
  const listing = library.entryListing;
  const entries: Json[] = Array.isArray(listing?.entries) ? listing.entries : [];
  const bound = !!listing?.reference && listing.libraryRef === library.reference;
  const source = listing?.source ?? library;
  const disabled = busy || pending || !available;
  const eligible = (entry: Json) => bound && listing.state === "observed" && entry.reviewable === true && typeof entry.reference === "string";
  const selected = chosen.filter(reference => entries.some(entry => entry.reference === reference && eligible(entry)));
  const perform = async (command: string, args: Record<string, unknown>) => {
    if (operation.current || disabled) return;
    operation.current = true;setPending(true);
    try { await act(command, args); }
    finally { operation.current = false;setPending(false); }
  };
  return <section aria-label="Library entries available for review">
    <h3>Library entries available for review</h3>
    <p>Opened {words(source.origin)} library · source {words(source.sourceRoot)}.</p>
    {nativePathText(source.root) !== null && <p>Folder: {nativePathText(source.root)}</p>}
    <p>These file observations do not register or select a workflow. Review rechecks the chosen entries; registration remains your separate native confirmation.</p>
    <button disabled={disabled} onClick={() => perform("workflow_library_entries_refresh", { libraryRef: library.reference })}>Refresh library entries</button>
    {!available && <p role="note">The displayed workflow source is unavailable or has changed; refresh the App view before acting.</p>}
    <p>Listing: {words(listing?.state ?? "not observed")}{listing?.observedAt ? ` · observed ${words(listing.observedAt)}` : ""}.</p>
    {(!listing || listing.state === "not observed") && <p>Open or refresh this library to observe its existing entries.</p>}
    {listing && listing.state !== "not observed" && !bound && <p role="note">The entry observation is not bound to this opened library; refresh its entries before choosing.</p>}
    {listing?.state === "absent" && <p>This library has no workflow entries folder.</p>}
    {listing?.state === "observed" && entries.length === 0 && <p>No library entries were observed.</p>}
    {(listing?.limits ?? []).map((limit: Json, index: number) => <p role="note" key={index}>Listing limit: {words(limit)}</p>)}
    <ul>{entries.map((entry: Json, index: number) => <li key={entry.reference ?? index}>
      <label><input type="checkbox" aria-label={`Review entry ${words(entry.name)}`} disabled={disabled || !eligible(entry)} checked={selected.includes(entry.reference)}
        onChange={event => setChosen(old => event.target.checked ? [...old.filter(reference => reference !== entry.reference), entry.reference] : old.filter(reference => reference !== entry.reference))} /> {words(entry.name)}</label>
      {" · "}{words(entry.state)}
      {entry.content?.value && <p>Content {words(entry.content.value)} ({words(entry.content.method)}).</p>}
      {(entry.fileCount !== undefined || entry.bytes !== undefined) && <p>{entry.fileCount !== undefined ? `${entry.fileCount} files` : "File count not established"}{entry.bytes !== undefined ? ` · ${entry.bytes} bytes` : ""}.</p>}
      {(entry.findings ?? []).map((finding: Json, at: number) => <p role="note" key={at}>{words(typeof finding === "string" ? finding : finding?.detail)}</p>)}
      {entry.limit && <p role="note">{words(entry.limit)}</p>}
    </li>)}</ul>
    {selected.length > 0 && <div><p>Review order:</p><ol aria-label="Entry review order">{selected.map(reference => <li key={reference}>{words(entries.find(entry => entry.reference === reference)?.name)}</li>)}</ol></div>}
    <button disabled={disabled || selected.length === 0} onClick={() => perform("workflow_review_library_entries", { libraryRef: library.reference, listingRef: listing?.reference, entryRefs: [...selected] })}>Review chosen entries…</button>
    {listing?.standing && <p><small>{words(listing.standing)}</small></p>}
  </section>;
}
