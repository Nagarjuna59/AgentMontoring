import React, { useEffect, useRef, useState } from 'react';
import './AgentCollaborationGraph.css';

const AgentCollaborationGraph = ({ agentStats, graphEdges }) => {
  const svgRef = useRef(null);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    if (!agentStats || Object.keys(agentStats).length === 0) {
      return;
    }

    // Process nodes from agent stats
    const agentNodes = Object.entries(agentStats).map(([name, stats], index) => {
      const scores = stats.scores || [];
      const avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
      const tokenUsage = stats.token_usage || 0;
      const latencies = stats.latencies || [];
      const avgLatency = latencies.length > 0 ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 0;

      return {
        id: name,
        name: name,
        avgScore: avgScore,
        tokenUsage: tokenUsage,
        avgLatency: avgLatency,
        interactions: scores.length,
        x: 0, // Will be calculated
        y: 0, // Will be calculated
      };
    });

    // Calculate positions in a circle or flow layout
    const width = 600;
    const height = 400;
    const centerX = width / 2;
    const centerY = height / 2;

    if (agentNodes.length === 4) {
      // Flow layout for 4 agents: Analyzer -> Coder -> Tester -> Reviewer
      const spacing = width / 5;
      agentNodes.forEach((node, index) => {
        node.x = spacing * (index + 1);
        node.y = centerY;
      });
    } else if (agentNodes.length === 1) {
      // Single agent in center
      agentNodes[0].x = centerX;
      agentNodes[0].y = centerY;
    } else {
      // Circular layout for other cases
      const radius = Math.min(width, height) / 3;
      agentNodes.forEach((node, index) => {
        const angle = (index / agentNodes.length) * 2 * Math.PI - Math.PI / 2;
        node.x = centerX + radius * Math.cos(angle);
        node.y = centerY + radius * Math.sin(angle);
      });
    }

    setNodes(agentNodes);

    // Process edges
    if (graphEdges && graphEdges.length > 0) {
      const processedEdges = graphEdges.map(edge => {
        const fromNode = agentNodes.find(n => n.id === edge.from);
        const toNode = agentNodes.find(n => n.id === edge.to);
        return {
          from: edge.from,
          to: edge.to,
          x1: fromNode?.x || 0,
          y1: fromNode?.y || 0,
          x2: toNode?.x || 0,
          y2: toNode?.y || 0,
        };
      });
      setEdges(processedEdges);
    }
  }, [agentStats, graphEdges]);

  const getNodeColor = (score) => {
    if (score >= 0.8) return '#4caf50'; // Green - Excellent
    if (score >= 0.6) return '#2196f3'; // Blue - Good
    if (score >= 0.4) return '#ff9800'; // Orange - Fair
    return '#f44336'; // Red - Poor
  };

  const getNodeRadius = (interactions) => {
    return Math.max(30, Math.min(60, 30 + interactions * 5));
  };

  if (!agentStats || Object.keys(agentStats).length === 0) {
    return (
      <div className="graph-container">
        <div className="graph-placeholder">
          <p>No agent collaboration data available</p>
          <p className="graph-hint">Submit a task to see the multi-agent collaboration network</p>
        </div>
      </div>
    );
  }

  return (
    <div className="graph-container">
      <div className="graph-header">
        <h3>🔬 Multi-Agent Collaboration Network</h3>
        <p className="graph-subtitle">Visual representation of agent interactions and performance</p>
      </div>

      <svg ref={svgRef} width="600" height="400" className="collaboration-graph">
        {/* Draw edges first (so they appear behind nodes) */}
        {edges.map((edge, index) => (
          <g key={`edge-${index}`}>
            <defs>
              <marker
                id={`arrowhead-${index}`}
                markerWidth="10"
                markerHeight="10"
                refX="9"
                refY="3"
                orient="auto"
                markerUnits="strokeWidth"
              >
                <path d="M0,0 L0,6 L9,3 z" fill="#666" />
              </marker>
            </defs>
            <line
              x1={edge.x1}
              y1={edge.y1}
              x2={edge.x2}
              y2={edge.y2}
              stroke="#666"
              strokeWidth="2"
              markerEnd={`url(#arrowhead-${index})`}
              className="graph-edge"
            />
          </g>
        ))}

        {/* Draw nodes */}
        {nodes.map((node, index) => (
          <g key={`node-${node.id}`} className="graph-node">
            {/* Node circle */}
            <circle
              cx={node.x}
              cy={node.y}
              r={getNodeRadius(node.interactions)}
              fill={getNodeColor(node.avgScore)}
              stroke="#fff"
              strokeWidth="3"
              className="node-circle"
            />
            
            {/* Agent name */}
            <text
              x={node.x}
              y={node.y - 5}
              textAnchor="middle"
              fill="#fff"
              fontSize="14"
              fontWeight="bold"
            >
              {node.name}
            </text>
            
            {/* Score */}
            <text
              x={node.x}
              y={node.y + 10}
              textAnchor="middle"
              fill="#fff"
              fontSize="12"
            >
              {node.avgScore.toFixed(2)}
            </text>

            {/* Tooltip on hover */}
            <title>
              {`${node.name}\nAvg Score: ${node.avgScore.toFixed(3)}\nTokens: ${node.tokenUsage}\nAvg Latency: ${node.avgLatency.toFixed(1)}s\nInteractions: ${node.interactions}`}
            </title>
          </g>
        ))}
      </svg>

      {/* Legend */}
      <div className="graph-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#4caf50' }}></div>
          <span>Excellent (≥0.8)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#2196f3' }}></div>
          <span>Good (0.6-0.8)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#ff9800' }}></div>
          <span>Fair (0.4-0.6)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#f44336' }}></div>
          <span>Poor (&lt;0.4)</span>
        </div>
        <div className="legend-note">
          <small>💡 Node size = interaction count | Arrows = collaboration flow</small>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="graph-stats">
        <div className="stat-card">
          <span className="stat-label">Agents</span>
          <span className="stat-value">{nodes.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Collaborations</span>
          <span className="stat-value">{edges.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Avg Score</span>
          <span className="stat-value">
            {nodes.length > 0 
              ? (nodes.reduce((sum, n) => sum + n.avgScore, 0) / nodes.length).toFixed(2)
              : '0.00'}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Total Tokens</span>
          <span className="stat-value">
            {nodes.reduce((sum, n) => sum + n.tokenUsage, 0)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default AgentCollaborationGraph;
