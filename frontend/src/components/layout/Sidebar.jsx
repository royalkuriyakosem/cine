import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
    const { user } = useAuth();
    const navLinkClasses = ({ isActive }) =>
        `flex items-center px-4 py-2 mt-2 text-gray-100 transition-colors duration-200 transform rounded-md hover:bg-gray-700 ${
            isActive ? 'bg-gray-700' : ''
        }`;

    return (
        <div className="hidden md:flex flex-col w-64 bg-gray-800">
            <div className="flex items-center justify-center h-16 bg-gray-900">
                <span className="text-white font-bold uppercase">FilmHub</span>
            </div>
            <div className="flex flex-col flex-1 overflow-y-auto">
                <nav className="flex-1 px-2 py-4 bg-gray-800">
                    <NavLink to="/pre-production" className={navLinkClasses}>
                        Pre-Production
                    </NavLink>
                    <NavLink to="/production" className={navLinkClasses}>
                        Production
                    </NavLink>
                    <NavLink to="/post-production" className={navLinkClasses}>
                        Post-Production
                    </NavLink>
                    {user?.role === 'ADMIN' && (
                         <NavLink to="/admin" className={navLinkClasses}>
                            Admin Dashboard
                        </NavLink>
                    )}
                </nav>
            </div>
        </div>
    );
};

export default Sidebar;