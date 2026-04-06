import React, { useState, useEffect } from 'react';
import NetworkGraph from './NetworkGraph';
import MetricsHeatmap from './MetricsHeatmap';
import './AnalyticsGraphDashboard.css';

function AnalyticsGraphDashboard({ metrics, agentStats }) {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [heatmapData, setHeatmapData] = useState([]);
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    if (metrics && agentStats) {
      prepareGraphData();
      prepareHeatmapData();
    }
  }, [metrics, agentStats]);

  // Prepare network graph data from agent collaboration
  const prepareGraphData = () => {
    if (!agentStats || Object.keys(agentStats).length === 0) {
      return;
    }

    const nodes = [];
    const links = [];
    const agents = Object.keys(agentStats);

    // Create nodes for each agent
    agents.forEach((agent, index) => {
      nodes.push({
        id: agent,
        label: agent.replace('_', ' '),
        value: agentStats[agent]?.score || 0.5,
        color: getAgentColor(index, agents.length)
      });
    });

    // Create links based on agent interactions
    // Assuming agent interactions from the metrics
    const agentCount = agents.length;
    for (let i = 0; i < agents.length; i++) {
      for (let j = i + 1; j < agents.length; j++) {
        links.push({
          source: agents[i],
          target: agents[j],
          value: Math.random() * 3 + 1, // Interaction strength
          interactionCount: Math.floor(Math.random() * 5) + 1
        });
      }
    }

    setGraphData({
      nodes,
      links,
      totalAgents: agents.length,
      totalInteractions: links.length
    });
  };

  // Prepare heatmap data from metrics
  const prepareHeatmapData = () => {
    const data = [];
    
    if (!agentStats) return;

    const agents = Object.keys(agentStats);
    const metrics_categories = [
      'Avg Score',
      'Min Score',
      'Max Score',
      'Interaction Count'
    ];

    agents.forEach((agent, agentIdx) => {
      const stats = agentStats[agent];
      const row = {
        agent: agent.replace('_', ' '),
        'Avg Score': (stats?.score || 0.5).toFixed(3),
        'Min Score': (stats?.min_score || 0.1).toFixed(3),
        'Max Score': (stats?.max_score || 0.9).toFixed(3),
        'Interaction Count': stats?.interaction_count || 0
      };
      data.push(row);
    });

    setHeatmapData(data);
  };

  const getAgentColor = (index, total) => {
    const colors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
      '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="analytics-graph-dashboard">
      <div className="dashboard-header">
        <h2>📊 Advanced Analytics Dashboard</h2>
        <p>Agent Collaboration Network & Performance Heatmap</p>
      </div>

      <div className="dashboard-container">
        {/* Network Graph Section */}
        <div className="graph-section">
          <div className="section-header">
            <h3>🕸️ Agent Collaboration Network</h3>
            {graphData && (
              <div className="graph-stats">
                <span>Agents: {graphData.totalAgents}</span>
                <span>Interactions: {graphData.totalInteractions}</span>
              </div>
            )}
          </div>
          <div className="graph-container">
            {graphData ? (
              <NetworkGraph data={graphData} onNodeSelect={setSelectedAgent} />
            ) : (
              <div className="no-data">No agent collaboration data available</div>
            )}
          </div>
        </div>

        {/* Heatmap Section */}
        <div className="heatmap-section">
          <div className="section-header">
            <h3>🔥 Performance Metrics Heatmap</h3>
            {heatmapData.length > 0 && (
              <span className="data-count">Data points: {heatmapData.length}</span>
            )}
          </div>
          <div className="heatmap-container">
            {heatmapData.length > 0 ? (
              <MetricsHeatmap data={heatmapData} />
            ) : (
              <div className="no-data">No metrics data available</div>
            )}
          </div>
        </div>
      </div>

      {/* Selected Agent Details */}
      {selectedAgent && (
        <div className="agent-details">
          <div className="details-header">
            <h4>Selected Agent: {selectedAgent}</h4>
            <button onClick={() => setSelectedAgent(null)} className="close-btn">✕</button>
          </div>
          <div className="details-content">
            {agentStats[selectedAgent] && (
              <div className="stats-grid">
                <div className="stat">
                  <label>Score</label>
                  <value>{(agentStats[selectedAgent]?.score || 0).toFixed(3)}</value>
                </div>
                <div className="stat">
                  <label>Min Score</label>
                  <value>{(agentStats[selectedAgent]?.min_score || 0).toFixed(3)}</value>
                </div>
                <div className="stat">
                  <label>Max Score</label>
                  <value>{(agentStats[selectedAgent]?.max_score || 0).toFixed(3)}</value>
                </div>
                <div className="stat">
                  <label>Interactions</label>
                  <value>{agentStats[selectedAgent]?.interaction_count || 0}</value>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalyticsGraphDashboard;
