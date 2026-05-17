import React from 'react';
import { useTheme } from '../context/ThemeContext';
import './ThemeSelector.css';

function ThemeSelector() {
  const { darkMode, setDarkMode } = useTheme();

  return (
    <div className="theme-selector" role="group" aria-label="Dark/Light theme selector">
      <button
        type="button"
        className={`theme-chip ${!darkMode ? 'active' : ''}`}
        onClick={() => setDarkMode(false)}
        title="Light mode"
        aria-pressed={!darkMode}
      >
        <span className="chip-label">Light</span>
      </button>
      <button
        type="button"
        className={`theme-chip ${darkMode ? 'active' : ''}`}
        onClick={() => setDarkMode(true)}
        title="Dark mode"
        aria-pressed={darkMode}
      >
        <span className="chip-label">Dark</span>
      </button>
    </div>
  );
}

export default ThemeSelector;
