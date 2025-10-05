import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';

const CallSheetForm = ({ onSave, onClose }) => {
    const [formData, setFormData] = useState({
        date: '',
        scenes: '', // User will enter comma-separated scene numbers
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Convert scene string to array of numbers
        const scenesArray = formData.scenes.split(',').map(s => parseInt(s.trim(), 10)).filter(Boolean);
        onSave({ date: formData.date, scenes: scenesArray });
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <h3 className="text-lg font-bold">Add Call Sheet</h3>
                <input name="date" type="date" value={formData.date} onChange={handleChange} className="w-full p-2 border rounded" required />
                <textarea name="scenes" value={formData.scenes} onChange={handleChange} placeholder="Scene numbers, separated by commas (e.g., 1, 2, 5)" className="w-full p-2 border rounded" />
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default CallSheetForm;