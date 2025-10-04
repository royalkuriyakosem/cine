import React from 'react';

export const Button = ({ children, onClick, disabled, size = 'md' }) => {
    const sizeClasses = {
        sm: 'px-2 py-1 text-xs',
        md: 'px-4 py-2 text-sm',
    };
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring transition-colors duration-200 ${sizeClasses[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
            {children}
        </button>
    );
};