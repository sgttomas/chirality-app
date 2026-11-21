import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  clearScreen: false,
  // src-tauri holds the staged Library and Cargo's output, none of it the interface's source.
  server: { host: "127.0.0.1", port: 1420, strictPort: true, watch: { ignored: ["**/src-tauri/**"] } },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["src/test-setup.ts"],
    // The engine's interface parts come as TypeScript source.
    server: { deps: { inline: [/@chirality\/engine-ui/] } },
  },
});
