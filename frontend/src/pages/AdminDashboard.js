import React, { useState, useEffect } from 'react';
import { getAllRuns, exportCSV } from '../api';
import { useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

function AdminDashboard({ user, onLogout }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadUserStats();
  }, []);

  const loadUserStats = async () => {
    try {
      setLoading(true);
      const runs = await getAllRuns();
      
      // Group runs by user
      const userMap = {};
      runs.forEach(run => {
        const userId = run.user_id || 'unknown';
        if (!userMap[userId]) {
          userMap[userId] = {
            user_id: userId,
            username: run.username || 'Unknown User',
            total_prompts: 0,
            scores: [],
            last_active: null
          };
        }
        
        userMap[userId].total_prompts += 1;
        if (run.predicted_score) {
          userMap[userId].scores.push(run.predicted_score);
        }
        
        const runDate = new Date(run.created_at);
        if (!userMap[userId].last_active || runDate > new Date(userMap[userId].last_active)) {
          userMap[userId].last_active = run.created_at;
        }
      });
      
      // Calculate average scores
      const userList = Object.values(userMap).map(u => ({
        ...u,
        avg_score: u.scores.length > 0 
          ? (u.scores.reduce((a, b) => a + b, 0) / u.scores.length).toFixed(3)
          : 'N/A'
      }));
      
      setUsers(userList);
    } catch (error) {
      console.error('Failed to load user stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCSV = async () => {
    try {
      setDownloading(true);
      const data = await exportCSV();
      
      // Create blob and download
      const blob = new Blob([data.csv || data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mas_data_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Failed to download CSV:', error);
      alert('Failed to download CSV');
    } finally {
      setDownloading(false);
    }
  };

  const handleUserClick = (userId) => {
    navigate(`/admin/user/${userId}`);
  };

  const getActivityStatus = (lastActive) => {
    if (!lastActive) return 'never';
    const diff = Date.now() - new Date(lastActive).getTime();
    const hours = diff / (1000 * 60 * 60);
    
    if (hours < 1) return 'active';
    if (hours < 24) return 'recent';
    if (hours < 168) return 'week';
    return 'old';
  };

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <header className="admin-header">
        <div className="header-content">
          <div className="header-left">
            <h1>🛡️ Admin Dashboard</h1>
            <p className="subtitle">Monitor & analyze all user activities</p>
          </div>
          <div className="header-right">
            <button 
              className="analytics-btn"
              onClick={() => navigate('/admin/analytics')}
            >
              📊 View Analytics
            </button>
            <button 
              className="download-csv-btn"
              onClick={handleDownloadCSV}
              disabled={downloading}
            >
              {downloading ? '⏳ Downloading...' : '📥 Download CSV'}
            </button>
            <span className="admin-username">👤 {user.username}</span>
            <button onClick={onLogout} className="logout-button">Logout</button>
          </div>
        </div>
      </header>

      {/* Stats Overview */}
      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{users.length}</div>
            <div className="stat-label">Total Users</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <div className="stat-value">
              {users.reduce((sum, u) => sum + u.total_prompts, 0)}
            </div>
            <div className="stat-label">Total Prompts</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">
              {users.length > 0 
                ? (users.reduce((sum, u) => sum + (parseFloat(u.avg_score) || 0), 0) / users.length).toFixed(3)
                : 'N/A'
              }
            </div>
            <div className="stat-label">Global Avg Score</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <div className="stat-value">
              {users.filter(u => getActivityStatus(u.last_active) === 'active').length}
            </div>
            <div className="stat-label">Active Now</div>
          </div>
        </div>
      </div>

      {/* User Cards */}
      <div className="users-section">
        <h2>👥 User Activity</h2>
        
        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading user data...</p>
          </div>
        ) : users.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <p>No users found</p>
          </div>
        ) : (
          <div className="user-cards-grid">
            {users.map((u, idx) => (
              <div 
                key={idx}
                className={`user-card ${getActivityStatus(u.last_active)}`}
                onClick={() => handleUserClick(u.user_id)}
              >
                <div className="user-card-header">
                  <div className="user-avatar">
                    {u.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="user-info">
                    <h3>{u.username}</h3>
                    <p className="user-id">ID: {u.user_id}</p>
                  </div>
                  <div className={`status-indicator ${getActivityStatus(u.last_active)}`}>
                    {getActivityStatus(u.last_active) === 'active' && '🟢'}
                    {getActivityStatus(u.last_active) === 'recent' && '🟡'}
                    {getActivityStatus(u.last_active) === 'week' && '🟠'}
                    {getActivityStatus(u.last_active) === 'old' && '⚪'}
                  </div>
                </div>
                
                <div className="user-card-stats">
                  <div className="stat-item">
                    <span className="stat-label">📝 Prompts</span>
                    <span className="stat-value">{u.total_prompts}</span>
                  </div>
                  
                  <div className="stat-item">
                    <span className="stat-label">⭐ Avg Score</span>
                    <span className="stat-value score">{u.avg_score}</span>
                  </div>
                  
                  <div className="stat-item full-width">
                    <span className="stat-label">🕒 Last Active</span>
                    <span className="stat-value">
                      {u.last_active 
                        ? new Date(u.last_active).toLocaleString()
                        : 'Never'
                      }
                    </span>
                  </div>
                </div>
                
                <div className="user-card-footer">
                  <button className="view-details-btn">
                    View Details →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
