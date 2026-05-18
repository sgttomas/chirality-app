"use strict";

/* eslint-disable @typescript-eslint/no-require-imports */
const { contextBridge, ipcRenderer } = require("electron");

const chiralityDesktopApi = {
  checkForUpdates() {
    return ipcRenderer.invoke("desktop:update:check");
  },
  openDownloadPage(url) {
    return ipcRenderer.invoke("desktop:update:open-download", url);
  },
};

if (process.contextIsolation) {
  contextBridge.exposeInMainWorld("chiralityDesktop", chiralityDesktopApi);
} else {
  window.chiralityDesktop = chiralityDesktopApi;
}
