import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface BlacklistedChat {
  id: number;
  chat_id: string;
  reason: string;
  is_permanent: boolean;
  expiry_time: string | null;
}

export default function Blacklist() {
  const router = useRouter();
  const [blacklistedChats, setBlacklistedChats] = useState<BlacklistedChat[]>([]);
  const [newChatId, setNewChatId] = useState<string>('');
  const [newReason, setNewReason] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  useEffect(() => {
    fetchBlacklistedChats();
  }, []);

  const fetchBlacklistedChats = async () => {
    try {
      const response = await fetch('/api/v1/blacklist');
      if (response.ok) {
        const data = await response.json();
        setBlacklistedChats(data.blacklisted_chats);
      } else {
        setError('Failed to fetch blacklisted chats');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToBlacklist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newChatId.trim() || !newReason.trim()) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/v1/blacklist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chat_id: newChatId.trim(),
          reason: newReason.trim(),
        }),
      });

      if (response.ok) {
        setSuccess('Chat added to blacklist successfully');
        setNewChatId('');
        setNewReason('');
        fetchBlacklistedChats();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add chat to blacklist');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFromBlacklist = async (chatId: string) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`/api/v1/blacklist/${encodeURIComponent(chatId)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSuccess('Chat removed from blacklist successfully');
        fetchBlacklistedChats();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to remove chat from blacklist');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const formatExpiryTime = (expiryTime: string | null) => {
    if (!expiryTime) return 'Permanent';
    
    const date = new Date(expiryTime);
    return date.toLocaleString();
  };

  const isExpired = (expiryTime: string | null) => {
    if (!expiryTime) return false;
    
    const now = new Date();
    const expiry = new Date(expiryTime);
    return expiry < now;
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Head>
        <title>Blacklist Management - Telegram Userbot TMA</title>
        <meta name="description" content="Manage blacklisted Telegram chats" />
      </Head>

      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Blacklist Management
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
          {/* Add to Blacklist */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Add to Blacklist
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Manually add a Telegram chat to the blacklist.
            </p>
            
            <form onSubmit={handleAddToBlacklist}>
              <div className="space-y-4">
                <div>
                  <label htmlFor="chatId" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Chat ID
                  </label>
                  <input
                    type="text"
                    id="chatId"
                    value={newChatId}
                    onChange={(e) => setNewChatId(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="e.g., -1001234567890"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="reason" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Reason
                  </label>
                  <input
                    type="text"
                    id="reason"
                    value={newReason}
                    onChange={(e) => setNewReason(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="e.g., Spam, Violation of terms"
                    required
                  />
                </div>
              </div>
              
              <div className="mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Adding...' : 'Add to Blacklist'}
                </button>
              </div>
            </form>
          </div>

          {/* Blacklist Guidelines */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Blacklist Guidelines
            </h2>
            <div className="prose prose-blue dark:prose-invert">
              <ul className="space-y-2">
                <li>Permanent blacklist for serious violations</li>
                <li>Temporary blacklist for rate limiting issues</li>
                <li>Automatic blacklist for Telegram errors:
                  <ul className="ml-4 mt-1 space-y-1">
                    <li>ChatForbidden</li>
                    <li>ChatIdInvalid</li>
                    <li>UserBlocked</li>
                    <li>PeerIdInvalid</li>
                    <li>ChannelInvalid</li>
                    <li>UserBannedInChannel</li>
                    <li>ChatWriteForbidden</li>
                    <li>ChatRestricted</li>
                  </ul>
                </li>
                <li>Temporary blacklists are automatically cleaned</li>
                <li>Manual entries require admin review</li>
              </ul>
            </div>
            
            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <h3 className="font-medium text-blue-800 dark:text-blue-200">Note</h3>
              <p className="mt-1 text-sm text-blue-700 dark:text-blue-300">
                Temporary blacklists expire automatically. Permanent blacklists require manual removal.
              </p>
            </div>
          </div>
        </div>

        {/* Blacklisted Chats List */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
            Blacklisted Chats
          </h2>
          
          {loading && blacklistedChats.length === 0 ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : blacklistedChats.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">
                No chats are currently blacklisted.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Chat ID
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Reason
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Type
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Expiry
                    </th>
                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {blacklistedChats.map((chat) => (
                    <tr 
                      key={chat.id} 
                      className={isExpired(chat.expiry_time) ? 'bg-red-50 dark:bg-red-900/20' : ''}
                    >
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {chat.chat_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {chat.reason}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {chat.is_permanent ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                            Permanent
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300">
                            Temporary
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatExpiryTime(chat.expiry_time)}
                        {isExpired(chat.expiry_time) && (
                          <span className="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                            Expired
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleRemoveFromBlacklist(chat.chat_id)}
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