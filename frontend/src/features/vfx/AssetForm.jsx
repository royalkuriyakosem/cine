import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { FileUpload } from '../../components/ui/FileUpload';

const AssetForm = ({ onSave, onClose }) => {
    const [name, setName] = useState('');
    const [file, setFile] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name || !file) return;
        const formData = new FormData();
        formData.append('name', name);
        formData.append('file', file);
        onSave(formData);
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <h3 className="text-lg font-bold">Upload Asset</h3>
                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Asset Name" className="w-full p-2 border rounded" required />
                <FileUpload onFileSelect={setFile} />
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Upload</Button>
                </div>
            </form>
        </Modal>
    );
};

export default AssetForm;