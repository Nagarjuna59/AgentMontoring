import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';

const ThemeContext = createContext(null);

const DEFAULT_THEME = 'classic';
const DEFAULT_MODE = 'dark'; // Default to dark mode like Claude

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('skillTheme') || DEFAULT_THEME;
  });

  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved !== null ? JSON.parse(saved) : DEFAULT_MODE === 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-skill-theme', theme);
    document.documentElement.setAttribute('data-mode', darkMode ? 'dark' : 'light');
    localStorage.setItem('skillTheme', theme);
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [theme, darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  const value = useMemo(() => ({ 
    theme, 
    setTheme, 
    darkMode, 
    setDarkMode,
    toggleDarkMode 
  }), [theme, darkMode]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error('useTheme must be used inside ThemeProvider');
  }
  return ctx;
}
