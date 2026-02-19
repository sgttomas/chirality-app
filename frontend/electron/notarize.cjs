/* eslint-disable @typescript-eslint/no-require-imports */
const path = require("node:path");

exports.default = async function notarizeIfConfigured(context) {
  if (context.electronPlatformName !== "darwin") {
    return;
  }

  const appleId = process.env.APPLE_ID;
  const appleIdPassword = process.env.APPLE_APP_SPECIFIC_PASSWORD;
  const teamId = process.env.APPLE_TEAM_ID;

  if (!appleId || !appleIdPassword || !teamId) {
    console.log(
      "[notarize] Skipping notarization. Set APPLE_ID, APPLE_APP_SPECIFIC_PASSWORD, and APPLE_TEAM_ID for release builds.",
    );
    return;
  }

  let notarize;
  try {
    ({ notarize } = require("@electron/notarize"));
  } catch {
    console.warn("[notarize] @electron/notarize is missing. Install it before running notarized releases.");
    return;
  }

  const appName = context.packager.appInfo.productFilename;
  const appPath = path.join(context.appOutDir, `${appName}.app`);

  console.log(`[notarize] Submitting ${appPath}`);
  await notarize({
    appPath,
    appleId,
    appleIdPassword,
    teamId,
  });
  console.log("[notarize] Completed successfully.");
};
