// DOM Elements
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const chatMessages = document.getElementById('chat-messages');

// Chat history
let chatHistory = [];

// Load chat history on startup
window.addEventListener('DOMContentLoaded', async () => {
  try {
    // Get chat history from main process
    chatHistory = await window.api.getChatHistory();
    
    // Render existing messages
    chatHistory.forEach(message => {
      addMessageToUI(message);
    });
    
    // Add welcome message if no history exists
    if (chatHistory.length === 0) {
      const welcomeMessage = {
        text: "Hello! I'm DoubtMate, your AI learning assistant. How can I help you today?",
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      
      addMessageToChat(welcomeMessage);
    }
    
    // Scroll to bottom of chat
    scrollToBottom();
  } catch (error) {
    console.error('Failed to load chat history:', error);
  }
});

// Handle message submission
messageForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;
  
  // Clear input
  messageInput.value = '';
  
  // Add user message to chat
  const userMessageObj = {
    text: userMessage,
    sender: 'user',
    timestamp: new Date().toISOString()
  };
  
  addMessageToChat(userMessageObj);
  
  try {
    // Show typing indicator
    showTypingIndicator();
    
    // Send message to main process
    const response = await window.api.sendMessage(userMessage);
    
    // Remove typing indicator
    removeTypingIndicator();
    
    // Add bot response to chat
    const botMessageObj = {
      text: response.text,
      sender: 'bot',
      timestamp: response.timestamp
    };
    
    addMessageToChat(botMessageObj);
  } catch (error) {
    console.error('Error sending message:', error);
    
    // Remove typing indicator
    removeTypingIndicator();
    
    // Show error message
    const errorMessageObj = {
      text: "Sorry, I encountered an error processing your request.",
      sender: 'bot',
      timestamp: new Date().toISOString()
    };
    
    addMessageToChat(errorMessageObj);
  }
});

// Add message to UI and chat history
function addMessageToChat(message) {
  // Add to UI
  addMessageToUI(message);
  
  // Add to chat history
  chatHistory.push(message);
  
  // Save chat history
  window.api.saveChatHistory(chatHistory);
  
  // Scroll to bottom
  scrollToBottom();
}

// Add a message to the UI
function addMessageToUI(message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(message.sender === 'user' ? 'user-message' : 'bot-message');
  
  // Format message text (handle markdown, etc.)
  messageElement.innerHTML = `
    <div class="message-text">${formatMessage(message.text)}</div>
    <div class="message-time">${formatTime(message.timestamp)}</div>
  `;
  
  chatMessages.appendChild(messageElement);
}

// Format text (basic markdown support)
function formatMessage(text) {
  // Replace URLs with links
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return text
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(urlRegex, '<a href="$1" target="_blank">$1</a>')
    .replace(/\n/g, '<br>');
}

// Format timestamp
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Show typing indicator
function showTypingIndicator() {
  const typingElement = document.createElement('div');
  typingElement.classList.add('message', 'bot-message', 'typing-indicator');
  typingElement.innerHTML = '<div class="dots"><span></span><span></span><span></span></div>';
  
  chatMessages.appendChild(typingElement);
  scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
  const typingIndicator = document.querySelector('.typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Scroll to bottom of chat
function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Auto-resize textarea
messageInput.addEventListener('input', () => {
  messageInput.style.height = 'auto';
  messageInput.style.height = messageInput.scrollHeight + 'px';
});

// Enable textarea submission with Enter key (Shift+Enter for new line)
messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    messageForm.dispatchEvent(new Event('submit'));
  }
});
