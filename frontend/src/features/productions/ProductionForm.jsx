import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';

const ProductionForm = ({ onSave, onClose, item }) => {
    const [formData, setFormData] = useState({
        title: item?.title || '',
        description: item?.description || '',
        start_date: item?.start_date || '',
        end_date: item?.end_date || '',
        status: item?.status || 'pre',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Simple slug generation
        const slug = formData.title.toLowerCase().replace(/\s+/g, '-').slice(0, 50);
        onSave({ ...formData, slug });
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <h3 className="text-lg font-bold">{item ? 'Edit' : 'Add'} Production</h3>
                <input name="title" value={formData.title} onChange={handleChange} placeholder="Title" className="w-full p-2 border rounded" required />
                <textarea name="description" value={formData.description} onChange={handleChange} placeholder="Description" className="w-full p-2 border rounded" />
                <input name="start_date" type="date" value={formData.start_date} onChange={handleChange} className="w-full p-2 border rounded" required />
                <input name="end_date" type="date" value={formData.end_date} onChange={handleChange} className="w-full p-2 border rounded" />
                <select name="status" value={formData.status} onChange={handleChange} className="w-full p-2 border rounded">
                    <option value="pre">Pre-production</option>
                    <option value="shooting">Shooting</option>
                    <option value="post">Post-production</option>
                    <option value="completed">Completed</option>
                </select>
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default ProductionForm;