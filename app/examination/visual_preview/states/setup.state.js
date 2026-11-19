// J1: first launch on a new machine. Setup is required; nothing operational started (no Codex, no project). The
// commands answer so the page can be clicked through: Browse… picks the invented project folder, Review setup shows
// the host's effects for new settings, and confirming returns the saved view (the native confirmation dialog is the
// host's and is not shown here).
import { setupHost, newSettingsPreview, setupRequiredView, pendingSave, PROJECT, nativePath } from "./_shared.js";
import { selfIssued } from "./_commands.js";

export default {
  title: "First launch: setup required",
  host: setupHost(),
  commands: selfIssued({
    // lib.rs desktop_setup_pick: the folder the native picker returned.
    desktop_setup_pick: () => ({ displayPath: PROJECT, nativePath: nativePath(PROJECT) }),
    desktop_setup_new_settings_preview: args => newSettingsPreview(args.projectPath ? new TextDecoder().decode(new Uint8Array(args.projectPath.bytes)) : null),
    // lib.rs desktop_setup_prepare → DesktopSetup::prepare_and_save after the person confirmed: the setup view with the pending request.
    desktop_setup_prepare: () => ({ ...setupRequiredView(), pending: pendingSave() }),
  }),
};
