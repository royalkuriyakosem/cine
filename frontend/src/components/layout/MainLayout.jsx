import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';

const MainLayout = ({ children }) => {
    return (
        <div className="flex h-screen bg-gray-100">
            <Sidebar />
            <div className="flex-1 flex flex-col overflow-hidden">
                <Header />
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-4 md:p-8">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default MainLayout;