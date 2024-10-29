import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from 'axios';

axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Redirect to login page or refresh token
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

createApp(App).use(router).mount("#app");
