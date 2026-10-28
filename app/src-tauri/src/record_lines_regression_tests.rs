//! Differential R-2 contract checks against the pre-optimization interpretation.
//! The old oracle intentionally retains eager Value lookahead and raw hashing;
//! it never supplies runtime authority or an alternate production reader.
use super::*;
fn old_parse_reader(
    mut reader: impl std::io::BufRead,
    name: &str,
    first: usize,
    base: u64,
    mut expected: u64,
    mut chain: Chain,
    each: &mut dyn FnMut(ParsedLine),
) -> std::io::Result<Parsed> {
    fn read(reader: &mut impl std::io::BufRead) -> std::io::Result<Vec<u8>> {
        let mut raw = Vec::new();
        reader.read_until(b'\n', &mut raw)?;
        Ok(raw)
    }
    let validator = crate::schema_validation::bundled();
    let mut raw = read(&mut reader)?;
    let mut offset = base;
    let mut no = first;
    while raw.ends_with(b"\n") {
        raw.pop();
        let next = read(&mut reader)?;
        no += 1;
        let mut line = ParsedLine {
            no,
            offset,
            len: raw.len(),
            digest: line_identity(&raw),
            entries: vec![],
            limits: vec![],
            notes: vec![],
            expected_before: expected,
            chain_before: chain.clone(),
        };
        // Only a complete following line can name a recovered partial. A
        // still-torn W-0 observation is not evidence that recovery happened.
        let mut recovered = false;
        if next.ends_with(b"\n") {
            if let Ok(v) = serde_json::from_slice::<Value>(&next[..next.len() - 1]) {
                let named = v["body"]["subjectRef"].as_str().unwrap_or_default();
                if v["kind"] == "evidence_limit"
                    && v["body"]["label"] == crate::records::PARTIAL_NOT_RECOVERED
                    && named.starts_with(&format!("line {no};"))
                {
                    let mismatch = if named != crate::records::torn_line_ref(no, &raw) {
                        Some(format!("line {no}: the \"partial entry not recovered\" limit after it names other bytes; read as written"))
                    } else if is_valid_line(&raw) {
                        Some(format!("line {no}: a complete entry, although the limit after it names it as torn; read as written"))
                    } else {
                        recovered = true;
                        None
                    };
                    line.limits.extend(mismatch.map(|m| format!("{name}: {m}")));
                }
            }
        }
        if recovered {
            line.notes.push(format!("{name}: line {no} is a torn line W-0 terminated; it is not a chain link, and the next line links to the line before it"));
        } else if !raw
            .strip_suffix(b"\r")
            .unwrap_or(&raw)
            .iter()
            .all(u8::is_ascii_whitespace)
        {
            let decoded = match &validator {
                Ok(v) => decode_line(&raw, v),
                Err(e) => Err(NotRead::Invalid(e.clone())),
            };
            match decoded {
                Ok((entries, link)) => {
                    if let Err(broken) = chain.step(no, &raw, link.as_ref()) {
                        line.limits.push(format!("{name}: {broken}"));
                    }
                    for entry in &entries {
                        let seq = entry["seq"].as_u64().unwrap_or(0);
                        if seq != expected {
                            line.limits.push(format!("{name}: sequence incomplete/disagrees: expected {expected}, found {seq} at line {no}"));
                        }
                        expected = seq.checked_add(1).unwrap_or(seq);
                    }
                    line.entries = entries;
                }
                Err(not_read) => {
                    chain.last = Some(line_identity(&raw));
                    chain.lines += 1;
                    line.limits.push(match not_read {
                        NotRead::Unreadable => format!("{name}: unreadable line {no}"),
                        NotRead::Invalid(e) => format!("{name}: invalid line {no}: {e}"),
                    });
                }
            }
        }
        each(line);
        offset += raw.len() as u64 + 1;
        raw = next;
    }
    let partial_tail = (!raw.is_empty() && !raw.iter().all(u8::is_ascii_whitespace))
        .then(|| format!("{name}: partial entry at end (not read)"));
    Ok(Parsed {
        lines: Vec::new(),
        partial_tail,
        tail_offset: offset,
        chain,
    })
}
fn chain_value(c: &Chain) -> Value {
    json!({"last":c.last,"lines":c.lines,"linked":c.linked,"unchained":c.unchained})
}
fn snapshot(parsed: Parsed) -> Value {
    json!({"lines":parsed.lines.into_iter().map(|line|json!({"no":line.no,"offset":line.offset,"len":line.len,"digest":line.digest,
        "entries":line.entries,"limits":line.limits,"notes":line.notes,"expectedBefore":line.expected_before,"chainBefore":chain_value(&line.chain_before)})).collect::<Vec<_>>(),
        "partial":parsed.partial_tail,"tailOffset":parsed.tail_offset,"chain":chain_value(&parsed.chain)})
}
fn old_parse(bytes: &[u8], first: usize, base: u64, expected: u64, chain: Chain) -> Parsed {
    let mut lines = Vec::new();
    let mut read = old_parse_reader(
        std::io::Cursor::new(bytes),
        "source",
        first,
        base,
        expected,
        chain,
        &mut |l| lines.push(l),
    )
    .unwrap();
    read.lines = lines;
    read
}
fn compare(bytes: &[u8]) {
    for (first, base, expected, chain) in [
        (0, 0, 1, Chain::default()),
        (
            7,
            139,
            8,
            Chain {
                last: Some(line_identity(b"earlier exact line\r")),
                lines: 7,
                linked: true,
                unchained: 2,
            },
        ),
    ] {
        let prior = snapshot(old_parse(bytes, first, base, expected, chain.clone()));
        let current = parse(bytes, "source", first, base, expected, chain.clone());
        // The independent raw-byte check catches accidental normalization or
        // hashing a parsed/reserialized Value even if chain comparisons agree.
        for (line, raw) in current.lines.iter().zip(
            bytes
                .split_inclusive(|b| *b == b'\n')
                .filter_map(|r| r.strip_suffix(b"\n")),
        ) {
            assert_eq!(line.digest, crate::util::sha256_hex(raw));
            assert_eq!(line.len, raw.len());
        }
        assert_eq!(
            snapshot(current),
            prior,
            "slice interpretation changed for {bytes:?}"
        );
        for size in [1, 3, 17] {
            let mut lines = Vec::new();
            let mut stream = parse_reader(
                std::io::BufReader::with_capacity(size, std::io::Cursor::new(bytes)),
                "source",
                first,
                base,
                expected,
                chain.clone(),
                &mut |l| lines.push(l),
            )
            .unwrap();
            stream.lines = lines;
            assert_eq!(
                snapshot(stream),
                prior,
                "stream interpretation changed (buffer {size}) for {bytes:?}"
            );
        }
    }
}
fn entry(seq: u64) -> Value {
    let mut e = crate::records::envelope(
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"invented","detail":"ordinary ü bytes"}),
        format!("rec:app:r2-{seq}"),
        seq,
        None,
        Some("2026-10-12T00:00:00.000Z"),
    );
    e["prevLine"] = link(None);
    e
}
fn append_line(out: &mut Vec<u8>, raw: &[u8]) {
    out.extend(raw);
    out.push(b'\n');
}
fn marker(raw: &[u8], no: usize) -> Value {
    let mut e = entry(1);
    e["body"] = json!({"label":crate::records::PARTIAL_NOT_RECOVERED,"subjectRef":crate::records::torn_line_ref(no,raw)});
    e
}
fn corpus() -> Vec<Vec<u8>> {
    let ordinary = serde_json::to_vec(&entry(1)).unwrap();
    let mut two = entry(2);
    two["prevLine"] = link(Some(&line_identity(&ordinary)));
    let mut group = json!({"format":GROUP_FORMAT,"formatVersion":"0.1","groupId":"grp:app:r2-regression","prevLine":null,"entries":[entry(1),entry(2)]});
    for member in group["entries"].as_array_mut().unwrap() {
        member.as_object_mut().unwrap().remove("prevLine");
    }
    group["prevLine"] = link(None);
    crate::schema_validation::bundled()
        .unwrap()
        .validate_group(&group)
        .unwrap();
    let group_bytes = serde_json::to_vec(&group).unwrap();
    let mut bad_group = group.clone();
    bad_group["entries"][1]["seq"] = json!(99);
    let currents = vec![
        ordinary.clone(),
        group_bytes,
        serde_json::to_vec(&bad_group).unwrap(),
        b" \t\r".to_vec(),
        b"{\"torn\":".to_vec(),
        vec![0xff, b'\r'],
        b"{\"unknown\":true}".to_vec(),
        [b" \t".as_slice(), &ordinary, b"  \r"].concat(),
        b"[]".to_vec(),
    ];
    let mut cases = Vec::new();
    for raw in currents {
        let m = marker(&raw, 1);
        let plain = serde_json::to_string(&m).unwrap();
        let mut wrong = m.clone();
        wrong["body"]["subjectRef"] = json!("line 1; 999 bytes; sha256 wrong");
        let mut other = m.clone();
        other["body"]["subjectRef"] = json!(crate::records::torn_line_ref(2, &raw));
        let body = serde_json::to_string(&m["body"]).unwrap();
        let marker_like_group = format!(
            "{{\"format\":\"{GROUP_FORMAT}\",\"kind\":\"evidence_limit\",\"body\":{body}}}"
        );
        let variants=vec![
            plain.clone(),format!(" \t{plain}  \r"),serde_json::to_string(&wrong).unwrap(),serde_json::to_string(&other).unwrap(),
            plain.replace("\"kind\"","\"k\\u0069nd\"").replace("\"body\"","\"b\\u006fdy\"").replace("partial entry not recovered","partial\\u0020entry not recovered").replace("\"subjectRef\"","\"subject\\u0052ef\"").replace("line 1;","line\\u00201;"),
            format!("{{\"kind\":\"model_turn\",\"kind\":\"evidence_limit\",\"body\":{body}}}"),
            format!("{{\"kind\":\"evidence_limit\",\"kind\":\"model_turn\",\"body\":{body}}}"),
            format!("{{\"kind\":\"evidence_limit\",\"body\":null,\"body\":{body}}}"),
            format!("{{\"kind\":\"evidence_limit\",\"body\":{body},\"body\":null}}"),
            format!("{{\"kind\":\"evidence_limit\",\"body\":{{\"label\":\"other\",\"label\":\"partial entry not recovered\",\"subjectRef\":{}}}}}",serde_json::to_string(&m["body"]["subjectRef"]).unwrap()),
            marker_like_group,format!("{plain} false"),"false".into(),"{\"body\":\"partial entry not recovered\"}".into(),
            "{\"kind\":\"evidence_limit\",\"body\":{\"label\":\"different\",\"detail\":\"escaped \\\\ bytes\"}}".into(),
            serde_json::to_string(&two).unwrap(),"{\"kind\":\"other\",\"kind\":\"model_turn\"}".into(),
        ];
        for next in variants {
            for terminated in [false, true] {
                let mut bytes = Vec::new();
                append_line(&mut bytes, &raw);
                bytes.extend(next.as_bytes());
                if terminated {
                    bytes.push(b'\n');
                }
                cases.push(bytes);
            }
        }
    }
    // Ordinary chains, exact CR/padding bytes, unchained prefix, later missing
    // or wrong-method links, sequence gaps and trailing partial/blank bytes.
    for padding in ["", " \r", " \t "] {
        let raw = [ordinary.as_slice(), padding.as_bytes()].concat();
        let mut after = entry(2);
        after["prevLine"] = link(Some(&line_identity(&raw)));
        for edit in 0..4 {
            let mut after = after.clone();
            match edit {
                1 => {
                    after.as_object_mut().unwrap().remove("prevLine");
                }
                2 => after["prevLine"]["method"] = json!("unknown"),
                3 => after["seq"] = json!(7),
                _ => {}
            }
            for tail in [b"".as_slice(), b" ", b"{\"partial\":", b"\r\n"] {
                let mut bytes = Vec::new();
                append_line(&mut bytes, &raw);
                append_line(&mut bytes, &serde_json::to_vec(&after).unwrap());
                bytes.extend(tail);
                cases.push(bytes);
            }
        }
    }
    cases
}
#[test]
fn optimized_r2_preserves_previous_whole_interpretation_for_adversarial_streams() {
    let cases = corpus();
    for bytes in &cases {
        compare(bytes);
    }
    assert!(cases.len() > 300);
}
#[test]
fn invalid_marker_envelopes_and_escaped_last_wins_fields_still_name_recovery() {
    let raw = b"{\"invented-torn\":";
    let reference = serde_json::to_string(&crate::records::torn_line_ref(1, raw)).unwrap();
    let next=format!("{{\"format\":\"{GROUP_FORMAT}\",\"kind\":\"other\",\"k\\u0069nd\":\"evidence_limit\",\"body\":null,\"b\\u006fdy\":{{\"label\":\"other\",\"lab\\u0065l\":\"partial\\u0020entry not recovered\",\"subjectRef\":{reference}}}}}");
    let mut bytes = Vec::new();
    append_line(&mut bytes, raw);
    append_line(&mut bytes, next.as_bytes());
    compare(&bytes);
    let read = parse(&bytes, "source", 0, 0, 1, Chain::default());
    assert!(read.lines[0].notes[0].contains("not a chain link"));
    assert!(read.lines[1].limits[0].contains("invalid line 2"));
}
#[test]
fn source_link_removal_limit_is_retained_after_the_optimized_stream_read() {
    let path = std::path::PathBuf::from(crate::util::opaque_id("r2-linked-source-").unwrap());
    let mut bytes = Vec::new();
    append_line(&mut bytes, &serde_json::to_vec(&entry(1)).unwrap());
    let read = parse(&bytes, "source", 0, 0, 1, Chain::default());
    assert!(links_removed(&path, "source", &read.chain).is_none());
    let mut legacy = entry(1);
    legacy.as_object_mut().unwrap().remove("prevLine");
    bytes.clear();
    append_line(&mut bytes, &serde_json::to_vec(&legacy).unwrap());
    compare(&bytes);
    let read = parse(&bytes, "source", 0, 0, 1, Chain::default());
    assert_eq!(links_removed(&path,"source",&read.chain),Some("source: chain broken: read with a chain earlier in this process, it now has no line carrying a link; never repaired".into()));
}
