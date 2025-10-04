import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const api = axios.create({
    baseURL: '/api'
});

api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refreshToken');
            if (refreshToken) {
                try {
                    const response = await axios.post('/api/accounts/token/refresh/', {
                        refresh: refreshToken
                    });
                    const { access } = response.data;
                    localStorage.setItem('accessToken', access);
                    api.defaults.headers.common['Authorization'] = 'Bearer ' + access;
                    originalRequest.headers['Authorization'] = 'Bearer ' + access;
                    return api(originalRequest);
                } catch (refreshError) {
                    // On refresh failure, clear tokens and redirect to login
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;