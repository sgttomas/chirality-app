use std::sync::atomic::{AtomicU8,Ordering};
fn main(){
 let state=AtomicU8::new(0);
 // First original-handle invocation reaches prepare, then waits for frame_write.
 state.compare_exchange(0,1,Ordering::SeqCst,Ordering::SeqCst).unwrap();
 // Exact failing CAS and shared error-cleanup expressions from frozen Host.
 let second:Result<(),&str>=(||{state.compare_exchange(0,1,Ordering::SeqCst,Ordering::SeqCst).map_err(|_|"original call already attempted")?; Ok(())})();
 if second.is_err(){let _=state.compare_exchange(1,5,Ordering::SeqCst,Ordering::SeqCst);}
 println!("second={second:?}; first_attempt_state={}",state.load(Ordering::SeqCst));
 assert_eq!(state.load(Ordering::SeqCst),1,"a rejected duplicate must not finalize the first invocation's prepared attempt");
}
