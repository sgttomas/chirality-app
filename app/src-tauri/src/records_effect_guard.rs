//! Test-only control shared by filesystem effect entry hooks.
// A read-only examination must fail even when an attempted sync or lock
// would leave identical bytes. Thread-local, so unrelated fixture setup and
// other tests cannot supply or consume the proof.
thread_local! { static FORBID_MUTATIONS: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
pub(crate) fn mutation_for_test(operation: &str) {
    FORBID_MUTATIONS.with(|forbidden| {
        assert!(
            !forbidden.get(),
            "read-only inspection attempted {operation}"
        )
    });
}
pub(crate) fn without_mutations_for_test<T>(read: impl FnOnce() -> T) -> T {
    struct Reset(bool);
    impl Drop for Reset {
        fn drop(&mut self) {
            FORBID_MUTATIONS.with(|slot| slot.set(self.0));
        }
    }
    let _reset = Reset(FORBID_MUTATIONS.with(|slot| slot.replace(true)));
    read()
}
