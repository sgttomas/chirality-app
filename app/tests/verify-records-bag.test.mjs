import { test } from "node:test";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

test("standalone BagIt byte verifier refuses leaf replacements and inventory races", () => {
  execFileSync("python3", [fileURLToPath(new URL("./verify_records_bag_test.py", import.meta.url))], { stdio: "inherit" });
});
