const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('api', {
  // Send a message to the chatbot
  sendMessage: (message) => {
    return ipcRenderer.invoke('send-message', message);
  },
  
  // Get chat history
  getChatHistory: () => {
    return ipcRenderer.invoke('get-chat-history');
  },
  
  // Save chat history
  saveChatHistory: (chatHistory) => {
    return ipcRenderer.invoke('save-chat-history', chatHistory);
  }
});
