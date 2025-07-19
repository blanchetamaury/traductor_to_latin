const { app, BrowserWindow, ipcMain, nativeTheme } = require('electron/main')
const path = require('node:path')

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,    // recommandé pour contextBridge
      nodeIntegration: false     // pour la sécurité
    }
  })

  win.loadFile('index.html')
  //win.webContents.openDevTools()  // <–– ouvre la console automatiquement
}


ipcMain.handle('dark-mode:toggle', () => {
  if (nativeTheme.shouldUseDarkColors) {
    nativeTheme.themeSource = 'light'
  } else {
    nativeTheme.themeSource = 'dark'
  }
  return nativeTheme.shouldUseDarkColors
})

ipcMain.handle('dark-mode:system', () => {
  nativeTheme.themeSource = 'system'
})

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})


async function translate(frText) {
  try {
    const resp = await fetch("http://127.0.0.1:5000/trad", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: frText })
    });

    // 1) Vérifier le code HTTP
    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`HTTP ${resp.status}: ${errText}`);
    }

    // 2) Vérifier que c'est bien du JSON
    const contentType = resp.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      const body = await resp.text();
      console.error("Réponse inattendue (pas du JSON) :", body);
      throw new Error("Réponse non JSON du serveur");
    }

    // 3) Parse en JSON
    const data = await resp.json();
    return data.latin;
  } catch (e) {
    console.error("Erreur dans translate():", e);
    // tu peux renvoyer une chaîne vide ou afficher un message à l'utilisateur
    return "";
  }
}
