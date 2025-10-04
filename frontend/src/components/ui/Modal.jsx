import React from 'react';

export const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center" onClick={onClose}>
            <div className="bg-white rounded-lg shadow-xl p-8 max-w-lg w-full" onClick={e => e.stopPropagation()}>
                {children}
                <button onClick={onClose} className="absolute top-2 right-2 text-gray-600 hover:text-gray-900">&times;</button>
            </div>
        </div>
    );
};