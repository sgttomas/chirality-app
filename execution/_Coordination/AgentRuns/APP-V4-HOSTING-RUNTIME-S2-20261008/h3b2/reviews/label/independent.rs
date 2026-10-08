use crate::distribution_semantics::*;
use serde_json::{json,Value};
use sha2::{Digest,Sha256};
fn pair(version:&str)->(Value,Value){(json!({"versionIdentity":{"observedVersionLabel":format!("codex-cli {version}"),"declaredPin":version}}),json!({"raw_version_label":format!("codex-cli {version}"),"observed_label":version,"pin":version}))}
#[test] fn independent_valid_forms_preserve_input_bytes(){
 for v in ["0.160.0","00.0160.000","12345.0.9"] {for lf in ["","\n"] {let(e,mut o)=pair(v);o["raw_version_label"]=format!("codex-cli {v}{lf}").into();let before=(e.clone(),o.clone());assert!(validate_label_join(&e,&o).is_ok());assert_eq!((e,o),before);}}
}
#[test] fn independent_full_label_grammar_matrix(){
 for bad in ["codex-cli 0.160.0\n","codex-cli 0.160.0\r\n","codex-cli 0.160.0\n\n","Codex-cli 0.160.0"," codex-cli 0.160.0","codex-cli 0.160.0 ","codex-cli 0.160.0\t","codex-cli 0.160.0\0","codex-cli ٠.160.0","codex-cli 0.160","codex-cli 0.160.0.1","codex-cli +0.160.0","0.160.0","codex-cli 0..0"] {
 let(mut e,o)=pair("0.160.0");e["versionIdentity"]["observedVersionLabel"]=bad.into();assert!(validate_label_join(&e,&o).is_err(),"legacy {bad:?}");
 if bad!="codex-cli 0.160.0\n" {let(e,mut o)=pair("0.160.0");o["raw_version_label"]=bad.into();assert!(validate_label_join(&e,&o).is_err(),"raw {bad:?}");}
 }
}
#[test] fn independent_no_coercion_missing_wrong_types_and_mismatch(){
 for value in [Value::Null,json!(0.160),json!(true),json!([]),json!({}),json!("0.0160.0"),json!("0.160.1")] {
 for field in ["observed_label","pin","raw_version_label"]{let(e,mut o)=pair("0.160.0");o[field]=value.clone();assert!(validate_label_join(&e,&o).is_err());}
 for field in ["declaredPin","observedVersionLabel"]{let(mut e,o)=pair("0.160.0");e["versionIdentity"][field]=value.clone();assert!(validate_label_join(&e,&o).is_err());}
 }
 for e in [json!({}),json!({"versionIdentity":null}),json!({"versionIdentity":{}})] {assert!(validate_label_join(&e,&pair("0.160.0").1).is_err());}
}
#[test] fn independent_reader_identity_binds_exact_compiled_sources(){
 let i=label_join_identity();let digest=|b:&[u8]|format!("{:x}",Sha256::digest(b));assert_eq!(i["readerSourceSha256"],digest(include_bytes!("distribution_semantics.rs")));assert_eq!(i["schemas"]["lifecycle-event.s1"],"e5713e88c720b2c4a2a1463923596e18b53302e3fae9195d433190ed098d0181");assert_eq!(i["schemas"]["observed-verification.s1"],"7f61951db0ba0db5a886a4100847f51e1a3c86f0ceae4b074918a94f353368a1");assert_eq!(i["scope"],"version-label-join-only");
}
