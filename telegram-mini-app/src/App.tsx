import { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import './App.css';
import { UserbotStatus } from './types';
import DashboardSection from './components/DashboardSection';
import AuthSection from './components/AuthSection';
import GroupsSection from './components/GroupsSection';
import MessagesSection from './components/MessagesSection';
import ConfigSection from './components/ConfigSection';
import BlacklistSection from './components/BlacklistSection';

// Type definitions for state
type ActiveSection = 'dashboard' | 'auth' | 'groups' | 'messages' | 'config' | 'blacklist';

function App() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...');
  const [userbotStatus, setUserbotStatus] = useState<string>('Unknown');
  const [activeSection, setActiveSection] = useState<ActiveSection>('dashboard');

  // Initialize Telegram Web App
  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
    
    // Set theme
    document.documentElement.className = WebApp.colorScheme;
    
    // Check status
    checkStatus();
  }, []);

  const checkStatus = async (): Promise<void> => {
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
        const data: UserbotStatus = await userbotResponse.json();
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
  const navigateTo = (section: ActiveSection): void => {
    setActiveSection(section);
    WebApp.MainButton.hide();
  };

  // Render different sections based on activeSection
  const renderSection = (): JSX.Element => {
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

export default App;