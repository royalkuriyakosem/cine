import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const { user } = useAuth();
    const location = useLocation();

    if (!user) {
        // User not logged in, redirect to login page
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (allowedRoles && !allowedRoles.includes(user.role)) {
        // User does not have the required role, redirect to an unauthorized page or home
        return <Navigate to="/unauthorized" replace />;
    }

    return children;
};

export default ProtectedRoute;