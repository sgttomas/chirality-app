// J1: the same first launch after the person confirmed setup: "You're set up". The launch is still the setup-required
// one (the saved request applies at the next launch); the view carries the pending request prepare_and_save saved.
import { setupHost, setupRequiredView, pendingSave } from "./_shared.js";
import { selfIssued } from "./_commands.js";

export default {
  title: "First launch: setup saved, quit and reopen",
  host: setupHost({ desktopSetup: { ...setupRequiredView(), pending: pendingSave() } }),
  commands: selfIssued({ quit_app: null }),
};
