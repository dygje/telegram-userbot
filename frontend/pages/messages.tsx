import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface Message {
  id: number;
  text: string;
}

export default function Messages() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState<string>('');
  const [editingMessage, setEditingMessage] = useState<Message | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch('/api/v1/messages');
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages);
      } else {
        setError('Failed to fetch messages');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAddMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('/api/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: newMessage.trim() }),
      });

      if (response.ok) {
        setSuccess('Message added successfully');
        setNewMessage('');
        fetchMessages();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add message');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingMessage || !editingMessage.text.trim()) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // For updating, we would need a PUT endpoint
      // For now, we'll remove the old message and add a new one
      const deleteResponse = await fetch(`/api/v1/messages/${editingMessage.id}`, {
        method: 'DELETE',
      });

      if (deleteResponse.ok) {
        const addResponse = await fetch('/api/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: editingMessage.text.trim() }),
        });

        if (addResponse.ok) {
          setSuccess('Message updated successfully');
          setEditingMessage(null);
          fetchMessages();
        } else {
          const errorData = await addResponse.json();
          setError(errorData.detail || 'Failed to update message');
        }
      } else {
        const errorData = await deleteResponse.json();
        setError(errorData.detail || 'Failed to update message');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMessage = async (id: number) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`/api/v1/messages/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSuccess('Message removed successfully');
        fetchMessages();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to remove message');
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
        <title>Message Management - Telegram Userbot TMA</title>
        <meta name="description" content="Manage automatic messages for Telegram groups" />
      </Head>

      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Message Management
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
          {/* Add New Message */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              {editingMessage ? 'Edit Message' : 'Add New Message'}
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              {editingMessage 
                ? 'Edit your automatic message below.' 
                : 'Create a new automatic message for your Telegram groups.'}
            </p>
            
            <form onSubmit={editingMessage ? handleUpdateMessage : handleAddMessage}>
              <div className="space-y-4">
                <div>
                  <label htmlFor="messageText" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Message Text
                  </label>
                  <textarea
                    id="messageText"
                    value={editingMessage ? editingMessage.text : newMessage}
                    onChange={(e) => 
                      editingMessage 
                        ? setEditingMessage({...editingMessage, text: e.target.value}) 
                        : setNewMessage(e.target.value)
                    }
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="Enter your automatic message here..."
                    required
                  />
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Messages will be sent as plain text without media
                  </p>
                </div>
              </div>
              
              <div className="mt-6 flex space-x-3">
                {editingMessage && (
                  <button
                    type="button"
                    onClick={() => setEditingMessage(null)}
                    className="flex-1 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                  >
                    Cancel
                  </button>
                )}
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? (editingMessage ? 'Updating...' : 'Adding...') : (editingMessage ? 'Update Message' : 'Add Message')}
                </button>
              </div>
            </form>
          </div>

          {/* Message Guidelines */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Message Guidelines
            </h2>
            <div className="prose prose-blue dark:prose-invert">
              <ul className="space-y-2">
                <li>Messages are sent as plain text only (no media support)</li>
                <li>Each message will be sent to all managed groups</li>
                <li>Messages are sent with random delays between 5-10 seconds</li>
                <li>Cycles are repeated with random delays between 1.1-1.3 hours</li>
                <li>Messages are stored securely in the database</li>
                <li>Use professional and appropriate language</li>
                <li>Avoid spam-like content that may trigger Telegram restrictions</li>
              </ul>
            </div>
            
            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <h3 className="font-medium text-blue-800 dark:text-blue-200">Tip</h3>
              <p className="mt-1 text-sm text-blue-700 dark:text-blue-300">
                You can create multiple messages to rotate content and avoid repetition.
              </p>
            </div>
          </div>
        </div>

        {/* Managed Messages List */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
            Managed Messages
          </h2>
          
          {loading && messages.length === 0 ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">
                No messages have been added yet.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Message
                    </th>
                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {messages.map((message) => (
                    <tr key={message.id}>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white max-w-md">
                        <div className="truncate" title={message.text}>
                          {message.text}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => setEditingMessage(message)}
                          className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 mr-4"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleRemoveMessage(message.id)}
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