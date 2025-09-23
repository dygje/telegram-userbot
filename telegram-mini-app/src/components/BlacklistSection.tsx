import { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { BlacklistedChat } from '../types';
import { ActiveSection } from '../types';

interface BlacklistSectionProps {
  navigateTo: (section: ActiveSection) => void;
}

export default function BlacklistSection({ navigateTo }: BlacklistSectionProps) {
  const [blacklistedChats, setBlacklistedChats] = useState<BlacklistedChat[]>([]);

  const fetchBlacklist = async (): Promise<void> => {
    try {
      const response = await fetch('/api/v1/blacklist');
      if (response.ok) {
        const data = await response.json();
        setBlacklistedChats(data.blacklisted_chats);
      }
    } catch (error) {
      console.error('Error fetching blacklist:', error);
    }
  };

  useEffect(() => {
    fetchBlacklist();
  }, []);

  const handleRemoveFromBlacklist = async (chatId: string): Promise<void> => {
    try {
      const response = await fetch(`/api/v1/blacklist/${chatId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        WebApp.showAlert('Chat removed from blacklist successfully');
        fetchBlacklist(); // Refresh the list
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to remove chat from blacklist'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    }
  };

  return (
    <div className="section">
      <h2>Blacklist Management</h2>
      <p>View and manage blacklisted chats.</p>
      
      {blacklistedChats.length > 0 ? (
        <div className="list-section">
          <ul className="item-list">
            {blacklistedChats.map((chat: BlacklistedChat) => (
              <li key={chat.id} className="list-item">
                <div className="item-info">
                  <span className="item-name">Chat ID: {chat.chat_id}</span>
                  <span className="item-reason">Reason: {chat.reason}</span>
                  {chat.expiry_time && (
                    <span className="item-expiry">
                      Expires: {new Date(chat.expiry_time).toLocaleString()}
                    </span>
                  )}
                  {chat.is_permanent && (
                    <span className="item-permanent">Permanent</span>
                  )}
                </div>
                <button 
                  className="remove-btn" 
                  onClick={() => handleRemoveFromBlacklist(chat.chat_id)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div className="blacklist-info">
          <p>No blacklisted chats at the moment.</p>
        </div>
      )}
      
      <div className="button-group">
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}