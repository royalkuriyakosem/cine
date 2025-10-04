import React from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';

// Placeholder Dashboard Components
const ProducerDashboard = () => <h2>Producer Dashboard</h2>;
const DirectorDashboard = () => <h2>Director Dashboard</h2>;
const CrewDashboard = () => <h2>Crew Dashboard</h2>;
const Unauthorized = () => <h1>403 - Unauthorized</h1>;

const App = () => {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Nav />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/unauthorized" element={<Unauthorized />} />

                    {/* Admin Dashboard */}
                    <Route
                        path="/admin-dashboard"
                        element={
                            <ProtectedRoute allowedRoles={['ADMIN']}>
                                <AdminDashboard />
                            </ProtectedRoute>
                        }
                    />

                    {/* Producer Dashboard */}
                    <Route
                        path="/producer-dashboard"
                        element={
                            <ProtectedRoute allowedRoles={['PRODUCER', 'ADMIN']}>
                                <ProducerDashboard />
                            </ProtectedRoute>
                        }
                    />

                    {/* Director Dashboard */}
                    <Route
                        path="/director-dashboard"
                        element={
                            <ProtectedRoute allowedRoles={['DIRECTOR', 'ADMIN']}>
                                <DirectorDashboard />
                            </ProtectedRoute>
                        }
                    />

                    {/* General Crew Dashboard */}
                    <Route
                        path="/crew-dashboard"
                        element={
                            <ProtectedRoute allowedRoles={['CREW', 'PRODUCER', 'DIRECTOR', 'ADMIN']}>
                                <CrewDashboard />
                            </ProtectedRoute>
                        }
                    />
                    
                    <Route path="/" element={<Navigate to="/crew-dashboard" />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
};

// Simple navigation component for demonstration
const Nav = () => {
    const { user, logout } = useAuth();
    return (
        <nav>
            {user?.role === 'ADMIN' && (
                <>
                    <Link to="/admin-dashboard">Admin</Link> |{" "}
                </>
            )}
            <Link to="/producer-dashboard">Producer</Link> |{" "}
            <Link to="/director-dashboard">Director</Link> |{" "}
            <Link to="/crew-dashboard">Crew</Link>
            {user && <button onClick={logout}>Logout</button>}
        </nav>
    );
};

export default App;