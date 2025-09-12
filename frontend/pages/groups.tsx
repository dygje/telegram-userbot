import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface Group {
  id: number;
  identifier: string;
  name: string;
}

export default function Groups() {
  const router = useRouter();
  const [groups, setGroups] = useState<Group[]>([]);
  const [newGroup, setNewGroup] = useState<string>('');
  const [bulkGroups, setBulkGroups] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await fetch('/api/v1/groups');
      if (response.ok) {
        const data = await response.json();
        setGroups(data.groups);
      } else {
        setError('Failed to fetch groups');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAddGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newGroup.trim()) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/v1/groups', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifier: newGroup.trim() }),
      });

      if (response.ok) {
        setSuccess('Group added successfully');
        setNewGroup('');
        fetchGroups();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add group');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAddBulkGroups = async (e: React.FormEvent) => {
    e.preventDefault();
    const identifiers = bulkGroups
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);

    if (identifiers.length === 0) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/v1/groups/bulk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifiers }),
      });

      if (response.ok) {
        setSuccess(`Added ${identifiers.length} groups successfully`);
        setBulkGroups('');
        fetchGroups();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add groups');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveGroup = async (identifier: string) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`/api/v1/groups/${encodeURIComponent(identifier)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSuccess('Group removed successfully');
        fetchGroups();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to remove group');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Head>
        <title>Group Management - Telegram Userbot TMA</title>
        <meta name="description" content="Manage Telegram groups for automatic posting" />
      </Head>

      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Group Management
          </h1>
          <button
            onClick={() => router.push('/')}
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-200"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-700 dark:text-red-300">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <p className="text-green-700 dark:text-green-300">{success}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Add Single Group */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Add Group
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Add a single Telegram group to the managed list.
            </p>
            
            <form onSubmit={handleAddGroup}>
              <div className="space-y-4">
                <div>
                  <label htmlFor="groupIdentifier" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Group Identifier
                  </label>
                  <input
                    type="text"
                    id="groupIdentifier"
                    value={newGroup}
                    onChange={(e) => setNewGroup(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="e.g., @groupname, t.me/groupname, or -100xxxxxxxxxx"
                    required
                  />
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Supported formats: @username, t.me/link, or group ID
                  </p>
                </div>
              </div>
              
              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Adding...' : 'Add Group'}
                </button>
              </div>
            </form>
          </div>

          {/* Add Bulk Groups */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Add Groups in Bulk
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Add multiple Telegram groups at once (one per line).
            </p>
            
            <form onSubmit={handleAddBulkGroups}>
              <div className="space-y-4">
                <div>
                  <label htmlFor="bulkGroups" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Group Identifiers
                  </label>
                  <textarea
                    id="bulkGroups"
                    value={bulkGroups}
                    onChange={(e) => setBulkGroups(e.target.value)}
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="@group1
t.me/group2
-1001234567890"
                  />
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Enter one group identifier per line
                  </p>
                </div>
              </div>
              
              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Adding...' : 'Add Groups'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Managed Groups List */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
            Managed Groups
          </h2>
          
          {loading && groups.length === 0 ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : groups.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">
                No groups have been added yet.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Group Identifier
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Name
                    </th>
                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {groups.map((group) => (
                    <tr key={group.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {group.identifier}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {group.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleRemoveGroup(group.identifier)}
                          disabled={loading}
                          className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300 disabled:opacity-50"
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}