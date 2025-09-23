import { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { Message } from '../types';
import { ActiveSection } from '../types';

interface MessagesSectionProps {
  navigateTo: (section: ActiveSection) => void;
}

export default function MessagesSection({ navigateTo }: MessagesSectionProps) {
  const [messageText, setMessageText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const fetchMessages = async (): Promise<void> => {
    try {
      const response = await fetch('/api/v1/messages');
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleAddMessage = async (): Promise<void> => {
    if (!messageText) {
      WebApp.showAlert('Please enter a message');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: messageText })
      });

      if (response.ok) {
        WebApp.showAlert('Message added successfully');
        setMessageText('');
        fetchMessages(); // Refresh the list
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to add message'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMessage = async (messageId: number): Promise<void> => {
    try {
      const response = await fetch(`/api/v1/messages/${messageId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        WebApp.showAlert('Message removed successfully');
        fetchMessages(); // Refresh the list
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to remove message'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    }
  };

  return (
    <div className="section">
      <h2>Message Management</h2>
      <p>Create and manage your automatic messages.</p>
      
      <div className="form-group">
        <label>Message Text</label>
        <textarea 
          placeholder="Enter your message template"
          value={messageText}
          onChange={(e) => setMessageText(e.target.value)}
          disabled={loading}
          rows={4}
        />
      </div>
      <div className="button-group">
        <button onClick={handleAddMessage} disabled={loading}>
          {loading ? 'Adding...' : 'Add Message'}
        </button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
      
      {messages.length > 0 && (
        <div className="list-section">
          <h3>Message Templates</h3>
          <ul className="item-list">
            {messages.map((message: Message) => (
              <li key={message.id} className="list-item">
                <div className="item-info">
                  <span className="item-text">{message.text}</span>
                </div>
                <button 
                  className="remove-btn" 
                  onClick={() => handleRemoveMessage(message.id)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}