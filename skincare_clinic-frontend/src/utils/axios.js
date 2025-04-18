// axios.js
import axios from 'axios';
import { useUserStore } from '@/stores/user';

// Create a custom Axios instance
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',  // Base URL for all requests
});

// Request interceptor: Attach the access token to every request
api.interceptors.request.use((config) => {
    const authStore = useUserStore();
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
});

// Response interceptor: Handle token expiration
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useUserStore();
        if (error.response.status === 401 && authStore.accessToken) {
            // Refresh the access token if it's expired
            await authStore.refreshAccessToken();
            // Retry the original request
            return api(error.config);
        }
        return Promise.reject(error);
    }
);

export default api;  // Export the configured Axios instance