import { useState } from 'react';
import WebApp from '@twa-dev/sdk';
import { ActiveSection } from '../types';

interface AuthSectionProps {
  navigateTo: (section: ActiveSection) => void;
}

export default function AuthSection({ navigateTo }: AuthSectionProps) {
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [phoneCodeHash, setPhoneCodeHash] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [authStep, setAuthStep] = useState<'phone' | 'code' | 'password'>('phone');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSendCode = async (): Promise<void> => {
    if (!phoneNumber) {
      WebApp.showAlert('Please enter your phone number');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/auth/send-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone_number: phoneNumber })
      });

      if (response.ok) {
        const data = await response.json();
        setPhoneCodeHash(data.phone_code_hash);
        setAuthStep('code');
        WebApp.showAlert('Code sent to your phone number');
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to send code'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (): Promise<void> => {
    if (!code || !phoneCodeHash) {
      WebApp.showAlert('Please enter the code you received');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/auth/sign-in', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          phone_code_hash: phoneCodeHash
        })
      });

      if (response.ok) {
        WebApp.showAlert('Authentication successful!');
        setTimeout(() => navigateTo('dashboard'), 1000);
      } else {
        const errorData = await response.json();
        // Check if 2FA is required
        if (errorData.detail && errorData.detail.includes('2FA')) {
          setAuthStep('password');
        } else {
          WebApp.showAlert(`Error: ${errorData.detail || 'Failed to sign in'}`);
        }
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSignInWithPassword = async (): Promise<void> => {
    if (!password) {
      WebApp.showAlert('Please enter your password');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/auth/sign-in-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password })
      });

      if (response.ok) {
        WebApp.showAlert('Authentication with password successful!');
        setTimeout(() => navigateTo('dashboard'), 1000);
      } else {
        const errorData = await response.json();
        WebApp.showAlert(`Error: ${errorData.detail || 'Failed to sign in with password'}`);
      }
    } catch (error) {
      WebApp.showAlert(`Network error: ${(error as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = (): void => {
    if (authStep === 'code') {
      setAuthStep('phone');
    } else if (authStep === 'password') {
      setAuthStep('code');
    } else {
      navigateTo('dashboard');
    }
  };

  return (
    <div className="section">
      <h2>Authentication</h2>
      
      {authStep === 'phone' && (
        <div className="auth-step">
          <p>Enter your phone number to begin authentication.</p>
          <div className="form-group">
            <label>Phone Number</label>
            <input 
              type="tel" 
              placeholder="+1234567890" 
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              disabled={loading}
            />
          </div>
          <div className="button-group">
            <button onClick={handleSendCode} disabled={loading}>
              {loading ? 'Sending...' : 'Send Code'}
            </button>
            <button onClick={handleBack}>Back</button>
          </div>
        </div>
      )}

      {authStep === 'code' && (
        <div className="auth-step">
          <p>Enter the code you received on your phone.</p>
          <div className="form-group">
            <label>Verification Code</label>
            <input 
              type="text" 
              placeholder="12345" 
              value={code}
              onChange={(e) => setCode(e.target.value)}
              disabled={loading}
            />
          </div>
          <div className="button-group">
            <button onClick={handleSignIn} disabled={loading}>
              {loading ? 'Verifying...' : 'Verify Code'}
            </button>
            <button onClick={handleBack}>Back</button>
          </div>
        </div>
      )}

      {authStep === 'password' && (
        <div className="auth-step">
          <p>Two-factor authentication is enabled on your account. Please enter your password.</p>
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              placeholder="Your password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>
          <div className="button-group">
            <button onClick={handleSignInWithPassword} disabled={loading}>
              {loading ? 'Verifying...' : 'Sign In'}
            </button>
            <button onClick={handleBack}>Back</button>
          </div>
        </div>
      )}
    </div>
  );
}