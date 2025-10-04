import React from 'react';

export const FileUpload = ({ onFileSelect, accept }) => {
    const handleFileChange = (e) => {
        if (e.target.files) {
            onFileSelect(e.target.files[0]);
        }
    };
    return (
        <input
            type="file"
            accept={accept}
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
    );
};