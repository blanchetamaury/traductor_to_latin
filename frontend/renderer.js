document.getElementById('toggle-dark-mode').addEventListener('click', async () => {
  const isDarkMode = await window.darkMode.toggle()
  document.getElementById('theme-source').innerHTML = isDarkMode ? 'Dark' : 'Light'
})

document.getElementById('reset-to-system').addEventListener('click', async () => {
  await window.darkMode.system()
  document.getElementById('theme-source').innerHTML = 'System'
})

// preload.js
const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("api", {
  translate: async (frText) => {
    const resp = await fetch("http://127.0.0.1:5000/trad", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: frText })
    });
    const { latin } = await resp.json();
    return latin;
  }
});
