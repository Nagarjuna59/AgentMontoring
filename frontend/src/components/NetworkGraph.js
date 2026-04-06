import React, { useEffect, useRef } from 'react';
import './NetworkGraph.css';

function NetworkGraph({ data, onNodeSelect }) {
  const svgRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (data && data.nodes.length > 0) {
      drawNetwork();
    }
  }, [data]);

  const drawNetwork = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);

    // Draw links first
    ctx.strokeStyle = '#d0d0d0';
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.5;

    data.links.forEach(link => {
      const sourceNode = data.nodes.find(n => n.id === link.source);
      const targetNode = data.nodes.find(n => n.id === link.target);

      if (sourceNode && targetNode) {
        ctx.beginPath();
        ctx.moveTo(sourceNode.x, sourceNode.y);
        ctx.lineTo(targetNode.x, targetNode.y);
        ctx.stroke();
      }
    });

    ctx.globalAlpha = 1;

    // Draw nodes
    data.nodes.forEach(node => {
      const nodeSize = 30 + (node.value * 20);

      // Node circle
      ctx.fillStyle = node.color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, nodeSize, 0, Math.PI * 2);
      ctx.fill();

      // Node border
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Node label
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 12px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const labelText = node.label.split(' ')[0];
      ctx.fillText(labelText, node.x, node.y);
    });

    // Draw title and legend
    ctx.fillStyle = '#333';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'left';
    ctx.fillText('Agent Network Visualization', 20, 30);

    // Add legend
    ctx.font = '12px Arial';
    ctx.fillText('Node size = Agent score', 20, height - 20);
  };

  const positionNodes = () => {
    if (!data || data.nodes.length === 0) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;

    // Position nodes in a circle
    data.nodes.forEach((node, index) => {
      const angle = (index / data.nodes.length) * Math.PI * 2;
      node.x = centerX + radius * Math.cos(angle);
      node.y = centerY + radius * Math.sin(angle);
    });
  };

  useEffect(() => {
    positionNodes();
  }, [data]);

  const handleCanvasClick = (e) => {
    if (!canvasRef.current || !data) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Check if click is on any node
    data.nodes.forEach(node => {
      const nodeSize = 30 + (node.value * 20);
      const distance = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2);

      if (distance <= nodeSize) {
        onNodeSelect(node.id);
      }
    });
  };

  return (
    <div className="network-graph-container">
      <canvas
        ref={canvasRef}
        width={800}
        height={500}
        onClick={handleCanvasClick}
        className="network-canvas"
        title="Click on a node to view agent details"
      />
      <div className="graph-legend">
        <div className="legend-item">
          <span className="legend-icon" style={{ backgroundColor: '#4ECDC4' }}></span>
          <span>Agent Nodes</span>
        </div>
        <div className="legend-item">
          <span className="legend-icon" style={{ backgroundColor: '#d0d0d0' }}></span>
          <span>Interactions</span>
        </div>
        <div className="legend-info">Tip: Click on a node to see agent details</div>
      </div>
    </div>
  );
}

export default NetworkGraph;
