import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Обработчик ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API методы для статей
export const articleAPI = {
  getArticles: (params = {}) => api.get('/articles', { params }),
  getArticleById: (id) => api.get(`/articles/${id}`),
  searchArticles: (query) => api.get('/articles/search/by-text', { params: { q: query } }),
  getArticlesBySource: (sourceId, params = {}) =>
    api.get(`/articles/source/${sourceId}`, { params }),
  getArticlesByProject: (projectId, params = {}) =>
    api.get(`/articles/project/${projectId}`, { params }),
  getStatsByProject: () => api.get('/articles/stats/by-project'),
  getStatsBySource: () => api.get('/articles/stats/by-source'),
  getStatsTimeline: () => api.get('/articles/stats/timeline'),
};

// API методы для проектов
export const projectAPI = {
  listProjects: (params = {}) => api.get('/projects', { params }),
  getProjectById: (id) => api.get(`/projects/${id}`),
  getProjectStats: (id) => api.get(`/projects/${id}/stats`),
  searchProjects: (query) => api.get('/projects/search/by-keyword', { params: { q: query } }),
};

// API методы для источников
export const sourceAPI = {
  listSources: (params = {}) => api.get('/sources', { params }),
  getSourceById: (id) => api.get(`/sources/${id}`),
  getSourceStats: (id) => api.get(`/sources/${id}/stats`),
  triggerParse: (id) => api.post(`/sources/${id}/parse`),
};

export default api;
