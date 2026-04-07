import React from 'react';
import { useTheme } from '../context/ThemeContext';
import './ThemeSelector.css';

const themeOptions = [
  // { key: 'leetcode', label: 'LeetCode', subtitle: 'Easy Medium Hard' },
  { key: 'focus', label: 'Focus', subtitle: 'Deep work mode' },
  { key: 'classic', label: 'Classic', subtitle: 'Neutral dashboard' },
];

function ThemeSelector() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="theme-selector" role="group" aria-label="Skill theme selector">
      {themeOptions.map((option) => (
        <button
          key={option.key}
          type="button"
          className={`theme-chip ${theme === option.key ? 'active' : ''}`}
          onClick={() => setTheme(option.key)}
          title={option.subtitle}
          aria-pressed={theme === option.key}
        >
          <span className="chip-label">{option.label}</span>
          {option.key === 'leetcode' && (
            <span className="chip-badges">
              <i className="b-easy">E</i>
              <i className="b-medium">M</i>
              <i className="b-hard">H</i>
            </span>
          )}
        </button>
      ))}
    </div>
  );
}

export default ThemeSelector;
