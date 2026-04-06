import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAllRuns } from '../api';
import './AdminUserDetail.css';

function AdminUserDetail() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [userRuns, setUserRuns] = useState([]);
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('date'); // date, score, loops

  useEffect(() => {
    loadUserRuns();
  }, [userId]);

  const loadUserRuns = async () => {
    try {
      setLoading(true);
      const allRuns = await getAllRuns();
      
      // Filter runs for this specific user
      const filtered = allRuns.filter(run => run.user_id === userId);
      
      if (filtered.length > 0) {
        setUserInfo({
          username: filtered[0].username,
          user_id: userId,
          total_runs: filtered.length,
          avg_score: (filtered.reduce((sum, r) => sum + (r.predicted_score || 0), 0) / filtered.length).toFixed(3),
          total_loops: filtered.reduce((sum, r) => sum + (r.features?.loops || 0), 0),
          avg_latency: (filtered.reduce((sum, r) => sum + (r.features?.latency || 0), 0) / filtered.length).toFixed(2)
        });
      }
      
      setUserRuns(filtered);
    } catch (error) {
      console.error('Failed to load user runs:', error);
    } finally {
      setLoading(false);
    }
  };

  const sortedRuns = [...userRuns].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(b.created_at) - new Date(a.created_at);
      case 'score':
        return (b.predicted_score || 0) - (a.predicted_score || 0);
      case 'loops':
        return (b.features?.loops || 0) - (a.features?.loops || 0);
      default:
        return 0;
    }
  });

  const handlePromptClick = (runId) => {
    navigate(`/admin/user/${userId}/prompt/${runId}`);
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return 'excellent';
    if (score >= 0.6) return 'good';
    if (score >= 0.4) return 'average';
    return 'poor';
  };

  return (
    <div className="admin-user-detail">
      {/* Header with Back Button */}
      <div className="detail-header">
        <button className="back-button" onClick={() => navigate('/admin-dashboard')}>
          ← Back to Admin Dashboard
        </button>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading user data...</p>
        </div>
      ) : !userInfo ? (
        <div className="empty-state">
          <div className="empty-icon">❌</div>
          <p>User not found</p>
        </div>
      ) : (
        <>
          {/* User Info Card */}
          <div className="user-info-card">
            <div className="user-header">
              <div className="user-avatar-large">
                {userInfo.username.charAt(0).toUpperCase()}
              </div>
              <div className="user-details">
                <h1>{userInfo.username}</h1>
                <p className="user-id">User ID: {userInfo.user_id}</p>
              </div>
            </div>
            
            <div className="user-stats-grid">
              <div className="stat-box">
                <div className="stat-icon">📝</div>
                <div className="stat-content">
                  <div className="stat-value">{userInfo.total_runs}</div>
                  <div className="stat-label">Total Prompts</div>
                </div>
              </div>
              
              <div className="stat-box">
                <div className="stat-icon">⭐</div>
                <div className="stat-content">
                  <div className="stat-value">{userInfo.avg_score}</div>
                  <div className="stat-label">Avg MAS Score</div>
                </div>
              </div>
              
              <div className="stat-box">
                <div className="stat-icon">🔄</div>
                <div className="stat-content">
                  <div className="stat-value">{userInfo.total_loops}</div>
                  <div className="stat-label">Total Loops</div>
                </div>
              </div>
              
              <div className="stat-box">
                <div className="stat-icon">⚡</div>
                <div className="stat-content">
                  <div className="stat-value">{userInfo.avg_latency}s</div>
                  <div className="stat-label">Avg Latency</div>
                </div>
              </div>
            </div>
          </div>

          {/* Prompts List */}
          <div className="prompts-section">
            <div className="section-header">
              <h2>📋 Prompt History ({userRuns.length})</h2>
              <div className="sort-controls">
                <label>Sort by:</label>
                <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                  <option value="date">Date (Newest)</option>
                  <option value="score">Score (Highest)</option>
                  <option value="loops">Loops (Most)</option>
                </select>
              </div>
            </div>

            {sortedRuns.length === 0 ? (
              <div className="empty-state">
                <p>No prompts found for this user</p>
              </div>
            ) : (
              <div className="prompts-table-container">
                <table className="prompts-table">
                  <thead>
                    <tr>
                      <th>Prompt Text</th>
                      <th>Date / Time</th>
                      <th>Initial Score</th>
                      <th>Final Score</th>
                      <th>Loops</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortedRuns.map((run) => (
                      <tr 
                        key={run._id} 
                        className="prompt-row"
                        onClick={() => handlePromptClick(run._id)}
                      >
                        <td className="prompt-text">
                          <div className="task-preview">
                            {run.task.length > 80 
                              ? run.task.substring(0, 80) + '...'
                              : run.task
                            }
                          </div>
                        </td>
                        <td className="date-cell">
                          <div className="date-display">
                            {new Date(run.created_at).toLocaleDateString()}
                          </div>
                          <div className="time-display">
                            {new Date(run.created_at).toLocaleTimeString()}
                          </div>
                        </td>
                        <td>
                          <span className={`score-badge ${getScoreColor(run.features?.personal_score || 0)}`}>
                            {(run.features?.personal_score || 0).toFixed(3)}
                          </span>
                        </td>
                        <td>
                          <span className={`score-badge ${getScoreColor(run.predicted_score || 0)}`}>
                            {(run.predicted_score || 0).toFixed(3)}
                          </span>
                        </td>
                        <td>
                          <span className="loops-badge">
                            {run.features?.loops || 0}
                          </span>
                        </td>
                        <td>
                          <button 
                            className="view-btn"
                            onClick={(e) => {
                              e.stopPropagation();
                              handlePromptClick(run._id);
                            }}
                          >
                            View →
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default AdminUserDetail;
