import React, { useState, useEffect, useMemo } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { Modal } from '../../components/ui/Modal';
import ProtectedRoute from '../../components/ProtectedRoute';
import { getBudgetLines, addBudgetLine, updateBudgetLine, deleteBudgetLine, generatePrediction } from '../../api/productions';

const BudgetManager = ({ productionId }) => {
    const [lines, setLines] = useState([]);
    const [prediction, setPrediction] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentItem, setCurrentItem] = useState(null);

    const fetchBudgetLines = async () => {
        try {
            setIsLoading(true);
            const data = await getBudgetLines(productionId);
            setLines(data);
        } catch (err) {
            setError('Failed to load budget data.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (productionId) {
            fetchBudgetLines();
        }
    }, [productionId]);

    const handleGeneratePrediction = async () => {
        try {
            const data = await generatePrediction(productionId);
            setPrediction(data);
        } catch (err) {
            setError('Could not generate prediction.');
        }
    };

    const handleOpenModal = (item = null) => {
        setCurrentItem(item);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setCurrentItem(null);
    };

    const handleSave = async (formData) => {
        const data = { ...formData, production: productionId };
        if (currentItem) {
            await updateBudgetLine(currentItem.id, data);
        } else {
            await addBudgetLine(data);
        }
        fetchBudgetLines(); // Refresh data
        handleCloseModal();
    };
    
    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this line item?')) {
            await deleteBudgetLine(id);
            fetchBudgetLines(); // Refresh data
        }
    };

    const summary = useMemo(() => {
        const estimated = lines.reduce((sum, line) => sum + parseFloat(line.estimated_amount || 0), 0);
        const actual = lines.reduce((sum, line) => sum + parseFloat(line.actual_amount || 0), 0);
        return { estimated, actual, variance: actual - estimated };
    }, [lines]);

    if (isLoading) return <Spinner />;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <Card>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-800">Budget Manager</h3>
                <ProtectedRoute allowedRoles={['PRODUCER', 'ADMIN']}>
                    <div className="space-x-2">
                        <Button onClick={() => handleOpenModal()}>Add Line Item</Button>
                        <Button onClick={handleGeneratePrediction}>Generate Prediction</Button>
                    </div>
                </ProtectedRoute>
            </div>

            {prediction && (
                <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg mb-6">
                    <h4 className="font-bold text-blue-800">Automated Budget Prediction</h4>
                    <p className="text-2xl font-semibold text-blue-900">${parseFloat(prediction.predicted_total).toLocaleString()}</p>
                    <p className="text-xs text-blue-600">{prediction.details.reasoning}</p>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 text-center">
                <div className="bg-gray-100 p-4 rounded-lg">
                    <h4 className="text-sm font-semibold text-gray-600">Total Estimated</h4>
                    <p className="text-2xl font-bold text-gray-800">${summary.estimated.toLocaleString()}</p>
                </div>
                <div className="bg-gray-100 p-4 rounded-lg">
                    <h4 className="text-sm font-semibold text-gray-600">Total Actual</h4>
                    <p className="text-2xl font-bold text-gray-800">${summary.actual.toLocaleString()}</p>
                </div>
                <div className={`p-4 rounded-lg ${summary.variance > 0 ? 'bg-red-100' : 'bg-green-100'}`}>
                    <h4 className={`text-sm font-semibold ${summary.variance > 0 ? 'text-red-600' : 'text-green-600'}`}>Variance</h4>
                    <p className={`text-2xl font-bold ${summary.variance > 0 ? 'text-red-800' : 'text-green-800'}`}>
                        {summary.variance < 0 ? '-' : ''}${Math.abs(summary.variance).toLocaleString()}
                    </p>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border">
                    <thead className="bg-gray-200">
                        <tr>
                            <th className="py-2 px-4 border-b">Category</th>
                            <th className="py-2 px-4 border-b">Vendor</th>
                            <th className="py-2 px-4 border-b text-right">Estimated</th>
                            <th className="py-2 px-4 border-b text-right">Actual</th>
                            <th className="py-2 px-4 border-b">Approved</th>
                            <th className="py-2 px-4 border-b">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lines.map(line => (
                            <tr key={line.id}>
                                <td className="py-2 px-4 border-b">{line.category}</td>
                                <td className="py-2 px-4 border-b">{line.vendor || 'N/A'}</td>
                                <td className="py-2 px-4 border-b text-right">${parseFloat(line.estimated_amount).toLocaleString()}</td>
                                <td className="py-2 px-4 border-b text-right">{line.actual_amount ? `$${parseFloat(line.actual_amount).toLocaleString()}` : '-'}</td>
                                <td className="py-2 px-4 border-b">{line.approved ? 'Yes' : 'No'}</td>
                                <td className="py-2 px-4 border-b">
                                    <ProtectedRoute allowedRoles={['PRODUCER', 'ADMIN']}>
                                        <div className="space-x-2">
                                            <Button size="sm" onClick={() => handleOpenModal(line)}>Edit</Button>
                                            <Button size="sm" onClick={() => handleDelete(line.id)}>Delete</Button>
                                        </div>
                                    </ProtectedRoute>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {isModalOpen && (
                <BudgetFormModal
                    item={currentItem}
                    onClose={handleCloseModal}
                    onSave={handleSave}
                />
            )}
        </Card>
    );
};

const BudgetFormModal = ({ item, onClose, onSave }) => {
    const [formData, setFormData] = useState({
        category: item?.category || '',
        vendor: item?.vendor || '',
        estimated_amount: item?.estimated_amount || '',
        actual_amount: item?.actual_amount || '',
        approved: item?.approved || false,
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(formData);
    };

    return (
        <Modal isOpen={true} onClose={onClose}>
            <form onSubmit={handleSubmit}>
                <h3 className="text-lg font-bold mb-4">{item ? 'Edit' : 'Add'} Budget Line</h3>
                <div className="space-y-4">
                    <input name="category" value={formData.category} onChange={handleChange} placeholder="Category" className="w-full p-2 border rounded" required />
                    <input name="vendor" value={formData.vendor} onChange={handleChange} placeholder="Vendor" className="w-full p-2 border rounded" />
                    <input name="estimated_amount" type="number" value={formData.estimated_amount} onChange={handleChange} placeholder="Estimated Amount" className="w-full p-2 border rounded" required />
                    <input name="actual_amount" type="number" value={formData.actual_amount} onChange={handleChange} placeholder="Actual Amount" className="w-full p-2 border rounded" />
                    <label className="flex items-center">
                        <input name="approved" type="checkbox" checked={formData.approved} onChange={handleChange} className="mr-2" />
                        Approved
                    </label>
                </div>
                <div className="mt-6 flex justify-end space-x-2">
                    <Button onClick={onClose}>Cancel</Button>
                    <Button type="submit">Save</Button>
                </div>
            </form>
        </Modal>
    );
};

export default BudgetManager;