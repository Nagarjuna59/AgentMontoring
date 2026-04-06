import React, { useMemo } from 'react';
import './MetricsHeatmap.css';

function MetricsHeatmap({ data }) {
  const metricsColumns = useMemo(() => {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]).filter(key => key !== 'agent');
  }, [data]);

  const getHeatmapColor = (value, metric) => {
    let normalizedValue = 0;

    // Normalize different metric types
    if (metric === 'Interaction Count') {
      normalizedValue = Math.min(parseFloat(value) / 10, 1);
    } else {
      normalizedValue = parseFloat(value);
    }

    // Color gradient from blue (low) to red (high)
    if (normalizedValue < 0.3) {
      return '#3498db'; // Blue
    } else if (normalizedValue < 0.5) {
      return '#2ecc71'; // Green
    } else if (normalizedValue < 0.7) {
      return '#f39c12'; // Orange
    } else {
      return '#e74c3c'; // Red
    }
  };

  const getTextColor = (bgColor) => {
    const colors = {
      '#3498db': '#fff',
      '#2ecc71': '#fff',
      '#f39c12': '#fff',
      '#e74c3c': '#fff'
    };
    return colors[bgColor] || '#333';
  };

  return (
    <div className="metrics-heatmap-container">
      <div className="heatmap-scroll-wrapper">
        <table className="heatmap-table">
          <thead>
            <tr>
              <th className="agent-header">Agent</th>
              {metricsColumns.map(metric => (
                <th key={metric} className="metric-header">
                  {metric}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="heatmap-row">
                <td className="agent-cell">{row.agent}</td>
                {metricsColumns.map(metric => {
                  const value = row[metric];
                  const bgColor = getHeatmapColor(value, metric);
                  const textColor = getTextColor(bgColor);

                  return (
                    <td
                      key={`${rowIndex}-${metric}`}
                      className="heatmap-cell"
                      style={{
                        backgroundColor: bgColor,
                        color: textColor
                      }}
                      title={`${metric}: ${value}`}
                    >
                      <div className="cell-value">
                        {metric === 'Interaction Count' ? value : parseFloat(value).toFixed(3)}
                      </div>
                      <div className="cell-bar" style={{
                        width: `${Math.min(parseFloat(value) * 100, 100)}%`,
                        backgroundColor: 'rgba(0,0,0,0.2)'
                      }}></div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="heatmap-legend">
        <div className="legend-title">Color Scale</div>
        <div className="legend-scale">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#3498db' }}></div>
            <span>Low (0-0.3)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#2ecc71' }}></div>
            <span>Medium (0.3-0.5)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#f39c12' }}></div>
            <span>High (0.5-0.7)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#e74c3c' }}></div>
            <span>Very High (0.7+)</span>
          </div>
        </div>
      </div>

      <div className="heatmap-stats">
        <div className="stat-item">
          <label>Total Agents:</label>
          <value>{data.length}</value>
        </div>
        <div className="stat-item">
          <label>Total Metrics:</label>
          <value>{metricsColumns.length}</value>
        </div>
        <div className="stat-item">
          <label>Data Points:</label>
          <value>{data.length * metricsColumns.length}</value>
        </div>
      </div>
    </div>
  );
}

export default MetricsHeatmap;
