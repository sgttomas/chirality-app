import { useEffect, useRef } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import type { WaitingRequestGroup } from "./RequestCards";

type Checkpoint = { consumer: string; revision: number };
type Claim = { intentId: string; target: WaitingRequestGroup; checkpoint: Checkpoint | null } | { refused: string } | null;

/** A menu selection retains the host's last acknowledged UI checkpoint. Missing
 * wake events cannot replace that checkpoint with the UI seen by a later poll.
 * A changed or unacknowledged ordering is refused; no clock comparison is used. */
export function NativeWaitingBridge({ ready, checkpoint, capture, report }: {
  ready: boolean;
  checkpoint: () => { signature: string; pristine: boolean };
  capture: () => (target: WaitingRequestGroup) => Promise<void>;
  report: (message: string) => void;
}) {
  const latest = useRef({ checkpoint, capture, report });
  latest.current = { checkpoint, capture, report };
  const session = useRef<{ publish: () => Promise<void> } | null>(null);
  const renderedCheckpoint = checkpoint().signature;
  useEffect(() => {
    if (!ready) return;
    const consumer = crypto.randomUUID();
    let stopped = false, busy = false, cleanupNeeded = false;
    let unlisten: (() => void) | undefined;
    const initialUI = latest.current.checkpoint();
    // Revision zero is reserved for a first attachment with no prior UI choice.
    // An edit made while host_status was pending cannot adopt an older menu intent.
    let signature = initialUI.signature, revision = initialUI.pristine ? 0 : 1, acknowledged = -1;
    let publication: Promise<void> | undefined;
    const observeUI = () => {
      const current = latest.current.checkpoint().signature;
      if (current !== signature) { signature = current; revision++; }
      return revision;
    };
    // Serialize checkpoint publications and await the latest observed revision.
    // Same-valued choices still change App's existing intent counters. A change
    // not rendered yet is caught by the live checkpoint read before claiming.
    const publish = async () => {
      while (!stopped) {
        observeUI();
        if (acknowledged === revision) return;
        if (!publication) {
          const submitted = revision;
          publication = invoke("checkpoint_native_waiting_ui", { consumer, revision: submitted })
            .then(() => { acknowledged = submitted; })
            .finally(() => { publication = undefined; });
        }
        await publication;
      }
    };
    const owner = { publish };
    session.current = owner;
    const abandon = async () => {
      await invoke("finish_native_waiting_intent", { consumer, intentId: null });
      cleanupNeeded = false;
    };
    const pump = async () => {
      if (stopped || busy) return;
      busy = true;
      let mayOwnClaim = false;
      try {
        if (cleanupNeeded) { await abandon(); return; }
        await publish();
        if (stopped) return;
        // Bind receiver guards to the acknowledged UI about to be claimed,
        // including edits made while listener installation was pending.
        // The returned checkpoint still refuses older queued selections.
        const receive = latest.current.capture();
        mayOwnClaim = true; // Host execution can precede a lost IPC response.
        const claim = await invoke<Claim>("claim_native_waiting_intent", { consumer });
        if (stopped) return; // A new consumer explicitly refuses interrupted claims.
        if (!claim || "refused" in claim) {
          mayOwnClaim = false;
          if (claim) latest.current.report(claim.refused);
          return;
        }
        try {
          if (claim.checkpoint?.consumer !== consumer || claim.checkpoint.revision !== observeUI()) {
            latest.current.report("Waiting-request navigation refused: its native selection has an older or uncertain UI checkpoint; choose again after the current UI checkpoint is acknowledged.");
          } else { await receive(claim.target); }
        } finally {
          await invoke("finish_native_waiting_intent", { consumer, intentId: claim.intentId });
          mayOwnClaim = false;
        }
      } catch (error) {
        if (mayOwnClaim) {
          cleanupNeeded = true;
          try { await abandon(); } catch { /* retain cleanupNeeded until acknowledgment */ }
        }
        if (!stopped) latest.current.report(`Waiting-request navigation unavailable: ${String(error)}. ${cleanupNeeded ? "Cleanup remains pending; only cleanup will be retried." : "Choose again from the current menu."}`);
      } finally { busy = false; }
    };
    // Initial registration and its live revision are independent of listener
    // availability. Polling also publishes/acknowledges before reading a claim.
    void publish().catch(error => { if (!stopped) latest.current.report(`Waiting menu UI checkpoint unavailable: ${String(error)}`); });
    void listen("chirality-native-waiting", () => { void pump(); }, { target: "main" })
      .then(off => { if (stopped) off(); else unlisten = off; })
      .catch(error => { if (!stopped) latest.current.report(`Waiting menu listener unavailable; checking pending selections: ${String(error)}`); })
      .finally(() => { void pump(); });
    const timer = setInterval(() => { void pump(); }, 1000);
    return () => {
      stopped = true; clearInterval(timer); unlisten?.();
      if (session.current === owner) session.current = null;
    };
  }, [ready]);
  // Publish after UI renders as well as at the claim boundary. This makes a new
  // native click usable after acknowledgment without waiting for a recovery poll.
  useEffect(() => {
    const owner = session.current;
    void owner?.publish().catch(error => {
      if (session.current === owner) latest.current.report(`Waiting menu UI checkpoint unavailable: ${String(error)}`);
    });
  }, [ready, renderedCheckpoint]);
  return null;
}
