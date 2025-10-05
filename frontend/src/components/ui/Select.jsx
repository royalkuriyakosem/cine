import React from 'react';

export const Select = ({ children, value, onChange, name }) => (
    <select
        name={name}
        value={value}
        onChange={onChange}
        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
    >
        {children}
    </select>
);