import React, { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

export default function Auth() {
  const router = useRouter();
  const [step, setStep] = useState<'setup' | 'code' | 'password' | 'success'>('setup');
  const [apiId, setApiId] = useState<string>('');
  const [apiHash, setApiHash] = useState<string>('');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [phoneCodeHash, setPhoneCodeHash] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSetupSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // In a real implementation, you would save these to the backend
      // For now, we'll just proceed to the next step
      const response = await fetch('/api/v1/auth/send-code', {
        method: 'POST',
      });

      if (response.ok) {
        const data = await response.json();
        setPhoneCodeHash(data.phone_code_hash);
        setStep('code');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to send code');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleCodeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/v1/auth/sign-in', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          phone_code_hash: phoneCodeHash,
        }),
      });

      if (response.ok) {
        setStep('success');
      } else {
        const errorData = await response.json();
        if (errorData.detail && errorData.detail.includes('SessionPasswordNeeded')) {
          setStep('password');
        } else {
          setError(errorData.detail || 'Failed to sign in');
        }
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/v1/auth/sign-in-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (response.ok) {
        setStep('success');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to sign in with password');
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
        <title>Authentication - Telegram Userbot TMA</title>
        <meta name="description" content="Authenticate your Telegram account" />
      </Head>

      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Telegram Authentication
          </h1>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="mb-6">
            <div className="flex justify-between">
              <div className={`flex-1 text-center pb-2 ${step === 'setup' ? 'border-b-2 border-blue-500' : 'border-b border-gray-200 dark:border-gray-700'}`}>
                <span className={step === 'setup' ? 'text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-500 dark:text-gray-400'}>Setup</span>
              </div>
              <div className={`flex-1 text-center pb-2 ${step === 'code' ? 'border-b-2 border-blue-500' : 'border-b border-gray-200 dark:border-gray-700'}`}>
                <span className={step === 'code' ? 'text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-500 dark:text-gray-400'}>Code</span>
              </div>
              <div className={`flex-1 text-center pb-2 ${step === 'password' ? 'border-b-2 border-blue-500' : 'border-b border-gray-200 dark:border-gray-700'}`}>
                <span className={step === 'password' ? 'text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-500 dark:text-gray-400'}>Password</span>
              </div>
              <div className={`flex-1 text-center pb-2 ${step === 'success' ? 'border-b-2 border-blue-500' : 'border-b border-gray-200 dark:border-gray-700'}`}>
                <span className={step === 'success' ? 'text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-500 dark:text-gray-400'}>Success</span>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-red-700 dark:text-red-300">{error}</p>
            </div>
          )}

          {step === 'setup' && (
            <form onSubmit={handleSetupSubmit}>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
                Telegram API Credentials
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Enter your Telegram API credentials and phone number to begin authentication.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="apiId" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    API ID
                  </label>
                  <input
                    type="text"
                    id="apiId"
                    value={apiId}
                    onChange={(e) => setApiId(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="apiHash" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    API Hash
                  </label>
                  <input
                    type="text"
                    id="apiHash"
                    value={apiHash}
                    onChange={(e) => setApiHash(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phoneNumber"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="+1234567890"
                    required
                  />
                </div>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Sending...' : 'Send Code'}
                </button>
              </div>
            </form>
          )}

          {step === 'code' && (
            <form onSubmit={handleCodeSubmit}>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
                Enter Verification Code
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                We've sent a code to your Telegram app. Please enter it below.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="code" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Verification Code
                  </label>
                  <input
                    type="text"
                    id="code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    placeholder="12345"
                    required
                  />
                </div>
              </div>
              
              <div className="mt-6 flex justify-between">
                <button
                  type="button"
                  onClick={() => setStep('setup')}
                  className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Verifying...' : 'Verify'}
                </button>
              </div>
            </form>
          )}

          {step === 'password' && (
            <form onSubmit={handlePasswordSubmit}>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
                Enter Password
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Your account has two-factor authentication enabled. Please enter your password.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    required
                  />
                </div>
              </div>
              
              <div className="mt-6 flex justify-between">
                <button
                  type="button"
                  onClick={() => setStep('code')}
                  className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition duration-200"
                >
                  {loading ? 'Authenticating...' : 'Authenticate'}
                </button>
              </div>
            </form>
          )}

          {step === 'success' && (
            <div className="text-center py-8">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 dark:bg-green-900/30">
                <svg className="h-6 w-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mt-4">
                Authentication Successful!
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mt-2">
                Your Telegram account has been successfully authenticated.
              </p>
              <div className="mt-6">
                <button
                  onClick={() => router.push('/')}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
                >
                  Continue to Dashboard
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}