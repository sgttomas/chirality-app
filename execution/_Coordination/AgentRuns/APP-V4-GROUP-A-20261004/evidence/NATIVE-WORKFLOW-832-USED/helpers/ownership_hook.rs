// PRIVATE COPY ONLY: pre-exec bookkeeping; no production authority or page changes.
fn parent_witness_own_spawn(command: &mut Command, stage: i32) {
    let register_fd: i32 = std::env::var("CHIRALITY_WITNESS_REGISTER_FD")
        .expect("Parent register FD")
        .parse()
        .unwrap();
    let ack_fd: i32 = std::env::var("CHIRALITY_WITNESS_ACK_FD")
        .expect("Parent ACK FD")
        .parse()
        .unwrap();
    unsafe {
        command.pre_exec(move || {
            // No allocation, locks, stdio, environment reads or non-signal-safe work here.
            if libc::fcntl(register_fd, libc::F_SETFD, libc::FD_CLOEXEC) == -1
                || libc::fcntl(ack_fd, libc::F_SETFD, libc::FD_CLOEXEC) == -1
            {
                libc::_exit(121);
            }
            let pid = libc::getpid();
            if libc::getpgrp() != pid {
                libc::_exit(122);
            }
            let packet = [pid, stage];
            if libc::write(
                register_fd,
                packet.as_ptr().cast(),
                std::mem::size_of_val(&packet),
            ) != 8
            {
                libc::_exit(123);
            }
            let mut poll = libc::pollfd {
                fd: ack_fd,
                events: libc::POLLIN,
                revents: 0,
            };
            if libc::poll(&mut poll, 1, 5000) != 1 {
                libc::_exit(124);
            }
            let mut ack = 0u8;
            if libc::read(ack_fd, (&mut ack as *mut u8).cast(), 1) != 1 || ack != 0x41 {
                libc::_exit(125);
            }
            libc::close(register_fd);
            libc::close(ack_fd);
            Ok(())
        });
    }
}
