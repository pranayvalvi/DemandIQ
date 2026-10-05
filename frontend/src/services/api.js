import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboardSummary = () => apiClient.get('/dashboard-summary').then(res => res.data);
export const getModelPerformance = () => apiClient.get('/model-performance').then(res => res.data.performance);
export const getSystemInfo = () => apiClient.get('/system-info').then(res => res.data);
export const getStores = () => apiClient.get('/stores').then(res => res.data.stores);
export const getProducts = () => apiClient.get('/products').then(res => res.data.products);
export const getCategories = () => apiClient.get('/categories').then(res => res.data.categories);
export const predictDemand = (payload) => apiClient.post('/predict', payload).then(res => res.data);
export const getInventoryInsights = (payload) => apiClient.post('/inventory-insights', payload).then(res => res.data);
