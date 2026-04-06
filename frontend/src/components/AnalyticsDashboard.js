import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = ({ allRuns }) => {
  const [featureImportance, setFeatureImportance] = useState([]);
  const [scoreDistribution, setScoreDistribution] = useState([]);
  const [agentPerformance, setAgentPerformance] = useState([]);
  const [featureRadar, setFeatureRadar] = useState([]);
  const [scoreEvolution, setScoreEvolution] = useState([]);

  useEffect(() => {
    if (allRuns && allRuns.length > 0) {
      calculateAnalytics();
    }
  }, [allRuns]);

  const calculateAnalytics = () => {
    // 1. Feature Importance (from XGBoost model - static weights)
    const importance = [
      { feature: 'avg_personal_score', value: 0.28, category: 'System' },
      { feature: 'collective_score', value: 0.22, category: 'Collective' },
      { feature: 'clustering_coefficient', value: 0.12, category: 'Graph' },
      { feature: 'total_token_usage', value: 0.10, category: 'System' },
      { feature: 'avg_degree_centrality', value: 0.08, category: 'Graph' },
      { feature: 'total_latency', value: 0.06, category: 'System' },
      { feature: 'num_edges', value: 0.05, category: 'Graph' },
      { feature: 'min_personal_score', value: 0.04, category: 'System' },
      { feature: 'max_loops', value: 0.03, category: 'System' },
      { feature: 'pagerank_entropy', value: 0.02, category: 'Graph' },
    ];
    setFeatureImportance(importance);

    // 2. Score Distribution
    const bins = [
      { range: '0.0-0.2', count: 0, color: '#f44336' },
      { range: '0.2-0.4', count: 0, color: '#ff9800' },
      { range: '0.4-0.6', count: 0, color: '#ffc107' },
      { range: '0.6-0.8', count: 0, color: '#2196f3' },
      { range: '0.8-1.0', count: 0, color: '#4caf50' },
    ];

    allRuns.forEach(run => {
      const score = run.predicted_score || 0;
      if (score < 0.2) bins[0].count++;
      else if (score < 0.4) bins[1].count++;
      else if (score < 0.6) bins[2].count++;
      else if (score < 0.8) bins[3].count++;
      else bins[4].count++;
    });

    setScoreDistribution(bins);

    // 3. Agent Performance Heatmap
    const agentStats = {};
    let scoreEvolutionData = [];

    allRuns.forEach((run, runIndex) => {
      if (run.monitor_data && run.monitor_data.agent_stats) {
        Object.entries(run.monitor_data.agent_stats).forEach(([agentName, stats]) => {
          if (!agentStats[agentName]) {
            agentStats[agentName] = {
              scores: [],
              latencies: [],
              tokens: 0,
              enhancements: 0,
              calls: 0
            };
          }

          if (stats.scores) agentStats[agentName].scores.push(...stats.scores);
          if (stats.latencies) agentStats[agentName].latencies.push(...stats.latencies);
          agentStats[agentName].tokens += stats.token_usage || 0;
          agentStats[agentName].enhancements += stats.enhancement_triggered || 0;
          agentStats[agentName].calls += stats.total_calls || 1;
        });
      }

      // Score evolution for recent runs (last 10)
      if (runIndex < 10) {
        scoreEvolutionData.push({
          run: `Run ${runIndex + 1}`,
          initial: run.initial_score || 0,
          final: run.predicted_score || 0,
        });
      }
    });

    const agentPerfArray = Object.entries(agentStats).map(([name, stats]) => ({
      agent: name,
      avgScore: stats.scores.length > 0 ? stats.scores.reduce((a, b) => a + b, 0) / stats.scores.length : 0,
      avgLatency: stats.latencies.length > 0 ? stats.latencies.reduce((a, b) => a + b, 0) / stats.latencies.length : 0,
      totalTokens: stats.tokens,
      enhancementRate: stats.calls > 0 ? (stats.enhancements / stats.calls) * 100 : 0,
    }));

    setAgentPerformance(agentPerfArray);
    setScoreEvolution(scoreEvolutionData.reverse()); // Most recent first

    // 4. Feature Radar (average across all runs)
    const featureAverages = {
      avg_personal_score: 0,
      min_personal_score: 0,
      max_loops: 0,
      total_latency: 0,
      total_token_usage: 0,
      num_agents_triggered_enhancement: 0,
      num_nodes: 0,
      num_edges: 0,
      clustering_coefficient: 0,
      avg_degree_centrality: 0,
      collective_score: 0,
    };

    let validRuns = 0;
    allRuns.forEach(run => {
      if (run.features) {
        Object.keys(featureAverages).forEach(key => {
          if (run.features[key] !== undefined) {
            featureAverages[key] += run.features[key];
          }
        });
        validRuns++;
      }
    });

    if (validRuns > 0) {
      Object.keys(featureAverages).forEach(key => {
        featureAverages[key] /= validRuns;
      });
    }

    // Normalize for radar chart (0-1 scale)
    const radarData = [
      { feature: 'Personal Score', value: featureAverages.avg_personal_score * 100, fullMark: 100 },
      { feature: 'Collaboration', value: featureAverages.num_edges * 10, fullMark: 100 },
      { feature: 'Agents', value: featureAverages.num_nodes * 25, fullMark: 100 },
      { feature: 'Clustering', value: featureAverages.clustering_coefficient * 100, fullMark: 100 },
      { feature: 'Collective', value: featureAverages.collective_score * 100, fullMark: 100 },
      { feature: 'Enhancement', value: featureAverages.num_agents_triggered_enhancement * 25, fullMark: 100 },
    ];

    setFeatureRadar(radarData);
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'System': return '#2196f3';
      case 'Graph': return '#4caf50';
      case 'Collective': return '#ff9800';
      default: return '#9e9e9e';
    }
  };

  if (!allRuns || allRuns.length === 0) {
    return (
      <div className="analytics-placeholder">
        <p>📊 No data available yet</p>
        <p className="hint">Run some tasks to see comprehensive analytics</p>
      </div>
    );
  }

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <h2>📊 AgentMonitor Analytics Dashboard</h2>
        <p className="subtitle">Comprehensive insights across {allRuns.length} runs</p>
      </div>

      {/* Chart 1: Feature Importance */}
      <div className="chart-card">
        <h3>🎯 Feature Importance (XGBoost Model)</h3>
        <p className="chart-description">Which features matter most for predicting MAS quality</p>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={featureImportance} layout="vertical" margin={{ left: 150 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 0.3]} />
            <YAxis dataKey="feature" type="category" width={140} />
            <Tooltip />
            <Bar dataKey="value" name="Importance">
              {featureImportance.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getCategoryColor(entry.category)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <div className="chart-legend">
          <span><span className="legend-dot" style={{ background: '#2196f3' }}></span> System Features</span>
          <span><span className="legend-dot" style={{ background: '#4caf50' }}></span> Graph Features</span>
          <span><span className="legend-dot" style={{ background: '#ff9800' }}></span> Collective Score</span>
        </div>
      </div>

      {/* Chart 2: Score Evolution Timeline */}
      <div className="chart-card">
        <h3>📈 Score Evolution (Recent 10 Runs)</h3>
        <p className="chart-description">How code quality improves from initial to final output</p>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={scoreEvolution}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="run" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="initial" stroke="#ff9800" strokeWidth={2} name="Initial Score" />
            <Line type="monotone" dataKey="final" stroke="#4caf50" strokeWidth={2} name="Final Score" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="charts-row">
        {/* Chart 3: Score Distribution */}
        <div className="chart-card half">
          <h3>📉 Score Distribution</h3>
          <p className="chart-description">Distribution of final scores across all runs</p>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" name="Runs">
                {scoreDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Chart 4: Feature Radar */}
        <div className="chart-card half">
          <h3>🎨 Feature Radar (Avg)</h3>
          <p className="chart-description">Holistic view of MAS characteristics</p>
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={featureRadar}>
              <PolarGrid />
              <PolarAngleAxis dataKey="feature" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar name="Average Features" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Chart 5: Agent Performance Heatmap */}
      <div className="chart-card">
        <h3>🔥 Agent Performance Comparison</h3>
        <p className="chart-description">Compare performance across different agents</p>
        <div className="heatmap-container">
          <table className="heatmap-table">
            <thead>
              <tr>
                <th>Agent</th>
                <th>Avg Score</th>
                <th>Avg Latency (s)</th>
                <th>Total Tokens</th>
                <th>Enhancement Rate (%)</th>
              </tr>
            </thead>
            <tbody>
              {agentPerformance.map((agent, index) => (
                <tr key={index}>
                  <td className="agent-name-cell">
                    {agent.agent === 'Analyzer' && '🔍'} 
                    {agent.agent === 'Coder' && '💻'} 
                    {agent.agent === 'Tester' && '🧪'} 
                    {agent.agent === 'Reviewer' && '👁️'}
                    {agent.agent}
                  </td>
                  <td className={`heatmap-cell ${getHeatmapClass(agent.avgScore, 'score')}`}>
                    {agent.avgScore.toFixed(3)}
                  </td>
                  <td className={`heatmap-cell ${getHeatmapClass(agent.avgLatency, 'latency')}`}>
                    {agent.avgLatency.toFixed(2)}
                  </td>
                  <td className={`heatmap-cell ${getHeatmapClass(agent.totalTokens, 'tokens')}`}>
                    {agent.totalTokens}
                  </td>
                  <td className={`heatmap-cell ${getHeatmapClass(agent.enhancementRate, 'rate')}`}>
                    {agent.enhancementRate.toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="summary-stats">
        <div className="stat-box">
          <div className="stat-value">{allRuns.length}</div>
          <div className="stat-label">Total Runs</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">
            {(allRuns.reduce((sum, r) => sum + (r.predicted_score || 0), 0) / allRuns.length).toFixed(3)}
          </div>
          <div className="stat-label">Avg Final Score</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">
            {allRuns.filter(r => r.monitor_data?.auto_enhanced).length}
          </div>
          <div className="stat-label">Auto-Enhanced</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">
            {agentPerformance.length}
          </div>
          <div className="stat-label">Active Agents</div>
        </div>
      </div>
    </div>
  );
};

const getHeatmapClass = (value, type) => {
  if (type === 'score') {
    if (value >= 0.8) return 'heat-excellent';
    if (value >= 0.6) return 'heat-good';
    if (value >= 0.4) return 'heat-fair';
    return 'heat-poor';
  } else if (type === 'latency') {
    if (value < 10) return 'heat-excellent';
    if (value < 20) return 'heat-good';
    if (value < 30) return 'heat-fair';
    return 'heat-poor';
  } else if (type === 'tokens') {
    if (value > 2000) return 'heat-poor';
    if (value > 1000) return 'heat-fair';
    if (value > 500) return 'heat-good';
    return 'heat-excellent';
  } else if (type === 'rate') {
    if (value >= 60) return 'heat-excellent';
    if (value >= 40) return 'heat-good';
    if (value >= 20) return 'heat-fair';
    return 'heat-poor';
  }
  return '';
};

export default AnalyticsDashboard;
