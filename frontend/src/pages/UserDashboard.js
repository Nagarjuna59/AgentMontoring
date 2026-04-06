import React, { useState, useEffect, useRef } from 'react';
import { runMAS, runMASStart, getUserRuns, getRun } from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import './UserDashboard.css';

function UserDashboard({ user, onLogout }) {
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hello! I\'m your AgentMonitor assistant. Describe a coding task and I\'ll run the Multi-Agent System to help you!' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentResult, setCurrentResult] = useState(null);
  const [initialResult, setInitialResult] = useState(null);
  const [showEnhancedCode, setShowEnhancedCode] = useState(false);
  const [recentRuns, setRecentRuns] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showDetailsPanel, setShowDetailsPanel] = useState(false); // Toggle for right panel
  const [useFullMAS, setUseFullMAS] = useState(false); // NEW: Toggle for full 4-agent MAS mode
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    loadRecentRuns();
  }, []);

  const loadRecentRuns = async () => {
    try {
      const runs = await getUserRuns();
      setRecentRuns(runs);
    } catch (err) {
      console.error('Failed to load recent runs:', err);
    }
  };

  const startNewConversation = () => {
    setMessages([
      { type: 'bot', text: 'Hello! I\'m your AgentMonitor assistant. Describe a coding task and I\'ll run the Multi-Agent System to help you!' }
    ]);
    setCurrentResult(null);
    setCurrentConversationId(null);
    setShowEnhancedCode(false);
  };

  const loadConversation = (run) => {
    // Load a previous conversation/run
    setMessages([
      { type: 'bot', text: 'Previous conversation loaded.' },
      { type: 'user', text: run.task },
      {
        type: 'bot',
        text: `✅ MAS execution completed! Predicted score: ${run.predicted_score.toFixed(2)}`,
        result: {
          run_id: run._id,
          predicted_score: run.predicted_score,
          final_score: run.predicted_score,
          initial_score: run.initial_score,
          initial_code: run.initial_code || run.code,
          final_code: run.code,
          features: run.features,
          result: run.code,
          code: run.code,
          enhancement_loops: run.enhancement_loops || 0,
          auto_enhanced: run.auto_enhanced || false
        }
      }
    ]);
    setCurrentResult({
      run_id: run._id,
      predicted_score: run.predicted_score,
      final_score: run.predicted_score,
      initial_score: run.initial_score,
      initial_code: run.initial_code || run.code,
      final_code: run.code,
      features: run.features,
      result: run.code,
      code: run.code,
      enhancement_loops: run.enhancement_loops || 0,
      auto_enhanced: run.auto_enhanced || false
    });
    setCurrentConversationId(run._id);
    setShowEnhancedCode(false);
    setShowDetailsPanel(false);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');

    // Add user message to chat
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setLoading(true);

    // Add loading message
    setMessages(prev => [...prev, { type: 'bot', text: 'Generating initial code...', isLoading: true }] );

    try {
  // Start the run and get initial code immediately (pass use_full_mas flag)
  const startResp = await runMASStart(userMessage, 'auto', useFullMAS);
      const runId = startResp.run_id;
      const initial_code = startResp.initial_code || '';

      // Remove loading message and show initial code
  setMessages(prev => prev.filter(m => !m.isLoading));
  // Show initial code inline as a chat-like message
  setMessages(prev => [...prev, { type: 'bot', text: '✅ Initial code (fast):', result: { code: initial_code, predicted_score: 0.0 } }]);

      setCurrentResult({ code: initial_code, predicted_score: 0.0, run_id: runId });
      setInitialResult({ code: initial_code, predicted_score: 0.0, run_id: runId });

      // Poll for enhanced result
      let attempts = 0;
      const maxAttempts = 40; // up to ~2 minutes
      const pollInterval = 3000;

      const poll = async () => {
        try {
          const runData = await getRun(runId);
          if (runData && runData.monitor_data) {
            // Enhancement complete
            setMessages(prev => [...prev, { type: 'bot', text: `🔄 Enhancement complete. Predicted score: ${runData.predicted_score.toFixed(2)}`, result: runData }]);
            setCurrentResult(runData);
            setShowEnhancedCode(true);
            setShowDetailsPanel(true);
            loadRecentRuns();
            setLoading(false);
            return;
          }
        } catch (e) {
          console.error('Polling error', e);
        }
        attempts += 1;
        if (attempts < maxAttempts) setTimeout(poll, pollInterval);
        else {
          setMessages(prev => [...prev, { type: 'bot', text: '⚠️ Enhancement did not finish in time. You can click Enhance Again.' }]);
          setLoading(false);
        }
      };

      setTimeout(poll, pollInterval);
    } catch (err) {
      setMessages(prev => prev.filter(m => !m.isLoading));
      setMessages(prev => [...prev, { type: 'bot', text: `❌ Error: ${err.message}`, isError: true }]);
    } finally {
      setLoading(false);
    }
  };

  const handleEnhanceAgain = async () => {
    if (!currentResult || loading) return;

    setLoading(true);
    setMessages(prev => [...prev, { type: 'bot', text: 'Enhancing code with improved MAS configuration...', isLoading: true }]);

    try {
      const lastUserMessage = messages.filter(msg => msg.type === 'user').slice(-1)[0]?.text || '';
      const currentCode = currentResult.code || currentResult.result || '';
      const data = await runMAS(lastUserMessage, currentCode);

      setMessages(prev => prev.filter(msg => !msg.isLoading));
      setMessages(prev => [...prev, { type: 'bot', text: `✅ Enhancement complete. Initial score: ${initialResult?.predicted_score || 0} → Enhanced: ${data.predicted_score.toFixed(2)}`, result: data }]);

      setCurrentResult(data);
      setShowEnhancedCode(true);
      setShowDetailsPanel(true);
      loadRecentRuns();
    } catch (err) {
      setMessages(prev => prev.filter(msg => !msg.isLoading));
      setMessages(prev => [...prev, { type: 'bot', text: `❌ Enhancement failed: ${err.message}`, isError: true }]);
    } finally {
      setLoading(false);
    }
  };

  const getFeatureChartData = (features) => {
    if (!features) return [];
    return Object.entries(features).map(([key, value]) => ({
      name: key.replace(/_/g, ' '),
      value: typeof value === 'number' ? value : 0
    }));
  };

  const getRadarData = (features) => {
    if (!features) return [];
    return [
      { metric: 'Avg Score', value: features.avg_personal_score * 100 },
      { metric: 'Min Score', value: features.min_personal_score * 100 },
      { metric: 'Collective', value: features.collective_score * 100 },
      { metric: 'Nodes', value: (features.num_nodes / 10) * 100 },
      { metric: 'Edges', value: (features.num_edges / 20) * 100 },
      { metric: 'Clustering', value: features.clustering_coefficient * 100 }
    ];
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <button 
            className="sidebar-toggle" 
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title={sidebarCollapsed ? "Show sidebar" : "Hide sidebar"}
          >
            {sidebarCollapsed ? '☰' : '✕'}
          </button>
          <h1>🤖 AgentMonitor Assistant</h1>
        </div>
        <div className="user-info">
          <span>Welcome, {user.username}</span>
          <button onClick={onLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      {/* Main Layout with Sidebar */}
      <div className="dashboard-body">
        {/* Sidebar - Recent Conversations */}
        <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
          <button className="new-chat-btn" onClick={startNewConversation}>
            ➕ New Conversation
          </button>
          
          <div className="recent-conversations">
            <h3>Recent</h3>
            <div className="conversations-list">
              {recentRuns.length === 0 ? (
                <p className="no-conversations">No conversations yet</p>
              ) : (
                recentRuns.map((run) => (
                  <div 
                    key={run._id} 
                    className={`conversation-item ${currentConversationId === run._id ? 'active' : ''}`}
                    onClick={() => loadConversation(run)}
                  >
                    <div className="conversation-title">
                      {run.task.substring(0, 40)}{run.task.length > 40 ? '...' : ''}
                    </div>
                    <div className="conversation-meta">
                      <span className="score">⭐ {run.predicted_score.toFixed(2)}</span>
                      <span className="date">{new Date(run.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </aside>

        {/* Main Content - 2 Column Layout */}
        <div className="main-content">
          {/* Left Panel - Chatbot Conversation */}
          <div className="chat-panel">
            <div className="messages-container">
              {messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.type}`}>
                  <div className="message-bubble">
                  {msg.isLoading && <div className="loading-dots"><span></span><span></span><span></span></div>}
                  {!msg.isLoading && <p>{msg.text}</p>}
                  {msg.result && (
                    <div className="inline-result">
                      <div className="result-header">
                        <div className="score-badge">Score: {msg.result.predicted_score.toFixed(2)}</div>
                        <button 
                          className="view-details-btn"
                          onClick={() => {
                            setCurrentResult(msg.result);
                            setShowDetailsPanel(true);
                          }}
                        >
                          📊 View More Details
                        </button>
                      </div>
                      
                      {/* Inline code preview */}
                      <div className="code-preview">
                        <div className="code-preview-header">
                          <span>💻 Generated Code</span>
                        </div>
                        <pre className="code-preview-content">
                          {(() => {
                            const codeText = msg.result.code || msg.result.result || 'No code generated';
                            console.log('Displaying code preview:', codeText.substring(0, 50));
                            return codeText.substring(0, 300) + (codeText.length > 300 ? '...' : '');
                          })()}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="chat-input-container">
            <div className="input-options">
              <label className="full-mas-toggle">
                <input 
                  type="checkbox" 
                  checked={useFullMAS} 
                  onChange={(e) => setUseFullMAS(e.target.checked)}
                />
                <span>🔬 Full MAS Mode (4 agents + graph metrics)</span>
              </label>
            </div>
            <div className="input-row">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Describe your coding task (e.g., 'Create a function to sort an array')..."
                disabled={loading}
                rows="3"
              />
              <button 
                onClick={handleSendMessage} 
                disabled={loading || !inputMessage.trim()}
                className="send-btn"
              >
                {loading ? '⏳' : '🚀 Run MAS'}
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel - Code & Indicators (Toggleable) */}
        {showDetailsPanel && currentResult && (
        <div className="details-panel show">
          {/* Close button */}
          <button 
            className="close-details-btn" 
            onClick={() => setShowDetailsPanel(false)}
            title="Close details panel"
          >
            ✕
          </button>
          
          {currentResult ? (
            <>
              {/* Code Section - Simple, clean code display */}
              <div className="code-section">
                {showEnhancedCode && initialResult ? (
                  <div className="code-comparison">
                    <div className="code-column">
                      <h3>📝 Initial Code (Score: {initialResult.predicted_score.toFixed(2)})</h3>
                      <div className="code-display white">
                        <pre>{initialResult.code || initialResult.result || 'No code'}</pre>
                      </div>
                    </div>
                    <div className="code-column">
                      <h3 className="enhanced-title">✨ Enhanced Code (Score: {currentResult.predicted_score.toFixed(2)})</h3>
                      <div className="code-display white enhanced">
                        <pre>{currentResult.code || currentResult.result || 'No code'}</pre>
                      </div>
                    </div>
                  </div>
                ) : (
                  <>
                    <h3>💻 Complete Generated Code</h3>
                    <div className="code-display white">
                      <pre>{currentResult.code || currentResult.result || 'No code generated'}</pre>
                    </div>
                  </>
                )}
              </div>

              {/* Performance Indicators & Charts Section */}
              <div className="indicators-section">
                <h3>📊 Performance Indicators</h3>
                
                <div className="indicator-grid">
                  <div className="indicator-card">
                    <div className="indicator-label">Predicted Score</div>
                    <div className="indicator-value score">{currentResult.predicted_score.toFixed(2)}</div>
                  </div>
                  <div className="indicator-card">
                    <div className="indicator-label">Agents</div>
                    <div className="indicator-value">{currentResult.features.num_nodes}</div>
                  </div>
                  <div className="indicator-card">
                    <div className="indicator-label">Interactions</div>
                    <div className="indicator-value">{currentResult.features.num_edges}</div>
                  </div>
                  <div className="indicator-card">
                    <div className="indicator-label">Avg Agent Score</div>
                    <div className="indicator-value">{currentResult.features.avg_personal_score.toFixed(2)}</div>
                  </div>
                  <div className="indicator-card">
                    <div className="indicator-label">Enhancement Loops</div>
                    <div className="indicator-value">{currentResult.features.max_loops}</div>
                  </div>
                  <div className="indicator-card">
                    <div className="indicator-label">Total Latency</div>
                    <div className="indicator-value">{currentResult.features.total_latency.toFixed(1)}s</div>
                  </div>
                </div>

                {/* Radar Chart */}
                <div className="chart-container">
                  <h4>Performance Metrics</h4>
                  <ResponsiveContainer width="100%" height={250}>
                    <RadarChart data={getRadarData(currentResult.features)}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="metric" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      <Radar name="Performance" dataKey="value" stroke="#667eea" fill="#667eea" fillOpacity={0.6} />
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>

                {/* All Features Bar Chart */}
                <div className="chart-container">
                  <h4>All Features Breakdown</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getFeatureChartData(currentResult.features)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" angle={-45} textAnchor="end" height={120} fontSize={10} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#667eea" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">🎯</div>
              <h3>No Results Yet</h3>
              <p>Submit a coding task in the chat to see generated code and performance indicators here.</p>
            </div>
          )}
        </div>
        )}
      </div>
      </div>

      {/* Bottom Action Buttons */}
      <div className="action-buttons">
        <button 
          onClick={handleEnhanceAgain} 
          disabled={!currentResult || loading}
          className="enhance-btn"
        >
          ✨ Enhance Again
        </button>
      </div>
    </div>
  );
}

export default UserDashboard;
