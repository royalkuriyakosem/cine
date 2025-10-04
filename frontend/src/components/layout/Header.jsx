import React from 'react';
import { useAuth } from '../../context/AuthContext';

const Header = () => {
    const { user, logout } = useAuth();

    return (
        <header className="flex items-center justify-between px-6 py-4 bg-white border-b-2 border-gray-200">
            <div className="flex items-center">
                {/* Mobile sidebar toggle can be added here */}
                <h2 className="text-xl font-semibold text-gray-800">Dashboard</h2>
            </div>
            <div className="flex items-center">
                <div className="relative">
                    <span className="mr-4 font-medium text-gray-700">{user?.username} ({user?.role})</span>
                    <button
                        onClick={logout}
                        className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring"
                    >
                        Logout
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;