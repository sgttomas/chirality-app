//! Native-only credential field. No renderer secret argument or persistent App copy.
#[derive(Clone, Copy)]
pub(crate) enum Labels {
    HomeKey,
}
/// The local field's explanation, naming the address the receiving Codex process is bound to.
/// The caller passes the validated address in force; nothing here reads a file.
pub(crate) fn local_text(address: &str) -> String {
    format!("Codex stores this key only in the dedicated oMLX home. Destination: {address}. No account-home configuration is shared. Configured does not mean verified.")
}
pub(crate) fn local(
    app: &tauri::AppHandle,
    window: tauri::Window,
    address: &str,
    current: impl Fn() -> bool + Send + Sync + 'static,
) -> Result<Option<String>, ()> {
    #[cfg(target_os = "macos")]
    {
        let informative = std::ffi::CString::new(local_text(address)).map_err(|_| ())?;
        let (sender, receiver) = std::sync::mpsc::sync_channel(1);
        app.run_on_main_thread(move || {
            use raw_window_handle::{HasDisplayHandle, HasWindowHandle};
            let original = || window.window_handle().is_ok() && window.display_handle().is_ok();
            let value = if original() && current() {
                unsafe { mac_secure_entry::show_local(&informative) }
            } else {
                Err(())
            };
            let value = if original() && current() {
                value
            } else {
                Err(())
            };
            let _ = sender.send(value);
        })
        .map_err(|_| ())?;
        receiver.recv().map_err(|_| ())?
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = (app, window, address, current);
        Err(())
    }
}
#[cfg(target_os = "macos")]
pub(crate) mod mac_secure_entry {
    use std::ffi::{c_char, c_void, CStr};
    type Id = *mut c_void;
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Point {
        x: f64,
        y: f64,
    }
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Size {
        width: f64,
        height: f64,
    }
    #[repr(C)]
    #[derive(Clone, Copy)]
    struct Rect {
        origin: Point,
        size: Size,
    }
    #[link(name = "AppKit", kind = "framework")]
    extern "C" {}
    #[link(name = "objc")]
    extern "C" {
        fn objc_getClass(name: *const c_char) -> Id;
        fn sel_registerName(name: *const c_char) -> Id;
        fn objc_msgSend();
    }
    unsafe fn selector(name: &'static [u8]) -> Id {
        sel_registerName(name.as_ptr().cast())
    }
    unsafe fn class(name: &'static [u8]) -> Id {
        objc_getClass(name.as_ptr().cast())
    }
    unsafe fn id(receiver: Id, name: &'static [u8]) -> Id {
        let f: unsafe extern "C" fn(Id, Id) -> Id = std::mem::transmute(objc_msgSend as *const ());
        f(receiver, selector(name))
    }
    unsafe fn object(receiver: Id, name: &'static [u8], value: Id) {
        let f: unsafe extern "C" fn(Id, Id, Id) = std::mem::transmute(objc_msgSend as *const ());
        f(receiver, selector(name), value);
    }
    unsafe fn string(text: &'static [u8]) -> Id {
        let f: unsafe extern "C" fn(Id, Id, *const c_char) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        f(
            class(b"NSString\0"),
            selector(b"stringWithUTF8String:\0"),
            text.as_ptr().cast(),
        )
    }
    unsafe fn owned_string(text: &CStr) -> Id {
        let f: unsafe extern "C" fn(Id, Id, *const c_char) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        f(
            class(b"NSString\0"),
            selector(b"stringWithUTF8String:\0"),
            text.as_ptr(),
        )
    }
    unsafe fn release(value: Id) {
        let f: unsafe extern "C" fn(Id, Id) = std::mem::transmute(objc_msgSend as *const ());
        f(value, selector(b"release\0"));
    }
    pub(crate) unsafe fn show(labels: super::Labels) -> Result<Option<String>, ()> {
        match labels {
            super::Labels::HomeKey => present(
                string(b"Add or replace API key through Codex\0"),
                string(b"The key is delivered once to this separate App key home. Native acknowledgment does not establish validity until actual use.\0"),
            ),
        }
    }
    /// The local field, with the explanation built by `local_text` for the address in force.
    pub(crate) unsafe fn show_local(informative: &CStr) -> Result<Option<String>, ()> {
        present(
            string(b"Add oMLX key through its local Codex home\0"),
            owned_string(informative),
        )
    }
    unsafe fn present(message: Id, informative: Id) -> Result<Option<String>, ()> {
        let pool = id(class(b"NSAutoreleasePool\0"), b"new\0");
        let alert = id(class(b"NSAlert\0"), b"new\0");
        let allocated = id(class(b"NSSecureTextField\0"), b"alloc\0");
        let initialize: unsafe extern "C" fn(Id, Id, Rect) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        let field = initialize(
            allocated,
            selector(b"initWithFrame:\0"),
            Rect {
                origin: Point { x: 0., y: 0. },
                size: Size {
                    width: 360.,
                    height: 26.,
                },
            },
        );
        if pool.is_null() || alert.is_null() || field.is_null() {
            if !field.is_null() {
                release(field);
            }
            if !alert.is_null() {
                release(alert);
            }
            if !pool.is_null() {
                release(pool);
            }
            return Err(());
        }
        if message.is_null() || informative.is_null() {
            object(field, b"setStringValue:\0", string(b"\0"));
            release(field);
            release(alert);
            release(pool);
            return Err(());
        }
        object(alert, b"setMessageText:\0", message);
        object(alert, b"setInformativeText:\0", informative);
        object(alert, b"setAccessoryView:\0", field);
        let add: unsafe extern "C" fn(Id, Id, Id) -> Id =
            std::mem::transmute(objc_msgSend as *const ());
        add(
            alert,
            selector(b"addButtonWithTitle:\0"),
            string(b"Submit key\0"),
        );
        add(
            alert,
            selector(b"addButtonWithTitle:\0"),
            string(b"Cancel\0"),
        );
        let modal: unsafe extern "C" fn(Id, Id) -> isize =
            std::mem::transmute(objc_msgSend as *const ());
        let accepted = modal(alert, selector(b"runModal\0")) == 1000;
        let result = if accepted {
            let value = id(field, b"stringValue\0");
            let length: unsafe extern "C" fn(Id, Id, usize) -> usize =
                std::mem::transmute(objc_msgSend as *const ());
            let n = length(value, selector(b"lengthOfBytesUsingEncoding:\0"), 4);
            let pointer: unsafe extern "C" fn(Id, Id) -> *const u8 =
                std::mem::transmute(objc_msgSend as *const ());
            let bytes = pointer(value, selector(b"UTF8String\0"));
            if bytes.is_null() || n == 0 {
                Err(())
            } else {
                std::str::from_utf8(std::slice::from_raw_parts(bytes, n))
                    .map(|text| Some(text.to_owned()))
                    .map_err(|_| ())
            }
        } else {
            Ok(None)
        };
        // Release the secure field before the caller receives its one transient
        // buffer. Ordinary drop/release is not allocator/OS physical erasure.
        object(field, b"setStringValue:\0", string(b"\0"));
        release(field);
        release(alert);
        release(pool);
        result
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn native_local_secure_entry_text_names_the_address_in_force_not_a_fixed_one() {
        let text = super::local_text("http://[::1]:9100/api/v1");
        assert!(text.contains("Destination: http://[::1]:9100/api/v1."), "{text}");
        assert!(!text.contains("8000"), "no fixed destination: {text}");
        assert!(super::local_text("http://127.0.0.1:8000/v1").contains("Destination: http://127.0.0.1:8000/v1."));
    }
}
