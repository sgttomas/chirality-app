// One engine revision for the adapter crate and the interface package, entry
// by entry: each manifest, and what each lockfile resolved; the bundle carries
// the pinned Library edition and the fonts' licence; and the app's identity.
import { describe, expect, it } from "vitest";

import cargoLock from "../src-tauri/Cargo.lock?raw";
import cargoToml from "../src-tauri/Cargo.toml?raw";
import tauriConf from "../src-tauri/tauri.conf.json?raw";
import edition from "../library.json";
import npmLock from "../package-lock.json?raw";
import npmPackage from "../package.json?raw";

/** Each `[[package]]` of a Cargo.lock: its name and source. */
function lockedCrates(lock: string) {
  return lock
    .split("[[package]]")
    .slice(1)
    .map((block) => ({ name: /^name = "([^"]+)"/m.exec(block)?.[1], source: /^source = "([^"]+)"/m.exec(block)?.[1] }));
}

/** The revision each entry names, or what it names instead. */
function pins(files: { cargoToml: string; cargoLock: string; npmPackage: string; npmLock: string }) {
  const rev = /^chirality-engine-tauri = \{ git = "https:\/\/github\.com\/sgttomas\/chirality-engine\.git", rev = "([0-9a-f]{40})" \}$/m.exec(files.cargoToml)?.[1];
  const npm = (spec: string | undefined) => /^git\+https:\/\/github\.com\/sgttomas\/chirality-engine\.git#([0-9a-f]{40})::path:packages\/ui$/.exec(spec ?? "")?.[1] ?? spec;
  const cargo = (source: string | undefined) => {
    const m = /^git\+https:\/\/github\.com\/sgttomas\/chirality-engine\.git\?rev=([0-9a-f]{40})#([0-9a-f]{40})$/.exec(source ?? "");
    return m && m[1] === m[2] ? m[1] : source;
  };
  const lock = JSON.parse(files.npmLock);
  const crates = lockedCrates(files.cargoLock);
  const locked = (name: string) => {
    const found = crates.filter((c) => c.name === name);
    return found.length === 1 ? cargo(found[0].source) : `${found.length} entries`;
  };
  return {
    "Cargo.toml": rev,
    "Cargo.lock chirality-engine-tauri": locked("chirality-engine-tauri"),
    "Cargo.lock chirality-engine": locked("chirality-engine"),
    "package.json": npm(JSON.parse(files.npmPackage).dependencies["@chirality/engine-ui"]),
    "package-lock.json root": npm(lock.packages[""].dependencies["@chirality/engine-ui"]),
    "package-lock.json resolved": npm(lock.packages["node_modules/@chirality/engine-ui"]?.resolved),
  };
}

const files = { cargoToml, cargoLock, npmPackage, npmLock };

describe("the engine pin", () => {
  it("is one revision in each manifest and each locked entry", () => {
    const found = pins(files);
    const rev = found["Cargo.toml"];
    expect(rev).toMatch(/^[0-9a-f]{40}$/);
    expect(found).toEqual(Object.fromEntries(Object.keys(found).map((k) => [k, rev])));
  });

  it("notices drift in any one entry", () => {
    const rev = pins(files)["Cargo.toml"]!;
    const other = "f".repeat(40);
    const lock = JSON.parse(npmLock);
    lock.packages["node_modules/@chirality/engine-ui"].resolved = lock.packages["node_modules/@chirality/engine-ui"].resolved.replace(rev, other);
    expect(pins({ ...files, npmLock: JSON.stringify(lock) })["package-lock.json resolved"]).toBe(other);
    const engineBlock = cargoLock.indexOf('name = "chirality-engine"\n');
    const drifted = cargoLock.slice(0, engineBlock) + cargoLock.slice(engineBlock).replace(`rev=${rev}#${rev}`, `rev=${other}#${other}`);
    expect(pins({ ...files, cargoLock: drifted })["Cargo.lock chirality-engine"]).toBe(other);
    expect(pins({ ...files, cargoLock: drifted })["Cargo.lock chirality-engine-tauri"]).toBe(rev);
    expect(pins({ ...files, cargoLock: cargoLock.replace(`rev=${rev}#${rev}`, `rev=${rev}#${other}`) })["Cargo.lock chirality-engine"]).not.toBe(rev);
  });
});

describe("the bundle's resources", () => {
  it("are the pinned edition's folder and the fonts' licence", () => {
    expect(JSON.parse(tauriConf).bundle.resources).toEqual({
      [`library/${edition.tag}/`]: `library/${edition.tag}/`,
      "../node_modules/@chirality/engine-ui/src/fonts/LICENSE-IBM-Plex-OFL.txt": "licenses/LICENSE-IBM-Plex-OFL.txt",
    });
  });
});

describe("the app's identity", () => {
  it("is a development build, apart from the installed Chirality, at one version", () => {
    const conf = JSON.parse(tauriConf);
    expect(conf.identifier).toBe("com.chirality.app.dev");
    expect(conf.productName).toBe("Chirality Dev");
    const versions = [conf.version, JSON.parse(npmPackage).version, /^version = "([^"]+)"$/m.exec(cargoToml)?.[1]];
    expect(versions).toEqual(["4.0.0-dev", "4.0.0-dev", "4.0.0-dev"]);
  });
});
