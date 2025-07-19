// preload.js
const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("api", {
  translate: async (text) => {
    const resp = await fetch("http://127.0.0.1:5000/trad", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    return (await resp.json()).latin;
  }
});
