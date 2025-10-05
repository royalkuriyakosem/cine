import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import MainLayout from './components/layout/MainLayout';
import PreProduction from './pages/PreProduction';
import { ProductionProvider } from './context/ProductionContext';
import Production from './pages/Production';
import PostProduction from './pages/PostProduction';

const App = () => {
    return (
        <AuthProvider>
            <ProductionProvider>
                <BrowserRouter>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/unauthorized" element={<h1>403 - Unauthorized</h1>} />

                        {/* Main application routes with layout */}
                        <Route 
                            path="/*"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Routes>
                                            <Route path="/admin" element={<ProtectedRoute allowedRoles={['ADMIN']}><AdminDashboard /></ProtectedRoute>} />
                                            <Route path="/pre-production" element={<PreProduction />} />
                                            <Route path="/production" element={<Production />} />
                                            <Route path="/post-production" element={<PostProduction />} />
                                            <Route path="/" element={<Navigate to="/pre-production" />} />
                                        </Routes>
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                    </Routes>
                </BrowserRouter>
            </ProductionProvider>
        </AuthProvider>
    );
};

export default App;