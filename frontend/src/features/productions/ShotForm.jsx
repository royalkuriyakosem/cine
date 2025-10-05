import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';

const ShotForm = ({ onSave, onClose, item }) => {
    const [formData, setFormData] = useState({
        shot_number: item?.shot_number || '',
        description: item?.description || '',
        status: item?.status || 'todo',
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
                <h3 className="text-lg font-bold">{item ? 'Edit' : 'Add'} Shot</h3>
                <input name="shot_number" type="number" value={formData.shot_number} onChange={handleChange} placeholder="Shot Number" className="w-full p-2 border rounded" required />
                <textarea name="description" value={formData.description} onChange={handleChange} placeholder="Description (e.g., Wide shot of the city)" className="w-full p-2 border rounded" />
                <select name="status" value={formData.status} onChange={handleChange} className="w-full p-2 border rounded">
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                </select>
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default ShotForm;