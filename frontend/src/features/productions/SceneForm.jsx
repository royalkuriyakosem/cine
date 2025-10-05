import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';

const SceneForm = ({ onSave, onClose, item }) => {
    const [formData, setFormData] = useState({
        number: item?.number || '',
        title: item?.title || '',
        location: item?.location || '',
        pages: item?.pages || '',
        estimated_cost: item?.estimated_cost || '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(formData);
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <h3 className="text-lg font-bold">{item ? 'Edit' : 'Add'} Scene</h3>
                <input name="number" type="number" value={formData.number} onChange={handleChange} placeholder="Scene Number" className="w-full p-2 border rounded" required />
                <input name="title" value={formData.title} onChange={handleChange} placeholder="Title (e.g., The Escape)" className="w-full p-2 border rounded" required />
                <input name="location" value={formData.location} onChange={handleChange} placeholder="Location (e.g., INT. WAREHOUSE - NIGHT)" className="w-full p-2 border rounded" required />
                <input name="pages" type="number" step="0.01" value={formData.pages} onChange={handleChange} placeholder="Pages (e.g., 2.5)" className="w-full p-2 border rounded" required />
                <input name="estimated_cost" type="number" step="0.01" value={formData.estimated_cost} onChange={handleChange} placeholder="Estimated Cost" className="w-full p-2 border rounded" required />
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default SceneForm;