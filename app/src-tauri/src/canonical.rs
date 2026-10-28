//! Offer digest `aac-offer-digest/0.1`, written from the text of DEL-01-04
//! APP_ACT_CONTROL.md §5.1 ("Offer digest (AAC-v0.3)"), not from a JSON library's
//! serializer: keys sorted in code-point order, `,` and `:` with no whitespace,
//! the escapes listed there and every other character as itself, integers only.

use crate::util::sha256_hex;
use serde_json::Value;

pub const OFFER_DIGEST_METHOD: &str = "aac-offer-digest/0.1";

pub fn canonical(v: &Value, out: &mut String) -> Result<(), String> {
    match v {
        Value::Null => out.push_str("null"),
        Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                out.push_str(&i.to_string());
            } else if let Some(u) = n.as_u64() {
                out.push_str(&u.to_string());
            } else {
                // §5.1: the method is not defined over a non-integer number.
                return Err("non-integer number: the offer is not offered".into());
            }
        }
        Value::String(s) => string(s, out),
        Value::Array(a) => {
            out.push('[');
            for (k, x) in a.iter().enumerate() {
                if k > 0 {
                    out.push(',');
                }
                canonical(x, out)?;
            }
            out.push(']');
        }
        Value::Object(m) => {
            // Rust's String order is UTF-8 byte order, which equals code-point order.
            let mut keys: Vec<&String> = m.keys().collect();
            keys.sort();
            out.push('{');
            for (k, key) in keys.iter().enumerate() {
                if k > 0 {
                    out.push(',');
                }
                string(key, out);
                out.push(':');
                canonical(&m[*key], out)?;
            }
            out.push('}');
        }
    }
    Ok(())
}

fn string(s: &str, out: &mut String) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\u{08}' => out.push_str("\\b"),
            '\t' => out.push_str("\\t"),
            '\n' => out.push_str("\\n"),
            '\u{0C}' => out.push_str("\\f"),
            '\r' => out.push_str("\\r"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
}

/// sha-256, lowercase hex, of the offer without its `offerDigest` member.
pub fn offer_digest(offer: &Value) -> Result<String, String> {
    let mut o = offer.clone();
    if let Some(m) = o.as_object_mut() {
        m.remove("offerDigest");
    }
    let mut s = String::new();
    canonical(&o, &mut s)?;
    Ok(sha256_hex(s.as_bytes()))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn escapes_and_order() {
        let mut s = String::new();
        canonical(&json!({"b": "x\u{2028}ü≈\u{7f}\u{1}\n", "a": [1, -2, true, null]}), &mut s).unwrap();
        assert_eq!(s, "{\"a\":[1,-2,true,null],\"b\":\"x\u{2028}ü≈\u{7f}\\u0001\\n\"}");
    }

    #[test]
    fn refuses_non_integer() {
        let mut s = String::new();
        assert!(canonical(&json!({"x": 1.5}), &mut s).is_err());
    }
}
