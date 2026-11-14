import { AgentText, wordOf } from "./AgentText";

const STANDINGS = {
  "keychain-verified": "seal verified with your keychain",
  "file-key-verified": "sealed with the App's key file, not your keychain",
  "not-verified": "seal not verified",
  unavailable: "seal could not be checked now",
  unsealed: "not sealed; the record does not say why",
  "unsealed-recorded-failure": "not sealed when recorded",
} as const;

// Product words come only from the closed table. The capture's explanation is
// attributed file text, even when it resembles a control or an App sentence.
export function DecisionSealStanding({ seal }: { seal: any }) {
  return <div>
    <p>Capture seal: {wordOf(STANDINGS, seal?.presentation) ?? "seal could not be checked now"}
      {seal?.presentation === "unsealed-recorded-failure" && <> (<AgentText value={seal?.recordedFailure} source="file"
        label="Recorded sealing failure:" name="Sealing failure stated by the capture; not independently established" />)</>}.
      Who wrote it is not established.</p>
    {seal?.presentation === "unavailable" && <p>Verification is unavailable now. The decision remains recorded.</p>}
    {(seal?.presentation === "unsealed" || seal?.presentation === "unsealed-recorded-failure") && <p>A decision recorded unsealed is never sealed later.</p>}
    {seal?.status === "verified" && seal?.recordedProvider == null && <p>The capture did not record its seal provider. The provider shown is the one whose key verified it here.</p>}
  </div>;
}
