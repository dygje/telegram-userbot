import { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { Config } from '../types';
import { ActiveSection } from '../types';

interface ConfigSectionProps {
  navigateTo: (section: ActiveSection) => void;
}

export default function ConfigSection({ navigateTo }: ConfigSectionProps) {
  const [messageInterval, setMessageInterval] = useState<string>('5-10');
  const [cycleInterval, setCycleInterval] = useState<string>('4200-4680');
  const [loading, setLoading] = useState<boolean>(false);

  const fetchConfig = async (): Promise<void> => {
    try {
      const response = await fetch('/api/v1/config');
      if (response.ok) {
        const data = await response.json();
        const messageIntervalConfig = data.config.find((c: Config) => c.key === 'message_interval');
        const cycleIntervalConfig = data.config.find((c: Config) => c.key === 'cycle_interval');
        
        if (messageIntervalConfig) {
          setMessageInterval(messageIntervalConfig.value);
        }
        if (cycleIntervalConfig) {
          setCycleInterval(cycleIntervalConfig.value);
        }
      }
    } catch (error) {
      console.error('Error fetching config:', error);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  const handleSaveConfig = async (): Promise<void> => {
    setLoading(true);
    try {
      // Save message interval
      const messageResponse = await fetch('/api/v1/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          key: 'message_interval', 
          value: messageInterval 
        })
      });

      // Save cycle interval
      const cycleResponse = await fetch('/api/v1/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          key: 'cycle_interval', 
          value: cycleInterval 
        })
      });

      if (messageResponse.ok && cycleResponse.ok) {
        WebApp.showAlert('Configuration saved successfully');
      } else {
        WebApp.showAlert('Failed to save configuration');
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section">
      <h2>Configuration</h2>
      <p>Configure automatic posting settings and intervals.</p>
      
      <div className="form-group">
        <label>Message Interval (seconds)</label>
        <input 
          type="text" 
          value={messageInterval}
          onChange={(e) => setMessageInterval(e.target.value)}
          disabled={loading}
        />
        <small>Format: min-max (e.g., 5-10 for 5-10 seconds between messages)</small>
      </div>
      
      <div className="form-group">
        <label>Cycle Interval (seconds)</label>
        <input 
          type="text" 
          value={cycleInterval}
          onChange={(e) => setCycleInterval(e.target.value)}
          disabled={loading}
        />
        <small>Format: min-max (e.g., 4200-4680 for 1.1-1.3 hours between cycles)</small>
      </div>
      
      <div className="button-group">
        <button onClick={handleSaveConfig} disabled={loading}>
          {loading ? 'Saving...' : 'Save Settings'}
        </button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
    </div>
  );
}