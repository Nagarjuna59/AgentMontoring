import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-content">
        <h1>AgentMonitor</h1>
        <p className="subtitle">Multi-Agent System Performance Monitoring</p>
        <p className="description">
          Monitor and analyze code generation performance using advanced multi-agent systems.
          Track 16 key features including token usage, API calls, iteration counts, and complexity metrics.
        </p>
        <div className="features">
          <div className="feature-card">
            <h3>🤖 Multi-Agent System</h3>
            <p>Powered by Gemini API with specialized agents for code generation</p>
          </div>
          <div className="feature-card">
            <h3>📊 Performance Tracking</h3>
            <p>Real-time monitoring of 16 critical performance features</p>
          </div>
          <div className="feature-card">
            <h3>🎯 XGBoost Prediction</h3>
            <p>Trained on 148 samples for accurate performance scoring</p>
          </div>
        </div>
        <button className="cta-button" onClick={() => navigate('/login')}>
          Get Started
        </button>
      </div>
    </div>
  );
}

export default Home;
