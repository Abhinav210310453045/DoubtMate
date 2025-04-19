const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Store = require('electron-store');

// Initialize persistent storage
const store = new Store();

// Keep a global reference of the window object to prevent garbage collection
let mainWindow;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, '../preload/preload.js')
    },
    icon: path.join(__dirname, '../renderer/assets/icon.png')
  });

  // Load the index.html file
  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));

  // Open DevTools in development mode
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  // Emitted when the window is closed
  mainWindow.on('closed', () => {
    // Dereference the window object
    mainWindow = null;
  });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    // On macOS it's common to re-create a window when the dock icon is clicked
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers for chat functionality
ipcMain.handle('send-message', async (event, message) => {
  // Here you would typically send the message to your backend API
  // and return the response
  console.log('Message received:', message);
  
  // Mock response for now
  return {
    text: `Response to: ${message}`,
    timestamp: new Date().toISOString()
  };
});

// Get chat history from store
ipcMain.handle('get-chat-history', () => {
  return store.get('chatHistory', []);
});

// Save chat history
ipcMain.handle('save-chat-history', (event, chatHistory) => {
  store.set('chatHistory', chatHistory);
  return true;
});
