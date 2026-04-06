import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import './AdminAnalytics.css';

const AdminAnalytics = () => {
  const [allRuns, setAllRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    dateRange: 'all', // all, today, week, month
    minScore: 0,
    maxScore: 1,
    autoEnhancedOnly: false
  });

  const navigate = useNavigate();

  useEffect(() => {
    fetchAllRuns();
  }, []);

  const fetchAllRuns = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:8080/admin/all_runs');
      
      if (!response.ok) {
        throw new Error(`Failed to fetch runs: ${response.status}`);
      }

      const data = await response.json();
      setAllRuns(data.runs || []);
    } catch (err) {
      console.error('Error fetching runs:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...allRuns];

    // Date range filter
    if (filters.dateRange !== 'all') {
      const now = new Date();
      const cutoff = new Date();

      if (filters.dateRange === 'today') {
        cutoff.setHours(0, 0, 0, 0);
      } else if (filters.dateRange === 'week') {
        cutoff.setDate(now.getDate() - 7);
      } else if (filters.dateRange === 'month') {
        cutoff.setMonth(now.getMonth() - 1);
      }

      filtered = filtered.filter(run => {
        const runDate = new Date(run.timestamp);
        return runDate >= cutoff;
      });
    }

    // Score range filter
    filtered = filtered.filter(run => {
      const score = run.predicted_score || 0;
      return score >= filters.minScore && score <= filters.maxScore;
    });

    // Auto-enhanced filter
    if (filters.autoEnhancedOnly) {
      filtered = filtered.filter(run => run.monitor_data?.auto_enhanced);
    }

    return filtered;
  };

  const filteredRuns = applyFilters();

  if (loading) {
    return (
      <div className="admin-analytics-page">
        <div className="analytics-loading">
          <div className="spinner"></div>
          <p>Loading analytics data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-analytics-page">
        <div className="analytics-error">
          <h2>❌ Error Loading Analytics</h2>
          <p>{error}</p>
          <button onClick={fetchAllRuns}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-analytics-page">
      {/* Header */}
      <div className="analytics-page-header">
        <div className="header-left">
          <button className="back-button" onClick={() => navigate('/admin')}>
            ← Back to Admin
          </button>
          <h1>🎯 AgentMonitor Analytics</h1>
        </div>
        <button className="refresh-button" onClick={fetchAllRuns}>
          🔄 Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="analytics-filters">
        <div className="filter-group">
          <label>Date Range:</label>
          <select 
            value={filters.dateRange} 
            onChange={(e) => setFilters({...filters, dateRange: e.target.value})}
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Min Score:</label>
          <input 
            type="number" 
            min="0" 
            max="1" 
            step="0.1"
            value={filters.minScore}
            onChange={(e) => setFilters({...filters, minScore: parseFloat(e.target.value)})}
          />
        </div>

        <div className="filter-group">
          <label>Max Score:</label>
          <input 
            type="number" 
            min="0" 
            max="1" 
            step="0.1"
            value={filters.maxScore}
            onChange={(e) => setFilters({...filters, maxScore: parseFloat(e.target.value)})}
          />
        </div>

        <div className="filter-group checkbox-group">
          <label>
            <input 
              type="checkbox"
              checked={filters.autoEnhancedOnly}
              onChange={(e) => setFilters({...filters, autoEnhancedOnly: e.target.checked})}
            />
            Auto-Enhanced Only
          </label>
        </div>

        <div className="filter-results">
          Showing {filteredRuns.length} of {allRuns.length} runs
        </div>
      </div>

      {/* Main Analytics Dashboard */}
      <AnalyticsDashboard allRuns={filteredRuns} />

      {/* Runs Table */}
      <div className="runs-table-section">
        <h2>📋 All Runs</h2>
        <div className="table-container">
          <table className="runs-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Prompt</th>
                <th>Initial Score</th>
                <th>Final Score</th>
                <th>Auto-Enhanced</th>
                <th>Agents</th>
                <th>Timestamp</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredRuns.map((run, index) => (
                <tr key={run._id || index}>
                  <td className="mono">{(run._id || '').substring(0, 8)}...</td>
                  <td>{run.user_id || 'Unknown'}</td>
                  <td className="prompt-cell" title={run.prompt}>
                    {run.prompt?.substring(0, 50) || 'N/A'}...
                  </td>
                  <td className={`score-cell ${getScoreClass(run.initial_score)}`}>
                    {(run.initial_score || 0).toFixed(3)}
                  </td>
                  <td className={`score-cell ${getScoreClass(run.predicted_score)}`}>
                    {(run.predicted_score || 0).toFixed(3)}
                  </td>
                  <td>
                    {run.monitor_data?.auto_enhanced ? (
                      <span className="badge badge-success">✓ Yes</span>
                    ) : (
                      <span className="badge badge-neutral">No</span>
                    )}
                  </td>
                  <td className="mono">
                    {run.monitor_data?.agent_stats ? Object.keys(run.monitor_data.agent_stats).length : 0}
                  </td>
                  <td className="mono">
                    {new Date(run.timestamp).toLocaleString()}
                  </td>
                  <td>
                    <button 
                      className="view-button"
                      onClick={() => navigate(`/admin/prompt/${run._id}`)}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const getScoreClass = (score) => {
  if (!score) return 'score-poor';
  if (score >= 0.8) return 'score-excellent';
  if (score >= 0.6) return 'score-good';
  if (score >= 0.4) return 'score-fair';
  return 'score-poor';
};

export default AdminAnalytics;
