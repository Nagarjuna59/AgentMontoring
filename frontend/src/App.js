import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import UserDashboardSimple from './pages/UserDashboardSimple';
import AdminDashboard from './pages/AdminDashboard';
import AdminUserDetail from './pages/AdminUserDetail';
import AdminPromptDetail from './pages/AdminPromptDetail';
import AdminAnalytics from './pages/AdminAnalytics';
import AnalyticsPage from './pages/AnalyticsPage';

function App() {
  const [user, setUser] = React.useState(null);

  // Removed auto-login from localStorage to prevent automatic login on page reload
  // Users will need to login each time they open the application

  const handleLogin = (userData) => {
    // Store in sessionStorage instead of localStorage
    // This will clear when browser/tab is closed
    sessionStorage.setItem('token', userData.token);
    sessionStorage.setItem('username', userData.username);
    sessionStorage.setItem('role', userData.role);
    setUser(userData);
  };

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('role');
    setUser(null);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={
          user ? <Navigate to={user.role === 'admin' ? '/admin-dashboard' : '/dashboard'} /> : 
          <Login onLogin={handleLogin} />
        } />
        <Route path="/register" element={
          user ? <Navigate to={user.role === 'admin' ? '/admin-dashboard' : '/dashboard'} /> : 
          <Register onLogin={handleLogin} />
        } />
        <Route path="/dashboard" element={
          user && user.role === 'user' ? 
          <UserDashboardSimple user={user} onLogout={handleLogout} /> : 
          <Navigate to="/login" />
        } />
        <Route path="/admin-dashboard" element={
          user && user.role === 'admin' ? 
          <AdminDashboard user={user} onLogout={handleLogout} /> : 
          <Navigate to="/login" />
        } />
        <Route path="/admin/user/:userId" element={
          user && user.role === 'admin' ? 
          <AdminUserDetail /> : 
          <Navigate to="/login" />
        } />
        <Route path="/admin/user/:userId/prompt/:promptId" element={
          user && user.role === 'admin' ? 
          <AdminPromptDetail /> : 
          <Navigate to="/login" />
        } />
        <Route path="/admin/analytics" element={
          user && user.role === 'admin' ? 
          <AdminAnalytics /> : 
          <Navigate to="/login" />
        } />
        <Route path="/analytics/:runId" element={
          user ? 
          <AnalyticsPage user={user} onLogout={handleLogout} /> : 
          <Navigate to="/login" />
        } />
      </Routes>
    </Router>
  );
}

export default App;
