import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 180000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const extractApiError = (error) => {
  if (error?.code === 'ECONNABORTED') {
    return 'Request timed out while waiting for model response. Please try again.';
  }
  if (error?.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error?.message) {
    return error.message;
  }
  return 'Unexpected API error';
};

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const response = await api.post('/login', { username, password });
  return response.data;
};

export const register = async (username, password) => {
  const response = await api.post('/register', { username, password });
  return response.data;
};

export const runMAS = async (task, code = '', language = 'auto', use_full_mas = false) => {
  try {
    const response = await api.post('/run-mas', { task, code, language, use_full_mas });
    return response.data;
  } catch (error) {
    throw new Error(extractApiError(error));
  }
};

// New: start a run and return initial code immediately; enhancement runs in background
export const runMASStart = async (task, language = 'auto', use_full_mas = false) => {
  try {
    const response = await api.post('/run-mas-start', { task, language, use_full_mas }, { timeout: 30000 });
    return response.data;
  } catch (error) {
    throw new Error(extractApiError(error));
  }
};

export const getUserRuns = async () => {
  const response = await api.get('/runs/user');
  return response.data;
};

export const getAllRuns = async () => {
  const response = await api.get('/runs/all');
  return response.data;
};

export const getRun = async (runId) => {
  const response = await api.get(`/run/${runId}`);
  return response.data;
};

export const exportCSV = async () => {
  const response = await api.get('/export_csv');
  return response.data;
};

export const getGraphMetrics = async (runId) => {
  const response = await api.get(`/graph-metrics/${runId}`);
  return response.data;
};

export const getDashboardSummary = async () => {
  const response = await api.get('/dashboard-summary');
  return response.data;
};

export default api;
