import React, { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [userbotStatus, setUserbotStatus] = useState('Unknown');
  const [activeSection, setActiveSection] = useState('dashboard');

  // Initialize Telegram Web App
  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
    
    // Set theme
    document.documentElement.className = WebApp.colorScheme;
    
    // Check status
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      // Check API status
      const apiResponse = await fetch('/api/v1/health');
      if (apiResponse.ok) {
        setApiStatus('Connected');
      } else {
        setApiStatus('Disconnected');
      }
      
      // Check userbot status
      const userbotResponse = await fetch('/api/v1/userbot/status');
      if (userbotResponse.ok) {
        const data = await userbotResponse.json();
        setUserbotStatus(data.running ? 'Running' : 'Stopped');
      } else {
        setUserbotStatus('Unknown');
      }
    } catch (error) {
      console.error('Error checking status:', error);
      setApiStatus('Disconnected');
      setUserbotStatus('Unknown');
    }
  };

  // Navigation functions
  const navigateTo = (section) => {
    setActiveSection(section);
    WebApp.MainButton.hide();
  };

  // Render different sections based on activeSection
  const renderSection = () => {
    switch (activeSection) {
      case 'auth':
        return <AuthSection navigateTo={navigateTo} />;
      case 'groups':
        return <GroupsSection navigateTo={navigateTo} />;
      case 'messages':
        return <MessagesSection navigateTo={navigateTo} />;
      case 'config':
        return <ConfigSection navigateTo={navigateTo} />;
      case 'blacklist':
        return <BlacklistSection navigateTo={navigateTo} />;
      default:
        return <DashboardSection 
          apiStatus={apiStatus} 
          userbotStatus={userbotStatus} 
          navigateTo={navigateTo} 
          checkStatus={checkStatus}
        />;
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Telegram Userbot TMA</h1>
        <div className="status-indicators">
          <div className={`status ${apiStatus === 'Connected' ? 'connected' : 'disconnected'}`}>
            API: {apiStatus}
          </div>
          <div className={`status ${userbotStatus === 'Running' ? 'running' : 'stopped'}`}>
            Userbot: {userbotStatus}
          </div>
        </div>
      </header>
      
      <main className="main">
        {renderSection()}
      </main>
      
      <nav className="bottom-nav">
        <button 
          className={activeSection === 'dashboard' ? 'active' : ''}
          onClick={() => navigateTo('dashboard')}
        >
          Home
        </button>
        <button 
          className={activeSection === 'auth' ? 'active' : ''}
          onClick={() => navigateTo('auth')}
        >
          Auth
        </button>
        <button 
          className={activeSection === 'groups' ? 'active' : ''}
          onClick={() => navigateTo('groups')}
        >
          Groups
        </button>
        <button 
          className={activeSection === 'messages' ? 'active' : ''}
          onClick={() => navigateTo('messages')}
        >
          Messages
        </button>
        <button 
          className={activeSection === 'config' ? 'active' : ''}
          onClick={() => navigateTo('config')}
        >
          Config
        </button>
      </nav>
    </div>
  );
}

// Dashboard Section Component
function DashboardSection({ apiStatus, userbotStatus, navigateTo, checkStatus }) {
  useEffect(() => {
    // Set up main button for quick actions
    WebApp.MainButton.text = 'Refresh Status';
    WebApp.MainButton.show();
    WebApp.MainButton.onClick(checkStatus);
    
    return () => {
      WebApp.MainButton.offClick(checkStatus);
    };
  }, [checkStatus]);

  const handleUserbotAction = async (action) => {
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
      WebApp.showAlert(`Error: ${error.message}`);
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

// Placeholder components for other sections
function AuthSection({ navigateTo }) {
  return (
    <div className="section">
      <h2>Authentication</h2>
      <p>Enter your Telegram API credentials and phone number to begin authentication.</p>
      <div className="form-group">
        <label>Phone Number</label>
        <input type="tel" placeholder="+1234567890" />
      </div>
      <div className="button-group">
        <button onClick={() => WebApp.showAlert('Send code functionality would be implemented here')}>Send Code</button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}

function GroupsSection({ navigateTo }) {
  return (
    <div className="section">
      <h2>Group Management</h2>
      <p>Manage your Telegram groups for automatic posting.</p>
      <div className="form-group">
        <label>Group Identifier</label>
        <input type="text" placeholder="t.me/groupname or @groupname or -100xxxxxxxxxx" />
      </div>
      <div className="button-group">
        <button onClick={() => WebApp.showAlert('Add group functionality would be implemented here')}>Add Group</button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}

function MessagesSection({ navigateTo }) {
  return (
    <div className="section">
      <h2>Message Management</h2>
      <p>Create and manage your automatic messages.</p>
      <div className="form-group">
        <label>Message Text</label>
        <textarea placeholder="Enter your message template"></textarea>
      </div>
      <div className="button-group">
        <button onClick={() => WebApp.showAlert('Add message functionality would be implemented here')}>Add Message</button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}

function ConfigSection({ navigateTo }) {
  return (
    <div className="section">
      <h2>Configuration</h2>
      <p>Configure automatic posting settings and intervals.</p>
      <div className="form-group">
        <label>Message Interval (seconds)</label>
        <input type="number" defaultValue="5-10" />
      </div>
      <div className="form-group">
        <label>Cycle Interval (hours)</label>
        <input type="number" defaultValue="1.1-1.3" />
      </div>
      <div className="button-group">
        <button onClick={() => WebApp.showAlert('Save configuration functionality would be implemented here')}>Save Settings</button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}

function BlacklistSection({ navigateTo }) {
  return (
    <div className="section">
      <h2>Blacklist Management</h2>
      <p>View and manage blacklisted chats.</p>
      <div className="blacklist-info">
        <p>No blacklisted chats at the moment.</p>
      </div>
      <div className="button-group">
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}

export default App;