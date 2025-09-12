import React, { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Dashboard() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...');
  const [userbotStatus, setUserbotStatus] = useState<string>('Unknown');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check API status
    const checkApiStatus = async () => {
      try {
        const response = await fetch('/api/v1/health');
        if (response.ok) {
          setApiStatus('Connected');
        } else {
          setApiStatus('Disconnected');
        }
      } catch (error) {
        setApiStatus('Disconnected');
      } finally {
        setIsLoading(false);
      }
    };

    // Check userbot status
    const checkUserbotStatus = async () => {
      try {
        const response = await fetch('/api/v1/userbot/status');
        if (response.ok) {
          const data = await response.json();
          setUserbotStatus(data.running ? 'Running' : 'Stopped');
        } else {
          setUserbotStatus('Unknown');
        }
      } catch (error) {
        setUserbotStatus('Unknown');
      }
    };

    checkApiStatus();
    checkUserbotStatus();

    // Set up interval to check status periodically
    const interval = setInterval(() => {
      checkUserbotStatus();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Head>
        <title>Telegram Userbot TMA</title>
        <meta name="description" content="Telegram Userbot Management Application" />
      </Head>

      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Telegram Userbot TMA
          </h1>
          <div className="flex items-center space-x-4">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              apiStatus === 'Connected' 
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' 
                : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
            }`}>
              API: {apiStatus}
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              userbotStatus === 'Running' 
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' 
                : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
            }`}>
              Userbot: {userbotStatus}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Authentication Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Authentication
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Setup Telegram API credentials and authenticate your account.
            </p>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
              onClick={() => window.location.href = '/auth'}
            >
              Configure
            </button>
          </div>

          {/* Group Management Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Group Management
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Manage your Telegram groups for automatic posting.
            </p>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
              onClick={() => window.location.href = '/groups'}
            >
              Manage Groups
            </button>
          </div>

          {/* Message Management Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Message Management
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Create and manage your automatic messages.
            </p>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
              onClick={() => window.location.href = '/messages'}
            >
              Manage Messages
            </button>
          </div>

          {/* Configuration Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Configuration
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Configure automatic posting settings and intervals.
            </p>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
              onClick={() => window.location.href = '/config'}
            >
              Configure Settings
            </button>
          </div>

          {/* Userbot Control Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Userbot Control
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Start or stop the userbot service.
            </p>
            <div className="flex space-x-2">
              <button 
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                onClick={() => {
                  fetch('/api/v1/userbot/start', { method: 'POST' });
                  setTimeout(() => window.location.reload(), 1000);
                }}
              >
                Start
              </button>
              <button 
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                onClick={() => {
                  fetch('/api/v1/userbot/stop', { method: 'POST' });
                  setTimeout(() => window.location.reload(), 1000);
                }}
              >
                Stop
              </button>
            </div>
          </div>

          {/* Blacklist Management Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Blacklist Management
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              View and manage blacklisted chats.
            </p>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
              onClick={() => window.location.href = '/blacklist'}
            >
              Manage Blacklist
            </button>
          </div>
        </div>

        {/* System Status */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
            System Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-gray-700 dark:text-gray-300">API Status</h3>
              <p className={`text-lg font-semibold ${apiStatus === 'Connected' ? 'text-green-600' : 'text-red-600'}`}>
                {apiStatus}
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-gray-700 dark:text-gray-300">Userbot Status</h3>
              <p className={`text-lg font-semibold ${userbotStatus === 'Running' ? 'text-green-600' : 'text-red-600'}`}>
                {userbotStatus}
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-gray-700 dark:text-gray-300">System Load</h3>
              <p className="text-lg font-semibold text-gray-600 dark:text-gray-400">Normal</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}