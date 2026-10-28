//! Pure production preparation used by the credential-free native supplier check.
//! This example cannot mint an App Host/private-receipt admission.
#[cfg(feature = "synthetic-distribution-anchor")]
fn main() -> Result<(), String> {
    let args = std::env::args().skip(1).collect::<Vec<_>>();
    if args.len() != 4 && args.len() != 6 {
        return Err("expected reading.json instructions-directory data-directory ROLE|none [owned-config-link target]".into());
    }
    let reading = serde_json::from_slice(
        &std::fs::read(&args[0]).map_err(|_| "synthetic config input unavailable")?,
    )
    .map_err(|_| "synthetic config input invalid")?;
    let role = if args[3] == "none" {
        None
    } else {
        Some(
            serde_json::from_value(serde_json::Value::String(args[3].clone()))
                .map_err(|_| "synthetic role invalid")?,
        )
    };
    let link = if args.len() == 6 {
        Some((
            std::path::PathBuf::from(&args[4]),
            std::path::PathBuf::from(&args[5]),
        ))
    } else {
        None
    };
    let output = chirality_app_v4_lib::child_roles::supplier_fixture(
        &reading,
        std::path::Path::new(&args[1]),
        std::path::Path::new(&args[2]),
        role,
        link,
    )?;
    println!(
        "{}",
        serde_json::to_string(&output).map_err(|_| "synthetic output invalid")?
    );
    Ok(())
}
#[cfg(not(feature = "synthetic-distribution-anchor"))]
fn main() {
    eprintln!("explicit synthetic-distribution-anchor feature required");
    std::process::exit(2);
}
