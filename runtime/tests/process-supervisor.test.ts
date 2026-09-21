import { describe, expect, it } from "vitest";
import { ProcessSupervisor } from "../packages/core/src/process-supervisor.js";

describe("ProcessSupervisor retirement", () => {
  it("memoizes retirement per exact generation, rejects stale generations and reports the interrupted signal", async () => {
    const supervisor = new ProcessSupervisor({ command: process.execPath, args: ["-e", "process.stdin.resume(); setTimeout(() => process.stdout.write('slow'), 60000)"], shutdownTimeoutMs: 500 });
    const worker = await supervisor.acquire("w1", "hello");
    const waiting = supervisor.wait(worker.workerId, worker.generation);
    const first = supervisor.retire(worker.workerId, worker.generation);
    const second = supervisor.retire(worker.workerId, worker.generation);
    expect(second).toBe(first);
    await first;
    await expect(waiting).resolves.toMatchObject({ exitCode: null, signal: "SIGTERM" });
    expect(await supervisor.inventory()).toEqual([]);
    await expect(supervisor.retire(worker.workerId, worker.generation)).resolves.toBeUndefined();
    await expect(supervisor.retire(worker.workerId, "stale")).rejects.toThrow("unknown or stale worker generation");
    await expect(supervisor.retire("unknown", worker.generation)).rejects.toThrow("unknown or stale worker generation");
    await supervisor.close();
  });

  it("echoes input to a completing worker and retires it cleanly", async () => {
    const supervisor = new ProcessSupervisor({ command: process.execPath, args: ["-e", "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>process.stdout.write('controlled:'+d))"] });
    const worker = await supervisor.acquire("w2", "ping");
    await expect(supervisor.wait(worker.workerId, worker.generation)).resolves.toMatchObject({ exitCode: 0, stdout: "controlled:ping" });
    await supervisor.retire(worker.workerId, worker.generation);
    expect(await supervisor.inventory()).toEqual([]);
    await supervisor.close();
  });
});
