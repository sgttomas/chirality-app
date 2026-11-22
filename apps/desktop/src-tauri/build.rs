//! Names the pinned Library edition (`library.json`'s tag) and the pinned Codex (`codex.json`'s tag and
//! entrypoint) for the app, which loads that edition and runs that Codex only.

/// A string field of a pin file, checked to be a plain path segment (or, for an entrypoint, plain segments).
fn field(file: &str, name: &str, ok: impl Fn(&str) -> bool) -> String {
    println!("cargo:rerun-if-changed={file}");
    let pin = std::fs::read_to_string(file).unwrap_or_else(|_| panic!("{file} names the pin"));
    pin.split_once(&format!("\"{name}\""))
        .and_then(|(_, rest)| rest.split('"').nth(1))
        .filter(|value| ok(value))
        .unwrap_or_else(|| panic!("{file} has the {name}"))
        .to_owned()
}

fn plain(segment: &str) -> bool {
    !segment.is_empty() && segment != "." && segment != ".." && segment.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '.' || c == '_')
}

fn main() {
    let tag = field("../library.json", "tag", |t| t.starts_with("library-v") && plain(t));
    println!("cargo:rustc-env=CHIRALITY_LIBRARY_TAG={tag}");
    let codex = field("../codex.json", "tag", |t| t.starts_with("codex-") && plain(t));
    let entrypoint = field("../codex.json", "entrypoint", |e| e.split('/').all(plain));
    let target = field("../codex.json", "target", plain);
    let building = std::env::var("TARGET").expect("cargo names the target");
    let staged = std::fs::read_dir(format!("codex/{codex}")).is_ok_and(|mut entries| entries.next().is_some());
    assert!(!staged || building == target, "Codex is bundled for {target} only; this build is for {building}");
    println!("cargo:rustc-env=CHIRALITY_CODEX_TAG={codex}");
    println!("cargo:rustc-env=CHIRALITY_CODEX_ENTRYPOINT={entrypoint}");
    // Their folders are bundle resources; empty until `npm run library` and `npm run codex` stage them,
    // which a build does first.
    std::fs::create_dir_all(format!("library/{tag}")).expect("the edition's resource folder");
    std::fs::create_dir_all(format!("codex/{codex}")).expect("Codex's resource folder");
    tauri_build::build()
}
