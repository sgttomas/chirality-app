// One engine revision for the adapter crate and the interface package.
import { describe, expect, it } from "vitest";

import cargoLock from "../src-tauri/Cargo.lock?raw";
import cargoToml from "../src-tauri/Cargo.toml?raw";
import npmLock from "../package-lock.json?raw";
import npmPackage from "../package.json?raw";

describe("the engine pin", () => {
  it("names the same engine revision in Cargo and npm, and the lockfiles hold it", () => {
    const npm = /chirality-engine\.git#([0-9a-f]{40})::path:packages\/ui/.exec(npmPackage)?.[1];
    const cargo = /chirality-engine\.git", rev = "([0-9a-f]{40})"/.exec(cargoToml)?.[1];
    expect(npm).toMatch(/^[0-9a-f]{40}$/);
    expect(cargo).toBe(npm);
    expect(npmLock).toContain(`chirality-engine.git#${npm}::path:packages/ui`);
    expect(cargoLock).toContain(`chirality-engine.git?rev=${npm}#${npm}`);
  });
});
