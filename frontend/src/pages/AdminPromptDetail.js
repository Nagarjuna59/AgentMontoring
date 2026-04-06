import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getRun } from '../api';
import AgentCollaborationGraph from '../components/AgentCollaborationGraph';
import './AdminPromptDetail.css';

function AdminPromptDetail() {
  const { userId, promptId } = useParams();
  const navigate = useNavigate();
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    loadPromptDetail();
  }, [promptId]);

  const loadPromptDetail = async () => {
    try {
      setLoading(true);
      const data = await getRun(promptId);
      setRun(data);
    } catch (error) {
      console.error('Failed to load prompt details:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadJSON = () => {
    if (!run) return;
    
    setDownloading(true);
    const dataStr = JSON.stringify(run, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prompt_${promptId}_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    setDownloading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.6) return '#3b82f6';
    if (score >= 0.4) return '#f59e0b';
    return '#ef4444';
  };

  if (loading) {
    return (
      <div className="admin-prompt-detail">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading prompt details...</p>
        </div>
      </div>
    );
  }

  if (!run) {
    return (
      <div className="admin-prompt-detail">
        <div className="empty-state">
          <div className="empty-icon">❌</div>
          <p>Prompt not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-prompt-detail">
      {/* Header */}
      <div className="detail-header">
        <button 
          className="back-button" 
          onClick={() => navigate(`/admin/user/${userId}`)}
        >
          ← Back to {run.username}'s Prompts
        </button>
        <button 
          className="download-json-btn"
          onClick={handleDownloadJSON}
          disabled={downloading}
        >
          {downloading ? '⏳ Downloading...' : '📥 Download JSON'}
        </button>
      </div>

      {/* Prompt Overview */}
      <div className="prompt-overview">
        <div className="overview-header">
          <h1>🔍 Prompt Details</h1>
          <span className="prompt-id">ID: {run._id}</span>
        </div>
        
        <div className="overview-meta">
          <div className="meta-item">
            <span className="meta-label">👤 User:</span>
            <span className="meta-value">{run.username}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">📅 Date:</span>
            <span className="meta-value">{new Date(run.created_at).toLocaleString()}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">🆔 Run ID:</span>
            <span className="meta-value">{run._id}</span>
          </div>
        </div>
      </div>

      {/* Prompt Text */}
      <div className="section-card">
        <h2>📝 Prompt Text</h2>
        <div className="prompt-text-display">
          {run.task}
        </div>
      </div>

      {/* Code Comparison */}
      <div className="code-comparison">
        <div className="code-panel">
          <div className="code-panel-header">
            <h3>📄 Initial Code</h3>
            <span className="code-status">First Generation</span>
          </div>
          <pre className="code-block">
            {run.initial_code || run.code || 'No initial code available'}
          </pre>
        </div>

        <div className="code-panel">
          <div className="code-panel-header">
            <h3>✨ Enhanced Code</h3>
            <span className="code-status enhanced">After MAS Enhancement</span>
          </div>
          <pre className="code-block enhanced">
            {run.code || 'No enhanced code available'}
          </pre>
        </div>
      </div>

      {/* MAS Indicators */}
      <div className="section-card">
        <h2>📊 MAS Performance Indicators</h2>
        <div className="indicators-grid">
          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">⭐</span>
              <span className="indicator-label">Avg Personal Score</span>
            </div>
            <div className="indicator-value-single" style={{ color: getScoreColor(run.features?.avg_personal_score || 0) }}>
              {(run.features?.avg_personal_score || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">📉</span>
              <span className="indicator-label">Min Personal Score</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.min_personal_score || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🎯</span>
              <span className="indicator-label">Collective Score</span>
            </div>
            <div className="indicator-value-single" style={{ color: getScoreColor(run.features?.collective_score || 0) }}>
              {(run.features?.collective_score || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🔄</span>
              <span className="indicator-label">Max Loops</span>
            </div>
            <div className="indicator-value-single">
              {run.features?.max_loops || 0}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">⚡</span>
              <span className="indicator-label">Total Latency</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.total_latency || 0).toFixed(2)}s
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🎯</span>
              <span className="indicator-label">Total Tokens</span>
            </div>
            <div className="indicator-value-single">
              {run.features?.total_token_usage || 0}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🤖</span>
              <span className="indicator-label">Agents Used</span>
            </div>
            <div className="indicator-value-single">
              {run.features?.num_nodes || 0}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🔗</span>
              <span className="indicator-label">Agent Interactions</span>
            </div>
            <div className="indicator-value-single">
              {run.features?.num_edges || 0}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">�</span>
              <span className="indicator-label">Clustering Coefficient</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.clustering_coefficient || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🔀</span>
              <span className="indicator-label">Transitivity</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.transitivity || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">�</span>
              <span className="indicator-label">Avg Degree Centrality</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.avg_degree_centrality || 0).toFixed(3)}
            </div>
          </div>

          <div className="indicator-card">
            <div className="indicator-header">
              <span className="indicator-icon">🔍</span>
              <span className="indicator-label">PageRank Entropy</span>
            </div>
            <div className="indicator-value-single">
              {(run.features?.pagerank_entropy || 0).toFixed(3)}
            </div>
          </div>
        </div>
      </div>

      {/* Per-Agent Breakdown */}
      {run.monitor_data && run.monitor_data.agent_stats && Object.keys(run.monitor_data.agent_stats).length > 0 && (
        <div className="section-card">
          <h2>👥 Agent-Level Enhancement Data</h2>
          <p className="section-description">
            Detailed view of each agent's performance including scores, latencies, and enhancement loops
          </p>
          
          {/* Agent Collaboration Graph */}
          <AgentCollaborationGraph 
            agentStats={run.monitor_data.agent_stats}
            graphEdges={run.monitor_data.graph_edges || []}
          />
          
          <div className="agents-breakdown">
            {Object.entries(run.monitor_data.agent_stats).map(([agentName, agentData]) => {
              const scores = agentData.scores || [];
              const latencies = agentData.latencies || [];
              const avgScore = scores.length > 0 ? (scores.reduce((a,b) => a+b, 0) / scores.length) : 0;
              const avgLatency = latencies.length > 0 ? (latencies.reduce((a,b) => a+b, 0) / latencies.length) : 0;
              
              return (
                <div key={agentName} className="agent-card">
                  <div className="agent-header">
                    <span className="agent-icon">
                      {agentName.toLowerCase().includes('analyzer') ? '🔍' : 
                       agentName.toLowerCase().includes('coder') ? '💻' : 
                       agentName.toLowerCase().includes('tester') ? '🧪' : 
                       agentName.toLowerCase().includes('reviewer') ? '👁️' : '🤖'}
                    </span>
                    <span className="agent-name">{agentName}</span>
                    <span className="agent-attempts">
                      {agentData.total_calls || 0} call{(agentData.total_calls || 0) !== 1 ? 's' : ''}
                    </span>
                  </div>

                  <div className="agent-stats-grid">
                    <div className="stat-item">
                      <div className="stat-label">Capability</div>
                      <div className="stat-value">{agentData.capability || 'N/A'}</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-label">Enhancement Triggered</div>
                      <div className="stat-value">{agentData.enhancement_triggered || 0}</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-label">Avg Score</div>
                      <div className="stat-value" style={{ color: getScoreColor(avgScore) }}>
                        {avgScore.toFixed(3)}
                      </div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-label">Scores</div>
                      <div className="stat-value">
                        {scores.length > 0 ? scores.map(s => s.toFixed(2)).join(', ') : 'None'}
                      </div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-label">Avg Latency</div>
                      <div className="stat-value">{avgLatency.toFixed(2)}s</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-label">Token Usage</div>
                      <div className="stat-value">{agentData.token_usage || 0}</div>
                    </div>
                  </div>

                  {/* Score Progression */}
                  {scores.length > 1 && (
                    <div className="score-progression">
                      <span className="progression-label">Score Progression:</span>
                      <span className={`progression-value ${scores[scores.length-1] > scores[0] ? 'positive' : 'neutral'}`}>
                        {scores[0].toFixed(3)} → {scores[scores.length-1].toFixed(3)}
                        {scores[scores.length-1] > scores[0] && (
                          <span className="improvement-badge">
                            +{(((scores[scores.length-1] - scores[0]) / scores[0]) * 100).toFixed(1)}%
                          </span>
                        )}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Collective Score (XGBoost) */}
      <div className="section-card highlight">
        <h2>🎯 Collective Score (XGBoost Prediction)</h2>
        <div className="collective-score-display">
          <div className="score-circle" style={{ borderColor: getScoreColor(run.predicted_score) }}>
            <span className="score-value" style={{ color: getScoreColor(run.predicted_score) }}>
              {(run.predicted_score || 0).toFixed(3)}
            </span>
            <span className="score-label">Predicted MAS Performance</span>
          </div>
          <div className="score-description">
            <p>
              This score represents the overall predicted Multi-Agent System performance
              based on {Object.keys(run.features || {}).length} behavioral features analyzed by the XGBoost model.
            </p>
            {run.auto_enhanced && (
              <div className="enhancement-notice">
                ✨ This code was auto-enhanced through iterative improvement loops
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Benchmark Scores (if available) */}
      {(run.humaneval_score || run.gsm8k_score || run.mmlu_score) && (
        <div className="section-card">
          <h2>📈 Benchmark Scores</h2>
          <div className="benchmark-grid">
            {run.humaneval_score && (
              <div className="benchmark-card">
                <div className="benchmark-icon">💻</div>
                <div className="benchmark-name">HumanEval</div>
                <div className="benchmark-score">{run.humaneval_score.toFixed(2)}%</div>
              </div>
            )}
            {run.gsm8k_score && (
              <div className="benchmark-card">
                <div className="benchmark-icon">🔢</div>
                <div className="benchmark-name">GSM8K</div>
                <div className="benchmark-score">{run.gsm8k_score.toFixed(2)}%</div>
              </div>
            )}
            {run.mmlu_score && (
              <div className="benchmark-card">
                <div className="benchmark-icon">📚</div>
                <div className="benchmark-name">MMLU</div>
                <div className="benchmark-score">{run.mmlu_score.toFixed(2)}%</div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* All Features */}
      <div className="section-card">
        <h2>🔧 All Features ({Object.keys(run.features || {}).length})</h2>
        <div className="features-table">
          <table>
            <thead>
              <tr>
                <th>Feature Name</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(run.features || {}).map(([key, value]) => (
                <tr key={key}>
                  <td className="feature-name">{key.replace(/_/g, ' ')}</td>
                  <td className="feature-value">
                    {typeof value === 'number' ? value.toFixed(4) : value}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AdminPromptDetail;
