import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const app = createApp(App)
app.use(createPinia())
app.use(router, axios)

// Initialize the store
const userStore = useUserStore();

// Track if a refresh is already in progress
let isRefreshing = false;
let failedQueue = [];

// Process queue of failed requests
const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

// Request interceptor
axios.interceptors.request.use(
  (config) => {
    if (userStore.access) {
      config.headers['Authorization'] = `Bearer ${userStore.access}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor 
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If not 401 error or no refresh token available, reject immediately
    if (!error.response || error.response.status !== 401 || !userStore.refresh) {
      return Promise.reject(error);
    }
    
    // Special case to avoid infinite loops
    // If the 401 comes from a refresh token attempt, logout immediately
    if (originalRequest.url && originalRequest.url.includes('token/refresh')) {
      userStore.removeToken();
      processQueue(new Error('Refresh token expired'));
      return Promise.reject(error);
    }

    // If retry already attempted for non-refresh endpoint or a refresh is already in progress
    if (originalRequest._retry === true) {
      return Promise.reject(error);
    }
    
    originalRequest._retry = true;
    
    // If we're already refreshing, add this request to the queue
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      })
        .then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          return axios(originalRequest);
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
    
    isRefreshing = true;
    
    try {
      // Attempt to refresh the token
      const newToken = await userStore.refreshToken();
      
      // If we get here, the refresh was successful
      processQueue(null, newToken);
      
      // Update the authorization header and retry the original request
      originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
      return axios(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError, null);
      userStore.removeToken();
      alert('Your session has expired. Please log in again.');
      router.push('/admin/login/2015');
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

app.mount('#app');
