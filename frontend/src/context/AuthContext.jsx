import React, { createContext, useState, useContext, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api/axiosConfig';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        // On initial load, check for token and set user state
        const token = localStorage.getItem('accessToken');
        if (token) {
            try {
                const decodedUser = jwtDecode(token);
                // You might need to fetch full user details here
                // For now, we'll use the decoded token payload
                setUser({ ...decodedUser, role: decodedUser.role }); // Use role from token
            } catch (error) {
                console.error("Invalid token:", error);
                localStorage.removeItem('accessToken');
            }
        }
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post('/accounts/token/', { username, password });
            const { access, refresh } = response.data;
            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);
            const decodedUser = jwtDecode(access);
            // This is a simplified user object. You might want to fetch more details.
            // The role should come from your backend's JWT payload.
            // I'm adding a placeholder role here for demonstration.
            const userRole = decodedUser.role || 'CREW'; // Default to CREW if not present
            setUser({ ...decodedUser, role: userRole });
            return { success: true, role: userRole };
        } catch (error) {
            console.error("Login failed:", error);
            return { success: false, error };
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};