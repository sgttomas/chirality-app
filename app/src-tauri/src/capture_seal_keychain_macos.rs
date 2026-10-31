//! macOS Data Protection keychain boundary for the separately admitted SEAL-C
//! provider. No default-keychain fallback, update, delete, enumeration or migration.
//! Merely constructing an ItemIdentity does not authorize this backend: its
//! constructor requires the parent's private, checked KeychainAuthority.
use super::{Backend, BackendError, ItemIdentity, KeychainAuthority};

pub(super) struct NativeBackend<'a> {
    _authority: &'a KeychainAuthority,
}
impl<'a> NativeBackend<'a> {
    pub(super) fn new(authority: &'a KeychainAuthority) -> Self {
        Self {
            _authority: authority,
        }
    }
}
impl Backend for NativeBackend<'_> {
    fn read(&self, identity: &ItemIdentity) -> Result<Vec<u8>, BackendError> {
        if !self._authority.admits(identity) {
            return Err(BackendError::Invalid);
        }
        #[cfg(target_os = "macos")]
        {
            native::read(identity)
        }
        #[cfg(not(target_os = "macos"))]
        {
            let _ = identity;
            Err(BackendError::Unavailable(-4))
        }
    }
    fn add(&self, identity: &ItemIdentity, bytes: &[u8]) -> Result<(), BackendError> {
        if !self._authority.admits(identity) {
            return Err(BackendError::Invalid);
        }
        #[cfg(target_os = "macos")]
        {
            native::add(identity, bytes)
        }
        #[cfg(not(target_os = "macos"))]
        {
            let _ = (identity, bytes);
            Err(BackendError::Unavailable(-4))
        }
    }
}

const MAX_ITEM_BYTES: usize = 64 * 1024;
fn status(value: i32) -> Result<(), BackendError> {
    match value {
        0 => Ok(()),
        -25300 => Err(BackendError::Missing),
        -25299 => Err(BackendError::Duplicate),
        other => Err(BackendError::Unavailable(other)),
    }
}
fn validate_identity(identity: &ItemIdentity) -> Result<(), BackendError> {
    for value in [&identity.service, &identity.account, &identity.access_group] {
        if value.is_empty() || value.len() > 1024 || value.chars().any(char::is_control) {
            return Err(BackendError::Invalid);
        }
    }
    Ok(())
}

#[cfg(target_os = "macos")]
mod native {
    use super::*;
    use std::{
        ffi::{c_char, c_void, CString},
        ptr,
    };
    type Ref = *const c_void;

    // ABI and key semantics checked against the installed public macOS SDK
    // SecItem.h and CoreFoundation headers. Data Protection is available 10.15+.
    #[link(name = "Security", kind = "framework")]
    extern "C" {
        fn SecItemCopyMatching(query: Ref, result: *mut Ref) -> i32;
        fn SecItemAdd(attributes: Ref, result: *mut Ref) -> i32;
        static kSecClass: Ref;
        static kSecClassGenericPassword: Ref;
        static kSecAttrService: Ref;
        static kSecAttrAccount: Ref;
        static kSecAttrAccessGroup: Ref;
        static kSecAttrAccessible: Ref;
        static kSecAttrAccessibleWhenUnlockedThisDeviceOnly: Ref;
        static kSecAttrSynchronizable: Ref;
        static kSecUseDataProtectionKeychain: Ref;
        static kSecUseAuthenticationUI: Ref;
        static kSecUseAuthenticationUIFail: Ref;
        static kSecMatchLimit: Ref;
        static kSecMatchLimitOne: Ref;
        static kSecReturnAttributes: Ref;
        static kSecReturnData: Ref;
        static kSecValueData: Ref;
    }
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFRelease(value: Ref);
        fn CFGetTypeID(value: Ref) -> usize;
        fn CFEqual(a: Ref, b: Ref) -> u8;
        fn CFStringGetTypeID() -> usize;
        fn CFStringCreateWithCString(allocator: Ref, text: *const c_char, encoding: u32) -> Ref;
        fn CFDictionaryGetTypeID() -> usize;
        fn CFDictionaryCreate(
            allocator: Ref,
            keys: *const Ref,
            values: *const Ref,
            count: isize,
            key_callbacks: Ref,
            value_callbacks: Ref,
        ) -> Ref;
        fn CFDictionaryGetValue(dictionary: Ref, key: Ref) -> Ref;
        fn CFBooleanGetTypeID() -> usize;
        fn CFBooleanGetValue(boolean: Ref) -> u8;
        fn CFDataGetTypeID() -> usize;
        fn CFDataCreate(allocator: Ref, bytes: *const u8, length: isize) -> Ref;
        fn CFDataGetLength(data: Ref) -> isize;
        fn CFDataGetBytePtr(data: Ref) -> *const u8;
        static kCFBooleanTrue: Ref;
        static kCFBooleanFalse: Ref;
    }
    struct Owned(Ref);
    impl Drop for Owned {
        fn drop(&mut self) {
            unsafe { CFRelease(self.0) }
        }
    }
    fn owned(value: Ref) -> Result<Owned, BackendError> {
        if value.is_null() {
            Err(BackendError::Invalid)
        } else {
            Ok(Owned(value))
        }
    }
    fn string(text: &str) -> Result<Owned, BackendError> {
        let text = CString::new(text).map_err(|_| BackendError::Invalid)?;
        owned(unsafe { CFStringCreateWithCString(ptr::null(), text.as_ptr(), 0x08000100) })
    }
    fn dictionary(entries: &[(Ref, Ref)]) -> Result<Owned, BackendError> {
        let keys: Vec<_> = entries.iter().map(|entry| entry.0).collect();
        let values: Vec<_> = entries.iter().map(|entry| entry.1).collect();
        // Null callbacks mean borrowed identity/value pointers. The Owned strings
        // and data below outlive the dictionary and the synchronous Security call.
        owned(unsafe {
            CFDictionaryCreate(
                ptr::null(),
                keys.as_ptr(),
                values.as_ptr(),
                entries.len() as isize,
                ptr::null(),
                ptr::null(),
            )
        })
    }
    struct IdentityStrings {
        service: Owned,
        account: Owned,
        group: Owned,
    }
    impl IdentityStrings {
        fn new(identity: &ItemIdentity) -> Result<Self, BackendError> {
            validate_identity(identity)?;
            Ok(Self {
                service: string(&identity.service)?,
                account: string(&identity.account)?,
                group: string(&identity.access_group)?,
            })
        }
        unsafe fn entries(&self) -> Vec<(Ref, Ref)> {
            vec![
                (kSecClass, kSecClassGenericPassword),
                (kSecAttrService, self.service.0),
                (kSecAttrAccount, self.account.0),
                (kSecAttrAccessGroup, self.group.0),
                (kSecUseDataProtectionKeychain, kCFBooleanTrue),
                (kSecAttrSynchronizable, kCFBooleanFalse),
                (kSecUseAuthenticationUI, kSecUseAuthenticationUIFail),
            ]
        }
    }
    unsafe fn typed(value: Ref, expected: usize) -> Result<Ref, BackendError> {
        if value.is_null() || CFGetTypeID(value) != expected {
            Err(BackendError::Invalid)
        } else {
            Ok(value)
        }
    }
    unsafe fn same_string(value: Ref, expected: Ref) -> Result<(), BackendError> {
        typed(value, CFStringGetTypeID())?;
        if CFEqual(value, expected) == 0 {
            Err(BackendError::Invalid)
        } else {
            Ok(())
        }
    }
    unsafe fn checked_result(
        result: Ref,
        identity: &IdentityStrings,
    ) -> Result<Vec<u8>, BackendError> {
        typed(result, CFDictionaryGetTypeID())?;
        let get = |key| CFDictionaryGetValue(result, key);
        // The queried class is exact. Some SDK implementations omit kSecClass
        // from returned attribute dictionaries; if present it must agree.
        let class = get(kSecClass);
        if !class.is_null() {
            same_string(class, kSecClassGenericPassword)?;
        }
        same_string(get(kSecAttrService), identity.service.0)?;
        same_string(get(kSecAttrAccount), identity.account.0)?;
        same_string(get(kSecAttrAccessGroup), identity.group.0)?;
        same_string(
            get(kSecAttrAccessible),
            kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        )?;
        let sync = typed(get(kSecAttrSynchronizable), CFBooleanGetTypeID())?;
        if CFBooleanGetValue(sync) != 0 {
            return Err(BackendError::Invalid);
        }
        let data = typed(get(kSecValueData), CFDataGetTypeID())?;
        let length = CFDataGetLength(data);
        if length <= 0 || length as usize > MAX_ITEM_BYTES {
            return Err(BackendError::Invalid);
        }
        let bytes = CFDataGetBytePtr(data);
        if bytes.is_null() {
            return Err(BackendError::Invalid);
        }
        Ok(std::slice::from_raw_parts(bytes, length as usize).to_vec())
    }

    // Even a mistaken test call through a native backend cannot query or mutate
    // the developer's keychain. Source tests use the parent's mock Backend.
    #[cfg(test)]
    unsafe fn copy_matching(_: Ref, _: *mut Ref) -> i32 {
        -25308
    }
    #[cfg(not(test))]
    unsafe fn copy_matching(query: Ref, result: *mut Ref) -> i32 {
        SecItemCopyMatching(query, result)
    }
    #[cfg(test)]
    unsafe fn add_item(_: Ref) -> i32 {
        -25308
    }
    #[cfg(not(test))]
    unsafe fn add_item(attributes: Ref) -> i32 {
        SecItemAdd(attributes, ptr::null_mut())
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        #[test]
        fn seal_keychain_returned_attributes_and_data_must_match_exact_policy() {
            let identity = IdentityStrings::new(&ItemIdentity {
                service: "invalid.example.seal".into(),
                account: "synthetic".into(),
                access_group: "SYNTHETIC0.invalid.example.seal".into(),
            })
            .unwrap();
            // Construct CoreFoundation values only. Never call a SecItem API.
            unsafe {
                let data = owned(CFDataCreate(
                    ptr::null(),
                    b"invented-keyring".as_ptr(),
                    b"invented-keyring".len() as isize,
                ))
                .unwrap();
                let wrong = string("other.synthetic").unwrap();
                let valid = vec![
                    (kSecClass, kSecClassGenericPassword),
                    (kSecAttrService, identity.service.0),
                    (kSecAttrAccount, identity.account.0),
                    (kSecAttrAccessGroup, identity.group.0),
                    (
                        kSecAttrAccessible,
                        kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                    ),
                    (kSecAttrSynchronizable, kCFBooleanFalse),
                    (kSecValueData, data.0),
                ];
                let result = dictionary(&valid).unwrap();
                assert_eq!(
                    checked_result(result.0, &identity).unwrap(),
                    b"invented-keyring"
                );
                for key in [
                    kSecAttrService,
                    kSecAttrAccount,
                    kSecAttrAccessGroup,
                    kSecAttrAccessible,
                ] {
                    let mut altered = valid.clone();
                    altered.iter_mut().find(|entry| entry.0 == key).unwrap().1 = wrong.0;
                    assert!(checked_result(dictionary(&altered).unwrap().0, &identity).is_err());
                }
                let mut sync = valid.clone();
                sync.iter_mut()
                    .find(|entry| entry.0 == kSecAttrSynchronizable)
                    .unwrap()
                    .1 = kCFBooleanTrue;
                assert!(checked_result(dictionary(&sync).unwrap().0, &identity).is_err());
                let mut absent = valid.clone();
                absent.retain(|entry| entry.0 != kSecAttrAccessGroup);
                assert!(checked_result(dictionary(&absent).unwrap().0, &identity).is_err());
                let mut wrong_data = valid;
                wrong_data
                    .iter_mut()
                    .find(|entry| entry.0 == kSecValueData)
                    .unwrap()
                    .1 = wrong.0;
                assert!(checked_result(dictionary(&wrong_data).unwrap().0, &identity).is_err());
            }
        }
    }

    pub(super) fn read(identity: &ItemIdentity) -> Result<Vec<u8>, BackendError> {
        let identity = IdentityStrings::new(identity)?;
        unsafe {
            let mut entries = identity.entries();
            entries.extend([
                (kSecMatchLimit, kSecMatchLimitOne),
                (kSecReturnAttributes, kCFBooleanTrue),
                (kSecReturnData, kCFBooleanTrue),
            ]);
            let query = dictionary(&entries)?;
            let mut result = ptr::null();
            let code = copy_matching(query.0, &mut result);
            // Release even a non-null result accompanying an error.
            let result = if result.is_null() {
                None
            } else {
                Some(Owned(result))
            };
            status(code)?;
            checked_result(result.as_ref().ok_or(BackendError::Invalid)?.0, &identity)
        }
    }
    pub(super) fn add(identity: &ItemIdentity, bytes: &[u8]) -> Result<(), BackendError> {
        if bytes.is_empty() || bytes.len() > MAX_ITEM_BYTES {
            return Err(BackendError::Invalid);
        }
        let identity = IdentityStrings::new(identity)?;
        unsafe {
            let data = owned(CFDataCreate(
                ptr::null(),
                bytes.as_ptr(),
                bytes.len() as isize,
            ))?;
            let mut entries = identity.entries();
            entries.extend([
                (
                    kSecAttrAccessible,
                    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                ),
                (kSecValueData, data.0),
            ]);
            let attributes = dictionary(&entries)?;
            status(add_item(attributes.0))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn seal_keychain_status_distinguishes_missing_duplicate_and_denial() {
        assert!(status(0).is_ok());
        assert!(matches!(status(-25300), Err(BackendError::Missing)));
        assert!(matches!(status(-25299), Err(BackendError::Duplicate)));
        assert!(matches!(
            status(-25308),
            Err(BackendError::Unavailable(-25308))
        ));
        assert!(matches!(
            status(-34018),
            Err(BackendError::Unavailable(-34018))
        ));
    }
    #[test]
    fn seal_keychain_identity_is_bounded_and_control_free() {
        let mut item = ItemIdentity {
            service: "invalid.example.seal".into(),
            account: "synthetic-installation".into(),
            access_group: "SYNTHETIC0.invalid.example.seal".into(),
        };
        assert!(validate_identity(&item).is_ok());
        item.service.push('\0');
        assert!(validate_identity(&item).is_err());
        item.service = "s".into();
        item.account.clear();
        assert!(validate_identity(&item).is_err());
        item.account = "a".into();
        item.access_group = "x".repeat(1025);
        assert!(validate_identity(&item).is_err());
    }
}
