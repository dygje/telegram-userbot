import { useState, useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { Group } from '../types';
import { ActiveSection } from '../types';

interface GroupsSectionProps {
  navigateTo: (section: ActiveSection) => void;
}

export default function GroupsSection({ navigateTo }: GroupsSectionProps) {
  const [groupIdentifier, setGroupIdentifier] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [groups, setGroups] = useState<Group[]>([]);

  const fetchGroups = async (): Promise<void> => {
    try {
      const response = await fetch('/api/v1/groups');
      if (response.ok) {
        const data = await response.json();
        setGroups(data.groups);
      }
    } catch (error) {
      console.error('Error fetching groups:', error);
    }
  };

  useEffect(() => {
    fetchGroups();
  }, []);

  const handleAddGroup = async (): Promise<void> => {
    if (!groupIdentifier) {
      WebApp.showAlert('Please enter a group identifier');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/groups', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifier: groupIdentifier })
      });

      if (response.ok) {
        WebApp.showAlert('Group added successfully');
        setGroupIdentifier('');
        fetchGroups(); // Refresh the list
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to add group'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveGroup = async (identifier: string): Promise<void> => {
    try {
      const response = await fetch(`/api/v1/groups/${identifier}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        WebApp.showAlert('Group removed successfully');
        fetchGroups(); // Refresh the list
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to remove group'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    }
  };

  return (
    <div className="section">
      <h2>Group Management</h2>
      <p>Manage your Telegram groups for automatic posting.</p>
      
      <div className="form-group">
        <label>Group Identifier</label>
        <input 
          type="text" 
          placeholder="t.me/groupname or @groupname or -100xxxxxxxxxx" 
          value={groupIdentifier}
          onChange={(e) => setGroupIdentifier(e.target.value)}
          disabled={loading}
        />
      </div>
      <div className="button-group">
        <button onClick={handleAddGroup} disabled={loading}>
          {loading ? 'Adding...' : 'Add Group'}
        </button>
        <button onClick={() => navigateTo('dashboard')}>Back</button>
      </div>
      
      {groups.length > 0 && (
        <div className="list-section">
          <h3>Managed Groups</h3>
          <ul className="item-list">
            {groups.map((group: Group) => (
              <li key={group.id} className="list-item">
                <div className="item-info">
                  <span className="item-name">{group.name}</span>
                  <span className="item-identifier">{group.identifier}</span>
                </div>
                <button 
                  className="remove-btn" 
                  onClick={() => handleRemoveGroup(group.identifier)}
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