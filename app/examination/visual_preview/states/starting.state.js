// Before the first status read answers: the read is pending and never settles.
export default { title: "Starting", commands: { host_status: () => new Promise(() => {}) } };
