use serde_json::json;
use std::sync::{Arc,Mutex,Condvar};
struct Inner;
#[path="core_r1.rs"] mod core;
fn main(){
let host=Arc::new((Mutex::new(Inner),Condvar::new()));let g=json!({"appSession":"s","home":"h","spawnCounter":1});
let req=json!({"id":1,"method":"turn/start","params":{"threadId":"t","input":[{"type":"text","text":"q","text_elements":[]}]}});
let mut c=core::Core::bind(core::CaptureReservation::new(&host,1),&host,1,&g,"r",&req,Some((1,(2,3))));c.prewrite(&g,1,"r",(1,(2,3)),0);c.settle(&g,1,"r",Some((1,(2,3))),true);
c.observe(&g,1,1,1,&json!({"id":1,"result":{"turn":{"id":"turn","items":[],"status":"inProgress"}}}));
// Host's unchanged class rule calls has_method && has_id a server-request.
c.observe(&g,1,1,2,&json!({"id":999,"method":"item/completed","params":{"threadId":"t","turnId":"turn","completedAtMs":42,"item":{"id":"i","type":"agentMessage","text":"a","phase":"final_answer"}}}));
c.observe(&g,1,1,3,&json!({"id":998,"method":"turn/completed","params":{"threadId":"t","turn":{"id":"turn","items":[],"status":"completed","error":null}}}));
println!("{:?}",c.readout());assert!(!matches!(c.readout().0,core::Standing::ConsistentThroughReceipt(..)),"server requests cannot provide notification evidence");
}
