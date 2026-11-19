// Development preview of the front end alone: the real src/ served by Vite with the host's
// commands answered from constructed snapshots. Root is app/, so /src/main.tsx is the App's own
// entry; the product build (app/vite.config.ts, index.html) never includes this folder.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

export default defineConfig({
  root: fileURLToPath(new URL("../..", import.meta.url)),
  plugins: [react()],
  clearScreen: false,
  server: { host: "127.0.0.1", port: 14207, strictPort: true },
});
