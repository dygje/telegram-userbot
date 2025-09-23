import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { ActiveSection } from '../types';

interface DashboardSectionProps {
  apiStatus: string;
  userbotStatus: string;
  navigateTo: (section: ActiveSection) => void;
  checkStatus: () => Promise<void>;
}

export default function DashboardSection({ apiStatus, userbotStatus, navigateTo, checkStatus }: DashboardSectionProps) {
  useEffect(() => {
    // Set up main button for quick actions
    WebApp.MainButton.text = 'Refresh Status';
    WebApp.MainButton.show();
    WebApp.MainButton.onClick(checkStatus);
    
    return () => {
      WebApp.MainButton.offClick(checkStatus);
    };
  }, [checkStatus]);

  const handleUserbotAction = async (action: 'start' | 'stop'): Promise<void> => {
    try {
      const response = await fetch(`/api/v1/userbot/${action}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        WebApp.showAlert(`Userbot ${action}ed successfully`);
        setTimeout(checkStatus, 1000);
      } else {
        WebApp.showAlert(`Failed to ${action} userbot`);
      }
    } catch (error) {
      WebApp.showAlert(`Error: ${(error as Error).message}`);
    }
  };

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      
      <div className="cards">
        <div className="card">
          <h3>Authentication</h3>
          <p>Setup Telegram API credentials and authenticate your account.</p>
          <button onClick={() => navigateTo('auth')}>Configure</button>
        </div>
        
        <div className="card">
          <h3>Group Management</h3>
          <p>Manage your Telegram groups for automatic posting.</p>
          <button onClick={() => navigateTo('groups')}>Manage Groups</button>
        </div>
        
        <div className="card">
          <h3>Message Management</h3>
          <p>Create and manage your automatic messages.</p>
          <button onClick={() => navigateTo('messages')}>Manage Messages</button>
        </div>
        
        <div className="card">
          <h3>Configuration</h3>
          <p>Configure automatic posting settings and intervals.</p>
          <button onClick={() => navigateTo('config')}>Configure Settings</button>
        </div>
        
        <div className="card">
          <h3>Userbot Control</h3>
          <p>Start or stop the userbot service.</p>
          <div className="button-group">
            <button onClick={() => handleUserbotAction('start')}>Start</button>
            <button onClick={() => handleUserbotAction('stop')}>Stop</button>
          </div>
        </div>
        
        <div className="card">
          <h3>Blacklist Management</h3>
          <p>View and manage blacklisted chats.</p>
          <button onClick={() => navigateTo('blacklist')}>Manage Blacklist</button>
        </div>
      </div>
      
      <div className="status-section">
        <h3>System Status</h3>
        <div className="status-grid">
          <div className="status-item">
            <span>API Status</span>
            <span className={apiStatus === 'Connected' ? 'green' : 'red'}>{apiStatus}</span>
          </div>
          <div className="status-item">
            <span>Userbot Status</span>
            <span className={userbotStatus === 'Running' ? 'green' : 'red'}>{userbotStatus}</span>
          </div>
          <div className="status-item">
            <span>System Load</span>
            <span className="gray">Normal</span>
          </div>
        </div>
      </div>
    </div>
  );
}