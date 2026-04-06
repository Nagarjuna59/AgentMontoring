import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AnalyticsGraphDashboard from '../components/AnalyticsGraphDashboard';
import { getGraphMetrics } from '../api';
import './AnalyticsPage.css';

function AnalyticsPage({ user, onLogout }) {
  const { runId } = useParams();
  const [metrics, setMetrics] = useState(null);
  const [agentStats, setAgentStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadGraphMetrics();
  }, [runId]);

  const loadGraphMetrics = async () => {
    try {
      setLoading(true);
      if (runId) {
        const data = await getGraphMetrics(runId);
        setMetrics(data.metrics);
        setAgentStats(data.agent_stats);
      }
    } catch (err) {
      setError(err.message || 'Failed to load metrics');
      console.error('Error loading graph metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="analytics-page-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading analytics dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-page-container">
        <div className="error-message">
          <p>❌ Error: {error}</p>
          <button onClick={loadGraphMetrics} className="retry-btn">Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-page-container">
      <div className="page-header">
        <button onClick={onLogout} className="logout-btn">Logout</button>
      </div>
      <AnalyticsGraphDashboard metrics={metrics} agentStats={agentStats} />
    </div>
  );
}

export default AnalyticsPage;
