//! Names the pinned Library edition (`library.json`'s tag) for the app, which loads that edition only.

fn main() {
    println!("cargo:rerun-if-changed=../library.json");
    let edition = std::fs::read_to_string("../library.json").expect("library.json names the edition");
    let tag = edition
        .split_once("\"tag\"")
        .and_then(|(_, rest)| rest.split('"').nth(1))
        .filter(|tag| tag.starts_with("library-v") && tag.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '.'))
        .expect("library.json has the edition's tag");
    println!("cargo:rustc-env=CHIRALITY_LIBRARY_TAG={tag}");
    // Its folder is the bundle's one resource; empty until `npm run library` stages it, which a release does first.
    std::fs::create_dir_all(format!("library/{tag}")).expect("the edition's resource folder");
    tauri_build::build()
}
