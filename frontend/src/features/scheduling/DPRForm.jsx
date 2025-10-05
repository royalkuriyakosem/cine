import React, { useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';

const DPRForm = ({ onSave, onClose }) => {
    const [formData, setFormData] = useState({
        dpr_date: '',
        scenes_completed_list: '', // User will enter comma-separated scene numbers
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const scenesArray = formData.scenes_completed_list.split(',').map(s => s.trim()).filter(Boolean);
        onSave({ dpr_date: formData.dpr_date, scenes_completed_list: scenesArray });
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4">
                <h3 className="text-lg font-bold">Add Daily Production Report</h3>
                <input name="dpr_date" type="date" value={formData.dpr_date} onChange={handleChange} className="w-full p-2 border rounded" required />
                <textarea name="scenes_completed_list" value={formData.scenes_completed_list} onChange={handleChange} placeholder="Completed scene numbers, separated by commas" className="w-full p-2 border rounded" />
                <div className="flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default DPRForm;