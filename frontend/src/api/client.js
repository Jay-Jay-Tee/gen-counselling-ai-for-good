/**
 * API Client Configuration
 * Axios instance with base URL and interceptors
 */

import axios from 'axios';

// Base URL for API calls (defaults to same-origin /api which Vite can proxy)
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Only log in development
    if (import.meta.env.DEV) {
      console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error('Request error:', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`API Response: ${response.config.url} - ${response.status}`);
    }
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      if (import.meta.env.DEV) {
        console.error('API Error:', error.response.status, error.response.data);
      }
      
      if (error.response.status === 401) {
        // Handle unauthorized - redirect to login if needed
        console.warn('Unauthorized access');
      } else if (error.response.status === 500) {
        console.error('Server error');
      }
    } else if (error.request) {
      // Request made but no response
      if (import.meta.env.DEV) {
        console.error('No response from server:', error.request);
      }
    } else {
      // Something else happened
      if (import.meta.env.DEV) {
        console.error('Request setup error:', error.message);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
