import React, { useState, useEffect, useRef } from 'react';
import { runMASStart, getRun, getUserRuns, getGraphMetrics } from '../api';
import AgentCollaborationGraph from '../components/AgentCollaborationGraph';
import AnalyticsGraphDashboard from '../components/AnalyticsGraphDashboard';
import './UserDashboardSimple.css';

function UserDashboardSimple({ user, onLogout }) {
  const [messages, setMessages] = useState([
    { 
      type: 'assistant', 
      text: '👋 Hi! I\'m your AI coding assistant powered by Multi-Agent System. Just describe what you want to code, and I\'ll generate it for you!',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedMetrics, setExpandedMetrics] = useState({});
  const [recentRuns, setRecentRuns] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [showHistoryDropdown, setShowHistoryDropdown] = useState(false);
  const [showAnalyticsDashboard, setShowAnalyticsDashboard] = useState(false);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const dropdownRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowHistoryDropdown(false);
      }
    };

    if (showHistoryDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showHistoryDropdown]);

  useEffect(() => {
    loadRecentRuns();
  }, []);

  const loadRecentRuns = async () => {
    try {
      const runs = await getUserRuns();
      setRecentRuns(runs);
    } catch (error) {
      console.error('Failed to load recent runs:', error);
    }
  };

  const pollRunResult = async (runId, initialCode, messageIndex, attempts = 0) => {
    // Max 40 attempts * 5 seconds = ~3.5 minutes timeout
    if (attempts >= 40) {
      setMessages((prev) => prev.map((msg, idx) => {
        if (idx !== messageIndex) return msg;
        return {
          ...msg,
          text: '⚠️ Still processing longer than expected. Please retry, or check again from Recent Conversations.',
          isFinalPending: false,
        };
      }));
      return;
    }

    try {
      const run = await getRun(runId);
      const status = run.status || run.progress || 'generating';
      const statusMessage = run.status_message || '';

      if (status === 'failed') {
        setMessages((prev) => prev.map((msg, idx) => {
          if (idx !== messageIndex) return msg;
          return {
            ...msg,
            text: `❌ Generation failed: ${statusMessage || 'Unknown error'}`,
            isFinalPending: false,
            isError: true,
          };
        }));
        loadRecentRuns();
        return;
      }

      // Handle progressive 2-stage generation: brute → optimal
      const progressiveStatuses = ['generating_brute', 'brute_ready', 'generating_optimal'];
      
      if (status === 'queued' || status === 'generating' || status === 'enhancing' || progressiveStatuses.includes(status)) {
        let phaseText = '🕒 Queued...';
        if (status === 'generating_brute') phaseText = '🔄 Stage 1/2: Generating brute force solution...';
        else if (status === 'brute_ready') phaseText = '✅ Brute force ready! Optimal solution in 5s...';
        else if (status === 'generating_optimal') phaseText = '🔄 Stage 2/2: Generating optimal solution...';
        else if (status === 'generating') phaseText = '⚙️ Generating initial code...';
        else if (status === 'enhancing') phaseText = '✨ Enhancing and scoring output...';

        setMessages((prev) => prev.map((msg, idx) => {
          if (idx !== messageIndex) return msg;
          return {
            ...msg,
            brute_code: run.brute_code || msg.brute_code,
            brute_explanation: run.brute_explanation || msg.brute_explanation,
            optimal_code: run.optimal_code || run.code || msg.optimal_code,
            optimal_explanation: run.optimal_explanation || msg.optimal_explanation,
            initial_code: run.brute_code || run.initial_code || msg.initial_code,
            final_code: run.code && run.code !== run.initial_code ? run.code : msg.final_code,
            code_explanation: run.code_explanation || run.optimal_explanation || msg.code_explanation,
            text: statusMessage || phaseText,
            metrics: {
              ...msg.metrics,
              run_id: run._id || runId,
              initial_score: run.initial_score || msg.metrics?.initial_score,
              final_score: run.predicted_score || msg.metrics?.final_score,
            },
          };
        }));
      }

      if (status === 'done') {
        setMessages((prev) => prev.map((msg, idx) => {
          if (idx !== messageIndex) return msg;
          return {
            ...msg,
            brute_code: run.brute_code || msg.brute_code,
            brute_explanation: run.brute_explanation || msg.brute_explanation,
            optimal_code: run.optimal_code || run.code,
            optimal_explanation: run.optimal_explanation || run.code_explanation,
            initial_code: run.brute_code || run.initial_code || msg.initial_code,
            final_code: run.code,
            code_explanation: run.code_explanation || run.optimal_explanation || msg.code_explanation,
            metrics: {
              ...msg.metrics,
              final_score: run.predicted_score,
              initial_score: run.initial_score,
              features: run.features,
              auto_enhanced: run.auto_enhanced,
              enhancement_loops: run.enhancement_loops,
              run_id: run._id,
            },
            text: '✨ All stages complete! Brute → Optimal',
            isFinalPending: false,
          };
        }));
        loadRecentRuns();
        return;
      }
    } catch (error) {
      console.error('Polling run failed:', error);
    }

    // Poll every 5 seconds instead of 3 to reduce server load
    setTimeout(() => pollRunResult(runId, initialCode, messageIndex, attempts + 1), 5000);
  };

  const startNewChat = () => {
    setMessages([
      { 
        type: 'assistant', 
        text: '👋 Hi! I\'m your AI coding assistant. What would you like to code today?',
        timestamp: new Date()
      }
    ]);
    setCurrentConversationId(null);
    setExpandedMetrics({});
  };

  const loadConversation = (run) => {
    setMessages([
      { 
        type: 'assistant', 
        text: '📂 Previous conversation loaded.',
        timestamp: new Date(run.created_at)
      },
      {
        type: 'user',
        text: run.task,
        timestamp: new Date(run.created_at)
      },
      {
        type: 'assistant',
        text: '✅ Here\'s your code:',
        initial_code: run.initial_code || run.code,
        final_code: run.code,
        code: run.code,
        metrics: {
          initial_score: run.initial_score || run.predicted_score,
          final_score: run.predicted_score,
          enhancement_loops: run.enhancement_loops || 0,
          auto_enhanced: run.auto_enhanced || false,
          features: run.features,
          run_id: run._id
        },
        timestamp: new Date(run.created_at)
      }
    ]);
    setCurrentConversationId(run._id);
    setSidebarOpen(false); // Close sidebar on mobile
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || loading) return;

    const userMessage = inputText.trim();
    setInputText('');

    const userMsg = {
      type: 'user',
      text: userMessage,
      timestamp: new Date()
    };
    setLoading(true);

    try {
      const response = await runMASStart(userMessage, 'auto', false);
      const initialCode = response.initial_code || '';
      const assistantMsg = {
        type: 'assistant',
        text: '🕒 Queued. Starting generation...',
        initial_code: initialCode,
        final_code: null,
        code_explanation: null,
        metrics: {
          initial_score: 0,
          final_score: 0,
          enhancement_loops: 0,
          auto_enhanced: false,
          features: null,
          run_id: response.run_id
        },
        timestamp: new Date(),
        isFinalPending: true
      };

      const messageIndex = messages.length + 1;
      setMessages(prev => [...prev, userMsg, assistantMsg]);
      pollRunResult(response.run_id, initialCode, messageIndex);
      loadRecentRuns();
    } catch (error) {
      const errorMsg = {
        type: 'assistant',
        text: `❌ Sorry, something went wrong: ${error.message}`,
        isError: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleMetrics = (index) => {
    setExpandedMetrics(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const loadAnalyticsData = async (runId) => {
    try {
      setAnalyticsLoading(true);
      const data = await getGraphMetrics(runId);
      setAnalyticsData(data);
      setShowAnalyticsDashboard(true);
    } catch (err) {
      console.error('Error loading analytics:', err);
      alert('Failed to load analytics dashboard. Please try again.');
    } finally {
      setAnalyticsLoading(false);
    }
  };

  const closeAnalyticsDashboard = () => {
    setShowAnalyticsDashboard(false);
    setAnalyticsData(null);
  };

  return (
    <div className="simple-dashboard">
      {/* Top Navigation Bar */}
      <div className="history-menubar">
        <button 
          className="sidebar-toggle-button"
          onClick={() => setShowHistoryDropdown(!showHistoryDropdown)}
          title="Toggle sidebar"
        >
          <span className="menu-icon">☰</span>
        </button>
        
        <div className="menubar-title">
          AgentMonitor - Multi-Agent Code Assistant
        </div>
        
        <div className="user-info">
          <span className="username">👤 {user.username}</span>
          <button className="logout-button-top" onClick={onLogout}>
            Logout
          </button>
        </div>
      </div>

      {/* Dashboard Content Area (Below Navbar) */}
      <div className="dashboard-content">
        {/* ChatGPT-Style Sidebar */}
        {showHistoryDropdown && (
          <>
            <div 
              className="sidebar-overlay" 
              onClick={() => setShowHistoryDropdown(false)}
            ></div>
            <div className="chat-sidebar" ref={dropdownRef}>
              <div className="sidebar-header">
                <button 
                  className="new-chat-btn"
                  onClick={() => {
                    startNewChat();
                    setShowHistoryDropdown(false);
                  }}
                >
                  <span className="btn-icon">+</span>
                  <span>New Chat</span>
                </button>
              </div>
              
              <div className="sidebar-content">
                <h3 className="sidebar-title">Recent Conversations</h3>
                <div className="recent-list">
                  {recentRuns.length === 0 ? (
                    <div className="empty-state">
                      <span style={{color: '#999', fontSize: '0.9rem'}}>No previous conversations</span>
                    </div>
                  ) : (
                    recentRuns.map((run, idx) => (
                      <div 
                        key={run._id || idx}
                        className={`chat-item ${currentConversationId === run._id ? 'active' : ''}`}
                        onClick={() => {
                          loadConversation(run);
                          setShowHistoryDropdown(false);
                        }}
                        title={run.task}
                      >
                        <span className="chat-icon">💬</span>
                        <div className="chat-info">
                          <div className="chat-title">
                            {run.task?.substring(0, 45) || 'Untitled'}
                            {run.task?.length > 45 && '...'}
                          </div>
                          <div className="chat-meta">
                            <span className="chat-score">⭐ {run.predicted_score?.toFixed(2) || 'N/A'}</span>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Main Chat Area */}
        <div className="main-chat-area">
          {/* Chat Container */}
          <div className="chat-container">
        {/* Messages */}
        <div className="messages-area">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.type}`}>
              <div className="message-bubble">
                {/* Message Text */}
                <div className="message-text">{msg.text}</div>

                {/* Progressive 2-Stage Code Display: Brute → Optimal */}
                {(msg.brute_code || msg.optimal_code || msg.initial_code || msg.final_code) && (
                  <div className="code-comparison-block">
                    <div className="comparison-header">
                      <h4>🤖 Progressive Code Generation (Brute → Optimal)</h4>
                      {msg.metrics && (
                        <div className="score-comparison">
                          <span className="score-badge brute">
                            Brute: {msg.metrics.initial_score?.toFixed(2) || '0.55'}
                          </span>
                          <span className="arrow">→</span>
                          <span className="score-badge final">
                            Optimal: {msg.metrics.final_score?.toFixed(2) || 'N/A'}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* 2-Panel Progressive Code Display */}
                    <div className="code-comparison-panels two-panels">
                      {/* Panel 1: Brute Force */}
                      <div className="code-panel brute-panel">
                        <div className="panel-label">🔨 Stage 1: Brute Force</div>
                        <pre className="code-content">{msg.brute_code || msg.initial_code || '⏳ Generating...'}</pre>
                        {msg.brute_explanation && (
                          <div className="panel-explanation">
                            <strong>💡 Explanation:</strong> {msg.brute_explanation}
                          </div>
                        )}
                      </div>
                      
                      <div className="comparison-divider">→</div>
                      
                      {/* Panel 2: Optimal */}
                      <div className="code-panel optimal-panel">
                        <div className="panel-label">🏆 Stage 2: Optimal</div>
                        <pre className="code-content highlighted">{msg.optimal_code || msg.final_code || (msg.brute_code ? '⏳ Generating in 5s...' : '⏳ Waiting...')}</pre>
                        {(msg.optimal_explanation || msg.code_explanation) && (
                          <div className="panel-explanation">
                            <strong>💡 Explanation:</strong> {msg.optimal_explanation || msg.code_explanation}
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Final Explanation Summary */}
                    <div className="explanation-block">
                      <h4>💡 Solution Summary</h4>
                      <p>
                        {msg.code_explanation || msg.optimal_explanation || (msg.isFinalPending ? 'Optimization in progress. Full explanation will appear after all 3 stages complete.' : 'No explanation available yet.')}
                      </p>
                    </div>
                    
                    {/* Metrics Toggle */}
                    {msg.metrics && (
                      <div className="message-actions">
                        <button 
                          className="metrics-toggle"
                          onClick={() => toggleMetrics(index)}
                        >
                          {expandedMetrics[index] ? '📊 Hide MAS Metrics' : '📊 Show MAS Metrics'}
                        </button>
                        
                        {msg.metrics.run_id && (
                          <button 
                            className="analytics-btn"
                            onClick={() => loadAnalyticsData(msg.metrics.run_id)}
                            disabled={analyticsLoading}
                          >
                            {analyticsLoading ? '⏳ Loading...' : '📈 View Analytics Dashboard'}
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Collapsible Metrics Panel */}
                {msg.metrics && expandedMetrics[index] && (
                  <div className="metrics-panel">
                    <h4>� Multi-Agent System Metrics</h4>
                    
                    <div className="metrics-section">
                      <h5>🎯 MAS Scores (XGBoost Predicted)</h5>
                      <div className="metrics-grid">
                        <div className="metric-item">
                          <div className="metric-label">Initial MAS Score</div>
                          <div className="metric-value">
                            {msg.metrics.initial_score?.toFixed(4) || 'N/A'}
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Final MAS Score</div>
                          <div className="metric-value highlight">
                            {msg.metrics.final_score?.toFixed(4) || 'N/A'}
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Score Improvement</div>
                          <div className="metric-value success">
                            +{((msg.metrics.final_score - msg.metrics.initial_score) * 100).toFixed(1)}%
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Enhancement Loops</div>
                          <div className="metric-value">
                            {msg.metrics.enhancement_loops || 0}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="metrics-section">
                      <h5>👥 Agent Collaboration</h5>
                      <div className="metrics-grid">
                        <div className="metric-item">
                          <div className="metric-label">Agents Used</div>
                          <div className="metric-value">
                            {msg.metrics.features?.num_nodes || 4}
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Agent Interactions</div>
                          <div className="metric-value">
                            {msg.metrics.features?.num_edges || 0}
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Avg Personal Score</div>
                          <div className="metric-value">
                            {msg.metrics.features?.avg_personal_score?.toFixed(4) || 'N/A'}
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Min Personal Score</div>
                          <div className="metric-value">
                            {msg.metrics.features?.min_personal_score?.toFixed(4) || 'N/A'}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="metrics-section">
                      <h5>⚡ Performance</h5>
                      <div className="metrics-grid">
                        <div className="metric-item">
                          <div className="metric-label">Total Latency</div>
                          <div className="metric-value">
                            {msg.metrics.features?.total_latency?.toFixed(2) || '0'}s
                          </div>
                        </div>
                        
                        <div className="metric-item">
                          <div className="metric-label">Token Usage</div>
                          <div className="metric-value">
                            {msg.metrics.features?.total_token_usage || 0}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Agent Collaboration Graph */}
                    {msg.metrics.agent_stats && Object.keys(msg.metrics.agent_stats).length > 0 && (
                      <div className="metrics-section">
                        <AgentCollaborationGraph 
                          agentStats={msg.metrics.agent_stats}
                          graphEdges={msg.metrics.monitor_data?.graph_edges || []}
                        />
                      </div>
                    )}
                    
                    {msg.metrics.auto_enhanced && (
                      <div className="enhancement-notice">
                        ✨ This code was automatically enhanced by the Multi-Agent System to improve quality
                      </div>
                    )}
                  </div>
                )}

                {/* Timestamp */}
                <div className="message-time">
                  {msg.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {/* Loading Indicator */}
          {loading && (
            <div className="message-wrapper assistant">
              <div className="message-bubble">
                <div className="loading-indicator">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <span>Generating code...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="input-area">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe what you want to code... (e.g., 'Create a function to sort an array')"
            disabled={loading}
            rows="3"
          />
          <button 
            onClick={handleSendMessage}
            disabled={loading || !inputText.trim()}
            className="send-button"
          >
            {loading ? '⏳' : '🚀 Generate'}
          </button>
        </div>
      </div>
      </div>

      {/* Analytics Dashboard Modal */}
      {showAnalyticsDashboard && (
        <div className="analytics-modal-overlay" onClick={closeAnalyticsDashboard}>
          <div className="analytics-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="analytics-modal-header">
              <h2>📊 Analytics Dashboard</h2>
              <button 
                className="close-modal-btn" 
                onClick={closeAnalyticsDashboard}
                title="Close analytics"
              >
                ✕
              </button>
            </div>
            
            <div className="analytics-modal-body">
              {analyticsLoading ? (
                <div className="analytics-loading">
                  <div className="spinner"></div>
                  <p>Loading analytics data...</p>
                </div>
              ) : analyticsData ? (
                <AnalyticsGraphDashboard 
                  metrics={analyticsData.metrics} 
                  agentStats={analyticsData.agent_stats}
                />
              ) : (
                <div className="analytics-error">
                  <p>Failed to load analytics data</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
    </div>
  );
}

export default UserDashboardSimple;
