import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await login(username, password);
      onLogin(data);
      navigate(data.role === 'admin' ? '/admin-dashboard' : '/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login to AgentMonitor</h2>
        <p className="login-subtitle">Monitor your Multi-Agent System performance</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <p style={{textAlign: 'center', marginTop: '1rem', color: '#666'}}>
          Don't have an account? <span style={{color: '#667eea', cursor: 'pointer'}} onClick={() => navigate('/register')}>Register here</span>
        </p>
        
        <button className="back-button" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Login;
