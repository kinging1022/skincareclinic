import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'
import App from './App.vue'
import router from './router'
import VueConfetti from 'vue-confetti';


import axios from 'axios'

axios.defaults.baseURL = "http://127.0.0.1:8000";


const app = createApp(App)

app.use(createPinia())
app.use(VueConfetti);
app.use(router,axios)

// Initialize the store
const userStore = useUserStore(); 

// Request interceptor -
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
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          await userStore.refreshToken();
          originalRequest.headers['Authorization'] = `Bearer ${userStore.access}`;
          return axios(originalRequest);
        } catch (error) {
          userStore.removeToken();
          alert('Your session has expired. Please log in again.');
          router.push('/admin/login');
        }
      }
      return Promise.reject(error);
    }
  );


app.mount('#app')
