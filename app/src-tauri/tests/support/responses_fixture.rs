// Test support only: a deterministic loopback Responses peer for the opt-in
// stock-Codex fixtures. It is not inference. Each `POST …/responses` gets the
// next scripted list of output items (the last list repeats), streamed as
// canned SSE; anything else gets 404. Only request facts are kept, never the
// request body.
//
// Shared by `tests/native_backend_smoke.rs` and the crate's own
// `runtime_session` workflow test module (included there; no product use). Both
// includers allow dead code, so the file carries no inner attributes.
use serde_json::{json, Value};
use std::{
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    sync::{
        atomic::{AtomicBool, Ordering},
        Arc, Mutex,
    },
    time::Duration,
};

/// One scripted assistant message output item.
pub fn message(id: &str, text: &str) -> Value {
    json!({"type":"message","role":"assistant","id":id,"content":[{"type":"output_text","text":text}]})
}

pub struct ResponsesFixture {
    pub port: u16,
    requests: Arc<Mutex<Vec<Value>>>,
    stop: Arc<AtomicBool>,
    thread: Option<std::thread::JoinHandle<()>>,
}
impl ResponsesFixture {
    /// `script[i]` is the output of the i-th Responses request (the last
    /// repeats). `markers` are `(label, text)`: each request's facts record only
    /// whether its body contained that text.
    pub fn start(script: Vec<Vec<Value>>, markers: Vec<(&'static str, String)>) -> Result<Self, &'static str> {
        if script.is_empty() {
            return Err("fixture script empty");
        }
        let listener = TcpListener::bind(("127.0.0.1", 0)).map_err(|_| "fixture bind on loopback failed")?;
        let port = listener.local_addr().map_err(|_| "fixture address unavailable")?.port();
        listener.set_nonblocking(true).map_err(|_| "fixture listener setup failed")?;
        let requests = Arc::new(Mutex::new(Vec::new()));
        let stop = Arc::new(AtomicBool::new(false));
        let (log, halt) = (Arc::clone(&requests), Arc::clone(&stop));
        let thread = std::thread::spawn(move || {
            let mut answered = 0usize;
            while !halt.load(Ordering::Relaxed) {
                match listener.accept() {
                    Ok((stream, peer)) => {
                        let fact = Self::serve(stream, peer.ip().is_loopback(), &script, &markers, &mut answered);
                        log.lock().unwrap().push(fact);
                    }
                    Err(_) => std::thread::sleep(Duration::from_millis(20)),
                }
            }
        });
        Ok(Self { port, requests, stop, thread: Some(thread) })
    }
    fn serve(
        mut stream: TcpStream,
        loopback_peer: bool,
        script: &[Vec<Value>],
        markers: &[(&'static str, String)],
        answered: &mut usize,
    ) -> Value {
        let _ = stream.set_nonblocking(false);
        let _ = stream.set_read_timeout(Some(Duration::from_secs(10)));
        let mut raw = Vec::new();
        let mut chunk = [0u8; 8192];
        let head_end = loop {
            if let Some(i) = raw.windows(4).position(|w| w == b"\r\n\r\n") {
                break Some(i + 4);
            }
            match stream.read(&mut chunk) {
                Ok(0) | Err(_) => break None,
                Ok(n) => raw.extend_from_slice(&chunk[..n]),
            }
            if raw.len() > 1 << 20 {
                break None;
            }
        };
        let Some(head_end) = head_end else {
            return json!({"loopbackPeer":loopback_peer,"parsed":false});
        };
        let head = String::from_utf8_lossy(&raw[..head_end]).to_string();
        let mut lines = head.split("\r\n");
        let mut request_line = lines.next().unwrap_or("").split(' ');
        let (method, path) = (request_line.next().unwrap_or("").to_string(), request_line.next().unwrap_or("").to_string());
        let header = |name: &str| {
            head.split("\r\n").find_map(|l| {
                let (k, v) = l.split_once(':')?;
                k.trim().eq_ignore_ascii_case(name).then(|| v.trim().to_string())
            })
        };
        let length: usize = header("content-length").and_then(|v| v.parse().ok()).unwrap_or(0);
        let mut body = raw[head_end..].to_vec();
        while body.len() < length {
            match stream.read(&mut chunk) {
                Ok(0) | Err(_) => break,
                Ok(n) => body.extend_from_slice(&chunk[..n]),
            }
            if body.len() > 16 << 20 {
                break;
            }
        }
        let encoding = header("content-encoding");
        let parsed: Option<Value> = if encoding.is_none() { serde_json::from_slice(&body).ok() } else { None };
        let responses = method == "POST" && path.ends_with("/responses");
        let text = String::from_utf8_lossy(&body);
        let found: serde_json::Map<String, Value> =
            markers.iter().map(|(label, marker)| (label.to_string(), json!(text.contains(marker.as_str())))).collect();
        // Names only: which tools were offered, and which tool results came back.
        let tools: Vec<Value> = parsed.as_ref().and_then(|b| b["tools"].as_array().cloned()).unwrap_or_default().iter()
            .map(|t| json!({"type":t["type"],"name":t.get("name").or_else(|| t.get("function").and_then(|f| f.get("name"))).cloned().unwrap_or(Value::Null)}))
            .collect();
        let outputs: Vec<Value> = parsed.as_ref().and_then(|b| b["input"].as_array().cloned()).unwrap_or_default().iter()
            .filter(|i| i["type"].as_str().is_some_and(|t| t.ends_with("_call_output")))
            .map(|i| json!({"type":i["type"],"callId":i["call_id"],"outputBytes":i["output"].to_string().len()}))
            .collect();
        let step = (*answered).min(script.len() - 1);
        let mut fact = json!({"loopbackPeer":loopback_peer,"parsed":true,"method":method,"path":path,
            "contentEncoding":encoding,"bodyBytes":body.len(),"bodyComplete":body.len() >= length,
            "model":parsed.as_ref().map(|b| b["model"].clone()).unwrap_or(Value::Null),
            "stream":parsed.as_ref().map(|b| b["stream"].clone()).unwrap_or(Value::Null),
            "markers":found,"tools":tools,"toolOutputs":outputs,"answered":if responses {"sse"} else {"404"}});
        let reply = if responses {
            fact["scriptStep"] = json!(step);
            *answered += 1;
            let id = format!("resp_fixture_{}", *answered);
            let mut events = vec![json!({"type":"response.created","response":{"id":id}})];
            for (index, item) in script[step].iter().enumerate() {
                let mut opened = item.clone();
                if item["type"] == "message" {
                    opened["content"] = json!([]);
                }
                events.push(json!({"type":"response.output_item.added","output_index":index,"item":opened}));
                if item["type"] == "message" {
                    for (part, content) in item["content"].as_array().into_iter().flatten().enumerate() {
                        events.push(json!({"type":"response.output_text.delta","item_id":item["id"],"output_index":index,"content_index":part,"delta":content["text"]}));
                    }
                }
                events.push(json!({"type":"response.output_item.done","output_index":index,"item":item}));
            }
            events.push(json!({"type":"response.completed","response":{"id":id,"usage":{"input_tokens":1,"input_tokens_details":null,"output_tokens":1,"output_tokens_details":null,"total_tokens":2}}}));
            let mut sse = String::new();
            for event in events {
                sse.push_str(&format!("event: {}\ndata: {}\n\n", event["type"].as_str().unwrap_or(""), event));
            }
            format!("HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}", sse.len(), sse)
        } else {
            "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".to_string()
        };
        let _ = stream.write_all(reply.as_bytes());
        let _ = stream.flush();
        fact
    }
    pub fn base_url(&self) -> String {
        format!("http://127.0.0.1:{}/v1", self.port)
    }
    pub fn requests(&self) -> Vec<Value> {
        self.requests.lock().unwrap().clone()
    }
}
impl Drop for ResponsesFixture {
    fn drop(&mut self) {
        self.stop.store(true, Ordering::Relaxed);
        if let Some(thread) = self.thread.take() {
            let _ = thread.join();
        }
    }
}
