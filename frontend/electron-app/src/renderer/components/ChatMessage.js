/**
 * ChatMessage Component
 * 
 * Creates and returns a DOM element for a chat message
 * 
 * @param {Object} message - The message object
 * @param {string} message.text - The message text
 * @param {string} message.sender - The message sender ('user' or 'bot')
 * @param {string} message.timestamp - ISO timestamp string
 * @returns {HTMLElement} - The message DOM element
 */
export function createChatMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(message.sender === 'user' ? 'user-message' : 'bot-message');
  
  // Format message text
  messageElement.innerHTML = `
    <div class="message-text">${formatMessage(message.text)}</div>
    <div class="message-time">${formatTime(message.timestamp)}</div>
  `;
  
  return messageElement;
}

/**
 * Format message text with basic formatting
 * 
 * @param {string} text - The raw message text
 * @returns {string} - Formatted HTML
 */
function formatMessage(text) {
  // Replace URLs with links
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  
  // Handle basic markdown-like formatting
  return text
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(urlRegex, '<a href="$1" target="_blank">$1</a>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

/**
 * Format timestamp to readable time
 * 
 * @param {string} timestamp - ISO timestamp string
 * @returns {string} - Formatted time string
 */
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
